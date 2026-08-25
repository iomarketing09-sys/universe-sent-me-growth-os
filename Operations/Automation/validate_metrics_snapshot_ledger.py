#!/usr/bin/env python3
"""Validate the USM append-only Metrics_Snapshot_Log.csv contract."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER = REPO / "Operations/Research/Metrics_Snapshot_Log.csv"
EXPECTED_FIELDS = [
    "Snapshot_ID", "Logical_Key", "Publicacion_ID", "Experiment_ID", "ID_Pieza", "CNT",
    "Plataforma", "Cuenta_ID", "Meta_Post_ID", "Meta_Photo_ID", "Reel_ID",
    "Published_At_UTC", "Published_At_Local", "Snapshot_Type", "Target_At_UTC",
    "Captured_At_UTC", "Age_Seconds", "Tolerance_Seconds", "Window_Status",
    "Reactions", "Comments", "Shares", "Lifetime_Interactions", "Delta_From_E0",
    "Source", "HTTP_Status", "Raw_Evidence_Path", "Idempotency_Key", "Anomaly_Code", "Notes",
]
VALID_STATUSES = {"Valid_E0", "Valid_24h", "Valid_72h", "Late", "Missing", "API_Error", "Anomaly"}
VALID_TYPES = {"baseline_e0", "snapshot_24h", "snapshot_72h", "observed_lifetime"}
CONTRACTUAL_STATUS = {"Valid_E0", "Valid_24h", "Valid_72h"}


def parse_int(value: str, field: str, errors: list[str], row_no: int) -> int | None:
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        errors.append(f"row {row_no}: {field} is not an integer: {value!r}")
        return None


def load(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    if not path.exists():
        return [], []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def validate(path: Path) -> dict[str, object]:
    rows, fields = load(path)
    errors: list[str] = []
    warnings: list[str] = []
    if fields != EXPECTED_FIELDS:
        errors.append("header does not match the approved Metrics_Snapshot_Log schema")
    seen_snapshot: Counter[str] = Counter()
    seen_valid_logical: Counter[str] = Counter()
    e0_by_post: dict[str, dict[str, str]] = {}
    status_counts: Counter[str] = Counter()

    for row_no, row in enumerate(rows, start=2):
        snapshot_id = row.get("Snapshot_ID", "")
        logical_key = row.get("Logical_Key", "")
        status = row.get("Window_Status", "")
        snapshot_type = row.get("Snapshot_Type", "")
        meta_post_id = row.get("Meta_Post_ID", "")
        status_counts[status] += 1
        if not snapshot_id:
            errors.append(f"row {row_no}: Snapshot_ID missing")
        seen_snapshot[snapshot_id] += 1
        if not logical_key:
            errors.append(f"row {row_no}: Logical_Key missing")
        if status not in VALID_STATUSES:
            errors.append(f"row {row_no}: invalid Window_Status {status!r}")
        if snapshot_type not in VALID_TYPES:
            errors.append(f"row {row_no}: invalid Snapshot_Type {snapshot_type!r}")
        if not meta_post_id:
            errors.append(f"row {row_no}: Meta_Post_ID missing")
        if row.get("Idempotency_Key") != logical_key:
            errors.append(f"row {row_no}: Idempotency_Key must equal Logical_Key")
        if status in CONTRACTUAL_STATUS:
            seen_valid_logical[logical_key] += 1
            required = ["Published_At_UTC", "Captured_At_UTC", "Target_At_UTC", "Source", "HTTP_Status", "Raw_Evidence_Path"]
            for field in required:
                if not row.get(field, ""):
                    errors.append(f"row {row_no}: {field} missing for contractual row")
            if row.get("HTTP_Status") != "200":
                errors.append(f"row {row_no}: contractual row must have HTTP_Status=200")
            for field in ("Reactions", "Comments", "Shares", "Lifetime_Interactions"):
                parse_int(row.get(field, ""), field, errors, row_no)
            if snapshot_type == "baseline_e0":
                if status != "Valid_E0":
                    errors.append(f"row {row_no}: baseline_e0 must use Valid_E0")
                if meta_post_id in e0_by_post:
                    errors.append(f"row {row_no}: duplicate valid E0 for Meta_Post_ID {meta_post_id}")
                e0_by_post[meta_post_id] = row
            if snapshot_type == "snapshot_24h" and status != "Valid_24h":
                errors.append(f"row {row_no}: snapshot_24h must use Valid_24h")
            if snapshot_type == "snapshot_72h" and status != "Valid_72h":
                errors.append(f"row {row_no}: snapshot_72h must use Valid_72h")
        else:
            if row.get("Delta_From_E0", ""):
                errors.append(f"row {row_no}: non-contractual row must not contain Delta_From_E0")
        if status in {"Valid_24h", "Valid_72h"}:
            if meta_post_id not in e0_by_post:
                errors.append(f"row {row_no}: {status} has no earlier valid E0 for Meta_Post_ID {meta_post_id}")
            if not row.get("Delta_From_E0", ""):
                errors.append(f"row {row_no}: {status} is missing Delta_From_E0")
        raw_value = row.get("Raw_Evidence_Path", "")
        if raw_value:
            raw_path = Path(raw_value)
            if not raw_path.is_absolute():
                raw_path = REPO / raw_path
            if not raw_path.exists():
                errors.append(f"row {row_no}: Raw_Evidence_Path does not exist: {raw_value}")
        tolerance = parse_int(row.get("Tolerance_Seconds", ""), "Tolerance_Seconds", errors, row_no)
        if tolerance is not None and tolerance < 0:
            errors.append(f"row {row_no}: Tolerance_Seconds cannot be negative")

    duplicate_snapshot_ids = sorted(key for key, count in seen_snapshot.items() if key and count > 1)
    duplicate_valid_keys = sorted(key for key, count in seen_valid_logical.items() if count > 1)
    if duplicate_snapshot_ids:
        errors.append("duplicate Snapshot_ID values: " + ", ".join(duplicate_snapshot_ids))
    if duplicate_valid_keys:
        errors.append("duplicate valid Logical_Key values: " + ", ".join(duplicate_valid_keys))
    for key, count in seen_snapshot.items():
        if not key:
            continue
        if count > 1:
            warnings.append(f"Snapshot_ID repeated {count} times: {key}")

    return {
        "ledger": str(path),
        "rows": len(rows),
        "status_counts": dict(status_counts),
        "valid_e0_posts": len(e0_by_post),
        "duplicate_snapshot_ids": duplicate_snapshot_ids,
        "duplicate_valid_logical_keys": duplicate_valid_keys,
        "errors": errors,
        "warnings": warnings,
        "VALIDATION": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", nargs="?", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--json", action="store_true", help="Print the report as JSON")
    args = parser.parse_args()
    report = validate(args.ledger)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report, ensure_ascii=False))
    return 0 if report["VALIDATION"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
