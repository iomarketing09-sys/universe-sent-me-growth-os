"""Orquestador CGO: despacha capacidades a los módulos dueños."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from modules.cgo.capabilities import ALL_TENANTS, CAPABILITIES
from modules.cgo.result import BLOCKED, GATE_UNKNOWN, CgoContext, CgoResult


def project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


class CgoOrchestrator:
    """Punto único de entrada para las 8 capacidades del Growth OS."""

    def __init__(
        self,
        base_path: Optional[str] = None,
        dry_run: bool = True,
        strict: bool = False,
        publish: bool = False,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ):
        self.ctx = CgoContext(
            base_path=Path(base_path) if base_path else project_root(),
            dry_run=dry_run,
            strict=strict,
            publish=publish,
            since=since,
            until=until,
        )

    @property
    def capabilities(self) -> List[str]:
        return sorted(CAPABILITIES)

    def run(self, capability: str, tenant_id: Optional[str] = None) -> List[CgoResult]:
        """Ejecuta una capacidad para un tenant o para todos."""
        if capability not in CAPABILITIES:
            raise ValueError(
                f"Capacidad desconocida: {capability}. Válidas: {', '.join(self.capabilities)}"
            )

        handler = CAPABILITIES[capability]
        if capability in ALL_TENANTS:
            results = [handler(self.ctx, tenant_id)]
        else:
            tenants = [tenant_id] if tenant_id else self.ctx.tenant_ids()
            if not tenants:
                raise ValueError("No hay tenants con config.json para ejecutar la capacidad.")
            results = [handler(self.ctx, current) for current in tenants]

        if self.ctx.strict:
            results = [self._apply_strict(result) for result in results]
        return results

    def run_one(self, capability: str, tenant_id: Optional[str] = None) -> CgoResult:
        results = self.run(capability, tenant_id)
        return results[0] if len(results) == 1 else results[-1]

    @staticmethod
    def _apply_strict(result: CgoResult) -> CgoResult:
        unknown = [gate for gate in result.gates if gate.state == GATE_UNKNOWN]
        if unknown and result.status != BLOCKED:
            result.status = BLOCKED
            detail = "; ".join(f"{gate.name}: {gate.reason}" for gate in unknown)
            result.reason = f"strict: {detail}"
        return result
