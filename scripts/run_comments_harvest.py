#!/usr/bin/env python3
"""Captura comentarios y genera una cola de revisión. Nunca publica."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Harvest de comentarios + cola de revisión (solo lectura de Meta)"
    )
    parser.add_argument("--tenant", default="universe")
    parser.add_argument("--base-path", type=Path, default=ROOT)
    parser.add_argument("--hours", type=int, default=48)
    parser.add_argument("--max-comments", type=int, default=100)
    parser.add_argument(
        "--skip-harvest",
        action="store_true",
        help="No consulta Meta; solo reconstruye la cola desde aprobaciones.json",
    )
    args = parser.parse_args(argv)
    base_path = Path(args.base_path).resolve()

    if not args.skip_harvest:
        harvest = base_path / "tenants" / args.tenant / "harvest_comments.py"
        if not harvest.is_file():
            print(f"ERROR: no existe {harvest}")
            return 2
        command = [
            sys.executable,
            str(harvest),
            "--agent",
            "--hours",
            str(max(1, args.hours)),
            "--max-comments",
            str(max(1, args.max_comments)),
        ]
        try:
            result = subprocess.run(
                command,
                cwd=str(base_path),
                text=True,
                timeout=900,
            )
        except subprocess.TimeoutExpired:
            print("ERROR: el harvest excedió 900s")
            return 1
        if result.returncode != 0:
            print(f"ERROR: el harvest terminó con código {result.returncode}")
            return result.returncode

    from modules.communications.comments.review_queue import build_new_proposals_queue

    review = build_new_proposals_queue(args.tenant, base_path=base_path)
    print(
        "Revisión: "
        f"{review['items']} propuestas nuevas"
        f" · {review['without_response']} sin respuesta"
    )
    print(f"Cola: {review['queue_file']}")
    print(f"Markdown: {review['markdown']}")
    print(f"CSV: {review['csv']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
