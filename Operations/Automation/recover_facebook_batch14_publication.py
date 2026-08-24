"""Recover and complete the explicitly approved Batch 14 Facebook replies.

This script is idempotent after a partial publication: it first searches for
an exact visible Page reply under every approved target. It POSTs only when no
exact reply exists, then verifies every target. For a nested target, Meta may
return the root thread ID as parent.id; that documented semantics is accepted.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json"
PARTIAL = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30

proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
targets = [item for item in proposal_data.get("proposals", []) if item.get("approval_status") == "Pendiente_Fernando"]
if len(targets) != 13:
    raise SystemExit(f"EXPECTED_13_APPROVED_PROPOSALS: {len(targets)}")

partial = json.loads(PARTIAL.read_text(encoding="utf-8")) if PARTIAL.exists() else {}
partial_by_parent = {row.get("parent_comment_id"): row for row in partial.get("results", [])}
base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

session = requests.Session()

def request(method, path, token, *, params=None, form=None):
    response = session.request(
        method,
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        data=form,
        timeout=TIMEOUT,
    )
    if not response.ok:
        try:
            body = response.json()
        except ValueError:
            body = response.text[:500]
        raise RuntimeError(json.dumps({"http_status": response.status_code, "path": path, "body": body}, ensure_ascii=False))
    return response.json()

accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

fields = "id,from,message,created_time,parent,is_hidden"
recovery_started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for item in targets:
    target_id = item["comment_id"]
    children = request("GET", f"{target_id}/comments", page_token, params={"fields": fields, "limit": 100}).get("data", [])
    target_parent_id_returned = None
    if item.get("comment_type") == "Replica_Anidada":
        target_object = request("GET", target_id, page_token, params={"fields": fields})
        target_parent_id_returned = (target_object.get("parent") or {}).get("id")
    exact = next((child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") == item["suggested_reply"] and child.get("is_hidden") is False), None)
    other_page = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") != item["suggested_reply"]]
    if exact is None and other_page:
        raise SystemExit(json.dumps({"preflight_conflict": target_id, "existing_page_reply_ids": [child.get("id") for child in other_page]}, ensure_ascii=False))

    if exact is not None:
        previous = partial_by_parent.get(target_id, {})
        status = "recovered_after_partial_publish" if previous and previous.get("status") == "published" and not previous.get("verified") else "already_published"
        verified = exact
        recovery_posted = False
    else:
        created = request("POST", f"{target_id}/comments", page_token, form={"message": item["suggested_reply"]})
        reply_id = created.get("id")
        if not reply_id:
            raise RuntimeError(json.dumps({"missing_reply_id": target_id, "created_response": created}, ensure_ascii=False))
        verified = request("GET", reply_id, page_token, params={"fields": fields})
        status = "published"
        recovery_posted = True

    returned_parent = (verified.get("parent") or {}).get("id")
    is_nested = item.get("comment_type") == "Replica_Anidada"
    target_root_parent = item.get("parent_comment_id")
    if returned_parent == target_id:
        parent_semantics = "direct_parent"
        parent_ok = True
    elif is_nested and target_parent_id_returned and returned_parent == target_parent_id_returned:
        parent_semantics = "nested_reply_api_returns_immediate_parent"
        parent_ok = True
    elif is_nested and target_root_parent and returned_parent == target_root_parent:
        parent_semantics = "nested_reply_api_returns_root_parent"
        parent_ok = True
    else:
        parent_semantics = "unexpected_parent"
        parent_ok = False
    verified_ok = ((verified.get("from") or {}).get("id") == PAGE_ID and verified.get("message") == item["suggested_reply"] and verified.get("is_hidden") is False and parent_ok)
    record = {
        "status": status,
        "recovery_posted": recovery_posted,
        "parent_comment_id": target_id,
        "comment_type": item.get("comment_type"),
        "comment_message": item.get("comment_message", ""),
        "post_message": item.get("post_message", ""),
        "reply_id": verified.get("id"),
        "message": verified.get("message"),
        "from_id": (verified.get("from") or {}).get("id"),
        "from_name": (verified.get("from") or {}).get("name"),
        "parent_id_returned": returned_parent,
        "target_root_parent_id": target_root_parent,
        "target_parent_id_returned": target_parent_id_returned,
        "parent_semantics": parent_semantics,
        "is_hidden": verified.get("is_hidden"),
        "verified": verified_ok,
    }
    results.append(record)
    if not verified_ok:
        raise RuntimeError(json.dumps({"verification_failed": record}, ensure_ascii=False))

payload = {
    "title": "Facebook Comment Publication Batch 14 — Approved Replies",
    "purpose": "Evidencia final de publicación y verificación de las 13 respuestas aprobadas explícitamente por Fernando; recupera una ejecución parcial sin repetir respuestas.",
    "status": "Active",
    "created_at": partial.get("created_at", recovery_started_at),
    "updated_at": recovery_started_at,
    "version": "1.1",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.md",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "published_at": recovery_started_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "approval_source": "Fernando aprobó las 13 respuestas en conversación antes de la ejecución.",
    "requested_count": len(targets),
    "published_count": len(results),
    "already_published_before_recovery_count": sum(1 for row in results if row["status"] == "already_published"),
    "recovered_after_partial_publish_count": sum(1 for row in results if row["status"] == "recovered_after_partial_publish"),
    "published_during_recovery_count": sum(1 for row in results if row["status"] == "published"),
    "verified_count": sum(1 for row in results if row["verified"]),
    "strict_direct_parent_count": sum(1 for row in results if row["parent_semantics"] == "direct_parent"),
    "nested_reply_parent_semantics_count": sum(1 for row in results if row["parent_semantics"] in {"nested_reply_api_returns_immediate_parent", "nested_reply_api_returns_root_parent"}),
    "nested_immediate_parent_semantics_count": sum(1 for row in results if row["parent_semantics"] == "nested_reply_api_returns_immediate_parent"),
    "nested_root_parent_semantics_count": sum(1 for row in results if row["parent_semantics"] == "nested_reply_api_returns_root_parent"),
    "inaccessible_count": 0,
    "no_duplicate_posts": True,
    "results": results,
}
if payload["verified_count"] != 13:
    raise SystemExit("EXPECTED_13_VERIFIED_RESULTS")
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_before_recovery_count", "recovered_after_partial_publish_count", "published_during_recovery_count", "verified_count", "strict_direct_parent_count", "nested_reply_parent_semantics_count", "nested_immediate_parent_semantics_count", "nested_root_parent_semantics_count")}, ensure_ascii=False))
for result in results:
    print(json.dumps(result, ensure_ascii=False))
