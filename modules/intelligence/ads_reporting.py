"""Construcción y renderizado de reportes de rendimiento por anuncio."""

from __future__ import annotations

from typing import Dict, List

from modules.intelligence.ads_ledger import latest_by_ad


DEFAULT_MAX_CPA = 8.0


def _float(value: object) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _money(value: float) -> str:
    return f"${value:,.2f}"


def build_report(rows: List[Dict], max_cpa: float = DEFAULT_MAX_CPA) -> Dict:
    """Resume el último corte por anuncio y ordena por eficiencia."""
    latest = latest_by_ad(rows)
    ads = []
    for row in latest:
        spend = _float(row.get("spend"))
        conversations = int(_float(row.get("conversations")))
        cpa = _float(row.get("cost_per_conversation"))
        ads.append(
            {
                "ad_id": row.get("ad_id", ""),
                "ad_name": row.get("ad_name", ""),
                "status": row.get("status", ""),
                "spend": round(spend, 2),
                "impressions": int(_float(row.get("impressions"))),
                "clicks": int(_float(row.get("clicks"))),
                "ctr": round(_float(row.get("ctr")), 2),
                "conversations": conversations,
                "cost_per_conversation": round(cpa, 2),
                "over_threshold": bool(conversations and cpa > max_cpa),
            }
        )
    ads.sort(
        key=lambda item: (
            0 if item["conversations"] else 1,
            item["cost_per_conversation"] if item["conversations"] else -item["spend"],
        )
    )
    total_spend = round(sum(item["spend"] for item in ads), 2)
    total_conv = sum(item["conversations"] for item in ads)
    return {
        "ads": ads,
        "total_spend": total_spend,
        "total_conversations": total_conv,
        "blended_cost_per_conversation": round(total_spend / total_conv, 2) if total_conv else 0.0,
        "max_cpa": max_cpa,
        "alerts": [item["ad_name"] for item in ads if item["over_threshold"]],
    }


def render_text(report: Dict) -> str:
    lines = [f"{'ANUNCIO':<28} {'GASTO':>9} {'CONV':>6} {'COSTO/CONV':>11} {'CTR':>7}", "-" * 66]
    for ad in report["ads"]:
        flag = "  ⚠️" if ad["over_threshold"] else ""
        lines.append(
            f"{ad['ad_name'][:28]:<28} {_money(ad['spend']):>9} "
            f"{ad['conversations']:>6} {_money(ad['cost_per_conversation']):>11} "
            f"{ad['ctr']:>6.2f}%{flag}"
        )
    lines.extend(
        [
            "-" * 66,
            f"Total: {_money(report['total_spend'])} · "
            f"{report['total_conversations']} conversaciones · "
            f"{_money(report['blended_cost_per_conversation'])} por conversación",
        ]
    )
    if report["alerts"]:
        lines.append(
            f"\nPor encima de {_money(report['max_cpa'])} por conversación: "
            f"{', '.join(report['alerts'])}"
        )
        lines.append("Revisar: pausar y redistribuir si el gasto ya es significativo.")
    return "\n".join(lines)


def render_markdown(
    report: Dict,
    *,
    tenant_id: str,
    campaign_slug: str,
    campaign_id: str,
    checkpoint: str,
    scheduled_for: str,
    captured_at: str,
    elapsed_hours: float,
    late_minutes: int,
) -> str:
    """Genera el reporte persistente de un corte E24/E48/E72/etc."""
    lines = [
        f"# Métricas {checkpoint} — {campaign_slug}",
        "",
        f"- **Tenant:** `{tenant_id}`",
        f"- **Campaña:** `{campaign_id}`",
        f"- **Corte programado:** {scheduled_for}",
        f"- **Capturado:** {captured_at}",
        f"- **Antigüedad de campaña:** {elapsed_hours:.1f} h",
        f"- **Retraso de captura:** {late_minutes} min",
        "",
        "| Anuncio | Gasto | Impresiones | Clics | CTR | Conversaciones | Costo / conversación |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for ad in report["ads"]:
        flag = " ⚠️" if ad["over_threshold"] else ""
        lines.append(
            f"| {ad['ad_name']}{flag} | {_money(ad['spend'])} | {ad['impressions']} | "
            f"{ad['clicks']} | {ad['ctr']:.2f}% | {ad['conversations']} | "
            f"{_money(ad['cost_per_conversation'])} |"
        )
    if not report["ads"]:
        lines.append("| Sin datos de anuncios | $0.00 | 0 | 0 | 0.00% | 0 | $0.00 |")
    lines.extend(
        [
            "",
            f"**Total:** {_money(report['total_spend'])} · "
            f"{report['total_conversations']} conversaciones · "
            f"{_money(report['blended_cost_per_conversation'])} por conversación.",
            "",
        ]
    )
    if report["alerts"]:
        lines.append(
            f"> ⚠️ Por encima de {_money(report['max_cpa'])} por conversación: "
            f"{', '.join(report['alerts'])}."
        )
    else:
        lines.append(f"> Sin anuncios por encima de {_money(report['max_cpa'])} por conversación.")
    return "\n".join(lines) + "\n"
