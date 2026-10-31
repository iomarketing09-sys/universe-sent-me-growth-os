"""Historial diario de métricas por anuncio.

``latest.json`` se sobrescribe en cada sync; este ledger conserva un corte por
día y anuncio para poder comparar 24/48/72 h sin perder los datos anteriores.
"""

from __future__ import annotations

import csv
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


LEDGER_FIELDS = [
    "date",
    "captured_at_utc",
    "campaign_id",
    "campaign_name",
    "adset_id",
    "ad_id",
    "ad_name",
    "status",
    "spend",
    "impressions",
    "clicks",
    "reach",
    "ctr",
    "cpc",
    "conversations",
    "cost_per_conversation",
]


def _project_root() -> Path:
    """Raíz del repo, sin depender del directorio desde el que se ejecute."""
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


def ledger_path(tenant_id: str, base_path: Optional[Path] = None) -> Path:
    root = Path(base_path) if base_path else _project_root()
    return root / "tenants" / tenant_id / "ads" / "insights" / "ad_insights_daily.csv"


def ad_insight_row(ad: Dict, day: str, captured_at: str) -> Dict[str, str]:
    """Normaliza una respuesta de Meta al esquema persistido del ledger."""
    return {
        "date": day,
        "captured_at_utc": captured_at,
        "campaign_id": str(ad.get("campaign_id", "")),
        "campaign_name": str(ad.get("campaign_name", "")),
        "adset_id": str(ad.get("adset_id", "")),
        "ad_id": str(ad.get("id", "")),
        "ad_name": str(ad.get("name", "")),
        "status": str(ad.get("status", "")),
        "spend": f"{float(ad.get('spend') or 0):.2f}",
        "impressions": str(int(ad.get("impressions") or 0)),
        "clicks": str(int(ad.get("clicks") or 0)),
        "reach": str(int(ad.get("reach") or 0)),
        "ctr": f"{float(ad.get('ctr') or 0):.2f}",
        "cpc": f"{float(ad.get('cpc') or 0):.2f}",
        "conversations": str(int(ad.get("conversations") or 0)),
        "cost_per_conversation": f"{float(ad.get('cost_per_conversation') or 0):.2f}",
    }


def record_ad_insights(
    tenant_id: str,
    ads: List[Dict],
    *,
    day: Optional[date] = None,
    base_path: Optional[Path] = None,
) -> Path:
    """Inserta o reemplaza el corte del día para cada anuncio.

    Idempotente: si el sync corre dos veces el mismo día, actualiza la fila en
    lugar de duplicarla.
    """
    path = ledger_path(tenant_id, base_path)
    if not ads:
        return path

    day_str = (day or date.today()).isoformat()
    captured_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    existing: List[Dict[str, str]] = []
    if path.is_file():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))

    new_rows = [ad_insight_row(ad, day_str, captured_at) for ad in ads]
    new_ids = {row["ad_id"] for row in new_rows}
    kept = [
        row
        for row in existing
        if not (row.get("date") == day_str and row.get("ad_id") in new_ids)
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept + new_rows)
    return path


def load_ad_insights(
    tenant_id: str,
    *,
    campaign_id: Optional[str] = None,
    base_path: Optional[Path] = None,
) -> List[Dict[str, str]]:
    path = ledger_path(tenant_id, base_path)
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if campaign_id:
        rows = [row for row in rows if row.get("campaign_id") == campaign_id]
    return rows


def latest_by_ad(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Última fotografía por anuncio (la fecha más reciente)."""
    latest: Dict[str, Dict[str, str]] = {}
    for row in rows:
        ad_id = row.get("ad_id", "")
        if not ad_id:
            continue
        if ad_id not in latest or row.get("date", "") >= latest[ad_id].get("date", ""):
            latest[ad_id] = row
    return list(latest.values())
