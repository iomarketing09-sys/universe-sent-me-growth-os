"""Tests del módulo intelligence: shims, KPIs y Meta Ads Agent (sin red)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import growth.audit as growth_audit
import growth.integrations.ads_adapters as growth_ads
import growth.metrics_snapshot as growth_metrics
import growth.planner as growth_planner
import modules.intelligence as intelligence
from modules.intelligence.agents.meta_ads_agent.agent import MetaAdsAgent


CAMPAIGN = {
    "id": "120247452749050665",
    "name": "2026-10_flexi_ads_500mxn",
    "objective": "OUTCOME_TRAFFIC",
    "status": "ACTIVE",
    "spend": 439.28,
    "impressions": 12772,
    "clicks": 999,
    "reach": 6653,
    "ctr": 7.82,
    "cpc": 0.44,
    "cpm": 34.39,
    "conversations": 79,
    "messaging_metrics": {"messaging_user_depth_2": 0},
}


def _tenant(tmp_path: Path, campaigns=None, with_snapshot: bool = True) -> Path:
    root = tmp_path
    tenant = root / "tenants" / "flexi"
    tenant.mkdir(parents=True)
    (tenant / "config.json").write_text(
        json.dumps({"ads": {"ad_account_id": "act_123"}}), encoding="utf-8"
    )
    if with_snapshot:
        sync_dir = tenant / "data" / "sync"
        sync_dir.mkdir(parents=True)
        (sync_dir / "latest.json").write_text(
            json.dumps({"sources": {"ads": {"campaigns": campaigns or [CAMPAIGN]}}}),
            encoding="utf-8",
        )
    return root


def test_shims_apuntan_al_modulo_nuevo():
    from modules.intelligence import ads_adapters, metrics_snapshot, planner

    assert growth_planner.build_schedule is planner.build_schedule
    assert growth_metrics.MetricsSnapshot is metrics_snapshot.MetricsSnapshot
    assert growth_audit.run_audit is intelligence.run_audit
    assert growth_ads.capture_ads_insights is ads_adapters.capture_ads_insights


def test_modulo_expone_api_publica():
    assert "MetaAdsAgent" in intelligence.__all__
    for name in intelligence.__all__:
        assert getattr(intelligence, name) is not None


def test_kpis_calculan_costo_por_conversacion():
    kpis = MetaAdsAgent._kpis(CAMPAIGN)
    assert kpis["cost_per_conversation"] == pytest.approx(5.56, abs=0.01)
    assert kpis["click_to_conversation"] == pytest.approx(12.65, abs=0.01)
    assert kpis["spend"] == 439.28


def test_offline_lee_el_snapshot_del_sync(tmp_path):
    root = _tenant(tmp_path)
    agent = MetaAdsAgent("flexi", base_path=str(root))

    report = agent.report(offline=True)

    assert report["source"] == "snapshot"
    assert report["totals"]["spend"] == 439.28
    assert report["totals"]["conversations"] == 79
    assert report["campaigns"][0]["name"] == CAMPAIGN["name"]


def test_filtro_por_campana(tmp_path):
    root = _tenant(tmp_path, campaigns=[CAMPAIGN, {**CAMPAIGN, "id": "2", "name": "otra_campana"}])
    agent = MetaAdsAgent("flexi", base_path=str(root))

    report = agent.report(offline=True, campaign_slug="2026-10_flexi")

    assert len(report["campaigns"]) == 1
    assert report["campaigns"][0]["id"] == CAMPAIGN["id"]


def test_fetcher_inyectado_no_usa_red(tmp_path):
    root = _tenant(tmp_path)
    calls = []

    def fake_fetcher(config):
        calls.append(config)
        return {"campaigns": [CAMPAIGN]}

    agent = MetaAdsAgent("flexi", base_path=str(root), fetcher=fake_fetcher)
    report = agent.report()

    assert calls and calls[0]["ads"]["ad_account_id"] == "act_123"
    assert report["source"] == "marketing_api"
    assert report["totals"]["clicks"] == 999


def test_tenant_sin_config_falla_con_mensaje_claro(tmp_path):
    agent = MetaAdsAgent("inexistente", base_path=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        agent.load_config()


def test_avisa_que_meta_no_reporta_profundidad(tmp_path):
    root = _tenant(tmp_path)
    report = MetaAdsAgent("flexi", base_path=str(root)).report(offline=True)
    assert any("profundidad" in note for note in report["notes"])
