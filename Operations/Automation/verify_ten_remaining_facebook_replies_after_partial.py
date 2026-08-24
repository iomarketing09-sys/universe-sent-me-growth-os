"""Recover and verify Batch 13 after all ten POSTs completed but one nested parent field differed."""

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
    "122151375549072582_1817089682764579",  # L Roberto
    "122151376011072582_1703056380925949",  # inaccessible Carlos Sadness
}

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
targets = [item for item in queue.get("pending", []) if item.get("comment_id") not in EXCLUDED]
if len(targets) != 10:
    raise SystemExit(f"EXPECTED_10_TARGETS: {len(targets)}")

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
for target in targets:
    target_id = target["comment_id"]
    item = {"parent_comment_id": target_id, "comment_excerpt": target.get("comment_message", ""), "comment_type": target.get("comment_type", ""), "expected_message": target.get("suggested_reply", ""), "status": "published_already", "accessible": False, "verified": False, "verification_mode": None}
    try:
        target_comment = get(target_id, page_token, {"fields": "id,message,from,created_time,parent,is_hidden"})
        item["accessible"] = True
        item["target_parent_id"] = (target_comment.get("parent") or {}).get("id")
        children = get(f"{target_id}/comments", page_token, {"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}).get("data", [])
        exact = next((child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") == target.get("suggested_reply")), None)
        if exact is None:
            item["error"] = "EXACT_PAGE_REPLY_NOT_FOUND"
        else:
            actual_parent = (exact.get("parent") or {}).get("id")
            target_parent = item["target_parent_id"]
            if target_parent is None and actual_parent == target_id:
                mode = "direct_root_parent"
                parent_ok = True
            elif target_parent is not None and actual_parent == target_parent:
                mode = "nested_reply_api_returns_root_parent"
                parent_ok = True
            else:
                mode = "parent_mismatch"
                parent_ok = False
            item.update({
                "reply_id": exact.get("id"),
                "message": exact.get("message"),
                "from_id": (exact.get("from") or {}).get("id"),
                "from_name": (exact.get("from") or {}).get("name"),
                "parent_id_returned": actual_parent,
                "is_hidden": exact.get("is_hidden"),
                "verification_mode": mode,
                "verified": bool(parent_ok and exact.get("is_hidden") is False),
            })
    except RuntimeError as exc:
        item["error"] = str(exc)
    results.append(item)

if any(not item.get("verified") for item in results):
    raise SystemExit(json.dumps({"verification_failed": results}, ensure_ascii=False))

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "title": "Facebook Comment Publication Batch 13 — Remaining Approved Replies",
    "purpose": "Evidencia recuperada de diez respuestas aprobadas: nueve raíces y una réplica musical accesible; excluye L Roberto y el comentario inaccesible.",
    "status": "Active",
    "created_at": now,
    "updated_at": now,
    "version": "1.1",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_13.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "published_at": now,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "excluded_comment_ids": sorted(EXCLUDED),
    "requested_count": 10,
    "published_count": 10,
    "already_published_count": 0,
    "inaccessible_count": 0,
    "verified_count": len(results),
    "strict_direct_parent_count": sum(1 for item in results if item["verification_mode"] == "direct_root_parent"),
    "nested_root_parent_semantics_count": sum(1 for item in results if item["verification_mode"] == "nested_reply_api_returns_root_parent"),
    "results": results,
}
BATCH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "verified_count", "strict_direct_parent_count", "nested_root_parent_semantics_count")}, ensure_ascii=False))
for item in results:
    print(json.dumps(item, ensure_ascii=False))
