#!/usr/bin/env python3
"""Importa los meme_text dictados en el CSV de revisión al contexto canónico.

Idempotente: solo escribe filas con `meme_text` cuando el JSON todavía no lo
tiene. Nunca borra ni pisa un chiste ya registrado.

Uso:
    python3 scripts/import_meme_context.py --tenant universe
    python3 scripts/import_meme_context.py --tenant universe --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_contexts(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _post_id_key(contexts: Dict[str, Any], post_id: str) -> str:
    clean = post_id.split("_")[-1]
    for key, value in contexts.items():
        candidate = str((value or {}).get("publication_id") or key)
        if candidate == post_id or candidate.split("_")[-1] == clean:
            return key
    return ""


def pending_rows(
    tenant: str, base_path: Path
) -> List[Dict[str, str]]:
    csv_path = base_path / "tenants" / tenant / "metrics" / "publication_contexts_review.csv"
    json_path = base_path / "tenants" / tenant / "publication_contexts.json"
    contexts = _load_contexts(json_path)
    if not csv_path.is_file():
        return []
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8-sig")))
    pending: List[Dict[str, str]] = []
    for row in rows:
        post_id = str(row.get("id") or "").strip()
        meme = str(row.get("meme_text") or "").strip()
        status = str(row.get("status") or "").strip().lower()
        if status in {"no_aprobado", "descartado", "discarded"}:
            continue
        if not post_id or not meme:
            continue
        key = _post_id_key(contexts, post_id)
        if key and str((contexts.get(key) or {}).get("meme_text") or "").strip():
            continue
        pending.append(row)
    return pending


def import_rows(tenant: str, base_path: Path) -> int:
    sys.path.insert(0, str(base_path / "tenants" / tenant))
    import context_manager

    json_path = base_path / "tenants" / tenant / "publication_contexts.json"
    contexts = _load_contexts(json_path)
    rows = pending_rows(tenant, base_path)
    for row in rows:
        post_id = str(row.get("id") or "").strip()
        key = _post_id_key(contexts, post_id)
        previous = contexts.get(key) or {}
        character = str(row.get("personaje") or "").strip() or "Universe"
        context_manager.record_publication(
            post_id=str(previous.get("publication_id") or post_id),
            asset_name=str(row.get("asset_ref") or previous.get("asset_ref") or ""),
            caption=str(row.get("copy") or previous.get("caption") or ""),
            published_at=str(previous.get("published_at") or ""),
            visual_info={
                "character": character,
                "meme_text": str(row.get("meme_text") or "").strip(),
                "visual_context": str(previous.get("visual_context") or ""),
            },
        )
    return len(rows)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Importa meme_text del CSV al contexto")
    parser.add_argument("--tenant", default="universe")
    parser.add_argument("--base-path", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.dry_run:
        rows = pending_rows(args.tenant, args.base_path)
        print(f"Pendientes de importar: {len(rows)}")
        for row in rows:
            print(f"  {row.get('id')} | {str(row.get('meme_text'))[:60]}")
        return 0

    total = import_rows(args.tenant, args.base_path)
    print(f"Importados: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
