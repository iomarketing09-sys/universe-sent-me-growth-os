#!/usr/bin/env python3
"""Validate local read-only Meta access for Universe Sent Me.

Design reminder: this probe makes only GET requests to Meta Graph API. It uses
an operator-provided local token, saves a private minimal evidence record outside
the repository, and never writes content, comments, schedules, Sheets, OmniRoute,
or canonical Growth OS ledgers.
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


def safe_error(response: requests.Response) -> dict[str, Any] | None:
    if response.status_code == 200:
        return None
    try:
        payload = response.json()
    except ValueError:
        return {"http_status": response.status_code, "message": "non_json_response"}
    error = payload.get("error", {}) if isinstance(payload, dict) else {}
    return {
        "http_status": response.status_code,
        "code": error.get("code"),
        "type": error.get("type"),
        "message": error.get("message"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", default="~/.local/share/usm-metrics/evidence")
    parser.add_argument("--page-id", default=PAGE_ID)
    parser.add_argument("--instagram-username", default=INSTAGRAM_USERNAME)
    args = parser.parse_args()

    token = os.environ.get("USM_META_USER_ACCESS_TOKEN")
    if not token:
        raise SystemExit("USM_META_USER_ACCESS_TOKEN is required locally; do not store it in the repository.")

    capture = utc_now()
    evidence_dir = Path(args.evidence_dir).expanduser().resolve()
    pages_response = get(
        "/me/accounts",
        token,
        {"fields": "id,instagram_business_account{id,username}", "limit": "100"},
    )
    pages_error = safe_error(pages_response)
    result: dict[str, Any] = {
        "brand": BRAND,
        "platforms": ["Facebook", "Instagram"],
        "captured_at_utc": capture,
        "operation": "GET-only connection and authorization validation",
        "facebook_page_id_expected": args.page_id,
        "instagram_username_expected": args.instagram_username,
        "facebook_connection": "not_validated",
        "instagram_connection": "not_validated",
        "limitations": [
            "This probe does not request posts, comments, messages, insights, or any publishing endpoint.",
            "This probe does not write GitHub, Google Sheets, canonical ledgers, content, schedules, or OmniRoute.",
            "A token or permission failure is retained as a failure; the probe never treats it as zero data.",
        ],
    }

    if pages_error:
        result["facebook_error"] = pages_error
        result["instagram_error"] = pages_error
    else:
        pages = pages_response.json().get("data", [])
        page = next((item for item in pages if str(item.get("id")) == str(args.page_id)), None)
        if page is None:
            result["facebook_error"] = {"message": "expected_page_not_returned"}
            result["instagram_error"] = {"message": "expected_page_not_returned"}
        else:
            result["facebook_connection"] = "validated"
            instagram = page.get("instagram_business_account")
            if not isinstance(instagram, dict) or not instagram.get("id"):
                result["instagram_error"] = {"message": "linked_instagram_business_account_not_returned"}
            else:
                instagram_response = get(
                    str(instagram["id"]),
                    token,
                    {"fields": "id,username"},
                )
                instagram_error = safe_error(instagram_response)
                if instagram_error:
                    result["instagram_error"] = instagram_error
                else:
                    username = str(instagram_response.json().get("username", ""))
                    if username.lower() == str(args.instagram_username).lower():
                        result["instagram_connection"] = "validated"
                    else:
                        result["instagram_error"] = {
                            "message": "linked_instagram_username_mismatch",
                            "returned_username": username,
                        }

    result["status"] = "validated" if (
        result["facebook_connection"] == "validated" and result["instagram_connection"] == "validated"
    ) else "blocked"
    evidence_path = evidence_dir / f"{capture[:10]}_Meta_Local_Readonly_Validation.json"
    write_private_json(evidence_path, result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "brand": BRAND,
                "facebook_connection": result["facebook_connection"],
                "instagram_connection": result["instagram_connection"],
                "evidence": str(evidence_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
