"""Subida de imágenes para Instagram: catbox puede devolver URLs de 0 bytes."""

from pathlib import Path

from modules.social.ig_publisher import IgPublisher


def _publisher() -> IgPublisher:
    return IgPublisher(
        page_token="token",
        ig_id="ig",
        imgbb_key="",
        asset_root=Path("."),
        image_host="catbox",
    )


def test_url_has_content_detects_zero_length(monkeypatch):
    class Response:
        status_code = 200
        headers = {"Content-Length": "0"}

        def iter_content(self, size):
            return iter(())

    monkeypatch.setattr(
        "modules.social.ig_publisher.requests.get", lambda *a, **k: Response()
    )
    assert IgPublisher._url_has_content("https://files.catbox.moe/empty.jpg") is False


def test_catbox_retries_with_reencoded_image(monkeypatch, tmp_path):
    temp_image = tmp_path / "re.jpg"
    temp_image.write_bytes(b"jpeg")
    urls = iter(["https://files.catbox.moe/broken.jpg", "https://files.catbox.moe/ok.jpg"])
    checks = iter([False, True])

    publisher = _publisher()
    monkeypatch.setattr(publisher, "_catbox_upload", lambda path: next(urls))
    monkeypatch.setattr(publisher, "_url_has_content", lambda url: next(checks))
    monkeypatch.setattr(publisher, "_reencode", lambda path: temp_image)

    result = publisher.upload_to_catbox(tmp_path / "original.jpg")

    assert result == "https://files.catbox.moe/ok.jpg"
    assert not temp_image.exists()
