"""Diagnóstico de ecos (``smb_message_echoes``) del webhook de WhatsApp.

Responde una sola pregunta: ¿estamos viendo lo que la sucursal contesta desde la
app del celular? Mezcla dos fuentes de solo lectura:

1. D1 del worker (eventos guardados y payloads crudos).
2. Graph API (apps suscritas al WABA), para saber si Meta nos está enviando
   ``message_echoes``.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from modules.communications.whatsapp import d1, graph


@dataclass
class EchoDiagnosis:
    tenant_id: str
    direction_counts: Dict[str, int] = field(default_factory=dict)
    status_counts: Dict[str, int] = field(default_factory=dict)
    payload_keys: Dict[str, int] = field(default_factory=dict)
    echoes_stored: int = 0
    payloads_with_echoes: int = 0
    connected_apps_count: int = 0
    connected_apps: List[Dict[str, Any]] = field(default_factory=list)
    subscription_check_error: Optional[str] = None
    outcome: str = "unknown"
    findings: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "direction_counts": self.direction_counts,
            "status_counts": self.status_counts,
            "payload_keys": self.payload_keys,
            "echoes_stored": self.echoes_stored,
            "payloads_with_echoes": self.payloads_with_echoes,
            "connected_apps_count": self.connected_apps_count,
            "connected_apps": self.connected_apps,
            "subscription_check_error": self.subscription_check_error,
            "outcome": self.outcome,
            "findings": self.findings,
            "next_actions": self.next_actions,
            "errors": self.errors,
        }


def _tenant_whatsapp_config(tenant_id: str, base_path: Optional[str]) -> Dict[str, Any]:
    from modules.communications.whatsapp.env import project_root

    root = project_root() if not base_path else None
    path = (root / "tenants" / tenant_id / "whatsapp" / "config.json") if root else None
    if path and path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _tenant_meta(tenant_id: str) -> Dict[str, Any]:
    from modules.communications.whatsapp.env import project_root

    path = project_root() / "tenants" / tenant_id / "config.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8")).get("meta", {}) or {}
    return {}


def _connected_apps(waba_id: str, page_id: str) -> tuple[List[Dict[str, Any]], Optional[str]]:
    if not waba_id or not page_id:
        return [], "Falta waba_id o page_id en la configuración del tenant."
    user_token = graph._load_user_token()
    if not user_token:
        return [], "No hay META_ACCESS_TOKEN disponible."
    page_token = graph.get_page_token(user_token, page_id)
    if not page_token:
        return [], "No se pudo obtener token de página."

    url = f"{graph.GRAPH_BASE}/{waba_id}/subscribed_apps"
    try:
        response = requests.get(url, params={"access_token": page_token}, timeout=30)
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        return [], f"No se pudo consultar subscribed_apps: {exc}"
    if response.status_code >= 400 or payload.get("error"):
        error = (payload.get("error") or {}).get("message") or f"HTTP {response.status_code}"
        return [], f"Graph rechazó subscribed_apps: {error}"
    return list(payload.get("data") or []), None


def _payload_stats(tenant_id: str, base_path: Optional[str], limit: int = 300):
    keys: Counter = Counter()
    with_echoes = 0
    rows = d1.query(
        "SELECT payload FROM raw_events ORDER BY id DESC LIMIT ?",
        params=[limit],
        tenant_id=tenant_id,
        base_path=base_path,
    )
    for row in rows:
        try:
            payload = json.loads(row.get("payload") or "{}")
        except (TypeError, ValueError):
            continue
        for entry in payload.get("entry") or []:
            for change in entry.get("changes") or []:
                value = change.get("value") or {}
                keys.update(value.keys())
                if value.get("smb_message_echoes") or value.get("message_echoes"):
                    with_echoes += 1
    return dict(keys.most_common()), with_echoes


def diagnose_echoes(
    tenant_id: str = "flexi",
    base_path: Optional[str] = None,
    check_graph: bool = True,
) -> EchoDiagnosis:
    """Diagnóstico completo; devuelve un objeto con ``to_dict()``."""
    result = EchoDiagnosis(tenant_id=tenant_id)

    try:
        for row in d1.query(
            "SELECT direction, COUNT(*) AS n FROM events GROUP BY direction",
            tenant_id=tenant_id,
            base_path=base_path,
        ):
            result.direction_counts[str(row.get("direction"))] = int(row.get("n") or 0)
        for row in d1.query(
            "SELECT COALESCE(status, 'unknown') AS status, COUNT(*) AS n"
            " FROM events WHERE direction = 'status' GROUP BY status",
            tenant_id=tenant_id,
            base_path=base_path,
        ):
            result.status_counts[str(row.get("status"))] = int(row.get("n") or 0)
        result.payload_keys, result.payloads_with_echoes = _payload_stats(
            tenant_id, base_path
        )
    except d1.D1Error as exc:
        result.outcome = "error"
        result.errors.append(str(exc))
        result.findings.append("No se pudo leer la base del worker.")
        result.next_actions.append("Revisar CF_API_TOKEN y los IDs de Cloudflare en la config del tenant.")
        return result

    result.echoes_stored = result.direction_counts.get("out_app", 0)

    if check_graph:
        whatsapp_config = _tenant_whatsapp_config(tenant_id, base_path)
        meta = _tenant_meta(tenant_id)
        apps, error = _connected_apps(
            str(whatsapp_config.get("waba_id") or ""), str(meta.get("page_id") or "")
        )
        result.connected_apps = [
            {
                "app_id": str(app.get("whatsapp_business_api_data", {}).get("id", "")),
                "name": app.get("whatsapp_business_api_data", {}).get("name", ""),
            }
            for app in apps
        ]
        result.connected_apps_count = len(apps)
        result.subscription_check_error = error

    inbound = result.direction_counts.get("in", 0)
    statuses = result.direction_counts.get("status", 0)
    result.findings = [
        f"Eventos entrantes: {inbound}.",
        f"Eventos de estado: {statuses}.",
        f"Ecos de app guardados: {result.echoes_stored}.",
        f"Payloads con ecos (smb_message_echoes/message_echoes): {result.payloads_with_echoes}.",
        "Estados observados: "
        + (", ".join(f"{k}={v}" for k, v in sorted(result.status_counts.items())) or "ninguno"),
        f"Apps actualmente reportadas por el WABA: {result.connected_apps_count}.",
    ]
    if result.subscription_check_error:
        result.findings.append(f"No se pudo verificar suscripción: {result.subscription_check_error}")

    dropped = result.payloads_with_echoes > 0 and result.echoes_stored == 0
    if result.echoes_stored and result.payloads_with_echoes:
        result.outcome = "ok"
    elif dropped:
        result.outcome = "echoes_dropped_by_worker"
        result.findings.append(
            "Meta está enviando ecos, pero el worker no los está guardando "
            "(espera `smb_message_echoes` y llegan en `message_echoes`)."
        )
    elif result.echoes_stored or result.payloads_with_echoes:
        result.outcome = "partial"
    elif not check_graph:
        result.outcome = "subscription_not_checked"
    elif result.connected_apps_count == 0 and not result.subscription_check_error:
        result.outcome = "blocked_no_waba_app_subscription"
    elif result.subscription_check_error:
        result.outcome = "cannot_verify_subscription"
    else:
        result.outcome = "waiting_first_echo"

    result.next_actions = {
        "ok": ["Los ecos están llegando; se puede medir la respuesta humana."],
        "partial": [
            "Hay ecos en payload pero no todos quedaron guardados.",
            "Revisar el insert de out_app en el worker desplegado.",
        ],
        "echoes_dropped_by_worker": [
            "Redesplegar el worker con soporte para `value.message_echoes`.",
            "Después de desplegar, responder desde el celular y volver a correr el diagnóstico.",
        ],
        "blocked_no_waba_app_subscription": [
            "Confirmar en Meta cuál es el App ID real asociado al WABA.",
            "Verificar que esa app siga suscrita al WABA y al campo messages.",
            "Hacer una prueba controlada: recibir un mensaje y responder desde la app de la sucursal.",
            "Ejecutar este diagnóstico otra vez; se espera al menos un out_app.",
        ],
        "cannot_verify_subscription": [
            "Resolver el error de Graph y volver a correr el diagnóstico.",
        ],
        "subscription_not_checked": [
            "Correr el diagnóstico con Graph habilitado para revisar apps suscritas.",
        ],
        "waiting_first_echo": [
            "La app está suscrita: falta que la sucursal responda desde el celular.",
        ],
    }[result.outcome]
    return result


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Diagnóstico de ecos de WhatsApp")
    parser.add_argument("tenant", nargs="?", default="flexi")
    parser.add_argument("--no-graph", action="store_true", help="No consultar Graph API")
    parser.add_argument("--output", default=None, help="Guardar JSON en esta ruta")
    args = parser.parse_args()

    diagnosis = diagnose_echoes(args.tenant, check_graph=not args.no_graph)
    payload = json.dumps(diagnosis.to_dict(), ensure_ascii=False, indent=2)
    if args.output:
        from pathlib import Path

        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
