"""Tests del orquestador CGO."""

from __future__ import annotations

import json

import pytest

from modules.cgo import CgoOrchestrator
from modules.cgo.__main__ import main as cgo_main
from modules.cgo.tracks import (
    NATIVE_DIGITAL,
    PHYSICAL_CRO,
    UNKNOWN,
    capability_allowed,
    tenant_track,
)
from tests.tenant_factory import make_tenant


def ctx(**kwargs):
    return CgoOrchestrator(**kwargs)


# --------------------------------------------------------------------- tracks
def test_tracks_por_tenant(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    make_tenant(tmp_path, "tienda", track="physical_cro")
    assert tenant_track("digital", tmp_path) == NATIVE_DIGITAL
    assert tenant_track("tienda", tmp_path) == PHYSICAL_CRO
    assert tenant_track("no-existe", tmp_path) == UNKNOWN


def test_capacidades_por_track():
    assert capability_allowed("weekly_calendar", NATIVE_DIGITAL)
    assert not capability_allowed("weekly_calendar", PHYSICAL_CRO)
    assert capability_allowed("daily_pipeline", PHYSICAL_CRO)


# ------------------------------------------------------------- daily pipeline
def test_daily_pipeline_ok(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    result = ctx(base_path=str(tmp_path)).run_one("daily_pipeline", "digital")
    assert result.status == "OK", result.to_dict()
    kinds = {item["kind"] for item in result.actions}
    assert {"snapshot", "schedule", "publication_log", "ads"} <= kinds
    assert result.data["schedule_rows"] == 3


def test_daily_pipeline_sin_calendario_es_partial(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital", with_schedule=False)
    result = ctx(base_path=str(tmp_path)).run_one("daily_pipeline", "digital")
    assert result.status == "PARTIAL"
    assert any("calendario" in item.lower() for item in result.next_actions)


# ------------------------------------------------------------ weekly calendar
def test_weekly_calendar_bloqueado_en_physical(tmp_path):
    make_tenant(tmp_path, "tienda", track="physical_cro")
    result = ctx(base_path=str(tmp_path)).run_one("weekly_calendar", "tienda")
    assert result.status == "BLOCKED"
    assert any(gate.name == "track" and gate.state == "FAIL" for gate in result.gates)


def test_weekly_calendar_native_cuenta_slots(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    result = ctx(base_path=str(tmp_path)).run_one("weekly_calendar", "digital")
    assert result.status == "OK", result.to_dict()
    assert result.data["counts"] == {"photo": 2, "text": 1}


# ------------------------------------------------------------ meta publishing
def test_meta_publishing_dry_run_no_publica(tmp_path, monkeypatch):
    import modules.social as social

    make_tenant(tmp_path, "tienda", track="physical_cro")

    def explotar(*args, **kwargs):
        raise AssertionError("no debe publicar en dry-run")

    monkeypatch.setattr(social, "IgScheduler", explotar)
    monkeypatch.setattr(social, "publish_schedule_from_dryrun", explotar)

    result = ctx(base_path=str(tmp_path)).run_one("meta_publishing", "tienda")
    routes = {item.get("platform"): item.get("route") for item in result.actions}
    assert routes["facebook"] == "native_scheduled"
    assert routes["instagram"] == "queued_for_cron"
    assert result.dry_run is True


def test_meta_publishing_publish_sin_token_bloquea(tmp_path, monkeypatch):
    import modules.cgo.gates as gates

    make_tenant(tmp_path, "tienda", track="physical_cro")
    monkeypatch.setattr(gates, "has_token", lambda ctx, tenant_id: False)

    result = ctx(base_path=str(tmp_path), dry_run=False, publish=True).run_one(
        "meta_publishing", "tienda"
    )
    assert result.status == "BLOCKED"
    assert any(gate.name == "token" and gate.state == "FAIL" for gate in result.gates)


def test_meta_publishing_publica_con_token(tmp_path, monkeypatch):
    import modules.cgo.capabilities.meta_publishing as publishing
    import modules.cgo.gates as gates

    make_tenant(tmp_path, "tienda", track="physical_cro")
    monkeypatch.setattr(gates, "has_token", lambda ctx, tenant_id: True)
    monkeypatch.setattr(
        publishing, "_publish_instagram", lambda ctx, tenant_id: {"published": 2}
    )
    monkeypatch.setattr(
        publishing, "_publish_facebook", lambda ctx, tenant_id: {"total": 1, "ok": 1}
    )

    result = ctx(base_path=str(tmp_path), dry_run=False, publish=True).run_one(
        "meta_publishing", "tienda"
    )
    assert result.status == "OK", result.to_dict()
    assert result.artifacts == ["publication_log:tienda"]


# ---------------------------------------------------------------- canon sync
def test_canon_sync_no_configurado(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    result = ctx(base_path=str(tmp_path)).run_one("canon_sync", "digital")
    assert result.status == "NOT_CONFIGURED"
    assert result.next_actions


def test_canon_sync_detecta_directorio(tmp_path):
    root = make_tenant(tmp_path, "digital", track="native_digital")
    canon = root / "canon"
    canon.mkdir()
    (canon / "governance.md").write_text("# canon", encoding="utf-8")

    result = ctx(base_path=str(tmp_path)).run_one("canon_sync", "digital")
    assert result.status == "OK", result.to_dict()
    assert result.data["canon_path"].endswith("canon")


# -------------------------------------------------------------- onboarding
def test_onboarding_reporta_checks(tmp_path):
    make_tenant(tmp_path, "tienda", track="physical_cro")
    result = ctx(base_path=str(tmp_path)).run_one("tenant_onboarding", "tienda")
    assert result.status == "OK", result.to_dict()
    assert any(item["kind"].startswith("check:") for item in result.actions)


# -------------------------------------------------------- cross-tenant report
def test_cross_tenant_agrega_totales(tmp_path):
    make_tenant(tmp_path, "uno", track="native_digital")
    make_tenant(tmp_path, "dos", track="physical_cro")
    result = ctx(base_path=str(tmp_path)).run_one("cross_tenant_report")
    assert result.status == "OK", result.to_dict()
    assert result.data["totals"]["spend"] == 200.0
    assert result.data["totals"]["conversations"] == 20
    assert set(result.data["tenants"]) == {"uno", "dos"}


# --------------------------------------------------------------- verify setup
def test_verify_setup_sin_env_es_partial(tmp_path):
    make_tenant(tmp_path, "uno", track="native_digital")
    result = ctx(base_path=str(tmp_path)).run_one("verify_setup")
    assert result.status == "PARTIAL"
    assert all(
        item["status"] == "ok"
        for item in result.actions
        if item["kind"].startswith("module:")
    )


# --------------------------------------------------------------- orchestrator
def test_capacidad_desconocida_falla(tmp_path):
    make_tenant(tmp_path, "uno", track="native_digital")
    with pytest.raises(ValueError):
        ctx(base_path=str(tmp_path)).run("no_existe", "uno")


def test_strict_convierte_unknown_en_blocked(tmp_path):
    root = make_tenant(tmp_path, "uno", track="native_digital")
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    config.pop("client_name")
    (root / "config.json").write_text(json.dumps(config), encoding="utf-8")

    normal = ctx(base_path=str(tmp_path)).run_one("daily_pipeline", "uno")
    strict = ctx(base_path=str(tmp_path), strict=True).run_one("daily_pipeline", "uno")
    assert normal.status == "PARTIAL"
    assert strict.status == "BLOCKED"
    assert "strict" in strict.reason


def test_cli_json(capsys):
    code = cgo_main(["--mode", "verify_setup", "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert code == 0
    assert payload[0]["capability"] == "verify_setup"
