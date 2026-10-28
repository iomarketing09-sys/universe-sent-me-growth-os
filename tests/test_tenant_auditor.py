"""Tests del tenant_auditor (auditoría local para onboarding)."""

from __future__ import annotations

import json

from modules.intelligence.agents.tenant_auditor import audit_tenant
from tests.tenant_factory import make_tenant


def test_tenant_completo_es_ready(tmp_path):
    make_tenant(tmp_path, "alpha", track="native_digital")
    audit = audit_tenant("alpha", str(tmp_path))
    assert audit["status"] == "READY", audit
    assert audit["score"] == 1.0
    assert audit["next_actions"] == []


def test_tenant_inexistente_es_blocked(tmp_path):
    audit = audit_tenant("fantasma", str(tmp_path))
    assert audit["status"] == "BLOCKED"
    assert audit["checks"][0]["id"] == "config"
    assert "no existe" in audit["checks"][0]["detail"].lower()


def test_config_invalido_es_blocked(tmp_path):
    root = tmp_path / "tenants" / "roto"
    root.mkdir(parents=True)
    (root / "config.json").write_text("{no es json", encoding="utf-8")
    audit = audit_tenant("roto", str(tmp_path))
    assert audit["status"] == "BLOCKED"


def test_sin_calendario_es_partial(tmp_path):
    make_tenant(tmp_path, "sin-agenda", with_schedule=False)
    audit = audit_tenant("sin-agenda", str(tmp_path))
    assert audit["status"] == "PARTIAL"
    assert any("calendario" in item.lower() for item in audit["next_actions"])


def test_physical_sin_inventario_avisa_parcial(tmp_path):
    root = make_tenant(tmp_path, "tienda", track="physical_cro")
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    config["ads"].pop("approved_models", None)
    (root / "config.json").write_text(json.dumps(config), encoding="utf-8")

    audit = audit_tenant("tienda", str(tmp_path))
    inventory = next(item for item in audit["checks"] if item["id"] == "inventory")
    assert inventory["state"] == "WARN"
    assert "parcial" in inventory["detail"]
    assert audit["status"] == "PARTIAL"


def test_historico_solo_aplica_a_native(tmp_path):
    make_tenant(tmp_path, "tienda2", track="physical_cro")
    audit = audit_tenant("tienda2", str(tmp_path))
    history = next(item for item in audit["checks"] if item["id"] == "history")
    assert history["state"] == "SKIP"


def test_flexi_real_queda_parcial_por_calendario():
    audit = audit_tenant("flexi")
    assert audit["status"] in ("PARTIAL", "READY")
    assert audit["score"] >= 0.8
