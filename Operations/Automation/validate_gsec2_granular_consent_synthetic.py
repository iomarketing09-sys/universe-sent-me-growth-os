#!/usr/bin/env python3
"""Validate fictional one-operation consent-card policy only.

This program does not request, collect, record, or verify a person's real
consent. It reads a public fictional fixture and checks completeness rules in
memory. It never imports collectors, reads private paths or environment
variables, opens a socket, calls an API, starts work, or writes any record.
"""

from __future__ import annotations

import json
import socket
from pathlib import Path
from unittest.mock import patch


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "gsec2_granular_consent_card_synthetic.json"
EXPECTED_METRICS = {
    "TikTok": "views_native",
    "YouTube": "views_native_closed_period",
    "Facebook": "reactions_native",
    "Instagram": "likes_native",
}
FORBIDDEN_FIELDS = {"token", "secret", "identifier", "evidence", "raw_response", "content", "url"}


def blocked_network(*_args: object, **_kwargs: object) -> None:
    raise AssertionError("G-SEC-2.4a must not open a network socket.")


def rejection_reason(card: dict[str, object]) -> str | None:
    if not isinstance(card.get("reference"), str) or not card["reference"]:
        return "missing_reference"
    if card.get("brand") != "Universe Sent Me":
        return "brand_not_allowed"
    if card.get("sample_size") != 4 or card.get("metrics") != EXPECTED_METRICS:
        return "scope_or_metric_contract_not_allowed"
    if card.get("retention_days") != 30:
        return "retention_contract_not_allowed"
    if card.get("execution") != "manual_read_only_once":
        return "execution_not_single_manual_read_only"
    if card.get("external_egress") is not False:
        return "external_egress_not_allowed"
    if card.get("validity_hours") != 24 or card.get("revocable") is not True:
        return "validity_or_revocation_not_allowed"
    if card.get("result_output") != "aggregate_safe_status_only":
        return "unsafe_result_output"
    if card.get("real_data") is not False:
        return "real_data_not_allowed_in_synthetic_fixture"
    if card.get("synthetic_approval_marker") is not True:
        return "synthetic_approval_marker_missing"
    if FORBIDDEN_FIELDS.intersection(card):
        return "forbidden_sensitive_field_present"
    return None


def main() -> int:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert payload == json.loads(FIXTURE.read_text(encoding="utf-8")), "fixture must not change during validation"
    assert payload.get("synthetic") is True, "fixture must be explicitly synthetic"
    assert payload.get("required_metrics") == EXPECTED_METRICS, "fixture contract metrics differ"
    cases = payload.get("cases")
    assert isinstance(cases, list) and cases, "fixture needs fictional card cases"

    results: dict[str, str] = {}
    with patch.object(socket, "socket", side_effect=blocked_network):
        try:
            socket.socket()
        except AssertionError:
            results["socket_guard"] = "blocked_as_designed"
        else:
            raise AssertionError("socket guard did not block")

        for card in cases:
            assert isinstance(card, dict), "every card must be an object"
            name = card.get("name")
            assert isinstance(name, str) and name, "every card requires a name"
            reason = rejection_reason(card)
            if name == "complete_single_operation_card_allowed":
                assert reason is None, f"{name} must be allowed: {reason}"
                results[name] = "allowed_synthetic_only"
            else:
                assert reason is not None, f"{name} must be rejected"
                results[name] = reason

    expected_rejections = {
        "missing_reference_blocked": "missing_reference",
        "scope_expansion_blocked": "scope_or_metric_contract_not_allowed",
        "financial_metric_blocked": "scope_or_metric_contract_not_allowed",
        "retention_extension_blocked": "retention_contract_not_allowed",
        "non_readonly_execution_blocked": "execution_not_single_manual_read_only",
        "external_egress_blocked": "external_egress_not_allowed",
        "expired_or_nonrevocable_card_blocked": "validity_or_revocation_not_allowed",
        "real_data_or_identifier_field_blocked": "real_data_not_allowed_in_synthetic_fixture",
    }
    for name, expected in expected_rejections.items():
        assert results.get(name) == expected, f"{name} differs: {results.get(name)}"

    print(json.dumps({
        "status": "gsec2_granular_consent_synthetic_passed",
        "allowed_case": "complete_single_operation_card_allowed",
        "blocked_cases": expected_rejections,
        "guarantees": [
            "fictional_consent_card_only_not_real_consent",
            "network_socket_blocked",
            "no_collector_import",
            "no_private_path_or_environment_read",
            "no_ledger_evidence_or_external_write",
            "no_operation_authorization_created",
        ],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
