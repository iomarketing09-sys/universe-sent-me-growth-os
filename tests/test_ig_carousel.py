"""Soporte de carruseles en la cola y el publisher de Instagram."""

from __future__ import annotations

from types import SimpleNamespace

from PIL import Image

from modules.social import ig_publisher
from modules.social.ig_publisher import IgPublisher
from modules.social.ig_scheduler import parse_tenant_schedule
from modules.social.preflight import preflight_tenant


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def test_publish_carousel_creates_children_and_parent(tmp_path, monkeypatch):
    first = tmp_path / "uno.jpg"
    second = tmp_path / "dos.jpg"
    first.write_bytes(b"uno")
    second.write_bytes(b"dos")
    publisher = IgPublisher("token", "ig", "key", tmp_path)
    payloads = [
        {"id": "child-1"},
        {"id": "child-2"},
        {"id": "carousel"},
        {"id": "post-1"},
    ]
    calls = []

    def fake_post(url, **kwargs):
        calls.append((url, kwargs["data"]))
        return FakeResponse(payloads.pop(0))

    monkeypatch.setattr(ig_publisher.requests, "post", fake_post)
    monkeypatch.setattr(
        publisher,
        "upload_image",
        lambda path: f"https://images.example/{path.name}",
    )
    monkeypatch.setattr(publisher, "wait_for_container_ready", lambda container_id: True)

    result = publisher.publish("uno.jpg|dos.jpg", "Caption")

    assert result == "post-1"
    item_payloads = [data for url, data in calls[:2] if url.endswith("/media")]
    assert [data["is_carousel_item"] for data in item_payloads] == ["true", "true"]
    assert calls[2][1]["media_type"] == "CAROUSEL"
    assert calls[2][1]["children"] == "child-1,child-2"
    assert calls[3][1]["creation_id"] == "carousel"


def test_parse_schedule_keeps_pipe_separated_carousel(tmp_path):
    tenant_dir = tmp_path / "tenants" / "demo"
    tenant_dir.mkdir(parents=True)
    (tenant_dir / "meta_import.csv").write_text(
        'Date (YYYY-MM-DD),"Time (HH:MM, 24h)",Timezone,Post Type,Media URL,Caption,Link URL,Hashtags,Location,First Comment\n'
        '2026-11-03,19:00,America/Matamoros,CAROUSEL,uno.jpg|dos.jpg,Caption,,,,\n',
        encoding="utf-8",
    )

    items = parse_tenant_schedule("demo", base_path=tmp_path)

    assert len(items) == 1
    assert items[0].post_type == "CAROUSEL"
    assert items[0].media_filename == "uno.jpg|dos.jpg"


def test_preflight_accepts_carousel_assets(tmp_path):
    tenant_dir = tmp_path / "tenants" / "demo"
    assets = tenant_dir / "assets"
    assets.mkdir(parents=True)
    (tenant_dir / ".env").write_text(
        "FB_PAGE_ID=1\nMETA_ACCESS_TOKEN=token\nIMAGE_HOST=imgbb\nIMGBB_API_KEY=key\n",
        encoding="utf-8",
    )
    Image.new("RGB", (800, 1000), "red").save(assets / "uno.jpg", "JPEG")
    Image.new("RGB", (800, 1000), "blue").save(assets / "dos.jpg", "JPEG")
    item = SimpleNamespace(post_type="CAROUSEL", media_filename="uno.jpg|dos.jpg")

    result = preflight_tenant("demo", item=item, base_path=tmp_path)

    assert result.ok is True
    assert not any(check["check"] == "format" and check["status"] == "fail" for check in result.checks)
