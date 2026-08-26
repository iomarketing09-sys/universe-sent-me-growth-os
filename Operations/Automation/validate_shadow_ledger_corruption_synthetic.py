#!/usr/bin/env python3
"""Simulate synthetic temporary ledger corruption and prove no repair occurs.

All files are created under a TemporaryDirectory and removed automatically.
The test never uses source evidence, real identifiers, environment secrets,
network access, canonical ledgers, Google Sheets, or OmniRoute.
"""

from __future__ import annotations

import copy
import json
import socket
import tempfile
from pathlib import Path
from unittest.mock import patch

from inspect_shadow_ledger_synthetic import inspect_ledger
from shadow_ledger_private import append_fixture, entry_key, load_events, stable_json


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "shadow_ledger_synthetic.json"


def block_network(*_args, **_kwargs):
    raise AssertionError("Corruption suite must not open a network socket.")


def assert_read_only(ledger: Path, expected_error: str) -> None:
    before = ledger.read_bytes()
    report = inspect_ledger(ledger)
    after = ledger.read_bytes()
    assert before == after, "The inspector must not repair or modify a corrupted temporary ledger."
    assert report["status"] == "invalid", report
    assert expected_error in report["errors"], report


def seed_ledger(ledger: Path, fixture: dict) -> list[dict]:
    result = append_fixture(ledger, fixture)
    assert result["summary"]["appended"] == 1, result
    return load_events(ledger)


def main() -> int:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    with patch.object(socket, "socket", side_effect=block_network):
        with tempfile.TemporaryDirectory(prefix="usm-shadow-corruption-") as temp_dir:
            root = Path(temp_dir)

            malformed = root / "malformed.jsonl"
            seed_ledger(malformed, fixture)
            malformed.write_bytes(malformed.read_bytes() + b'{"record_type":"observation"\n')
            assert_read_only(malformed, "jsonl_invalid")

            without_genesis = root / "without-genesis.jsonl"
            valid_events = seed_ledger(root / "seed.jsonl", fixture)
            without_genesis.write_text(stable_json(valid_events[1]) + "\n", encoding="utf-8")
            assert_read_only(without_genesis, "genesis_missing_or_not_first")

            inconsistent = root / "inconsistent-supersession.jsonl"
            seed_events = seed_ledger(inconsistent, fixture)
            invalid_event = copy.deepcopy(seed_events[1])
            invalid_event["evidence_fingerprint"] = "3" * 64
            invalid_event["supersedes_observation_key"] = "4" * 64
            invalid_event["ledger_entry_key"] = entry_key(invalid_event)
            inconsistent.write_text(
                "".join(stable_json(event) + "\n" for event in [*seed_events, invalid_event]),
                encoding="utf-8",
            )
            assert_read_only(inconsistent, "supersession_target_missing")

    print(
        json.dumps(
            {
                "status": "shadow_ledger_corruption_synthetic_validation_passed",
                "tests": ["malformed_jsonl_detected", "genesis_missing_detected", "inconsistent_supersession_detected", "byte_invariance_confirmed"],
                "guarantees": ["synthetic_only", "temporary_ledger_only", "network_socket_blocked", "read_only_inspection", "no_automatic_repair", "no_canonical_write"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
