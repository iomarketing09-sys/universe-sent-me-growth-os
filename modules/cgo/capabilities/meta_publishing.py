"""meta_publishing: coordina publicación IG/FB.

Facebook programa en Meta (published=false + scheduled_publish_time), así que no
necesita cron. Instagram no tiene programación nativa: el slot queda en el
calendario y lo publica ``ig_scheduler`` desde el cron.
"""

from __future__ import annotations

from pathlib import Path

from modules.cgo.capabilities._common import count_csv_rows, schedule_path
from modules.cgo.gates import gate_config, gate_token, gate_track
from modules.cgo.result import CgoContext, CgoResult, action, status_from


def _publish_instagram(ctx: CgoContext, tenant_id: str) -> dict:
    if Path.cwd().resolve() != Path(ctx.base_path).resolve():
        return {"error": "Ejecutar desde la raíz del repo para publicar en Instagram."}
    from modules.social import IgScheduler

    scheduler = IgScheduler([tenant_id])
    return scheduler.run_once()


def _publish_facebook(ctx: CgoContext, tenant_id: str) -> dict:
    from modules.social import publish_schedule_from_dryrun

    dryrun = ctx.tenant_path(tenant_id) / "dryrun_output.json"
    if not dryrun.is_file():
        return {"error": "Sin tenants/<id>/dryrun_output.json para Facebook."}
    responses = publish_schedule_from_dryrun(
        dryrun_path=dryrun,
        tenant_root=ctx.tenant_path(tenant_id),
        dry_run=False,
    )
    return {
        "total": len(responses),
        "ok": sum(1 for item in responses if item.success),
        "failed": sum(1 for item in responses if not item.success),
    }


def run(ctx: CgoContext, tenant_id: str) -> CgoResult:
    gates = [
        gate_track(ctx, "meta_publishing", tenant_id),
        gate_config(ctx, tenant_id)[0],
        gate_token(ctx, tenant_id),
    ]
    if any(gate.state == "FAIL" for gate in gates):
        return CgoResult(
            capability="meta_publishing",
            tenant_id=tenant_id,
            status="BLOCKED",
            dry_run=ctx.dry_run,
            gates=gates,
            reason="; ".join(gate.reason for gate in gates if gate.state == "FAIL"),
        )

    path = schedule_path(ctx.tenant_path(tenant_id))
    rows = count_csv_rows(path)
    actions = [
        action(
            "route:facebook",
            "ok",
            "Programación nativa en Meta; no requiere cron.",
            platform="facebook",
            route="native_scheduled",
        ),
        action(
            "route:instagram",
            "ok",
            "Requiere cron: ig_scheduler publica cuando vence el slot.",
            platform="instagram",
            route="queued_for_cron",
        ),
        action("schedule", "ok" if path else "warn", f"{rows} slots en {path.name if path else 'sin calendario'}"),
    ]
    next_actions = []
    if path is None:
        next_actions.append("Crear el calendario antes de publicar")

    artifacts = []
    if ctx.publish and not ctx.dry_run:
        for platform, handler in (
            ("instagram", _publish_instagram),
            ("facebook", _publish_facebook),
        ):
            try:
                result = handler(ctx, tenant_id)
            except Exception as exc:
                actions.append(
                    action(f"publish:{platform}", "warn", f"{type(exc).__name__}: {exc}")
                )
                continue
            if result.get("error"):
                actions.append(action(f"publish:{platform}", "warn", result["error"]))
                continue
            actions.append(
                action(f"publish:{platform}", "ok", str(result))
            )
            if result.get("published"):
                artifacts.append(f"publication_log:{tenant_id}")

    return CgoResult(
        capability="meta_publishing",
        tenant_id=tenant_id,
        status=status_from(gates, actions),
        dry_run=ctx.dry_run or not ctx.publish,
        gates=gates,
        actions=actions,
        artifacts=artifacts,
        next_actions=next_actions,
        data={"schedule_rows": rows, "schedule_file": str(path) if path else None},
    )
