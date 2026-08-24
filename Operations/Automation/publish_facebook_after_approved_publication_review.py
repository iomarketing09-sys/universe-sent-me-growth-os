"""Publish exactly the five replies explicitly approved by Fernando.

The script is one-shot and idempotent. It uses Meta Graph API v26.0 only,
performs a complete GET preflight before the first POST, blocks on conflicting
Page replies, and verifies author, exact text, visibility, and parent semantics
for every published or already-existing exact reply.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
PROPOSALS = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json"
OUT = RESEARCH / "2026-08-24_Facebook_Comment_Publication_After_Approved_Publication_Review.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
EXPECTED = 5
TIMEOUT = 30
MAX_PAGES = 20
EXPECTED_IDS = {
    "122151376539072582_1063233976446841",
    "122151376539072582_2056563468318334",
    "122151376539072582_1406586844746099",
    "122151376083072582_1036099909244517",
    "122151376083072582_1620854262795787",
}

proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
targets = [
    row
    for row in proposal_data.get("records", [])
    if row.get("editorial_decision") == "Pendiente_Respuesta"
    and row.get("approval_state") == "Pendiente_Fernando"
]
if len(targets) != EXPECTED or {row.get("comment_id") for row in targets} != EXPECTED_IDS:
    raise SystemExit(f"AUTHORIZED_TARGET_SET_MISMATCH: expected={sorted(EXPECTED_IDS)} found={[row.get('comment_id') for row in targets]}")
if any(not row.get("proposed_reply") or row.get("proposed_reply") == "No responder" for row in targets):
    raise SystemExit("TARGET_WITHOUT_PROPOSED_REPLY")

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

session = requests.Session()


def decode(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text[:1000]}


def request(method: str, path_or_url: str, token: str, *, params: dict[str, Any] | None = None, form: dict[str, Any] | None = None) -> Any:
    url = path_or_url if path_or_url.startswith("http") else f"{GRAPH}/{path_or_url.lstrip('/')}"
    response = session.request(
        method,
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        data=form,
        timeout=TIMEOUT,
    )
    body = decode(response)
    if not response.ok:
        raise RuntimeError(json.dumps({"http_status": response.status_code, "url": url, "body": body}, ensure_ascii=False))
    return body


def paged_children(comment_id: str, token: str) -> list[dict[str, Any]]:
    url: str | None = f"{GRAPH}/{comment_id}/comments"
    params: dict[str, Any] | None = {
        "fields": "id,from,message,created_time,parent,is_hidden",
        "limit": 100,
    }
    rows: list[dict[str, Any]] = []
    for _ in range(MAX_PAGES):
        if not url:
            break
        body = request("GET", url, token, params=params)
        params = None
        rows.extend(body.get("data", []))
        url = (body.get("paging") or {}).get("next")
    return rows


def fetch_verified(reply_id: str, token: str) -> dict[str, Any]:
    last_error: str | None = None
    for delay in (0, 1, 2, 3):
        if delay:
            time.sleep(delay)
        try:
            return request(
                "GET",
                reply_id,
                token,
                params={"fields": "id,from,message,created_time,parent,is_hidden"},
            )
        except Exception as exc:  # noqa: BLE001 - evidence must retain the exact failure
            last_error = str(exc)
    raise RuntimeError(last_error or f"Unable to verify {reply_id}")


def compact_page_reply(reply: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": reply.get("id"),
        "message": reply.get("message"),
        "created_time": reply.get("created_time"),
        "is_hidden": reply.get("is_hidden"),
        "from_id": (reply.get("from") or {}).get("id"),
        "parent_id": (reply.get("parent") or {}).get("id"),
    }


accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
prechecks: list[dict[str, Any]] = []
try:
    for row in targets:
        target_id = row["comment_id"]
        target_details = request(
            "GET",
            target_id,
            page_token,
            params={"fields": "id,message,created_time,parent,is_hidden"},
        )
        children = paged_children(target_id, page_token)
        page_replies = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID]
        exact = next(
            (
                child
                for child in page_replies
                if child.get("message") == row["proposed_reply"] and child.get("is_hidden") is False
            ),
            None,
        )
        conflicting = [child for child in page_replies if child.get("message") != row["proposed_reply"]]
        if conflicting and exact is None:
            raise RuntimeError(
                json.dumps(
                    {
                        "preflight_conflict": target_id,
                        "existing_page_reply_ids": [child.get("id") for child in conflicting],
                    },
                    ensure_ascii=False,
                )
            )
        prechecks.append(
            {
                "target": row,
                "target_parent_id": (target_details.get("parent") or {}).get("id"),
                "target_is_hidden": target_details.get("is_hidden"),
                "existing_child_count": len(children),
                "existing_page_reply_count": len(page_replies),
                "existing_exact": compact_page_reply(exact) if exact else None,
            }
        )
except Exception as exc:  # no POST is attempted when preflight is incomplete
    blocked = {
        "title": "Facebook Comment Publication — five approved replies blocked at preflight",
        "purpose": "Evidence that the exact five-comment authorization was not written because preflight failed or found a conflicting Page reply.",
        "status": "Blocked_Preflight",
        "created_at": started_at,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "requested_count": EXPECTED,
        "preflight_completed_count": len(prechecks),
        "published_count": 0,
        "verified_count": 0,
        "error": str(exc),
        "results": [],
    }
    OUT.write_text(json.dumps(blocked, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise

results: list[dict[str, Any]] = []
try:
    for check in prechecks:
        row = check["target"]
        target_id = row["comment_id"]
        existing = check["existing_exact"]
        if existing is not None:
            verified = fetch_verified(existing["id"], page_token)
            status = "already_published"
        else:
            created = request("POST", f"{target_id}/comments", page_token, form={"message": row["proposed_reply"]})
            reply_id = created.get("id")
            if not reply_id:
                raise RuntimeError(json.dumps({"missing_reply_id": target_id, "created_response": created}, ensure_ascii=False))
            verified = fetch_verified(reply_id, page_token)
            status = "published"

        returned_parent = (verified.get("parent") or {}).get("id")
        target_parent_id = check.get("target_parent_id")
        is_nested = row.get("comment_type") == "Replica_Anidada" or bool(target_parent_id)
        if returned_parent == target_id:
            parent_semantics = "direct_target_parent"
            parent_ok = True
        elif is_nested and target_parent_id and returned_parent == target_parent_id:
            parent_semantics = "nested_reply_api_returns_target_parent"
            parent_ok = True
        else:
            parent_semantics = "unexpected_parent"
            parent_ok = False

        verified_ok = (
            (verified.get("from") or {}).get("id") == PAGE_ID
            and verified.get("message") == row["proposed_reply"]
            and verified.get("is_hidden") is False
            and parent_ok
        )
        record = {
            "status": status,
            "parent_comment_id": target_id,
            "comment_type": row.get("comment_type"),
            "comment_message": row.get("comment_message", ""),
            "post_id": row.get("post_id", ""),
            "post_reference": row.get("post_reference", ""),
            "proposed_reply": row["proposed_reply"],
            "reply_id": verified.get("id"),
            "message": verified.get("message"),
            "from_id": (verified.get("from") or {}).get("id"),
            "parent_id_returned": returned_parent,
            "target_parent_id_from_meta": target_parent_id,
            "parent_semantics": parent_semantics,
            "created_time": verified.get("created_time"),
            "is_hidden": verified.get("is_hidden"),
            "verified": verified_ok,
        }
        results.append(record)
        if not verified_ok:
            raise RuntimeError(json.dumps({"verification_failed": record}, ensure_ascii=False))
except Exception as exc:  # write recovery evidence and never auto-retry
    partial = {
        "title": "Facebook Comment Publication — five approved replies partial evidence",
        "purpose": "Partial evidence for the five explicitly approved replies; inspect before any recovery. No automatic retry.",
        "status": "Review",
        "created_at": started_at,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "0.1",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json",
            "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "requested_count": EXPECTED,
        "preflight_completed_count": len(prechecks),
        "published_or_found_count": len(results),
        "verified_count": sum(1 for result in results if result.get("verified")),
        "error": str(exc),
        "results": results,
    }
    OUT.write_text(json.dumps(partial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise

finished_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "title": "Facebook Comment Publication — five Approved Replies After Approved Publication Review",
    "purpose": "Evidence of publication and verification for exactly the five replies explicitly approved by Fernando; no other comments are included.",
    "status": "Active",
    "created_at": started_at,
    "updated_at": finished_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "published_at": finished_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "approval_source": "Fernando autorizó explícitamente las cinco respuestas propuestas en conversación antes de la ejecución.",
    "requested_count": EXPECTED,
    "published_count": sum(1 for result in results if result["status"] == "published"),
    "already_published_count": sum(1 for result in results if result["status"] == "already_published"),
    "verified_count": sum(1 for result in results if result["verified"]),
    "strict_direct_parent_count": sum(1 for result in results if result["parent_semantics"] == "direct_target_parent"),
    "nested_target_parent_semantics_count": sum(1 for result in results if result["parent_semantics"] == "nested_reply_api_returns_target_parent"),
    "inaccessible_count": 0,
    "preflight": [
        {
            "comment_id": check["target"]["comment_id"],
            "target_parent_id": check.get("target_parent_id"),
            "target_is_hidden": check.get("target_is_hidden"),
            "existing_child_count": check.get("existing_child_count"),
            "existing_page_reply_count": check.get("existing_page_reply_count"),
            "existing_exact": check.get("existing_exact"),
        }
        for check in prechecks
    ],
    "results": results,
}
if payload["verified_count"] != EXPECTED:
    raise SystemExit(f"EXPECTED_{EXPECTED}_VERIFIED_RESULTS: got={payload['verified_count']}")
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count", "strict_direct_parent_count", "nested_target_parent_semantics_count")}, ensure_ascii=False))
for result in results:
    print(json.dumps(result, ensure_ascii=False))
