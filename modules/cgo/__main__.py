"""CLI del orquestador CGO."""

from __future__ import annotations

import argparse
import json
from typing import List, Optional

from modules.cgo.orchestrator import CgoOrchestrator
from modules.cgo.result import BLOCKED, ERROR, CgoResult


def _print_result(result: CgoResult) -> None:
    mode = "publish" if not result.dry_run else "dry-run"
    print(f"[{result.status}] {result.capability} · {result.tenant_id} · {mode}")
    for gate in result.gates:
        print(f"  gate {gate.name}: {gate.state} {gate.reason}".rstrip())
    for item in result.actions:
        print(f"  - {item['kind']}: {item['status']} · {item['detail']}")
    for item in result.next_actions:
        print(f"  next: {item}")
    if result.reason:
        print(f"  reason: {result.reason}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m modules.cgo",
        description="Orquestador del Growth OS.",
    )
    parser.add_argument("--mode", default="daily_pipeline", help="capacidad a ejecutar")
    parser.add_argument("--tenant", default=None, help="tenant objetivo")
    parser.add_argument("--all", action="store_true", help="todos los tenants")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    parser.add_argument("--strict", action="store_true", help="UNKNOWN bloquea")
    parser.add_argument("--since", default=None, help="Fecha inicial YYYY-MM-DD")
    parser.add_argument("--until", default=None, help="Fecha final YYYY-MM-DD")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="publica de verdad (por defecto solo dry-run)",
    )
    args = parser.parse_args(argv)

    orchestrator = CgoOrchestrator(
        dry_run=not args.publish,
        strict=args.strict,
        publish=args.publish,
        since=args.since,
        until=args.until,
    )
    tenant = None if args.all else args.tenant

    try:
        results = orchestrator.run(args.mode, tenant_id=tenant)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2

    if args.json:
        print(json.dumps([item.to_dict() for item in results], ensure_ascii=False, indent=2))
    else:
        for index, result in enumerate(results):
            if index:
                print()
            _print_result(result)

    return 1 if any(item.status in (BLOCKED, ERROR) for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
