#!/usr/bin/env python3
"""Propone el plan de la semana con inventario disponible y ranking histórico.

No publica. Con ``--write`` deja la propuesta en ``plan_contenido.csv`` para
revisión; después se carga con ``plan_to_meta_import.py``.

Uso:
    python3 scripts/propose_week.py --tenant universe --start 2026-11-05 --days 3
    python3 scripts/propose_week.py --tenant universe --start 2026-11-05 --days 3 --write
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.intelligence.planner import SLOT_HOURS, Planner, propose_week


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Propuesta de calendario semanal")
    parser.add_argument("--tenant", default="universe")
    parser.add_argument(
        "--start",
        default=(date.today() + timedelta(days=1)).isoformat(),
        help="Primer día (YYYY-MM-DD). Por defecto mañana.",
    )
    parser.add_argument("--days", type=int, default=3)
    parser.add_argument("--per-day", type=int, default=1)
    parser.add_argument("--hour", default=None, help="Forzar hora (HH:MM)")
    parser.add_argument(
        "--hours",
        default=",".join(SLOT_HOURS),
        help="Parrilla del día separada por comas. Vacío = un solo slot a la mejor hora.",
    )
    parser.add_argument(
        "--reuse-per-day", type=int, default=None, help="Reuse por día (2-3)"
    )
    parser.add_argument("--assets-dir", type=Path, default=None)
    parser.add_argument("--base-path", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true", help="Escribe plan_contenido.csv")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    proposal = propose_week(
        args.tenant,
        start_date=args.start,
        days=args.days,
        hour=args.hour,
        per_day=args.per_day,
        hours=[value.strip() for value in args.hours.split(",") if value.strip()] or None,
        reuse_per_day=args.reuse_per_day,
        assets_dir=args.assets_dir,
        base_path=args.base_path,
    )
    items = proposal["items"]

    if args.json:
        print(
            json.dumps(
                {
                    **{key: value for key, value in proposal.items() if key != "items"},
                    "items": [item.to_dict() for item in items],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(
        f"{args.tenant} · {len(items)} slots propuestos"
        f" · {proposal['assets_available']} nuevos, {proposal.get('reuse_available', 0)} reuse"
    )
    for note in proposal["notes"]:
        print(f"  nota: {note}")
    for item in items:
        character = item.hashtags.split()[0] if item.hashtags else "-"
        print(
            f"  {item.date} {item.time}  {item.origin:6} {character:<14}"
            f" {item.pillar[:20]:<21} {item.asset_filename[:52]}"
        )

    if args.write:
        target = Path(args.base_path).resolve() / "tenants" / args.tenant / "plan_contenido.csv"
        summary = Planner(args.tenant).write_meta_import(items, target, merge=False)
        print(f"Escrito: {summary['path']} ({summary['total']} slots)")
    else:
        print("Sin escribir. Agrega --write para dejar la propuesta en plan_contenido.csv.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
