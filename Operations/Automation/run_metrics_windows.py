#!/usr/bin/env python3
"""Capture due E24/E72 Meta windows from valid E0 rows.

This worker is deliberately separate from scheduling. It can be run from a
controlled cron/service later, but it does not create a schedule itself.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import record_metrics_snapshot as capture  # noqa: E402


WINDOWS = (("snapshot_24h", 3600), ("snapshot_72h", 3600))


@contextmanager
def ledger_lock(ledger: Path):
    lock_path = ledger.with_suffix(ledger.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f"ledger is locked by another worker: {lock_path}") from exc
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    try:
        lock_path.unlink()
    except FileNotFoundError:
        pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--now", help="Current UTC timestamp for deterministic replay")
    parser.add_argument("--ledger", type=Path, default=capture.DEFAULT_LEDGER)
    parser.add_argument("--raw-dir", type=Path, default=capture.DEFAULT_RAW_DIR)
    parser.add_argument("--payload-dir", type=Path, help="Optional replay directory; expects <Meta_Post_ID>_<Snapshot_Type>.json wrappers.")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    now = capture.parse_dt(args.now) if args.now else datetime.now(timezone.utc)
    assert now is not None
    run_id = args.run_id or now.strftime("%Y%m%dT%H%M%SZ")
    report: dict[str, object] = {
        "run_id": run_id,
        "now_utc": capture.iso(now),
        "ledger": str(args.ledger),
        "dry_run": args.dry_run,
        "candidates": [],
        "recorded": [],
        "no_op": [],
        "not_due": [],
        "errors": [],
    }

    try:
        with ledger_lock(args.ledger):
            rows = capture.read_rows(args.ledger)
            e0_rows = [row for row in rows if row.get("Window_Status") == "Valid_E0"]
            for e0 in e0_rows:
                published = capture.parse_dt(e0.get("Published_At_UTC"))
                meta_post_id = e0.get("Meta_Post_ID", "").strip()
                if not published or not meta_post_id:
                    report["errors"].append({"reason": "invalid_e0_identity", "snapshot_id": e0.get("Snapshot_ID", "")})
                    continue
                for snapshot_type, tolerance in WINDOWS:
                    target = capture.target_for(snapshot_type, published)
                    assert target is not None
                    logical_key = f"{meta_post_id}+{snapshot_type}"
                    existing = capture.valid_row_for(rows, logical_key)
                    distance = abs((now - target).total_seconds())
                    candidate = {
                        "meta_post_id": meta_post_id,
                        "snapshot_type": snapshot_type,
                        "target_at_utc": capture.iso(target),
                        "distance_seconds": round(distance, 3),
                    }
                    if existing:
                        report["no_op"].append({**candidate, "snapshot_id": existing.get("Snapshot_ID", "")})
                        continue
                    if distance > tolerance:
                        report["not_due"].append({**candidate, "reason": "outside_tolerance"})
                        continue
                    report["candidates"].append(candidate)
                    if args.dry_run:
                        continue
                    try:
                        replay_path = args.payload_dir / f"{meta_post_id}_{snapshot_type}.json" if args.payload_dir else None
                        if replay_path and replay_path.exists():
                            wrapper = json.loads(replay_path.read_text(encoding="utf-8"))
                            if isinstance(wrapper, dict) and isinstance(wrapper.get("payload"), dict):
                                payload = wrapper["payload"]
                                http_status = int(wrapper.get("http_status", 200))
                            else:
                                payload = wrapper
                                http_status = 200
                        else:
                            if args.payload_dir:
                                report["errors"].append({**candidate, "reason": "replay_payload_missing", "path": str(replay_path)})
                                continue
                            token = os.environ.get("META_PAGE_ACCESS_TOKEN")
                            if not token:
                                report["errors"].append({**candidate, "reason": "META_PAGE_ACCESS_TOKEN_missing"})
                                continue
                            payload, http_status = capture.fetch_meta_payload(meta_post_id, token)
                        args.raw_dir.mkdir(parents=True, exist_ok=True)
                        raw_path = args.raw_dir / f"{meta_post_id}_{snapshot_type}_{now.strftime('%Y%m%dT%H%M%SZ')}.json"
                        raw_record = {
                            "captured_at_utc": capture.iso(now),
                            "meta_post_id": meta_post_id,
                            "snapshot_type": snapshot_type,
                            "http_status": http_status,
                            "payload": payload,
                            "worker_run_id": run_id,
                        }
                        raw_path.write_text(json.dumps(raw_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                        row = capture.make_snapshot_row(
                            payload=payload,
                            http_status=http_status,
                            snapshot_type=snapshot_type,
                            meta_post_id=meta_post_id,
                            publicacion_id=e0.get("Publicacion_ID", ""),
                            experiment_id=e0.get("Experiment_ID", ""),
                            id_pieza=e0.get("ID_Pieza", ""),
                            cnt=e0.get("CNT", ""),
                            platform=e0.get("Plataforma", "Facebook"),
                            account_id=e0.get("Cuenta_ID", capture.DEFAULT_ACCOUNT_ID),
                            meta_photo_id=e0.get("Meta_Photo_ID", ""),
                            reel_id=e0.get("Reel_ID", ""),
                            published_override=published,
                            captured=now,
                            tolerance=tolerance,
                            source="Meta_Graph_API",
                            raw_path=capture.relative_or_absolute(raw_path),
                            existing_rows=rows,
                            notes=f"Window worker run {run_id}.",
                            run_id=run_id,
                        )
                        capture.append_row(args.ledger, row)
                        rows.append(row)
                        report["recorded"].append({**candidate, "snapshot_id": row["Snapshot_ID"], "window_status": row["Window_Status"]})
                    except Exception as exc:
                        report["errors"].append({**candidate, "reason": type(exc).__name__, "message": str(exc)})
    except Exception as exc:
        report["errors"].append({"reason": type(exc).__name__, "message": str(exc)})
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    report["status"] = "PASS" if not report["errors"] else "PARTIAL"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not report["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
