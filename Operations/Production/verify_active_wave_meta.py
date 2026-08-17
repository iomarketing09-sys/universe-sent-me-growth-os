#!/usr/bin/env python3
"""Read-only verification of the active Facebook publication wave."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://graph.facebook.com/v26.0"
TOKEN = os.environ["META_PAGE_ACCESS_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

accounts = requests.get(
    f"{BASE}/me/accounts",
    headers=HEADERS,
    params={"fields": "id,name,access_token,tasks", "limit": 100},
    timeout=30,
)
accounts.raise_for_status()
page = next(x for x in accounts.json().get("data", []) if x.get("name") == "Universe Sent Me")
page_token = page["access_token"]
page_id = page["id"]

feed = requests.get(
    f"{BASE}/{page_id}/feed",
    headers={"Authorization": f"Bearer {page_token}"},
    params={
        "fields": "id,created_time,message,permalink_url,attachments{media_type,media,target}",
        "since": "2026-08-17T00:00:00-05:00",
        "until": "2026-08-31T00:00:00-05:00",
        "limit": 100,
    },
    timeout=30,
)
feed.raise_for_status()
result = {
    "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
    "page_id": page_id,
    "page_name": page["name"],
    "page_tasks": page.get("tasks", []),
    "posts": feed.json().get("data", []),
    "paging": feed.json().get("paging", {}),
}
Path("Operations/Research/2026-08-17_Verificacion_Meta_Ola_Activa.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({"page_id": page_id, "page_name": page["name"], "post_count": len(result["posts"]), "output": "Operations/Research/2026-08-17_Verificacion_Meta_Ola_Activa.json"}, ensure_ascii=False))
for post in result["posts"]:
    print(post.get("created_time"), post.get("id"), post.get("message", "")[:100].replace("\n", " "))
