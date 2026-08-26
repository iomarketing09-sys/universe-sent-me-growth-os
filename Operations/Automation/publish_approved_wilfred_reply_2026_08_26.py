#!/usr/bin/env python3
"""Publish exactly the one Facebook reply explicitly approved by Fernando."""
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
QUEUE = RESEARCH / "2026-08-26_18-15-41_Facebook_Pending_Queue_GET_Only.json"
OUT = RESEARCH / "2026-08-26_18-24-00_Facebook_Wilfred_Publication.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TARGET_ID = "122151377553072582_1857148135657699"
EXPECTED_REPLY = "Wilfred ya tomó nota: un guiño y un toque de canela. 🌲😂"
TIMEOUT = 30
MAX_PAGES = 20

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
targets = [item for item in queue.get("pending_comments", []) if item.get("comment_id") == TARGET_ID]
if len(targets) != 1:
    raise SystemExit(f"TARGET_QUEUE_MISMATCH:{len(targets)}")
target = targets[0]
if target.get("candidate_reply") != EXPECTED_REPLY:
    raise SystemExit("TARGET_REPLY_MISMATCH")
if target.get("approval_status") not in ("Pendiente_Fernando", "Aprobada"):
    raise SystemExit(f"TARGET_APPROVAL_STATE_UNEXPECTED:{target.get('approval_status')}")

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
    response = session.request(method, url, headers={"Authorization": f"Bearer {token}"}, params=params, data=form, timeout=TIMEOUT)
    body = decode(response)
    if not response.ok:
        raise RuntimeError(json.dumps({"http_status": response.status_code, "body": body}, ensure_ascii=False))
    return body


def paged_children(comment_id: str, token: str) -> list[dict[str, Any]]:
    url: str | None = f"{GRAPH}/{comment_id}/comments"
    params: dict[str, Any] | None = {"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}
    children: list[dict[str, Any]] = []
    for _ in range(MAX_PAGES):
        if not url:
            break
        body = request("GET", url, token, params=params)
        params = None
        children.extend(body.get("data", []))
        url = (body.get("paging") or {}).get("next")
    return children


def verify_reply(reply_id: str, token: str) -> dict[str, Any]:
    last_error = None
    for delay in (0, 1, 2, 3):
        if delay:
            time.sleep(delay)
        try:
            return request("GET", reply_id, token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
    raise RuntimeError(last_error or "verification failed")


def compact(reply: dict[str, Any] | None) -> dict[str, Any] | None:
    if reply is None:
        return None
    return {
        "id": reply.get("id"),
        "message": reply.get("message"),
        "created_time": reply.get("created_time"),
        "is_hidden": reply.get("is_hidden"),
        "from_id": (reply.get("from") or {}).get("id"),
        "parent_id": (reply.get("parent") or {}).get("id"),
    }


accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]
started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

comment = request("GET", TARGET_ID, page_token, params={"fields": "id,message,created_time,parent,is_hidden"})
children = paged_children(TARGET_ID, page_token)
page_replies = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID]
exact = next((child for child in page_replies if child.get("message") == EXPECTED_REPLY and child.get("is_hidden") is False), None)
conflicts = [child for child in page_replies if child.get("message") != EXPECTED_REPLY]
if conflicts and exact is None:
    blocked = {
        "title": "Facebook Wilfred Reply — blocked preflight",
        "purpose": "Evidence that the explicitly approved Wilfred reply was not published because a conflicting Page reply exists.",
        "status": "Blocked_Preflight",
        "created_at": started_at,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [str(QUEUE.relative_to(ROOT)), "Operations/Research/2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json"],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "target_comment_id": TARGET_ID,
        "proposed_reply": EXPECTED_REPLY,
        "preflight": {"target_is_hidden": comment.get("is_hidden"), "child_count": len(children), "page_reply_count": len(page_replies), "existing_exact": compact(exact), "conflicting_page_replies": [compact(item) for item in conflicts]},
        "post_attempted": False,
        "error": "conflicting_page_reply_without_exact_match",
    }
    OUT.write_text(json.dumps(blocked, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise SystemExit("CONFLICTING_PAGE_REPLY")

if exact is not None:
    reply_id = exact.get("id")
    verified = verify_reply(reply_id, page_token)
    status = "already_published"
else:
    created = request("POST", f"{TARGET_ID}/comments", page_token, form={"message": EXPECTED_REPLY})
    reply_id = created.get("id")
    if not reply_id:
        raise SystemExit("MISSING_CREATED_REPLY_ID")
    verified = verify_reply(reply_id, page_token)
    status = "published"

returned_parent = (verified.get("parent") or {}).get("id")
verified_ok = (
    (verified.get("from") or {}).get("id") == PAGE_ID
    and verified.get("message") == EXPECTED_REPLY
    and verified.get("is_hidden") is False
    and returned_parent == TARGET_ID
)
record = {
    "status": status,
    "parent_comment_id": TARGET_ID,
    "comment_type": "Comentario_Raiz",
    "post_id": target.get("post_id"),
    "post_reference": target.get("post_reference"),
    "proposed_reply": EXPECTED_REPLY,
    "reply_id": verified.get("id"),
    "message": verified.get("message"),
    "from_id": (verified.get("from") or {}).get("id"),
    "parent_id_returned": returned_parent,
    "created_time": verified.get("created_time"),
    "is_hidden": verified.get("is_hidden"),
    "verified": verified_ok,
}
if not verified_ok:
    raise SystemExit(json.dumps({"verification_failed": record}, ensure_ascii=False))

payload = {
    "title": "Facebook Wilfred Reply — explicit approval publication",
    "purpose": "Evidence of publication and verification for exactly one reply explicitly approved by Fernando.",
    "status": "Active",
    "created_at": started_at,
    "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [str(QUEUE.relative_to(ROOT)), "Operations/Research/2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json", "Operations/Research/2026-08-15_Community_Engagement_Log.csv"],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "approval_source": "Fernando aprobó explícitamente la respuesta propuesta para el comentario de Wilfred en la conversación actual.",
    "requested_count": 1,
    "published_count": 1 if status == "published" else 0,
    "already_published_count": 1 if status == "already_published" else 0,
    "verified_count": 1,
    "preflight": {"target_comment_id": TARGET_ID, "target_is_hidden": comment.get("is_hidden"), "child_count": len(children), "page_reply_count": len(page_replies), "existing_exact_before_post": compact(exact), "conflicting_page_reply_count": len(conflicts)},
    "result": record,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": status, "published_count": payload["published_count"], "already_published_count": payload["already_published_count"], "verified_count": 1, "reply_id": verified.get("id")}, ensure_ascii=False))
