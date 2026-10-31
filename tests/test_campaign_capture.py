"""Programación idempotente de cortes E24/E48/E72/FINAL por campaña."""

import json
from datetime import datetime, timedelta
from pathlib import Path

import requests

from modules.intelligence import campaign_capture


START = datetime.fromisoformat("2026-10-30T17:36:37-05:00")
STOP = datetime.fromisoformat("2026-11-05T16:19:00-06:00")


def make_campaign_root(tmp_path: Path) -> Path:
    tenant = tmp_path / "tenants" / "flexi"
    (tenant / "ads" / "campanas" / "campaña-48h").mkdir(parents=True)
    (tenant / "config.json").write_text(
        json.dumps(
            {
                "tenant_id": "flexi",
                "client_name": "Flexi",
                "tenant_type": "physical_cro",
                "timezone": "America/Matamoros",
                "ads": {"ad_account_id": "act_1"},
            }
        ),
        encoding="utf-8",
    )
    (tenant / "ads" / "campanas" / "campaña-48h" / "meta_ids.json").write_text(
        json.dumps(
            {
                "campaign": {
                    "id": "cmp_1",
                    "name": "Flexi prueba",
                    "start_time": START.isoformat(),
                    "stop_time": STOP.isoformat(),
                },
                "adset": {"id": "set_1"},
            }
        ),
        encoding="utf-8",
    )
    (tenant / "ads" / "campanas" / "campaña-48h" / "campaign.json").write_text(
        json.dumps(
            {
                "slug": "campaña-48h",
                "published": {"campaign_id": "cmp_1", "adset_id": "set_old"},
            }
        ),
        encoding="utf-8",
    )
    return tmp_path


