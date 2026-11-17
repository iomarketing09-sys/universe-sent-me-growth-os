from modules.communications.comments.sticker_library import list_stickers, suggest_sticker


def test_inventory_lists_images_without_modifying_originals(tmp_path):
    (tmp_path / "toma este corazon.jpeg").write_bytes(b"image")
    (tmp_path / "unknown.jpg").write_bytes(b"image")
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    items = list_stickers(tmp_path)
    assert len(items) == 2
    assert next(item for item in items if item["filename"] == "unknown.jpg")["classified"] is False
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before


def test_suggests_matching_sticker_but_never_authorizes_publication(tmp_path):
    (tmp_path / "no hay meme, solo te amo.jpeg").write_bytes(b"image")
    suggestion = suggest_sticker("Te amo", library_dir=tmp_path)
    assert suggestion["filename"] == "no hay meme, solo te amo.jpeg"
    assert suggestion["requires_human_approval"] is True
    assert suggestion["publication_authorized"] is False


def test_ambiguous_or_unavailable_sticker_is_not_suggested(tmp_path):
    (tmp_path / "no hay meme, solo te amo.jpeg").write_bytes(b"image")
    (tmp_path / "toma este corazon.jpeg").write_bytes(b"image")
    assert suggest_sticker("amor y corazón", library_dir=tmp_path) is None


def test_sensitive_stickers_are_not_selected_automatically(tmp_path):
    (tmp_path / "Pastillas para esquizofrenia.jpeg").write_bytes(b"image")
    assert suggest_sticker("pastillas para esquizofrenia", library_dir=tmp_path) is None


def test_universe_responder_attaches_sticker_suggestion_for_human_review(tmp_path, monkeypatch):
    from modules.communications.comments import sticker_library
    from modules.communications.comments.responder import UniverseResponder

    (tmp_path / "no hay meme, solo te amo.jpeg").write_bytes(b"image")
    monkeypatch.setattr(sticker_library, "DEFAULT_LIBRARY_DIR", tmp_path)
    responder = UniverseResponder(tenant_id="universe")
    monkeypatch.setattr(responder, "_generate_omniroute_response", lambda *args, **kwargs: "El universo tomó nota.")

    result = responder.respond(
        {"meme_text": "Te amo", "character": "Universe"},
        "Te amo",
    )

    assert result["decision"] in {"respond", "review"}
    assert result["sticker_suggestion"]["filename"] == "no hay meme, solo te amo.jpeg"
    assert result["sticker_suggestion"]["publication_authorized"] is False


def test_non_universe_tenant_does_not_receive_universe_sticker_suggestions(tmp_path, monkeypatch):
    from modules.communications.comments.responder import UniverseResponder

    (tmp_path / "no hay meme, solo te amo.jpeg").write_bytes(b"image")
    responder = UniverseResponder(tenant_id="firma-bordados")
    monkeypatch.setattr(responder, "_generate_omniroute_response", lambda *args, **kwargs: "El universo tomó nota.")

    result = responder.respond(
        {"meme_text": "Te amo", "character": "Universe"},
        "Te amo",
    )

    assert result["sticker_suggestion"] is None


def test_all_twelve_classified_rules_have_specific_trigger_and_metadata(tmp_path):
    from modules.communications.comments.sticker_library import STICKER_RULES

    for filename in STICKER_RULES:
        (tmp_path / filename).write_bytes(b"image")

    inventory = {item["filename"]: item for item in list_stickers(tmp_path)}
    assert len(STICKER_RULES) == 12
    for filename, rule in STICKER_RULES.items():
        assert inventory[filename]["classified"] is True
        assert inventory[filename]["label"] == rule["label"]
        assert inventory[filename]["category"] == rule["category"]
        assert inventory[filename]["triggers"] == list(rule["triggers"])
        suggestion = suggest_sticker(rule["triggers"][0], library_dir=tmp_path)
        assert suggestion is not None, filename
        assert suggestion["filename"] == filename
        assert suggestion["requires_human_approval"] is True
        assert suggestion["publication_authorized"] is False

def test_revised_rules_require_contextual_phrases_not_broad_keywords(tmp_path):
    from modules.communications.comments.sticker_library import STICKER_RULES

    for filename in STICKER_RULES:
        (tmp_path / filename).write_bytes(b"image")

    # La imagen de dormir no debe responder a cansancio o sueño literal.
    assert suggest_sticker("Estoy cansado y tengo sueño", library_dir=tmp_path) is None
    assert suggest_sticker("Si no tienes nada que poner, no pongas nada", library_dir=tmp_path)["filename"] == "Duermete otro rato.jpeg"

    # La imagen del payaso se reserva para autoironía o situaciones ridículas,
    # no para etiquetar directamente a una persona.
    assert suggest_sticker("Ese usuario es un payaso", library_dir=tmp_path) is None
    assert suggest_sticker("Hice el ridículo", library_dir=tmp_path)["filename"] == "payaso.jpeg"

    # La imagen de dinero no debe activarse por cualquier referencia genérica.
    assert suggest_sticker("Hoy fue un día complicado", library_dir=tmp_path) is None
    assert suggest_sticker("Cuánto me vas a pagar", library_dir=tmp_path)["filename"] == "money.jpeg"

    # La imagen de estado interior requiere una expresión explícita de contraste.
    assert suggest_sticker("Soy yo, me representa", library_dir=tmp_path) is None
    assert suggest_sticker("Así estoy por dentro", library_dir=tmp_path)["filename"] == "Yo por dentro.jpeg"


def test_revised_rules_expose_intent_tone_and_context_guards(tmp_path):
    from modules.communications.comments.sticker_library import STICKER_RULES

    for filename in STICKER_RULES:
        (tmp_path / filename).write_bytes(b"image")

    inventory = {item["filename"]: item for item in list_stickers(tmp_path)}
    for filename in STICKER_RULES:
        item = inventory[filename]
        assert item["intent"]
        assert item["tone"]
        assert item["compatible_context"]
        assert item["avoid_context"]
