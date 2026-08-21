from __future__ import annotations

import json
import os
from pathlib import Path

import requests

BASE = "https://graph.facebook.com"
API_VERSION = "v26.0"
PREPARED = Path("/tmp/comparable_facebook_prepared.json")
USER_TOKEN = os.environ["META_PAGE_ACCESS_TOKEN"]
USER_HEADERS = {"Authorization": f"Bearer {USER_TOKEN}"}
accounts_response = requests.get(
    f"{BASE}/{API_VERSION}/me/accounts",
    headers=USER_HEADERS,
    params={"fields": "id,name,access_token,tasks"},
    timeout=30,
)
accounts_response.raise_for_status()
page = next((item for item in accounts_response.json().get("data", []) if item.get("id") == "1036844829507460" or item.get("name") == "Universe Sent Me"), None)
if not page or not page.get("access_token"):
    raise RuntimeError("Could not derive Universe Sent Me Page Access Token")
PAGE_HEADERS = {"Authorization": f"Bearer {page['access_token']}"}

with PREPARED.open(encoding="utf-8") as handle:
    prepared = json.load(handle)["prepared"]

assert len(prepared) == 3
results = []
for item in prepared:
    post_id = item["old_meta_post_id"]
    check = requests.get(
        f"{BASE}/{API_VERSION}/{post_id}",
        headers=PAGE_HEADERS,
        params={"fields": "id,is_published,scheduled_publish_time"},
        timeout=30,
    )
    check.raise_for_status()
    current = check.json()
    if current.get("is_published") is True:
        raise RuntimeError(f"Refusing to delete already-published post {post_id}")
    if not current.get("scheduled_publish_time"):
        raise RuntimeError(f"Refusing to delete post without scheduled time {post_id}")

    deleted = requests.delete(f"{BASE}/{API_VERSION}/{post_id}", headers=PAGE_HEADERS, timeout=30)
    deleted.raise_for_status()
    deleted_payload = deleted.json()
    if deleted_payload.get("success") is not True:
        raise RuntimeError(f"Meta did not confirm deletion for {post_id}: {deleted_payload}")

    verify = requests.get(
        f"{BASE}/{API_VERSION}/{post_id}",
        headers=PAGE_HEADERS,
        params={"fields": "id,is_published,scheduled_publish_time"},
        timeout=30,
    )
    if verify.ok:
        verification = {"http_status": verify.status_code, "body": verify.json()}
        raise RuntimeError(f"Deleted post remains readable: {post_id}: {verification}")
    verification = {"http_status": verify.status_code, "body": verify.json()}
    results.append({
        "brief_id": item["brief_id"],
        "old_meta_post_id": post_id,
        "old_meta_photo_id": item["old_meta_photo_id"],
        "scheduled_publish_time": current["scheduled_publish_time"],
        "delete_response": deleted_payload,
        "verification": verification,
        "status": "Cancelled_Verified",
    })

print(json.dumps({"cancelled": results, "count": len(results)}, ensure_ascii=False, indent=2))
