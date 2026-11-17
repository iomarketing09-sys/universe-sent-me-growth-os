from pathlib import Path

from PIL import Image

from modules.social.ig_publisher import IgPublisher
from modules.social.preflight import preflight_tenant
from modules.social.publish_state import job_key


def _publisher(asset_root: Path) -> IgPublisher:
    return IgPublisher(
        page_token="page-token",
        ig_id="instagram-id",
        imgbb_key="imgbb-key",
        asset_root=asset_root,
    )


def test_publish_story_uses_story_container_and_publishes(monkeypatch, tmp_path):
    asset = tmp_path / "story.jpg"
    Image.new("RGB", (1080, 1920), "blue").save(asset, "JPEG")
    publisher = _publisher(tmp_path)
    calls = []

    monkeypatch.setattr(publisher, "upload_image", lambda path: "https://cdn.example/story.jpg")
    monkeypatch.setattr(
        publisher,
        "create_story_container",
        lambda url: calls.append(("container", url)) or "creation-123",
    )
    monkeypatch.setattr(publisher, "wait_for_container_ready", lambda creation_id: calls.append(("ready", creation_id)))
    monkeypatch.setattr(
        publisher,
        "publish_media_container",
        lambda creation_id: calls.append(("publish", creation_id)) or "published-456",
    )

    assert publisher.publish_story("story.jpg") == "published-456"
    assert calls == [
        ("container", "https://cdn.example/story.jpg"),
        ("ready", "creation-123"),
        ("publish", "creation-123"),
    ]


def test_publish_story_rejects_multiple_assets(tmp_path):
    publisher = _publisher(tmp_path)
    try:
        publisher.publish_story("one.jpg|two.jpg")
    except ValueError as exc:
        assert "un solo archivo" in str(exc)
    else:
        raise AssertionError("Expected multiple assets to be rejected")


def test_preflight_accepts_vertical_story_image(tmp_path):
    tenant = tmp_path / "tenants" / "demo"
    (tenant / "assets").mkdir(parents=True)
    (tenant / ".env").write_text(
        "FB_PAGE_ID=1\nMETA_ACCESS_TOKEN=token\nIMAGE_HOST=imgbb\nIMGBB_API_KEY=key\n",
        encoding="utf-8",
    )
    Image.new("RGB", (1080, 1920), "blue").save(tenant / "assets" / "story.jpg", "JPEG")

    class Item:
        post_type = "STORY"
        media_filename = "story.jpg"

    result = preflight_tenant("demo", item=Item(), base_path=tmp_path)

    assert result.ok is True, result.issues
    assert any(check["check"] == "story:aspect" and check["status"] == "ok" for check in result.checks)


def test_preflight_rejects_square_story_image(tmp_path):
    tenant = tmp_path / "tenants" / "demo"
    (tenant / "assets").mkdir(parents=True)
    (tenant / ".env").write_text(
        "FB_PAGE_ID=1\nMETA_ACCESS_TOKEN=token\nIMAGE_HOST=imgbb\nIMGBB_API_KEY=key\n",
        encoding="utf-8",
    )
    Image.new("RGB", (1080, 1080), "blue").save(tenant / "assets" / "square.jpg", "JPEG")

    class Item:
        post_type = "STORY"
        media_filename = "square.jpg"

    result = preflight_tenant("demo", item=Item(), base_path=tmp_path)

    assert result.ok is False
    assert any("story:aspect" in issue for issue in result.issues)


def test_story_and_feed_slots_have_distinct_state_keys():
    class Item:
        date_str = "2026-11-20"
        time_str = "19:30"
        media_filename = "story.jpg"
        post_type = "PHOTO"

    feed_key = job_key("demo", Item())
    Item.post_type = "STORY"
    story_key = job_key("demo", Item())

    assert feed_key != story_key
    assert feed_key.endswith("story.jpg")
    assert story_key.endswith("story.jpg|story")
