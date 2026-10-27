import json
import subprocess
import sys
from pathlib import Path

from growth import sync
from modules.social import meta_graph


def test_redact_sensitive_data_removes_keys_and_url_parameters():
    source = {
        "access_token": "secret-value",
        "next": "https://graph.example/media?limit=25&access_token=secret-value",
        "authorization": "Bearer secret-value",
        "safe": {"id": "123"},
    }

    result = sync.redact_sensitive_data(source)

    assert result["access_token"] == sync.REDACTED_VALUE
    assert "secret-value" not in json.dumps(result)
    assert "access_token=[REDACTED]" in result["next"]
    assert result["safe"] == {"id": "123"}
    assert source["access_token"] == "secret-value"


def test_write_snapshot_redacts_before_persisting(tmp_path):
    snapshot = {
        "generated_at": "2026-10-27T00:00:00+00:00",
        "tenant_id": "flexi",
        "mode": "local_evidence",
        "summary": {"success": 1},
        "sources": {
            "meta": {
                "paging": {
                    "next": "https://graph.example/media?access_token=secret-value"
                }
            }
        },
    }

    paths = sync.write_snapshot(snapshot, tmp_path)

    saved = paths["latest"].read_text(encoding="utf-8")
    assert "secret-value" not in saved
    assert "access_token=[REDACTED]" in saved


def test_sanitize_saved_snapshots_redacts_existing_files(tmp_path):
    sync_dir = tmp_path / "data" / "sync"
    sync_dir.mkdir(parents=True)
    snapshot_path = sync_dir / "latest.json"
    snapshot_path.write_text(
        json.dumps({"next": "https://graph.example/?access_token=old-secret"}),
        encoding="utf-8",
    )

    assert sync.sanitize_saved_snapshots(tmp_path) == 1
    assert "old-secret" not in snapshot_path.read_text(encoding="utf-8")


def test_capture_organic_requests_supported_facebook_fields(monkeypatch):
    calls = []

    class Response:
        status_code = 200
        content = b"{}"

        def __init__(self, body):
            self.body = body

        def json(self):
            return self.body

    def fake_get(url, params, timeout):
        calls.append((url, params, timeout))
        if url.endswith("/media"):
            return Response({"data": []})
        return Response({"id": "page-1", "name": "Flexi"})

    monkeypatch.setattr(meta_graph, "_load_user_token", lambda: "test-token")
    monkeypatch.setattr(meta_graph.requests, "get", fake_get)

    result = meta_graph.capture_organic({"meta": {"page_id": "page-1", "ig_user_id": "ig-1"}})

    assert result["status"] == "success"
    assert result["Facebook_Page"] == {"id": "page-1", "name": "Flexi"}
    page_request = next(params for url, params, _ in calls if url.endswith("/page-1"))
    assert page_request["fields"] == "id,name,followers_count,website"
    assert "remembered_email_access_token" not in page_request["fields"]


def test_sync_all_cli_executes_main_entrypoint():
    project_root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "scripts/sync_all.py", "--list"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert completed.returncode == 0
    assert "TENANT" in completed.stdout
    assert "flexi" in completed.stdout
