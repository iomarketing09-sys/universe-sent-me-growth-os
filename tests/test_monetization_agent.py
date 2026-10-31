"""Tests del Monetization Agent y su integración con CGO."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.cgo import CgoOrchestrator
from modules.intelligence import MonetizationAgent
from modules.intelligence.monetization import MonetizationStore
from tests.tenant_factory import make_tenant


def _enable_monetization(tenant: Path, threshold: float = 25.0) -> None:
    path = tenant / "config.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    config["monetization"] = {
        "payout_threshold": {
            "amount": threshold,
            "currency": "USD",
            "program": "meta_content_monetization",
            "platform": "Facebook",
        }
    }
    path.write_text(json.dumps(config), encoding="utf-8")


def _seed_ledger(base: Path, tenant_id: str = "universe") -> MonetizationStore:
    store = MonetizationStore(tenant_id, base_path=base)
    store.add_period(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-09-01",
        period_end="2026-09-30",
        approved_net=22.43,
        status="approved",
        source="statement",
    )
    store.add_payout(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-09-01",
        period_end="2026-09-30",
        paid_at="2026-09-30",
        gross=22.43,
        net=22.43,
        status="paid",
        source="statement",
    )
    store.add_period(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-10-01",
        period_end="2026-10-31",
        estimated_net=4.74,
        status="estimated",
        source="meta_app",
    )
    return store


def _write_evidence(tenant: Path) -> None:
    evidence = tenant / "metrics" / "monetization"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "2026-10-31_Meta_Content_Earnings.json").write_text(
        json.dumps(
            {
                "period_start": "2026-10-01",
                "period_end": "2026-10-31",
                "generated_at": "2026-10-31T10:00:00+00:00",
                "total_content_monetization_usd": 4.03,
                "total_approximate_earnings_usd": 4.13,
            }
        ),
        encoding="utf-8",
    )
    (evidence / "2026-10-31_Meta_Post_Earnings_October.json").write_text(
        json.dumps(
            {
                "period_start": "2026-10-01",
                "period_end": "2026-10-31",
                "generated_at": "2026-10-31T11:00:00+00:00",
                "post_level_content_earnings_usd": 1.29,
                "app_reported_earnings_usd": 4.74,
            }
        ),
        encoding="utf-8",
    )


def test_agent_conciles_app_api_and_posts(tmp_path):
    tenant = make_tenant(tmp_path, "universe", track="native_digital")
    _enable_monetization(tenant)
    _seed_ledger(tmp_path)
    _write_evidence(tenant)

    summary = MonetizationAgent("universe", base_path=str(tmp_path)).summary(
        since="2026-10-01", until="2026-10-31"
    )

    assert summary["configured"] is True
    assert summary["latest_period"]["estimated_net"] == 4.74
    assert summary["money"]["payout_threshold"]["remaining"] == 20.26
    assert summary["reconciliation"]["differences"] == {
        "app_vs_page_content": 0.71,
        "app_vs_approximate": 0.61,
        "page_vs_post_level": 2.74,
    }
    assert any("0.71" in warning for warning in summary["warnings"])
    assert summary["boundary"]["mode"] == "read_only"


def test_agent_does_not_modify_ledger(tmp_path):
    tenant = make_tenant(tmp_path, "universe", track="native_digital")
    _enable_monetization(tenant)
    store = _seed_ledger(tmp_path)
    before = {
        "periods": store.periods_path.read_bytes(),
        "payouts": store.payouts_path.read_bytes(),
    }

    MonetizationAgent("universe", base_path=str(tmp_path)).summary()

    assert store.periods_path.read_bytes() == before["periods"]
    assert store.payouts_path.read_bytes() == before["payouts"]


def test_agent_imports_local_signals_idempotently(tmp_path):
    tenant = make_tenant(tmp_path, "universe", track="native_digital")
    _enable_monetization(tenant)
    evidence = tenant / "metrics" / "monetization"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "2026-10-02_Meta_Monetization_Signals.json").write_text(
        json.dumps(
            {
                "date": "2026-10-02",
                "posts": [
                    {
                        "post_id": "pub-1",
                        "date": "2026-10-01",
                        "preview": "preview",
                        "reactions": 10,
                        "comments": 2,
                        "shares": 1,
                        "bonus_points": 17,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    log = tenant / "metrics" / "meta_monetization_log.csv"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "Fecha", "Plataforma", "Business_ID", "Posts_Analizados",
            "Reacciones", "Comentarios", "Shares", "Interacciones_Bonus_Elegibles",
        ])
        writer.writerow(["2026-10-02", "Facebook Page", "", 1, 10, 2, 1, 17])

    agent = MonetizationAgent("universe", base_path=str(tmp_path))
    first = agent.import_local_signals()
    second = agent.import_local_signals()

    assert first["signals"]["inserted"] == 1
    assert first["account"]["inserted"] == 1
    assert second["signals"]["unchanged"] == 1
    assert second["account"]["unchanged"] == 1
    assert not first["errors"]


def test_cgo_monetization_report_capability(tmp_path):
    tenant = make_tenant(tmp_path, "universe", track="native_digital")
    _enable_monetization(tenant)
    _seed_ledger(tmp_path)

    result = CgoOrchestrator(base_path=str(tmp_path)).run_one(
        "monetization_report", "universe"
    )

    assert result.capability == "monetization_report"
    assert result.status == "OK", result.to_dict()
    assert any(item["kind"] == "monetization:threshold" for item in result.actions)
    assert result.data["money"]["payout_threshold"]["remaining"] == 20.26


def test_cgo_monetization_report_not_configured(tmp_path):
    make_tenant(tmp_path, "universe", track="native_digital")

    result = CgoOrchestrator(base_path=str(tmp_path)).run_one(
        "monetization_report", "universe"
    )

    assert result.status == "NOT_CONFIGURED"
    assert any(gate.name == "monetization" for gate in result.gates)
