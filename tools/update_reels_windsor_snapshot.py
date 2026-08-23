"""Append source-labelled Windsor lifetime insights to the Facebook Reel inventory."""
from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INVENTORY = REPO / "Operations" / "Research" / "2026-08-21_Reels_Publication_Inventory.csv"
SUMMARY = REPO / "Operations" / "Research" / "2026-08-23_Facebook_24_72_and_Video_Insights_Summary.json"

SNAPSHOTS = {
    "2210896633022235": {
        "reach": 184,
        "plays": 203,
        "replays": 27,
        "avg_watch": "11.017s",
        "length": "13.403s",
        "watch_share": "0.822 descriptive",
        "complete": 8,
        "view_time": "0.5325h",
        "interactions": 2,
    },
    "2815726225473165": {
        "reach": 390,
        "plays": 451,
        "replays": 43,
        "avg_watch": "4.420s",
        "length": "30.133s",
        "watch_share": "0.1467 descriptive",
        "complete": 19,
        "view_time": "0.4973h",
        "interactions": 11,
    },
    "2005557463434064": {
        "reach": 252,
        "plays": 336,
        "replays": 79,
        "avg_watch": "5.621s",
        "length": "8.125s",
        "watch_share": "0.6918 descriptive",
        "complete": 38,
        "view_time": "0.3982h",
        "interactions": 13,
    },
    "1581447113440863": {
        "reach": 666,
        "plays": 706,
        "replays": 70,
        "avg_watch": "5.112s",
        "length": "29.458s",
        "watch_share": "0.1735 descriptive",
        "complete": 24,
        "view_time": "0.8919h",
        "interactions": 26,
    },
}

BASE_STATUS = "Windsor_lifetime_snapshot_2026-08-23; metric_window=lifetime_actual; source=Windsor_facebook_organic; reach=reels_post_impressions_unique; plays=fb_reels_total_plays; replays=fb_reels_replay_count; avg_watch={avg_watch}; length={length}; avg_watch_share_of_length={watch_share}; complete_views_organic_95pct_count={complete}; view_time={view_time}; Windsor_observable_interactions={interactions}; evidence=L2_Discovery+partial_watch_signals; retention_not_complete; 24h_72h_pending; fetched_at=2026-08-23T21:02:08; source_file=Operations/Research/2026-08-23_Facebook_Reels_Video_Insights.csv"
SOURCE_NOTE = "Operations/Research/2026-08-23_Facebook_Reels_Video_Insights.csv; Operations/Research/2026-08-23_Facebook_Windsor_Insights_Raw.json"


def main() -> int:
    with INVENTORY.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    if not fields:
        raise SystemExit("inventory has no header")

    matched = 0
    for row in rows:
        reel_id = row.get("Meta_Reel_ID", "")
        snapshot = SNAPSHOTS.get(reel_id)
        if not snapshot:
            continue
        matched += 1
        existing = row.get("Metrics_Status", "")
        # Idempotent replacement of only this run's generated Windsor block.
        prefix = "Windsor_lifetime_snapshot_2026-08-23;"
        if prefix in existing:
            existing = existing.split(prefix, 1)[0].rstrip(" ;")
        generated = BASE_STATUS.format(**snapshot)
        row["Metrics_Status"] = "; ".join(part for part in (existing, generated) if part)
        existing_source = row.get("Source", "")
        if SOURCE_NOTE not in existing_source:
            row["Source"] = "; ".join(part for part in (existing_source, SOURCE_NOTE) if part)
        row["Last_Sync"] = "2026-08-23"

    if matched != len(SNAPSHOTS):
        raise SystemExit(f"expected {len(SNAPSHOTS)} Reel rows, updated {matched}")

    temp = INVENTORY.with_suffix(".csv.tmp")
    with temp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(INVENTORY)
    print({"updated_reels": matched, "inventory": str(INVENTORY), "summary_reference": str(SUMMARY)})


if __name__ == "__main__":
    main()
