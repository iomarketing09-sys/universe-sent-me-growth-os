"""Tests offline del backfill lifetime de Universe."""

from __future__ import annotations

from tenants.universe.metrics import backfill_lifetime as bf


def test_build_backfill_snapshot_marks_lifetime_window(monkeypatch):
    def fake_api_get(token, endpoint, params=None):
        return {
            "reactions": {"summary": {"total_count": 10}},
            "comments": {"summary": {"total_count": 2}},
            "shares": {"count": 3},
        }

    def fake_capture_post_insights(token, post_id):
        return {
            "post_clicks": 7,
            "post_reactions_by_type_total": {"LIKE": 6, "LOVE": 4},
            "_unavailable_metrics": "post_video_views",
            "_unavailable_reasons": {"post_video_views": "retired"},
        }

    monkeypatch.setattr(bf, "api_get", fake_api_get)
    monkeypatch.setattr(bf, "capture_post_insights", fake_capture_post_insights)

    snapshot = bf.build_backfill_snapshot(
        "token", "1036844829507460_123", "2026-10-31T06:00:00+00:00"
    )

    assert snapshot.window == "LIFETIME_BACKFILL"
    assert snapshot.platform == "Facebook"
    assert snapshot.publication_id == "1036844829507460_123"
    assert (snapshot.reactions, snapshot.comments, snapshot.shares) == (10, 2, 3)
    assert snapshot.total_interactions == 15
    assert (snapshot.reaction_like, snapshot.reaction_love) == (6, 4)
    assert snapshot.clicks == 7
    assert snapshot.insights_available is True
    assert snapshot.unavailable_metrics == "post_video_views,post_video_views:retired"
    assert snapshot.status == bf.SnapshotStatus.CAPTURED.value


def test_facebook_post_ids_are_unique_and_facebook_only():
    snapshots = [
        bf.MetricsSnapshot(publication_id="1", platform="Facebook"),
        bf.MetricsSnapshot(publication_id="1", platform="Facebook", window="E24"),
        bf.MetricsSnapshot(publication_id="2", platform="Instagram"),
        bf.MetricsSnapshot(publication_id="3", platform="Facebook"),
    ]

    assert bf.facebook_post_ids(snapshots) == ["1", "3"]
