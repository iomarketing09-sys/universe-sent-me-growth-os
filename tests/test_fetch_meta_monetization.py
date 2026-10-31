"""Tests del extractor legacy de señales de monetización."""

from __future__ import annotations

import csv
import importlib.util
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tenants" / "universe" / "metrics" / "fetch_meta_monetization.py"
SPEC = importlib.util.spec_from_file_location("fetch_meta_monetization", SCRIPT)
assert SPEC and SPEC.loader
fetch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fetch)


def test_load_env_merges_root_env_and_environment(tmp_path, monkeypatch):
    tenant_env = tmp_path / "tenant.env"
    root_env = tmp_path / ".env"
    tenant_env.write_text("PAGE_ACCESS_TOKEN=tenant\n", encoding="utf-8")
    root_env.write_text(
        "FB_PAGE_ID=page-from-file\nMETA_ACCESS_TOKEN=file-token\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(fetch, "ENV_PATH", tenant_env)
    monkeypatch.setattr(fetch, "REPO_ROOT", tmp_path)
    monkeypatch.setenv("META_ACCESS_TOKEN", "env-token")

    values = fetch.load_env()

    assert values["PAGE_ACCESS_TOKEN"] == "tenant"
    assert values["FB_PAGE_ID"] == "page-from-file"
    assert values["META_ACCESS_TOKEN"] == "env-token"


def test_main_returns_error_without_token(monkeypatch, capsys):
    monkeypatch.setattr(fetch, "load_env", lambda: {})

    assert fetch.main() == 1
    assert "META_ACCESS_TOKEN" in capsys.readouterr().out


def test_main_returns_error_when_meta_rejects_page(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        fetch,
        "load_env",
        lambda: {"PAGE_ACCESS_TOKEN": "token", "FB_PAGE_ID": "123"},
    )
    monkeypatch.setattr(fetch, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(fetch, "api_get", lambda *args, **kwargs: {"error": {"message": "denied"}})

    assert fetch.main() == 2
    assert "denied" in capsys.readouterr().out


def test_main_replaces_same_day_csv_row(monkeypatch, tmp_path):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    csv_log = tmp_path / "meta_monetization_log.csv"
    with csv_log.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Fecha", "Plataforma", "Business_ID", "Posts_Analizados"])
        writer.writerow([today, "Facebook Page", "1", 10])
        writer.writerow([today, "Facebook Page", "1", 20])
    monkeypatch.setattr(fetch, "load_env", lambda: {"PAGE_ACCESS_TOKEN": "token", "FB_PAGE_ID": "123"})
    monkeypatch.setattr(fetch, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(fetch, "CSV_LOG", csv_log)
    monkeypatch.setattr(fetch, "DRIVE_DIR", tmp_path / "missing-drive")

    def fake_api(endpoint, params):
        if endpoint.endswith("/published_posts"):
            return {"data": [{"id": "p1", "reactions": {"summary": {"total_count": 2}}}]}
        return {"business": {"name": "Business"}}

    monkeypatch.setattr(fetch, "api_get", fake_api)

    assert fetch.main() == 0
    with csv_log.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    assert [row[0] for row in rows[1:]] == [today]
    assert rows[1][3] == "1"
