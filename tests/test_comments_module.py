"""Tests del módulo canónico de comentarios y su capacidad CGO."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from modules.cgo import CgoOrchestrator
from modules.communications.comments import CommentPaths, inbox_snapshot
from modules.communications.comments.log import write_comment_log
from tests.tenant_factory import make_tenant


def _write_approvals(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "generated_at": "2026-10-31T00:00:00+00:00",
                "reviewed_at": "2026-10-31T01:00:00+00:00",
                "approvals": items,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_comment_paths_use_tenant_and_do_not_create_directories(tmp_path):
    paths = CommentPaths.for_tenant("digital", tmp_path)

    assert paths.storage_dir == tmp_path / "tenants" / "digital" / "comment_responses" / "facebook_comments"
    assert paths.approvals_file == paths.storage_dir / "aprobaciones.json"
    assert paths.comments_log_file == paths.storage_dir / "data" / "comments_log.csv"
    assert not paths.storage_dir.exists()


def test_inbox_snapshot_classifies_without_writing(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [
            {"comment_id": "pending", "approved": True, "approved_response": "Lista"},
            {"comment_id": "done", "approved": True, "approved_response": "Hecha", "reply_id": "r1"},
            {"comment_id": "skipped", "approved": False, "approved_response": "No va"},
            {"comment_id": "invalid", "approved": True, "approved_response": ""},
        ],
    )
    write_comment_log(
        paths.comments_log_file,
        [
            {"comment_id": "pending", "publish_status": "pending_approval"},
            {"comment_id": "done", "publish_status": "published"},
        ],
    )
    before = paths.storage_dir.stat().st_mtime_ns

    snapshot = inbox_snapshot("digital", base_path=tmp_path)

    assert snapshot["configured"] is True
    assert snapshot["approvals"] == {
        "total": 4,
        "approved": 3,
        "approved_pending": 1,
        "approved_without_response": 1,
        "not_approved": 1,
        "published": 1,
        "errors": 0,
        "pending_comment_ids": ["pending"],
    }
    assert snapshot["comments_log"]["rows"] == 2
    assert snapshot["comments_log"]["published"] == 1
    assert paths.storage_dir.stat().st_mtime_ns == before


def test_comments_review_dry_run_is_local_and_does_not_publish(tmp_path, monkeypatch):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [{"comment_id": "pending", "approved": True, "approved_response": "Lista"}],
    )

    import modules.communications.comments as comments

    def explotar(*args, **kwargs):
        raise AssertionError("no debe publicar")

    monkeypatch.setattr(comments, "publish_approved", explotar)

    result = CgoOrchestrator(base_path=str(tmp_path)).run_one("comments_review", "digital")

    assert result.status == "OK", result.to_dict()
    assert result.dry_run is True
    assert result.data["approvals"]["approved_pending"] == 1
    assert all(gate.name != "token" for gate in result.gates)


def test_comments_review_publish_requires_token(tmp_path, monkeypatch):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [{"comment_id": "pending", "approved": True, "approved_response": "Lista"}],
    )

    import modules.cgo.gates as gates

    monkeypatch.setattr(gates, "has_token", lambda ctx, tenant_id: False)

    result = CgoOrchestrator(base_path=str(tmp_path), dry_run=False, publish=True).run_one(
        "comments_review", "digital"
    )

    assert result.status == "BLOCKED"
    assert any(gate.name == "token" and gate.state == "FAIL" for gate in result.gates)


def test_comments_review_publish_calls_module_with_tenant_paths(tmp_path, monkeypatch):
    make_tenant(tmp_path, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", tmp_path)
    _write_approvals(
        paths.approvals_file,
        [{"comment_id": "pending", "approved": True, "approved_response": "Lista"}],
    )

    import modules.cgo.gates as gates
    import modules.communications.comments as comments

    monkeypatch.setattr(gates, "has_token", lambda ctx, tenant_id: True)
    calls = []

    def fake_publish(approval_file, comments_log_path=None, **kwargs):
        calls.append((approval_file, comments_log_path, kwargs))
        return 0

    monkeypatch.setattr(comments, "publish_approved", fake_publish)

    result = CgoOrchestrator(base_path=str(tmp_path), dry_run=False, publish=True).run_one(
        "comments_review", "digital"
    )

    assert result.status == "OK", result.to_dict()
    assert calls == [
        (
            str(paths.approvals_file),
            str(paths.comments_log_file),
            {"tenant_id": "digital", "base_path": tmp_path},
        )
    ]


def test_comments_review_is_native_only(tmp_path):
    make_tenant(tmp_path, "tienda", track="physical_cro")

    result = CgoOrchestrator(base_path=str(tmp_path)).run_one("comments_review", "tienda")

    assert result.status == "BLOCKED"
    assert any(gate.name == "track" and gate.state == "FAIL" for gate in result.gates)


def test_comments_review_without_approvals_is_not_configured(tmp_path):
    make_tenant(tmp_path, "digital", track="native_digital")

    result = CgoOrchestrator(base_path=str(tmp_path)).run_one("comments_review", "digital")

    assert result.status == "NOT_CONFIGURED"


def test_legacy_tenant_entrypoints_reexport_canonical_module():
    root = Path(__file__).resolve().parents[1]
    entrypoints = [
        root / "tenants/universe/comment_responses/facebook_comments/main.py",
        root / "tenants/universe/comment_responses/facebook_comments/comment_log.py",
        root / "tenants/universe/comment_responses/facebook_comments/responders/universe_responder.py",
    ]

    for index, path in enumerate(entrypoints):
        spec = importlib.util.spec_from_file_location(f"legacy_comments_{index}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    assert entrypoints[0].read_text(encoding="utf-8").count("def main(") == 0
    assert entrypoints[2].read_text(encoding="utf-8").count("class UniverseResponder") == 0
