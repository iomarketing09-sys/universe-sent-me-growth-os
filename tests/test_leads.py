"""Leads Lite: intención, aislamiento por tenant y reporte sin ventas."""

import json
from datetime import date, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from growthos.core.models import Lead
from modules.intelligence.leads import LeadStore, summarize_leads


def _tenant(root: Path, tenant_id: str) -> Path:
    tenant = root / "tenants" / tenant_id
    tenant.mkdir(parents=True)
    (tenant / "config.json").write_text(
        json.dumps(
            {
                "tenant_id": tenant_id,
                "client_name": tenant_id,
                "timezone": "America/Matamoros",
                "contact_channel": "WhatsApp",
                "tenant_type": "physical_cro",
            }
        ),
        encoding="utf-8",
    )
    return tenant


def test_add_lead_and_report(tmp_path: Path):
    _tenant(tmp_path, "flexi")
    store = LeadStore("flexi", base_path=tmp_path)

    lead = store.add(
        contact_name="Cliente",
        phone="8781234567",
        source="whatsapp",
        intent="caliente",
        product_interest="Botines Quirelli",
        campaign_id="2026-10_flexi_ads_500mxn",
    )

    assert lead.lead_id == "L-0001"
    assert lead.intent == "caliente"
    assert lead.status == "nuevo"
    assert lead.lead_source == "WhatsApp"

    report = store.report()
    assert report["leads"] == 1
    assert report["hot"] == 1
    assert report["by_intent"] == {"caliente": 1}
    assert report["by_source"] == {"WhatsApp": 1}


def test_update_intent_and_status(tmp_path: Path):
    _tenant(tmp_path, "flexi")
    store = LeadStore("flexi", base_path=tmp_path)
    store.add(contact_name="Cliente", intent="frio", status="nuevo")

    updated = store.update("L-0001", intent="tibio", status="cotizado")

    assert updated.intent == "tibio"
    assert updated.status == "cotizado"
    assert store.report()["quote_rate"] == 1.0


def test_followups_due_and_new_last_7d(tmp_path: Path):
    _tenant(tmp_path, "flexi")
    store = LeadStore("flexi", base_path=tmp_path)

    store.add(
        contact_name="A",
        next_action_at=date.today() - timedelta(days=1),
    )
    store.add(
        contact_name="B",
        created_at=date.today() - timedelta(days=30),
        status="perdido",
        lost_reason="sin_respuesta",
    )

    report = store.report()
    assert report["followups_due"] == 1
    assert report["new_last_7d"] == 1
    assert report["lost"] == 1


def test_tenant_isolation(tmp_path: Path):
    _tenant(tmp_path, "flexi")
    _tenant(tmp_path, "micas-art-deco")

    LeadStore("flexi", base_path=tmp_path).add(contact_name="Flexi")
    LeadStore("micas-art-deco", base_path=tmp_path).add(contact_name="Mica")

    assert LeadStore("flexi", base_path=tmp_path).report()["leads"] == 1
    assert LeadStore("micas-art-deco", base_path=tmp_path).report()["leads"] == 1
    assert LeadStore("flexi", base_path=tmp_path).load()[0].contact_name == "Flexi"


def test_invalid_intent_rejected(tmp_path: Path):
    _tenant(tmp_path, "flexi")
    store = LeadStore("flexi", base_path=tmp_path)

    with pytest.raises(ValueError):
        store.add(contact_name="Cliente", intent="urgente")


def test_lead_requires_identification():
    with pytest.raises(ValidationError):
        Lead(lead_id="L-0001", tenant_id="flexi")


def test_csv_roundtrip_preserves_fields(tmp_path: Path):
    _tenant(tmp_path, "flexi")
    store = LeadStore("flexi", base_path=tmp_path)
    store.add(
        contact_name="Cliente",
        phone="8781234567",
        source="facebook",
        intent="tibio",
        status="contactado",
        product_interest="Botas altas",
        budget_range="1000-1500",
        publication_id="123_456",
        campaign_id="2026-10_flexi_ads_500mxn",
        conversation_id="conv-1",
        notes="Pidió talla 25",
        assigned_to="Ale",
        next_action_at=date.today() + timedelta(days=2),
    )

    reloaded = LeadStore("flexi", base_path=tmp_path).load()
    assert len(reloaded) == 1
    lead = reloaded[0]
    assert lead.contact_phone == "8781234567"
    assert lead.source_conversation_id == "conv-1"
    assert lead.lead_source == "Facebook"
    assert lead.next_action_at == date.today() + timedelta(days=2)


def test_filters_by_intent_and_status(tmp_path: Path):
    _tenant(tmp_path, "flexi")
    store = LeadStore("flexi", base_path=tmp_path)
    store.add(contact_name="A", intent="caliente", status="cotizado")
    store.add(contact_name="B", intent="frio", status="nuevo")

    assert [lead.contact_name for lead in store.filtered(intent="caliente")] == ["A"]
    assert [lead.contact_name for lead in store.filtered(status="nuevo")] == ["B"]


def test_empty_report():
    report = summarize_leads([], tenant_id="flexi")
    assert report["leads"] == 0
    assert report["hot_rate"] == 0.0
    assert report["by_intent"] == {}
