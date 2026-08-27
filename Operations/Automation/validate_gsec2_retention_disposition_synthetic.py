#!/usr/bin/env python3
"""Validate G-SEC-2 retention and disposition policy with a fictional fixture.

The verifier models policy outcomes in memory only. It never opens private data,
environment variables, sockets, collectors, APIs, services, or persistent files.
It does not delete, rewrite, archive, or otherwise mutate any ledger or evidence.
"""

from __future__ import annotations

import json
import socket
from pathlib import Path
from unittest.mock import patch


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "gsec2_retention_disposition_synthetic.json"
ALLOWED_DESTINATION = "temporary_memory"


def blocked_network(*_args: object, **_kwargs: object) -> None:
    raise AssertionError("G-SEC-2.2a must not open a network socket.")


def policy_outcome(case: dict[str, object], retention_days: int) -> str | None:
    age_days = case.get("age_days")
    if not isinstance(age_days, int) or age_days < 0:
        return "invalid_retention_age"
    if case.get("destination") != ALLOWED_DESTINATION:
        return "external_archive_not_allowed"
    if case.get("mutates_record") is not False:
        return "automatic_or_in_place_mutation_not_allowed"
    if age_days > retention_days:
        return "expired_record_requires_human_disposition"
    if age_days == retention_days:
        if case.get("human_review") is not True or case.get("proposed_action") != "block_new_writes_and_request_human_review":
            return "retention_boundary_requires_human_review"
    return None


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert payload == json.loads(FIXTURE.read_text(encoding="utf-8")), "fixture must not change during validation"
    assert payload.get("synthetic") is True, "fixture must be explicitly synthetic"
    assert payload.get("brand") == "Universe Sent Me", "fixture brand must be Universe Sent Me"
    retention_days = payload.get("retention_days")
    cases = payload.get("cases")
    assert retention_days == 30, "synthetic retention policy must be 30 days"
    assert isinstance(cases, list) and cases, "fixture needs synthetic cases"

    results: dict[str, str] = {}
    with patch.object(socket, "socket", side_effect=blocked_network):
        try:
            socket.socket()
        except AssertionError:
            results["socket_guard"] = "blocked_as_designed"
        else:
            raise AssertionError("socket guard did not block")

        for case in cases:
            assert isinstance(case, dict), "every case must be an object"
            name = case.get("name")
            assert isinstance(name, str) and name, "every case requires a name"
            outcome = policy_outcome(case, retention_days)
            if name in {"active_record_allowed", "boundary_requires_human_review"}:
                assert outcome is None, f"{name} must be allowed: {outcome}"
                results[name] = "allowed_synthetic_policy_only"
            else:
                assert outcome is not None, f"{name} must be rejected"
                results[name] = outcome

    expected_rejections = {
        "expired_without_review_blocked": "expired_record_requires_human_disposition",
        "automatic_delete_blocked": "automatic_or_in_place_mutation_not_allowed",
        "in_place_rewrite_blocked": "automatic_or_in_place_mutation_not_allowed",
        "external_archive_blocked": "external_archive_not_allowed",
        "indefinite_hold_blocked": "expired_record_requires_human_disposition",
    }
    for name, expected in expected_rejections.items():
        assert results.get(name) == expected, f"{name} differs: {results.get(name)}"

    print(json.dumps({
        "status": "gsec2_retention_disposition_synthetic_passed",
        "allowed_cases": ["active_record_allowed", "boundary_requires_human_review"],
        "blocked_cases": expected_rejections,
        "retention_days": retention_days,
        "guarantees": [
            "synthetic_fixture_only",
            "network_socket_blocked",
            "no_collector_import",
            "no_private_path_or_environment_read",
            "no_ledger_evidence_or_external_write",
            "no_automatic_deletion_or_in_place_mutation",
        ],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
