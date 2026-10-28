"""tenant_onboarding: auditoría local de un tenant."""

from __future__ import annotations

from modules.cgo.gates import gate_config, gate_track
from modules.cgo.result import CgoContext, CgoResult, action
from modules.intelligence.agents.tenant_auditor import audit_tenant

STATE_TO_STATUS = {"PASS": "ok", "WARN": "warn", "FAIL": "fail", "SKIP": "skip"}
AUDIT_TO_STATUS = {"READY": "OK", "PARTIAL": "PARTIAL", "BLOCKED": "BLOCKED"}


def run(ctx: CgoContext, tenant_id: str) -> CgoResult:
    gates = [
        gate_track(ctx, "tenant_onboarding", tenant_id),
        gate_config(ctx, tenant_id)[0],
    ]
    audit = audit_tenant(tenant_id, str(ctx.base_path))
    actions = [
        action(
            f"check:{item['id']}",
            STATE_TO_STATUS.get(item["state"], "warn"),
            item["detail"],
        )
        for item in audit.get("checks", [])
    ]

    return CgoResult(
        capability="tenant_onboarding",
        tenant_id=tenant_id,
        status=AUDIT_TO_STATUS.get(audit["status"], "PARTIAL"),
        dry_run=ctx.dry_run,
        gates=gates,
        actions=actions,
        next_actions=list(audit.get("next_actions") or []),
        reason=f"score={audit['score']} track={audit.get('track') or 'unknown'}",
        data=audit,
    )
