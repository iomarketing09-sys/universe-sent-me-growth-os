"""Audit current Facebook pending rows without publishing."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12_Audit.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

def get(path, token, params=None):
    response = requests.get(f"{GRAPH}/{path.lstrip('/')}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=30)
    if not response.ok:
        raise RuntimeError(f"META_HTTP_{response.status_code}: {response.text[:500]}")
    return response.json()

accounts = get("me/accounts", base_token, {"fields": "id,name,access_token", "limit": 100})
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

results = []
for item in queue.get("pending", []):
    cid = item.get("comment_id")
    result = {"comment_id": cid, "post_id": item.get("post_id"), "comment_type": item.get("comment_type"), "suggested_reply": item.get("suggested_reply"), "accessible": False, "api_error": None, "page_replies": [], "exact_reply_exists": False, "other_page_reply_exists": False}
    try:
        comment = get(cid, page_token, {"fields": "id,message,from,created_time,parent,is_hidden"})
        result.update({"accessible": True, "comment_message": comment.get("message"), "comment_created_time": comment.get("created_time"), "parent": comment.get("parent")})
        children = get(f"{cid}/comments", page_token, {"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}).get("data", [])
        page_replies = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID]
        result["page_replies"] = [{"id": child.get("id"), "message": child.get("message"), "is_hidden": child.get("is_hidden"), "parent_id": (child.get("parent") or {}).get("id")} for child in page_replies]
        result["exact_reply_exists"] = any(child.get("message") == item.get("suggested_reply") for child in page_replies)
        result["other_page_reply_exists"] = any(child.get("message") != item.get("suggested_reply") for child in page_replies)
    except RuntimeError as exc:
        result["api_error"] = str(exc)
    results.append(result)

payload = {
    "title": "Current Facebook Pending Queue Audit After Batch 12",
    "purpose": "Comprobar por Meta Graph API el estado actual de los 12 registros pendientes sin publicar respuestas.",
    "status": "Active",
    "created_at": "2026-08-24",
    "updated_at": "2026-08-24",
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 read-only",
    "audited_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "requested_count": len(results),
    "accessible_count": sum(1 for result in results if result["accessible"]),
    "inaccessible_count": sum(1 for result in results if not result["accessible"]),
    "exact_reply_exists_count": sum(1 for result in results if result["exact_reply_exists"]),
    "other_page_reply_exists_count": sum(1 for result in results if result["other_page_reply_exists"]),
    "api_error_count": sum(1 for result in results if result["api_error"]),
    "results": results,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "accessible_count", "inaccessible_count", "exact_reply_exists_count", "other_page_reply_exists_count", "api_error_count")}, ensure_ascii=False))
