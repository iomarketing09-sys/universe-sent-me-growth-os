#!/usr/bin/env python3
"""Fetch official TikTok public-video metrics for Universe Sent Me.

The script reads the local OAuth token, refreshes it when needed, and writes
private local evidence. It never writes GitHub ledgers, Google Sheets, content
or OmniRoute inputs. A later deterministic review step decides what can move.
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
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
VIDEO_LIST_URL = "https://open.tiktokapis.com/v2/video/list/"
FIELDS = "id,create_time,share_url,title,like_count,comment_count,share_count,view_count"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def expand(value: str) -> Path:
    return Path(value).expanduser().resolve()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(temp, 0o600)
    temp.replace(path)
    os.chmod(path, 0o600)


def load_config(path: Path) -> dict[str, Any]:
    config = load_json(path)
    if config.get("brand") != BRAND:
        raise RuntimeError("Configuration brand must be exactly 'Universe Sent Me'.")
    return config


def refresh_if_needed(config: dict[str, Any], token: dict[str, Any]) -> dict[str, Any]:
    obtained = datetime.fromisoformat(str(token["obtained_at_utc"]).replace("Z", "+00:00"))
    expires_in = int(token.get("expires_in", 0))
    age_seconds = (datetime.now(timezone.utc) - obtained.astimezone(timezone.utc)).total_seconds()
    if token.get("access_token") and age_seconds < max(0, expires_in - 300):
        return token
    tiktok = config["tiktok"]
    client_key = os.environ.get(str(tiktok["client_key_env"]))
    client_secret = os.environ.get(str(tiktok["client_secret_env"]))
    if not client_key or not client_secret:
        raise RuntimeError("TikTok client values are required locally to refresh the access token.")
    response = requests.post(
        TOKEN_URL,
        data={
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    refreshed = response.json()
    if response.status_code != 200 or refreshed.get("error"):
        raise RuntimeError(f"TikTok refresh failed with HTTP {response.status_code}: {refreshed.get('error_description', refreshed.get('error'))}")
    approved = set(tiktok.get("required_scopes", []))
    granted = set(str(refreshed.get("scope", "")).split(","))
    if granted != approved:
        raise RuntimeError("Refreshed TikTok token scopes no longer match the approved scope.")
    refreshed["brand"] = BRAND
    refreshed["obtained_at_utc"] = utc_now()
    refreshed["redirect_uri"] = tiktok["redirect_uri"]
    write_private_json(expand(str(tiktok["token_file"])), refreshed)
    return refreshed


def list_videos(access_token: str, max_pages: int) -> list[dict[str, Any]]:
    cursor: int | None = None
    videos: list[dict[str, Any]] = []
    for _ in range(max_pages):
        body: dict[str, Any] = {"max_count": 20}
        if cursor is not None:
            body["cursor"] = cursor
        response = requests.post(
            VIDEO_LIST_URL,
            params={"fields": FIELDS},
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
            json=body,
            timeout=30,
        )
        payload = response.json()
        if response.status_code != 200 or payload.get("error", {}).get("code") not in {None, "ok"}:
            raise RuntimeError(f"TikTok video list failed with HTTP {response.status_code}: {payload.get('error')}")
        data = payload.get("data", {})
        videos.extend(data.get("videos", []))
        if not data.get("has_more"):
            break
        cursor = data.get("cursor")
        if not isinstance(cursor, int):
            raise RuntimeError("TikTok response indicated more videos without a valid cursor.")
    return videos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("~/.config/usm-metrics/config.json").expanduser())
    parser.add_argument("--max-pages", type=int, default=5)
    args = parser.parse_args()
    if args.max_pages < 1 or args.max_pages > 50:
        raise SystemExit("--max-pages must be between 1 and 50.")

    config = load_config(args.config.expanduser())
    tiktok = config["tiktok"]
    token_file = expand(str(tiktok["token_file"]))
    token = refresh_if_needed(config, load_json(token_file))
    videos = list_videos(str(token["access_token"]), args.max_pages)
    evidence_dir = expand(str(config["evidence_dir"]))
    captured = utc_now()
    evidence = {
        "brand": BRAND,
        "platform": "TikTok",
        "source": "TikTok Display API v2 / video.list",
        "captured_at_utc": captured,
        "scope": token.get("scope"),
        "account_label": tiktok.get("account_label"),
        "metric_type": "lifetime_public_video_counters_at_capture",
        "videos": videos,
        "limitations": [
            "The API returns public-video counters at capture time; the script does not infer E24/E72 deltas.",
            "No raw evidence is written to GitHub, Google Sheets or OmniRoute by this collector.",
        ],
    }
    output = evidence_dir / f"{captured[:10]}_TikTok_Official_Metrics.json"
    write_private_json(output, evidence)
    print(json.dumps({"status": "collected", "brand": BRAND, "platform": "TikTok", "records": len(videos), "evidence": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
