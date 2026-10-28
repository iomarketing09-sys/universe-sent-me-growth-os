"""Utilidades compartidas por las capacidades de CGO."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from modules.cgo.result import CgoContext
from modules.cgo.tracks import load_config


def schedule_path(tenant_dir: Path) -> Optional[Path]:
    candidates = list(tenant_dir.glob("meta_import*.csv")) + list(
        tenant_dir.glob("future_schedule.csv")
    )
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def count_csv_rows(path: Optional[Path]) -> int:
    if path is None or not path.is_file():
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def snapshot_age_days(tenant_dir: Path) -> Optional[int]:
    path = tenant_dir / "data" / "sync" / "latest.json"
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        stamp = payload.get("generated_at") or payload.get("timestamp")
        when = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
    except (OSError, ValueError, TypeError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max(0, (datetime.now(timezone.utc) - when).days)


def ads_summary(ctx: CgoContext, tenant_id: str) -> Dict[str, Any]:
    """Resumen local de Meta Ads (sin red)."""
    from modules.intelligence import MetaAdsAgent

    agent = MetaAdsAgent(tenant_id, base_path=str(ctx.base_path))
    return agent.summary(offline=True)


def tenant_config(ctx: CgoContext, tenant_id: str) -> Dict[str, Any]:
    try:
        return load_config(tenant_id, ctx.base_path)
    except (FileNotFoundError, ValueError):
        return {}
