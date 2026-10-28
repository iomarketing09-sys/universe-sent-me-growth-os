"""Factory de tenants temporales para los tests de CGO y auditoría."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

META_IMPORT_COLUMNS = [
    "Media URL",
    "Caption",
    "Hashtags",
    "Link URL",
    "Post Type",
    "Date (YYYY-MM-DD)",
    "Time (HH:MM, 24h)",
    "Timezone",
    "First Comment",
]


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def make_tenant(
    base: Path,
    name: str,
    track: str = "native_digital",
    complete: bool = True,
    with_ads: bool = True,
    with_schedule: bool = True,
) -> Path:
    """Crea un tenant local con los insumos que revisa el auditor."""
    base = Path(base)
    root = base / "tenants" / name
    root.mkdir(parents=True, exist_ok=True)

    config: Dict[str, Any] = {
        "tenant_id": name,
        "client_name": f"Cliente {name}",
        "timezone": "America/Matamoros",
        "contact_channel": "WhatsApp",
        "tenant_type": track,
        "meta": {"page_id": "111", "ig_user_id": "222"},
        "ads": {
            "ad_account_id": "act_123",
            "approved_models": [
                {"code": "123456", "name": "MODELO", "asset_dir": "assets/models/123456"}
            ],
        },
    }

    if not complete:
        _write_json(root / "config.json", config)
        return root

    _write_json(root / "config.json", config)

    asset_dir = root / "assets" / "models" / "123456"
    asset_dir.mkdir(parents=True, exist_ok=True)
    (asset_dir / "123456 - modelo.jpg").write_bytes(b"fake-image")
    (root / "assets" / "logo.png").write_bytes(b"fake-logo")

    _write_json(
        root / "brand_kit.json",
        {
            "tenant_id": name,
            "brand": f"Cliente {name}",
            "voice": "Cercano y directo.",
            "palette": [{"name": "rojo", "hex": "#D82232"}],
            "logo": {"primary": "assets/logo.png"},
        },
    )
    _write_json(root / "whatsapp" / "config.json", {"tenant_id": name})

    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    rows = []
    for index in range(3):
        day = (tomorrow + timedelta(days=index)).date().isoformat()
        rows.append(
            {
                "Media URL": "123456 - modelo.jpg",
                "Caption": f"Slot {index}",
                "Hashtags": "#test",
                "Link URL": "",
                "Post Type": "PHOTO" if index < 2 else "TEXT_ONLY",
                "Date (YYYY-MM-DD)": day,
                "Time (HH:MM, 24h)": "10:00",
                "Timezone": "America/Matamoros",
                "First Comment": "",
            }
        )

    if with_schedule:
        with (root / "meta_import.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=META_IMPORT_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    _write_json(
        root / "data" / "sync" / "latest.json",
        {
            "tenant_id": name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sources": {
                "ads": {
                    "campaigns": (
                        [
                            {
                                "id": "c1",
                                "name": "Campaña test",
                                "status": "ACTIVE",
                                "spend": 100.0,
                                "impressions": 1000,
                                "clicks": 50,
                                "reach": 800,
                                "conversations": 10,
                            }
                        ]
                        if with_ads
                        else []
                    )
                }
            },
        },
    )

    if track == "native_digital":
        (root / "historical" / "metrics").mkdir(parents=True, exist_ok=True)

    return root
