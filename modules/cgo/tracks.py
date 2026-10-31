"""Resolución de track (native_digital vs physical_cro) por tenant."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

NATIVE_DIGITAL = "native_digital"
PHYSICAL_CRO = "physical_cro"
UNKNOWN = "unknown"

CAPABILITIES_BY_TRACK = {
    NATIVE_DIGITAL: {
        "daily_pipeline",
        "weekly_calendar",
        "tenant_onboarding",
        "cross_tenant_report",
        "canon_sync",
        "meta_publishing",
        "monetization_report",
        "verify_setup",
    },
    PHYSICAL_CRO: {
        "daily_pipeline",
        "tenant_onboarding",
        "cross_tenant_report",
        "meta_publishing",
        "monetization_report",
        "verify_setup",
    },
}

PRODUCT_TYPES = {PHYSICAL_CRO, "retail", "ecommerce_product"}


def load_config(tenant_id: str, base_path: Optional[Path] = None) -> Dict[str, Any]:
    """Lee config.json sin crear directorios."""
    root = Path(base_path) if base_path else Path.cwd()
    path = root / "tenants" / tenant_id / "config.json"
    if not path.is_file():
        raise FileNotFoundError(f"No existe tenants/{tenant_id}/config.json")
    return json.loads(path.read_text(encoding="utf-8"))


def tenant_track(tenant_id: str, base_path: Optional[Path] = None) -> str:
    """Track declarado en config; ``unknown`` si falta o es inválido."""
    try:
        config = load_config(tenant_id, base_path)
    except (FileNotFoundError, ValueError):
        return UNKNOWN
    track = str(config.get("tenant_type") or "")
    if track in (NATIVE_DIGITAL, PHYSICAL_CRO):
        return track
    if track in PRODUCT_TYPES:
        return PHYSICAL_CRO
    return UNKNOWN


def tenant_ids(base_path: Optional[Path] = None) -> List[str]:
    root = Path(base_path) if base_path else Path.cwd()
    tenants_dir = root / "tenants"
    if not tenants_dir.is_dir():
        return []
    return sorted(
        path.name
        for path in tenants_dir.iterdir()
        if path.is_dir() and (path / "config.json").is_file()
    )


def capability_allowed(capability: str, track: str) -> bool:
    allowed = CAPABILITIES_BY_TRACK.get(track)
    if allowed is None:
        return False
    return capability in allowed
