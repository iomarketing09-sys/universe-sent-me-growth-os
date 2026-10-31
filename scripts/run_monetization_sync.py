#!/usr/bin/env python3
"""Sincroniza evidencia de monetización y actualiza el reporte local.

Por defecto captura los ingresos de contenido de Meta para el periodo indicado,
importa las señales locales y devuelve el resumen del Monetization Agent. No
aprueba periodos, no registra payouts y no escribe en Meta.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.intelligence import MonetizationAgent


def _load_env(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("'\"")
    return values


def _child_env(base_path: Path, tenant_id: str) -> Dict[str, str]:
    env = os.environ.copy()
    env.update(_load_env(base_path / ".env"))
    env.update(_load_env(base_path / "tenants" / tenant_id / ".env"))
    return env


def _run_script(script: Path, args: List[str], env: Dict[str, str]) -> Dict[str, Any]:
    if not script.is_file():
        return {"status": "not_configured", "script": str(script)}
    try:
        completed = subprocess.run(
            [sys.executable, str(script), *args],
            cwd=str(script.parent),
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "status": "error",
            "script": str(script),
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {
        "status": "ok" if completed.returncode == 0 else "error",
        "script": str(script),
        "returncode": completed.returncode,
        "stdout": (completed.stdout or "").strip()[-2000:],
        "stderr": (completed.stderr or "").strip()[-2000:],
    }


def eligible_tenants(base_path: Path) -> List[str]:
    tenants_dir = base_path / "tenants"
    if not tenants_dir.is_dir():
        return []
    result = []
    for tenant_dir in sorted(tenants_dir.iterdir()):
        config_path = tenant_dir / "config.json"
        if not config_path.is_file():
            continue
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (
            config.get("monetization")
            or (tenant_dir / "metrics" / "monetization").is_dir()
            or (tenant_dir / "data" / "monetization").is_dir()
        ):
            result.append(tenant_dir.name)
    return result


def sync_tenant(
    tenant_id: str,
    *,
    base_path: Path,
    since: str,
    until: str,
    fetch: bool = True,
    fetch_signals: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    tenant_dir = base_path / "tenants" / tenant_id
    if not (tenant_dir / "config.json").is_file():
        return {"tenant_id": tenant_id, "status": "not_configured", "error": "Falta config.json"}

    fetches: List[Dict[str, Any]] = []
    imports: Dict[str, Any] = {}
    if fetch:
        env = _child_env(base_path, tenant_id)
        fetches.append(
            _run_script(
                tenant_dir / "metrics" / "fetch_meta_content_earnings.py",
                ["--since", since, "--until", until],
                env,
            )
        )
        if fetch_signals:
            fetches.append(
                _run_script(
                    tenant_dir / "metrics" / "fetch_meta_monetization.py",
                    [],
                    env,
                )
            )

    agent = MonetizationAgent(tenant_id, base_path=str(base_path))
    if not dry_run:
        imports = agent.import_local_signals()

    summary = agent.summary(since=since, until=until)
    errors = [item for item in fetches if item.get("status") == "error"]
    errors.extend(imports.get("errors") or [])
    if errors:
        status = "error"
    elif summary.get("warnings"):
        status = "partial"
    else:
        status = "ok"
    return {
        "tenant_id": tenant_id,
        "status": status,
        "period": {"since": since, "until": until},
        "fetches": fetches,
        "imports": imports,
        "summary": summary,
        "errors": errors,
    }


def main(argv: Optional[List[str]] = None) -> int:
    today = date.today()
    parser = argparse.ArgumentParser(description="Sync de Monetization Agent")
    parser.add_argument("--tenant", default=None)
    parser.add_argument("--all", action="store_true", help="Todos los tenants con monetización")
    parser.add_argument("--since", default=today.replace(day=1).isoformat())
    parser.add_argument("--until", default=today.isoformat())
    parser.add_argument("--no-fetch", action="store_true", help="No llama a Meta; solo importa y reporta")
    parser.add_argument(
        "--fetch-signals",
        action="store_true",
        help="También ejecuta el extractor legacy de señales/bonus",
    )
    parser.add_argument("--dry-run", action="store_true", help="No captura ni escribe; solo lee")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--base-path", default=str(ROOT))
    args = parser.parse_args(argv)

    base_path = Path(args.base_path)
    if args.tenant:
        tenants = [args.tenant]
    else:
        tenants = eligible_tenants(base_path)
    if not tenants:
        print("No hay tenants con monetización configurada.", file=sys.stderr)
        return 1

    results = [
        sync_tenant(
            tenant_id,
            base_path=base_path,
            since=args.since,
            until=args.until,
            fetch=not args.no_fetch and not args.dry_run,
            fetch_signals=args.fetch_signals,
            dry_run=args.dry_run,
        )
        for tenant_id in tenants
    ]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            summary = result.get("summary") or {}
            threshold = (summary.get("money") or {}).get("payout_threshold") or {}
            print(
                f"[{result['status']}] {result['tenant_id']} | "
                f"pipeline ${float((summary.get('money') or {}).get('pipeline_net') or 0):,.2f} | "
                f"faltan ${float(threshold.get('remaining') or 0):,.2f}"
            )
            for error in result.get("errors") or []:
                print(f"  error: {error}", file=sys.stderr)

    return 1 if any(item["status"] == "error" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
