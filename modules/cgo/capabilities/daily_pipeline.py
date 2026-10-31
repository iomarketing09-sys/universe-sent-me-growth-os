"""daily_pipeline: estado local del día por tenant (sin red)."""

from __future__ import annotations

from modules.cgo.capabilities._common import (
    ads_summary,
    count_csv_rows,
    schedule_path,
    snapshot_age_days,
)
from modules.cgo.gates import gate_config, gate_track
from modules.cgo.result import (
    CgoContext,
    CgoResult,
    action,
    status_from,
)
from modules.cgo.tracks import PHYSICAL_CRO, tenant_track


def run(ctx: CgoContext, tenant_id: str) -> CgoResult:
    gates = [gate_track(ctx, "daily_pipeline", tenant_id)]
    config_gate, _ = gate_config(ctx, tenant_id)
    gates.append(config_gate)

    tenant_dir = ctx.tenant_path(tenant_id)
    actions = []
    next_actions = []

    age = snapshot_age_days(tenant_dir)
    if age is None:
        actions.append(action("snapshot", "warn", "Sin snapshot de sync legible."))
        next_actions.append("Ejecutar scripts/sync_all.py para el tenant")
    else:
        state = "ok" if age <= 3 else "warn"
        actions.append(action("snapshot", state, f"Snapshot de hace {age} días."))

    path = schedule_path(tenant_dir)
    rows = count_csv_rows(path)
    if path is None:
        actions.append(action("schedule", "warn", "Sin calendario de publicación."))
        next_actions.append("Crear el calendario (meta_import.csv o future_schedule.csv)")
    else:
        actions.append(action("schedule", "ok", f"{rows} slots en {path.name}."))

    published = count_csv_rows(tenant_dir / "publication_log_week2.csv")
    actions.append(action("publication_log", "ok", f"{published} filas publicadas."))

    try:
        ads = ads_summary(ctx, tenant_id)
        actions.append(
            action(
                "ads",
                "ok",
                f"campañas={ads.get('campaigns')}, gasto={ads.get('spend')}, "
                f"conversaciones={ads.get('conversations')}",
            )
        )
        ads_data = ads
    except Exception as exc:
        actions.append(action("ads", "skip", f"Sin datos locales de ads: {type(exc).__name__}"))
        ads_data = {}

    monetization_data = {}
    try:
        from modules.intelligence import MonetizationAgent

        monetization = MonetizationAgent(tenant_id, base_path=str(ctx.base_path)).summary(
            since=ctx.since, until=ctx.until
        )
        if monetization.get("configured"):
            monetization_data = monetization
            threshold = (monetization.get("money") or {}).get("payout_threshold") or {}
            state = "warn" if monetization.get("warnings") else "ok"
            detail = (
                f"pipeline ${float((monetization.get('money') or {}).get('pipeline_net') or 0):,.2f} | "
                f"faltan ${float(threshold.get('remaining') or 0):,.2f} para el umbral"
                if threshold
                else "Ledger de monetización disponible."
            )
            actions.append(
                action("monetization", state, detail)
            )
            next_actions.extend((monetization.get("next_actions") or [])[:2])
        else:
            actions.append(action("monetization", "skip", "Sin datos de monetización."))
    except Exception as exc:
        actions.append(
            action("monetization", "skip", f"Sin ledger legible: {type(exc).__name__}")
        )

    track = tenant_track(tenant_id, ctx.base_path)
    if track == PHYSICAL_CRO:
        actions.append(
            action(
                "reuse",
                "ok",
                "Tenant de producto: la restricción es inventario, no la ventana de 30 días.",
            )
        )

    status = status_from(gates, actions)
    reason = "; ".join(gate.reason for gate in gates if gate.state not in ("PASS", "SKIP"))
    return CgoResult(
        capability="daily_pipeline",
        tenant_id=tenant_id,
        status=status,
        dry_run=ctx.dry_run,
        gates=gates,
        actions=actions,
        next_actions=next_actions,
        reason=reason,
        data={
            "schedule_rows": rows,
            "published_rows": published,
            "snapshot_age_days": age,
            "ads": ads_data,
            "monetization": monetization_data,
        },
    )
