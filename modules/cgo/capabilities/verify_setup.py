"""verify_setup: salud del entorno Growth OS (local, sin red)."""

from __future__ import annotations

import importlib
from pathlib import Path

from modules.cgo.gates import _env_key_names
from modules.cgo.result import CgoContext, CgoResult, action, status_from
from modules.cgo.tracks import tenant_ids

MODULES = ("social", "identity", "creative", "communications", "intelligence")


def run(ctx: CgoContext, tenant_id: str = None) -> CgoResult:
    actions = []

    for name in MODULES:
        try:
            importlib.import_module(f"modules.{name}")
            actions.append(action(f"module:{name}", "ok", "import OK"))
        except Exception as exc:
            actions.append(action(f"module:{name}", "fail", f"{type(exc).__name__}: {exc}"))

    tenants = tenant_ids(ctx.base_path)
    if tenants:
        actions.append(action("tenants", "ok", f"{len(tenants)} tenants con config: {', '.join(tenants)}"))
    else:
        actions.append(action("tenants", "fail", "No hay tenants con config.json"))

    if (ctx.base_path / ".env").is_file():
        keys = _env_key_names(ctx.base_path / ".env")
        actions.append(action("env", "ok", f".env presente ({len(keys)} variables, valores no leídos)"))
    else:
        actions.append(action("env", "warn", "No existe .env en la raíz"))

    cron = ctx.base_path / "scripts" / "cron_sync.sh"
    if cron.is_file() and cron.stat().st_mode & 0o111:
        actions.append(action("cron", "ok", "scripts/cron_sync.sh ejecutable"))
    else:
        actions.append(action("cron", "warn", "scripts/cron_sync.sh falta o no es ejecutable"))

    timer = Path("/etc/systemd/system/growth-os-sync.timer")
    if timer.is_file():
        actions.append(action("timer", "ok", "growth-os-sync.timer instalado"))
    else:
        actions.append(action("timer", "skip", "Timer no visible desde este entorno"))

    if any(item["status"] == "fail" for item in actions):
        status = "BLOCKED"
    else:
        status = status_from([], actions)

    return CgoResult(
        capability="verify_setup",
        tenant_id="*",
        status=status,
        dry_run=ctx.dry_run,
        actions=actions,
        data={"tenants": tenants},
    )
