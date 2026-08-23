"""Validate Facebook temporal-window closure and Windsor Reel insight artifacts.

This validator is intentionally strict about metric semantics: lifetime snapshots
must not populate contractual 24h/72h fields, and only rows with a native Reel
ID may enter the video-insight table.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESEARCH = REPO / "Operations" / "Research"
SUMMARY = RESEARCH / "2026-08-23_Facebook_24_72_and_Video_Insights_Summary.json"
WINDOWS = RESEARCH / "2026-08-23_Facebook_24_72_Window_Closure.json"
INVENTORY = RESEARCH / "2026-08-21_Reels_Publication_Inventory.csv"
PUBLICATION_LOG = RESEARCH / "2026-08-15_Publication_Log.csv"
EXPERIMENT_LOG = RESEARCH / "2026-08-15_ExperimentLog.csv"
COMMUNITY_LOG = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"

EXPECTED_REELS = {
    "2815726225473165",
    "2005557463434064",
    "1581447113440863",
    "2210896633022235",
}
RUN_MARKER = "20260823T210000Z"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    windows = json.loads(WINDOWS.read_text(encoding="utf-8"))

    closure = summary.get("window_closure", {})
    expected_closure = {
        "candidate_count": 33,
        "eligible_count": 27,
        "eligible_24h_windows": 22,
        "eligible_72h_windows": 20,
        "exact_window_writes": 0,
        "status": "Unavailable_No_Baseline",
    }
    for key, expected in expected_closure.items():
        if closure.get(key) != expected:
            fail(errors, f"window_closure.{key}={closure.get(key)!r}; expected {expected!r}")
    eligible_candidates = [candidate for candidate in windows.get("candidates", []) if candidate.get("due_windows")]
    evidence_flags = [
        (candidate.get("evidence") or {}).get("exact_window_available")
        for candidate in eligible_candidates
    ]
    if len(evidence_flags) != 27 or any(flag is not False for flag in evidence_flags):
        fail(errors, "eligible source evidence does not mark all 27 windows exact_window_available=false")
    if windows.get("exact_window_writes") != 0:
        fail(errors, "source window evidence reports non-zero exact_window_writes")

    records = summary.get("video_insights", {}).get("records", [])
    record_ids = [str(row.get("reel_id")) for row in records]
    if set(record_ids) != EXPECTED_REELS:
        fail(errors, f"Reel IDs in summary={sorted(record_ids)!r}; expected {sorted(EXPECTED_REELS)!r}")
    if len(record_ids) != len(set(record_ids)):
        fail(errors, "duplicate Reel IDs in summary")
    fetched_at = {row.get("data_fetched_at_utc") for row in records}
    if fetched_at != {"2026-08-23T21:02:08"}:
        fail(errors, f"unexpected Windsor fetch timestamps: {sorted(fetched_at)!r}")
    for row in records:
        if row.get("metric_window_type") != "lifetime_actual":
            fail(errors, f"Reel {row.get('reel_id')} is not labelled lifetime_actual")
        if row.get("metric_source") != "Windsor_facebook_organic":
            fail(errors, f"Reel {row.get('reel_id')} has unexpected source")
        if not row.get("page_post_id"):
            fail(errors, f"Reel {row.get('reel_id')} has no Page Post ID")
        if not row.get("reels_post_impressions_unique"):
            fail(errors, f"Reel {row.get('reel_id')} has no positive discovery metric")
        if row.get("video_length_seconds") and row.get("average_watch_time_seconds"):
            share = row.get("average_watch_as_share_of_length")
            if share is None or not 0 < share <= 1:
                fail(errors, f"Reel {row.get('reel_id')} has invalid descriptive watch share {share!r}")

    for path in (PUBLICATION_LOG, EXPERIMENT_LOG):
        fields, rows = read_csv(path)
        for required in ("Interacciones_24h", "Interacciones_72h"):
            if required not in fields:
                fail(errors, f"{path.name} missing {required}")
        for row in rows:
            text = " ".join(row.values())
            if RUN_MARKER not in text:
                continue
            if "24h_snapshot_unavailable" in text and row.get("Interacciones_24h", "").strip():
                fail(errors, f"{path.name} writes 24h value on unavailable run for {row.get('Meta_Post_ID') or row.get('Meta_ID')}")
            if "72h_snapshot_unavailable" in text and row.get("Interacciones_72h", "").strip():
                fail(errors, f"{path.name} writes 72h value on unavailable run for {row.get('Meta_Post_ID') or row.get('Meta_ID')}")

    fields, rows = read_csv(INVENTORY)
    for required in ("Meta_Reel_ID", "Metrics_Status", "Views", "Reach", "Source", "Last_Sync"):
        if required not in fields:
            fail(errors, f"inventory missing {required}")
    matching = [row for row in rows if row.get("Meta_Reel_ID") in EXPECTED_REELS]
    if {row.get("Meta_Reel_ID") for row in matching} != EXPECTED_REELS:
        fail(errors, "inventory does not contain exactly one row for each expected Reel")
    if len(matching) != len(EXPECTED_REELS):
        fail(errors, "inventory contains duplicate rows for one of the expected Reel IDs")
    for row in matching:
        status = row.get("Metrics_Status", "")
        if "Windsor_lifetime_snapshot_2026-08-23" not in status:
            fail(errors, f"inventory Reel {row.get('Meta_Reel_ID')} lacks Windsor snapshot label")
        if "24h_72h_pending" not in status:
            fail(errors, f"inventory Reel {row.get('Meta_Reel_ID')} lacks pending 24/72 label")
        if "Interacciones_24h" in status or "Interacciones_72h" in status:
            fail(errors, f"inventory Reel {row.get('Meta_Reel_ID')} appears to store exact temporal values")

    community_fields, community_rows = read_csv(COMMUNITY_LOG)
    if not community_fields or not community_rows:
        fail(errors, "community engagement ledger is empty or missing a header")
    if "Comentario_ID" not in community_fields or "Respuesta_Estado" not in community_fields:
        fail(errors, "community engagement ledger failed standard shape check")

    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({
        "status": "PASS",
        "window_closure": "27 eligible; 22 x 24h; 20 x 72h; 0 exact writes; no baseline",
        "reel_insights": 4,
        "inventory_rows_checked": len(matching),
        "community_ledger": "shape_and_nonempty_pass",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
