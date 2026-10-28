"""weekly_calendar: calendario semanal (solo tenants native_digital)."""

from __future__ import annotations

from modules.cgo.capabilities._common import schedule_path
from modules.cgo.gates import gate_config, gate_track
from modules.cgo.result import CgoContext, CgoResult, GateResult, action, status_from


def run(ctx: CgoContext, tenant_id: str) -> CgoResult:
    gates = [
        gate_track(ctx, "weekly_calendar", tenant_id),
        gate_config(ctx, tenant_id)[0],
    ]
    if any(gate.state == "FAIL" for gate in gates):
        return CgoResult(
            capability="weekly_calendar",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=ctx.dry_run,
            gates=gates,
            reason="; ".join(gate.reason for gate in gates if gate.state == "FAIL"),
        )

    path = schedule_path(ctx.tenant_path(tenant_id))
    if path is None:
        gates.append(
            GateResult(
                "schedule", "NOT_CONFIGURED", "Sin meta_import.csv ni future_schedule.csv."
            )
        )
        return CgoResult(
            capability="weekly_calendar",
            tenant_id=tenant_id,
            status="NOT_CONFIGURED",
            dry_run=ctx.dry_run,
            gates=gates,
            next_actions=["Crear el calendario del tenant"],
            reason="Sin fuente de calendario.",
        )

    from modules.intelligence import build_schedule

    items = build_schedule(
        tenant_id,
        source="meta_import",
        meta_import_path=path,
        future_only=True,
    )
    counts = {}
    for item in items:
        counts[item.type] = counts.get(item.type, 0) + 1

    actions = [
        action("schedule", "ok", f"{len(items)} slots futuros desde {path.name}"),
        action("breakdown", "ok", ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))),
    ]
    next_actions = [] if items else ["Cargar slots futuros en el calendario"]

    return CgoResult(
        capability="weekly_calendar",
        tenant_id=tenant_id,
        status=status_from(gates, actions),
        dry_run=ctx.dry_run,
        gates=gates,
        actions=actions,
        next_actions=next_actions,
        data={"slots": [item.to_dict() for item in items], "counts": counts},
    )
