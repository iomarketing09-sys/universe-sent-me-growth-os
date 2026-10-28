"""cross_tenant_report: consolidado de todos los tenants (local)."""

from __future__ import annotations

from modules.cgo.capabilities._common import ads_summary, schedule_path, snapshot_age_days
from modules.cgo.result import CgoContext, CgoResult, action, status_from


def run(ctx: CgoContext, tenant_id: str = None) -> CgoResult:
    tenants = ctx.tenant_ids()
    actions = []
    data = {}

    totals = {"spend": 0.0, "impressions": 0, "clicks": 0, "conversations": 0}
    for current in tenants:
        entry = {"ads": {}, "snapshot_age_days": None, "has_schedule": False}
        try:
            ads = ads_summary(ctx, current)
            entry["ads"] = ads
            for key in totals:
                totals[key] += float(ads.get(key) or 0)
            actions.append(
                action(
                    f"tenant:{current}",
                    "ok",
                    f"gasto={ads.get('spend')}, conversaciones={ads.get('conversations')}",
                )
            )
        except Exception as exc:
            entry["ads"] = {"error": type(exc).__name__}
            actions.append(
                action(f"tenant:{current}", "skip", f"Sin ads locales: {type(exc).__name__}")
            )

        age = snapshot_age_days(ctx.tenant_path(current))
        entry["snapshot_age_days"] = age
        if age is None:
            actions.append(action(f"sync:{current}", "warn", "Sin snapshot del sync."))
        elif age > 3:
            actions.append(action(f"sync:{current}", "warn", f"Snapshot de hace {age} días."))

        entry["has_schedule"] = schedule_path(ctx.tenant_path(current)) is not None
        if not entry["has_schedule"]:
            actions.append(action(f"schedule:{current}", "warn", "Sin calendario."))

        data[current] = entry

    actions.append(
        action(
            "totals",
            "ok",
            f"gasto={round(totals['spend'], 2)}, clics={totals['clicks']}, "
            f"conversaciones={totals['conversations']}",
        )
    )

    return CgoResult(
        capability="cross_tenant_report",
        tenant_id="*",
        status=status_from([], actions),
        dry_run=ctx.dry_run,
        actions=actions,
        data={"tenants": data, "totals": totals},
    )
