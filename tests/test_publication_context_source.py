import csv
from pathlib import Path

from modules.intelligence.publication_context_source import (
    context_matches,
    load_external_contexts,
    source_path,
)


def test_load_external_context_translates_editorial_fields(tmp_path: Path):
    source = tmp_path / "november.csv"
    fields = [
        "Fecha", "Hora", "Asset", "Personaje", "Caption publicado",
        "ID de FB", "Enlace", "Notas", "Contexto", "Texto de la imagen",
    ]
    with source.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "Fecha": "2026-11-01", "Hora": "09:35", "Asset": "260723",
            "Personaje": "Kiri", "Caption publicado": "Caption",
            "ID de FB": "pfbid02abc", "Enlace": "https://facebook.com/page/posts/pfbid02abc",
            "Notas": "nota", "Contexto": "Kiri en un taxi",
            "Texto de la imagen": "Texto del meme",
        })
        writer.writerow({"ID de FB": "por verificar", "Enlace": "por verificar"})
    contexts = load_external_contexts(source)
    assert len(contexts) == 1
    context = contexts[0]
    assert context["character"] == "Kiri"
    assert context["meme_text"] == "Texto del meme"
    assert context["visual_context"] == "Kiri en un taxi"
    assert context["caption"] == "Caption"
    assert context["source_notes"] == "nota"
    assert context_matches(context, "1036844829507460_pfbid02abc")
    assert context_matches(context, "1036844829507460_123", context["permalink_url"])
    assert not context_matches(context, "1036844829507460_456")


def test_source_path_can_be_overridden_by_environment(monkeypatch, tmp_path):
    configured = tmp_path / "editorial.csv"
    monkeypatch.setenv("UNIVERSE_PUBLICATION_CONTEXT_CSV", str(configured))
    assert source_path("universe") == configured
    assert source_path("other-tenant") is None
