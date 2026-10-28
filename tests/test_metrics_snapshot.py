"""Tests del ledger E0/E24/E72 sin llamadas reales a Meta."""

from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path

from modules.intelligence import metrics_snapshot as ms


PUBLISHED_AT = "2026-10-28T10:06:11"
PUBLISHED_UTC = datetime.fromisoformat("2026-10-28T15:06:11+00:00")


def _write_publication_log(root: Path, rows: list[dict[str, str]]) -> None:
    tenant = root / "tenants" / "flexi"
    tenant.mkdir(parents=True, exist_ok=True)
    fields = ["date", "time", "platform", "piece", "asset_filename", "status",
              "publication_id", "published_at", "reach", "interactions", "DMs", "leads"]
    with (tenant / "publication_log_week2.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _ig_row(**overrides: str) -> dict[str, str]:
    row = {
        "date": "2026-10-28",
        "time": "10:00",
        "platform": "Instagram",
        "piece": "ISAURA",
        "asset_filename": "ISAURA_142801_BEIGE_OI26_HERO.jpg",
        "status": "published",
        "publication_id": "18129355670309228",
        "published_at": PUBLISHED_AT,
    }
    row.update(overrides)
    return row


def test_ensure_snapshots_is_idempotent(tmp_path, monkeypatch):
    _write_publication_log(tmp_path, [_ig_row()])
    monkeypatch.chdir(tmp_path)

    created = ms.ensure_snapshots_for_publications("flexi", now=PUBLISHED_UTC)
    assert [snap.window for snap in created] == ["E0", "E24", "E72"]
    assert ms.ensure_snapshots_for_publications("flexi", now=PUBLISHED_UTC) == []
    assert len(ms.load_snapshot_log("flexi")) == 3

    e0 = next(snap for snap in ms.load_snapshot_log("flexi") if snap.window == "E0")
    assert e0.target_at_utc == "2026-10-28T15:06:11+00:00"


def test_snapshots_ignore_mock_ids_and_pending_rows(tmp_path, monkeypatch):
    _write_publication_log(tmp_path, [
        _ig_row(publication_id="mock_slot_1"),
        _ig_row(status="pending", publication_id=""),
    ])
    monkeypatch.chdir(tmp_path)

    assert ms.ensure_snapshots_for_publications("flexi", now=PUBLISHED_UTC) == []
    assert ms.load_snapshot_log("flexi") == []


def test_future_windows_are_not_due(tmp_path, monkeypatch):
    _write_publication_log(tmp_path, [_ig_row()])
    monkeypatch.chdir(tmp_path)
    ms.ensure_snapshots_for_publications("flexi", now=PUBLISHED_UTC)

    cutoff = ms.publication_target_utc(_ig_row())
    assert cutoff is not None
    assert ms.get_pending_snapshots("flexi", now=cutoff - timedelta(seconds=1)) == []
    assert [snap.window for snap in ms.get_pending_snapshots("flexi", now=cutoff)] == ["E0"]
    assert [snap.window for snap in ms.get_pending_snapshots("flexi", now=cutoff + timedelta(hours=24))] == ["E0", "E24"]


def test_facebook_capture_includes_reach_and_impressions(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    metrics = {
        "post_reactions_by_type_total": {"LIKE": 2, "LOVE": 1},
        "post_clicks": 7,
        "post_engaged_users": 40,
        "post_impressions": 1200,
        "post_impressions_unique": 500,
    }

    def fake_api_get(token, endpoint, params=None):
        params = params or {}
        if endpoint.endswith("/insights"):
            value = metrics.get(params.get("metric"))
            if value is None:
                return {"error": "Invalid metric"}
            return {"data": [{"name": params["metric"], "values": [{"value": value}]}]}
        if endpoint.endswith("/reactions"):
            return {"data": []}
        return {
            "reactions": {"summary": {"total_count": 3}},
            "comments": {"summary": {"total_count": 1}},
            "shares": {"count": 2},
        }

    monkeypatch.setattr(ms, "api_get", fake_api_get)
    snapshot = ms.MetricsSnapshot(publication_id="123_456", tenant_id="flexi", platform="Facebook", window="E0")
    result = ms.capture_snapshot("flexi", snapshot, "token", "")

    assert result.status == ms.SnapshotStatus.CAPTURED.value
    assert result.insights_available is True
    assert (result.reach, result.impressions, result.engaged_users, result.clicks) == (500, 1200, 40, 7)
    assert (result.reactions, result.comments, result.shares) == (3, 1, 2)
    assert (result.reaction_like, result.reaction_love) == (2, 1)


def test_instagram_capture_tolerates_unavailable_metric(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    insight_values = {"reach": 420, "views": 700, "total_interactions": 35, "saved": 4, "likes": 20, "comments": 3}

    def fake_api_get(token, endpoint, params=None):
        params = params or {}
        if endpoint.endswith("/insights"):
            value = insight_values.get(params.get("metric"))
            if value is None:
                return {"error": "Invalid metric"}
            return {"data": [{"name": params["metric"], "values": [{"value": value}]}]}
        return {"like_count": 20, "comments_count": 3, "media_type": "IMAGE"}

    monkeypatch.setattr(ms, "api_get", fake_api_get)
    snapshot = ms.MetricsSnapshot(publication_id="18129355670309228", tenant_id="flexi", platform="Instagram", window="E0")
    result = ms.capture_snapshot("flexi", snapshot, "token", "17841467713484855")

    assert result.status == ms.SnapshotStatus.CAPTURED.value
    assert (result.reach, result.views, result.total_interactions, result.saved) == (420, 700, 35, 4)
    assert result.reactions == 20 and result.comments == 3
    assert "shares" in result.error


def test_capture_public_counts_does_not_crash(monkeypatch):
    monkeypatch.setattr(ms, "api_get", lambda *args, **kwargs: {
        "reactions": {"summary": {"total_count": "5"}},
        "comments": {"summary": {"total_count": "2"}},
        "shares": {"count": "1"},
    })
    assert ms.capture_public_counts("token", "123_456") == {"reactions": 5, "comments": 2, "shares": 1}
