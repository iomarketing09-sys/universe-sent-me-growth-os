"""Tests de los reportes Markdown/CSV para revisión humana."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.communications.review_report import generate_review_files, load_review_items


def test_genera_markdown_y_csv_desde_aprobaciones(tmp_path):
    source = tmp_path / "aprobaciones.json"
    source.write_text(
        json.dumps(
            {
                "approvals": [
                    {
                        "comment_id": "c1",
                        "author": "Usuario",
                        "comment_text": "No lo creo jajaja",
                        "character": "Universe",
                        "approved_response": "No lo creas.",
                        "approved": False,
                        "agent": {
                            "model": "openai/gpt-4.1-mini",
                            "quality_ok": True,
                            "policy_flags": [],
                        },
                    },
                    {
                        "comment_id": "c2",
                        "author": "Usuario 2",
                        "comment_text": "¿Precio?",
                        "character": "Universe",
                        "approved_response": "El precio es $1,899.",
                        "approved": False,
                        "review_reason": "No puede afirmar precios.",
                        "agent": {
                            "model": "openai/gpt-4.1-mini",
                            "quality_ok": False,
                            "policy_flags": ["commercial_claim"],
                        },
                    },
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = generate_review_files(source)

    markdown_path = Path(result["markdown"])
    csv_path = Path(result["csv"])
    assert markdown_path.is_file()
    assert csv_path.is_file()
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "No lo creo jajaja" in markdown
    assert "No lo creas." in markdown
    assert "[ ] Aprobada para publicar" in markdown
    assert "commercial_claim" in markdown
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 2
    assert rows[0]["respuesta_propuesta"] == "No lo creas."
    assert rows[1]["calidad"] == "REVISAR"


def test_acepta_reporte_sombra_y_lo_convierte(tmp_path):
    source = tmp_path / "shadow.json"
    source.write_text(
        json.dumps(
            {
                "records": [
                    {
                        "comment_id": "c1",
                        "comment_text": "Comentario",
                        "reference": {"approved": True},
                        "agent": {
                            "character": "Universe",
                            "draft": "Respuesta propuesta.",
                            "response": "Respuesta propuesta.",
                            "decision": "suggest",
                            "quality_ok": True,
                            "policy_flags": [],
                            "model": "openai/gpt-4.1-mini",
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    items = load_review_items(source)

    assert items[0]["estado"] == "aprobada"
    assert items[0]["respuesta_propuesta"] == "Respuesta propuesta."
    assert items[0]["calidad"] == "OK"


def test_filtra_solo_propuestas_sugeridas(tmp_path):
    source = tmp_path / "shadow.json"
    source.write_text(
        json.dumps(
            {
                "records": [
                    {
                        "comment_id": "c1",
                        "comment_text": "Comentario uno",
                        "agent": {
                            "character": "Universe",
                            "draft": "Propuesta uno.",
                            "decision": "suggest",
                            "quality_ok": True,
                            "policy_flags": [],
                        },
                    },
                    {
                        "comment_id": "c2",
                        "comment_text": "Comentario dos",
                        "agent": {
                            "character": "Universe",
                            "draft": "Propuesta dos.",
                            "decision": "review",
                            "quality_ok": False,
                            "policy_flags": ["context_mismatch"],
                        },
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    items = load_review_items(source, only_decision="suggest")

    assert len(items) == 1
    assert items[0]["comment_id"] == "c1"
