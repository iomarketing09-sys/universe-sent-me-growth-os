#!/usr/bin/env python3
"""Run a fully isolated E0 -> E24 -> E72 pipeline simulation.

This never calls Meta and never writes the production snapshot ledger. It uses
an explicitly synthetic test post with Meta-shaped payloads to exercise the
same adapter, worker, validator, idempotency, raw evidence and delta logic.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "Operations/Automation/capture_e0_after_publish.py"
WORKER = ROOT / "Operations/Automation/run_metrics_windows.py"
VALIDATOR = ROOT / "Operations/Automation/validate_metrics_snapshot_ledger.py"
PRODUCT_LEDGER = ROOT / "Operations/Research/Metrics_Snapshot_Log.csv"


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def run(args: list[str]) -> dict:
    proc = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)
    return json.loads(proc.stdout)


def payload(post_id: str, created: datetime, reactions: int, comments: int, shares: int) -> dict:
    return {
        "created_time": iso(created),
        "id": post_id,
        "reactions": {"summary": {"total_count": reactions}},
        "comments": {"summary": {"total_count": comments}},
        "shares": {"count": shares},
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product-ledger", type=Path, default=PRODUCT_LEDGER)
    parser.add_argument("--published-at-utc", default="2026-08-25T15:00:00Z")
    parser.add_argument("--post-id", default="SIMULATED-POST-E0-E72-001")
    args = parser.parse_args()

    published = datetime.fromisoformat(args.published_at_utc.replace("Z", "+00:00")).astimezone(timezone.utc)
    before_hash = sha256(args.product_ledger)
    with tempfile.TemporaryDirectory(prefix="usm-e2e-simulation-") as temp:
        root = Path(temp)
        ledger = root / "Metrics_Snapshot_Log.csv"
        raw_dir = root / "raw"
        payload_dir = root / "payloads"
        payload_dir.mkdir()
        event_file = root / "publication_result.json"
        event_file.write_text(json.dumps({
            "meta_post_id": args.post_id,
            "publicacion_id": "SIM-PUBLICATION-E2E-001",
            "experiment_id": "SIM-EXPERIMENT-E2E-001",
            "id_pieza": "SIM-TEST-POST",
            "cnt": "SIM-TEST-POST",
            "is_published": True,
            "created_time": iso(published),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        for snapshot_type, moment, counts in [
            ("baseline_e0", published, (1, 2, 1)),
            ("snapshot_24h", published + timedelta(hours=24, minutes=5), (5, 4, 1)),
            ("snapshot_72h", published + timedelta(hours=72, minutes=5), (8, 7, 2)),
        ]:
            (payload_dir / f"{args.post_id}_{snapshot_type}.json").write_text(json.dumps({
                "http_status": 200,
                "payload": payload(args.post_id, published, *counts),
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        e0 = run([
            str(ADAPTER), "--publication-result", str(event_file), "--payload-file", str(payload_dir / f"{args.post_id}_baseline_e0.json"),
            "--captured-at-utc", iso(published), "--run-id", "SIM-E0-001", "--ledger", str(ledger), "--raw-dir", str(raw_dir),
        ])
        e0_retry = run([
            str(ADAPTER), "--publication-result", str(event_file), "--payload-file", str(payload_dir / f"{args.post_id}_baseline_e0.json"),
            "--captured-at-utc", iso(published), "--run-id", "SIM-E0-001-RETRY", "--ledger", str(ledger), "--raw-dir", str(raw_dir),
        ])
        e24_at = published + timedelta(hours=24, minutes=5)
        e24 = run([
            str(WORKER), "--now", iso(e24_at), "--run-id", "SIM-E24-001", "--ledger", str(ledger), "--raw-dir", str(raw_dir), "--payload-dir", str(payload_dir),
        ])
        e24_retry = run([
            str(WORKER), "--now", iso(e24_at), "--run-id", "SIM-E24-001-RETRY", "--ledger", str(ledger), "--raw-dir", str(raw_dir), "--payload-dir", str(payload_dir),
        ])
        e72_at = published + timedelta(hours=72, minutes=5)
        e72 = run([
            str(WORKER), "--now", iso(e72_at), "--run-id", "SIM-E72-001", "--ledger", str(ledger), "--raw-dir", str(raw_dir), "--payload-dir", str(payload_dir),
        ])
        e72_retry = run([
            str(WORKER), "--now", iso(e72_at), "--run-id", "SIM-E72-001-RETRY", "--ledger", str(ledger), "--raw-dir", str(raw_dir), "--payload-dir", str(payload_dir),
        ])
        validation = run([str(VALIDATOR), str(ledger), "--json"])
        with ledger.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        by_type = {row["Snapshot_Type"]: row for row in rows}
        expected = {
            "baseline_e0": {"Window_Status": "Valid_E0", "Lifetime_Interactions": "4", "Delta_From_E0": ""},
            "snapshot_24h": {"Window_Status": "Valid_24h", "Lifetime_Interactions": "10", "Delta_From_E0": "6"},
            "snapshot_72h": {"Window_Status": "Valid_72h", "Lifetime_Interactions": "17", "Delta_From_E0": "13"},
        }
        assertions = {}
        for snapshot_type, checks in expected.items():
            row = by_type.get(snapshot_type, {})
            assertions[snapshot_type] = all(row.get(key) == value for key, value in checks.items())
        after_hash = sha256(args.product_ledger)
        report = {
            "title": "Simulación aislada del pipeline E0 a E72",
            "simulation_id": "SIM-E0-E72-20260825-001",
            "post_id": args.post_id,
            "post_is_synthetic": True,
            "meta_api_called": False,
            "production_ledger_written": False,
            "production_ledger_sha256_before": before_hash,
            "production_ledger_sha256_after": after_hash,
            "production_ledger_unchanged": before_hash == after_hash,
            "temporary_ledger_rows": len(rows),
            "temporary_raw_files": len(list(raw_dir.glob("*.json"))),
            "steps": {
                "e0": e0,
                "e0_retry": e0_retry,
                "e24": e24,
                "e24_retry": e24_retry,
                "e72": e72,
                "e72_retry": e72_retry,
                "validator": validation,
            },
            "expected_values": {
                "E0": 4,
                "E24_lifetime": 10,
                "E24_delta": 6,
                "E72_lifetime": 17,
                "E72_delta": 13,
            },
            "assertions": assertions,
            "status": "PASS" if all(assertions.values()) and validation.get("VALIDATION") == "PASS" and before_hash == after_hash else "FAIL",
            "limitations": [
                "This is a local contract simulation; it does not create a real Meta post.",
                "Payload counters are synthetic fixtures using the Meta response shape; no production metric is inferred.",
                "The production ledger remains unchanged and must receive its first row only from a real publication event."
            ],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
