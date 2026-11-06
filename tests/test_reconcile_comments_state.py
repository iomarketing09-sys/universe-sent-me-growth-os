"""Pruebas de la reconciliación de la cola maestra de comentarios."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from modules.communications.comments.log import write_comment_log
from modules.communications.comments.paths import CommentPaths
from scripts import reconcile_comments_state as reconcile
from tests.tenant_factory import make_tenant


def _write_queue(path: Path, items: list[dict], *, kind: str | None = None) -> None:
    payload = {"approvals": items}
    if kind:
        payload["kind"] = kind
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _write_log(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_comment_log(path, rows)


def test_reconcilia_publicado_desde_lote_cerrado(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_queue(
        paths.approvals_file,
        [
            {
                "comment_id": "c1",
                "comment_text": "Hola",
                "approved": False,
                "discarded": True,
                "discard_reason": "duplicado",
            }
        ],
    )
    source = paths.storage_dir / "aprobaciones_nuevas_8.json"
    _write_queue(
        source,
        [
            {
                "comment_id": "c1",
                "approved": True,
                "published": True,
                "approved_response": "Texto del lote",
                "reply_id": "reply-1",
                "published_at": "2026-11-01T05:00:00+00:00",
            }
        ],
        kind="batch",
    )
    _write_log(
        paths.comments_log_file,
        [
            {
                "timestamp": "2026-11-01T04:00:00+00:00",
                "comment_id": "c1",
                "publish_status": "published",
                "published_at": "2026-11-01T05:00:00+00:00",
                "reply_id": "reply-1",
                "response_text": "Texto publicado en Meta",
            }
        ],
    )

    master = reconcile._load_queue(paths.approvals_file)
    published, _ = reconcile._log_indexes(paths.comments_log_file)
    changes, skipped = reconcile.reconcile_published(
        master, [source], published, now="2026-11-02T12:00:00+00:00"
    )

    item = master["approvals"][0]
    assert [change["comment_id"] for change in changes] == ["c1"]
    assert skipped == []
    assert item["approved"] is True
    assert item["published"] is True
    assert item["reply_id"] == "reply-1"
    assert item["approved_response"] == "Texto publicado en Meta"
    assert "discarded" not in item
    assert item["reconciled_from"] == source.name


def test_no_descarta_un_comentario_ya_publicado(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_queue(
        paths.approvals_file,
        [{"comment_id": "c1", "published": True, "reply_id": "reply-1"}],
    )
    master = reconcile._load_queue(paths.approvals_file)

    changes, errors = reconcile.apply_discards(
        master,
        [("c1", "motivo cualquiera")],
        now="2026-11-02T12:00:00+00:00",
    )

    assert changes == []
    assert errors[0]["reason"] == "ya está publicado"
    assert master["approvals"][0].get("discarded") is None


def test_main_solo_escribe_con_apply(tmp_path, capsys):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_queue(
        paths.approvals_file,
        [{"comment_id": "c1", "approved": False}],
    )
    source = paths.storage_dir / "aprobaciones_nuevas_8.json"
    _write_queue(
        source,
        [{"comment_id": "c1", "published": True, "reply_id": "reply-1"}],
        kind="batch",
    )
    _write_log(
        paths.comments_log_file,
        [{"timestamp": "2026-11-01T04:00:00+00:00", "comment_id": "c1"}],
    )
    before = paths.approvals_file.read_text(encoding="utf-8")

    code = reconcile.main(
        [
            "--tenant",
            "digital",
            "--base-path",
            str(tmp_path),
            "--source",
            str(source),
        ]
    )

    assert code == 0
    assert paths.approvals_file.read_text(encoding="utf-8") == before
    assert "Dry-run" in capsys.readouterr().out


def test_descarta_comentario_ausente_usando_el_log(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_queue(paths.approvals_file, [])
    _write_log(
        paths.comments_log_file,
        [
            {
                "timestamp": "2026-11-02T23:00:00+00:00",
                "comment_id": "c1",
                "comment_text": "Comentario viejo",
                "created_time": "2026-11-02T22:53:00+00:00",
                "publish_status": "pending_approval",
            }
        ],
    )
    master = reconcile._load_queue(paths.approvals_file)
    log_rows = reconcile._latest_log_rows(paths.comments_log_file)

    changes, errors = reconcile.apply_discards(
        master,
        [("c1", "contenido sexual")],
        now="2026-11-06T15:00:00+00:00",
        log_rows=log_rows,
    )

    assert errors == []
    assert [change["comment_id"] for change in changes] == ["c1"]
    item = master["approvals"][0]
    assert item["discarded"] is True
    assert item["discard_reason"] == "contenido sexual"
    assert item["tombstoned_from"] == "comments_log"
    assert item["comment_text"] == "Comentario viejo"


def test_main_permite_descartar_sin_lote_cerrado(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_queue(
        paths.approvals_file,
        [{"comment_id": "c1", "comment_text": "Comentario", "approved": False}],
    )
    _write_log(
        paths.comments_log_file,
        [{"timestamp": "2026-11-02T23:00:00+00:00", "comment_id": "c1"}],
    )

    code = reconcile.main(
        [
            "--tenant",
            "digital",
            "--base-path",
            str(tmp_path),
            "--discard",
            "c1",
            "contenido sexual",
            "--apply",
        ]
    )

    assert code == 0
    master = json.loads(paths.approvals_file.read_text(encoding="utf-8"))
    assert master["approvals"][0]["discarded"] is True
    assert master["total_pending"] == 0
    rows = list(csv.DictReader(paths.comments_log_file.open(encoding="utf-8-sig")))
    assert rows[-1]["publish_status"] == "discarded"
    assert rows[-1]["filter_reason"] == "contenido sexual"
