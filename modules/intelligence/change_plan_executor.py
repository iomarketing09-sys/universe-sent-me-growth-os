"""Ejecutor de planes de cambio de Ads.

``campaign_optimizer.build_change_plan`` solo recomienda. Este módulo aplica
las acciones aprobadas, con tres salvaguardas:

1. Dry-run por defecto: sin ``--apply`` no se escribe nada en Meta.
2. Solo se ejecutan acciones de la lista blanca (hoy únicamente ``pause_ad``).
3. Cada acción se verifica leyendo ``status`` y se deja rastro en un JSONL
   append-only del tenant.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

import requests

from modules.config.env import META_ENV_KEYS, load_env_values

SUPPORTED_ACTIONS = {"pause_ad"}
NOOP_ACTIONS = {"keep", "watch"}
DEFAULT_API_VERSION = "v21.0"

Transport = Callable[[str, str, Mapping[str, Any]], Dict[str, Any]]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_transport(base_url: str, access_token: str) -> Transport:
    def send(method: str, path: str, params: Mapping[str, Any]) -> Dict[str, Any]:
        payload = dict(params)
        payload["access_token"] = access_token
        response = requests.request(method, f"{base_url}/{path}", params=payload, data=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    return send


def load_change_plan(plan_path: Path) -> Dict[str, Any]:
    return json.loads(Path(plan_path).read_text(encoding="utf-8"))


def build_plan_from_capture(
    capture_path: Path,
    *,
    base_path: Optional[Path] = None,
    policy: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Reconstruye el plan de cambios a partir de una captura E24/E48/... ya guardada."""
    from modules.intelligence.campaign_optimizer import build_change_plan, load_policy

    root = Path(base_path) if base_path else _project_root()
    payload = json.loads(Path(capture_path).read_text(encoding="utf-8"))
    tenant_id = payload["tenant_id"]
    effective_policy = policy or load_policy(root / "tenants" / tenant_id)
    return build_change_plan(
        payload,
        tenant_id=tenant_id,
        campaign_id=payload["campaign_id"],
        campaign_slug=payload["campaign_slug"],
        campaign_name=payload["campaign_name"],
        elapsed_hours=float(payload.get("scheduled_elapsed_hours") or payload["elapsed_hours"]),
        capture_elapsed_hours=payload.get("elapsed_hours"),
        scheduled_for=payload.get("scheduled_for"),
        checkpoint=payload.get("checkpoint", "LATEST"),
        policy=effective_policy,
    )


@dataclass
class ActionOutcome:
    target_id: str
    target_name: str
    action: str
    result: str
    detail: str = ""


