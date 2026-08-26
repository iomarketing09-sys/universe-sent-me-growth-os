#!/usr/bin/env python3
"""Simulate synthetic temporary ledger inconsistencies and prove no repair occurs.

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

            invalid_genesis = root / "invalid-genesis-contract.jsonl"
            invalid_genesis_events = seed_ledger(invalid_genesis, fixture)
            invalid_genesis_events[0]["brand"] = "Synthetic Other Brand"
            invalid_genesis.write_text(
                "".join(stable_json(event) + "\n" for event in invalid_genesis_events),
                encoding="utf-8",
            )
            assert_read_only(invalid_genesis, "genesis_contract_invalid")

            unknown_record = root / "unknown-record-type.jsonl"
            unknown_record_events = seed_ledger(unknown_record, fixture)
            unknown_record_events.append({"record_type": "synthetic_audit_marker"})
            unknown_record.write_text(
                "".join(stable_json(event) + "\n" for event in unknown_record_events),
                encoding="utf-8",
            )
            assert_read_only(unknown_record, "record_type_invalid")

            collision = root / "observation-key-collision.jsonl"
            collision_events = seed_ledger(collision, fixture)
            duplicate_observation = copy.deepcopy(collision_events[1])
            duplicate_observation["evidence_fingerprint"] = "5" * 64
            duplicate_observation["transform_run_id"] = "shadow-synthetic-collision"
            duplicate_observation["ledger_entry_key"] = entry_key(duplicate_observation)
            collision.write_text(
                "".join(stable_json(event) + "\n" for event in [*collision_events, duplicate_observation]),
                encoding="utf-8",
            )
            assert_read_only(collision, "observation_key_collision")

            altered_entry_key = root / "altered-entry-key.jsonl"
            altered_entry_events = seed_ledger(altered_entry_key, fixture)
            altered_entry_events[1]["ledger_entry_key"] = "0" * 64
            altered_entry_key.write_text(
                "".join(stable_json(event) + "\n" for event in altered_entry_events),
                encoding="utf-8",
            )
            assert_read_only(altered_entry_key, "entry_key_invalid")

            invalid_norm = root / "invalid-normalized-observation.jsonl"
            invalid_norm_events = seed_ledger(invalid_norm, fixture)
            invalid_norm_events[1]["metric_value"] = -1
            invalid_norm.write_text(
                "".join(stable_json(event) + "\n" for event in invalid_norm_events),
                encoding="utf-8",
            )
            assert_read_only(invalid_norm, "observation_norm_invalid")

            duplicate_entry = root / "duplicate-ledger-entry-key.jsonl"
            duplicate_entry_events = seed_ledger(duplicate_entry, fixture)
            duplicate_entry.write_text(
                "".join(stable_json(event) + "\n" for event in [*duplicate_entry_events, copy.deepcopy(duplicate_entry_events[1])]),
                encoding="utf-8",
            )
            assert_read_only(duplicate_entry, "ledger_entry_key_duplicate")

    print(
        json.dumps(
            {
                "status": "shadow_ledger_corruption_synthetic_validation_passed",
                "tests": [
                    "malformed_jsonl_detected",
                    "genesis_missing_detected",
                    "inconsistent_supersession_detected",
                    "invalid_genesis_contract_detected",
                    "unknown_record_type_detected",
                    "observation_key_collision_detected",
                    "altered_entry_key_detected",
                    "invalid_normalized_observation_detected",
                    "duplicate_ledger_entry_key_detected",
                    "byte_invariance_confirmed",
                ],
                "guarantees": ["synthetic_only", "temporary_ledger_only", "network_socket_blocked", "read_only_inspection", "no_automatic_repair", "no_canonical_write"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
