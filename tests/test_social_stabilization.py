"""Pruebas de la Fase 1 de estabilización de Social."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from PIL import Image

from modules.social import ig_scheduler
from modules.social.preflight import preflight_tenant
from modules.social.publish_state import (
    STATUS_BLOCKED,
    STATUS_DEAD,
    STATUS_PUBLISHED,
    STATUS_RETRY,
    PublishJobStore,
    job_key,
)


class Item:
    tenant_id = "demo"
    date_str = "2026-11-02"
    time_str = "10:00"
    media_filename = "foto.jpg"
    caption = "Hola"
    post_type = "PHOTO"


def _tenant(base: Path, name: str = "demo", *, with_env: bool = True) -> Path:
    root = base / "tenants" / name
    root.mkdir(parents=True)
    if with_env:
        (root / ".env").write_text(
            "FB_PAGE_ID=1\nMETA_ACCESS_TOKEN=token\nIMAGE_HOST=imgbb\nIMGBB_API_KEY=key\n",
            encoding="utf-8",
        )
    assets = root / "assets"
    assets.mkdir()
    Image.new("RGB", (1080, 1350), "red").save(assets / "foto.jpg", "JPEG")
    return root


def _schedule(root: Path, when: datetime) -> None:
    with (root / "meta_import.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "Media URL",
                "Caption",
                "Hashtags",
                "Link URL",
                "Post Type",
                "Date (YYYY-MM-DD)",
                "Time (HH:MM, 24h)",
                "Timezone",
                "First Comment",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "Media URL": "foto.jpg",
                "Caption": "Hola",
                "Hashtags": "",
                "Link URL": "",
                "Post Type": "PHOTO",
                "Date (YYYY-MM-DD)": when.date().isoformat(),
                "Time (HH:MM, 24h)": when.strftime("%H:%M"),
                "Timezone": "America/Matamoros",
                "First Comment": "",
            }
        )


def test_failure_uses_exponential_backoff_and_dead_letters(tmp_path):
    now = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)
    store = PublishJobStore(
        tmp_path,
        "demo",
        max_attempts=3,
        base_delay_seconds=900,
        clock=lambda: now,
    )
    key = job_key("demo", Item())

    first = store.record_failure(key, Item(), "timeout")
    assert first.status == STATUS_RETRY
    assert first.next_attempt_at == "2026-11-02T12:15:00+00:00"

    second = store.record_failure(key, Item(), "timeout")
    assert second.next_attempt_at == "2026-11-02T12:30:00+00:00"

    third = store.record_failure(key, Item(), "timeout")
    assert third.status == STATUS_DEAD
    assert third.next_attempt_at is None
    assert store.is_due(key, now + timedelta(days=1)) is False
    assert [job.key for job in store.dead_letters()] == [key]
    assert store.dead_letter_path.read_text(encoding="utf-8").count("\n") == 1


def test_success_is_terminal_and_idempotent(tmp_path):
    store = PublishJobStore(tmp_path, "demo")
    key = job_key("demo", Item())

    job = store.record_success(key, Item(), "ig_123")

    assert job.status == STATUS_PUBLISHED
    assert job.publication_id == "ig_123"
    assert store.is_due(key) is False


def test_release_returns_blocked_job_to_queue(tmp_path):
    store = PublishJobStore(tmp_path, "demo")
    key = job_key("demo", Item())
    store.mark_blocked(key, Item(), "asset faltante")

    assert store.get(key).status == STATUS_BLOCKED
    assert store.is_due(key) is False

    released = store.release(key)

    assert released.status == STATUS_RETRY
    assert released.attempts == 0
    assert store.is_due(key) is True


def test_preflight_passes_valid_feed_image(tmp_path):
    _tenant(tmp_path)

    result = preflight_tenant("demo", item=Item(), base_path=tmp_path)

    assert result.ok is True
    assert {check["check"] for check in result.checks} >= {
        "credentials",
        "image_host",
        "format",
        "asset",
        "asset:dimensions",
    }


def test_preflight_blocks_catbox_and_video(tmp_path):
    root = _tenant(tmp_path)
    (root / ".env").write_text(
        "FB_PAGE_ID=1\nMETA_ACCESS_TOKEN=token\nIMAGE_HOST=catbox\n",
        encoding="utf-8",
    )

    item = Item()
    item.post_type = "VIDEO"
    result = preflight_tenant("demo", item=item, base_path=tmp_path)

    assert result.ok is False
    assert any("catbox" in issue for issue in result.issues)
    assert any("VIDEO" in issue for issue in result.issues)


def test_preflight_blocks_wrong_dimensions(tmp_path):
    root = _tenant(tmp_path)
    Image.new("RGB", (300, 600), "blue").save(root / "assets" / "foto.jpg", "JPEG")

    result = preflight_tenant("demo", item=Item(), base_path=tmp_path)

    assert result.ok is False
    assert any("dimensiones" in issue or "mínimo" in issue for issue in result.issues)


class FakePublisher:
    ig_id = "ig_demo"

    def __init__(self, fail: bool = False):
        self.fail = fail
        self.calls = 0

    def publish(self, media_filename, caption):
        self.calls += 1
        if self.fail:
            raise RuntimeError("Meta timeout")
        return "ig_123"


def test_run_once_isolates_tenant_failures_and_applies_backoff(tmp_path, monkeypatch):
    now = datetime.now(timezone.utc)
    when = (now - timedelta(minutes=5)).astimezone(ZoneInfo("America/Matamoros"))
    good = _tenant(tmp_path, "good")
    bad = _tenant(tmp_path, "bad")
    _schedule(good, when)
    _schedule(bad, when)

    publishers = {"good": FakePublisher(), "bad": FakePublisher(fail=True)}
    monkeypatch.setattr(
        ig_scheduler,
        "create_ig_publisher_for_tenant",
        lambda tenant_id, base_path=None: publishers[tenant_id],
    )

    scheduler = ig_scheduler.IgScheduler(
        ["good", "bad"],
        base_path=tmp_path,
        max_attempts=3,
        base_delay_seconds=900,
        clock=lambda: now,
    )

    first = scheduler.run_once()
    assert first["published"] == 1
    assert first["failed"] == 1
    assert publishers["good"].calls == 1
    assert publishers["bad"].calls == 1

    second = scheduler.run_once()
    assert second["published"] == 0
    assert second["failed"] == 0
    assert second["skipped_backoff"] == 1
    assert publishers["bad"].calls == 1

    bad_state = json.loads(
        (bad / "data" / "social" / "publish_state.json").read_text(encoding="utf-8")
    )
    assert len(bad_state["jobs"]) == 1
    assert next(iter(bad_state["jobs"].values()))["status"] == STATUS_RETRY
