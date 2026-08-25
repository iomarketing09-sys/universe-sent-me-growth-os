#!/usr/bin/env python3
"""Fetch a bounded, private, read-only Instagram Professional metrics snapshot for USM.

Design reminder: GET-only, no caption/media URLs/comments/messages, no Growth OS
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
INSTAGRAM_USERNAME = "universe_sent_me_0326"
MEDIA_FIELDS = "id,timestamp,media_type,media_product_type,like_count,comments_count,saved_count,shares_count,total_like_count,total_comments_count,total_views_count,reposts_count"


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page-id", default=PAGE_ID)
    parser.add_argument("--instagram-username", default=INSTAGRAM_USERNAME)
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
        "platform": "Instagram",
        "source": "Meta Graph API v26 / Instagram Professional media",
        "captured_at_utc": captured,
        "page_id_expected": str(args.page_id),
        "instagram_username_expected": str(args.instagram_username),
        "metric_type": "lifetime_native_media_counters_at_capture",
        "requested_fields": MEDIA_FIELDS.split(","),
        "limitations": [
            "No caption, media URL, permalink, comment, message or insight is requested.",
            "Unavailable native fields remain absent or null and are never converted to zero.",
            "No GitHub, Sheets, ledger, content, schedule or OmniRoute write is performed.",
        ],
    }
    accounts = get(
        "/me/accounts",
        user_token,
        {"fields": "id,instagram_business_account{id,username}", "limit": "100"},
    )
    if accounts.status_code != 200:
        evidence.update({"status": "blocked", "stage": "discover_linked_instagram", "error": error_summary(accounts)})
    else:
        page = next((item for item in accounts.json().get("data", []) if str(item.get("id")) == str(args.page_id)), None)
        instagram = page.get("instagram_business_account") if isinstance(page, dict) else None
        instagram_id = instagram.get("id") if isinstance(instagram, dict) else None
        username = instagram.get("username") if isinstance(instagram, dict) else None
        if not instagram_id:
            evidence.update({"status": "blocked", "stage": "discover_linked_instagram", "error": {"message": "linked_instagram_business_account_not_returned"}})
        elif str(username).lower() != str(args.instagram_username).lower():
            evidence.update({"status": "blocked", "stage": "verify_username", "error": {"message": "linked_instagram_username_mismatch"}})
        else:
            media = get(str(instagram_id) + "/media", user_token, {"fields": MEDIA_FIELDS, "limit": str(args.limit)})
            if media.status_code != 200:
                evidence.update({"status": "blocked", "stage": "read_instagram_media", "error": error_summary(media)})
            else:
                records = media.json().get("data", [])
                requested_fields = MEDIA_FIELDS.split(",")
                evidence.update(
                    {
                        "status": "collected",
                        "records": records,
                        "field_availability": {
                            field: any(field in record for record in records) for field in requested_fields
                        },
                    }
                )

    destination = Path(args.evidence_dir).expanduser().resolve() / f"{captured[:10]}_Instagram_Official_Metrics.json"
    write_private_json(destination, evidence)
    print(
        json.dumps(
            {
                "status": evidence["status"],
                "brand": BRAND,
                "platform": "Instagram",
                "records": len(evidence.get("records", [])),
                "available_native_fields": sum(evidence.get("field_availability", {}).values()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
