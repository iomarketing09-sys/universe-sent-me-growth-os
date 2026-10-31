"""Captura de Ads por anuncio, ledger diario y reporte."""

import csv
from datetime import date
from pathlib import Path

from modules.intelligence import ads_adapters, ads_ledger
from tools import ads_report


def _ad(**overrides):
    ad = {
        "campaign_id": "c1",
        "campaign_name": "Campaña",
        "adset_id": "as1",
        "id": "ad1",
        "name": "ARISHA",
        "status": "ACTIVE",
        "spend": 40.0,
        "impressions": 1000,
        "clicks": 50,
        "reach": 800,
        "ctr": 5.0,
        "cpc": 0.8,
        "conversations": 10,
        "cost_per_conversation": 4.0,
    }
    ad.update(overrides)
    return ad


def test_metric_row_extracts_conversations():
    row = ads_adapters._metric_row(
        {
            "spend": "12.5",
            "impressions": "500",
            "clicks": "25",
            "ctr": "5.0",
            "cpc": "0.5",
            "actions": [
                {"action_type": "onsite_conversion.messaging_conversation_started_7d", "value": "5"}
            ],
        },
        "ARISHA",
        "c1",
        "Campaña",
    )
    assert row["conversations"] == 5
    assert row["cost_per_conversation"] == 2.5
    assert row["spend"] == 12.5


def test_metric_row_without_conversations_does_not_divide_by_zero():
    row = ads_adapters._metric_row({"spend": "10"}, "Ad", "c1", "C")
    assert row["conversations"] == 0
    assert row["cost_per_conversation"] == 0.0


def test_capture_includes_ads(monkeypatch):
    calls = []

    class Response:
        def __init__(self, payload):
            self.payload = payload
            self.status_code = 200
            self.content = b"{}"

        def json(self):
            return self.payload

    def fake_get(url, params=None, timeout=None):
        calls.append((url, dict(params or {})))
        if url.endswith("/campaigns"):
            return Response({"data": [{"id": "c1", "name": "Campaña", "objective": "OUTCOME_TRAFFIC"}]})
        if url.endswith("/c1/insights"):
            return Response({"data": [{"spend": "10", "impressions": "100", "clicks": "5", "actions": [
                {"action_type": "onsite_conversion.messaging_conversation_started_7d", "value": "2"}
            ]}]})
        if url.endswith("/c1/ads"):
            return Response({"data": [{
                "id": "ad1", "name": "ARISHA", "status": "ACTIVE", "adset_id": "as1",
                "insights": {"data": [{"spend": "10", "impressions": "100", "clicks": "5", "actions": [
                    {"action_type": "onsite_conversion.messaging_conversation_started_7d", "value": "2"}
                ]}]},
            }]})
        return Response({"data": []})

    monkeypatch.setattr(ads_adapters, "_load_user_token", lambda: "token")
    monkeypatch.setattr("requests.get", fake_get)

    result = ads_adapters.capture_ads_insights({"ads": {"ad_account_id": "act_1"}})

    assert result["status"] == "success"
    assert len(result["ads"]) == 1
    assert result["ads"][0]["id"] == "ad1"
    assert result["ads"][0]["conversations"] == 2
    assert any(url.endswith("/c1/ads") for url, _ in calls)
    assert all(params.get("date_preset") == "maximum" for url, params in calls if "/insights" in url or url.endswith("/c1/ads"))


def test_ledger_is_idempotent_per_day(tmp_path: Path):
    path = ads_ledger.record_ad_insights("flexi", [_ad()], day=date(2026, 10, 30), base_path=tmp_path)
    ads_ledger.record_ad_insights("flexi", [_ad(spend=55.0)], day=date(2026, 10, 30), base_path=tmp_path)
    ads_ledger.record_ad_insights("flexi", [_ad(spend=70.0)], day=date(2026, 10, 31), base_path=tmp_path)

    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 2
    assert rows[0]["date"] == "2026-10-30"
    assert rows[0]["spend"] == "55.00"
    assert rows[1]["spend"] == "70.00"


def test_latest_by_ad_keeps_newest(tmp_path: Path):
    ads_ledger.record_ad_insights("flexi", [_ad(spend=10.0)], day=date(2026, 10, 30), base_path=tmp_path)
    ads_ledger.record_ad_insights("flexi", [_ad(spend=20.0)], day=date(2026, 10, 31), base_path=tmp_path)

    rows = ads_ledger.load_ad_insights("flexi", base_path=tmp_path)
    latest = ads_ledger.latest_by_ad(rows)

    assert len(latest) == 1
    assert latest[0]["spend"] == "20.00"


def test_ledger_defaults_to_project_root(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.setattr(ads_ledger, "_project_root", lambda: repo)
    monkeypatch.chdir(other)

    path = ads_ledger.record_ad_insights("flexi", [_ad()], day=date(2026, 10, 30))

    assert path == repo / "tenants" / "flexi" / "ads" / "insights" / "ad_insights_daily.csv"
    assert path.is_file()


def test_report_flags_ads_over_threshold():
    report = ads_report.build_report(
        [
            {"ad_id": "a1", "ad_name": "Caro", "spend": "90", "conversations": "10", "cost_per_conversation": "9", "ctr": "5"},
            {"ad_id": "a2", "ad_name": "Bueno", "spend": "40", "conversations": "10", "cost_per_conversation": "4", "ctr": "5"},
            {"ad_id": "a3", "ad_name": "Sin conversaciones", "spend": "20", "conversations": "0", "cost_per_conversation": "0", "ctr": "1"},
        ],
        8.0,
    )
    assert report["ads"][0]["ad_name"] == "Bueno"
    assert report["ads"][-1]["ad_name"] == "Sin conversaciones"
    assert report["alerts"] == ["Caro"]
    assert report["total_conversations"] == 20
    assert report["blended_cost_per_conversation"] == 7.5
