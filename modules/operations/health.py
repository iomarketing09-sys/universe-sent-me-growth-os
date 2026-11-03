"""Salud de los servicios compartidos de Growth OS.

El watchdog es deliberadamente de solo lectura: consulta systemd y archivos de
salida, pero nunca reinicia servicios ni modifica datos de negocio.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "ops" / "services.yaml"
DEFAULT_STATE_FILE = ROOT / "logs" / "ops" / "alert_state.json"

SystemctlShow = Callable[[str, Sequence[str]], Optional[Mapping[str, str]]]


class RegistryError(ValueError):
    """El registro de servicios no tiene el formato esperado."""


@dataclass(frozen=True)
class ServiceSpec:
    id: str
    name: str
    building: str
    functional_owner: str
    timer_unit: str
    service_unit: str
    schedule: str
    severity: str
    max_age_minutes: Optional[int]
    next_elapse_grace_minutes: int
    output_glob: Optional[str]
    output_max_age_minutes: Optional[int]
    runbook: str


@dataclass(frozen=True)
class WorkflowSpec:
    """Chequeo de negocio que no depende de un timer concreto."""

    id: str
    name: str
    building: str
    functional_owner: str
    severity: str
    kind: str
    tenant: Optional[str]
    max_pending: Optional[int]
    max_age_minutes: Optional[int]
    max_approved_pending: Optional[int]
    runbook: str


@dataclass(frozen=True)
class Registry:
    version: int
    accountable: str
    operator: str
    alert_channel: str
    services: tuple[ServiceSpec, ...]
    workflows: tuple[WorkflowSpec, ...] = ()


def _optional_int(value: Any, field: str) -> Optional[int]:
    if value is None:
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise RegistryError(f"{field} debe ser entero") from exc
    if parsed < 0:
        raise RegistryError(f"{field} no puede ser negativo")
    return parsed


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise RegistryError(f"Falta {field}")
    return text


def load_registry(path: Path = DEFAULT_REGISTRY) -> Registry:
    """Carga y valida ``ops/services.yaml``."""
    try:
        payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise RegistryError(f"No se pudo leer el registro {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise RegistryError(f"YAML inválido en {path}: {exc}") from exc

    if not isinstance(payload, Mapping):
        raise RegistryError("El registro debe ser un objeto YAML")

    ownership = payload.get("ownership")
    if not isinstance(ownership, Mapping):
        raise RegistryError("Falta la sección ownership")

    channel = payload.get("alert_channel")
    if not isinstance(channel, Mapping):
        raise RegistryError("Falta la sección alert_channel")

    raw_services = payload.get("services")
    if not isinstance(raw_services, list) or not raw_services:
        raise RegistryError("El registro no contiene servicios")

    services: list[ServiceSpec] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(raw_services):
        if not isinstance(raw, Mapping):
            raise RegistryError(f"services[{index}] debe ser un objeto")
        service_id = _required_text(raw.get("id"), f"services[{index}].id")
        if service_id in seen_ids:
            raise RegistryError(f"ID de servicio duplicado: {service_id}")
        seen_ids.add(service_id)

        timer_unit = _required_text(raw.get("timer"), f"services[{index}].timer")
        service_unit = _required_text(raw.get("service"), f"services[{index}].service")
        if not timer_unit.endswith(".timer"):
            raise RegistryError(f"{service_id}: timer debe terminar en .timer")
        if not service_unit.endswith(".service"):
            raise RegistryError(f"{service_id}: service debe terminar en .service")

        services.append(
            ServiceSpec(
                id=service_id,
                name=_required_text(raw.get("name"), f"services[{index}].name"),
                building=_required_text(
                    raw.get("building"), f"services[{index}].building"
                ),
                functional_owner=_required_text(
                    raw.get("functional_owner"),
                    f"services[{index}].functional_owner",
                ),
                timer_unit=timer_unit,
                service_unit=service_unit,
                schedule=_required_text(
                    raw.get("schedule"), f"services[{index}].schedule"
                ),
                severity=_required_text(
                    raw.get("severity"), f"services[{index}].severity"
                ),
                max_age_minutes=_optional_int(
                    raw.get("max_age_minutes"), f"{service_id}.max_age_minutes"
                ),
                next_elapse_grace_minutes=_optional_int(
                    raw.get("next_elapse_grace_minutes", 0),
                    f"{service_id}.next_elapse_grace_minutes",
                )
                or 0,
                output_glob=(
                    str(raw["output_glob"]).strip()
                    if raw.get("output_glob")
                    else None
                ),
                output_max_age_minutes=_optional_int(
                    raw.get("output_max_age_minutes"),
                    f"{service_id}.output_max_age_minutes",
                ),
                runbook=_required_text(
                    raw.get("runbook", "docs/OPERACION_COMPARTIDA.md"),
                    f"services[{index}].runbook",
                ),
            )
        )

    raw_workflows = payload.get("workflows") or []
    if not isinstance(raw_workflows, list):
        raise RegistryError("workflows debe ser una lista")

    workflows: list[WorkflowSpec] = []
    seen_workflow_ids: set[str] = set()
    for index, raw in enumerate(raw_workflows):
        if not isinstance(raw, Mapping):
            raise RegistryError(f"workflows[{index}] debe ser un objeto")
        workflow_id = _required_text(raw.get("id"), f"workflows[{index}].id")
        if workflow_id in seen_workflow_ids:
            raise RegistryError(f"ID de workflow duplicado: {workflow_id}")
        seen_workflow_ids.add(workflow_id)
        workflows.append(
            WorkflowSpec(
                id=workflow_id,
                name=_required_text(raw.get("name"), f"workflows[{index}].name"),
                building=_required_text(
                    raw.get("building"), f"workflows[{index}].building"
                ),
                functional_owner=_required_text(
                    raw.get("functional_owner"),
                    f"workflows[{index}].functional_owner",
                ),
                severity=_required_text(
                    raw.get("severity", "warning"),
                    f"workflows[{index}].severity",
                ),
                kind=_required_text(
                    raw.get("kind", "comments_backlog"),
                    f"workflows[{index}].kind",
                ),
                tenant=(
                    str(raw["tenant"]).strip() if raw.get("tenant") else None
                ),
                max_pending=_optional_int(
                    raw.get("max_pending"), f"{workflow_id}.max_pending"
                ),
                max_age_minutes=_optional_int(
                    raw.get("max_age_minutes"), f"{workflow_id}.max_age_minutes"
                ),
                max_approved_pending=_optional_int(
                    raw.get("max_approved_pending"),
                    f"{workflow_id}.max_approved_pending",
                ),
                runbook=_required_text(
                    raw.get("runbook", "docs/OPERACION_COMPARTIDA.md"),
                    f"workflows[{index}].runbook",
                ),
            )
        )

    return Registry(
        version=int(payload.get("version", 1)),
        accountable=_required_text(ownership.get("accountable"), "ownership.accountable"),
        operator=_required_text(ownership.get("operator"), "ownership.operator"),
        alert_channel=_required_text(channel.get("type"), "alert_channel.type"),
        services=tuple(services),
        workflows=tuple(workflows),
    )


def systemctl_show(unit: str, properties: Sequence[str]) -> Optional[Mapping[str, str]]:
    """Consulta propiedades de una unit sin escribir en systemd."""
    command = [
        "systemctl",
        "show",
        unit,
        "--property=" + ",".join(properties),
        "--timestamp=unix",
        "--no-pager",
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    values: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def parse_systemd_timestamp(value: Optional[str]) -> Optional[datetime]:
    """Convierte ``@epoch`` de ``systemctl --timestamp=unix`` a datetime UTC."""
    if not value:
        return None
    raw = value.strip()
    if raw.startswith("@"):
        raw = raw[1:]
    try:
        epoch = float(raw)
    except (TypeError, ValueError):
        return None
    try:
        return datetime.fromtimestamp(epoch, tz=timezone.utc)
    except (OverflowError, OSError, ValueError):
        return None


def parse_alert_timestamp(value: Optional[str]) -> Optional[datetime]:
    """Acepta epoch de systemd o ISO-8601 del estado local."""
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return parse_systemd_timestamp(value)
    return _as_utc(parsed)


def _issue(code: str, message: str, severity: str = "critical") -> dict[str, str]:
    return {"code": code, "message": message, "severity": severity}


def _newest_output(root: Path, pattern: str) -> Optional[tuple[Path, datetime]]:
    newest: Optional[tuple[Path, datetime]] = None
    for path in root.glob(pattern):
        try:
            modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if newest is None or modified > newest[1]:
            newest = (path, modified)
    return newest


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


def _workflow_result(
    spec: WorkflowSpec,
    *,
    status: str,
    issues: list[dict[str, str]],
    output: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    return {
        "id": spec.id,
        "name": spec.name,
        "building": spec.building,
        "functional_owner": spec.functional_owner,
        "severity": spec.severity,
        "timer": None,
        "service": None,
        "schedule": "continuo",
        "status": status,
        "last_success_at": None,
        "next_elapse_at": None,
        "output": output,
        "issues": issues,
        "runbook": spec.runbook,
    }


def _status_for_issues(issues: list[dict[str, str]]) -> str:
    if any(item["severity"] == "critical" for item in issues):
        return "critical"
    if issues:
        return "warning"
    return "ok"


def _comment_first_seen(path: Path) -> dict[str, datetime]:
    """Primer avistamiento por comentario según el log local."""
    from modules.communications.comments.log import read_comment_log

    first_seen: dict[str, datetime] = {}
    for row in read_comment_log(path):
        comment_id = str(row.get("comment_id") or "").strip()
        timestamp = parse_alert_timestamp(row.get("timestamp"))
        if not comment_id or timestamp is None:
            continue
        current = first_seen.get(comment_id)
        if current is None or timestamp < current:
            first_seen[comment_id] = timestamp
    return first_seen


def check_comments_backlog(
    spec: WorkflowSpec,
    *,
    root: Path = ROOT,
    now: Optional[datetime] = None,
) -> dict[str, Any]:
    """Mide trabajo pendiente real, no solo el latido de los timers."""
    from modules.communications.comments.paths import CommentPaths

    current = _as_utc(now or datetime.now(timezone.utc))
    issues: list[dict[str, str]] = []
    try:
        paths = CommentPaths.for_tenant(spec.tenant or "universe", root)
    except ValueError as exc:
        return _workflow_result(
            spec,
            status="critical",
            issues=[_issue("tenant_invalid", str(exc))],
        )

    queue_path = paths.approvals_file
    try:
        payload = json.loads(queue_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _workflow_result(
            spec,
            status="critical",
            issues=[
                _issue(
                    "queue_unavailable",
                    f"No se pudo leer {queue_path}: {type(exc).__name__}",
                )
            ],
            output={"path": str(queue_path)},
        )

    items = payload.get("approvals") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        return _workflow_result(
            spec,
            status="critical",
            issues=[_issue("queue_invalid", "'approvals' debe ser una lista")],
            output={"path": str(queue_path)},
        )

    first_seen = _comment_first_seen(paths.comments_log_file)
    try:
        queue_modified = datetime.fromtimestamp(
            queue_path.stat().st_mtime, tz=timezone.utc
        )
    except OSError:
        queue_modified = current

    pending_review: list[dict[str, Any]] = []
    approved_pending: list[dict[str, Any]] = []
    approved_without_response = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        published = item.get("published") is True or bool(
            str(item.get("reply_id") or "").strip()
        )
        discarded = item.get("discarded") is True
        approved = item.get("approved") is True
        response = str(item.get("approved_response") or "").strip()
        if not approved and not discarded and not published:
            pending_review.append(item)
        elif approved and not published and not response:
            approved_without_response += 1
        elif approved and not published and response:
            approved_pending.append(item)

    oldest_age: Optional[float] = None
    oldest_comment_id: Optional[str] = None
    for item in pending_review:
        comment_id = str(item.get("comment_id") or "").strip()
        timestamp = (
            parse_alert_timestamp(str(item.get("first_seen_at") or ""))
            or first_seen.get(comment_id)
            or parse_alert_timestamp(str(item.get("created_time") or ""))
            or queue_modified
        )
        age = max(0.0, (current - timestamp).total_seconds() / 60)
        if oldest_age is None or age > oldest_age:
            oldest_age = age
            oldest_comment_id = comment_id or None

    if spec.max_pending is not None and len(pending_review) > spec.max_pending:
        issues.append(
            _issue(
                "review_backlog",
                f"Hay {len(pending_review)} propuestas sin revisar "
                f"(máximo {spec.max_pending})",
                severity="warning",
            )
        )
    if (
        spec.max_age_minutes is not None
        and oldest_age is not None
        and oldest_age > spec.max_age_minutes
    ):
        issues.append(
            _issue(
                "review_stale",
                f"La propuesta más vieja lleva {oldest_age:.0f} minutos sin revisar "
                f"(máximo {spec.max_age_minutes})",
                severity="warning",
            )
        )
    approved_pending_limit = (
        0 if spec.max_approved_pending is None else spec.max_approved_pending
    )
    if len(approved_pending) > approved_pending_limit:
        issues.append(
            _issue(
                "approved_not_published",
                f"{len(approved_pending)} respuestas aprobadas siguen sin publicar "
                f"(máximo {approved_pending_limit})",
            )
        )
    if approved_without_response:
        issues.append(
            _issue(
                "approved_without_response",
                f"{approved_without_response} aprobaciones no tienen texto de respuesta",
                severity="warning",
            )
        )

    output = {
        "path": str(queue_path.relative_to(root)) if queue_path.is_relative_to(root) else str(queue_path),
        "pending_review": len(pending_review),
        "approved_pending": len(approved_pending),
        "approved_without_response": approved_without_response,
        "oldest_pending_age_minutes": round(oldest_age, 1) if oldest_age is not None else None,
        "oldest_pending_comment_id": oldest_comment_id,
    }
    return _workflow_result(
        spec,
        status=_status_for_issues(issues),
        issues=issues,
        output=output,
    )


def check_workflow(
    spec: WorkflowSpec,
    *,
    root: Path = ROOT,
    now: Optional[datetime] = None,
) -> dict[str, Any]:
    if spec.kind == "comments_backlog":
        return check_comments_backlog(spec, root=root, now=now)
    return _workflow_result(
        spec,
        status="critical",
        issues=[_issue("workflow_unknown", f"Tipo de workflow desconocido: {spec.kind}")],
    )


def check_service(
    spec: ServiceSpec,
    *,
    root: Path = ROOT,
    now: Optional[datetime] = None,
    show: SystemctlShow = systemctl_show,
) -> dict[str, Any]:
    """Evalúa un servicio sin ejecutar acciones correctivas."""
    current = _as_utc(now or datetime.now(timezone.utc))
    issues: list[dict[str, str]] = []

    timer = show(
        spec.timer_unit,
        ("ActiveState", "SubState", "Result", "LastTriggerUSec", "NextElapseUSecRealtime"),
    )
    service = show(
        spec.service_unit,
        ("ActiveState", "SubState", "Result", "ExecMainStatus"),
    )

    last_trigger: Optional[datetime] = None
    next_elapse: Optional[datetime] = None
    if timer is None:
        issues.append(_issue("timer_unavailable", "No se pudo consultar el timer"))
    else:
        if timer.get("ActiveState") != "active":
            issues.append(
                _issue(
                    "timer_inactive",
                    f"Timer no activo ({timer.get('ActiveState') or 'desconocido'})",
                )
            )
        if timer.get("Result") == "failed":
            issues.append(_issue("timer_failed", "El timer reporta fallo"))
        last_trigger = parse_systemd_timestamp(timer.get("LastTriggerUSec"))
        next_elapse = parse_systemd_timestamp(timer.get("NextElapseUSecRealtime"))

        if next_elapse is not None:
            deadline = next_elapse + timedelta(minutes=spec.next_elapse_grace_minutes)
            if current > deadline:
                issues.append(
                    _issue(
                        "schedule_overdue",
                        "La siguiente ejecución programada ya venció",
                    )
                )

    if service is None:
        issues.append(
            _issue(
                "service_unavailable",
                "No se pudo consultar el servicio",
                severity="warning",
            )
        )
    else:
        result = str(service.get("Result") or "").strip()
        if result and result != "success":
            issues.append(
                _issue(
                    "service_failed",
                    f"La última ejecución terminó con Result={result}",
                )
            )

    if spec.max_age_minutes is not None:
        if last_trigger is None:
            issues.append(
                _issue("no_last_trigger", "No hay una última ejecución registrada")
            )
        else:
            age_minutes = (current - last_trigger).total_seconds() / 60
            if age_minutes > spec.max_age_minutes:
                issues.append(
                    _issue(
                        "heartbeat_stale",
                        f"Sin latido desde hace {age_minutes:.0f} minutos "
                        f"(máximo {spec.max_age_minutes})",
                    )
                )

    output_info: Optional[dict[str, Any]] = None
    if spec.output_glob:
        newest = _newest_output(root, spec.output_glob)
        if newest is None:
            issues.append(
                _issue("output_missing", f"No existe salida para {spec.output_glob}")
            )
        else:
            output_path, output_modified = newest
            output_age = (current - output_modified).total_seconds() / 60
            output_info = {
                "path": str(output_path.relative_to(root)),
                "modified_at": output_modified.isoformat(),
                "age_minutes": round(output_age, 1),
            }
            limit = spec.output_max_age_minutes
            if limit is not None and output_age > limit:
                issues.append(
                    _issue(
                        "output_stale",
                        f"La salida {output_info['path']} tiene {output_age:.0f} minutos "
                        f"(máximo {limit})",
                    )
                )

    if any(item["severity"] == "critical" for item in issues):
        status = "critical"
    elif issues:
        status = "warning"
    else:
        status = "ok"

    return {
        "id": spec.id,
        "name": spec.name,
        "building": spec.building,
        "functional_owner": spec.functional_owner,
        "severity": spec.severity,
        "timer": spec.timer_unit,
        "service": spec.service_unit,
        "schedule": spec.schedule,
        "status": status,
        "last_success_at": last_trigger.isoformat() if last_trigger else None,
        "next_elapse_at": next_elapse.isoformat() if next_elapse else None,
        "output": output_info,
        "issues": issues,
        "runbook": spec.runbook,
    }


def check_registry(
    registry: Registry,
    *,
    root: Path = ROOT,
    now: Optional[datetime] = None,
    show: SystemctlShow = systemctl_show,
) -> dict[str, Any]:
    """Devuelve un reporte JSON-serializable de toda la operación compartida."""
    current = _as_utc(now or datetime.now(timezone.utc))
    services = [
        check_service(spec, root=root, now=current, show=show)
        for spec in registry.services
    ]
    services.extend(
        check_workflow(spec, root=root, now=current)
        for spec in registry.workflows
    )
    if any(item["status"] == "critical" for item in services):
        status = "critical"
    elif any(item["status"] == "warning" for item in services):
        status = "warning"
    else:
        status = "ok"
    return {
        "generated_at": current.isoformat(),
        "status": status,
        "ownership": {
            "accountable": registry.accountable,
            "operator": registry.operator,
        },
        "alert_channel": registry.alert_channel,
        "services": services,
    }


def status_exit_code(report: Mapping[str, Any]) -> int:
    status = report.get("status")
    if status == "critical":
        return 2
    if status == "warning":
        return 1
    return 0


def problem_fingerprint(report: Mapping[str, Any]) -> str:
    problems = [
        {
            "id": service.get("id"),
            "status": service.get("status"),
            "issues": sorted(issue.get("code", "") for issue in service.get("issues", [])),
        }
        for service in report.get("services", [])
        if service.get("status") != "ok"
    ]
    return json.dumps(problems, sort_keys=True, ensure_ascii=False)


def format_alert(report: Mapping[str, Any]) -> str:
    status = str(report.get("status", "unknown")).upper()
    lines = [f"🚨 Growth OS · Operación compartida: {status}"]
    for service in report.get("services", []):
        if service.get("status") == "ok":
            continue
        lines.append("")
        lines.append(f"Servicio: {service.get('name')} ({service.get('id')})")
        lines.append(
            f"Edificio: {service.get('building')} · Owner funcional: "
            f"{service.get('functional_owner')}"
        )
        for issue in service.get("issues", []):
            lines.append(f"Problema: {issue.get('message')}")
        if service.get("last_success_at"):
            lines.append(f"Último latido: {service['last_success_at']}")
        lines.append(f"Runbook: {service.get('runbook')}")
    lines.append("")
    ownership = report.get("ownership") or {}
    lines.append(
        f"Accountable: {ownership.get('accountable', '?')} · "
        f"Operador: {ownership.get('operator', '?')}"
    )
    return "\n".join(lines)


def format_recovery(report: Mapping[str, Any]) -> str:
    ownership = report.get("ownership") or {}
    return (
        "✅ Growth OS · Operación compartida recuperada\n"
        f"Estado: {str(report.get('status', 'ok')).upper()}\n"
        f"Accountable: {ownership.get('accountable', '?')} · "
        f"Operador: {ownership.get('operator', '?')}"
    )


def load_alert_state(path: Path = DEFAULT_STATE_FILE) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def save_alert_state(path: Path, state: Mapping[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(dict(state), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def should_send_alert(
    state: Mapping[str, Any],
    fingerprint: str,
    *,
    now: Optional[datetime] = None,
    cooldown_minutes: int = 60,
) -> bool:
    if state.get("fingerprint") != fingerprint:
        return True
    last_sent = parse_alert_timestamp(str(state.get("last_sent_at", "")))
    if last_sent is None:
        return True
    current = _as_utc(now or datetime.now(timezone.utc))
    return current - last_sent >= timedelta(minutes=max(0, cooldown_minutes))
