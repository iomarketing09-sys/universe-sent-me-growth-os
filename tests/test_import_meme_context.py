"""Pruebas del backfill de contexto para comentarios sin meme_text."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.communications.comments.log import write_comment_log
from scripts import import_meme_context


POSTS = [
    {
        "id": "1036844829507460_122179805529072582",
        "copy": "para todos todo!",
        "character": "Wilfred",
        "meme": "que las cagadas sean el abono que fertilice tu exito.",
        "asset": "",
        "published_at": "2026-11-02T15:51:07+00:00",
    },
    {
        "id": "1036844829507460_122180166741072582",
        "copy": "Se cancela mi velorio",
        "character": "Silvio",
        "meme": "Se cancela mi velorio las pastillas que me tome eran vitaminas y estoy mas fuerte que nunca",
        "asset": "",
        "published_at": "2026-11-05T01:02:35+00:00",
    },
    {
        "id": "1036844829507460_122180220495072582",
        "copy": "Wilfred acaba de darse cuenta de algo",
        "character": "Wilfred",
        "meme": "No vivas del que diran",
        "asset": "2608001 - Wilfred - No vivas del que diran.jpeg",
        "published_at": "2026-11-05T16:00:00+00:00",
    },
    {
        "id": "1036844829507460_122180220543072582",
        "copy": "Maeve viendo slashers para procesar que existe.",
        "character": "Maeve",
        "meme": "El cine de terror como soporte emocional (maeve abrazando a un muñeco de peluche con la figura de Wilfred)",
        "asset": "2611003 - Maeve - El cine de terror como soporte emocional (maeve abrazando a un muñeco de peluche con la figura de Wilfred).jpg",
        "published_at": "2026-11-05T17:00:00+00:00",
    },
    {
        "id": "1036844829507460_122180220621072582",
        "copy": "El cardio que el universo quería que hicieras",
        "character": "Wilfred",
        "meme": "mi condición física está más preparada para culiar por 3 horas que para correr 30 minutos",
        "asset": "2611005 - Wilfred - mi condición física está más preparada para culiar por 3 horas que para correr 30 minutos.jpg",
        "published_at": "2026-11-05T19:30:02+00:00",
    },
    {
        "id": "1036844829507460_122180220693072582",
        "copy": "Evan defendiendo sus gustos culposos sin pedir permiso",
        "character": "Evan+Elara",
        "meme": "Te dije que era mi pelicula favorita no que fuera buena",
        "asset": "2611015 - Evan+Elara - Te dije que era mi pelicula favorita no que fuera buena.jpg",
        "published_at": "2026-11-05T22:00:07+00:00",
    },
    {
        "id": "1036844829507460_122180220771072582",
        "copy": "Obvio que sí, pero nadie preguntó por qué",
        "character": "Universe",
        "meme": "Andan detonando a las preguntonas",
        "asset": "2611009 - Universe - Andan detonando a las preguntonas.jpg",
        "published_at": "2026-11-05T23:00:03+00:00",
    },
    {
        "id": "1036844829507460_122180220843072582",
        "copy": "Evan convencido de que su energía lo protege del tráfico",
        "character": "Evan",
        "meme": "Yo aura fuerte",
        "asset": "260733 - Evan - Yo aura fuerte (10-jun-26).png",
        "published_at": "2026-11-06T01:00:01+00:00",
    },
]


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _setup_tenant(tmp_path: Path) -> Path:
    tenant = tmp_path / "tenants" / "universe"
    _write_csv(
        tenant / "metrics" / "publication_contexts_review.csv",
        ["id", "copy", "personaje", "meme_text", "asset_ref", "status"],
        [
            {
                "id": post["id"],
                "copy": post["copy"],
                "personaje": post["character"],
                "meme_text": post["meme"] if not post["asset"] else "",
                "asset_ref": "",
                "status": "",
            }
            for post in POSTS
        ],
    )
    ledger_fields = [
        "date",
        "time",
        "platform",
        "piece",
        "asset_filename",
        "status",
        "publication_id",
        "published_at",
        "reach",
        "interactions",
        "DMs",
        "leads",
    ]
    ledger_rows: list[dict[str, str]] = []
    for post in POSTS:
        short_id = post["id"].split("_")[-1]
        if post["asset"]:
            ledger_rows.append(
                {
                    "date": "2026-11-05",
                    "time": "10:00",
                    "platform": "Facebook",
                    "piece": post["copy"],
                    "asset_filename": post["asset"],
                    "status": "scheduled",
                    "publication_id": short_id,
                    "published_at": "",
                    "reach": "",
                    "interactions": "",
                    "DMs": "",
                    "leads": "",
                }
            )
        ledger_rows.append(
            {
                "date": "2026-11-05",
                "time": "10:00",
                "platform": "Facebook",
                "piece": post["copy"],
                "asset_filename": "",
                "status": "published",
                "publication_id": post["id"],
                "published_at": post["published_at"],
                "reach": "",
                "interactions": "",
                "DMs": "",
                "leads": "",
            }
        )
    _write_csv(
        tenant / "publication_log_week2.csv",
        ledger_fields,
        ledger_rows,
    )
    write_comment_log(
        tenant
        / "comment_responses"
        / "facebook_comments"
        / "data"
        / "comments_log.csv",
        [
            {
                "comment_id": f"{post['id'].split('_')[-1]}_comment-{index}",
                "comment_text": "Comentario pendiente",
                "decision": "sin_contexto",
                "publish_status": "sin_contexto",
            }
            for index, post in enumerate(POSTS)
        ],
    )
    return tenant


def _contexts(tenant: Path) -> dict:
    path = tenant / "publication_contexts.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def test_backfill_reconstruye_dictados_y_assets(tmp_path, capsys):
    tenant = _setup_tenant(tmp_path)

    code = import_meme_context.main(
        [
            "--tenant",
            "universe",
            "--base-path",
            str(tmp_path),
            "--backfill-missing",
            "--dry-run",
        ]
    )

    output = capsys.readouterr().out
    assert code == 0
    assert "Reconstruibles: 8" in output
    assert not (tenant / "publication_contexts.json").exists()

    rows = import_meme_context.backfill_rows("universe", tmp_path)
    assert len(rows) == 8
    by_short = {row["id"].split("_")[-1]: row for row in rows}
    for post in POSTS:
        row = by_short[post["id"].split("_")[-1]]
        assert row["meme_text"] == post["meme"]
        assert row["character"] == post["character"]
        assert row["published_at"] == post["published_at"]


def test_backfill_es_idempotente(tmp_path):
    tenant = _setup_tenant(tmp_path)

    assert import_meme_context.import_backfill("universe", tmp_path) == 8
    first = (tenant / "publication_contexts.json").read_text(encoding="utf-8")
    contexts = _contexts(tenant)
    assert all(contexts[post["id"]]["meme_text"] for post in POSTS)

    assert import_meme_context.import_backfill("universe", tmp_path) == 0
    assert (tenant / "publication_contexts.json").read_text(encoding="utf-8") == first


def test_backfill_no_inventa_meme_sin_fuente(tmp_path):
    tenant = tmp_path / "tenants" / "universe"
    write_comment_log(
        tenant
        / "comment_responses"
        / "facebook_comments"
        / "data"
        / "comments_log.csv",
        [
            {
                "comment_id": "122180408325072582_1",
                "decision": "sin_contexto",
                "publish_status": "sin_contexto",
            }
        ],
    )

    assert import_meme_context.backfill_rows("universe", tmp_path)[0]["meme_text"] == ""
    assert import_meme_context.import_backfill("universe", tmp_path) == 0
    assert not (tenant / "publication_contexts.json").exists()
