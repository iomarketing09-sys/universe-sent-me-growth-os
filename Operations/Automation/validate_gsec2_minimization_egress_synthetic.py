#!/usr/bin/env python3
"""Validate G-SEC-2 minimization and egress policy using only fictional data.

This verifier reads one public, versioned fixture. It never imports collectors,
reads private paths or environment variables, opens a socket, calls OAuth/API,
starts processes, installs packages, or writes a ledger, evidence, or output.
"""

from __future__ import annotations

import json
import socket
from pathlib import Path
from unittest.mock import patch


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "gsec2_minimization_egress_synthetic.json"
EXPECTED_BRAND = "Universe Sent Me"
ALLOWED_DATA_CLASS = "synthetic_observation"
ALLOWED_DESTINATION = "temporary_memory"


def blocked_network(*_args: object, **_kwargs: object) -> None:
    raise AssertionError("G-SEC-2.1a must not open a network socket.")


def rejection_reason(case: dict[str, object], allowed_fields: set[str]) -> str | None:
    if case.get("brand") != EXPECTED_BRAND:
        return "brand_not_allowed"
    if case.get("data_class") != ALLOWED_DATA_CLASS:
        return "data_class_not_allowed"
    fields = case.get("fields")
    if not isinstance(fields, list) or not all(isinstance(field, str) for field in fields):
        return "invalid_field_declaration"
    if set(fields) - allowed_fields:
        return "nonminimal_field_not_allowed"
    if case.get("destination") != ALLOWED_DESTINATION or case.get("external_egress") is not False:
        return "external_egress_not_allowed"
    return None


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert payload == json.loads(FIXTURE.read_text(encoding="utf-8")), "fixture must not change during validation"
    assert payload.get("synthetic") is True, "fixture must be explicitly synthetic"
    assert payload.get("brand") == EXPECTED_BRAND, "fixture brand must be Universe Sent Me"
    fields = payload.get("allowed_fields")
    cases = payload.get("cases")
    assert isinstance(fields, list) and fields, "fixture needs an allowed field list"
    assert isinstance(cases, list) and cases, "fixture needs synthetic cases"
    allowed_fields = set(fields)

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
            reason = rejection_reason(case, allowed_fields)
            if name == "minimum_local_aggregate_allowed":
                assert reason is None, f"{name} must be allowed: {reason}"
                results[name] = "allowed_synthetic_only"
            else:
                assert reason is not None, f"{name} must be rejected"
                results[name] = reason

    expected_rejections = {
        "caption_field_blocked": "nonminimal_field_not_allowed",
        "creator_identifier_blocked": "nonminimal_field_not_allowed",
        "raw_response_blocked": "data_class_not_allowed",
        "drive_egress_blocked": "external_egress_not_allowed",
        "sheets_egress_blocked": "external_egress_not_allowed",
        "other_brand_blocked": "brand_not_allowed",
    }
    for name, expected in expected_rejections.items():
        assert results.get(name) == expected, f"{name} differs: {results.get(name)}"

    print(json.dumps({
        "status": "gsec2_minimization_egress_synthetic_passed",
        "allowed_case": "minimum_local_aggregate_allowed",
        "blocked_cases": expected_rejections,
        "guarantees": [
            "synthetic_fixture_only",
            "network_socket_blocked",
            "no_collector_import",
            "no_private_path_or_environment_read",
            "no_ledger_evidence_or_external_write",
            "minimum_fields_and_local_memory_only",
        ],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
