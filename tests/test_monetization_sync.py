"""Tests del sincronizador de Monetization Agent."""

from __future__ import annotations

import json
from pathlib import Path

from modules.intelligence.monetization import MonetizationStore
from scripts.run_monetization_sync import eligible_tenants, sync_tenant
from tests.tenant_factory import make_tenant


def _enable_monetization(tenant: Path) -> None:
    path = tenant / "config.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    config["monetization"] = {
        "payout_threshold": {
            "amount": 25.0,
            "currency": "USD",
            "program": "meta_content_monetization",
            "platform": "Facebook",
        }
    }
    path.write_text(json.dumps(config), encoding="utf-8")


def test_sync_tenant_imports_and_reports_without_fetch(tmp_path):
    tenant = make_tenant(tmp_path, "universe", track="native_digital")
    _enable_monetization(tenant)
    evidence = tenant / "metrics" / "monetization"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "2026-10-02_Meta_Monetization_Signals.json").write_text(
        json.dumps(
            {
                "date": "2026-10-02",
                "posts": [{"post_id": "pub-1", "reactions": 5, "comments": 1, "shares": 1}],
            }
        ),
        encoding="utf-8",
    )

    result = sync_tenant(
        "universe",
        base_path=tmp_path,
        since="2026-10-01",
        until="2026-10-31",
        fetch=False,
    )

    assert result["status"] in {"ok", "partial"}
    assert not result["errors"]
    assert result["summary"]["signals"]["rows"] == 1
    assert len(MonetizationStore("universe", base_path=tmp_path).load_signals()) == 1


def test_sync_tenant_dry_run_does_not_write(tmp_path):
    tenant = make_tenant(tmp_path, "universe", track="native_digital")
    _enable_monetization(tenant)
    evidence = tenant / "metrics" / "monetization"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "2026-10-02_Meta_Monetization_Signals.json").write_text(
        json.dumps({"date": "2026-10-02", "posts": [{"post_id": "pub-1"}]}),
        encoding="utf-8",
    )

    sync_tenant(
        "universe",
        base_path=tmp_path,
        since="2026-10-01",
        until="2026-10-31",
        fetch=False,
        dry_run=True,
    )

    assert not (tenant / "data" / "monetization" / "signals.csv").exists()


def test_eligible_tenants_only_includes_monetization_tenants(tmp_path):
    monetized = make_tenant(tmp_path, "universe", track="native_digital")
    _enable_monetization(monetized)
    make_tenant(tmp_path, "flexi", track="physical_cro")

    assert eligible_tenants(tmp_path) == ["universe"]
