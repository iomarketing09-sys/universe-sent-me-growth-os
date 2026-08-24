"""Publish exactly the 24 explicitly approved Facebook replies after Batch 14.

This script is intentionally one-shot and idempotent. It performs a complete
preflight before the first POST, detects existing exact Page replies, blocks on
conflicting Page replies, verifies each write, and accepts Meta's observed
parent semantics for the single nested target.
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
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Batch14.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
EXPECTED = 24
TIMEOUT = 30
MAX_PAGES = 20

proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
targets = [
    row
    for row in proposal_data.get("records", [])
    if row.get("editorial_decision") == "Pendiente_Respuesta"
    and row.get("approval_state") == "Pendiente_Fernando"
]
if len(targets) != EXPECTED:
    raise SystemExit(f"EXPECTED_{EXPECTED}_APPROVED_PROPOSALS: found={len(targets)}")
if any(not row.get("proposed_reply") or row.get("proposed_reply") == "No responder" for row in targets):
    raise SystemExit("TARGET_WITHOUT_APPROVED_REPLY")
if any(row.get("publication_count", 0) != 0 for row in targets):
    raise SystemExit("TARGET_ALREADY_RECORDED_AS_PUBLISHED")

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


def paged_comments(comment_id: str, token: str) -> list[dict[str, Any]]:
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


def fetch_with_retry(reply_id: str, token: str) -> dict[str, Any]:
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
        except Exception as exc:  # noqa: BLE001 - preserve exact API error in evidence
            last_error = str(exc)
    raise RuntimeError(last_error or f"Unable to verify {reply_id}")


accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
prechecks: list[dict[str, Any]] = []
for row in targets:
    target_id = row["comment_id"]
    target_details = request(
        "GET",
        target_id,
        page_token,
        params={"fields": "id,message,created_time,parent,is_hidden"},
    )
    children = paged_comments(target_id, page_token)
    exact = next(
        (
            child
            for child in children
            if (child.get("from") or {}).get("id") == PAGE_ID
            and child.get("message") == row["proposed_reply"]
            and child.get("is_hidden") is False
        ),
        None,
    )
    conflicting = [
        child
        for child in children
        if (child.get("from") or {}).get("id") == PAGE_ID
        and child.get("message") != row["proposed_reply"]
    ]
    if conflicting and exact is None:
        raise SystemExit(
            json.dumps(
                {
                    "preflight_conflict": target_id,
                    "existing_page_reply_ids": [child.get("id") for child in conflicting],
                },
                ensure_ascii=False,
            )
        )
    target_parent_id = (target_details.get("parent") or {}).get("id")
    prechecks.append(
        {
            "target": row,
            "target_parent_id": target_parent_id,
            "existing_exact": exact,
            "existing_child_count": len(children),
        }
    )

results: list[dict[str, Any]] = []
try:
    for check in prechecks:
        row = check["target"]
        target_id = row["comment_id"]
        existing = check["existing_exact"]
        if existing is not None:
            verified = existing
            status = "already_published"
        else:
            created = request(
                "POST",
                f"{target_id}/comments",
                page_token,
                form={"message": row["proposed_reply"]},
            )
            reply_id = created.get("id")
            if not reply_id:
                raise RuntimeError(json.dumps({"missing_reply_id": target_id, "created_response": created}, ensure_ascii=False))
            verified = fetch_with_retry(reply_id, page_token)
            status = "published"

        returned_parent = (verified.get("parent") or {}).get("id")
        expected_parent = target_id
        target_parent_id = check.get("target_parent_id")
        is_nested = row.get("comment_type") == "Replica_Anidada" or bool(target_parent_id)
        if returned_parent == expected_parent:
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
            "post_message": row.get("post_message", ""),
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
except Exception as exc:  # noqa: BLE001 - write recovery evidence before failing
    partial = {
        "title": "Facebook Comment Publication — post-Batch 14 partial evidence",
        "purpose": "Partial evidence for the 24 explicitly approved replies; inspect before any recovery. No automatic retry.",
        "status": "Review",
        "created_at": started_at,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "0.1",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "requested_count": len(targets),
        "published_or_found_count": len(results),
        "verified_count": sum(1 for result in results if result.get("verified")),
        "error": str(exc),
        "results": results,
    }
    OUT.write_text(json.dumps(partial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise

finished_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "title": "Facebook Comment Publication — 24 Approved Replies After Batch 14",
    "purpose": "Evidence of publication and verification for the 24 replies explicitly approved by Fernando; no other comments are included.",
    "status": "Active",
    "created_at": started_at,
    "updated_at": finished_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Batch14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "published_at": finished_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "approval_source": "Fernando aprobó las 24 respuestas en conversación antes de la ejecución.",
    "requested_count": len(targets),
    "published_count": sum(1 for result in results if result["status"] == "published"),
    "already_published_count": sum(1 for result in results if result["status"] == "already_published"),
    "verified_count": sum(1 for result in results if result["verified"]),
    "strict_direct_parent_count": sum(1 for result in results if result["parent_semantics"] == "direct_target_parent"),
    "nested_target_parent_semantics_count": sum(1 for result in results if result["parent_semantics"] == "nested_reply_api_returns_target_parent"),
    "inaccessible_count": 0,
    "results": results,
}
if payload["verified_count"] != EXPECTED:
    raise SystemExit(f"EXPECTED_{EXPECTED}_VERIFIED_RESULTS: got={payload['verified_count']}")
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count", "strict_direct_parent_count", "nested_target_parent_semantics_count")}, ensure_ascii=False))
for result in results:
    print(json.dumps(result, ensure_ascii=False))
