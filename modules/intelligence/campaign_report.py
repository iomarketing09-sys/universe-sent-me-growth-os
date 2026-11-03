"""Reporte unificado de campaña: Meta + conversaciones de WhatsApp.

Un solo origen de datos y dos salidas derivadas:

- ``reporte_cliente.md``: una página, sin jerga, para presentar.
- ``reporte_interno.md``: IDs, checkpoints, política y discrepancias.

La llave que une ambas fuentes es ``ad_id``.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Matamoros")

ConversationProvider = Callable[..., Dict[str, Any]]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _money(value: float) -> str:
    return f"${value:,.2f}"


def _short_name(name: str) -> str:
    return name.split(" - ")[0].strip() or name


def campaign_dir(tenant_id: str, slug: str, base_path: Optional[Path] = None) -> Path:
    root = Path(base_path) if base_path else _project_root()
    return root / "tenants" / tenant_id / "ads" / "campanas" / slug


def captures_dir(tenant_id: str, slug: str, base_path: Optional[Path] = None) -> Path:
    root = Path(base_path) if base_path else _project_root()
    return root / "tenants" / tenant_id / "ads" / "insights" / "captures" / slug


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def latest_capture(
    tenant_id: str,
    slug: str,
    base_path: Optional[Path] = None,
    checkpoint: Optional[str] = None,
) -> tuple[Path, Dict[str, Any]]:
    """Devuelve la captura más reciente; ``checkpoint`` fuerza una concreta."""
    directory = captures_dir(tenant_id, slug, base_path)
    if checkpoint:
        path = directory / f"{checkpoint}.json"
        if not path.is_file():
            raise FileNotFoundError(f"No existe la captura {path}")
        return path, load_json(path)

    candidates = sorted(directory.glob("*.json"), key=lambda item: item.stat().st_mtime)
    if not candidates:
        raise FileNotFoundError(f"Sin capturas en {directory}")
    path = candidates[-1]
    return path, load_json(path)


def ad_names(meta_ids: Dict[str, Any]) -> Dict[str, str]:
    return {
        str(ad.get("id")): _short_name(str(ad.get("name") or ad.get("id")))
        for ad in meta_ids.get("ads") or []
        if ad.get("id")
    }


def collect_conversations(
    tenant_id: str,
    ad_ids: Sequence[str],
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    *,
    base_path: Optional[Path] = None,
    provider: Optional[ConversationProvider] = None,
) -> Dict[str, Any]:
    """Cuenta personas distintas atribuidas a los anuncios, dentro de la ventana."""
    if provider is None:
        from modules.communications.whatsapp.conversations import conversation_summary

        provider = conversation_summary

    try:
        payload = provider(tenant_id, limit=1000, base_path=base_path)
    except Exception as exc:  # noqa: BLE001 - el reporte no debe caerse por WhatsApp
        return {"available": False, "error": str(exc), "total": 0, "per_ad": {}, "depth": {}}

    wanted = {str(item) for item in ad_ids}
    per_ad: Dict[str, int] = {}
    depth = {"1": 0, "2": 0, "3+": 0}
    total = 0
    seen = set()
    for conversation in payload.get("conversations") or []:
        if not conversation.get("from_ad"):
            continue
        ad_id = str(conversation.get("ad_id") or "")
        if wanted and ad_id not in wanted:
            continue
        first_at = conversation.get("first_at")
        moment = datetime.fromisoformat(str(first_at).replace("Z", "+00:00")) if first_at else None
        if since is not None and moment is not None and moment < since:
            continue
        if until is not None and moment is not None and moment > until:
            continue
        key = conversation.get("contact") or conversation.get("contact_hash") or id(conversation)
        if key in seen:
            continue
        seen.add(key)
        total += 1
        per_ad[ad_id] = per_ad.get(ad_id, 0) + 1
        value = int(conversation.get("depth") or 0)
        depth["1" if value <= 1 else "2" if value == 2 else "3+"] += 1

    return {"available": True, "total": total, "per_ad": per_ad, "depth": depth}


def _campaign_start(meta_ids: Dict[str, Any]) -> Optional[datetime]:
    raw = (meta_ids.get("campaign") or {}).get("start_time")
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return None


def _parse_moment(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def build_client_report(bundle: Dict[str, Any]) -> str:
    capture = bundle["capture"]
    meta_ids = bundle["meta_ids"]
    conversations = bundle["conversations"]
    names = ad_names(meta_ids)
    spend = float(capture.get("total_spend") or 0)
    impressions = sum(int(ad.get("impressions") or 0) for ad in capture.get("ads") or [])
    clicks = sum(int(ad.get("clicks") or 0) for ad in capture.get("ads") or [])
    budget = float((meta_ids.get("campaign") or {}).get("lifetime_budget") or 0) / 100
    total_wa = conversations.get("total") or 0
    cost_per_person = spend / total_wa if total_wa else 0
    meta_conv = int(capture.get("total_conversations") or 0)
    meta_cpa = float(capture.get("blended_cost_per_conversation") or 0)
    latest_wa = (bundle.get("conversations_latest") or conversations).get("total") or 0
    cost_latest = spend / latest_wa if latest_wa else 0
    start = (meta_ids.get("campaign") or {}).get("start_time", "")
    stop = (meta_ids.get("campaign") or {}).get("stop_time", "")

    lines = [
        f"# Campaña {capture.get('campaign_name') or bundle['slug']}",
        "",
        f"**Periodo:** {start[:10]} al {stop[:10]}  ",
        "**Reporte:** avance de resultados",
        "",
        "---",
        "",
        "## Qué hicimos",
        "",
        "Anuncios en Facebook e Instagram con botón directo a WhatsApp, enfocados en",
        "personas de Piedras Negras interesadas en calzado. Varios creativos para ver",
        "cuál conecta mejor con la audiencia.",
        "",
        "## Resultados principales",
        "",
        "| Indicador | Resultado |",
        "| --- | ---: |",
    ]
    if budget:
        lines.append(f"| Inversión ejercida | {_money(spend)} de {_money(budget)} |")
    else:
        lines.append(f"| Inversión ejercida | {_money(spend)} |")
    lines.extend(
        [
            f"| Personas que vieron los anuncios | {impressions:,} |",
            f"| Clics al anuncio | {clicks:,} |",
            f"| Conversaciones reportadas por Meta | {meta_conv} |",
            f"| Costo por conversación (Meta) | {_money(meta_cpa)} |",
            f"| Personas por WhatsApp (mismo corte) | {total_wa} |",
            f"| Costo por persona (WhatsApp, mismo corte) | {_money(cost_per_person)} |",
            "",
            "## Desempeño por anuncio",
            "",
            "| Anuncio | Inversión | Conv. Meta | Costo Meta | Personas WA | Costo WA |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for ad in sorted(capture.get("ads") or [], key=lambda item: float(item.get("spend") or 0), reverse=True):
        ad_id = str(ad.get("ad_id"))
        wa_count = conversations.get("per_ad", {}).get(ad_id, 0)
        cost = float(ad.get("spend") or 0) / wa_count if wa_count else 0
        ad_meta_conv = int(ad.get("conversations") or 0)
        ad_meta_cpa = float(ad.get("cost_per_conversation") or 0)
        label = names.get(ad_id) or _short_name(str(ad.get("ad_name") or ad_id))
        lines.append(
            f"| {label} | {_money(float(ad.get('spend') or 0))} | {ad_meta_conv} | "
            f"{_money(ad_meta_cpa) if ad_meta_conv else '—'} | {wa_count} | "
            f"{_money(cost) if wa_count else '—'} |"
        )

    depth = conversations.get("depth") or {}
    lines.extend(["", "## Conversaciones en WhatsApp", ""])
    if conversations.get("available") and total_wa:
        lines.extend(
            [
                f"- {total_wa} personas llegaron desde un anuncio de esta campaña.",
                f"- {depth.get('3+', 0)} sostuvieron conversación de 3 mensajes o más.",
                f"- {depth.get('1', 0)} escribieron una sola vez.",
                "",
                "La ventana es la misma que la de Meta: del inicio de la campaña al",
                "corte del reporte. Meta y WhatsApp cuentan distinto, por eso los",
                "totales no coinciden; ambos se muestran sin ajustar.",
                "",
                f"Al día de hoy el número subió a {latest_wa} personas ({_money(cost_latest)} por persona).",
                "",
            ]
        )
    else:
        lines.extend(["Sin datos de conversaciones disponibles.", ""])

    lines.extend(["## Lectura", ""])
    per_ad = conversations.get("per_ad", {})
    # Un anuncio con una sola conversación no alcanza para declararlo eficiente.
    minimum = max(3, round(total_wa * 0.1))
    eligible = [
        (float(ad.get("spend") or 0) / per_ad[str(ad.get("ad_id"))], str(ad.get("ad_id")))
        for ad in capture.get("ads") or []
        if per_ad.get(str(ad.get("ad_id")), 0) >= minimum
    ]
    best_id = None
    if eligible:
        best_cost, best_id = min(eligible)
        best_name = names.get(best_id, best_id)
        lines.append(f"- **{best_name}** es el anuncio más eficiente: {_money(best_cost)} por persona.")
    low_volume = [
        names.get(str(ad.get("ad_id")), str(ad.get("ad_id")))
        for ad in capture.get("ads") or []
        if 0 < per_ad.get(str(ad.get("ad_id")), 0) < minimum
    ]
    if low_volume:
        lines.append(
            f"- {' y '.join(low_volume)} tienen menos de {minimum} conversaciones: su costo aún no es concluyente."
        )
    top = max(
        ((conversations["per_ad"].get(str(ad.get("ad_id")), 0), str(ad.get("ad_id"))) for ad in capture.get("ads") or []),
        default=(0, ""),
    )
    if top[0] and top[1] != best_id:
        lines.append(f"- **{names.get(top[1], top[1])}** concentra el mayor volumen: {top[0]} conversaciones.")
    elif top[0] and top[1] == best_id:
        lines.append(f"- También concentra el mayor volumen: {top[0]} conversaciones.")
    if total_wa:
        lines.append("- Cada conversación es una oportunidad real de venta, no un clic.")
    lines.extend(
        [
            "",
            "## Siguiente paso",
            "",
            f"La campaña cierra el **{stop[:10]}**. El reporte final se entrega con los",
            "números definitivos del periodo completo.",
            "",
        ]
    )
    return "\n".join(lines)


def build_internal_report(bundle: Dict[str, Any]) -> str:
    capture = bundle["capture"]
    meta_ids = bundle["meta_ids"]
    conversations = bundle["conversations"]
    names = ad_names(meta_ids)
    campaign = meta_ids.get("campaign") or {}

    lines = [
        f"# Reporte interno — {bundle['slug']}",
        "",
        f"- **Tenant:** `{bundle['tenant_id']}`",
        f"- **Campaña:** `{campaign.get('id')}` · {campaign.get('name')}",
        f"- **Estado:** {campaign.get('status')} / {campaign.get('effective_status')}",
        f"- **Presupuesto:** {_money(float(campaign.get('lifetime_budget') or 0) / 100)}",
        f"- **Ventana:** {campaign.get('start_time')} → {campaign.get('stop_time')}",
        f"- **Corte usado:** {capture.get('checkpoint')} · programado {capture.get('scheduled_for')} · capturado {capture.get('captured_at')}",
        f"- **Fuente Meta:** `{bundle['capture_path']}`",
        "",
        "## Meta por anuncio",
        "",
        "| Anuncio | ad_id | Estado | Gasto | Impr. | Clics | CTR | Conv. Meta | CPA |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for ad in capture.get("ads") or []:
        ad_id = str(ad.get("ad_id"))
        lines.append(
            f"| {names.get(ad_id, ad.get('ad_name'))} | `{ad_id}` | {ad.get('status')} | "
            f"{_money(float(ad.get('spend') or 0))} | {ad.get('impressions')} | {ad.get('clicks')} | "
            f"{float(ad.get('ctr') or 0):.2f}% | {ad.get('conversations')} | "
            f"{_money(float(ad.get('cost_per_conversation') or 0))} |"
        )

    lines.extend(
        [
            "",
            f"**Total Meta:** {_money(float(capture.get('total_spend') or 0))} · "
            f"{capture.get('total_conversations')} conversaciones · "
            f"{_money(float(capture.get('blended_cost_per_conversation') or 0))} por conversación.",
            "",
            "## WhatsApp atribuido",
            "",
            "| Anuncio | Conversaciones |",
            "| --- | ---: |",
        ]
    )
    for ad_id, count in sorted(conversations.get("per_ad", {}).items(), key=lambda item: item[1], reverse=True):
        lines.append(f"| {names.get(ad_id, ad_id)} | {count} |")
    if conversations.get("available"):
        lines.append(f"\n**Total:** {conversations.get('total', 0)} conversaciones únicas.")
        depth = conversations.get("depth") or {}
        lines.append(f"Profundidad: 1 mensaje {depth.get('1', 0)} · 2 mensajes {depth.get('2', 0)} · 3+ {depth.get('3+', 0)}.")
    else:
        lines.append(f"\nSin datos de WhatsApp: {conversations.get('error')}")

    meta_conv = int(capture.get("total_conversations") or 0)
    wa_conv = int(conversations.get("total") or 0)
    latest_wa = (bundle.get("conversations_latest") or conversations).get("total") or 0
    lines.extend(
        [
            "",
            "## Discrepancias",
            "",
            f"- Meta contabiliza {meta_conv} conversaciones; WhatsApp registra {wa_conv}. "
            "Meta corta a 72 h y cuenta clics a WhatsApp; WhatsApp cuenta personas que escribieron.",
            f"- Al día de hoy WhatsApp acumula {latest_wa} personas; el reporte usa la ventana del corte.",
            "- La captura puede ser anterior al momento del reporte; el estado de los anuncios es el del corte.",
            "",
        ]
    )
    return "\n".join(lines)


def build_bundle(
    tenant_id: str,
    slug: str,
    *,
    base_path: Optional[Path] = None,
    checkpoint: Optional[str] = None,
    provider: Optional[ConversationProvider] = None,
) -> Dict[str, Any]:
    directory = campaign_dir(tenant_id, slug, base_path)
    meta_path = directory / "meta_ids.json"
    meta_ids = load_json(meta_path) if meta_path.is_file() else {"ads": []}
    capture_path, capture = latest_capture(tenant_id, slug, base_path, checkpoint)
    ad_ids = [str(ad.get("id")) for ad in meta_ids.get("ads") or [] if ad.get("id")]
    since = _campaign_start(meta_ids)
    cutoff = _parse_moment(capture.get("scheduled_for"))
    conversations = collect_conversations(
        tenant_id,
        ad_ids,
        since,
        until=cutoff,
        base_path=base_path,
        provider=provider,
    )
    conversations_latest = (
        collect_conversations(
            tenant_id,
            ad_ids,
            since,
            base_path=base_path,
            provider=provider,
        )
        if cutoff
        else conversations
    )
    return {
        "tenant_id": tenant_id,
        "slug": slug,
        "meta_ids": meta_ids,
        "capture": capture,
        "capture_path": capture_path,
        "conversations": conversations,
        "conversations_latest": conversations_latest,
        "cutoff": cutoff,
    }


def write_reports(
    bundle: Dict[str, Any], base_path: Optional[Path] = None
) -> tuple[Path, Path, Path]:
    from modules.intelligence.report_template import render_client_html

    directory = campaign_dir(bundle["tenant_id"], bundle["slug"], base_path)
    client = directory / "reporte_cliente.md"
    internal = directory / "reporte_interno.md"
    page = directory / "reporte_cliente.html"
    client.write_text(build_client_report(bundle), encoding="utf-8")
    internal.write_text(build_internal_report(bundle), encoding="utf-8")
    page.write_text(render_client_html(bundle), encoding="utf-8")
    return client, internal, page


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Genera reporte de cliente e interno de una campaña")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--campaign", required=True, help="slug de la campaña")
    parser.add_argument("--checkpoint", help="fuerza una captura (E24, E48, FINAL...)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    bundle = build_bundle(args.tenant, args.campaign, checkpoint=args.checkpoint)
    client, internal, page = write_reports(bundle)
    if args.json:
        print(json.dumps({"cliente": str(client), "interno": str(internal), "html": str(page)}, ensure_ascii=False))
    else:
        print(f"cliente: {client}")
        print(f"interno: {internal}")
        print(f"html:    {page}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
