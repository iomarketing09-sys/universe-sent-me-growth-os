#!/usr/bin/env python3
"""Validate proposed G-SEC-2 barriers with a synthetic fixture only.

Safety boundary: this validator reads one versioned synthetic JSON fixture. It
never imports collectors, reads private paths or environment variables, opens a
network socket, invokes OAuth or APIs, starts processes, installs packages, or
writes a ledger, evidence, canonical record, or external destination.
"""

from __future__ import annotations

import json
import socket
from pathlib import Path
from unittest.mock import patch


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "gsec2_readonly_barriers_synthetic.json"
ALLOWED_DESTINATION = "temporary_memory"
ALLOWED_EXECUTION = "manual_once"
ALLOWED_DATA_CLASS = "synthetic_fixture"
EXPECTED_BRAND = "Universe Sent Me"


def blocked_network(*_args: object, **_kwargs: object) -> None:
    raise AssertionError("G-SEC-2 synthetic barrier validation must not open a network socket.")


def rejection_reason(case: dict[str, object]) -> str | None:
    if case.get("brand") != EXPECTED_BRAND:
        return "brand_not_allowed"
    if case.get("data_class") != ALLOWED_DATA_CLASS:
        return "data_class_not_allowed"
    if case.get("destination") != ALLOWED_DESTINATION:
        return "external_or_persistent_destination_not_allowed"
    if case.get("execution") != ALLOWED_EXECUTION or case.get("automation") is not False:
        return "automation_or_nonmanual_execution_not_allowed"
    if case.get("network") is not False:
        return "network_not_allowed"
    if case.get("financial") is not False:
        return "financial_data_not_allowed"
    return None


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert payload == json.loads(FIXTURE.read_text(encoding="utf-8")), "fixture must be immutable during validation"
    assert payload.get("synthetic") is True, "fixture must be explicitly synthetic"
    assert payload.get("brand") == EXPECTED_BRAND, "fixture brand must be Universe Sent Me"
    cases = payload.get("cases")
    assert isinstance(cases, list) and cases, "fixture must contain synthetic cases"

    results: dict[str, str] = {}
    with patch.object(socket, "socket", side_effect=blocked_network):
        try:
            socket.socket()
        except AssertionError:
            results["socket_guard"] = "blocked_as_designed"
        else:
            raise AssertionError("socket guard did not block")

        for case in cases:
            assert isinstance(case, dict), "every synthetic case must be an object"
            name = case.get("name")
            assert isinstance(name, str) and name, "every synthetic case needs a name"
            reason = rejection_reason(case)
            if name == "manual_local_minimum_allowed":
                assert reason is None, f"{name} must be allowed: {reason}"
                results[name] = "allowed_synthetic_only"
            else:
                assert reason is not None, f"{name} must be rejected"
                results[name] = reason

    expected_rejections = {
        "external_egress_blocked": "external_or_persistent_destination_not_allowed",
        "scheduler_blocked": "automation_or_nonmanual_execution_not_allowed",
        "private_evidence_blocked": "data_class_not_allowed",
        "network_blocked": "network_not_allowed",
        "financial_metric_blocked": "financial_data_not_allowed",
        "cross_brand_blocked": "brand_not_allowed",
    }
    for name, expected in expected_rejections.items():
        assert results.get(name) == expected, f"{name} rejection differs: {results.get(name)}"

    print(
        json.dumps(
            {
                "status": "gsec2_synthetic_barriers_passed",
                "allowed_case": "manual_local_minimum_allowed",
                "blocked_cases": expected_rejections,
                "guarantees": [
                    "synthetic_fixture_only",
                    "network_socket_blocked",
                    "no_collector_import",
                    "no_private_path_or_environment_read",
                    "no_ledger_evidence_or_canonical_write",
                    "no_scheduler_or_service_start",
                ],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
