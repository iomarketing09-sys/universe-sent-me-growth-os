#!/usr/bin/env python3
"""Ranking histórico de contenido para decidir qué publicar.

Lee los snapshots capturados, el personaje del contexto y la hora del log de
publicaciones. No escribe nada.

Uso:
    python3 scripts/rank_content.py --tenant universe
    python3 scripts/rank_content.py --tenant universe --days 60 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.intelligence.historical_baseline import rank_publications


def _table(title: str, rows: List[dict], key: str) -> None:
    print(f"\n{title}")
    print(f"  {'':<22} {'posts':>5} {'prom':>8} {'mediana':>8} {'mejor':>7}")
    for row in rows:
        label = str(row.get(key) or "-")[:22]
        print(
            f"  {label:<22} {row['publications']:>5} {row['avg_score']:>8}"
            f" {row['median_score']:>8} {row['best']:>7}"
        )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Ranking histórico de contenido")
    parser.add_argument("--tenant", default="universe")
    parser.add_argument("--days", type=int, default=120)
    parser.add_argument("--window", default=None, help="Forzar ventana (E24, E72, ...)")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = rank_publications(
        args.tenant, days=args.days, window=args.window
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(
        f"{args.tenant} · {report['publications']} publicaciones medidas"
        f" · ventana {report['window']} · últimos {report['days']} días"
    )
    for note in report["notes"]:
        print(f"  nota: {note}")
    _table("Por personaje", report["by_character"], "character")
    _table("Por banda horaria", report["by_hour_band"], "hour_band")

    print("\nMejores publicaciones (interacciones + compartidos + guardados)")
    for item in report["top"][: args.top]:
        print(
            f"  {item['score']:>6}  {item['character'][:18]:<18}"
            f" {item['hour'] or '-':>5}  {item['window']:<16} {item['publication_id']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
