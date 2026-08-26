#!/usr/bin/env python3
"""Validate and normalize synthetic multichannel metric observations for Universe Sent Me.

This utility is intentionally dry-run only. It accepts a fixture explicitly
marked synthetic, makes no network requests, never reads tokens or private
evidence, and does not write files, ledgers, Sheets, or OmniRoute payloads.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


BRAND = "Universe Sent Me"
NORMALIZER_VERSION = "0.1.0-dry-run"
ALLOWED_PLATFORMS = {"facebook", "instagram", "tiktok", "youtube"}
ALLOWED_SCOPES = {"content", "channel", "account"}
ALLOWED_UNITS = {"count", "seconds", "percentage", "currency", "ratio"}
ALLOWED_WINDOWS = {
    "lifetime_at_capture",
    "daily_activity",
    "interval_delta",
    "exact_window",
    "observed_cut",
    "historical_snapshot",
}
ALLOWED_AVAILABILITY = {
    "available",
    "not_available",
    "missing_field",
    "not_authorized",
    "not_applicable",
    "source_error",
    "deferred",
}
ALLOWED_COMPARABILITY = {
    "C0_not_comparable",
    "C1_same_platform_observed",
    "C2_same_platform_cohort",
    "C3_exact_window",
    "C4_cross_platform_directional",
}
DERIVED_METRICS = {"actions_available_sum", "actions_per_reach", "actions_per_view", "interval_delta"}
FORBIDDEN_FIELD_TOKENS = {
    "raw",
    "token",
    "secret",
    "caption",
    "title",
    "comment",
    "permalink",
    "share_url",
    "raw_evidence_path",
    "evidence_path",
    "private_url",
    "profile",
    "handle",
    "url",
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def observation_key(row: dict[str, Any]) -> str:
    components = [
        row.get("brand"),
        row.get("platform"),
        row.get("entity_scope"),
        row.get("platform_content_id"),
        row.get("metric_name"),
        row.get("window_type"),
        row.get("window_start_utc"),
        row.get("window_end_utc"),
        row.get("observed_at_utc"),
        row.get("source_system"),
        NORMALIZER_VERSION,
    ]
    return sha256_text("|".join("" if item is None else str(item) for item in components))


def is_numeric_nonnegative(value: Any) -> bool:
    try:
        return Decimal(str(value)) >= 0
    except (InvalidOperation, ValueError, TypeError):
        return False


def contains_forbidden_field(row: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for key in row:
        lowered = key.lower()
        if lowered in FORBIDDEN_FIELD_TOKENS or lowered.endswith("_url") or "path" in lowered:
            found.append(key)
    return sorted(found)


def validate_row(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if row.get("brand") != BRAND:
        errors.append("NORM-01: brand must be exactly Universe Sent Me")
    if row.get("platform") not in ALLOWED_PLATFORMS or row.get("target_account_confirmed") is not True:
        errors.append("NORM-02: platform must be allowed and target account confirmed")
    if row.get("entity_scope") not in ALLOWED_SCOPES:
        errors.append("NORM-03: entity_scope must be content, channel, or account")
    elif row.get("entity_scope") == "content" and not row.get("platform_content_id"):
        errors.append("NORM-03: content observations require platform_content_id")
    required = ("observed_at_utc", "source_system", "source_endpoint", "metric_definition", "window_type")
    if any(not row.get(field) for field in required) or row.get("window_type") not in ALLOWED_WINDOWS:
        errors.append("NORM-04: source, observation time, definition, and valid window are required")
    availability = row.get("availability_status")
    value = row.get("metric_value")
    if availability == "available" and (value is None or not is_numeric_nonnegative(value)):
        errors.append("NORM-05: available values must be numeric and non-negative")
    if availability not in ALLOWED_AVAILABILITY:
        errors.append("NORM-06: availability_status is invalid")
    elif value is None and availability == "available":
        errors.append("NORM-06: null values cannot be marked available")
    elif value is not None and availability != "available":
        errors.append("NORM-06: unavailable values must be null")
    if row.get("metric_unit") not in ALLOWED_UNITS:
        errors.append("NORM-05: metric_unit is invalid")
    if row.get("metric_name") in DERIVED_METRICS:
        formula = row.get("derivation_formula")
        components = row.get("derivation_components")
        denominator = row.get("derivation_denominator")
        if not formula or not isinstance(components, list) or not denominator:
            errors.append("NORM-07: derived metrics require formula, components, and denominator")
    mixed = row.get("aggregate_window_types")
    if mixed:
        errors.append("NORM-08: a normalized observation cannot aggregate window types")
    fingerprint = row.get("evidence_fingerprint")
    if not isinstance(fingerprint, str) or len(fingerprint) != 64:
        errors.append("NORM-09: evidence_fingerprint must be a SHA-256 hash")
    if row.get("metric_unit") == "currency" and row.get("financial_restricted") is not True:
        errors.append("NORM-11: currency metrics must be financial_restricted")
    if row.get("comparability_tier") not in ALLOWED_COMPARABILITY:
        errors.append("NORM-08: comparability_tier is invalid")
    forbidden = contains_forbidden_field(row)
    if forbidden:
        errors.append(f"NORM-12: forbidden fields present: {', '.join(forbidden)}")
    return errors


def normalise(input_payload: dict[str, Any]) -> dict[str, Any]:
    if input_payload.get("synthetic") is not True:
        raise RuntimeError("Dry-run accepts only payloads explicitly marked synthetic=true.")
    if input_payload.get("brand") != BRAND:
        raise RuntimeError("Dry-run input brand must be exactly Universe Sent Me.")
    rows = input_payload.get("observations")
    if not isinstance(rows, list) or not rows:
        raise RuntimeError("Dry-run input requires a non-empty observations list.")
    input_hash = sha256_text(stable_json(input_payload))
    transform_run_id = f"dryrun-{input_hash[:16]}"
    seen: set[str] = set()
    output_rows: list[dict[str, Any]] = []
    validation_counts = {"valid": 0, "partial": 0, "rejected": 0, "duplicate_skip": 0}

    for source_row in rows:
        if not isinstance(source_row, dict):
            output_rows.append({"row_status": "rejected", "validation_errors": ["Observation must be an object."]})
            validation_counts["rejected"] += 1
            continue
        row = dict(source_row)
        errors = validate_row(row)
        key = observation_key(row)
        if key in seen:
            output_rows.append(
                {
                    "observation_key": key,
                    "row_status": "duplicate_skip",
                    "validation_errors": ["NORM-10: duplicate observation key within dry-run batch"],
                }
            )
            validation_counts["duplicate_skip"] += 1
            continue
        seen.add(key)
        if errors:
            output_rows.append(
                {
                    "observation_key": key,
                    "row_status": "rejected",
                    "validation_errors": errors,
                }
            )
            validation_counts["rejected"] += 1
            continue
        row["observation_key"] = key
        row["transform_run_id"] = transform_run_id
        row["normalizer_version"] = NORMALIZER_VERSION
        row["row_status"] = "partial" if row.get("availability_status") != "available" else "valid"
        row["validation_errors"] = []
        output_rows.append(row)
        validation_counts[row["row_status"]] += 1

    return {
        "status": "dry_run_complete",
        "mode": "synthetic_only_no_write",
        "brand": BRAND,
        "transform_run_id": transform_run_id,
        "normalizer_version": NORMALIZER_VERSION,
        "input_fingerprint": input_hash,
        "input_observations": len(rows),
        "validation_counts": validation_counts,
        "normalized_observations": output_rows,
        "guarantees": [
            "No network requests were made.",
            "No private evidence, tokens, paths, or canonical ledgers were read or written.",
            "Only a payload explicitly marked synthetic=true was accepted.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Synthetic JSON fixture to validate.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON instead of indented JSON.")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = normalise(payload)
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
