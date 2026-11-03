#!/usr/bin/env python3
"""Ciclo de métricas de intelligence para todos los tenants conectados."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.intelligence.metrics_snapshot import (  # noqa: E402
    run_all_tenants_cycle,
    run_capture_cycle,
)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Ciclo de métricas de intelligence")
    parser.add_argument("--tenant", action="append", help="tenant específico (repetible)")
    parser.add_argument("--all-tenants", action="store_true", help="todos los tenants conectados")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    os.chdir(ROOT)
    if args.tenant:
        results: Dict[str, Dict[str, object]] = {}
        for tenant_id in args.tenant:
            try:
                results[tenant_id] = run_capture_cycle(tenant_id)
            except Exception as exc:  # noqa: BLE001
                results[tenant_id] = {"error": f"{type(exc).__name__}: {exc}"}
    else:
        results = run_all_tenants_cycle(ROOT)
    failed = [tenant for tenant, result in results.items() if result.get("error")]

    if args.json:
        print(json.dumps({"tenants": results, "failed": failed}, ensure_ascii=False))
    else:
        for tenant_id, result in results.items():
            print(f"[intelligence] {tenant_id}: {result}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
