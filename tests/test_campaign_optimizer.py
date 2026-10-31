"""Planes de cambio auditables: recomiendan, nunca ejecutan."""

from modules.intelligence.campaign_optimizer import build_change_plan, render_plan_markdown


def bad_ad(**overrides):
    ad = {
        "ad_id": "ad_1",
        "ad_name": "ARISHA",
        "spend": 100.0,
        "impressions": 5000,
        "clicks": 100,
        "ctr": 2.0,
        "conversations": 4,
        "cost_per_conversation": 25.0,
    }
    ad.update(overrides)
    return ad


def report(ad):
    return {
        "ads": [ad],
        "total_spend": ad.get("spend", 0.0),
        "total_conversations": ad.get("conversations", 0),
        "blended_cost_per_conversation": ad.get("cost_per_conversation", 0.0),
    }


def plan(ad, elapsed_hours):
    return build_change_plan(
        report(ad),
        tenant_id="flexi",
        campaign_id="cmp_1",
        campaign_slug="campaña",
        campaign_name="Flexi",
        elapsed_hours=elapsed_hours,
        checkpoint=f"E{int(elapsed_hours)}",
    )


def test_e48_con_cpa_malo_genera_watch_no_pausa():
    result = plan(bad_ad(), 48)

    assert result["actions"][0]["action"] == "watch"
    assert result["execution_allowed"] is False
    assert result["writes_to_meta"] is False
    assert result["mode"] == "recommendation_only"


def test_e72_con_cpa_malo_propone_pausar_solo_el_anuncio():
    result = plan(bad_ad(), 72)

    action = result["actions"][0]
    assert action["action"] == "pause_ad"
    assert action["target_type"] == "ad"
    assert action["target_id"] == "ad_1"
    assert action["writes_to_meta"] is False
    assert result["execution_allowed"] is False


def test_captura_tardia_no_adelanta_una_pausa():
    result = build_change_plan(
        report(bad_ad()),
        tenant_id="flexi",
        campaign_id="cmp_1",
        campaign_slug="campaña",
        campaign_name="Flexi",
        elapsed_hours=48,
        capture_elapsed_hours=50,
        checkpoint="E48",
    )

    assert result["actions"][0]["action"] == "watch"
    assert result["capture_elapsed_hours"] == 50
    assert any("Captura tardía" in warning for warning in result["warnings"])


def test_pocas_conversaciones_generan_watch_no_pausa():
    result = plan(
        bad_ad(conversations=2, cost_per_conversation=50.0, spend=100.0),
        96,
    )

    assert result["actions"][0]["action"] == "watch"
    assert result["execution_allowed"] is False


def test_markdown_deja_claro_que_no_hay_ejecucion():
    text = render_plan_markdown(plan(bad_ad(), 72))

    assert "no envía cambios a Meta" in text
    assert "Toda acción requiere aprobación humana" in text
    assert "No se pausa la campaña completa" in text


def test_metadata_inconsistente_bloquea_ejecucion_pero_no_medicion():
    result = build_change_plan(
        report(bad_ad()),
        tenant_id="flexi",
        campaign_id="cmp_1",
        campaign_slug="campaña",
        campaign_name="Flexi",
        elapsed_hours=72,
        checkpoint="E72",
        metadata_reconciliation={
            "status": "blocked",
            "execution_blocked": True,
            "execution_blockers": ["IDs inconsistentes"],
        },
    )

    assert result["actions"][0]["action"] == "pause_ad"
    assert result["execution_allowed"] is False
    assert result["execution_blocked"] is True
    assert result["execution_blockers"] == ["IDs inconsistentes"]
    assert result["approval"]["status"] == "blocked"
    assert any("Ejecución bloqueada" in warning for warning in result["warnings"])
    assert "## Bloqueos de ejecución" in render_plan_markdown(result)
