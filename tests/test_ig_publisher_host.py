"""Tests del host de imágenes del publisher de Instagram."""

from __future__ import annotations

import pytest

from modules.social import ig_publisher
from modules.social.ig_publisher import IgPublisher, load_tenant_credentials


class FakeResponse:
    def __init__(self, status_code=200, text="", payload=None):
        self.status_code = status_code
        self.text = text
        self._payload = payload or {}

    def json(self):
        return self._payload


def _publisher(tmp_path, host):
    asset = tmp_path / "foto.jpg"
    asset.write_bytes(b"fake-image")
    return IgPublisher(
        page_token="page-token",
        ig_id="17841400000000000",
        imgbb_key="key",
        asset_root=tmp_path,
        image_host=host,
    ), asset


def test_catbox_devuelve_url(tmp_path, monkeypatch):
    publisher, asset = _publisher(tmp_path, "catbox")
    calls = []

    def fake_post(url, **kwargs):
        calls.append(url)
        return FakeResponse(200, "https://files.catbox.moe/abc.png")

    monkeypatch.setattr(ig_publisher.requests, "post", fake_post)

    assert publisher.upload_image(asset) == "https://files.catbox.moe/abc.png"
    assert calls == ["https://catbox.moe/user/api.php"]


def test_imgbb_es_default(tmp_path, monkeypatch):
    publisher, asset = _publisher(tmp_path, "imgbb")
    calls = []

    def fake_post(url, **kwargs):
        calls.append(url)
        return FakeResponse(200, payload={"success": True, "data": {"url": "https://i.ibb.co/x.png"}})

    monkeypatch.setattr(ig_publisher.requests, "post", fake_post)

    assert publisher.upload_image(asset) == "https://i.ibb.co/x.png"
    assert calls == ["https://api.imgbb.com/1/upload"]


def test_catbox_error_no_devuelve_basura(tmp_path, monkeypatch):
    publisher, asset = _publisher(tmp_path, "catbox")
    monkeypatch.setattr(
        ig_publisher.requests, "post", lambda url, **k: FakeResponse(400, "forbidden")
    )

    with pytest.raises(RuntimeError, match="catbox"):
        publisher.upload_image(asset)


def test_host_invalido_falla(tmp_path):
    with pytest.raises(ValueError, match="IMAGE_HOST"):
        IgPublisher("t", "1", "k", tmp_path, image_host="otro")


def _write_env(tmp_path, lines):
    root = tmp_path / "tenants" / "demo"
    root.mkdir(parents=True)
    (root / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def test_credenciales_catbox_no_exige_imgbb(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_env(
        tmp_path,
        ["FB_PAGE_ID=1", "META_ACCESS_TOKEN=t", "IMAGE_HOST=catbox"],
    )

    creds = load_tenant_credentials("demo")
    assert creds["IMAGE_HOST"] == "catbox"


def test_credenciales_imgbb_exige_key(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_env(tmp_path, ["FB_PAGE_ID=1", "META_ACCESS_TOKEN=t"])

    with pytest.raises(ValueError, match="IMGBB_API_KEY"):
        load_tenant_credentials("demo")
