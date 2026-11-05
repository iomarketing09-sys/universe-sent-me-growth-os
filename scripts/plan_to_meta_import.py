#!/usr/bin/env python3
"""Convierte un plan de contenido en el calendario ``meta_import.csv``.

El plan es una tabla con las mismas columnas del calendario. El script valida
fecha, hora, tipo y asset, y mezcla por (fecha, hora) para que se pueda volver
a correr sin duplicar slots.

Uso:
    python3 scripts/plan_to_meta_import.py --tenant universe --plan plan.csv
    python3 scripts/plan_to_meta_import.py --tenant universe --plan plan.csv --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.intelligence.planner import META_IMPORT_FIELDS, Planner, ScheduleItem


def _repair_header(header: List[str]) -> List[str]:
    """Recompone ``Time (HH:MM, 24h)`` si se escribió sin comillas."""
    repaired: List[str] = []
    index = 0
    while index < len(header):
        current = header[index].strip()
        following = header[index + 1].strip() if index + 1 < len(header) else ""
        if current.startswith("Time (HH:MM") and "24h" in following:
            repaired.append("Time (HH:MM, 24h)")
            index += 2
            continue
        repaired.append(current)
        index += 1
    return repaired


def load_plan(path: Path, tenant_id: str) -> List[ScheduleItem]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = _repair_header(next(reader, []))
        rows = [dict(zip(header, row)) for row in reader if any(cell.strip() for cell in row)]
    optional = {"Pilar", "Hypothesis ID", "Experiment ID"}
    missing = [
        field
        for field in META_IMPORT_FIELDS
        if rows and field not in rows[0] and field not in optional
    ]
    if missing:
        raise ValueError(f"Faltan columnas en el plan: {', '.join(missing)}")
    return [ScheduleItem.from_meta_import_row(row, tenant_id) for row in rows]


def tenant_timezone(tenant_dir: Path) -> str:
    config_path = tenant_dir / "config.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "America/Matamoros"
    return str(config.get("timezone") or "America/Matamoros")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Plan de contenido -> meta_import.csv")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--base-path", type=Path, default=ROOT)
    parser.add_argument("--replace", action="store_true", help="Reescribe el calendario completo")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    tenant_dir = Path(args.base_path).resolve() / "tenants" / args.tenant
    target = tenant_dir / "meta_import.csv"
    if not tenant_dir.is_dir():
        print(f"ERROR: no existe el tenant {args.tenant}")
        return 2

    try:
        items = load_plan(args.plan, args.tenant)
        planner = Planner(args.tenant)
        if args.dry_run:
            rows, errors = planner.validate_items(
                items, timezone_name=tenant_timezone(tenant_dir)
            )
            for item in items:
                print(f"  {item.date} {item.time} {item.type:5} {item.asset_filename or '-'}")
            if errors:
                for error in errors:
                    print(f"  PENDIENTE: {error}")
                print(f"Slots válidos: {len(rows)} de {len(items)} (destino {target})")
                return 1
            print(f"Slots válidos en el plan: {len(rows)} (destino {target})")
            return 0
        summary = planner.write_meta_import(
            items,
            target,
            timezone_name=tenant_timezone(tenant_dir),
            merge=not args.replace,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(
        f"Escritos {summary['written']} slots "
        f"({summary['replaced']} reemplazados) · total {summary['total']}"
    )
    print(f"Calendario: {summary['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
