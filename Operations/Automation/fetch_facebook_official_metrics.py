#!/usr/bin/env python3
"""Fetch a bounded, private, read-only Facebook Page metrics snapshot for USM.

Design reminder: GET-only, no content text, no comments/messages, no Growth OS
ledger writes, no Sheets, no OmniRoute and no operations on other brands.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


BRAND = "Universe Sent Me"
GRAPH_BASE = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
FEED_FIELDS = "id,created_time,is_published,reactions.limit(0).summary(true),comments.limit(0).summary(true),shares"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(temporary, 0o600)
    temporary.replace(path)
    os.chmod(path, 0o600)


def get(path: str, token: str, params: dict[str, str]) -> requests.Response:
    return requests.get(
        f"{GRAPH_BASE}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )


def error_summary(response: requests.Response) -> dict[str, Any]:
    try:
        error = response.json().get("error", {})
    except ValueError:
        error = {}
    return {
        "http_status": response.status_code,
        "code": error.get("code"),
        "type": error.get("type"),
        "message": error.get("message", "non_json_response"),
    }


def counter(value: Any, *, share: bool = False) -> int | None:
    if share:
        raw = value.get("count") if isinstance(value, dict) else None
    else:
        raw = value.get("summary", {}).get("total_count") if isinstance(value, dict) else None
    return int(raw) if isinstance(raw, (int, float)) and not isinstance(raw, bool) else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page-id", default=PAGE_ID)
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--evidence-dir", default="~/.local/share/usm-metrics/evidence")
    args = parser.parse_args()
    if not 1 <= args.limit <= 25:
        raise SystemExit("--limit must be between 1 and 25.")

    user_token = os.environ.get("USM_META_USER_ACCESS_TOKEN")
    if not user_token:
        raise SystemExit("USM_META_USER_ACCESS_TOKEN is required locally; do not store it in the repository.")

    captured = utc_now()
    evidence: dict[str, Any] = {
        "brand": BRAND,
        "platform": "Facebook",
        "source": "Meta Graph API v26 / Page Feed",
        "captured_at_utc": captured,
        "page_id_expected": str(args.page_id),
        "metric_type": "lifetime_native_post_counters_at_capture",
        "requested_fields": ["id", "created_time", "is_published", "reactions", "comments", "shares"],
        "limitations": [
            "No post message, URL, attachment, profile, comment, message or insight is requested.",
            "Missing reactions, comments or shares stay null and are never converted to zero.",
            "No GitHub, Sheets, ledger, content, schedule or OmniRoute write is performed.",
        ],
    }
    accounts = get("/me/accounts", user_token, {"fields": "id,access_token", "limit": "100"})
    if accounts.status_code != 200:
        evidence.update({"status": "blocked", "stage": "derive_page_token", "error": error_summary(accounts)})
    else:
        page = next((item for item in accounts.json().get("data", []) if str(item.get("id")) == str(args.page_id)), None)
        page_token = page.get("access_token") if isinstance(page, dict) else None
        if not page_token:
            evidence.update({"status": "blocked", "stage": "derive_page_token", "error": {"message": "expected_page_token_not_returned"}})
        else:
            feed = get(
                f"/{args.page_id}/feed",
                str(page_token),
                {"fields": FEED_FIELDS, "limit": str(args.limit)},
            )
            if feed.status_code != 200:
                evidence.update({"status": "blocked", "stage": "read_page_feed", "error": error_summary(feed)})
            else:
                posts = [item for item in feed.json().get("data", []) if item.get("is_published") is True]
                evidence.update(
                    {
                        "status": "collected",
                        "records": [
                            {
                                "id": item.get("id"),
                                "created_time": item.get("created_time"),
                                "reactions": counter(item.get("reactions")),
                                "comments": counter(item.get("comments")),
                                "shares": counter(item.get("shares"), share=True),
                            }
                            for item in posts
                        ],
                    }
                )

    destination = Path(args.evidence_dir).expanduser().resolve() / f"{captured[:10]}_Facebook_Official_Metrics.json"
    write_private_json(destination, evidence)
    print(
        json.dumps(
            {
                "status": evidence["status"],
                "brand": BRAND,
                "platform": "Facebook",
                "records": len(evidence.get("records", [])),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
