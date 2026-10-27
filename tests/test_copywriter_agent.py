"""Tests del Copywriter Agent: voz, validación y escritura de propuesta."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from modules.creative.agents.copywriter_agent.agent import CopywriterAgent
from modules.creative.agents.copywriter_agent.skills.copy_validator import validate_variant
from modules.creative.agents.copywriter_agent.skills.prompt_builder import build_messages
from modules.creative.agents.copywriter_agent.skills.voice_loader import load_voice_profile


ROOT = Path(__file__).resolve().parents[1]
FLEXI = ROOT / "tenants" / "flexi"
CAMPAIGN = "2026-10_flexi_ads_500mxn"


def _variant(**overrides):
    variant = {
        "id": "v1",
        "angle": "beneficio_directo",
        "model_code": "142801",
        "headline": "Confort para tu día",
        "primary_text": "Conoce ISAURA y escríbenos para asesorarte.",
        "description": "Asesoría en tienda",
        "cta": "SEND_MESSAGE",
        "hypothesis": "El anuncio superará el CTR de control.",
    }
    variant.update(overrides)
    return variant


def test_voice_profile_loads_for_flexi():
    profile = load_voice_profile(FLEXI)
    assert profile["brand_identity"]["name"] == "Flexi"
    assert profile["_source_path"].endswith("brand_voice.json")


def test_voice_profiles_are_isolated_by_tenant():
    flexi = load_voice_profile(FLEXI)
    micas = load_voice_profile(ROOT / "tenants" / "micas-art-deco")
    assert flexi["brand_identity"]["name"] == "Flexi"
    assert micas["brand_identity"]["name"] == "Mica's Art & Deco"
    assert flexi["_source_path"] != micas["_source_path"]


def test_validator_blocks_forbidden_claim():
    result = validate_variant(
        _variant(primary_text="Compra hoy y escríbenos para asesorarte."),
        allowed_angles=["beneficio_directo", "prueba_social"],
        approved_model_codes=["142801"],
        forbidden_terms=["compra"],
    )
    assert result["passed"] is False
    assert any("compra" in error for error in result["errors"])


def test_validator_requires_whatsapp_invitation():
    result = validate_variant(
        _variant(primary_text="Conoce ISAURA y su confort diario."),
        allowed_angles=["beneficio_directo", "prueba_social"],
        approved_model_codes=["142801"],
    )
    assert result["passed"] is False
    assert any("conversación de WhatsApp" in error for error in result["errors"])


def test_offline_generation_returns_four_valid_variants():
    agent = CopywriterAgent("flexi", base_path=str(ROOT), offline=True)
    result = agent.generate(CAMPAIGN, write=False)

    assert result["passed"] is True
    assert len(result["variants"]) == 4
    assert {variant["cta"] for variant in result["variants"]} == {"SEND_MESSAGE"}
    assert {variant["model_code"] for variant in result["variants"]} == {
        "142801",
        "143201",
        "306703",
        "143001",
    }


def test_write_proposal_inside_campaign_copy_folder(tmp_path):
    tenant = tmp_path / "tenants" / "flexi"
    tenant.mkdir(parents=True)
    shutil.copy2(FLEXI / "brand_voice.json", tenant / "brand_voice.json")
    shutil.copy2(FLEXI / "config.json", tenant / "config.json")
    campaign_src = FLEXI / "ads" / "campanas" / CAMPAIGN
    campaign_dst = tenant / "ads" / "campanas" / CAMPAIGN
    shutil.copytree(campaign_src, campaign_dst)
    shutil.rmtree(campaign_dst / "piezas" / "copy", ignore_errors=True)

    agent = CopywriterAgent("flexi", base_path=str(tmp_path), offline=True)
    result = agent.generate(CAMPAIGN, write=True)

    markdown = Path(result["written"]["markdown"])
    payload = Path(result["written"]["json"])
    assert markdown.is_file()
    assert payload.is_file()
    assert markdown.parent == campaign_dst / "piezas" / "copy"
    proposal = markdown.read_text(encoding="utf-8")
    assert "pendiente de aprobación" in proposal
    assert "(G2)" in proposal

    state = (campaign_dst / "00_estado.md").read_text(encoding="utf-8")
    assert "propuesta v1 generada" in state
    assert "G2 pendiente" in state

    data = json.loads(payload.read_text(encoding="utf-8"))
    assert data["campaign_slug"] == CAMPAIGN
    assert len(data["variants"]) == 4


def test_vendor_skills_have_provenance_and_no_scripts():
    vendor = ROOT / "modules" / "creative" / "agents" / "copywriter_agent" / "skills" / "vendor"
    for name in ("marketingskills-copywriting", "marketingskills-ad-creative"):
        folder = vendor / name
        assert (folder / "SKILL.md").is_file()
        assert (folder / "PROVENANCE.md").is_file()
        assert (folder / "LICENSE").is_file()
        assert not list(folder.glob("*.py"))
        assert not list(folder.glob("*.sh"))


def test_prompt_includes_real_published_copy_evidence():
    profile = load_voice_profile(FLEXI)
    messages = build_messages(
        tenant_id="flexi",
        campaign_slug=CAMPAIGN,
        voice=profile,
        ads_config={},
        brief="Brief de prueba",
        audience="Mujeres de 28 a 55 años en Piedras Negras",
        assets_manifest="",
        assignments=[
            {
                "id": "v1",
                "angle": "beneficio_directo",
                "model_code": "142801",
                "model_name": "ISAURA",
            }
        ],
    )
    prompt = messages[1]["content"]

    assert "published_copy_evidence" in prompt
    assert "Tus pies" in prompt
    assert "posts_analyzed" in prompt
