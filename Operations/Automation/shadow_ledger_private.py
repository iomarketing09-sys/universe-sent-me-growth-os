#!/usr/bin/env python3
"""Append synthetic normalized observations to a private USM shadow ledger.

G-NORM-4 safety contract: input must be explicitly synthetic, every event is
append-only JSONL, no network is used, and the command never writes canonical
ledgers, Sheets, OmniRoute, or source evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from normalize_metrics_dry_run import BRAND, NORMALIZER_VERSION, observation_key, validate_row


LEDGER_SCHEMA_VERSION = "shadow-ledger-v1"
FORBIDDEN_VALUES = ("http://", "https://", "~/.local", "/home/", "access_token", "refresh_token")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def entry_key(row: dict[str, Any]) -> str:
    return sha256_text(
        "|".join(
            [
                str(row["observation_key"]),
                str(row["evidence_fingerprint"]),
                str(row["transform_run_id"]),
                str(row.get("supersedes_observation_key") or ""),
            ]
        )
    )


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeError(f"Shadow ledger contains invalid JSONL at line {line_number}.") from error
            if not isinstance(event, dict):
                raise RuntimeError(f"Shadow ledger event {line_number} is not an object.")
            events.append(event)
    return events


def ensure_ledger(path: Path) -> list[dict[str, Any]]:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    events = load_events(path)
    if events:
        return events
    genesis = {
        "record_type": "genesis",
        "ledger_schema_version": LEDGER_SCHEMA_VERSION,
        "brand": BRAND,
        "created_at_utc": utc_now(),
        "normalizer_version": NORMALIZER_VERSION,
        "contract": "G-NORM-4_synthetic_only_append_only",
    }
    append_event(path, genesis)
    return [genesis]


def append_event(path: Path, event: dict[str, Any]) -> None:
    encoded = stable_json(event) + "\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    descriptor = os.open(path, flags, 0o600)
    try:
        os.write(descriptor, encoded.encode("utf-8"))
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(path, 0o600)


def unsafe_values_present(row: dict[str, Any]) -> bool:
    serialized = stable_json(row).lower()
    return any(value in serialized for value in FORBIDDEN_VALUES)


def existing_state(events: list[dict[str, Any]]) -> tuple[set[str], dict[str, str], set[str]]:
    entry_keys: set[str] = set()
    observation_to_entry: dict[str, str] = {}
    superseded: set[str] = set()
    for event in events:
        if event.get("record_type") != "observation":
            continue
        if isinstance(event.get("ledger_entry_key"), str):
            entry_keys.add(event["ledger_entry_key"])
        if isinstance(event.get("observation_key"), str):
            observation_to_entry[event["observation_key"]] = event.get("ledger_entry_key", "")
        if isinstance(event.get("supersedes_observation_key"), str):
            superseded.add(event["supersedes_observation_key"])
    return entry_keys, observation_to_entry, superseded


def prepare_row(source: dict[str, Any], run_id: str) -> tuple[dict[str, Any] | None, str | None]:
    row = dict(source)
    errors = validate_row(row)
    if errors:
        return None, "validation_rejected"
    if unsafe_values_present(row):
        return None, "sanitization_rejected"
    row["observation_key"] = observation_key(row)
    row["transform_run_id"] = run_id
    row["normalizer_version"] = NORMALIZER_VERSION
    row["row_status"] = "partial" if row["availability_status"] != "available" else "valid"
    row["record_type"] = "observation"
    row["ledger_schema_version"] = LEDGER_SCHEMA_VERSION
    row["supersedes_observation_key"] = row.get("supersedes_observation_key") or None
    row["ledger_entry_key"] = entry_key(row)
    return row, None


def append_fixture(ledger_path: Path, fixture: dict[str, Any]) -> dict[str, Any]:
    if fixture.get("synthetic") is not True or fixture.get("brand") != BRAND:
        raise RuntimeError("G-NORM-4 accepts only fixtures marked synthetic=true for Universe Sent Me.")
    observations = fixture.get("observations")
    if not isinstance(observations, list) or not observations:
        raise RuntimeError("Fixture requires a non-empty observations list.")
    events = ensure_ledger(ledger_path)
    entry_keys, observations_by_key, superseded = existing_state(events)
    run_id = "shadow-" + sha256_text(stable_json(fixture))[:16]
    summary = {"appended": 0, "duplicate_skip": 0, "rejected": 0, "supersessions": 0}
    for source in observations:
        if not isinstance(source, dict):
            summary["rejected"] += 1
            continue
        prepared, issue = prepare_row(source, run_id)
        if issue or prepared is None:
            summary["rejected"] += 1
            continue
        if prepared["ledger_entry_key"] in entry_keys:
            summary["duplicate_skip"] += 1
            continue
        previous_key = prepared.get("supersedes_observation_key")
        existing_observation = prepared["observation_key"] in observations_by_key
        if previous_key:
            if previous_key not in observations_by_key or previous_key in superseded:
                summary["rejected"] += 1
                continue
            summary["supersessions"] += 1
            superseded.add(previous_key)
        elif existing_observation:
            summary["rejected"] += 1
            continue
        append_event(ledger_path, prepared)
        events.append(prepared)
        entry_keys.add(prepared["ledger_entry_key"])
        observations_by_key[prepared["observation_key"]] = prepared["ledger_entry_key"]
        summary["appended"] += 1
    return {
        "status": "shadow_ledger_synthetic_write_complete",
        "mode": "G-NORM-4_private_append_only_synthetic",
        "brand": BRAND,
        "normalizer_version": NORMALIZER_VERSION,
        "summary": summary,
        "ledger_event_counts": {
            "genesis": sum(1 for event in events if event.get("record_type") == "genesis"),
            "observations": sum(1 for event in events if event.get("record_type") == "observation"),
        },
        "guarantees": [
            "No network requests were made.",
            "Only fixtures marked synthetic=true are accepted.",
            "The private ledger is append-only; no event is updated or deleted.",
            "No canonical ledger, Google Sheet, OmniRoute payload, cron, or source evidence was written.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Synthetic fixture JSON.")
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path("~/.local/share/usm-metrics/shadow-ledger/normalized_metric_observations.shadow.jsonl").expanduser(),
        help="Private local JSONL ledger path.",
    )
    args = parser.parse_args()
    fixture = json.loads(args.input.read_text(encoding="utf-8"))
    result = append_fixture(args.ledger.expanduser().resolve(), fixture)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
