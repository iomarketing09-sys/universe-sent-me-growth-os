from __future__ import annotations

import json
import os
from pathlib import Path

import requests

BASE = "https://graph.facebook.com"
API_VERSION = "v26.0"
PAGE_ID = "1036844829507460"
PREPARED = Path("/tmp/comparable_facebook_prepared.json")
CDN_URLS = Path("/tmp/comparable_cdn_urls.json")
TOKEN = os.environ["META_PAGE_ACCESS_TOKEN"]
USER_HEADERS = {"Authorization": f"Bearer {TOKEN}"}

accounts = requests.get(
    f"{BASE}/{API_VERSION}/me/accounts",
    headers=USER_HEADERS,
    params={"fields": "id,name,access_token,tasks"},
    timeout=30,
)
accounts.raise_for_status()
page = next((item for item in accounts.json().get("data", []) if item.get("id") == PAGE_ID or item.get("name") == "Universe Sent Me"), None)
if not page or not page.get("access_token"):
    raise RuntimeError("Could not derive Universe Sent Me Page Access Token")
PAGE_HEADERS = {"Authorization": f"Bearer {page['access_token']}"}

with PREPARED.open(encoding="utf-8") as handle:
    prepared = json.load(handle)["prepared"]
with CDN_URLS.open(encoding="utf-8") as handle:
    cdn_urls = json.load(handle)

assert len(prepared) == 3
results = []
for item in prepared:
    brief_id = item["brief_id"]
    image_url = cdn_urls[brief_id]
    photo_response = requests.post(
        f"{BASE}/{API_VERSION}/{PAGE_ID}/photos",
        headers=PAGE_HEADERS,
        data={"url": image_url, "published": "false", "temporary": "true"},
        timeout=60,
    )
    photo_response.raise_for_status()
    photo_payload = photo_response.json()
    photo_id = photo_payload.get("id")
    if not photo_id:
        raise RuntimeError(f"Meta did not return a photo ID for {brief_id}: {photo_payload}")

    feed_response = requests.post(
        f"{BASE}/{API_VERSION}/{PAGE_ID}/feed",
        headers=PAGE_HEADERS,
        data={
            "message": item["caption"],
            "attached_media[0]": json.dumps({"media_fbid": photo_id}),
            "published": "false",
            "scheduled_publish_time": str(item["scheduled_publish_time"]),
            "unpublished_content_type": "SCHEDULED",
        },
        timeout=60,
    )
    feed_response.raise_for_status()
    feed_payload = feed_response.json()
    post_id = feed_payload.get("id")
    if not post_id:
        raise RuntimeError(f"Meta did not return a post ID for {brief_id}: {feed_payload}")

    verification_response = requests.get(
        f"{BASE}/{API_VERSION}/{post_id}",
        headers=PAGE_HEADERS,
        params={"fields": "id,is_published,scheduled_publish_time,permalink_url"},
        timeout=30,
    )
    verification_response.raise_for_status()
    verification = verification_response.json()
    if verification.get("is_published") is not False:
        raise RuntimeError(f"Post {post_id} is not in scheduled unpublished state: {verification}")
    results.append({
        "brief_id": brief_id,
        "hypothesis_id": item["hypothesis_id"],
        "photo_id": photo_id,
        "post_id": post_id,
        "scheduled_publish_time": item["scheduled_publish_time"],
        "verification": verification,
        "status": "Scheduled_Verified",
    })

print(json.dumps({"scheduled": results, "count": len(results)}, ensure_ascii=False, indent=2))
