#!/usr/bin/env python3
"""Validate synthetic idempotency and supersedence for the private shadow ledger."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from normalize_metrics_dry_run import observation_key
from shadow_ledger_private import append_fixture, load_events


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "shadow_ledger_synthetic.json"


def main() -> int:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="usm-shadow-ledger-test-") as temp_dir:
        ledger = Path(temp_dir) / "shadow.jsonl"
        first = append_fixture(ledger, fixture)
        assert first["summary"] == {"appended": 1, "duplicate_skip": 0, "rejected": 0, "supersessions": 0}, first
        duplicate = append_fixture(ledger, fixture)
        assert duplicate["summary"] == {"appended": 0, "duplicate_skip": 1, "rejected": 0, "supersessions": 0}, duplicate

        original_key = observation_key(fixture["observations"][0])
        collision = json.loads(json.dumps(fixture))
        collision["observations"][0]["metric_value"] = 43
        collision["observations"][0]["evidence_fingerprint"] = "2222222222222222222222222222222222222222222222222222222222222222"
        collision_result = append_fixture(ledger, collision)
        assert collision_result["summary"]["rejected"] == 1, collision_result

        correction = json.loads(json.dumps(collision))
        correction["observations"][0]["supersedes_observation_key"] = original_key
        corrected = append_fixture(ledger, correction)
        assert corrected["summary"] == {"appended": 1, "duplicate_skip": 0, "rejected": 0, "supersessions": 1}, corrected
        events = load_events(ledger)
        assert len(events) == 3, events
        assert [event["record_type"] for event in events] == ["genesis", "observation", "observation"], events

    print(
        json.dumps(
            {
                "status": "shadow_ledger_synthetic_validation_passed",
                "tests": ["initial_append", "idempotent_rerun", "in_place_collision_rejected", "append_only_supersession"],
                "guarantees": ["synthetic_only", "private_temp_ledger", "no_network", "no_canonical_write"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