class ChangePlanExecutor:
    """Aplica un plan de cambios con aprobación explícita y verificación posterior."""

    def __init__(
        self,
        *,
        tenant_id: str,
        access_token: Optional[str] = None,
        api_version: str = DEFAULT_API_VERSION,
        dry_run: bool = True,
        base_path: Optional[Path] = None,
        transport: Optional[Transport] = None,
        only: Optional[Sequence[str]] = None,
        now: Optional[datetime] = None,
    ) -> None:
        self.root = Path(base_path) if base_path else _project_root()
        self.tenant_id = tenant_id
        self.dry_run = dry_run
        self.only = {str(item) for item in only} if only else None
        self.base_url = f"https://graph.facebook.com/{api_version}"
        self.access_token = access_token
        self._now = now
        self._transport = transport

    @property
    def transport(self) -> Transport:
        if self._transport is None:
            if not self.access_token:
                raise RuntimeError("Falta access_token para aplicar cambios en Meta.")
            self._transport = _default_transport(self.base_url, self.access_token)
        return self._transport

    def apply(self, plan: Dict[str, Any]) -> List[ActionOutcome]:
        outcomes: List[ActionOutcome] = []
        for item in plan.get("actions") or []:
            target_id = str(item.get("target_id") or "")
            target_name = str(item.get("target_name") or "")
            action = str(item.get("action") or "")

            if not target_id:
                outcomes.append(ActionOutcome(target_id, target_name, action, "invalid", "sin target_id"))
                continue
            if self.only is not None and target_id not in self.only:
                continue
            if action in NOOP_ACTIONS:
                continue
            if action not in SUPPORTED_ACTIONS:
                outcomes.append(
                    ActionOutcome(target_id, target_name, action, "unsupported", "acción no automatizada")
                )
                continue
            if self.dry_run:
                outcomes.append(ActionOutcome(target_id, target_name, action, "would_apply", "dry-run"))
                continue

            outcomes.append(self._pause(target_id, target_name, action))

        if outcomes and not self.dry_run:
            self._audit(plan, outcomes)
        return outcomes

    def _pause(self, target_id: str, target_name: str, action: str) -> ActionOutcome:
        try:
            response = self.transport("POST", target_id, {"status": "PAUSED"})
        except (requests.RequestException, ValueError) as exc:
            return ActionOutcome(target_id, target_name, action, "failed", f"write: {exc}")

        if not response.get("success"):
            return ActionOutcome(target_id, target_name, action, "failed", f"write: {response}")

        try:
            verification = self.transport("GET", target_id, {"fields": "status"})
        except (requests.RequestException, ValueError) as exc:
            return ActionOutcome(target_id, target_name, action, "unverified", f"read: {exc}")

        if verification.get("status") == "PAUSED":
            return ActionOutcome(target_id, target_name, action, "applied")
        return ActionOutcome(
            target_id,
            target_name,
            action,
            "failed",
            f"status tras pausar: {verification.get('status')}",
        )

    def _audit(self, plan: Dict[str, Any], outcomes: List[ActionOutcome]) -> None:
        directory = self.root / "tenants" / self.tenant_id / "ads" / "insights"
        directory.mkdir(parents=True, exist_ok=True)
        timestamp = (self._now or datetime.now(timezone.utc)).isoformat()
        with (directory / "actions.jsonl").open("a", encoding="utf-8") as handle:
            for outcome in outcomes:
                handle.write(
                    json.dumps(
                        {
                            "timestamp": timestamp,
                            "tenant_id": self.tenant_id,
                            "campaign_id": plan.get("campaign_id"),
                            "campaign_slug": plan.get("campaign_slug"),
                            "checkpoint": plan.get("checkpoint"),
                            **asdict(outcome),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )


def _resolve_token(tenant_id: str, base_path: Path) -> Optional[str]:
    values = load_env_values(
        (base_path / ".env", base_path / "tenants" / tenant_id / ".env"),
        keys=META_ENV_KEYS,
    )
    return values.get("META_ACCESS_TOKEN") or values.get("META_PAGE_ACCESS_TOKEN")


def _print_outcomes(outcomes: List[ActionOutcome], dry_run: bool) -> None:
    mode = "dry-run" if dry_run else "aplicado"
    if not outcomes:
        print(f"[{mode}] sin acciones que ejecutar")
        return
    for outcome in outcomes:
        detail = f" · {outcome.detail}" if outcome.detail else ""
        print(f"[{mode}] {outcome.result:11} {outcome.action:14} {outcome.target_name or outcome.target_id}{detail}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Aplica planes de cambio de Ads con verificación")
    parser.add_argument("--tenant", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--plan", type=Path, help="JSON de plan generado por campaign_optimizer")
    source.add_argument("--capture", type=Path, help="JSON de captura E24/E48/E72 para reconstruir el plan")
    parser.add_argument("--apply", action="store_true", help="escribe en Meta (default: dry-run)")
    parser.add_argument("--only", action="append", help="limita a un ad_id; repetible")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = _project_root()
    plan = load_change_plan(args.plan) if args.plan else build_plan_from_capture(args.capture, base_path=root)
    executor = ChangePlanExecutor(
        tenant_id=args.tenant,
        access_token=_resolve_token(args.tenant, root),
        dry_run=not args.apply,
        base_path=root,
        only=args.only,
    )
    outcomes = executor.apply(plan)
    if args.json:
        print(json.dumps([asdict(item) for item in outcomes], ensure_ascii=False, indent=2))
    else:
        _print_outcomes(outcomes, executor.dry_run)
    return 1 if any(item.result in {"failed", "unverified", "invalid"} for item in outcomes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
