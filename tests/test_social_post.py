"""Tests del caption orgánico: no repite el chiste y respeta la voz."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.creative.agents.copywriter_agent.social_post import (
    CaptionError,
    build_social_messages,
    generate_caption,
    is_duplicate,
)
from modules.creative.agents.copywriter_agent.skills.omni_client import ChatResult
from modules.creative.agents.copywriter_agent.skills.voice_loader import load_voice_profile


ROOT = Path(__file__).resolve().parents[1]
MEME = "El cine de terror como soporte emocional"


class _FakeClient:
    def __init__(self, captions):
        self._captions = list(captions)
        self.calls = 0

    def chat_with_fallback(self, messages, models, max_tokens=300, temperature=0.8):
        self.calls += 1
        caption = self._captions.pop(0)
        return ChatResult(content=json.dumps({"caption": caption}), model="fake", usage={})


def test_is_duplicate_detects_verbatim_and_near_verbatim():
    assert is_duplicate("El cine de terror como soporte emocional", MEME)
    assert is_duplicate("el cine de terror como soporte emocional!!", MEME)
    assert not is_duplicate("Nadie sale ileso de una maratón de terror.", MEME)


def test_prompt_includes_voice_and_anti_tono():
    voice = load_voice_profile(ROOT / "tenants" / "universe")
    messages = build_social_messages(
        voice, meme_text=MEME, characters=["Maeve"], pillar="Humor Existencial"
    )
    system = messages[0]["content"]
    assert "no repite" in system.lower()
    assert "se ríe con" in system.lower()
    user = messages[1]["content"]
    assert "Maeve" in user
    assert "Humor Existencial" in user


def test_generate_caption_retries_when_model_repeats_the_meme():
    client = _FakeClient([MEME, "Y aun así lo volvería a ver."])
    result = generate_caption(
        "universe",
        meme_text=MEME,
        characters=["Maeve"],
        pillar="Humor Existencial",
        base_path=ROOT,
        client=client,
    )
    assert result["caption"] == "Y aun así lo volvería a ver."
    assert client.calls == 2


def test_generate_caption_fails_instead_of_publishing_a_flat_copy():
    client = _FakeClient([MEME, MEME, MEME])
    with pytest.raises(CaptionError):
        generate_caption(
            "universe",
            meme_text=MEME,
            characters=["Maeve"],
            pillar="Humor Existencial",
            base_path=ROOT,
            client=client,
        )


def test_parse_response_survives_truncated_json():
    from modules.creative.agents.copywriter_agent.social_post import _parse_response

    caption, pillar, parsed = _parse_response(
        '{"caption":"El cardio es un concepto.", "pillar":"Humor Existencial'
    )
    assert caption == "El cardio es un concepto."
    assert pillar == "Humor Existencial"
    assert parsed is False


def test_is_usable_rejects_truncated_captions():
    from modules.creative.agents.copywriter_agent.social_post import is_usable

    assert not is_usable("Yo también pref")
    assert not is_usable("")
    assert is_usable("Mi cardio es un mito.")
    assert is_usable("La cordura se fue de vacaciones")


def test_trim_caption_drops_the_remate():
    from modules.creative.agents.copywriter_agent.social_post import trim_caption

    long_copy = (
        "Obvio que mi cuerpo está en modo maratón de placer. "
        "Pero la pista sigue siendo un misterio sin nombre."
    )
    assert trim_caption(long_copy) == "Obvio que mi cuerpo está en modo maratón de placer."


def test_trim_caption_caps_length():
    from modules.creative.agents.copywriter_agent.social_post import trim_caption

    caption = trim_caption("palabra " * 40)
    assert len(caption) <= 100
