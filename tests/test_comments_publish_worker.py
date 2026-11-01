"""Tests del worker de publicación de comentarios aprobados."""

from __future__ import annotations

import json
from pathlib import Path

from modules.communications.comments import CommentPaths
from scripts import run_comments_publish as worker
from tests.tenant_factory import make_tenant


def _write_queue(path: Path, items: list[dict], *, kind: str | None = None) -> None:
    payload = {"approvals": items}
    if kind:
        payload["kind"] = kind
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_queue_candidates_incluye_principal_y_lotes_pero_no_vista_revision(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_queue(paths.approvals_file, [])
    _write_queue(paths.storage_dir / "aprobaciones_lote.json", [])
    _write_queue(
        paths.storage_dir / "aprobaciones_nuevas.json",
        [],
        kind="review_queue",
    )

    names = [path.name for path in worker.queue_candidates(paths)]

    assert names == ["aprobaciones.json", "aprobaciones_lote.json"]


def test_pending_approvals_exige_aprobacion_texto_y_no_publicado():
    payload = {
        "approvals": [
            {"comment_id": "ok", "approved": True, "approved_response": "Hola"},
            {"comment_id": "sin-texto", "approved": True, "approved_response": " "},
            {"comment_id": "no-aprobado", "approved": False, "approved_response": "Hola"},
            {
                "comment_id": "publicado",
                "approved": True,
                "approved_response": "Hola",
                "published": True,
            },
        ]
    }

    assert [item["comment_id"] for item in worker.pending_approvals(payload)] == ["ok"]


def test_vista_revision_nunca_se_publica():
    payload = {
        "kind": "review_queue",
        "approvals": [{"comment_id": "ok", "approved": True, "approved_response": "Hola"}],
    }

    assert worker.pending_approvals(payload) == []


def test_worker_publica_solo_colas_con_pendientes(tmp_path, monkeypatch):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_queue(
        paths.approvals_file,
        [{"comment_id": "ok", "approved": True, "approved_response": "Hola"}],
    )
    _write_queue(
        paths.storage_dir / "aprobaciones_nuevas_8.json",
        [{"comment_id": "batch", "approved": True, "approved_response": "Lote"}],
        kind="batch",
    )
    _write_queue(
        paths.storage_dir / "aprobaciones_nuevas.json",
        [{"comment_id": "view", "approved": True, "approved_response": "Vista"}],
        kind="review_queue",
    )
    calls = []

    def fake_publish_queue(**kwargs):
        calls.append(Path(kwargs["queue_path"]).name)
        return 0

    monkeypatch.setattr(worker, "publish_queue", fake_publish_queue)

    code = worker.main(
        [
            "--tenant",
            "digital",
            "--base-path",
            str(tmp_path),
            "--no-drive-sync",
        ]
    )

    assert code == 0
    assert calls == ["aprobaciones.json", "aprobaciones_nuevas_8.json"]


def test_candado_impide_dos_publicadores(tmp_path):
    lock_path = tmp_path / ".publish.lock"
    first = worker.acquire_lock(lock_path)
    assert first is not None
    try:
        assert worker.acquire_lock(lock_path) is None
    finally:
        first.close()
