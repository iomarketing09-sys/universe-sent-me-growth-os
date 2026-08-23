#!/usr/bin/env python3
"""Summarize Facebook 24/72-hour closure evidence and Windsor video insights.

The script keeps exact temporal windows separate from lifetime snapshots. It never
writes lifetime metrics into 24h/72h fields and labels partial video evidence
explicitly when retention metrics are incomplete.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESEARCH = REPO / "Operations" / "Research"
WINDOWS = RESEARCH / "2026-08-23_Facebook_24_72_Window_Closure.json"
WINDSOR = RESEARCH / "2026-08-23_Facebook_Windsor_Insights_Raw.json"
OUT_JSON = RESEARCH / "2026-08-23_Facebook_24_72_and_Video_Insights_Summary.json"
OUT_CSV = RESEARCH / "2026-08-23_Facebook_Reels_Video_Insights.csv"


def num(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def round_or_none(value, digits=3):
    return round(value, digits) if isinstance(value, (int, float)) else None


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00").replace("+0000", "+00:00"))


def load_windsor_rows() -> list[dict]:
    raw = json.loads(WINDSOR.read_text(encoding="utf-8"))
    # The text payload contains the complete row shape; structuredContent can
    # omit optional fields such as length, post_message, or post_id.
    for item in raw.get("content", []):
        if item.get("type") != "text":
            continue
        try:
            parsed = json.loads(item.get("text", ""))
        except (TypeError, json.JSONDecodeError):
            continue
        if isinstance(parsed, list):
            return parsed
    structured = raw.get("structuredContent", {}).get("result", [])
    return structured if isinstance(structured, list) else []


def reels_rows(rows: list[dict], captured_at: datetime) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        reel_id = row.get("id")
        if not reel_id:
            continue
        created = parse_dt(row.get("post_created_time") or row.get("created_time"))
        length = num(row.get("length"))
        avg_ms = num(row.get("post_video_avg_time_watched"))
        view_ms = num(row.get("post_video_view_time"))
        impressions_unique = num(row.get("reels_post_impressions_unique"))
        play_count = num(row.get("blue_reels_play_count"))
        total_plays = num(row.get("fb_reels_total_plays"))
        replays = num(row.get("fb_reels_replay_count"))
        complete = num(row.get("post_video_complete_views_organic"))
        comments = num(row.get("post_video_social_actions_comment"))
        shares = num(row.get("post_video_social_actions_share"))
        reactions = num(row.get("post_video_total_reactions"))
        out.append({
            "reel_id": str(reel_id),
            "page_post_id": row.get("post_id"),
            "permalink": row.get("permalink_url"),
            "published_at_utc": created.isoformat() if created else None,
            "age_hours_at_capture": round_or_none((captured_at - created).total_seconds() / 3600, 3) if created else None,
            "metric_window_type": "lifetime_actual",
            "metric_source": "Windsor_facebook_organic",
            "post_impressions": num(row.get("post_impressions")),
            "post_impressions_unique": num(row.get("post_impressions_unique")),
            "reels_post_impressions_unique": impressions_unique,
            "blue_reels_play_count": play_count,
            "fb_reels_total_plays": total_plays,
            "fb_reels_replay_count": replays,
            "post_video_views_3s_or_nearly_all": num(row.get("post_video_views")),
            "average_watch_time_seconds": round_or_none(avg_ms / 1000, 3) if avg_ms is not None else None,
            "video_length_seconds": length,
            "average_watch_as_share_of_length": round_or_none((avg_ms / 1000) / length, 4) if avg_ms is not None and length else None,
            "complete_views_organic_95pct": complete,
            "view_time_hours": round_or_none(view_ms / 3_600_000, 4) if view_ms is not None else None,
            "comments": comments,
            "shares": shares,
            "reactions": reactions,
            "observable_interactions": round_or_none(sum(v for v in (comments, shares, reactions) if v is not None), 0),
            "discovery_evidence_status": "L2_Discovery" if impressions_unique and impressions_unique > 0 else "Unavailable",
            "video_evidence_status": "L2_plus_watch_signals_partial" if avg_ms is not None and view_ms is not None and complete is not None else "L2_only",
            "retention_status": "Not_complete_no_3s_or_completion_rate" if avg_ms is not None else "Unavailable",
            "data_fetched_at_utc": row.get("data_fetched_at"),
            "post_message": row.get("post_message"),
        })
    return out


def main() -> int:
    windows = json.loads(WINDOWS.read_text(encoding="utf-8"))
    captured_at = parse_dt(windows.get("extracted_at_utc")) or datetime.now(timezone.utc)
    rows = load_windsor_rows()
    reels = reels_rows(rows, captured_at)
    candidates = windows.get("candidates", [])
    due = [c for c in candidates if c.get("due_windows")]
    due_24 = sum("24h" in c.get("due_windows", []) for c in due)
    due_72 = sum("72h" in c.get("due_windows", []) for c in due)
    responses = windows.get("responses", [])
    http_counts: dict[str, int] = {}
    for response in responses:
        key = str(response.get("http_status"))
        http_counts[key] = http_counts.get(key, 0) + 1
    lifetime_interactions = sum(
        (response.get("lifetime_totals") or {}).get("interactions") or 0
        for response in responses
    )
    summary = {
        "title": "Cierre de ventanas 24/72 e insights de video de Facebook",
        "purpose": "Separar cierres temporales exactos de evidencia lifetime y consolidar alcance, plays y señales de consumo de los Reels recientes.",
        "status": "Active",
        "created": "2026-08-23",
        "updated": captured_at.date().isoformat(),
        "version": "1.1",
        "author": "Manus AI (CGO)",
        "related_documents": [
            "Operations/Research/2026-08-23_Facebook_24_72_Window_Closure.json",
            "Operations/Research/2026-08-23_Facebook_Windsor_Insights_Raw.json",
            "Operations/Research/2026-08-21_Reels_Publication_Inventory.csv",
            "Operations/Research/2026-08-22_Reels_Metric_Instrumentation_Protocol.md",
            "Operations/Research/2026-08-23_Reporte_Rendimiento_Engagement_Facebook.md",
            "GrowthOS/07_00_Registro_Maestro_Reels.md",
            "GrowthOS/Integracion_Growth_OS.md",
        ],
        "organization": "Operations/Research",
        "timezone": windows.get("timezone"),
        "captured_at_utc": windows.get("extracted_at_utc"),
        "source_window_evidence": str(WINDOWS.relative_to(REPO)),
        "source_windsor_raw": str(WINDSOR.relative_to(REPO)),
        "window_closure": {
            "candidate_count": windows.get("candidate_count"),
            "eligible_count": windows.get("eligible_count"),
            "eligible_24h_windows": due_24,
            "eligible_72h_windows": due_72,
            "exact_window_writes": windows.get("exact_window_writes"),
            "status": "Unavailable_No_Baseline" if windows.get("exact_window_writes") == 0 and due else "Exact_Windows_Available",
            "rule": "No lifetime total is written into Interacciones_24h or Interacciones_72h without a baseline and a time-valid snapshot.",
            "api_http_status_counts": http_counts,
            "lifetime_interactions_evidence_sum": lifetime_interactions,
        },
        "video_insights": {
            "rows_with_reel_id": len(reels),
            "source": "Windsor.ai facebook_organic",
            "reach_field": "reels_post_impressions_unique",
            "plays_fields": ["blue_reels_play_count", "fb_reels_total_plays", "fb_reels_replay_count"],
            "watch_fields": ["post_video_avg_time_watched", "post_video_view_time", "post_video_complete_views_organic"],
            "retention_limit": "No 3-second retention percentage or exact completion rate was returned; average-watch share of length is descriptive, not a retention verdict.",
            "records": reels,
        },
        "interpretation": {
            "24_72": "The due windows were processed, but exact values remain unavailable because the historical baseline was not captured. The run records current lifetime totals as evidence only.",
            "video": "The four Reel rows provide L2 discovery plus partial watch signals. They do not yet qualify as complete L3 retention evidence.",
        },
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = [
        "reel_id", "page_post_id", "permalink", "published_at_utc", "age_hours_at_capture", "metric_window_type", "metric_source",
        "post_impressions", "post_impressions_unique", "reels_post_impressions_unique", "blue_reels_play_count", "fb_reels_total_plays",
        "fb_reels_replay_count", "post_video_views_3s_or_nearly_all", "average_watch_time_seconds", "video_length_seconds",
        "average_watch_as_share_of_length", "complete_views_organic_95pct", "view_time_hours", "comments", "shares", "reactions",
        "observable_interactions", "discovery_evidence_status", "video_evidence_status", "retention_status", "data_fetched_at_utc", "post_message",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(reels)
    print(json.dumps({
        "summary_json": str(OUT_JSON),
        "reels_csv": str(OUT_CSV),
        "eligible_windows": len(due),
        "eligible_24h": due_24,
        "eligible_72h": due_72,
        "exact_window_writes": windows.get("exact_window_writes"),
        "reels_with_insights": len(reels),
        "status": summary["window_closure"]["status"],
    }, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
