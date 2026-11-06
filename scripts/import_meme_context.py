#!/usr/bin/env python3
"""Importa meme_text al contexto canónico de publicaciones.

El modo normal copia los chistes dictados en
``metrics/publication_contexts_review.csv``. El modo ``--backfill-missing``
reconstruye publicaciones cuyo último estado de comentarios es
``sin_contexto`` usando el ledger, el CSV de revisión y el nombre del asset.

Ambos modos son idempotentes y escriben únicamente mediante
``record_publication``. Nunca borran ni pisan un chiste ya registrado.

Uso:
    python3 scripts/import_meme_context.py --tenant universe
    python3 scripts/import_meme_context.py --tenant universe --dry-run
    python3 scripts/import_meme_context.py --tenant universe --backfill-missing
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


def _short_id(value: Any) -> str:
    return str(value or "").strip().split("_")[-1]


def _post_id_key(contexts: Dict[str, Any], post_id: str) -> str:
    clean = _short_id(post_id)
    for key, value in contexts.items():
        candidate = str((value or {}).get("publication_id") or key)
        if candidate == post_id or _short_id(candidate) == clean:
            return key
    return ""


def _context_value(contexts: Dict[str, Any], *post_ids: str) -> Dict[str, Any]:
    for post_id in post_ids:
        key = _post_id_key(contexts, post_id)
        value = contexts.get(key) if key else None
        if isinstance(value, dict):
            return value
    return {}


def _csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _review_index(tenant_root: Path) -> Dict[str, Dict[str, str]]:
    path = tenant_root / "metrics" / "publication_contexts_review.csv"
    index: Dict[str, Dict[str, str]] = {}
    for row in _csv_rows(path):
        post_id = str(row.get("id") or "").strip()
        status = str(row.get("status") or "").strip().lower()
        if not post_id or status in {"no_aprobado", "descartado", "discarded"}:
            continue
        index[_short_id(post_id)] = row
    return index


def _ledger_index(tenant_root: Path) -> Dict[str, Dict[str, str]]:
    index: Dict[str, Dict[str, str]] = {}
    for path in sorted(tenant_root.glob("publication_log*.csv")):
        for row in _csv_rows(path):
            short = _short_id(row.get("publication_id"))
            if not short:
                continue
            entry = index.setdefault(short, {})
            publication_id = str(row.get("publication_id") or "").strip()
            if publication_id:
                entry["publication_id"] = publication_id
            asset = str(row.get("asset_filename") or "").strip()
            if asset:
                entry["asset_ref"] = asset
            status = str(row.get("status") or "").strip().lower()
            published_at = str(row.get("published_at") or "").strip()
            if published_at:
                entry["published_at"] = published_at
            caption = str(row.get("piece") or "").strip()
            if caption and (status == "published" or not entry.get("caption")):
                entry["caption"] = caption
    return index


def _asset_text_index(tenant_root: Path) -> Dict[str, str]:
    index: Dict[str, str] = {}
    for row in _csv_rows(tenant_root / "assets_meme_text.csv"):
        filename = str(row.get("filename") or "").strip()
        meme = str(row.get("meme_text") or "").strip()
        if filename and meme:
            index[filename] = meme
    return index


def _derived_asset_fields(
    asset_filename: str, asset_text: Dict[str, str]
) -> Dict[str, str]:
    from modules.intelligence.planner import parse_asset_filename

    filename = Path(str(asset_filename or "")).name
    parsed = parse_asset_filename(filename) if filename else {}
    characters = parsed.get("characters") or []
    meme = str(parsed.get("meme_text") or "").strip()
    if not meme and filename:
        meme = asset_text.get(filename, "")
    return {
        "character": "+".join(str(name) for name in characters),
        "meme_text": meme,
    }


def _last_missing_parents(tenant_root: Path) -> List[str]:
    from modules.communications.comments.log import read_comment_log

    log_path = (
        tenant_root
        / "comment_responses"
        / "facebook_comments"
        / "data"
        / "comments_log.csv"
    )
    latest: Dict[str, Dict[str, str]] = {}
    for row in read_comment_log(log_path):
        comment_id = str(row.get("comment_id") or "").strip()
        if comment_id:
            latest[comment_id] = row

    parents: List[str] = []
    seen: set[str] = set()
    for comment_id, row in latest.items():
        decision = str(row.get("decision") or "").strip()
        publish_status = str(row.get("publish_status") or "").strip()
        if decision != "sin_contexto" and publish_status != "sin_contexto":
            continue
        parent = comment_id.split("_", 1)[0].strip()
        if parent and parent not in seen:
            seen.add(parent)
            parents.append(parent)
    return parents


def pending_rows(tenant: str, base_path: Path) -> List[Dict[str, str]]:
    tenant_root = base_path / "tenants" / tenant
    contexts = _load_contexts(tenant_root / "publication_contexts.json")
    pending: List[Dict[str, str]] = []
    for row in _csv_rows(tenant_root / "metrics" / "publication_contexts_review.csv"):
        post_id = str(row.get("id") or "").strip()
        meme = str(row.get("meme_text") or "").strip()
        status = str(row.get("status") or "").strip().lower()
        if status in {"no_aprobado", "descartado", "discarded"}:
            continue
        if not post_id or not meme:
            continue
        key = _post_id_key(contexts, post_id)
        stored = str((contexts.get(key) or {}).get("meme_text") or "").strip() if key else ""
        if stored:
            continue
        pending.append(row)
    return pending


def backfill_rows(tenant: str, base_path: Path) -> List[Dict[str, str]]:
    """Devuelve los contextos reconstruibles sin escribir en disco."""
    tenant_root = base_path / "tenants" / tenant
    contexts = _load_contexts(tenant_root / "publication_contexts.json")
    reviews = _review_index(tenant_root)
    ledger = _ledger_index(tenant_root)
    asset_text = _asset_text_index(tenant_root)

    rows: List[Dict[str, str]] = []
    for parent in _last_missing_parents(tenant_root):
        review = reviews.get(parent) or {}
        publication = ledger.get(parent) or {}
        full_id = str(
            publication.get("publication_id")
            or review.get("id")
            or parent
        ).strip()
        existing = _context_value(contexts, full_id, parent)
        if str(existing.get("meme_text") or "").strip():
            continue

        asset_ref = str(
            review.get("asset_ref")
            or publication.get("asset_ref")
            or existing.get("asset_ref")
            or ""
        ).strip()
        derived = _derived_asset_fields(asset_ref, asset_text)
        meme = str(review.get("meme_text") or existing.get("meme_text") or "").strip()
        if not meme:
            meme = derived["meme_text"]

        rows.append(
            {
                "id": full_id,
                "publication_id": str(
                    existing.get("publication_id") or full_id
                ).strip(),
                "asset_ref": asset_ref,
                "character": str(
                    review.get("personaje")
                    or existing.get("character")
                    or derived["character"]
                    or ""
                ).strip(),
                "meme_text": meme,
                "copy": str(
                    review.get("copy")
                    or publication.get("caption")
                    or existing.get("caption")
                    or ""
                ).strip(),
                "published_at": str(
                    publication.get("published_at")
                    or existing.get("published_at")
                    or ""
                ).strip(),
            }
        )
    return rows


def _record(tenant_root: Path, row: Dict[str, str]) -> None:
    from modules.intelligence.publication_context import record_publication

    record_publication(
        tenant_root,
        post_id=str(row.get("publication_id") or row.get("id") or ""),
        asset_filename=str(row.get("asset_ref") or ""),
        caption=str(row.get("copy") or ""),
        published_at=str(row.get("published_at") or ""),
        character=str(row.get("character") or ""),
        meme_text=str(row.get("meme_text") or ""),
    )


def import_rows(tenant: str, base_path: Path) -> int:
    tenant_root = base_path / "tenants" / tenant
    contexts = _load_contexts(tenant_root / "publication_contexts.json")
    rows = pending_rows(tenant, base_path)
    for row in rows:
        post_id = str(row.get("id") or "").strip()
        existing = _context_value(contexts, post_id)
        _record(
            tenant_root,
            {
                "publication_id": str(existing.get("publication_id") or post_id),
                "asset_ref": str(
                    row.get("asset_ref") or existing.get("asset_ref") or ""
                ),
                "character": str(row.get("personaje") or ""),
                "meme_text": str(row.get("meme_text") or ""),
                "copy": str(row.get("copy") or existing.get("caption") or ""),
                "published_at": str(existing.get("published_at") or ""),
            },
        )
    return len(rows)


def import_backfill(tenant: str, base_path: Path) -> int:
    tenant_root = base_path / "tenants" / tenant
    rows = [row for row in backfill_rows(tenant, base_path) if row.get("meme_text")]
    for row in rows:
        _record(tenant_root, row)
    return len(rows)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Importa meme_text al contexto")
    parser.add_argument("--tenant", default="universe")
    parser.add_argument("--base-path", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--backfill-missing",
        action="store_true",
        help="Reconstruye publicaciones cuyo último estado es sin_contexto",
    )
    args = parser.parse_args(argv)

    if args.backfill_missing and args.dry_run:
        rows = backfill_rows(args.tenant, args.base_path)
        ready = [row for row in rows if str(row.get("meme_text") or "").strip()]
        unresolved = [row for row in rows if not str(row.get("meme_text") or "").strip()]
        print(f"Reconstruibles: {len(ready)}")
        for row in ready:
            meme = str(row.get("meme_text") or "").strip()
            print(
                f"  {row.get('publication_id')} | "
                f"{row.get('character') or 'Sin personaje'} | {meme[:70]}"
            )
        if unresolved:
            print(f"Sin datos para reconstruir: {len(unresolved)}")
            for row in unresolved:
                print(f"  {row.get('publication_id')} | falta asset o meme_text")
        return 0

    if args.backfill_missing:
        total = import_backfill(args.tenant, args.base_path)
        print(f"Reconstruidos: {total}")
        return 0

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
