#!/usr/bin/env python3
"""Completa contextos faltantes usando el importador canónico."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.import_meme_context import backfill_rows, import_backfill  # noqa: E402


def main() -> int:
    rows = backfill_rows("universe", ROOT)
    ready = [row for row in rows if str(row.get("meme_text") or "").strip()]
    unresolved = [row for row in rows if not str(row.get("meme_text") or "").strip()]
    imported = import_backfill("universe", ROOT)
    print(f"Contextos reconstruidos: {imported}")
    for row in unresolved:
        print(
            "Pendiente de dictado: "
            f"{row.get('publication_id')} (sin asset o meme_text)"
        )
    return 0 if imported == len(ready) else 1


if __name__ == "__main__":
    raise SystemExit(main())
