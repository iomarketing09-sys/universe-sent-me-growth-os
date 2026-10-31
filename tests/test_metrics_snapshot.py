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


def test_stale_windows_are_not_created(tmp_path, monkeypatch):
    _write_publication_log(tmp_path, [_ig_row()])
    monkeypatch.chdir(tmp_path)

    now = PUBLISHED_UTC + timedelta(hours=30)
    created = ms.ensure_snapshots_for_publications("flexi", now=now)

    assert [snap.window for snap in created] == ["E72"]


def test_facebook_capture_uses_vigentes_metrics(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    metrics = {
        "post_reactions_by_type_total": {"LIKE": 2, "LOVE": 1},
        "post_clicks": 7,
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
    assert result.clicks == 7
    assert (result.reactions, result.comments, result.shares) == (3, 1, 2)
    assert (result.reaction_like, result.reaction_love) == (2, 1)
    assert "post_video_views" in result.unavailable_metrics


def test_facebook_capture_marks_retired_metrics(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    def fake_api_get(token, endpoint, params=None):
        params = params or {}
        if endpoint.endswith("/insights"):
            return {"error": "The value must be a valid insights metric"}
        if endpoint.endswith("/reactions"):
            return {"data": []}
        return {"reactions": {"summary": {"total_count": 0}}}

    monkeypatch.setattr(ms, "api_get", fake_api_get)
    snapshot = ms.MetricsSnapshot(publication_id="123_456", tenant_id="flexi", platform="Facebook", window="E0")
    result = ms.capture_snapshot("flexi", snapshot, "token", "")

    assert result.insights_available is False
    assert result.reach == 0 and result.impressions == 0
    assert "retired" in result.error
    assert result.status == ms.SnapshotStatus.NO_DATA.value


def test_page_insights_use_vigentes_metrics(monkeypatch):
    calls = []

    def fake_api_get(token, endpoint, params=None):
        params = params or {}
        calls.append(params["metric"])
        return {"data": [{"name": params["metric"], "values": [{"value": 12}]}]}

    monkeypatch.setattr(ms, "api_get", fake_api_get)
    result = ms.capture_page_insights("token", "page", 0, 10)

    assert calls == ms.FACEBOOK_PAGE_INSIGHT_METRICS
    assert result["page_post_engagements"] == 12


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


def test_normalize_snapshot_log_migrates_mixed_rows(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tenant = tmp_path / "tenants" / "universe"
    metrics_dir = tenant / "metrics"
    metrics_dir.mkdir(parents=True)
    target = metrics_dir / "metrics_snapshot_log.csv"
    log_path = tenant / "metrics_snapshot_log.csv"
    log_path.symlink_to(Path("metrics/metrics_snapshot_log.csv"))

    old_header = [
        field for field in ms.SNAPSHOT_LOG_FIELDS
        if field not in {"views", "saved", "total_interactions", "unavailable_metrics", "attempts"}
    ]
    canonical = {field: "" for field in old_header}
    canonical.update({
        "snapshot_id": "SNAP-CANONICAL",
        "publication_id": "18105325243907452",
        "tenant_id": "universe",
        "platform": "Instagram",
        "window": "E0",
        "target_at_utc": "2026-09-06T08:37:40+00:00",
        "captured_at_utc": "2026-09-06T08:42:02+00:00",
        "status": "Captured",
        "insights_available": "False",
        "created_at": "2026-09-06T08:37:40+00:00",
    })
    legacy = [
        "2026-09-21T00:04:30+00:00",
        "1036844829507460_123",
        "2026-09-19T00:00:01+0000",
        "48.0",
        "E48h",
        "General",
        "10",
        "2",
        "5",
        "17",
        "caption",
        "https://www.facebook.com/example",
    ]

    with target.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(old_header)
        writer.writerow([canonical[field] for field in old_header])
        writer.writerow(legacy)

    result = ms.normalize_snapshot_log("universe")

    assert result["canonical"] == 1
    assert result["legacy"] == 1
    assert result["skipped"] == 0
    assert log_path.is_symlink()
    assert Path(result["backup"]).name.startswith("metrics_snapshot_log.pre-normalize-")

    snapshots = ms.load_snapshot_log("universe")
    assert len(snapshots) == 2
    migrated = next(snap for snap in snapshots if snap.publication_id.endswith("_123"))
    assert migrated.platform == "Facebook"
    assert migrated.window == "E48h"
    assert migrated.status == ms.SnapshotStatus.CAPTURED.value
    assert (migrated.reactions, migrated.comments, migrated.shares) == (10, 2, 5)
    assert migrated.total_interactions == 17

    assert ms.normalize_snapshot_log("universe")["changed"] == 0


def test_lifetime_backfill_window_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    snapshot = ms.MetricsSnapshot(
        snapshot_id="SNAP-BF-TEST",
        publication_id="1036844829507460_123",
        tenant_id="universe",
        platform="Facebook",
        window="LIFETIME_BACKFILL",
        target_at_utc="2026-10-31T06:00:00+00:00",
        captured_at_utc="2026-10-31T06:00:00+00:00",
        reactions=10,
        comments=2,
        shares=3,
        total_interactions=15,
        status=ms.SnapshotStatus.CAPTURED.value,
        insights_available=True,
    )

    ms.save_snapshot_log("universe", [snapshot])
    loaded = ms.load_snapshot_log("universe")

    assert len(loaded) == 1
    assert loaded[0].window == "LIFETIME_BACKFILL"
    assert loaded[0].total_interactions == 15


def test_dedupe_snapshot_log_keeps_first_captured_window(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    base = {
        "publication_id": "1036844829507460_123",
        "tenant_id": "universe",
        "platform": "Facebook",
        "window": "E24",
        "target_at_utc": "2026-09-21T00:06:02+00:00",
        "reactions": 2,
    }
    snapshots = [
        ms.MetricsSnapshot(
            **base,
            snapshot_id="SNAP-NO-DATA",
            captured_at_utc="2026-09-21T00:04:00+00:00",
            status=ms.SnapshotStatus.NO_DATA.value,
        ),
        ms.MetricsSnapshot(
            **base,
            snapshot_id="SNAP-CAPTURED-EARLY",
            captured_at_utc="2026-09-21T00:08:00+00:00",
            status=ms.SnapshotStatus.CAPTURED.value,
        ),
        ms.MetricsSnapshot(
            **base,
            snapshot_id="SNAP-CAPTURED-LATE",
            captured_at_utc="2026-09-21T05:29:00+00:00",
            status=ms.SnapshotStatus.CAPTURED.value,
        ),
        ms.MetricsSnapshot(
            publication_id="",
            tenant_id="universe",
            platform="Facebook",
            window="E24",
            snapshot_id="SNAP-UNATTRIBUTED",
            captured_at_utc="2026-09-21T00:09:00+00:00",
            status=ms.SnapshotStatus.CAPTURED.value,
        ),
    ]
    ms.save_snapshot_log("universe", snapshots)

    result = ms.dedupe_snapshot_log("universe")

    assert result["removed"] == 2
    assert result["kept"] == 2
    assert Path(result["backup"]).name.startswith("metrics_snapshot_log.pre-dedupe-")
    loaded = ms.load_snapshot_log("universe")
    assert {snap.snapshot_id for snap in loaded} == {"SNAP-CAPTURED-EARLY", "SNAP-UNATTRIBUTED"}
    assert ms.dedupe_snapshot_log("universe")["changed"] == 0


def test_dedupe_dry_run_does_not_write(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    snapshot = ms.MetricsSnapshot(
        snapshot_id="SNAP-1",
        publication_id="pub-1",
        tenant_id="universe",
        platform="Facebook",
        window="E0",
        captured_at_utc="2026-09-21T00:00:00+00:00",
        status=ms.SnapshotStatus.CAPTURED.value,
    )
    duplicate = ms.MetricsSnapshot(
        snapshot_id="SNAP-2",
        publication_id="pub-1",
        tenant_id="universe",
        platform="Facebook",
        window="E0",
        captured_at_utc="2026-09-21T00:10:00+00:00",
        status=ms.SnapshotStatus.CAPTURED.value,
    )
    ms.save_snapshot_log("universe", [snapshot, duplicate])

    result = ms.dedupe_snapshot_log("universe", dry_run=True)

    assert result["removed"] == 1
    assert result["backup"] == ""
    assert len(ms.load_snapshot_log("universe")) == 2
