"""Publish exactly the 13 explicitly approved Batch 14 Facebook replies.

Safety properties:
- Reads the approved proposal artifact and refuses any count mismatch.
- Performs all duplicate/conflict preflights before the first POST.
- Publishes only to the specified comment/reply IDs.
- Verifies Page authorship, exact text, visibility, and direct/nested parent semantics.
- Writes a partial evidence file if an unexpected write-time error occurs.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30

proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
targets = [item for item in proposal_data.get("proposals", []) if item.get("approval_status") == "Pendiente_Fernando"]
if len(proposal_data.get("proposals", [])) != 13 or len(targets) != 13:
    raise SystemExit(f"EXPECTED_13_APPROVED_PROPOSALS: total={len(proposal_data.get('proposals', []))}, pending={len(targets)}")
if proposal_data.get("published") is True:
    raise SystemExit("PROPOSAL_ARTIFACT_ALREADY_MARKED_PUBLISHED")
if any(not item.get("suggested_reply") for item in targets):
    raise SystemExit("TARGET_WITHOUT_MESSAGE")

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

published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
prechecks = []
for item in targets:
    parent_id = item["comment_id"]
    children = request("GET", f"{parent_id}/comments", page_token, params={"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}).get("data", [])
    exact = next((child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") == item["suggested_reply"] and child.get("is_hidden") is False), None)
    other_page = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") != item["suggested_reply"]]
    if other_page and exact is None:
        raise SystemExit(json.dumps({"preflight_conflict": parent_id, "existing_page_reply_ids": [child.get("id") for child in other_page]}, ensure_ascii=False))
    prechecks.append({"target": item, "existing_exact": exact})

results = []
try:
    for check in prechecks:
        item = check["target"]
        parent_id = item["comment_id"]
        existing = check["existing_exact"]
        if existing is not None:
            verified = existing
            status = "already_published"
        else:
            created = request("POST", f"{parent_id}/comments", page_token, form={"message": item["suggested_reply"]})
            reply_id = created.get("id")
            if not reply_id:
                raise RuntimeError(json.dumps({"missing_reply_id": parent_id, "created_response": created}, ensure_ascii=False))
            verified = request("GET", reply_id, page_token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
            status = "published"
        returned_parent = (verified.get("parent") or {}).get("id")
        expected_parent = parent_id
        is_nested = item.get("comment_type") == "Replica_Anidada"
        target_root_parent = item.get("parent_comment_id")
        if returned_parent == expected_parent:
            parent_semantics = "direct_parent"
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
            "parent_comment_id": parent_id,
            "comment_type": item.get("comment_type"),
            "comment_message": item.get("comment_message", ""),
            "post_message": item.get("post_message", ""),
            "reply_id": verified.get("id"),
            "message": verified.get("message"),
            "from_id": (verified.get("from") or {}).get("id"),
            "from_name": (verified.get("from") or {}).get("name"),
            "parent_id_returned": returned_parent,
            "parent_semantics": parent_semantics,
            "is_hidden": verified.get("is_hidden"),
            "verified": verified_ok,
        }
        results.append(record)
        if not verified_ok:
            raise RuntimeError(json.dumps({"verification_failed": record}, ensure_ascii=False))
except Exception as exc:
    partial = {
        "title": "Facebook Comment Publication Batch 14 — partial evidence",
        "purpose": "Evidence parcial de publicación; revisar antes de cualquier recuperación. No reintentar automáticamente.",
        "status": "Review",
        "created_at": published_at,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "0.1",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "requested_count": len(targets),
        "published_or_found_count": len(results),
        "verified_count": sum(1 for row in results if row.get("verified")),
        "error": str(exc),
        "results": results,
    }
    OUT.write_text(json.dumps(partial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise

payload = {
    "title": "Facebook Comment Publication Batch 14 — Approved Replies",
    "purpose": "Evidencia de publicación y verificación de las 13 respuestas aprobadas explícitamente por Fernando; no incluye otros comentarios.",
    "status": "Active",
    "created_at": published_at,
    "updated_at": published_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "published_at": published_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "approval_source": "Fernando aprobó las 13 respuestas en conversación antes de la ejecución.",
    "requested_count": len(targets),
    "published_count": sum(1 for result in results if result["status"] == "published"),
    "already_published_count": sum(1 for result in results if result["status"] == "already_published"),
    "verified_count": sum(1 for result in results if result["verified"]),
    "strict_direct_parent_count": sum(1 for result in results if result["parent_semantics"] == "direct_parent"),
    "nested_root_parent_semantics_count": sum(1 for result in results if result["parent_semantics"] == "nested_reply_api_returns_root_parent"),
    "inaccessible_count": 0,
    "results": results,
}
if payload["verified_count"] != 13:
    raise SystemExit("EXPECTED_13_VERIFIED_RESULTS")
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count", "strict_direct_parent_count", "nested_root_parent_semantics_count")}, ensure_ascii=False))
for result in results:
    print(json.dumps(result, ensure_ascii=False))
