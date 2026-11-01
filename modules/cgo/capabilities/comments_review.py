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

        before = inbox_snapshot(
            tenant_id,
            base_path=ctx.base_path,
            approvals_file=ctx.comments_approvals_file,
        )
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
    is_review_view = before.get("kind") == "review_queue"
    review_source = before.get("source") or before["approvals_file"]
    actions: List[Dict[str, Any]] = [
        action(
            "comments:review",
            "ok",
            f"{approvals['total']} revisados: {approvals['approved']} aprobados, "
            f"{approvals['review_pending']} por revisar, "
            f"{approvals['discarded']} descartados",
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
    if approvals["review_pending"]:
        actions.append(
            action(
                "comments:review_pending",
                "ok",
                f"{approvals['review_pending']} propuestas nuevas por revisar",
            )
        )
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
    if should_publish and is_review_view:
        gates.append(
            GateResult(
                "comments",
                GATE_FAIL,
                "La vista de revisión es de solo lectura; aprueba en la cola fuente.",
            )
        )
        return CgoResult(
            capability="comments_review",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=False,
            gates=gates,
            actions=actions,
            reason="La vista de revisión es de solo lectura y no se publica directamente.",
            data=before,
        )
    if not should_publish:
        review_target = review_source if is_review_view else before["approvals_file"]
        publish_command = (
            f"python3 -m modules.cgo --mode comments_review --tenant {tenant_id} --publish"
        )
        if ctx.comments_approvals_file is not None:
            publish_command += f" --comments-approvals-file {review_target}"
        return CgoResult(
            capability="comments_review",
            tenant_id=tenant_id,
            status=status_from(gates, actions),
            dry_run=True,
            gates=gates,
            actions=actions,
            artifacts=[before["approvals_file"], before["comments_log_file"]],
            next_actions=[
                f"Revisar {review_target} y marcar approved: true solo en respuestas autorizadas.",
                f"Publicar con: {publish_command}",
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
            batch_size=ctx.comments_batch_size,
            batch_pause_seconds=ctx.comments_batch_pause_seconds,
        )

    after = inbox_snapshot(
        tenant_id,
        base_path=ctx.base_path,
        approvals_file=ctx.comments_approvals_file,
    )
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
        next_actions=[
            f"Revisar last_error en {before['approvals_file']} si quedaron pendientes."
        ],
        data={"before": before, "after": after, "publish_returncode": result_code},
    )
