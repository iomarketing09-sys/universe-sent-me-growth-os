"""canon_sync: pre-check del repo canon (solo native_digital)."""

from __future__ import annotations

from modules.cgo.gates import canon_path, gate_canon, gate_config, gate_track
from modules.cgo.result import CgoContext, CgoResult, action, status_from


def run(ctx: CgoContext, tenant_id: str) -> CgoResult:
    gates = [
        gate_track(ctx, "canon_sync", tenant_id),
        gate_config(ctx, tenant_id)[0],
        gate_canon(ctx, tenant_id),
    ]
    if any(gate.state == "FAIL" for gate in gates):
        return CgoResult(
            capability="canon_sync",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=ctx.dry_run,
            gates=gates,
            reason="; ".join(gate.reason for gate in gates if gate.state == "FAIL"),
        )

    path = canon_path(ctx, tenant_id)
    actions = []
    next_actions = []
    if path is None:
        next_actions.append("Definir CANON_REPO_PATH o montar tenants/<id>/canon")
    else:
        files = sum(1 for item in path.rglob("*") if item.is_file())
        actions.append(action("canon", "ok", f"{files} archivos en {path.name}"))
        next_actions.append("Validar cambios contra Claude/Fernando antes de publicar")

    return CgoResult(
        capability="canon_sync",
        tenant_id=tenant_id,
        status=status_from(gates, actions),
        dry_run=ctx.dry_run,
        gates=gates,
        actions=actions,
        next_actions=next_actions,
        data={"canon_path": str(path) if path else None},
    )
