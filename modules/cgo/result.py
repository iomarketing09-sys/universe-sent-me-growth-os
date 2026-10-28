"""Contrato de salida del orquestador CGO."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

OK = "OK"
PARTIAL = "PARTIAL"
BLOCKED = "BLOCKED"
NOT_CONFIGURED = "NOT_CONFIGURED"
ERROR = "ERROR"

GATE_PASS = "PASS"
GATE_FAIL = "FAIL"
GATE_SKIP = "SKIP"
GATE_UNKNOWN = "UNKNOWN"
GATE_NOT_CONFIGURED = "NOT_CONFIGURED"


@dataclass
class CgoContext:
    """Configuración de una ejecución del orquestador."""

    base_path: Path
    dry_run: bool = True
    strict: bool = False
    publish: bool = False

    @property
    def tenants_dir(self) -> Path:
        return self.base_path / "tenants"

    def tenant_path(self, tenant_id: str) -> Path:
        return self.tenants_dir / tenant_id

    def tenant_ids(self) -> List[str]:
        if not self.tenants_dir.is_dir():
            return []
        return sorted(
            path.name
            for path in self.tenants_dir.iterdir()
            if path.is_dir() and (path / "config.json").is_file()
        )


@dataclass
class GateResult:
    name: str
    state: str
    reason: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "state": self.state, "reason": self.reason}


@dataclass
class CgoResult:
    capability: str
    tenant_id: Optional[str]
    status: str
    dry_run: bool
    gates: List[GateResult] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    reason: str = ""
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability": self.capability,
            "tenant_id": self.tenant_id,
            "status": self.status,
            "dry_run": self.dry_run,
            "gates": [gate.to_dict() for gate in self.gates],
            "actions": self.actions,
            "artifacts": self.artifacts,
            "next_actions": self.next_actions,
            "reason": self.reason,
            "data": self.data,
        }

    @property
    def ok(self) -> bool:
        return self.status in (OK, PARTIAL)


def action(kind: str, status: str, detail: str, **extra: Any) -> Dict[str, Any]:
    return {"kind": kind, "status": status, "detail": detail, **extra}


def status_from(gates: List[GateResult], actions: List[Dict[str, Any]]) -> str:
    """Deriva el estado global de gates y acciones."""
    states = {gate.state for gate in gates}
    if GATE_FAIL in states:
        return BLOCKED
    if GATE_NOT_CONFIGURED in states:
        return NOT_CONFIGURED
    if any(item.get("status") == "warn" for item in actions):
        return PARTIAL
    if GATE_UNKNOWN in states:
        return PARTIAL
    return OK
