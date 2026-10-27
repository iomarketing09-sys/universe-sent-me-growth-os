"""Tests del módulo communications: D1, conversaciones y ecos (sin red)."""

from __future__ import annotations

import json

import pytest

from modules.communications.whatsapp import conversations, d1, echo_diagnostics


def test_d1_rechaza_consultas_de_escritura():
    with pytest.raises(d1.D1Error):
        d1.query("DELETE FROM events")
    with pytest.raises(d1.D1Error):
        d1.query("UPDATE events SET status = 'x'")


def test_d1_permite_select_y_with():
    assert d1._validate("SELECT 1") == "SELECT 1"
    assert d1._validate("  with x as (select 1) select * from x").strip().lower().startswith("with")


def test_conversation_summary_mapea_y_enmascara(monkeypatch):
    rows = [
        {
            "contact_name": "Luz",
            "contact_last4": "5292",
            "first_at": "2026-10-19T18:25:02Z",
            "last_at": "2026-10-27T20:17:13Z",
            "inbound": 39,
            "outbound_app": 0,
            "statuses": 52,
            "from_ad": 1,
            "ad_id": "120247453536330665",
            "ad_headline": "Distribuidor Oficial Flexi",
        }
    ]
    monkeypatch.setattr(d1, "query", lambda *a, **k: rows)
    result = conversations.conversation_summary("flexi", limit=1)
    assert result["total"] == 1
    convo = result["conversations"][0]
    assert convo["contact"] == "…5292"
    assert convo["depth"] == 39
    assert convo["from_ad"] is True


def test_conversation_summary_degrada_sin_columnas_referral(monkeypatch):
    def fake_query(sql, **kwargs):
        if "referral" in sql:
            raise d1.D1Error("D1 rechazó la consulta: no such column: referral_source_id")
        return [{"contact_last4": "1111", "inbound": 2}]

    monkeypatch.setattr(d1, "query", fake_query)
    result = conversations.conversation_summary("flexi")
    assert result["warnings"], "debe avisar que no hay atribución"
    assert result["conversations"][0]["from_ad"] is False


def test_depth_distribution_agrupa_en_tres_buckets(monkeypatch):
    rows = [
        {"inbound": 1, "conversations": 8},
        {"inbound": 2, "conversations": 7},
        {"inbound": 3, "conversations": 4},
        {"inbound": 5, "conversations": 2},
    ]
    monkeypatch.setattr(d1, "query", lambda *a, **k: rows)
    result = conversations.depth_distribution("flexi")
    assert result["buckets"] == {"1": 8, "2": 7, "3+": 6}
    assert result["conversations"] == 21
    assert result["average_depth"] == pytest.approx(2.1, abs=0.01)


def test_campaign_conversations_sin_referral_devuelve_no_disponible(monkeypatch):
    def fake_query(sql, **kwargs):
        raise d1.D1Error("no such column: referral_source_id")

    monkeypatch.setattr(d1, "query", fake_query)
    result = conversations.campaign_conversations("flexi")
    assert result["available"] is False
    assert result["campaigns"] == []
    assert result["warnings"]


def _fake_d1(monkeypatch, echoes_payload=True):
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {},
                            "messages": [],
                            "message_echoes": [{"id": "wamid.1", "type": "text"}]
                            if echoes_payload
                            else [],
                        }
                    }
                ]
            }
        ]
    }

    def fake_query(sql, **kwargs):
        if "GROUP BY direction" in sql:
            return [{"direction": "in", "n": 10}, {"direction": "out_app", "n": 0}]
        if "FROM events WHERE direction = 'status'" in sql:
            return [{"status": "delivered", "n": 4}]
        if "FROM raw_events" in sql:
            return [{"payload": json.dumps(payload)}]
        return []

    monkeypatch.setattr(d1, "query", fake_query)


def test_echo_diagnostico_detecta_ecos_perdidos(monkeypatch):
    _fake_d1(monkeypatch, echoes_payload=True)
    result = echo_diagnostics.diagnose_echoes("flexi", check_graph=False)
    assert result.outcome == "echoes_dropped_by_worker"
    assert result.payloads_with_echoes == 1
    assert result.echoes_stored == 0
    assert any("message_echoes" in finding for finding in result.findings)


def test_echo_diagnostico_sin_red_ni_ecos_no_afirma_bloqueo(monkeypatch):
    _fake_d1(monkeypatch, echoes_payload=False)
    result = echo_diagnostics.diagnose_echoes("flexi", check_graph=False)
    assert result.outcome == "subscription_not_checked"


def test_modulo_expone_whatsapp_agent():
    import modules.communications as communications

    assert "diagnose_echoes" in communications.__all__
    from modules.communications.whatsapp.agent import WhatsAppAgent

    assert WhatsAppAgent("flexi").tenant_id == "flexi"
