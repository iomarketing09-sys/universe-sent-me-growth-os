from __future__ import annotations

import csv
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


COMMENT_LOG_FIELDS = [
    "timestamp",
    "comment_id",
    "comment_text",
    "from_id",
    "created_time",
    "processed",
    "needs_response",
    "response_text",
    "comment_type",
    "apparent_intent",
    "relation_to_meme",
    "decision",
    "risk_level",
    "review_reason",
    "filter_reason",
    "publish_status",
    "published_at",
    "reply_id",
]

LEGACY_FIELDS = COMMENT_LOG_FIELDS[:15]

LEGACY_NINE_COLUMN_FIELDS = [
    "comment_id",
    "comment_text",
    "processed",
    "needs_response",
    "filter_reason",
    "comment_type",
    "decision",
    "response_text",
    "created_time",
]


@dataclass(frozen=True)
class LogMigration:
    path: Path
    rows: int
    legacy_rows: int
    changed: bool


def _cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _is_blank(value: Any) -> bool:
    return value is None or str(value).strip().lower() in {"", "none", "null"}


def normalize_comment_row(row: Mapping[str, Any] | Iterable[Any]) -> dict[str, str]:
    if isinstance(row, Mapping):
        return {field: _cell(row.get(field)) for field in COMMENT_LOG_FIELDS}

    values = list(row)
    if len(values) == len(COMMENT_LOG_FIELDS):
        source_fields = COMMENT_LOG_FIELDS
    elif len(values) == len(LEGACY_FIELDS):
        source_fields = LEGACY_FIELDS
    elif len(values) == len(LEGACY_NINE_COLUMN_FIELDS):
        source_fields = LEGACY_NINE_COLUMN_FIELDS
    else:
        raise ValueError(f"Unsupported comment log width: {len(values)}")

    normalized = {field: "" for field in COMMENT_LOG_FIELDS}
    normalized.update({field: _cell(value) for field, value in zip(source_fields, values)})
    return normalized


def read_comment_log(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))

    if not rows:
        return []

    first = rows[0]
    has_header = first == COMMENT_LOG_FIELDS or first == LEGACY_FIELDS
    data_rows = rows[1:] if has_header else rows

    if has_header:
        source_fields = first
        normalized_rows = []
        for row in data_rows:
            if not row:
                continue
            if len(row) == len(source_fields):
                normalized_rows.append(normalize_comment_row(dict(zip(source_fields, row))))
            else:
                normalized_rows.append(normalize_comment_row(row))
        return normalized_rows

    return [normalize_comment_row(row) for row in data_rows if row]


def write_comment_log(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = [normalize_comment_row(row) for row in rows]

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=COMMENT_LOG_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(normalized)
        temp_path = Path(handle.name)

    os.replace(temp_path, path)


def migrate_comment_log(path: Path) -> LogMigration:
    if not path.exists():
        return LogMigration(path=path, rows=0, legacy_rows=0, changed=False)

    with path.open("r", encoding="utf-8", newline="") as handle:
        raw_rows = list(csv.reader(handle))

    has_canonical_header = bool(raw_rows) and raw_rows[0] == COMMENT_LOG_FIELDS
    data_rows = raw_rows[1:] if raw_rows and raw_rows[0] in (COMMENT_LOG_FIELDS, LEGACY_FIELDS) else raw_rows
    legacy_rows = sum(len(row) != len(COMMENT_LOG_FIELDS) for row in data_rows if row)

    if has_canonical_header and legacy_rows == 0:
        return LogMigration(path=path, rows=len(data_rows), legacy_rows=0, changed=False)

    normalized = read_comment_log(path)
    write_comment_log(path, normalized)
    return LogMigration(path=path, rows=len(normalized), legacy_rows=legacy_rows, changed=True)


def append_comment_log(path: Path, record: Mapping[str, Any]) -> None:
    migrate_comment_log(path)
    row = normalize_comment_row(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COMMENT_LOG_FIELDS)
        writer.writerow(row)


def write_json_atomic(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def merge_approval_payload(
    existing: Mapping[str, Any] | None,
    generated: Iterable[Mapping[str, Any]],
    *,
    generated_at: str | None = None,
    lookback_hours: int | None = None,
) -> dict[str, Any]:
    existing_items = list((existing or {}).get("approvals", []))
    generated_items = [dict(item) for item in generated]
    generated_by_id = {item.get("comment_id"): item for item in generated_items}
    merged: list[dict[str, Any]] = []
    used_ids: set[str] = set()

    for item in existing_items:
        comment_id = str(item.get("comment_id", ""))
        if not comment_id or comment_id in used_ids:
            continue
        replacement = generated_by_id.get(comment_id)
        if replacement is None:
            keep_existing = (
                item.get("discarded")
                or item.get("approved")
                or item.get("published")
                or not _is_blank(item.get("approved_response"))
            )
            if not keep_existing:
                continue
        combined = dict(item)
        if replacement:
            refresh = not combined.get("approved") and not combined.get("published")
            preserve = {
                "approved",
                "published",
                "reply_id",
                "published_at",
                "discarded",
                "discard_reason",
                "first_seen_at",
                "comment_created_at",
            }
            for key, value in replacement.items():
                if key in preserve:
                    continue
                if refresh:
                    if key == "approved_response":
                        combined[key] = value or ""
                    elif not _is_blank(value):
                        combined[key] = value
                elif key not in combined or _is_blank(combined.get(key)):
                    combined[key] = value
        merged.append(combined)
        used_ids.add(comment_id)

    for item in generated_items:
        comment_id = str(item.get("comment_id", ""))
        if not comment_id or comment_id in used_ids:
            continue
        merged.append(dict(item))
        used_ids.add(comment_id)

    pending = sum(
        1
        for item in merged
        if not item.get("published")
        and not item.get("reply_id")
        and not item.get("discarded")
    )
    return {
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "lookback_hours": lookback_hours,
        "total_pending": pending,
        "instructions": "Cambia 'approved: true' en los comentarios que quieras publicar y edita el texto si deseas.",
        "approvals": merged,
    }
