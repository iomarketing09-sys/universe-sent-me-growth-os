"""Plan de cambios para campañas de Ads, sin ejecutar ninguna escritura.

El optimizador convierte un reporte de métricas en recomendaciones auditables.
No contiene llamadas de escritura a Meta y siempre marca el plan como
``recommendation_only``. La ejecución requerirá una capacidad separada de CGO y
aprobación explícita.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


PLAN_SCHEMA_VERSION = "1.0"
MODE = "recommendation_only"

DEFAULT_POLICY = {
    "target_cpa_mxn": 8.0,
    "pause_after_hours": 72,
    "min_spend_for_decision_mxn": 60.0,
    "min_conversations_for_decision": 3,
    "scale_cpa_mxn": 5.6,
    "min_conversations_to_scale": 5,
    "min_impressions_for_ctr": 1000,
    "min_ctr_percent": 1.0,
}


def load_policy(tenant_dir: Optional[Path] = None) -> Dict:
    """Carga ``ads/campaign_policy.json`` y completa los valores faltantes."""
    policy = dict(DEFAULT_POLICY)
    if tenant_dir is None:
        return policy
    path = Path(tenant_dir) / "ads" / "campaign_policy.json"
    if not path.is_file():
        return policy
    try:
        override = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return policy
    if isinstance(override, dict):
        policy.update({key: value for key, value in override.items() if key in DEFAULT_POLICY})
    return policy


def plan_dir(
    tenant_id: str,
    campaign_slug: str,
    base_path: Optional[Path] = None,
) -> Path:
    """Directorio versionable de planes; separado de las capturas operativas."""
    root = Path(base_path) if base_path else Path(__file__).resolve().parents[2]
    return root / "tenants" / tenant_id / "ads" / "plans" / campaign_slug


def plan_paths(
    tenant_id: str,
    campaign_slug: str,
    checkpoint: str,
    base_path: Optional[Path] = None,
) -> tuple[Path, Path]:
    base = plan_dir(tenant_id, campaign_slug, base_path)
    return base / f"{checkpoint}.json", base / f"{checkpoint}.md"


def _evidence(ad: Dict) -> Dict:
    return {
        "spend_mxn": ad.get("spend", 0.0),
        "impressions": ad.get("impressions", 0),
        "clicks": ad.get("clicks", 0),
        "ctr_percent": ad.get("ctr", 0.0),
        "conversations": ad.get("conversations", 0),
        "cost_per_conversation_mxn": ad.get("cost_per_conversation", 0.0),
    }


def _ad_action(ad: Dict, elapsed_hours: float, policy: Dict) -> Dict:
    spend = float(ad.get("spend") or 0)
    conversations = int(ad.get("conversations") or 0)
    cpa = float(ad.get("cost_per_conversation") or 0)
    ctr = float(ad.get("ctr") or 0)
    impressions = int(ad.get("impressions") or 0)
    target = float(policy["target_cpa_mxn"])
    pause_after = float(policy["pause_after_hours"])
    min_spend = float(policy["min_spend_for_decision_mxn"])
    min_conversations = int(policy["min_conversations_for_decision"])

    base = {
        "target_type": "ad",
        "target_id": ad.get("ad_id", ""),
        "target_name": ad.get("ad_name", ""),
        "evidence": _evidence(ad),
        "approval_required": True,
        "status": "proposed",
        "writes_to_meta": False,
    }

    bad_cpa = conversations >= min_conversations and cpa > target and spend >= min_spend
    no_conversations = conversations == 0 and spend >= min_spend

    if bad_cpa or no_conversations:
        if elapsed_hours >= pause_after:
            reason = (
                "CPA por encima del objetivo con muestra suficiente."
                if bad_cpa
                else "Gasto suficiente sin conversaciones."
            )
            return {
                **base,
                "action": "pause_ad",
                "priority": "high",
                "reason": reason,
                "preconditions": [
                    "Aprobación humana explícita",
                    "Confirmar que no hay un problema temporal de atribución",
                    "Pausar el anuncio, no la campaña",
                ],
            }
        return {
            **base,
            "action": "watch",
            "priority": "high" if no_conversations else "medium",
            "reason": (
                "Señal negativa, pero todavía no se cumple la ventana mínima de pausa."
            ),
            "preconditions": [
                f"Reevaluar a las {pause_after:.0f} h antes de proponer pausa",
                "No pausar automáticamente en E48",
            ],
            "recheck_after_hours": max(0, pause_after - elapsed_hours),
        }

    if spend >= min_spend and 0 < conversations < min_conversations:
        return {
            **base,
            "action": "watch",
            "priority": "medium",
            "reason": "Hay gasto, pero aún no hay conversaciones suficientes para juzgar el CPA.",
            "preconditions": [
                "Seguir midiendo antes de proponer pausa",
                "No pausar por una muestra de una o dos conversaciones",
            ],
            "recheck_after_hours": max(0, pause_after - elapsed_hours),
        }

    scale_cpa = float(policy["scale_cpa_mxn"])
    min_scale_conversations = int(policy["min_conversations_to_scale"])
    if conversations >= min_scale_conversations and cpa <= scale_cpa:
        return {
            **base,
            "action": "scale_candidate",
            "priority": "medium",
            "reason": "CPA por debajo del umbral de escala con muestra suficiente.",
            "preconditions": [
                "Revisión humana de capacidad y margen",
                "No aumentar presupuesto automáticamente",
            ],
        }

    if (
        impressions >= int(policy["min_impressions_for_ctr"])
        and ctr < float(policy["min_ctr_percent"])
    ):
        return {
            **base,
            "action": "rotate_creative",
            "priority": "medium",
            "reason": "CTR bajo con impresiones suficientes para evaluar el creativo.",
            "preconditions": [
                "Generar una variante nueva",
                "Validar marca y claims antes de publicar",
            ],
        }

    return {
        **base,
        "action": "keep",
        "priority": "low",
        "reason": "Sin señal suficiente para proponer un cambio.",
        "preconditions": ["Mantener y seguir midiendo"],
    }


def build_change_plan(
    report: Dict,
    *,
    tenant_id: str,
    campaign_id: str,
    campaign_slug: str,
    campaign_name: str,
    elapsed_hours: float,
    capture_elapsed_hours: Optional[float] = None,
    scheduled_for: Optional[str] = None,
    generated_at: Optional[datetime] = None,
    checkpoint: str = "LATEST",
    policy: Optional[Dict] = None,
    metadata_reconciliation: Optional[Dict] = None,
) -> Dict:
    """Genera recomendaciones; nunca aplica cambios.

    ``elapsed_hours`` es la antigüedad programada del corte y es la que gobierna
    la decisión. ``capture_elapsed_hours`` solo documenta cuánto había pasado al
    capturar, para que un E48 atrasado no se convierta en una pausa E72.
    """
    current = generated_at or datetime.now(timezone.utc)
    effective_policy = dict(DEFAULT_POLICY)
    if policy:
        effective_policy.update(policy)

    actions = [
        _ad_action(ad, elapsed_hours, effective_policy) for ad in report.get("ads") or []
    ]
    counts = {
        action: sum(1 for item in actions if item["action"] == action)
        for action in ("pause_ad", "watch", "scale_candidate", "rotate_creative", "keep")
    }

    warnings: List[str] = []
    if not actions:
        warnings.append("Sin datos de anuncios; no hay una base para recomendar cambios.")
    if elapsed_hours < 24:
        warnings.append("Muestra inmadura: no se recomienda cambiar la campaña antes de E24.")
    if capture_elapsed_hours is not None and capture_elapsed_hours >= elapsed_hours + 1:
        warnings.append(
            "Captura tardía: la decisión usa la antigüedad programada del corte "
            f"({elapsed_hours:.1f} h), no la antigüedad real de la captura "
            f"({capture_elapsed_hours:.1f} h)."
        )
    if counts["pause_ad"]:
        warnings.append(
            "Hay candidatos a pausa, pero CGO debe exigir aprobación humana antes de escribir en Meta."
        )
    execution_blocked = bool(
        metadata_reconciliation and metadata_reconciliation.get("execution_blocked")
    )
    execution_blockers = list(
        (metadata_reconciliation or {}).get("execution_blockers") or []
    )
    if execution_blocked:
        warnings.append(
            "Ejecución bloqueada por IDs inconsistentes; la recomendación se genera, "
            "pero no debe aplicarse hasta reconciliar la metadata local."
        )

    if counts["pause_ad"]:
        campaign_recommendation = (
            "Revisar pausas individuales; no pausar la campaña completa ni redistribuir "
            "presupuesto sin aprobación."
        )
    elif counts["scale_candidate"]:
        campaign_recommendation = (
            "Mantener la campaña y revisar capacidad/margen antes de considerar escala."
        )
    elif counts["watch"]:
        campaign_recommendation = "Mantener y reevaluar en el siguiente corte."
    else:
        campaign_recommendation = "Mantener sin cambios; las métricas no justifican una acción."

    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "mode": MODE,
        "execution_allowed": False,
        "approval_required": True,
        "writes_to_meta": False,
        "execution_blocked": execution_blocked,
        "execution_blockers": execution_blockers,
        "tenant_id": tenant_id,
        "campaign_id": campaign_id,
        "campaign_slug": campaign_slug,
        "campaign_name": campaign_name,
        "checkpoint": checkpoint,
        "generated_at": current.isoformat(),
        "elapsed_hours": round(elapsed_hours, 2),
        "capture_elapsed_hours": (
            round(capture_elapsed_hours, 2) if capture_elapsed_hours is not None else None
        ),
        "scheduled_for": scheduled_for,
        "policy": effective_policy,
        "metadata_reconciliation": metadata_reconciliation or {"status": "not_checked"},
        "summary": {
            "campaign_recommendation": campaign_recommendation,
            "counts": counts,
            "total_spend_mxn": report.get("total_spend", 0.0),
            "total_conversations": report.get("total_conversations", 0),
            "blended_cost_per_conversation_mxn": report.get(
                "blended_cost_per_conversation", 0.0
            ),
        },
        "actions": actions,
        "warnings": warnings,
        "approval": {
            "status": "blocked" if execution_blocked else "pending",
            "approver_role": "Fernando / CGO",
            "note": (
                "La ejecución está bloqueada hasta reconciliar la metadata."
                if execution_blocked
                else "El plan no puede ejecutarse por sí mismo."
            ),
        },
        "next_steps": [
            "Revisar este plan con CGO/Fernando",
            "No ejecutar ninguna acción desde el plan",
            "Si se aprueba, crear un plan de ejecución separado con auditoría",
        ],
    }


def render_plan_markdown(plan: Dict) -> str:
    counts = plan["summary"]["counts"]
    lines = [
        f"# Plan de cambios {plan['checkpoint']} — {plan['campaign_slug']}",
        "",
        "> **Modo recomendación.** Este plan no envía cambios a Meta.",
        "",
        f"- **Campaña:** `{plan['campaign_id']}`",
        f"- **Generado:** {plan['generated_at']}",
        f"- **Antigüedad usada para decidir:** {plan['elapsed_hours']:.1f} h",
        f"- **Corte programado:** {plan.get('scheduled_for') or 'no registrado'}",
        f"- **Recomendación de campaña:** {plan['summary']['campaign_recommendation']}",
        f"- **Gasto:** ${plan['summary']['total_spend_mxn']:,.2f} MXN",
        f"- **Conversaciones:** {plan['summary']['total_conversations']}",
        f"- **CPA mezclado:** ${plan['summary']['blended_cost_per_conversation_mxn']:,.2f} MXN",
        "",
        "| Anuncio | Acción propuesta | Prioridad | CPA | Conversaciones | Motivo |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for action in plan["actions"]:
        evidence = action["evidence"]
        lines.append(
            f"| {action['target_name']} | `{action['action']}` | {action['priority']} | "
            f"${evidence['cost_per_conversation_mxn']:,.2f} | "
            f"{evidence['conversations']} | {action['reason']} |"
        )
    if not plan["actions"]:
        lines.append("| Sin datos | `keep` | low | $0.00 | 0 | Sin base para recomendar |")

    lines.extend(
        [
            "",
            f"**Conteo:** pausa={counts['pause_ad']}, watch={counts['watch']}, "
            f"escala={counts['scale_candidate']}, rotar={counts['rotate_creative']}, "
            f"mantener={counts['keep']}.",
            "",
            "## Condiciones de ejecución",
            "",
            "- Toda acción requiere aprobación humana explícita.",
            "- La ejecución, cuando exista, irá por una capacidad separada de CGO.",
            "- No se pausa la campaña completa; se pausan anuncios individuales.",
            "- No se modifica presupuesto desde este plan.",
        ]
    )
    if plan["warnings"]:
        lines.extend(["", "## Advertencias", ""])
        lines.extend(f"- {warning}" for warning in plan["warnings"])
    if plan.get("execution_blockers"):
        lines.extend(["", "## Bloqueos de ejecución", ""])
        lines.extend(f"- {blocker}" for blocker in plan["execution_blockers"])
    return "\n".join(lines) + "\n"
