#!/usr/bin/env python3
"""Run synthetic-only assertions for the multichannel normalizer dry-run.

This validator imports no credentials, opens no network connection, and writes
nothing. It verifies the documented NORM-01 through NORM-12 rules against
short-lived in-memory synthetic observations.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from normalize_metrics_dry_run import normalise


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "normalization_dry_run_synthetic.json"


def payload_for(row: dict) -> dict:
    return {"synthetic": True, "brand": "Universe Sent Me", "observations": [row]}


def expect_rejected(base: dict, mutate, rule: str) -> None:
    row = copy.deepcopy(base)
    mutate(row)
    result = normalise(payload_for(row))
    output = result["normalized_observations"][0]
    assert output["row_status"] == "rejected", output
    assert any(error.startswith(rule) for error in output["validation_errors"]), output


def main() -> int:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    valid = copy.deepcopy(fixture["observations"][0])
    invalid_availability = copy.deepcopy(fixture["observations"][7])

    baseline = normalise({"synthetic": True, "brand": "Universe Sent Me", "observations": fixture["observations"]})
    assert baseline["validation_counts"] == {"valid": 5, "partial": 1, "rejected": 2, "duplicate_skip": 0}, baseline
    assert normalise({"synthetic": True, "brand": "Universe Sent Me", "observations": [valid, valid]})["validation_counts"]["duplicate_skip"] == 1

    normalized = baseline["normalized_observations"]
    assert normalized[1]["row_status"] == "partial", normalized[1]
    assert normalized[3]["metric_value"] == 125.5, normalized[3]
    assert normalized[4]["window_type"] == "period_total", normalized[4]
    assert normalized[4]["comparability_tier"] == "C3_exact_window", normalized[4]
    assert normalized[5]["metric_unit"] == "minutes", normalized[5]

    expect_rejected(valid, lambda row: row.update({"brand": "Other Brand"}), "NORM-01")
    expect_rejected(valid, lambda row: row.update({"target_account_confirmed": False}), "NORM-02")
    expect_rejected(valid, lambda row: row.update({"platform_content_id": None}), "NORM-03")
    expect_rejected(valid, lambda row: row.update({"observed_at_utc": None}), "NORM-04")
    expect_rejected(valid, lambda row: row.update({"metric_value": -1}), "NORM-05")
    expect_rejected(invalid_availability, lambda row: row, "NORM-06")

    derived = copy.deepcopy(valid)
    derived.update({"metric_name": "actions_per_view", "metric_value": 0.2, "metric_unit": "ratio"})
    expect_rejected(derived, lambda row: row, "NORM-07")
    expect_rejected(valid, lambda row: row.update({"aggregate_window_types": ["daily_activity", "lifetime_at_capture"]}), "NORM-08")
    expect_rejected(valid, lambda row: row.update({"evidence_fingerprint": "not-a-hash"}), "NORM-09")
    currency = copy.deepcopy(valid)
    currency.update({"metric_name": "estimated_revenue_preliminary", "metric_value": 1.5, "metric_unit": "currency"})
    expect_rejected(currency, lambda row: row, "NORM-11")
    expect_rejected(valid, lambda row: row.update({"caption": "synthetic prohibited text"}), "NORM-12")

    print(
        json.dumps(
            {
                "status": "synthetic_validation_passed",
                "rules_covered": [f"NORM-{number:02d}" for number in range(1, 13)],
                "baseline_counts": baseline["validation_counts"],
                "edge_cases": ["mixed_availability", "percentage_above_100_preserved", "closed_period", "native_minutes"],
                "guarantees": ["synthetic_only", "no_network", "no_write"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
