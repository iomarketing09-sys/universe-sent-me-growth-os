"""monetization_report: estado local de monetización (sin red)."""

from __future__ import annotations

from typing import Any, Dict, List

from modules.cgo.gates import gate_config, gate_track
from modules.cgo.result import (
    GATE_FAIL,
    GATE_NOT_CONFIGURED,
    CgoContext,
    CgoResult,
    GateResult,
    action,
    status_from,
)


def _money(value: Any) -> str:
    return f"${float(value or 0):,.2f}"


def run(ctx: CgoContext, tenant_id: str) -> CgoResult:
    gates = [
        gate_track(ctx, "monetization_report", tenant_id),
        gate_config(ctx, tenant_id)[0],
    ]

    try:
        from modules.intelligence import MonetizationAgent

        agent = MonetizationAgent(tenant_id, base_path=str(ctx.base_path))
        summary = agent.summary(since=ctx.since, until=ctx.until)
    except Exception as exc:
        gates.append(
            GateResult(
                "monetization",
                GATE_FAIL,
                f"No se pudo leer el ledger: {type(exc).__name__}",
            )
        )
        return CgoResult(
            capability="monetization_report",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=ctx.dry_run,
            gates=gates,
            reason=str(exc),
        )

    if not summary.get("configured"):
        gates.append(
            GateResult("monetization", GATE_NOT_CONFIGURED, "Sin periodos, payouts ni umbral configurado.")
        )
        return CgoResult(
            capability="monetization_report",
            tenant_id=tenant_id,
            status="NOT_CONFIGURED",
            dry_run=ctx.dry_run,
            gates=gates,
            next_actions=["Configurar monetization.payout_threshold o registrar un periodo."],
            data=summary,
        )

    actions: List[Dict[str, Any]] = []
    money = summary.get("money") or {}
    latest = summary.get("latest_period")
    if latest:
        actions.append(
            action(
                "monetization:period",
                "ok",
                f"{latest['period_start']} -> {latest['period_end']} | {latest['status']} | "
                f"estimado {_money(latest.get('estimated_net'))} | aprobado {_money(latest.get('approved_net'))}",
            )
        )

    threshold = money.get("payout_threshold")
    if threshold:
        actions.append(
            action(
                "monetization:threshold",
                "ok",
                f"saldo {_money(threshold.get('current_balance'))} {threshold['currency']} | "
                f"faltan {_money(threshold.get('remaining'))}",
            )
        )

    actions.append(
        action(
            "monetization:money",
            "ok",
            f"pipeline {_money(money.get('pipeline_net'))} | pagado {_money(money.get('paid_net'))} | "
            f"reconocido {_money(money.get('recognized_net'))}",
        )
    )
    if summary.get("warnings"):
        actions.append(
            action(
                "monetization:quality",
                "warn",
                f"{len(summary['warnings'])} avisos: " + "; ".join(summary["warnings"][:3]),
            )
        )

    artifacts = [f"{key}:{value}" for key, value in (summary.get("paths") or {}).items()]
    return CgoResult(
        capability="monetization_report",
        tenant_id=tenant_id,
        status=status_from(gates, actions),
        dry_run=ctx.dry_run,
        gates=gates,
        actions=actions,
        artifacts=artifacts,
        next_actions=summary.get("next_actions") or [],
        data=summary,
    )
