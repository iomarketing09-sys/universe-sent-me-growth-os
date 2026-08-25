#!/usr/bin/env python3
"""Create a production E0 snapshot from a confirmed publication result.

The general publisher is currently external to this repository. This adapter
is the explicit contract it can call after Meta confirms is_published=true.
It never publishes content and it never fabricates a publication timestamp.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import record_metrics_snapshot as capture  # noqa: E402


def parse_dt(value: str | None) -> datetime | None:
    return capture.parse_dt(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publication-result", type=Path, required=True, help="JSON result emitted by the publisher after verification.")
    parser.add_argument("--ledger", type=Path, default=capture.DEFAULT_LEDGER)
    parser.add_argument("--raw-dir", type=Path, default=capture.DEFAULT_RAW_DIR)
    parser.add_argument("--payload-file", type=Path, help="Optional archived Meta payload wrapper for deterministic replay.")
    parser.add_argument("--captured-at-utc", help="Optional capture timestamp for deterministic replay.")
    parser.add_argument("--run-id", default="")
    args = parser.parse_args()

    event = json.loads(args.publication_result.read_text(encoding="utf-8"))
    meta_post_id = str(event.get("meta_post_id") or event.get("id") or "").strip()
    if not meta_post_id:
        raise SystemExit("publication result must contain meta_post_id or id")
    if event.get("is_published") is not True:
        print(json.dumps({"status": "E0_PENDING", "meta_post_id": meta_post_id, "reason": "is_published is not true; no snapshot written."}, ensure_ascii=False))
        return 0

    published = parse_dt(event.get("published_at_utc") or event.get("created_time"))
    if published is None:
        raise SystemExit("publication result must contain confirmed published_at_utc or created_time")
    captured = parse_dt(args.captured_at_utc) if args.captured_at_utc else datetime.now(timezone.utc)
    assert captured is not None
    rows = capture.read_rows(args.ledger)
    logical_key = f"{meta_post_id}+baseline_e0"
    existing = capture.valid_row_for(rows, logical_key)
    if existing:
        print(json.dumps({"status": "no_op_valid_already_exists", "logical_key": logical_key, "snapshot_id": existing.get("Snapshot_ID", "")}, ensure_ascii=False))
        return 0

    if args.payload_file:
        wrapper = json.loads(args.payload_file.read_text(encoding="utf-8"))
        if isinstance(wrapper, dict) and isinstance(wrapper.get("payload"), dict):
            payload = wrapper["payload"]
            http_status = int(wrapper.get("http_status", 200))
        else:
            payload = wrapper
            http_status = 200
    else:
        token = os.environ.get("META_PAGE_ACCESS_TOKEN")
        if not token:
            raise SystemExit("META_PAGE_ACCESS_TOKEN is required for production E0 capture")
        payload, http_status = capture.fetch_meta_payload(meta_post_id, token)
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    run_id = args.run_id or captured.strftime("%Y%m%dT%H%M%SZ")
    raw_path = args.raw_dir / f"{meta_post_id}_baseline_e0_{captured.strftime('%Y%m%dT%H%M%SZ')}.json"
    raw_record = {
        "captured_at_utc": capture.iso(captured),
        "meta_post_id": meta_post_id,
        "snapshot_type": "baseline_e0",
        "http_status": http_status,
        "publication_event": event,
        "payload": payload,
        "hook_run_id": run_id,
    }
    raw_path.write_text(json.dumps(raw_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    row = capture.make_snapshot_row(
        payload=payload,
        http_status=http_status,
        snapshot_type="baseline_e0",
        meta_post_id=meta_post_id,
        publicacion_id=str(event.get("publicacion_id", "")),
        experiment_id=str(event.get("experiment_id", "")),
        id_pieza=str(event.get("id_pieza", "")),
        cnt=str(event.get("cnt", "")),
        platform=str(event.get("platform", "Facebook")),
        account_id=str(event.get("account_id", capture.DEFAULT_ACCOUNT_ID)),
        meta_photo_id=str(event.get("meta_photo_id", "")),
        reel_id=str(event.get("reel_id", "")),
        published_override=published,
        captured=captured,
        tolerance=600,
        source="Meta_Graph_API",
        raw_path=capture.relative_or_absolute(raw_path),
        existing_rows=rows,
        notes="E0 hook invoked after publisher confirmed is_published=true.",
        run_id=run_id,
    )
    capture.append_row(args.ledger, row)
    print(json.dumps({"status": "recorded", "snapshot_id": row["Snapshot_ID"], "logical_key": row["Logical_Key"], "window_status": row["Window_Status"], "raw_evidence_path": row["Raw_Evidence_Path"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
