"""Pruebas del heartbeat hacia el monitor externo."""

from __future__ import annotations

import pytest

from scripts.ping_external_monitor import HeartbeatError, load_heartbeat_url, ping


def test_lee_la_url_desde_el_env_sin_exponerla(tmp_path):
    (tmp_path / ".env").write_text(
        "EXTERNAL_MONITOR_HEARTBEAT_URL=https://monitor.example/heartbeat/abc\n",
        encoding="utf-8",
    )

    assert (
        load_heartbeat_url(tmp_path, environ={})
        == "https://monitor.example/heartbeat/abc"
    )


def test_ping_acepta_200():
    class Response:
        status = 200

        def close(self):
            return None

    def opener(request, timeout):
        assert request.method == "GET"
        assert timeout == 10
        return Response()

    assert ping("https://monitor.example/heartbeat/abc", opener=opener) == 200


def test_ping_falla_si_el_monitor_responde_503():
    class Response:
        status = 503

        def close(self):
            return None

    def opener(request, timeout):
        return Response()

    with pytest.raises(HeartbeatError):
        ping("https://monitor.example/heartbeat/abc", opener=opener)
