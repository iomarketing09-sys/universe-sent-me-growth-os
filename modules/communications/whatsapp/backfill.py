"""Recupera los ecos que el worker descartó antes del fix.

El worker guardaba cada payload en ``raw_events`` aunque no pudiera interpretarlo.
Este backfill relee esos payloads, reconstruye las filas ``out_app`` y las inserta
con ``INSERT OR IGNORE`` (el índice único por ``message_id`` evita duplicados).

Uso:

    python3 -m modules.communications.whatsapp.backfill flexi            # dry-run
    python3 -m modules.communications.whatsapp.backfill flexi --apply
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from modules.communications.whatsapp import d1, d1_write

TIMEZONE = ZoneInfo("America/Matamoros")
INSERT_SQL = """INSERT OR IGNORE INTO events (
  received_at, direction, wa_ts, local_time, intent, type, text, text_len,
  has_media, is_reply_to_template, contact_hash, contact_last4, contact_name,
  status, message_id,
  referral_source_url, referral_source_id, referral_source_type,
  referral_body, referral_headline, referral_media_type, referral_image_url,
  referral_ctwa_clid, referral_welcome_message_text
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

MEDIA_TYPES = {"image", "audio", "video", "document", "sticker"}


def _hash_contact(wa_id: str) -> tuple[str, str]:
    digest = hashlib.sha256(str(wa_id).encode("utf-8")).hexdigest()
    return digest[:12], str(wa_id)[-4:]


def _text_of(message: Dict[str, Any]) -> str:
    text = message.get("text")
    if isinstance(text, dict) and text.get("body"):
        return str(text["body"])
    if message.get("caption"):
        return str(message["caption"])
    interactive = message.get("interactive") or {}
    return str(
        (interactive.get("button_reply") or {}).get("title")
        or (interactive.get("list_reply") or {}).get("title")
        or ""
    )


def _local_time(timestamp: Any) -> str:
    try:
        seconds = int(timestamp)
    except (TypeError, ValueError):
        return ""
    if seconds <= 0:
        return ""
    return datetime.fromtimestamp(seconds, tz=TIMEZONE).strftime("%Y-%m-%d %H:%M")


def _row(message: Dict[str, Any], received_at: str) -> Optional[tuple]:
    message_id = message.get("id") or ""
    if not message_id:
        return None
    wa_id = message.get("to") or message.get("from") or ""
    if not wa_id:
        return None
    contact_hash, last4 = _hash_contact(wa_id)
    text = _text_of(message)
    message_type = message.get("type") or "desconocido"
    return (
        received_at,
        "out_app",
        message.get("timestamp") or "",
        _local_time(message.get("timestamp")),
        None,
        message_type,
        text,
        len(text),
        1 if message_type in MEDIA_TYPES else 0,
        0,
        contact_hash,
        last4,
        "",
        None,
        message_id,
        "", "", "", "", "", "", "", "", "",
    )


def _candidate_rows(tenant_id: str, base_path: Optional[str]) -> List[tuple]:
    existing = {
        row["message_id"]
        for row in d1.query(
            "SELECT message_id FROM events WHERE direction = 'out_app' AND message_id IS NOT NULL",
            tenant_id=tenant_id,
            base_path=base_path,
        )
    }
    rows = d1.query(
        "SELECT received_at, payload FROM raw_events ORDER BY id",
        tenant_id=tenant_id,
        base_path=base_path,
    )
    out: List[tuple] = []
    seen = set()
    for row in rows:
        try:
            payload = json.loads(row.get("payload") or "{}")
        except (TypeError, ValueError):
            continue
        for entry in payload.get("entry") or []:
            for change in entry.get("changes") or []:
                value = change.get("value") or {}
                for echo in (value.get("smb_message_echoes") or []) + (
                    value.get("message_echoes") or []
                ):
                    message = echo.get("message", echo)
                    message_id = message.get("id") or ""
                    if not message_id or message_id in existing or message_id in seen:
                        continue
                    built = _row(message, row.get("received_at") or "")
                    if built:
                        seen.add(message_id)
                        out.append(built)
    return out


def backfill(
    tenant_id: str = "flexi",
    base_path: Optional[str] = None,
    apply: bool = False,
    limit: int = 0,
) -> Dict[str, Any]:
    rows = _candidate_rows(tenant_id, base_path)
    if limit:
        rows = rows[:limit]

    inserted = 0
    errors = 0
    if apply:
        for row in rows:
            try:
                d1_write.execute(
                    INSERT_SQL, list(row), tenant_id=tenant_id, base_path=base_path
                )
                inserted += 1
            except d1.D1Error:
                errors += 1

    return {
        "tenant_id": tenant_id,
        "applied": apply,
        "recoverable": len(rows),
        "inserted": inserted,
        "errors": errors,
        "sample_ids": [row[14] for row in rows[:5]],
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Backfill de ecos de WhatsApp")
    parser.add_argument("tenant", nargs="?", default="flexi")
    parser.add_argument("--apply", action="store_true", help="Escribe en D1")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    result = backfill(args.tenant, apply=args.apply, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
