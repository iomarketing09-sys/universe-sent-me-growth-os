"""Publish the ten remaining approved replies, excluding two explicitly withheld cases."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json"
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_13.json"
EXCLUDED = {
    "122151375549072582_1817089682764579",  # L Roberto, user-to-user reply
    "122151376011072582_1703056380925949",  # inaccessible Carlos Sadness comment
}

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
targets = [
    {"parent_comment_id": item["comment_id"], "message": item["suggested_reply"], "comment_excerpt": item.get("comment_message", ""), "comment_type": item.get("comment_type", "")}
    for item in queue.get("pending", [])
    if item.get("comment_id") not in EXCLUDED
]
if len(queue.get("pending", [])) != 12 or len(targets) != 10:
    raise SystemExit(f"EXPECTED_12_QUEUE_AND_10_TARGETS: queue={len(queue.get('pending', []))}, targets={len(targets)}")
if any(not item["message"] for item in targets):
    raise SystemExit("TARGET_WITHOUT_MESSAGE")

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

def request(method, path, token, *, params=None, form=None):
    response = requests.request(method, f"{GRAPH}/{path.lstrip('/')}", headers={"Authorization": f"Bearer {token}"}, params=params, data=form, timeout=30)
    if not response.ok:
        raise RuntimeError(f"META_HTTP_{response.status_code}: {response.text[:500]}")
    return response.json()

accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

prechecks = []
for target in targets:
    children = request("GET", f"{target['parent_comment_id']}/comments", page_token, params={"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}).get("data", [])
    exact = next((child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") == target["message"]), None)
    other_page = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") != target["message"]]
    if other_page and exact is None:
        raise SystemExit(json.dumps({"preflight_conflict": target["parent_comment_id"], "existing_page_reply_ids": [child.get("id") for child in other_page]}, ensure_ascii=False))
    prechecks.append({**target, "verified": exact})

published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for item in prechecks:
    status = "already_published"
    verified = item["verified"]
    if verified is None:
        created = request("POST", f"{item['parent_comment_id']}/comments", page_token, form={"message": item["message"]})
        reply_id = created.get("id")
        if not reply_id:
            raise SystemExit(json.dumps({"missing_reply_id": item["parent_comment_id"]}, ensure_ascii=False))
        verified = request("GET", reply_id, page_token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
        status = "published"
    parent = verified.get("parent") or {}
    results.append({
        "status": status,
        "parent_comment_id": item["parent_comment_id"],
        "comment_excerpt": item["comment_excerpt"],
        "comment_type": item["comment_type"],
        "reply_id": verified.get("id"),
        "message": verified.get("message"),
        "from_id": (verified.get("from") or {}).get("id"),
        "from_name": (verified.get("from") or {}).get("name"),
        "parent_id_returned": parent.get("id"),
        "is_hidden": verified.get("is_hidden"),
        "verified": ((verified.get("from") or {}).get("id") == PAGE_ID and verified.get("message") == item["message"] and parent.get("id") == item["parent_comment_id"] and verified.get("is_hidden") is False),
    })
if any(not result["verified"] for result in results):
    raise SystemExit(json.dumps({"verification_failed": results}, ensure_ascii=False))

payload = {
    "title": "Facebook Comment Publication Batch 13 — Remaining Approved Replies",
    "purpose": "Evidencia de la publicación y verificación de diez respuestas aprobadas; excluye la réplica de L Roberto y el comentario inaccesible.",
    "status": "Active",
    "created_at": published_at,
    "updated_at": published_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_13.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "published_at": published_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "excluded_comment_ids": sorted(EXCLUDED),
    "requested_count": len(targets),
    "published_count": sum(1 for result in results if result["status"] == "published"),
    "already_published_count": sum(1 for result in results if result["status"] == "already_published"),
    "inaccessible_count": 0,
    "verified_count": sum(1 for result in results if result["verified"]),
    "results": results,
}
BATCH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "inaccessible_count", "verified_count")}, ensure_ascii=False))
for result in results:
    print(json.dumps(result, ensure_ascii=False))
