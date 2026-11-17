from __future__ import annotations

from modules.communications.policy import comment_signal, is_low_signal
from modules.communications.comments.responder import UniverseResponder


def test_low_signal_only_discards_empty_emoji_and_laughter():
    for value in ("", "   ", "😂😂", "❤️", "jajaja", "JAJAJA 😂", "xdxd"):
        assert is_low_signal(value), value


def test_short_affirmations_are_not_discarded_as_low_signal():
    for value in ("Sí", "Si", "Cierto", "Exacto", "Así es", "Total", "x2"):
        assert not is_low_signal(value), value
        assert comment_signal(value) == ""


def test_tagged_mentions_and_brand_mentions_are_distinguished():
    assert comment_signal("@seguidores") == "tagged_mention"
    assert comment_signal("@amigo mira esto") == "tagged_mention"
    assert comment_signal("Universe Sent Me, qué buen meme") == "brand_mention"
    assert comment_signal("@seguidores Universe Sent Me") == "brand_mention"
    assert comment_signal("@amigo ¿qué opinas?") == "question"
    assert comment_signal("Qué significa esto") == "question"
    assert comment_signal("Que Diablos haha") == ""
    assert comment_signal("Universe Sent Me 🖤€r€S S€x¥  KA€£🖤~") == "risky_brand_mention"
    assert comment_signal("Universe Sent Me Así es Reciprocidad 🔮~") == "brand_mention"


def test_responder_routes_short_affirmations_to_contextual_review(monkeypatch):
    responder = UniverseResponder(tenant_id="universe")
    monkeypatch.setattr(responder, "_generate_omniroute_response", lambda *args, **kwargs: None)
    context = {"meme_text": "Cuando el universo responde", "caption": "Humor"}

    for value in ("Sí", "Cierto", "Exacto"):
        result = responder.respond(context, value)
        assert result["decision"] == "review", (value, result)
        assert result["comment_type"] != "baja_señal"


def test_responder_discards_only_empty_emoji_or_laughter():
    responder = UniverseResponder(tenant_id="universe")
    for value in ("😂😂", "jajaja", "❤️"):
        result = responder.respond({"meme_text": "Meme"}, value)
        assert result["decision"] == "no_response"
        assert result["comment_type"] == "baja_señal"


def test_responder_logs_brand_signal_and_ignores_user_tags():
    responder = UniverseResponder(tenant_id="universe")
    context = {"meme_text": "Meme"}

    brand = responder.respond(context, "Universe Sent Me, qué buen contenido")
    tagged = responder.respond(context, "@seguidores")

    assert brand["decision"] == "brand_signal"
    assert brand["comment_type"] == "brand_mention"
    assert tagged["decision"] == "ignore_mention"
    assert tagged["comment_type"] == "mention"


def test_risky_brand_mention_is_held_for_human_review_without_brand_signal():
    responder = UniverseResponder(tenant_id="universe")
    result = responder.respond(
        {"meme_text": "Meme"},
        "Universe Sent Me 🖤€r€S S€x¥  KA€£🖤~",
    )
    assert result["decision"] == "review"
    assert result["comment_type"] == "brand_mention_risky"
    assert result["response"] is None
