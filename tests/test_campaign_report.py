"""Tests del reporte unificado de campaña."""

import json

import pytest

from modules.intelligence import campaign_report


TENANT = "flexi"
SLUG = "2026-11_flexi_ads_560mxn"


def _meta_ids():
    return {
        "campaign": {
            "id": "120247658527630665",
            "name": "Flexi OI26 · WhatsApp · Piedras Negras",
            "status": "ACTIVE",
            "effective_status": "ACTIVE",
            "lifetime_budget": 56000,
            "start_time": "2026-10-30T17:36:37-0500",
            "stop_time": "2026-11-05T16:19:00-0600",
        },
        "ads": [
            {"id": "izadora", "name": "Izadora"},
            {"id": "amalia", "name": "Amalia de Quirelli"},
        ],
    }


def _capture(checkpoint="E72"):
    return {
        "tenant_id": TENANT,
        "campaign_slug": SLUG,
        "campaign_id": "120247658527630665",
        "campaign_name": "Flexi OI26 · WhatsApp · Piedras Negras",
        "checkpoint": checkpoint,
        "scheduled_for": "2026-11-02T16:36:37-06:00",
        "captured_at": "2026-11-02T16:46:45-06:00",
        "elapsed_hours": 72.2,
        "ads": [
            {
                "ad_id": "izadora",
                "ad_name": "Izadora",
                "status": "ACTIVE",
                "spend": 141.20,
                "impressions": 5926,
                "clicks": 396,
                "ctr": 6.68,
                "conversations": 21,
                "cost_per_conversation": 6.72,
            },
            {
                "ad_id": "amalia",
                "ad_name": "Amalia de Quirelli",
                "status": "PAUSED",
                "spend": 30.56,
                "impressions": 1482,
                "clicks": 94,
                "ctr": 6.34,
                "conversations": 3,
                "cost_per_conversation": 10.19,
            },
        ],
        "total_spend": 171.76,
        "total_conversations": 24,
        "blended_cost_per_conversation": 7.16,
    }


def _provider(conversations):
    def provide(tenant_id, limit=1000, base_path=None):
        return {"tenant_id": tenant_id, "conversations": conversations}

    return provide


def _write_campaign(tmp_path, checkpoint="E72", capture=None):
    directory = tmp_path / "tenants" / TENANT / "ads" / "campanas" / SLUG
    directory.mkdir(parents=True)
    (directory / "meta_ids.json").write_text(json.dumps(_meta_ids()), encoding="utf-8")
    captures = tmp_path / "tenants" / TENANT / "ads" / "insights" / "captures" / SLUG
    captures.mkdir(parents=True)
    payload = capture or _capture(checkpoint)
    (captures / f"{checkpoint}.json").write_text(json.dumps(payload), encoding="utf-8")
    return directory


def _conversation(ad_id, first_at="2026-11-01T12:00:00Z", depth=3, contact="…1234"):
    return {
        "from_ad": True,
        "ad_id": ad_id,
        "first_at": first_at,
        "depth": depth,
        "contact": contact,
        "contact_name": "Cliente",
    }


class TestLatestCapture:
    def test_uses_latest_file_or_explicit_checkpoint(self, tmp_path):
        directory = _write_campaign(tmp_path)
        captures = tmp_path / "tenants" / TENANT / "ads" / "insights" / "captures" / SLUG
        (captures / "E48.json").write_text(json.dumps(_capture("E48")), encoding="utf-8")

        _, payload = campaign_report.latest_capture(TENANT, SLUG, tmp_path)
        _, forced = campaign_report.latest_capture(TENANT, SLUG, tmp_path, "E48")

        assert payload["checkpoint"] in {"E72", "E48"}
        assert forced["checkpoint"] == "E48"
        assert directory.is_dir()

    def test_missing_capture_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            campaign_report.latest_capture(TENANT, SLUG, tmp_path)


class TestConversations:
    def test_filters_by_ad_and_start(self):
        provider = _provider(
            [
                _conversation("izadora", contact="…1111"),
                _conversation("amalia", contact="…2222"),
                _conversation("otra-campana"),
                {**_conversation("izadora"), "from_ad": False},
                _conversation("izadora", first_at="2026-10-01T12:00:00Z"),
            ]
        )
        since = campaign_report._campaign_start(_meta_ids())
        result = campaign_report.collect_conversations(
            TENANT, ["izadora", "amalia"], since, provider=provider
        )

        assert result["total"] == 2
        assert result["per_ad"] == {"izadora": 1, "amalia": 1}
        assert result["depth"]["3+"] == 2

    def test_provider_failure_degrades(self):
        def broken(*args, **kwargs):
            raise RuntimeError("sin D1")

        result = campaign_report.collect_conversations(TENANT, ["izadora"], provider=broken)

        assert result["available"] is False
        assert result["total"] == 0


class TestReports:
    def test_client_report_is_business_facing(self, tmp_path):
        _write_campaign(tmp_path)
        bundle = campaign_report.build_bundle(
            TENANT,
            SLUG,
            base_path=tmp_path,
            provider=_provider([
                _conversation("izadora", contact="…1111"),
                _conversation("amalia", depth=1, contact="…2222"),
            ]),
        )
        text = campaign_report.build_client_report(bundle)

        assert "Personas por WhatsApp (mismo corte) | 2" in text
        assert "Conversaciones reportadas por Meta | 24" in text
        assert "Izadora" in text
        assert "$560.00" in text
        assert "izadora" not in text
        assert "ad_id" not in text

    def test_internal_report_has_ids(self, tmp_path):
        _write_campaign(tmp_path)
        bundle = campaign_report.build_bundle(
            TENANT,
            SLUG,
            base_path=tmp_path,
            provider=_provider([_conversation("izadora")]),
        )
        text = campaign_report.build_internal_report(bundle)

        assert "120247658527630665" in text
        assert "izadora" in text
        assert "Discrepancias" in text

    def test_write_reports_creates_both_files(self, tmp_path):
        _write_campaign(tmp_path)
        bundle = campaign_report.build_bundle(
            TENANT, SLUG, base_path=tmp_path, provider=_provider([_conversation("izadora")])
        )
        client, internal, page = campaign_report.write_reports(bundle, tmp_path)

        assert client.is_file() and client.name == "reporte_cliente.md"
        assert internal.is_file() and internal.name == "reporte_interno.md"
        assert page.is_file() and page.name == "reporte_cliente.html"
        html = page.read_text(encoding="utf-8")
        assert "personas escribieron desde un anuncio" in html
        assert "izadora" not in html
