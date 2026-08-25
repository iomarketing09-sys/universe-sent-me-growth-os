#!/usr/bin/env python3
"""Record Meta metric snapshots in the append-only USM ledger.

This module is intentionally conservative: it never writes 24h/72h values to
Publication_Log or ExperimentLog, and it never treats a lifetime observation as
a contractual time window. It can read a saved API payload for deterministic
replay or query one Meta post using META_PAGE_ACCESS_TOKEN.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

REPO = Path(os.environ.get("USM_GROWTH_OS_REPO", "/home/ubuntu/universe-sent-me-growth-os"))
DEFAULT_LEDGER = REPO / "Operations/Research/Metrics_Snapshot_Log.csv"
DEFAULT_RAW_DIR = REPO / "Operations/Research/Metrics_Raw"
GRAPH_BASE = "https://graph.facebook.com/v26.0"
DEFAULT_ACCOUNT_ID = "1036844829507460"
LOCAL_TZ = ZoneInfo("America/Matamoros")
LEDGER_FIELDS = [
    "Snapshot_ID",
    "Logical_Key",
    "Publicacion_ID",
    "Experiment_ID",
    "ID_Pieza",
    "CNT",
    "Plataforma",
    "Cuenta_ID",
    "Meta_Post_ID",
    "Meta_Photo_ID",
    "Reel_ID",
    "Published_At_UTC",
    "Published_At_Local",
    "Snapshot_Type",
    "Target_At_UTC",
    "Captured_At_UTC",
    "Age_Seconds",
    "Tolerance_Seconds",
    "Window_Status",
    "Reactions",
    "Comments",
    "Shares",
    "Lifetime_Interactions",
    "Delta_From_E0",
    "Source",
    "HTTP_Status",
    "Raw_Evidence_Path",
    "Idempotency_Key",
    "Anomaly_Code",
    "Notes",
]


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    if len(text) >= 5 and text[-5] in "+-" and text[-3] != ":":
        text = text[:-2] + ":" + text[-2:]
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso(dt: datetime | None) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if dt else ""


def as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return None


def counter_from_summary(value: Any) -> int | None:
    if not isinstance(value, dict):
        return None
    summary = value.get("summary")
    if isinstance(summary, dict):
        count = as_int(summary.get("total_count"))
        if count is not None:
            return count
    return as_int(value.get("count"))


def extract_counters(payload: dict[str, Any]) -> dict[str, int | None]:
    reactions = counter_from_summary(payload.get("reactions"))
    comments = counter_from_summary(payload.get("comments"))
    shares_obj = payload.get("shares")
    shares = as_int(shares_obj.get("count")) if isinstance(shares_obj, dict) else as_int(shares_obj)
    return {"reactions": reactions, "comments": comments, "shares": shares}


def ensure_ledger(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", encoding="utf-8", newline="") as handle:
            csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n").writeheader()
        return
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    if header != LEDGER_FIELDS:
        raise RuntimeError("Metrics_Snapshot_Log.csv header does not match the approved schema")


def read_rows(path: Path) -> list[dict[str, str]]:
    ensure_ledger(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def append_row(path: Path, row: dict[str, str]) -> None:
    ensure_ledger(path)
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=LEDGER_FIELDS, lineterminator="\n").writerow(row)


def default_tolerance(snapshot_type: str) -> int:
    return 600 if snapshot_type == "baseline_e0" else 3600


def target_for(snapshot_type: str, published: datetime) -> datetime | None:
    if snapshot_type == "baseline_e0":
        return published
    if snapshot_type == "snapshot_24h":
        return published + timedelta(hours=24)
    if snapshot_type == "snapshot_72h":
        return published + timedelta(hours=72)
    return None


def classify_window(
    snapshot_type: str,
    published: datetime,
    captured: datetime,
    tolerance: int,
    counters: dict[str, int | None],
) -> tuple[str, str, str]:
    if any(value is None for value in counters.values()):
        return "Anomaly", "missing_counter", "At least one contractual counter was absent; row is not canonical."
    target = target_for(snapshot_type, published)
    if captured < published:
        return "Anomaly", "capture_before_publication", "Capture timestamp precedes confirmed publication timestamp."
    if snapshot_type == "observed_lifetime":
        return "Anomaly", "none", "Lifetime observation is evidence only and never fills a contractual window."
    if target is None:
        raise ValueError(f"Unsupported Snapshot_Type: {snapshot_type}")
    distance = abs((captured - target).total_seconds())
    if distance <= tolerance:
        return (
            {"baseline_e0": "Valid_E0", "snapshot_24h": "Valid_24h", "snapshot_72h": "Valid_72h"}[snapshot_type],
            "none",
            "Capture falls within the approved tolerance.",
        )
    return "Late", "late_capture", "Capture is outside the approved tolerance; excluded from contractual closure."


def relative_or_absolute(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO.resolve()))
    except ValueError:
        return str(path)


def valid_row_for(rows: list[dict[str, str]], logical_key: str) -> dict[str, str] | None:
    valid = {"Valid_E0", "Valid_24h", "Valid_72h"}
    for row in rows:
        if row.get("Logical_Key") == logical_key and row.get("Window_Status") in valid:
            return row
    return None


def make_snapshot_row(
    *,
    payload: dict[str, Any],
    http_status: int,
    snapshot_type: str,
    meta_post_id: str,
    publicacion_id: str,
    experiment_id: str,
    id_pieza: str,
    cnt: str,
    platform: str,
    account_id: str,
    meta_photo_id: str,
    reel_id: str,
    published_override: datetime | None,
    captured: datetime,
    tolerance: int,
    source: str,
    raw_path: str,
    existing_rows: list[dict[str, str]],
    notes: str,
    run_id: str,
) -> dict[str, str]:
    published = published_override or parse_dt(str(payload.get("created_time", "")))
    if published is None:
        raise ValueError("Published_At_UTC is required or payload must contain created_time")
    counters = extract_counters(payload)
    status, anomaly, classification_note = classify_window(snapshot_type, published, captured, tolerance, counters)
    target = target_for(snapshot_type, published)
    interactions = sum(counters.values()) if all(value is not None for value in counters.values()) else None
    logical_key = f"{meta_post_id}+{snapshot_type}"
    e0 = valid_row_for(existing_rows, f"{meta_post_id}+baseline_e0")
    delta = ""
    if snapshot_type in {"snapshot_24h", "snapshot_72h"} and status in {"Valid_24h", "Valid_72h"} and e0 and interactions is not None:
        e0_interactions = as_int(e0.get("Lifetime_Interactions"))
        if e0_interactions is not None:
            delta = str(interactions - e0_interactions)
    seed = f"{run_id}|{logical_key}|{iso(captured)}|{uuid.uuid4().hex}"
    snapshot_id = "MS-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20].upper()
    all_notes = "; ".join(part for part in [classification_note, notes.strip()] if part)
    return {
        "Snapshot_ID": snapshot_id,
        "Logical_Key": logical_key,
        "Publicacion_ID": publicacion_id,
        "Experiment_ID": experiment_id,
        "ID_Pieza": id_pieza,
        "CNT": cnt,
        "Plataforma": platform,
        "Cuenta_ID": account_id,
        "Meta_Post_ID": meta_post_id,
        "Meta_Photo_ID": meta_photo_id,
        "Reel_ID": reel_id,
        "Published_At_UTC": iso(published),
        "Published_At_Local": published.astimezone(LOCAL_TZ).isoformat(),
        "Snapshot_Type": snapshot_type,
        "Target_At_UTC": iso(target),
        "Captured_At_UTC": iso(captured),
        "Age_Seconds": str(round((captured - published).total_seconds(), 3)),
        "Tolerance_Seconds": str(tolerance),
        "Window_Status": status,
        "Reactions": "" if counters["reactions"] is None else str(counters["reactions"]),
        "Comments": "" if counters["comments"] is None else str(counters["comments"]),
        "Shares": "" if counters["shares"] is None else str(counters["shares"]),
        "Lifetime_Interactions": "" if interactions is None else str(interactions),
        "Delta_From_E0": delta,
        "Source": source,
        "HTTP_Status": str(http_status),
        "Raw_Evidence_Path": raw_path,
        "Idempotency_Key": logical_key,
        "Anomaly_Code": anomaly,
        "Notes": all_notes,
    }


def fetch_meta_payload(meta_post_id: str, token: str) -> tuple[dict[str, Any], int]:
    fields = "created_time,reactions.limit(0).summary(true),comments.limit(0).summary(true),shares"
    response = requests.get(
        f"{GRAPH_BASE}/{meta_post_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"fields": fields},
        timeout=30,
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw_text": response.text}
    return payload, response.status_code


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meta-post-id", required=True)
    parser.add_argument("--snapshot-type", choices=["baseline_e0", "snapshot_24h", "snapshot_72h", "observed_lifetime"], required=True)
    parser.add_argument("--publicacion-id", default="")
    parser.add_argument("--experiment-id", default="")
    parser.add_argument("--id-pieza", default="")
    parser.add_argument("--cnt", default="")
    parser.add_argument("--platform", default="Facebook")
    parser.add_argument("--account-id", default=DEFAULT_ACCOUNT_ID)
    parser.add_argument("--meta-photo-id", default="")
    parser.add_argument("--reel-id", default="")
    parser.add_argument("--published-at-utc")
    parser.add_argument("--captured-at-utc")
    parser.add_argument("--tolerance-seconds", type=int)
    parser.add_argument("--source", default="Meta_Graph_API")
    parser.add_argument("--payload-file", type=Path, help="Saved API payload for deterministic replay; avoids network calls.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--notes", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger = args.ledger
    existing_rows = read_rows(ledger)
    logical_key = f"{args.meta_post_id}+{args.snapshot_type}"
    existing_valid = valid_row_for(existing_rows, logical_key)
    if existing_valid:
        print(json.dumps({"status": "no_op_valid_already_exists", "logical_key": logical_key, "snapshot_id": existing_valid.get("Snapshot_ID")}, ensure_ascii=False))
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
            raise SystemExit("META_PAGE_ACCESS_TOKEN is required when --payload-file is not provided")
        payload, http_status = fetch_meta_payload(args.meta_post_id, token)

    captured = parse_dt(args.captured_at_utc) if args.captured_at_utc else datetime.now(timezone.utc)
    assert captured is not None
    published_override = parse_dt(args.published_at_utc)
    tolerance = args.tolerance_seconds if args.tolerance_seconds is not None else default_tolerance(args.snapshot_type)
    run_id = args.run_id or captured.strftime("%Y%m%dT%H%M%SZ")

    args.raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = args.raw_dir / f"{args.meta_post_id}_{args.snapshot_type}_{captured.strftime('%Y%m%dT%H%M%SZ')}.json"
    raw_record = {
        "captured_at_utc": iso(captured),
        "meta_post_id": args.meta_post_id,
        "snapshot_type": args.snapshot_type,
        "http_status": http_status,
        "payload": payload,
    }
    raw_path.write_text(json.dumps(raw_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    row = make_snapshot_row(
        payload=payload,
        http_status=http_status,
        snapshot_type=args.snapshot_type,
        meta_post_id=args.meta_post_id,
        publicacion_id=args.publicacion_id,
        experiment_id=args.experiment_id,
        id_pieza=args.id_pieza,
        cnt=args.cnt,
        platform=args.platform,
        account_id=args.account_id,
        meta_photo_id=args.meta_photo_id,
        reel_id=args.reel_id,
        published_override=published_override,
        captured=captured,
        tolerance=tolerance,
        source=args.source,
        raw_path=relative_or_absolute(raw_path),
        existing_rows=existing_rows,
        notes=args.notes,
        run_id=run_id,
    )
    append_row(ledger, row)
    print(json.dumps({"status": "recorded", "snapshot_id": row["Snapshot_ID"], "logical_key": row["Logical_Key"], "window_status": row["Window_Status"], "raw_evidence_path": row["Raw_Evidence_Path"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
