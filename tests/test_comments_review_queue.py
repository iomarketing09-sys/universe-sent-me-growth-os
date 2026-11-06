"""Tests de la vista de propuestas nuevas para revisión humana."""

from __future__ import annotations

import json
from pathlib import Path

from modules.cgo import CgoOrchestrator
from modules.communications.comments import CommentPaths
from modules.communications.comments.facebook import CommentProcessor
from modules.communications.comments.review_queue import build_new_proposals_queue
from tests.tenant_factory import make_tenant


def _write_approvals(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "generated_at": "2026-10-31T00:00:00+00:00",
                "approvals": items,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_review_queue_incluye_solo_no_aprobadas_y_no_descartadas(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [
            {
                "comment_id": "approved",
                "comment_text": "Comentario aprobado invisible",
                "approved_response": "Ya aprobada.",
                "approved": True,
            },
            {
                "comment_id": "published",
                "comment_text": "Comentario publicado invisible",
                "approved_response": "Ya publicada.",
                "approved": True,
                "published": True,
            },
            {
                "comment_id": "discarded",
                "comment_text": "Comentario descartado invisible",
                "approved_response": "No va.",
                "approved": False,
                "discarded": True,
            },
            {
                "comment_id": "new",
                "comment_text": "Comentario nuevo visible",
                "approved_response": "Propuesta nueva.",
                "approved": False,
            },
            {
                "comment_id": "no-response",
                "comment_text": "Comentario sin propuesta visible",
                "approved_response": "",
                "approved": False,
            },
        ],
    )
    original = paths.approvals_file.read_text(encoding="utf-8")

    result = build_new_proposals_queue("digital", base_path=tmp_path)

    queue = json.loads(Path(result["queue_file"]).read_text(encoding="utf-8"))
    assert [item["comment_id"] for item in queue["approvals"]] == ["new", "no-response"]
    assert queue["source"] == str(paths.approvals_file)
    assert result["items"] == 2
    assert result["without_response"] == 1
    assert paths.approvals_file.read_text(encoding="utf-8") == original

    markdown = Path(result["markdown"]).read_text(encoding="utf-8")
    assert "Comentario nuevo visible" in markdown
    assert "Comentario aprobado invisible" not in markdown
    assert "Comentario descartado invisible" not in markdown
    assert Path(result["csv"]).is_file()


def test_review_queue_vacia_cuando_todo_esta_revisado(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [
            {
                "comment_id": "approved",
                "approved_response": "Lista.",
                "approved": True,
            }
        ],
    )

    result = build_new_proposals_queue("digital", base_path=tmp_path)

    queue = json.loads(Path(result["queue_file"]).read_text(encoding="utf-8"))
    assert result["items"] == 0
    assert queue["approvals"] == []


def test_run_comments_harvest_skip_harvest_solo_reconstruye_cola(tmp_path):
    from scripts.run_comments_harvest import main

    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [
            {
                "comment_id": "new",
                "comment_text": "Comentario pendiente",
                "approved_response": "Propuesta.",
                "approved": False,
            }
        ],
    )

    code = main(
        [
            "--tenant",
            "digital",
            "--skip-harvest",
            "--base-path",
            str(tmp_path),
        ]
    )

    assert code == 0
    queue_file = paths.storage_dir / "aprobaciones_nuevas.json"
    assert queue_file.is_file()
    queue = json.loads(queue_file.read_text(encoding="utf-8"))
    assert [item["comment_id"] for item in queue["approvals"]] == ["new"]


def test_processor_detecta_ids_delegados_y_evita_duplicarlos(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.storage_dir / "aprobaciones_nuevas_8.json",
        [
            {
                "comment_id": "batch-approved",
                "approved_response": "Va en lote.",
                "approved": True,
            }
        ],
    )
    _write_approvals(
        paths.approvals_file,
        [
            {
                "comment_id": "tombstone",
                "approved_response": "Delegada.",
                "approved": False,
                "discarded": True,
                "delegated_to": "aprobaciones_nuevas_8.json",
            }
        ],
    )

    processor = CommentProcessor(tenant_id="digital", base_path=tmp_path)

    assert processor._load_delegated_comment_ids() == {
        "batch-approved",
        "tombstone",
    }


def test_processor_respeta_decisiones_previas(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [
            {"comment_id": "descartado", "discarded": True},
            {"comment_id": "aprobado", "approved": True, "approved_response": "Va."},
            {"comment_id": "publicado", "published": True, "reply_id": "r1"},
            {"comment_id": "pendiente", "approved": False},
        ],
    )

    processor = CommentProcessor(tenant_id="digital", base_path=tmp_path)

    assert processor._load_decided_comment_ids() == {
        "descartado": "discarded",
        "aprobado": "approved",
        "publicado": "published",
    }


def test_cgo_no_publica_la_vista_de_revision(tmp_path, monkeypatch):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [
            {
                "comment_id": "new",
                "comment_text": "Pendiente",
                "approved_response": "Propuesta.",
                "approved": False,
            }
        ],
    )
    view = build_new_proposals_queue("digital", base_path=tmp_path)
    view_path = Path(view["queue_file"])

    dry = CgoOrchestrator(
        base_path=str(tmp_path),
        comments_approvals_file=view_path,
    ).run_one("comments_review", "digital")

    assert dry.status == "OK"
    assert dry.data["kind"] == "review_queue"
    assert any(str(paths.approvals_file) in item for item in dry.next_actions)

    import modules.communications.comments as comments

    monkeypatch.setattr(
        comments,
        "publish_approved",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no publicar")),
    )
    blocked = CgoOrchestrator(
        base_path=str(tmp_path),
        dry_run=False,
        publish=True,
        comments_approvals_file=view_path,
    ).run_one("comments_review", "digital")

    assert blocked.status == "BLOCKED"
    assert "solo lectura" in blocked.reason
