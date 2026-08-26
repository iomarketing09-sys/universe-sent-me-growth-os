#!/usr/bin/env python3
"""Inspect a synthetic shadow ledger without modifying or repairing it.

The inspector is deliberately read-only. Its result reports only aggregate
integrity findings and never emits ledger rows, identifiers, paths, raw
evidence, credentials, or any real observations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from shadow_ledger_private import BRAND, LEDGER_SCHEMA_VERSION, entry_key, load_events


def inspect_ledger(ledger_path: Path) -> dict[str, Any]:
    """Return an integrity report without writing, repairing, or deleting data."""
    if not ledger_path.exists():
        return {"status": "invalid", "errors": ["ledger_missing"], "event_count": 0}

    try:
        events = load_events(ledger_path)
    except RuntimeError as error:
        return {"status": "invalid", "errors": ["jsonl_invalid"], "event_count": 0, "detail": str(error)}

    errors: list[str] = []
    if not events:
        errors.append("ledger_empty")
    elif events[0].get("record_type") != "genesis":
        errors.append("genesis_missing_or_not_first")

    genesis_events = [event for event in events if event.get("record_type") == "genesis"]
    if len(genesis_events) != 1:
        errors.append("genesis_count_invalid")
    elif (
        genesis_events[0].get("brand") != BRAND
        or genesis_events[0].get("ledger_schema_version") != LEDGER_SCHEMA_VERSION
    ):
        errors.append("genesis_contract_invalid")

    observed_keys: set[str] = set()
    superseded_keys: set[str] = set()
    for event in events:
        record_type = event.get("record_type")
        if record_type == "genesis":
            continue
        if record_type != "observation":
            errors.append("record_type_invalid")
            continue

        observation_key = event.get("observation_key")
        ledger_entry_key = event.get("ledger_entry_key")
        if not isinstance(observation_key, str) or not isinstance(ledger_entry_key, str):
            errors.append("observation_identity_invalid")
            continue
        if entry_key(event) != ledger_entry_key:
            errors.append("entry_key_invalid")

        previous_key = event.get("supersedes_observation_key")
        if previous_key is not None:
            if not isinstance(previous_key, str) or previous_key not in observed_keys:
                errors.append("supersession_target_missing")
            elif previous_key in superseded_keys:
                errors.append("supersession_target_already_superseded")
            else:
                superseded_keys.add(previous_key)
        elif observation_key in observed_keys:
            errors.append("observation_key_collision")

        observed_keys.add(observation_key)

    return {
        "status": "valid" if not errors else "invalid",
        "errors": sorted(set(errors)),
        "event_count": len(events),
        "observation_count": len(observed_keys),
        "superseded_count": len(superseded_keys),
        "guarantees": ["read_only", "no_repair", "no_network", "no_canonical_write"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True, help="Synthetic temporary JSONL ledger.")
    args = parser.parse_args()
    print(json.dumps(inspect_ledger(args.ledger), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
