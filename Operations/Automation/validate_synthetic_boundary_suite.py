#!/usr/bin/env python3
"""Run the synthetic normalizer and shadow-ledger boundaries in a no-network process.

This file is intentionally fixture-only. It creates a temporary ledger through
the existing validator and exits without emitting normalized rows or a path.
"""

from __future__ import annotations

import io
import json
import socket
from contextlib import redirect_stdout
from unittest.mock import patch

import validate_normalization_dry_run
import validate_shadow_ledger_synthetic


def run_validator(main_func) -> dict:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        exit_code = main_func()
    assert exit_code == 0
    return json.loads(buffer.getvalue())


def block_network(*_args, **_kwargs):
    raise AssertionError("Synthetic boundary suite must not open a network socket.")


def main() -> int:
    with patch.object(socket, "socket", side_effect=block_network):
        normalizer = run_validator(validate_normalization_dry_run.main)
        ledger = run_validator(validate_shadow_ledger_synthetic.main)

    assert normalizer["status"] == "synthetic_validation_passed", normalizer
    assert ledger["status"] == "shadow_ledger_synthetic_validation_passed", ledger
    print(
        json.dumps(
            {
                "status": "synthetic_boundary_suite_passed",
                "normalizer_rules": normalizer["rules_covered"],
                "normalizer_edge_cases": normalizer["edge_cases"],
                "ledger_tests": ledger["tests"],
                "guarantees": ["synthetic_only", "network_socket_blocked", "temporary_ledger_only", "no_canonical_write"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
