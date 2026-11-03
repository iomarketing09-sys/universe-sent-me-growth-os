"""El publisher no debe escribir fragmentos de token en el log."""

from __future__ import annotations

import pytest

from modules.social import meta_publisher

TOKEN = "SECRETO1234567890ABCDEF"


class FakeResponse:
    status_code = 200

    def json(self):
        return {"access_token": TOKEN}


def test_get_page_token_no_expone_token(monkeypatch):
    monkeypatch.setattr(
        meta_publisher.requests, "get", lambda *args, **kwargs: FakeResponse()
    )
    messages = []
    monkeypatch.setattr(
        meta_publisher.logger, "info", lambda msg, *args, **kwargs: messages.append(str(msg))
    )

    publisher = meta_publisher.MetaPublisher(page_id="1", access_token="x", dry_run=True)

    assert publisher._get_page_access_token() == TOKEN
    text = " ".join(messages)
    assert TOKEN[:20] not in text
    assert "Token de página obtenido correctamente." in text


def test_real_mode_error_no_expone_token():
    with pytest.raises(ValueError) as exc_info:
        meta_publisher.MetaPublisher(
            page_id="",
            dry_run=False,
            environment={"META_ACCESS_TOKEN": TOKEN},
        )

    assert TOKEN not in str(exc_info.value)
