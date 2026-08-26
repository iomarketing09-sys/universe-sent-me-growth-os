#!/usr/bin/env python3
"""Run a private, bounded G-NORM-3 coverage pilot on local USM evidence.

The utility reads only the most recent local evidence file for each supported
platform, maps at most eight source records per platform in memory, and emits a
coverage-only report. It makes no network requests and never writes normalized
rows, ledgers, Sheets, OmniRoute payloads, or source evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from normalize_metrics_dry_run import BRAND, NORMALIZER_VERSION, observation_key, validate_row


EVIDENCE_PATTERNS = {
    "facebook": "*_Facebook_Official_Metrics.json",
    "instagram": "*_Instagram_Official_Metrics.json",
    "tiktok": "*_TikTok_Official_Metrics.json",
    "youtube": "*_YouTube_Official_Metrics.json",
}
PLATFORM_LABELS = {
    "facebook": "Facebook",
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "youtube": "YouTube",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def latest_evidence(directory: Path, pattern: str) -> Path | None:
    candidates = sorted(directory.glob(pattern), key=lambda candidate: candidate.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def utc_from_epoch(value: Any) -> str | None:
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (TypeError, ValueError, OSError, OverflowError):
        return None


def make_row(
    *,
    platform: str,
    content_id: Any,
    metric_name: str,
    metric_value: Any,
    metric_unit: str,
    metric_definition: str,
    window_type: str,
    published_at_utc: str | None,
    observed_at_utc: str,
    source_system: str,
    source_endpoint: str,
    evidence_fingerprint: str,
    window_start_utc: str | None = None,
    window_end_utc: str | None = None,
) -> dict[str, Any]:
    available = metric_value is not None
    return {
        "brand": BRAND,
        "platform": platform,
        "target_account_confirmed": True,
        "entity_scope": "content",
        "platform_content_id": str(content_id) if content_id is not None else None,
        "metric_name": metric_name,
        "metric_value": metric_value if available else None,
        "metric_unit": metric_unit,
        "metric_definition": metric_definition,
        "window_type": window_type,
        "window_start_utc": window_start_utc,
        "window_end_utc": window_end_utc,
        "published_at_utc": published_at_utc,
        "observed_at_utc": observed_at_utc,
        "source_system": source_system,
        "source_endpoint": source_endpoint,
        "source_schema_version": "private-pilot-v1",
        "availability_status": "available" if available else "not_available",
        "availability_reason": None if available else "field_not_returned_or_null",
        "comparability_tier": "C1_same_platform_observed" if window_type == "lifetime_at_capture" else "C0_not_comparable",
        "evidence_fingerprint": evidence_fingerprint,
        "publication_ref": None,
        "concept_id": None,
        "cnt_id": None,
        "experiment_id": None,
        "hypothesis_id": None,
    }


def adapt_facebook(payload: dict[str, Any], fingerprint: str, limit: int) -> Iterable[dict[str, Any]]:
    observed = str(payload.get("captured_at_utc", ""))
    for record in payload.get("records", [])[:limit]:
        for source_field, metric_name in (("reactions", "reactions_native"), ("comments", "comments_native"), ("shares", "shares_native")):
            yield make_row(
                platform="facebook",
                content_id=record.get("id"),
                metric_name=metric_name,
                metric_value=record.get(source_field),
                metric_unit="count",
                metric_definition=f"Meta Graph API Page Feed {source_field} counter at capture.",
                window_type="lifetime_at_capture",
                published_at_utc=record.get("created_time"),
                observed_at_utc=observed,
                source_system="meta_graph_api",
                source_endpoint="page_feed",
                evidence_fingerprint=fingerprint,
            )


def adapt_instagram(payload: dict[str, Any], fingerprint: str, limit: int) -> Iterable[dict[str, Any]]:
    observed = str(payload.get("captured_at_utc", ""))
    mapping = (
        ("like_count", "likes_native"),
        ("comments_count", "comments_native"),
        ("saved_count", "saves_native"),
        ("shares_count", "shares_native"),
        ("total_views_count", "views_native"),
        ("reposts_count", "reposts_native"),
    )
    for record in payload.get("records", [])[:limit]:
        for source_field, metric_name in mapping:
            yield make_row(
                platform="instagram",
                content_id=record.get("id"),
                metric_name=metric_name,
                metric_value=record.get(source_field),
                metric_unit="count",
                metric_definition=f"Meta Graph API Instagram Professional {source_field} at capture.",
                window_type="lifetime_at_capture",
                published_at_utc=record.get("timestamp"),
                observed_at_utc=observed,
                source_system="meta_graph_api",
                source_endpoint="instagram_media",
                evidence_fingerprint=fingerprint,
            )


def adapt_tiktok(payload: dict[str, Any], fingerprint: str, limit: int) -> Iterable[dict[str, Any]]:
    observed = str(payload.get("captured_at_utc", ""))
    mapping = (
        ("view_count", "views_native"),
        ("like_count", "likes_native"),
        ("comment_count", "comments_native"),
        ("share_count", "shares_native"),
    )
    for record in payload.get("videos", [])[:limit]:
        for source_field, metric_name in mapping:
            yield make_row(
                platform="tiktok",
                content_id=record.get("id"),
                metric_name=metric_name,
                metric_value=record.get(source_field),
                metric_unit="count",
                metric_definition=f"TikTok Display API video/list {source_field} at capture.",
                window_type="lifetime_at_capture",
                published_at_utc=utc_from_epoch(record.get("create_time")),
                observed_at_utc=observed,
                source_system="tiktok_display_api",
                source_endpoint="video_list",
                evidence_fingerprint=fingerprint,
            )


def adapt_youtube(payload: dict[str, Any], fingerprint: str, limit: int) -> Iterable[dict[str, Any]]:
    observed = str(payload.get("captured_at_utc", ""))
    mapping = (
        ("views", "views_native", "count"),
        ("engagedViews", "engaged_views_native", "count"),
        ("likes", "likes_native", "count"),
        ("comments", "comments_native", "count"),
        ("shares", "shares_native", "count"),
        ("estimatedMinutesWatched", "estimated_watch_minutes_native", "minutes"),
        ("averageViewDuration", "average_watch_time_seconds_native", "seconds"),
        ("averageViewPercentage", "average_view_percentage_native", "percentage"),
        ("subscribersGained", "subscribers_gained_native", "count"),
    )
    for record in payload.get("performance_rows", [])[:limit]:
        for source_field, metric_name, unit in mapping:
            yield make_row(
                platform="youtube",
                content_id=record.get("video"),
                metric_name=metric_name,
                metric_value=record.get(source_field),
                metric_unit=unit,
                metric_definition=f"YouTube Analytics {source_field} for requested closed period.",
                window_type="period_total",
                published_at_utc=None,
                observed_at_utc=observed,
                source_system="youtube_analytics_api",
                source_endpoint="reports_query",
                evidence_fingerprint=fingerprint,
                window_start_utc=str(payload.get("window_start", "")) + "T00:00:00Z",
                window_end_utc=str(payload.get("window_end", "")) + "T23:59:59Z",
            )


ADAPTERS = {
    "facebook": adapt_facebook,
    "instagram": adapt_instagram,
    "tiktok": adapt_tiktok,
    "youtube": adapt_youtube,
}


def source_records(payload: dict[str, Any], platform: str) -> list[dict[str, Any]]:
    if platform == "tiktok":
        return payload.get("videos", [])
    if platform == "youtube":
        return payload.get("performance_rows", [])
    return payload.get("records", [])


def assess_platform(platform: str, evidence_path: Path, limit: int) -> dict[str, Any]:
    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    if payload.get("brand") != BRAND or str(payload.get("platform", "")).lower() != PLATFORM_LABELS[platform].lower():
        return {"status": "blocked", "reason": "brand_or_platform_mismatch"}
    if platform in {"facebook", "instagram"} and payload.get("status") != "collected":
        return {"status": "blocked", "reason": "source_not_collected"}
    raw_rows = source_records(payload, platform)
    fingerprint = sha256_file(evidence_path)
    rows = list(ADAPTERS[platform](payload, fingerprint, limit))
    validation_counts: Counter[str] = Counter()
    availability: Counter[str] = Counter()
    metric_coverage: dict[str, Counter[str]] = defaultdict(Counter)
    keys: set[str] = set()
    for row in rows:
        errors = validate_row(row)
        key = observation_key(row)
        if key in keys:
            validation_counts["duplicate_skip"] += 1
            continue
        keys.add(key)
        if errors:
            validation_counts["rejected"] += 1
            continue
        status = "partial" if row["availability_status"] != "available" else "valid"
        validation_counts[status] += 1
        availability[row["availability_status"]] += 1
        metric_coverage[row["metric_name"]][row["availability_status"]] += 1
    return {
        "status": "coverage_complete",
        "source_records_available": len(raw_rows),
        "sample_records_processed": min(len(raw_rows), limit),
        "normalized_observations_in_memory": len(rows),
        "validation_counts": dict(sorted(validation_counts.items())),
        "availability_counts": dict(sorted(availability.items())),
        "metric_coverage": {metric: dict(sorted(counts.items())) for metric, counts in sorted(metric_coverage.items())},
        "financial_evidence_excluded": platform == "youtube",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, default=Path("~/.local/share/usm-metrics/evidence").expanduser())
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.sample_limit <= 8:
        raise SystemExit("--sample-limit must be between 1 and 8 for G-NORM-3.")
    directory = args.evidence_dir.expanduser().resolve()
    report: dict[str, Any] = {
        "status": "private_pilot_coverage_complete",
        "mode": "G-NORM-3_private_in_memory_no_write",
        "brand": BRAND,
        "sample_limit_per_platform": args.sample_limit,
        "platform_coverage": {},
        "guarantees": [
            "No network requests were made.",
            "No normalized observations or source evidence were written.",
            "No IDs, captions, URLs, paths, tokens, raw values, or monetary amounts are printed.",
            "YouTube monetization evidence is excluded from the pilot.",
        ],
    }
    for platform, pattern in EVIDENCE_PATTERNS.items():
        path = latest_evidence(directory, pattern)
        report["platform_coverage"][platform] = (
            {"status": "blocked", "reason": "evidence_not_found"}
            if path is None
            else assess_platform(platform, path, args.sample_limit)
        )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
