"""Conversaciones de WhatsApp: volumen, profundidad y atribución a anuncios.

Todo se calcula sobre la tabla ``events`` del worker (solo lectura). Si la base
desplegada todavía no tiene las columnas de ``referral``, se devuelve el resumen
sin atribución y se avisa en ``warnings``.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from modules.communications.whatsapp import d1

BASE_COLUMNS = """
    contact_hash,
    MAX(contact_name) AS contact_name,
    MAX(contact_last4) AS contact_last4,
    MIN(received_at) AS first_at,
    MAX(received_at) AS last_at,
    SUM(CASE WHEN direction = 'in' THEN 1 ELSE 0 END) AS inbound,
    SUM(CASE WHEN direction = 'out_app' THEN 1 ELSE 0 END) AS outbound_app,
    SUM(CASE WHEN direction = 'status' THEN 1 ELSE 0 END) AS statuses
"""

REFERRAL_COLUMNS = """,
    MAX(CASE WHEN referral_source_id <> '' THEN 1 ELSE 0 END) AS from_ad,
    MAX(referral_source_id) AS ad_id,
    MAX(referral_headline) AS ad_headline,
    MAX(referral_source_url) AS ad_source_url
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _rows_with_fallback(prefix: str, suffix: str, **kwargs: Any):
    """Intenta con columnas de referral y degrada si el esquema no las tiene."""
    try:
        return d1.query(prefix + REFERRAL_COLUMNS + suffix, **kwargs), []
    except d1.D1Error as exc:
        message = str(exc).lower()
        if "referral" not in message and "no such column" not in message:
            raise
        return d1.query(prefix + suffix, **kwargs), [
            "La base del worker no tiene columnas de referral; se omite la atribución a anuncios."
        ]


def conversation_summary(
    tenant_id: str = "flexi",
    limit: int = 200,
    base_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Una fila por conversación (contacto), ordenada por actividad reciente."""
    prefix = "SELECT" + BASE_COLUMNS
    suffix = (
        " FROM events "
        "WHERE contact_hash IS NOT NULL AND contact_hash <> '' "
        "GROUP BY contact_hash ORDER BY last_at DESC LIMIT ?"
    )
    rows, warnings = _rows_with_fallback(
        prefix, suffix, params=[limit], tenant_id=tenant_id, base_path=base_path
    )

    conversations = []
    for row in rows:
        inbound = int(row.get("inbound") or 0)
        last4 = row.get("contact_last4") or ""
        conversations.append(
            {
                "contact": f"…{last4}" if last4 else "—",
                "contact_name": row.get("contact_name") or "",
                "first_at": row.get("first_at"),
                "last_at": row.get("last_at"),
                "inbound": inbound,
                "outbound_app": int(row.get("outbound_app") or 0),
                "statuses": int(row.get("statuses") or 0),
                "depth": inbound,
                "from_ad": bool(row.get("from_ad")),
                "ad_id": row.get("ad_id") or "",
                "ad_headline": row.get("ad_headline") or "",
            }
        )

    return {
        "tenant_id": tenant_id,
        "generated_at": _now(),
        "total": len(conversations),
        "warnings": warnings,
        "conversations": conversations,
    }


def depth_distribution(
    tenant_id: str = "flexi", base_path: Optional[str] = None
) -> Dict[str, Any]:
    """Cuántas conversaciones llegaron a 1, 2 o 3+ mensajes del cliente."""
    sql = (
        "SELECT inbound, COUNT(*) AS conversations FROM ("
        "  SELECT contact_hash, COUNT(*) AS inbound FROM events"
        "  WHERE direction = 'in' AND contact_hash IS NOT NULL AND contact_hash <> ''"
        "  GROUP BY contact_hash"
        ") GROUP BY inbound ORDER BY inbound"
    )
    rows = d1.query(sql, tenant_id=tenant_id, base_path=base_path)
    buckets = {"1": 0, "2": 0, "3+": 0}
    total = 0
    weighted = 0
    for row in rows:
        inbound = int(row.get("inbound") or 0)
        count = int(row.get("conversations") or 0)
        if inbound <= 0:
            continue
        key = "1" if inbound == 1 else "2" if inbound == 2 else "3+"
        buckets[key] += count
        total += count
        weighted += inbound * count
    return {
        "tenant_id": tenant_id,
        "generated_at": _now(),
        "conversations": total,
        "buckets": buckets,
        "average_depth": round(weighted / total, 2) if total else 0.0,
    }


def campaign_conversations(
    tenant_id: str = "flexi", base_path: Optional[str] = None
) -> Dict[str, Any]:
    """Conversaciones que traen ``referral`` de un anuncio (click to WhatsApp)."""
    sql = (
        "SELECT referral_source_id AS ad_id, MAX(referral_headline) AS headline,"
        " COUNT(DISTINCT contact_hash) AS conversations,"
        " SUM(CASE WHEN direction = 'in' THEN 1 ELSE 0 END) AS inbound"
        " FROM events WHERE referral_source_id IS NOT NULL AND referral_source_id <> ''"
        " GROUP BY referral_source_id ORDER BY conversations DESC"
    )
    try:
        rows = d1.query(sql, tenant_id=tenant_id, base_path=base_path)
    except d1.D1Error as exc:
        if "referral" in str(exc).lower() or "no such column" in str(exc).lower():
            return {
                "tenant_id": tenant_id,
                "generated_at": _now(),
                "available": False,
                "warnings": ["La base del worker no tiene columnas de referral."],
                "campaigns": [],
                "total_conversations": 0,
            }
        raise
    campaigns = [
        {
            "ad_id": row.get("ad_id"),
            "headline": row.get("headline") or "",
            "conversations": int(row.get("conversations") or 0),
            "inbound": int(row.get("inbound") or 0),
        }
        for row in rows
    ]
    return {
        "tenant_id": tenant_id,
        "generated_at": _now(),
        "available": True,
        "warnings": [],
        "campaigns": campaigns,
        "total_conversations": sum(c["conversations"] for c in campaigns),
    }


def summary_sql_export(tenant_id: str = "flexi", base_path: Optional[str] = None) -> str:
    """Resumen completo en un solo JSON (para CLI)."""
    return json.dumps(
        {
            "summary": conversation_summary(tenant_id, base_path=base_path),
            "depth": depth_distribution(tenant_id, base_path=base_path),
            "campaigns": campaign_conversations(tenant_id, base_path=base_path),
        },
        ensure_ascii=False,
        indent=2,
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Conversaciones de WhatsApp")
    parser.add_argument("tenant", nargs="?", default="flexi")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--depth", action="store_true", help="Solo distribución de profundidad")
    parser.add_argument("--campaigns", action="store_true", help="Solo atribución a anuncios")
    args = parser.parse_args()

    if args.depth:
        result: Any = depth_distribution(args.tenant)
    elif args.campaigns:
        result = campaign_conversations(args.tenant)
    else:
        result = conversation_summary(args.tenant, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