def fake_ads():
    return [
        {
            "campaign_id": "cmp_1",
            "campaign_name": "Flexi prueba",
            "adset_id": "set_1",
            "id": "ad_1",
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
    ]


def test_calendario_incluye_48h_diarios_y_final(tmp_path):
    root = make_campaign_root(tmp_path)
    campaign = campaign_capture.discover_campaigns(root)[0]
    points = campaign_capture.checkpoint_schedule(campaign)

    assert [point.label for point in points] == ["E24", "E48", "E72", "E96", "E120", "FINAL"]
    e48 = next(point for point in points if point.label == "E48")
    assert e48.due_at.isoformat() == "2026-11-01T16:36:37-06:00"


def test_no_captura_antes_de_24_horas(tmp_path):
    root = make_campaign_root(tmp_path)
    calls = []

    result = campaign_capture.run_due_captures(
        base_path=root,
        now=START + timedelta(hours=5),
        fetcher=lambda config: calls.append(config) or {"status": "success", "ads": []},
    )

    assert result["status"] == "no_due"
    assert calls == []


def test_captura_e48_es_idempotente_y_escribe_reporte(tmp_path):
    root = make_campaign_root(tmp_path)
    calls = []

    def fetcher(config):
        calls.append(config)
        return {"status": "success", "ads": fake_ads()}

    now = START + timedelta(hours=48, minutes=10)
    first = campaign_capture.run_due_captures(base_path=root, now=now, fetcher=fetcher)
    second = campaign_capture.run_due_captures(base_path=root, now=now, fetcher=fetcher)

    assert first["status"] == "success"
    assert second["status"] == "no_due"
    assert len(calls) == 1

    report_json = (
        root
        / "tenants"
        / "flexi"
        / "ads"
        / "insights"
        / "captures"
        / "campaña-48h"
        / "E48.json"
    )
    report_md = report_json.with_suffix(".md")
    payload = json.loads(report_json.read_text(encoding="utf-8"))
    assert payload["checkpoint"] == "E48"
    assert payload["total_conversations"] == 10
    assert payload["scheduled_elapsed_hours"] == 48.0
    assert payload["blended_cost_per_conversation"] == 4.0
    assert "E48" in report_md.read_text(encoding="utf-8")

    state = json.loads(
        (root / "tenants" / "flexi" / "ads" / "insights" / "capture_state.json").read_text(
            encoding="utf-8"
        )
    )
    assert state["campaigns"]["campaña-48h"]["checkpoints"]["E48"]["status"] == "captured"


def test_captura_genera_plan_sin_red_y_usa_la_hora_del_corte(tmp_path, monkeypatch):
    root = make_campaign_root(tmp_path)

    def fail_network(*args, **kwargs):
        raise AssertionError("El plan no debe llamar a Meta")

    monkeypatch.setattr(requests, "get", fail_network)
    monkeypatch.setattr(requests, "post", fail_network)

    ad = fake_ads()[0]
    ad.update({"spend": 100.0, "conversations": 4, "cost_per_conversation": 25.0})
    now = START + timedelta(hours=50)
    result = campaign_capture.run_due_captures(
        base_path=root,
        now=now,
        fetcher=lambda config: {"status": "success", "ads": [ad]},
    )

    assert result["status"] == "success"
    plan_path = (
        root
        / "tenants"
        / "flexi"
        / "ads"
        / "plans"
        / "campaña-48h"
        / "E48.json"
    )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert plan["elapsed_hours"] == 48.0
    assert plan["capture_elapsed_hours"] == 50.0
    assert plan["actions"][0]["action"] == "watch"
    assert plan["execution_allowed"] is False
    assert plan["writes_to_meta"] is False
    assert plan["metadata_reconciliation"]["status"] == "reconciled"
    assert plan_path.with_suffix(".md").is_file()

    spec = json.loads(
        (
            root
            / "tenants"
            / "flexi"
            / "ads"
            / "campanas"
            / "campaña-48h"
            / "campaign.json"
        ).read_text(encoding="utf-8")
    )
    assert spec["published"]["adset_id"] == "set_1"
    assert spec["metadata_reconciliation"]["changes"][0]["previous"] == "set_old"

    state = json.loads(
        (root / "tenants" / "flexi" / "ads" / "insights" / "capture_state.json").read_text(
            encoding="utf-8"
        )
    )
    artifacts = state["campaigns"]["campaña-48h"]["checkpoints"]["E48"]["artifacts"]
    assert "tenants/flexi/ads/plans/campaña-48h/E48.json" in artifacts
    assert "tenants/flexi/ads/campanas/campaña-48h/campaign.json" in artifacts


def test_reconciliacion_bloquea_si_hay_varios_adsets(tmp_path):
    root = make_campaign_root(tmp_path)
    campaign = campaign_capture.discover_campaigns(root)[0]
    other_ad = {**fake_ads()[0], "id": "ad_2", "adset_id": "set_2"}

    result = campaign_capture.reconcile_campaign_metadata(
        campaign,
        root,
        ads=[*fake_ads(), other_ad],
        now=START + timedelta(hours=48),
    )

    assert result["status"] == "blocked"
    assert result["execution_blocked"] is True
    spec = json.loads(
        (
            root
            / "tenants"
            / "flexi"
            / "ads"
            / "campanas"
            / "campaña-48h"
            / "campaign.json"
        ).read_text(encoding="utf-8")
    )
    assert spec["published"]["adset_id"] == "set_old"


def test_error_de_meta_no_avanza_estado(tmp_path):
    root = make_campaign_root(tmp_path)
    calls = []

    def fetcher(config):
        calls.append(config)
        return {"status": "error", "note": "Meta no disponible"}

    now = START + timedelta(hours=48)
    first = campaign_capture.run_due_captures(base_path=root, now=now, fetcher=fetcher)
    second = campaign_capture.run_due_captures(base_path=root, now=now, fetcher=fetcher)

    assert first["status"] == "error"
    assert second["status"] == "error"
    assert len(calls) == 2
    assert not (
        root / "tenants" / "flexi" / "ads" / "insights" / "capture_state.json"
    ).exists()


def test_captura_retrasada_marca_anteriores_como_perdidas(tmp_path):
    root = make_campaign_root(tmp_path)

    result = campaign_capture.run_due_captures(
        base_path=root,
        now=START + timedelta(hours=50),
        fetcher=lambda config: {"status": "success", "ads": fake_ads()},
    )

    assert result["status"] == "success"
    state = json.loads(
        (root / "tenants" / "flexi" / "ads" / "insights" / "capture_state.json").read_text(
            encoding="utf-8"
        )
    )
    checkpoints = state["campaigns"]["campaña-48h"]["checkpoints"]
    assert checkpoints["E24"]["status"] == "missed"
    assert checkpoints["E48"]["status"] == "captured"


def test_campana_reemplazada_con_mismo_slug_vuelve_a_capturar(tmp_path):
    root = make_campaign_root(tmp_path)
    meta_path = root / "tenants" / "flexi" / "ads" / "campanas" / "campaña-48h" / "meta_ids.json"
    now = START + timedelta(hours=48)
    calls = []

    def fetcher(config):
        calls.append(config)
        return {"status": "success", "ads": fake_ads()}

    campaign_capture.run_due_captures(base_path=root, now=now, fetcher=fetcher)
    payload = json.loads(meta_path.read_text(encoding="utf-8"))
    payload["campaign"]["id"] = "cmp_2"
    meta_path.write_text(json.dumps(payload), encoding="utf-8")

    result = campaign_capture.run_due_captures(base_path=root, now=now, fetcher=fetcher)

    assert result["status"] == "success"
    assert len(calls) == 2
