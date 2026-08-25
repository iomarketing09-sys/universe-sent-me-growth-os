#!/usr/bin/env python3
"""Fetch official YouTube performance and monetization metrics for Universe Sent Me.

OAuth tokens and raw evidence remain local. This collector does not write
canonical ledgers, Google Sheets, content, comments, schedules or OmniRoute.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BRAND = "Universe Sent Me"
PERFORMANCE_METRICS = [
    "views",
    "engagedViews",
    "likes",
    "comments",
    "shares",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "subscribersGained",
]
MONETARY_METRICS = [
    "estimatedRevenue",
    "estimatedAdRevenue",
    "estimatedRedPartnerRevenue",
    "grossRevenue",
    "adImpressions",
    "monetizedPlaybacks",
    "cpm",
    "playbackBasedCpm",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def expand(value: str) -> Path:
    return Path(value).expanduser().resolve()


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("brand") != BRAND:
        raise RuntimeError("Configuration brand must be exactly 'Universe Sent Me'.")
    return config


def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(temp, 0o600)
    temp.replace(path)
    os.chmod(path, 0o600)


def credentials(config: dict[str, Any]) -> Credentials:
    youtube = config["youtube"]
    scopes = list(youtube["scopes"])
    required = {
        "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/yt-analytics.readonly",
        "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
    }
    if set(scopes) != required:
        raise RuntimeError("YouTube scopes must match the approved read-only and monetary scope set.")
    token_file = expand(str(youtube["token_file"]))
    creds: Credentials | None = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        client_secret_file = expand(str(youtube["client_secret_file"]))
        if not client_secret_file.exists():
            raise RuntimeError("Local YouTube OAuth client file is missing. Do not store it in the repository.")
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_file), scopes)
        creds = flow.run_local_server(host="127.0.0.1", port=0, prompt="consent")
    write_private_json(token_file, json.loads(creds.to_json()))
    return creds


def as_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    headers = [column["name"] for column in payload.get("columnHeaders", [])]
    return [dict(zip(headers, row, strict=False)) for row in payload.get("rows", [])]


def query_report(analytics: Any, metrics: list[str], start_date: str, end_date: str, include_currency: bool = False) -> dict[str, Any]:
    params: dict[str, Any] = {
        "ids": "channel==MINE",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": ",".join(metrics),
        "dimensions": "video",
        "sort": "-views",
        "maxResults": 200,
    }
    if include_currency:
        params["currency"] = "USD"
    return analytics.reports().query(**params).execute()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("~/.config/usm-metrics/config.json").expanduser())
    parser.add_argument("--date-from", help="YYYY-MM-DD; defaults to seven days before date_to.")
    parser.add_argument("--date-to", help="YYYY-MM-DD; defaults to yesterday UTC to avoid incomplete daily rows.")
    args = parser.parse_args()
    end_date = date.fromisoformat(args.date_to) if args.date_to else date.today() - timedelta(days=1)
    start_date = date.fromisoformat(args.date_from) if args.date_from else end_date - timedelta(days=6)
    if start_date > end_date:
        raise SystemExit("--date-from cannot be after --date-to.")

    config = load_config(args.config.expanduser())
    creds = credentials(config)
    analytics = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    channel = youtube.channels().list(part="id,snippet", mine=True).execute()
    channels = channel.get("items", [])
    if len(channels) != 1:
        raise RuntimeError("Expected exactly one authorized YouTube channel for Universe Sent Me.")
    channel_record = channels[0]
    configured_handle = str(config["youtube"].get("channel_handle", ""))

    performance_payload = query_report(analytics, PERFORMANCE_METRICS, start_date.isoformat(), end_date.isoformat())
    monetization_status = "available"
    monetary_payload: dict[str, Any] | None = None
    monetization_error: str | None = None
    try:
        monetary_payload = query_report(
            analytics,
            MONETARY_METRICS,
            start_date.isoformat(),
            end_date.isoformat(),
            include_currency=True,
        )
    except HttpError as error:
        monetization_status = "not_available"
        monetization_error = str(error)

    captured = utc_now()
    evidence = {
        "brand": BRAND,
        "platform": "YouTube",
        "source": "YouTube Data API v3 + YouTube Analytics API v2",
        "captured_at_utc": captured,
        "channel_handle_expected": configured_handle,
        "channel_id": channel_record.get("id"),
        "channel_title": channel_record.get("snippet", {}).get("title"),
        "window_start": start_date.isoformat(),
        "window_end": end_date.isoformat(),
        "performance_rows": as_rows(performance_payload),
        "monetization_status": monetization_status,
        "financial_status": "preliminary" if monetization_status == "available" else "not_available",
        "monetization_rows": as_rows(monetary_payload) if monetary_payload else [],
        "monetization_error": monetization_error,
        "limitations": [
            "Revenue metrics are estimated and may be adjusted after month-end.",
            "A missing metric is retained as not_available; the collector never converts it to zero.",
            "Raw monetary values stay in private local evidence and are not sent to OmniRoute by this collector.",
            "No canonical ledger, Google Sheet, publication, comment or schedule is modified by this collector.",
        ],
    }
    output = expand(str(config["evidence_dir"])) / f"{captured[:10]}_YouTube_Official_Metrics.json"
    write_private_json(output, evidence)
    print(
        json.dumps(
            {
                "status": "collected",
                "brand": BRAND,
                "platform": "YouTube",
                "performance_rows": len(evidence["performance_rows"]),
                "monetization_status": monetization_status,
                "evidence": str(output),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
