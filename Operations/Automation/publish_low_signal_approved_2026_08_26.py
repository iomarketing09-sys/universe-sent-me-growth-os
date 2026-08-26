#!/usr/bin/env python3
"""Publish exactly four low-signal Facebook replies approved by Fernando."""
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
QUEUE = RESEARCH / "2026-08-26_18-38-17_Facebook_Pending_Queue_Low_Signal_Proposals.json"
OUT = RESEARCH / "2026-08-26_18-44-00_Facebook_Low_Signal_Publication.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30
MAX_PAGES = 20
TARGETS = {
    "122151377649072582_2511249876017099": {
        "post_id": "1036844829507460_122151377649072582",
        "reply": "Jajaja, ese «ni voy» sonó a que de aquí no te mueve nadie. 😂",
    },
    "122151377649072582_2227921178135227": {
        "post_id": "1036844829507460_122151377649072582",
        "reply": "El universo confirmó que aquí nadie se escapa tan fácil. 👁️🔥",
    },
    "122151377109072582_1103053779073759": {
        "post_id": "1036844829507460_122151377109072582",
        "reply": "Ese «seeeee» sonó a confirmación oficial. 😂",
    },
    "122151377109072582_28380292711566338": {
        "post_id": "1036844829507460_122151377109072582",
        "reply": "Jajaja, el recuerdo llegó sin tocar la puerta. 😅",
    },
}

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
queue_targets = {item.get("comment_id"): item for item in queue.get("pending_comments", [])}
if set(queue_targets) != set(TARGETS):
    raise SystemExit(f"AUTHORIZED_TARGET_SET_MISMATCH:{sorted(queue_targets)}")
if any(queue_targets[cid].get("approval_status") != "Pendiente_Fernando" for cid in TARGETS):
    raise SystemExit("UNEXPECTED_APPROVAL_STATE")

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


def children(comment_id: str, token: str) -> list[dict[str, Any]]:
    url: str | None = f"{GRAPH}/{comment_id}/comments"
    params: dict[str, Any] | None = {"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}
    rows: list[dict[str, Any]] = []
    for _ in range(MAX_PAGES):
        if not url:
            break
        body = request("GET", url, token, params=params)
        params = None
        rows.extend(body.get("data", []))
        url = (body.get("paging") or {}).get("next")
    return rows


def verify(reply_id: str, token: str) -> dict[str, Any]:
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
preflight: dict[str, dict[str, Any]] = {}

try:
    for cid, target in TARGETS.items():
        target_details = request("GET", cid, page_token, params={"fields": "id,message,created_time,parent,is_hidden"})
        child_rows = children(cid, page_token)
        page_replies = [item for item in child_rows if (item.get("from") or {}).get("id") == PAGE_ID]
        exact = next((item for item in page_replies if item.get("message") == target["reply"] and item.get("is_hidden") is False), None)
        conflicts = [item for item in page_replies if item.get("message") != target["reply"]]
        if conflicts and exact is None:
            raise RuntimeError(json.dumps({"preflight_conflict": cid, "existing_page_reply_ids": [item.get("id") for item in conflicts]}, ensure_ascii=False))
        preflight[cid] = {
            "target_is_hidden": target_details.get("is_hidden"),
            "child_count": len(child_rows),
            "page_reply_count": len(page_replies),
            "existing_exact": compact(exact),
            "conflicting_page_reply_count": len(conflicts),
        }
except Exception as exc:
    blocked = {
        "title": "Facebook Low-Signal Publication — blocked at preflight",
        "purpose": "Evidence that the four explicitly approved low-signal replies were not published because preflight failed or found a conflict.",
        "status": "Blocked_Preflight",
        "created_at": started_at,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [str(QUEUE.relative_to(ROOT)), "Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json"],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "requested_count": len(TARGETS),
        "preflight_completed_count": len(preflight),
        "published_count": 0,
        "verified_count": 0,
        "error": str(exc),
        "preflight": preflight,
    }
    OUT.write_text(json.dumps(blocked, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise

results: list[dict[str, Any]] = []
for cid, target in TARGETS.items():
    existing = preflight[cid].get("existing_exact")
    if existing is not None:
        reply_id = existing.get("id")
        verified = verify(reply_id, page_token)
        status = "already_published"
    else:
        created = request("POST", f"{cid}/comments", page_token, form={"message": target["reply"]})
        reply_id = created.get("id")
        if not reply_id:
            raise SystemExit(f"MISSING_CREATED_REPLY_ID:{cid}")
        verified = verify(reply_id, page_token)
        status = "published"
    returned_parent = (verified.get("parent") or {}).get("id")
    verified_ok = (
        (verified.get("from") or {}).get("id") == PAGE_ID
        and verified.get("message") == target["reply"]
        and verified.get("is_hidden") is False
        and returned_parent == cid
    )
    record = {
        "status": status,
        "parent_comment_id": cid,
        "post_id": target["post_id"],
        "proposed_reply": target["reply"],
        "reply_id": verified.get("id"),
        "message": verified.get("message"),
        "from_id": (verified.get("from") or {}).get("id"),
        "parent_id_returned": returned_parent,
        "created_time": verified.get("created_time"),
        "is_hidden": verified.get("is_hidden"),
        "verified": verified_ok,
    }
    results.append(record)
    if not verified_ok:
        raise SystemExit(json.dumps({"verification_failed": record}, ensure_ascii=False))

payload = {
    "title": "Facebook Low-Signal Publication — four approved replies",
    "purpose": "Evidence of publication and verification for exactly the four low-signal replies explicitly approved by Fernando.",
    "status": "Active",
    "created_at": started_at,
    "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [str(QUEUE.relative_to(ROOT)), "Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json", "Operations/Research/2026-08-15_Community_Engagement_Log.csv"],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "explicit_user_approval": True,
    "approval_source": "Fernando autorizó explícitamente las cuatro respuestas de baja señal en la conversación actual y corrigió el primer texto.",
    "requested_count": len(TARGETS),
    "published_count": sum(1 for item in results if item["status"] == "published"),
    "already_published_count": sum(1 for item in results if item["status"] == "already_published"),
    "verified_count": sum(1 for item in results if item["verified"]),
    "strict_direct_parent_count": sum(1 for item in results if item["parent_id_returned"] == item["parent_comment_id"]),
    "preflight": preflight,
    "results": results,
}
if payload["verified_count"] != len(TARGETS):
    raise SystemExit("EXPECTED_FOUR_VERIFIED_RESULTS")
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count", "strict_direct_parent_count")}, ensure_ascii=False))
for item in results:
    print(json.dumps(item, ensure_ascii=False))
