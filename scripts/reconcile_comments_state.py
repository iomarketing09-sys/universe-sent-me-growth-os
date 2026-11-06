#!/usr/bin/env python3
"""Reconcilia la cola maestra de comentarios sin publicar nada.

El comando es dry-run por defecto. Con ``--apply``:

- copia a la maestra los replies ya publicados que viven en un lote cerrado;
- reconstruye ``first_seen_at`` desde ``comments_log.csv``;
- descarta casos concretos con un motivo explícito.

La cola maestra sigue siendo la única fuente de verdad para publicar.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.communications.comments.log import (
    append_comment_log,
    read_comment_log,
    write_json_atomic,
)
from modules.communications.comments.paths import CommentPaths


def _text(value: Any) -> str:
    return str(value or "").strip()


def _load_queue(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("approvals"), list):
        raise ValueError(f"{path} no contiene una lista 'approvals'")
    return payload


def _parse_timestamp(value: Any) -> Optional[datetime]:
    raw = _text(value)
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def _log_indexes(log_path: Path) -> Tuple[Dict[str, Dict[str, str]], Dict[str, str]]:
    published: Dict[str, Dict[str, str]] = {}
    first_seen: Dict[str, str] = {}
    for row in read_comment_log(log_path):
        comment_id = _text(row.get("comment_id"))
        if not comment_id:
            continue
        timestamp = _parse_timestamp(row.get("timestamp"))
        if timestamp is not None:
            existing = _parse_timestamp(first_seen.get(comment_id))
            if existing is None or timestamp < existing:
                first_seen[comment_id] = timestamp.isoformat()

        if row.get("publish_status") not in {"published", "already_published"}:
            continue
        entry = published.setdefault(comment_id, {})
        if _text(row.get("reply_id")):
            entry["reply_id"] = _text(row.get("reply_id"))
        if _text(row.get("response_text")):
            entry["response_text"] = _text(row.get("response_text"))
        published_at = _text(row.get("published_at"))
        if published_at:
            entry["published_at"] = published_at
        elif timestamp is not None:
            entry.setdefault("published_at", timestamp.isoformat())
    return published, first_seen


def _latest_log_rows(log_path: Path) -> Dict[str, Dict[str, str]]:
    latest: Dict[str, Dict[str, str]] = {}
    for row in read_comment_log(log_path):
        comment_id = _text(row.get("comment_id"))
        if comment_id:
            latest[comment_id] = dict(row)
    return latest


def _pending_count(items: Iterable[Dict[str, Any]]) -> int:
    return sum(
        1
        for item in items
        if isinstance(item, dict)
        and item.get("published") is not True
        and not _text(item.get("reply_id"))
        and item.get("discarded") is not True
    )


def _clear_discard(item: Dict[str, Any]) -> None:
    item.pop("discarded", None)
    item.pop("discarded_at", None)
    item.pop("discard_reason", None)


def reconcile_published(
    master: Dict[str, Any],
    sources: Sequence[Path],
    published_index: Dict[str, Dict[str, str]],
    *,
    now: str,
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    items = master["approvals"]
    by_id = {_text(item.get("comment_id")): item for item in items if isinstance(item, dict)}
    changes: List[Dict[str, str]] = []
    skipped: List[Dict[str, str]] = []

    for source in sources:
        payload = _load_queue(source)
        for source_item in payload["approvals"]:
            if not isinstance(source_item, dict):
                continue
            comment_id = _text(source_item.get("comment_id"))
            if not comment_id:
                continue
            if source_item.get("published") is not True and not _text(source_item.get("reply_id")):
                continue

            target = by_id.get(comment_id)
            if target is None:
                target = {"comment_id": comment_id}
                items.append(target)
                by_id[comment_id] = target
            if target.get("published") is True and _text(target.get("reply_id")):
                continue

            log_entry = published_index.get(comment_id, {})
            reply_id = _text(source_item.get("reply_id")) or _text(log_entry.get("reply_id"))
            if not reply_id:
                skipped.append({"comment_id": comment_id, "reason": "sin reply_id verificable"})
                continue

            response = (
                _text(log_entry.get("response_text"))
                or _text(source_item.get("approved_response"))
                or _text(target.get("approved_response"))
            )
            published_at = (
                _text(source_item.get("published_at"))
                or _text(log_entry.get("published_at"))
            )
            target.update(
                {
                    "approved": True,
                    "approved_response": response,
                    "published": True,
                    "published_at": published_at,
                    "reply_id": reply_id,
                    "reconciled_from": source.name,
                    "reconciled_at": now,
                }
            )
            _clear_discard(target)
            changes.append(
                {
                    "comment_id": comment_id,
                    "reply_id": reply_id,
                    "source": source.name,
                }
            )
    return changes, skipped


def backfill_first_seen(
    master: Dict[str, Any],
    first_seen_index: Dict[str, str],
) -> List[str]:
    changed: List[str] = []
    for item in master["approvals"]:
        if not isinstance(item, dict) or _text(item.get("first_seen_at")):
            continue
        comment_id = _text(item.get("comment_id"))
        timestamp = (
            first_seen_index.get(comment_id)
            or _text(item.get("comment_created_at"))
            or _text(item.get("created_time"))
            or _text(item.get("approved_at"))
            or _text(item.get("published_at"))
            or _text(item.get("discarded_at"))
        )
        if not timestamp:
            continue
        item["first_seen_at"] = timestamp
        changed.append(comment_id)
    return changed


def apply_discards(
    master: Dict[str, Any],
    decisions: Iterable[Tuple[str, str]],
    *,
    now: str,
    log_rows: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    by_id = {
        _text(item.get("comment_id")): item
        for item in master["approvals"]
        if isinstance(item, dict)
    }
    changes: List[Dict[str, str]] = []
    errors: List[Dict[str, str]] = []
    for comment_id, reason in decisions:
        comment_id = _text(comment_id)
        reason = _text(reason)
        if not reason:
            errors.append({"comment_id": comment_id, "reason": "falta el motivo"})
            continue
        item = by_id.get(comment_id)
        if item is None:
            source = (log_rows or {}).get(comment_id)
            if not source:
                errors.append(
                    {"comment_id": comment_id, "reason": "no existe en la maestra"}
                )
                continue
            item = {
                "comment_id": comment_id,
                "comment_text": _text(source.get("comment_text")),
                "comment_created_at": _text(source.get("created_time")),
                "first_seen_at": _text(source.get("timestamp")),
                "tombstoned_from": "comments_log",
            }
            master["approvals"].append(item)
            by_id[comment_id] = item
        if item.get("published") is True or _text(item.get("reply_id")):
            errors.append({"comment_id": comment_id, "reason": "ya está publicado"})
            continue
        if item.get("approved") is True:
            errors.append({"comment_id": comment_id, "reason": "ya está aprobado"})
            continue
        item.update(
            {
                "approved": False,
                "discarded": True,
                "discard_reason": reason,
                "discarded_at": now,
            }
        )
        changes.append({"comment_id": comment_id, "reason": reason})
    return changes, errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reconcilia la cola maestra de comentarios (dry-run por defecto)."
    )
    parser.add_argument("--tenant", default="universe")
    parser.add_argument("--base-path", type=Path, default=ROOT)
    parser.add_argument(
        "--source",
        type=Path,
        action="append",
        default=None,
        help="Lote cerrado a reconciliar; se puede repetir.",
    )
    parser.add_argument(
        "--discard",
        nargs=2,
        action="append",
        default=[],
        metavar=("COMMENT_ID", "REASON"),
        help="Descarta un caso con motivo explícito; se puede repetir.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Escribe los cambios; sin este flag solo muestra el plan.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    base_path = Path(args.base_path).resolve()
    paths = CommentPaths.for_tenant(args.tenant, base_path)
    sources = [Path(path) for path in (args.source or [])]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        print("ERROR: no existen: " + ", ".join(missing))
        return 2

    master = _load_queue(paths.approvals_file)
    published_index, first_seen_index = _log_indexes(paths.comments_log_file)
    latest_log_rows = _latest_log_rows(paths.comments_log_file)
    now = datetime.now(timezone.utc).isoformat()

    if sources:
        reconciled, skipped = reconcile_published(
            master, sources, published_index, now=now
        )
    else:
        reconciled, skipped = [], []
    backfilled = backfill_first_seen(master, first_seen_index)
    discarded, discard_errors = apply_discards(
        master, args.discard, now=now, log_rows=latest_log_rows
    )

    print(f"Cola: {paths.approvals_file}")
    print(f"Publicados reconciliados: {len(reconciled)}")
    for change in reconciled:
        print(
            f"  - {change['comment_id']} -> {change['reply_id']} "
            f"({change['source']})"
        )
    print(f"first_seen_at reconstruidos: {len(backfilled)}")
    print(f"Descartes con motivo: {len(discarded)}")
    for change in discarded:
        print(f"  - {change['comment_id']}: {change['reason']}")
    for warning in skipped + discard_errors:
        print(f"  ⚠️ {warning['comment_id']}: {warning['reason']}")

    if not reconciled and not backfilled and not discarded:
        print("Sin cambios.")
        return 0
    if not args.apply:
        print("Dry-run: no se escribió nada. Usa --apply para guardar.")
        return 0

    master["last_reconciled_at"] = now
    master["total_pending"] = _pending_count(master["approvals"])
    write_json_atomic(paths.approvals_file, master)
    by_id = {
        _text(item.get("comment_id")): item
        for item in master["approvals"]
        if isinstance(item, dict)
    }
    for change in discarded:
        item = by_id.get(change["comment_id"], {})
        append_comment_log(
            paths.comments_log_file,
            {
                "timestamp": now,
                "comment_id": change["comment_id"],
                "comment_text": _text(item.get("comment_text")),
                "created_time": _text(item.get("comment_created_at")),
                "decision": "discarded",
                "publish_status": "discarded",
                "filter_reason": change["reason"],
            },
        )
    print("✅ Cola maestra actualizada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
