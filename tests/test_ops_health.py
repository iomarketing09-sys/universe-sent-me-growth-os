"""Pruebas del watchdog de operación compartida."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from modules.operations.health import (
    ServiceSpec,
    WorkflowSpec,
    check_comments_backlog,
    check_service,
    format_alert,
    load_registry,
    should_send_alert,
)
from modules.communications.comments.paths import CommentPaths
from modules.operations.telegram import send_message
from tests.tenant_factory import make_tenant


NOW = datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc)


def _epoch(value: datetime) -> str:
    return f"@{int(value.timestamp())}"


def _spec(**overrides) -> ServiceSpec:
    values = {
        "id": "test-service",
        "name": "Servicio de prueba",
        "building": "communications",
        "functional_owner": "communications",
        "timer_unit": "growth-os-test.timer",
        "service_unit": "growth-os-test.service",
        "schedule": "cada 15 minutos",
        "severity": "high",
        "max_age_minutes": 45,
        "next_elapse_grace_minutes": 15,
        "output_glob": None,
        "output_max_age_minutes": None,
        "runbook": "docs/OPERACION_COMPARTIDA.md#test-service",
    }
    values.update(overrides)
    return ServiceSpec(**values)


def _show(*, last_trigger=NOW - timedelta(minutes=10), service_result="success"):
    def fake(unit, properties):
        if unit.endswith(".timer"):
            return {
                "ActiveState": "active",
                "SubState": "waiting",
                "Result": "success",
                "LastTriggerUSec": _epoch(last_trigger) if last_trigger else "",
                "NextElapseUSecRealtime": "",
            }
        return {
            "ActiveState": "inactive",
            "SubState": "dead",
            "Result": service_result,
            "ExecMainStatus": "0" if service_result == "success" else "1",
        }

    return fake


def _workflow_spec(**overrides) -> WorkflowSpec:
    values = {
        "id": "comments-review-backlog",
        "name": "Backlog de comentarios",
        "building": "communications",
        "functional_owner": "communications",
        "severity": "high",
        "kind": "comments_backlog",
        "tenant": "digital",
        "max_pending": 5,
        "max_age_minutes": 240,
        "max_approved_pending": 0,
        "runbook": "docs/OPERACION_COMPARTIDA.md#comments-backlog",
    }
    values.update(overrides)
    return WorkflowSpec(**values)


def _write_comments_queue(root: Path, items: list[dict]) -> CommentPaths:
    make_tenant(root, "digital", track="native_digital")
    paths = CommentPaths.for_tenant("digital", root)
    paths.storage_dir.mkdir(parents=True, exist_ok=True)
    paths.approvals_file.write_text(
        json.dumps({"approvals": items}, ensure_ascii=False),
        encoding="utf-8",
    )
    return paths


def test_registry_has_no_manus_owner():
    registry = load_registry(Path("ops/services.yaml"))

    assert registry.accountable == "Fernando"
    assert registry.operator == "CGO"
    assert "manus" not in registry.accountable.lower()
    assert "manus" not in registry.operator.lower()
    assert len(registry.services) == 5
    assert len(registry.workflows) == 1
    assert registry.workflows[0].kind == "comments_backlog"
    assert registry.workflows[0].tenant == "universe"


def test_healthy_service_has_no_issues():
    result = check_service(_spec(), now=NOW, show=_show())

    assert result["status"] == "ok"
    assert result["issues"] == []
    assert result["last_success_at"] == (NOW - timedelta(minutes=10)).isoformat()


def test_failed_service_is_critical():
    result = check_service(_spec(), now=NOW, show=_show(service_result="exit-code"))

    assert result["status"] == "critical"
    assert any(issue["code"] == "service_failed" for issue in result["issues"])


def test_stale_heartbeat_is_critical():
    result = check_service(
        _spec(max_age_minutes=15),
        now=NOW,
        show=_show(last_trigger=NOW - timedelta(minutes=40)),
    )

    assert result["status"] == "critical"
    assert any(issue["code"] == "heartbeat_stale" for issue in result["issues"])


def test_stale_output_is_critical(tmp_path):
    output = tmp_path / "out.json"
    output.write_text("{}", encoding="utf-8")
    old = (NOW - timedelta(hours=2)).timestamp()
    os.utime(output, (old, old))

    result = check_service(
        _spec(output_glob="out.json", output_max_age_minutes=60),
        root=tmp_path,
        now=NOW,
        show=_show(),
    )

    assert result["status"] == "critical"
    assert any(issue["code"] == "output_stale" for issue in result["issues"])


def test_identical_alert_respects_cooldown():
    fingerprint = '[{"id": "test-service", "issues": ["timer_inactive"]}]'
    state = {
        "active": True,
        "fingerprint": fingerprint,
        "last_sent_at": NOW.isoformat(),
    }

    assert not should_send_alert(state, fingerprint, now=NOW, cooldown_minutes=60)
    assert should_send_alert(
        state, fingerprint, now=NOW + timedelta(minutes=61), cooldown_minutes=60
    )


def test_alert_message_contains_service_and_runbook():
    result = check_service(_spec(), now=NOW, show=_show(service_result="exit-code"))
    report = {
        "status": "critical",
        "ownership": {"accountable": "Fernando", "operator": "CGO"},
        "services": [result],
    }

    message = format_alert(report)

    assert "Servicio de prueba" in message
    assert "docs/OPERACION_COMPARTIDA.md#test-service" in message
    assert "Fernando" in message


def test_telegram_message_uses_plain_text_payload():
    captured = {}

    class Response:
        def read(self):
            return b'{"ok": true}'

        def close(self):
            return None

    def opener(request, timeout):
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return Response()

    result = send_message(
        "Hola operación",
        token="test-token",
        chat_id="123",
        opener=opener,
    )

    assert result["ok"] is True
    assert captured["body"]["text"] == "Hola operación"
    assert captured["body"]["chat_id"] == "123"
    assert captured["timeout"] == 10


def test_comments_backlog_verde_con_pocas_propuestas_recientes(tmp_path):
    _write_comments_queue(
        tmp_path,
        [
            {
                "comment_id": "c1",
                "approved": False,
                "first_seen_at": (NOW - timedelta(hours=1)).isoformat(),
            }
        ],
    )

    result = check_comments_backlog(_workflow_spec(), root=tmp_path, now=NOW)

    assert result["status"] == "ok"
    assert result["output"]["pending_review"] == 1
    assert result["output"]["approved_pending"] == 0


def test_comments_backlog_avisa_por_cola_y_antiguedad(tmp_path):
    items = [
        {
            "comment_id": f"c{index}",
            "approved": False,
            "first_seen_at": (NOW - timedelta(hours=1)).isoformat(),
        }
        for index in range(6)
    ]
    items[0]["first_seen_at"] = (NOW - timedelta(hours=5)).isoformat()
    _write_comments_queue(tmp_path, items)

    result = check_comments_backlog(_workflow_spec(), root=tmp_path, now=NOW)

    assert result["status"] == "warning"
    codes = {issue["code"] for issue in result["issues"]}
    assert {"review_backlog", "review_stale"} <= codes
    assert result["output"]["oldest_pending_age_minutes"] == 300.0


def test_comments_backlog_critico_si_hay_aprobadas_sin_publicar(tmp_path):
    _write_comments_queue(
        tmp_path,
        [
            {
                "comment_id": "c1",
                "approved": True,
                "approved_response": "Hola",
                "first_seen_at": (NOW - timedelta(minutes=30)).isoformat(),
            }
        ],
    )

    result = check_comments_backlog(_workflow_spec(), root=tmp_path, now=NOW)

    assert result["status"] == "critical"
    assert any(
        issue["code"] == "approved_not_published" for issue in result["issues"]
    )
