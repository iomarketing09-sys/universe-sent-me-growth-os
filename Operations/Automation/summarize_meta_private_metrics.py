#!/usr/bin/env python3
"""Print a safe aggregate-only summary of the latest private Meta evidence.

Design reminder: this utility is read-only. It does not display record IDs,
captions, URLs, people, paths, tokens or raw records, and does not write files.
"""

from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any


FILES = {
    "facebook": "Facebook_Official_Metrics.json",
    "instagram": "Instagram_Official_Metrics.json",
}


def latest_evidence(evidence_dir: Path, suffix: str) -> Path:
    candidates = [path for path in evidence_dir.glob(f"*_{suffix}") if path.is_file()]
    if not candidates:
        raise FileNotFoundError(f"No private evidence file found for {suffix}.")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def numeric(values: list[Any]) -> list[float]:
    return [float(value) for value in values if isinstance(value, (int, float)) and not isinstance(value, bool)]


def metric_summary(records: list[dict[str, Any]], field: str) -> dict[str, int | float | None]:
    values = numeric([record.get(field) for record in records])
    return {
        "available_records": len(values),
        "unavailable_records": len(records) - len(values),
        "total_available": int(sum(values)) if values else None,
        "median_available": round(statistics.median(values), 2) if values else None,
    }


def date_window(records: list[dict[str, Any]], field: str) -> dict[str, str | None]:
    values = sorted(str(record[field]) for record in records if record.get(field))
    return {"from": values[0] if values else None, "to": values[-1] if values else None}


def count_by(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = record.get(field)
        if isinstance(value, str) and value:
            counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("platform", choices=sorted(FILES))
    parser.add_argument("--evidence-dir", default="~/.local/share/usm-metrics/evidence")
    args = parser.parse_args()

    evidence_path = latest_evidence(Path(args.evidence_dir).expanduser(), FILES[args.platform])
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if payload.get("status") != "collected" or not isinstance(records, list):
        raise SystemExit("Latest evidence is not a collected records snapshot.")

    if args.platform == "facebook":
        output = {
            "brand": payload.get("brand"),
            "platform": "Facebook",
            "records": len(records),
            "published_window": date_window(records, "created_time"),
            "native_counters": {
                "reactions": metric_summary(records, "reactions"),
                "comments": metric_summary(records, "comments"),
                "shares": metric_summary(records, "shares"),
            },
            "note": "Counters are lifetime values at capture. Missing values are reported as unavailable, not zero.",
        }
    else:
        fields = [
            "like_count", "comments_count", "saved_count", "shares_count", "total_like_count",
            "total_comments_count", "total_views_count", "reposts_count",
        ]
        output = {
            "brand": payload.get("brand"),
            "platform": "Instagram",
            "records": len(records),
            "published_window": date_window(records, "timestamp"),
            "media_types": count_by(records, "media_type"),
            "media_product_types": count_by(records, "media_product_type"),
            "native_counters": {field: metric_summary(records, field) for field in fields},
            "note": "Counters are lifetime native values at capture. Missing values are reported as unavailable, not zero.",
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
