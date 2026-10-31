"""Tests de Monetization Lite: ledger, importación y reporte."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.intelligence.monetization import (
    MonetizationSignal,
    MonetizationStore,
    summarize_monetization,
)


def _tenant(root: Path, tenant_id: str = "universe", timezone: str = "America/Matamoros") -> Path:
    tenant = root / "tenants" / tenant_id
    tenant.mkdir(parents=True, exist_ok=True)
    (tenant / "config.json").write_text(
        json.dumps({"tenant_id": tenant_id, "timezone": timezone}), encoding="utf-8"
    )
    return tenant


def _set_payout_threshold(
    tenant: Path,
    amount: float = 25.0,
    currency: str = "USD",
    program: str = "meta_content_monetization",
    platform: str = "Facebook",
) -> None:
    config = json.loads((tenant / "config.json").read_text(encoding="utf-8"))
    config["monetization"] = {
        "payout_threshold": {
            "amount": amount,
            "currency": currency,
            "program": program,
            "platform": platform,
        }
    }
    (tenant / "config.json").write_text(json.dumps(config), encoding="utf-8")


def _signal_file(path: Path, signal_date: str, posts: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"date": signal_date, "posts": posts}, ensure_ascii=False),
        encoding="utf-8",
    )


def _post(post_id: str, bonus: int, reactions: int = 1, comments: int = 0, shares: int = 0) -> dict:
    return {
        "post_id": post_id,
        "date": "2026-10-01",
        "preview": "preview",
        "reactions": reactions,
        "comments": comments,
        "shares": shares,
        "bonus_points": bonus,
    }


def test_import_signal_dir_is_idempotent_and_uses_context(tmp_path):
    tenant = _tenant(tmp_path)
    (tenant / "publication_contexts.json").write_text(json.dumps({
        "pub-1": {
            "publication_id": "pub-1",
            "character": "Existencial 2607966",
            "meme_text": "Universe - Existencial",
            "caption": "caption",
            "published_at": "2026-10-01T16:30:00+00:00",
        }
    }), encoding="utf-8")
    _signal_file(
        tenant / "metrics" / "monetization" / "2026-10-02_Meta_Monetization_Signals.json",
        "2026-10-02",
        [_post("pub-1", 50, 40, 2, 2)],
    )
    _signal_file(
        tenant / "metrics" / "monetization" / "2026-10-03_Meta_Monetization_Signals.json",
        "2026-10-03",
        [_post("pub-1", 60, 45, 3, 3)],
    )

    store = MonetizationStore("universe", base_path=tmp_path)
    first = store.import_signal_dir()
    second = store.import_signal_dir()

    assert first["files"] == 2
    assert first["rows"] == 2
    assert first["inserted"] == 2
    assert second["inserted"] == 0
    assert second["updated"] == 0
    assert second["unchanged"] == 2
    signals = store.load_signals()
    assert len(signals) == 2
    assert {item.series for item in signals} == {"Existencial"}
    assert {item.character for item in signals} == {"Universe"}


def test_report_uses_increments_not_cumulative_bonus(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    signals = [
        MonetizationSignal(
            signal_id="MS-1", tenant_id="universe", platform="Facebook",
            program="meta_content_monetization", signal_date="2026-10-01",
            publication_id="pub-1", reactions=5, comments=1, shares=1,
            bonus_points=10,
        ),
        MonetizationSignal(
            signal_id="MS-2", tenant_id="universe", platform="Facebook",
            program="meta_content_monetization", signal_date="2026-10-02",
            publication_id="pub-1", reactions=15, comments=2, shares=3,
            bonus_points=30,
        ),
        MonetizationSignal(
            signal_id="MS-3", tenant_id="universe", platform="Facebook",
            program="meta_content_monetization", signal_date="2026-10-03",
            publication_id="pub-1", reactions=20, comments=3, shares=4,
            bonus_points=40,
        ),
    ]
    store.save_signals(signals)

    report = store.report()

    assert report["signals"]["latest_bonus_points"] == 40
    assert report["signals"]["incremental_bonus_points"] == 40
    daily = {row["period"]: row for row in report["signals"]["increments"]["daily"]}
    assert daily["2026-10-01"]["bonus_points"] == 10
    assert daily["2026-10-02"]["bonus_points"] == 20
    assert daily["2026-10-03"]["bonus_points"] == 10


def test_report_handles_negative_corrections(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    store.save_signals([
        MonetizationSignal(
            signal_id="MS-1", tenant_id="universe", platform="Facebook",
            program="meta_content_monetization", signal_date="2026-10-01",
            publication_id="pub-1", bonus_points=10,
        ),
        MonetizationSignal(
            signal_id="MS-2", tenant_id="universe", platform="Facebook",
            program="meta_content_monetization", signal_date="2026-10-02",
            publication_id="pub-1", bonus_points=8,
        ),
    ])

    report = store.report()

    assert report["signals"]["latest_bonus_points"] == 8
    assert report["signals"]["incremental_bonus_points"] == 8
    daily = {row["period"]: row for row in report["signals"]["increments"]["daily"]}
    assert daily["2026-10-02"]["bonus_points"] == -2
    assert daily["2026-10-02"]["corrections"] == 1


def test_money_separates_estimated_approved_and_paid(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    store.add_period(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-10-01",
        period_end="2026-10-31",
        estimated_net=25,
        status="estimated",
    )
    store.add_period(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-09-01",
        period_end="2026-09-30",
        approved_net=18,
        status="approved",
    )
    store.add_payout(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-09-01",
        period_end="2026-09-30",
        paid_at="2026-10-15",
        gross=20,
        fee=2,
        net=18,
    )

    report = store.report()

    assert report["money"]["estimated_net"] == 25
    assert report["money"]["approved_unpaid_net"] == 0
    assert report["money"]["pipeline_net"] == 25
    assert report["money"]["paid_net"] == 18
    assert report["money"]["recognized_net"] == 18
    assert report["money"]["payouts"]["net"] == 18


def test_period_and_payout_are_idempotent(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    kwargs = dict(
        platform="Facebook", program="meta_content_monetization",
        period_start="2026-10-01", period_end="2026-10-31",
    )
    store.add_period(**kwargs, estimated_net=10, status="estimated")
    store.add_period(**kwargs, estimated_net=12, status="estimated")
    store.add_payout(**kwargs, paid_at="2026-11-15", gross=10, fee=1, net=9)
    store.add_payout(**kwargs, paid_at="2026-11-15", gross=12, fee=1, net=11)

    assert len(store.load_periods()) == 1
    assert store.load_periods()[0].estimated_net == 12
    assert len(store.load_payouts()) == 1
    assert store.load_payouts()[0].net == 11


def test_tenant_isolation(tmp_path):
    _tenant(tmp_path, "universe")
    _tenant(tmp_path, "flexi")
    universe = MonetizationStore("universe", base_path=tmp_path)
    flexi = MonetizationStore("flexi", base_path=tmp_path)
    universe.upsert_signals([MonetizationSignal(
        signal_id="MS-U", tenant_id="universe", platform="Facebook",
        program="meta_content_monetization", signal_date="2026-10-01",
        publication_id="pub-u", bonus_points=10,
    )])
    flexi.upsert_signals([MonetizationSignal(
        signal_id="MS-F", tenant_id="flexi", platform="Facebook",
        program="meta_content_monetization", signal_date="2026-10-01",
        publication_id="pub-f", bonus_points=20,
    )])

    assert [item.publication_id for item in universe.load_signals()] == ["pub-u"]
    assert [item.publication_id for item in flexi.load_signals()] == ["pub-f"]


def test_payout_mismatch_and_no_payout_warning(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    store.add_period(
        platform="Facebook", program="meta_content_monetization",
        period_start="2026-10-01", period_end="2026-10-31",
        estimated_net=10, status="estimated",
    )
    report = store.report()
    assert "Sin payout confirmado" in " ".join(report["data_quality"]["warnings"])

    store.add_payout(
        platform="Facebook", program="meta_content_monetization",
        period_start="2026-10-01", period_end="2026-10-31",
        paid_at="2026-11-15", gross=10, fee=0, net=9,
    )
    report = store.report()
    assert report["data_quality"]["payout_net_mismatch"] == 1


def test_negative_money_is_rejected(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    with pytest.raises(ValueError):
        store.add_period(
            platform="Facebook", program="meta_content_monetization",
            period_start="2026-10-01", period_end="2026-10-31",
            estimated_net=-1,
        )
    with pytest.raises(ValueError):
        store.add_payout(
            platform="Facebook", program="meta_content_monetization",
            period_start="2026-10-01", period_end="2026-10-31",
            paid_at="2026-11-15", gross=10, fee=1, net=-1,
        )


def test_account_log_deduplicates_and_filters_other_business(tmp_path):
    tenant = _tenant(tmp_path)
    config = json.loads((tenant / "config.json").read_text(encoding="utf-8"))
    config["meta"] = {"business_id": "2294927867461766"}
    (tenant / "config.json").write_text(json.dumps(config), encoding="utf-8")
    log_path = tenant / "metrics" / "meta_monetization_log.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "Fecha,Plataforma,Business_ID,Posts_Analizados,Reacciones,Comentarios,Shares,Interacciones_Bonus_Elegibles\n"
        "2026-09-24,Facebook Page,2294927867461766,30,10,2,3,20\n"
        "2026-09-24,Facebook Page,2294927867461766,30,12,3,4,25\n"
        "2026-09-24,Facebook Page,1940942776222567,30,99,9,9,999\n"
        "2026-09-25,Facebook Page,2294927867461766,30,20,4,5,40\n",
        encoding="utf-8",
    )

    store = MonetizationStore("universe", base_path=tmp_path)
    first = store.import_account_log()
    second = store.import_account_log()

    assert first["rows"] == 2
    assert first["duplicates_collapsed"] == 1
    assert first["skipped_other_business"] == 1
    assert second["inserted"] == 0
    assert second["unchanged"] == 2
    account = [item for item in store.load_signals() if item.publication_id == "__account__"]
    assert [item.bonus_points for item in account] == [25, 40]

    report = store.report()
    assert report["signals"]["unique_posts"] == 0
    assert report["signals"]["account_rows"] == 2
    assert report["signals"]["account"]["date_end"] == "2026-09-25"
    assert report["signals"]["account"]["latest_bonus_points"] == 40
    assert report["signals"]["account"]["daily_bonus_points"] == 65
    assert report["by_series"] == {}


def test_account_signals_do_not_create_fake_posts(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    store.save_signals([
        MonetizationSignal(
            signal_id="MS-POST", tenant_id="universe", platform="Facebook",
            program="meta_content_monetization", signal_date="2026-10-01",
            publication_id="pub-1", bonus_points=10,
        ),
        MonetizationSignal(
            signal_id="MS-ACCOUNT", tenant_id="universe", platform="Facebook",
            program="meta_content_monetization", signal_date="2026-10-21",
            publication_id="__account__", series="Cuenta", character="Cuenta",
            reactions=584, comments=72, shares=84, bonus_points=740,
        ),
    ])

    report = store.report()

    assert report["signals"]["unique_posts"] == 1
    assert report["signals"]["date_end"] == "2026-10-21"
    assert report["signals"]["latest_bonus_points"] == 10
    assert report["signals"]["account"]["latest_bonus_points"] == 740
    assert set(report["by_series"]) == {"sin_serie"}


def test_confirmed_payout_is_recognized_without_estimated_period(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)
    store.add_payout(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-09-01",
        period_end="2026-09-30",
        paid_at="2026-09-30",
        gross=22.43,
        fee=0,
        net=22.43,
        source="meta_statement",
        evidence="Statement_375095669.pdf",
    )

    report = store.report()

    assert report["money"]["paid_net"] == 22.43
    assert report["money"]["recognized_net"] == 22.43
    assert report["money"]["payouts"]["count"] == 1


def test_payout_threshold_shows_unpaid_balance_and_shortfall(tmp_path):
    tenant = _tenant(tmp_path)
    _set_payout_threshold(tenant)
    store = MonetizationStore("universe", base_path=tmp_path)
    store.add_period(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-10-01",
        period_end="2026-10-31",
        estimated_net=4.74,
        status="estimated",
    )
    store.add_payout(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-09-01",
        period_end="2026-09-30",
        paid_at="2026-09-30",
        gross=22.43,
        fee=0,
        net=22.43,
    )

    report = store.report()
    threshold = report["money"]["payout_threshold"]

    assert threshold["amount"] == 25.0
    assert threshold["current_balance"] == 4.74
    assert threshold["remaining"] == 20.26
    assert threshold["reached"] is False
    assert report["money"]["recognized_net"] == 22.43


def test_payout_threshold_includes_approved_unpaid_and_reaches_limit(tmp_path):
    tenant = _tenant(tmp_path)
    _set_payout_threshold(tenant, amount=25.0)
    store = MonetizationStore("universe", base_path=tmp_path)
    store.add_period(
        platform="Facebook",
        program="meta_content_monetization",
        period_start="2026-10-01",
        period_end="2026-10-31",
        approved_net=25.0,
        status="approved",
    )

    report = store.report()
    threshold = report["money"]["payout_threshold"]

    assert threshold["current_balance"] == 25.0
    assert threshold["remaining"] == 0.0
    assert threshold["reached"] is True
    assert report["money"]["recognized_net"] == 0.0


def test_without_payout_threshold_report_omits_threshold(tmp_path):
    _tenant(tmp_path)
    store = MonetizationStore("universe", base_path=tmp_path)

    report = store.report()

    assert report["money"]["payout_threshold"] is None
