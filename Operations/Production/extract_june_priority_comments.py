#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://graph.facebook.com/v26.0"
USER_TOKEN = os.environ["META_PAGE_ACCESS_TOKEN"]
accounts = requests.get(f"{BASE}/me/accounts", headers={"Authorization": f"Bearer {USER_TOKEN}"}, params={"fields": "id,name,access_token,tasks", "limit": 100}, timeout=30)
accounts.raise_for_status()
page = next(x for x in accounts.json().get("data", []) if x.get("name") == "Universe Sent Me")
TOKEN = page["access_token"]
POST_IDS = [
    "1036844829507460_122134061121072582",  # 2607823, 27 comments
    "1036844829507460_122129214813072582",  # 260740, 14 comments
    "1036844829507460_122130411897072582",  # 260765, 14 comments
    "1036844829507460_122134374249072582",  # 2607837, 11 comments
    "1036844829507460_122128536909072582",  # 260731, 10 comments
]
fields = "id,created_time,message,comments.limit(100){id,from,message,created_time,like_count,comment_count,parent}"
batch = [{"method": "GET", "relative_url": f"{pid}?fields={fields}"} for pid in POST_IDS]
resp = requests.post(
    BASE,
    headers={"Authorization": f"Bearer {TOKEN}"},
    data={"batch": json.dumps(batch)},
    timeout=45,
)
resp.raise_for_status()
out = {
    "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
    "post_ids": POST_IDS,
    "selection_basis": "Top visible comments among reviewed June priority assets; no publishing action.",
    "batch_response": resp.json(),
}
path = Path("Operations/Research/2026-08-18_Comentarios_Junio_Lote_Prioritario.json")
path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"status": resp.status_code, "posts": len(POST_IDS), "output": str(path)}, ensure_ascii=False))
for idx, item in enumerate(out["batch_response"]):
    body = item.get("body", "")
    try:
        parsed = json.loads(body)
        comments = parsed.get("comments", {}).get("data", []) if isinstance(parsed, dict) else []
        print(idx, POST_IDS[idx], "http", item.get("code"), "comments", len(comments), "post_message", parsed.get("message", "")[:80] if isinstance(parsed, dict) else "")
    except Exception:
        print(idx, POST_IDS[idx], "http", item.get("code"), "body", body[:160])
