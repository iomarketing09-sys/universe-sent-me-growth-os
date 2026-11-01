"""comments_review: revisión local y publicación aprobada de comentarios."""

from __future__ import annotations

from typing import Any, Dict, List

from modules.cgo.gates import gate_config, gate_token, gate_track
from modules.cgo.result import (
    GATE_FAIL,
    GATE_NOT_CONFIGURED,
    CgoContext,
    CgoResult,
    GateResult,
    action,
    status_from,
)


def run(ctx: CgoContext, tenant_id: str) -> CgoResult:
    gates = [
        gate_track(ctx, "comments_review", tenant_id),
        gate_config(ctx, tenant_id)[0],
    ]
    if any(gate.state == GATE_FAIL for gate in gates):
        return CgoResult(
            capability="comments_review",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=ctx.dry_run,
            gates=gates,
            reason="; ".join(gate.reason for gate in gates if gate.state == GATE_FAIL),
        )

    try:
        from modules.communications.comments import inbox_snapshot, publish_approved

        before = inbox_snapshot(tenant_id, base_path=ctx.base_path)
    except Exception as exc:
        gates.append(GateResult("comments", GATE_FAIL, f"No se pudo leer la bandeja: {type(exc).__name__}"))
        return CgoResult(
            capability="comments_review",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=ctx.dry_run,
            gates=gates,
            reason=str(exc),
        )

    approvals = before["approvals"]
    actions: List[Dict[str, Any]] = [
        action(
            "comments:review",
            "ok",
            f"{approvals['total']} revisados: {approvals['approved']} aprobados, "
            f"{approvals['not_approved']} sin aprobar",
        ),
        action(
            "comments:pending",
            "ok",
            f"{approvals['approved_pending']} aprobados pendientes de publicación",
        ),
        action(
            "comments:log",
            "ok",
            f"{before['comments_log']['rows']} filas; "
            f"{before['comments_log']['published']} publicadas, "
            f"{before['comments_log']['already_published']} ya existentes",
        ),
    ]
    if approvals["errors"]:
        actions.append(
            action(
                "comments:errors",
                "warn",
                f"{approvals['errors']} aprobaciones con error; revisar last_error",
            )
        )
    if approvals["approved_without_response"]:
        actions.append(
            action(
                "comments:invalid",
                "warn",
                f"{approvals['approved_without_response']} aprobadas sin texto de respuesta",
            )
        )

    if before["configured"] is False:
        gates.append(
            GateResult(
                "comments",
                GATE_NOT_CONFIGURED,
                f"Sin {before['approvals_file']}; ejecutar la captura del tenant.",
            )
        )
        return CgoResult(
            capability="comments_review",
            tenant_id=tenant_id,
            status="NOT_CONFIGURED",
            dry_run=ctx.dry_run,
            gates=gates,
            actions=actions,
            next_actions=["Ejecutar la captura de comentarios del tenant."],
            data=before,
        )

    should_publish = bool(ctx.publish and not ctx.dry_run)
    if not should_publish:
        return CgoResult(
            capability="comments_review",
            tenant_id=tenant_id,
            status=status_from(gates, actions),
            dry_run=True,
            gates=gates,
            actions=actions,
            artifacts=[before["approvals_file"], before["comments_log_file"]],
            next_actions=[
                "Revisar aprobaciones.json y marcar approved: true solo en respuestas autorizadas.",
                "Publicar con: python3 -m modules.cgo --mode comments_review "
                f"--tenant {tenant_id} --publish",
            ],
            data=before,
        )

    token_gate = gate_token(ctx, tenant_id)
    gates.append(token_gate)
    if token_gate.state == GATE_FAIL:
        return CgoResult(
            capability="comments_review",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=False,
            gates=gates,
            actions=actions,
            reason=token_gate.reason,
            data=before,
        )

    result_code = 0
    if approvals["approved_pending"]:
        result_code = publish_approved(
            before["approvals_file"],
            before["comments_log_file"],
            tenant_id=tenant_id,
            base_path=ctx.base_path,
        )

    after = inbox_snapshot(tenant_id, base_path=ctx.base_path)
    published_now = max(0, after["approvals"]["published"] - before["approvals"]["published"])
    actions.append(
        action(
            "comments:publish",
            "ok" if result_code == 0 else "warn",
            f"{published_now} confirmadas en Meta; "
            f"{after['approvals']['approved_pending']} siguen pendientes",
        )
    )
    if result_code != 0:
        actions.append(action("comments:publish_error", "warn", "La publicación devolvió error."))

    return CgoResult(
        capability="comments_review",
        tenant_id=tenant_id,
        status=status_from(gates, actions),
        dry_run=False,
        gates=gates,
        actions=actions,
        artifacts=[before["approvals_file"], before["comments_log_file"]],
        next_actions=["Revisar last_error en aprobaciones.json si quedaron pendientes."],
        data={"before": before, "after": after, "publish_returncode": result_code},
    )
