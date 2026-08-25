#!/usr/bin/env python3
"""Preflight and publish exactly the eight approved additional Facebook replies."""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
QUEUE = RESEARCH / "2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json"
PREflight = RESEARCH / "2026-08-25_18-49-39_Facebook_Additional_Publication_Preflight.json"
PUBLICATION = RESEARCH / "2026-08-25_18-49-39_Facebook_Additional_Publication.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
EXPECTED = 8
TIMEOUT = 30
MAX_PAGES = 20


def decode(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text[:1000]}


def request(method: str, path_or_url: str, token: str, *, params: dict[str, Any] | None = None, form: dict[str, Any] | None = None) -> Any:
    url = path_or_url if path_or_url.startswith("http") else f"{GRAPH}/{path_or_url.lstrip('/')}"
    response = requests.request(
        method,
        url,
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        data=form,
        timeout=TIMEOUT,
    )
    body = decode(response)
    if not response.ok:
        raise RuntimeError(json.dumps({"http_status": response.status_code, "body": body}, ensure_ascii=False))
    return body


def page_token() -> str:
    base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
    if not base_token:
        raise RuntimeError("META_PAGE_ACCESS_TOKEN is not set")
    accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
    page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
    if not page or not page.get("access_token"):
        raise RuntimeError("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
    return page["access_token"]


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


def compact_reply(reply: dict[str, Any] | None) -> dict[str, Any] | None:
    if not reply:
        return None
    return {
        "id": reply.get("id"),
        "message": reply.get("message"),
        "created_time": reply.get("created_time"),
        "is_hidden": reply.get("is_hidden"),
        "from_id": (reply.get("from") or {}).get("id"),
        "parent_id": (reply.get("parent") or {}).get("id"),
    }


def targets() -> list[dict[str, Any]]:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    rows = queue.get("pending_comments", [])
    if len(rows) != EXPECTED or len({row.get("comment_id") for row in rows}) != EXPECTED:
        raise RuntimeError(f"QUEUE_TARGET_SET_MISMATCH:{len(rows)}")
    if any(row.get("approval_state") != "Aprobada" for row in rows):
        raise RuntimeError("QUEUE_CONTAINS_UNAPPROVED_TARGET")
    if any(row.get("publication_status") != "Pendiente_Publicacion" for row in rows):
        raise RuntimeError("QUEUE_CONTAINS_NON_PENDING_TARGET")
    if any(not row.get("proposed_reply") for row in rows):
        raise RuntimeError("QUEUE_TARGET_WITHOUT_PROPOSED_REPLY")
    return rows


def write_blocked(started: str, checks: list[dict[str, Any]], error: Exception) -> None:
    blocked = {
        "title": "Facebook Additional Publication Preflight — blocked",
        "purpose": "Evidencia del preflight GET-only de las ocho respuestas aprobadas; ningún POST fue ejecutado si el preflight no completó.",
        "status": "Blocked_Preflight",
        "created_at": started,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
            "Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "requested_count": EXPECTED,
        "preflight_completed_count": len(checks),
        "published_count": 0,
        "verified_count": 0,
        "error": str(error),
        "checks": checks,
    }
    PREflight.write_text(json.dumps(blocked, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preflight() -> None:
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = targets()
    token = page_token()
    checks: list[dict[str, Any]] = []
    try:
        for row in rows:
            cid = row["comment_id"]
            target = request("GET", cid, token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
            children = paged_children(cid, token)
            page_replies = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID]
            exact = next((child for child in page_replies if child.get("message") == row["proposed_reply"] and child.get("is_hidden") is False), None)
            conflicting = [child for child in page_replies if child.get("message") != row["proposed_reply"]]
            if target.get("is_hidden") is True:
                raise RuntimeError(json.dumps({"hidden_target": cid}, ensure_ascii=False))
            if conflicting and exact is None:
                raise RuntimeError(json.dumps({"preflight_conflict": cid, "existing_page_reply_ids": [child.get("id") for child in conflicting]}, ensure_ascii=False))
            checks.append({
                "comment_id": cid,
                "post_id": row.get("post_id"),
                "comment_type": "Comentario_Raiz",
                "target_parent_id": (target.get("parent") or {}).get("id"),
                "target_is_hidden": target.get("is_hidden"),
                "existing_child_count": len(children),
                "existing_page_reply_count": len(page_replies),
                "existing_exact": compact_reply(exact),
            })
    except Exception as exc:
        write_blocked(started, checks, exc)
        raise
    payload = {
        "title": "Facebook Additional Publication Preflight — eight approved replies",
        "purpose": "Preflight GET-only completo de las ocho respuestas aprobadas antes de cualquier publicación.",
        "status": "Preflight_Pass",
        "created_at": started,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
            "Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "requested_count": EXPECTED,
        "preflight_completed_count": len(checks),
        "conflict_count": 0,
        "existing_exact_count": sum(1 for check in checks if check["existing_exact"]),
        "published_count": 0,
        "verified_count": 0,
        "checks": checks,
    }
    PREflight.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "requested_count": EXPECTED, "preflight_completed_count": len(checks), "existing_exact_count": payload["existing_exact_count"], "conflict_count": 0, "published_count": 0}, ensure_ascii=False))


def fetch_verified(reply_id: str, token: str) -> dict[str, Any]:
    last_error: str | None = None
    for delay in (0, 1, 2, 3):
        if delay:
            time.sleep(delay)
        try:
            return request("GET", reply_id, token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
        except Exception as exc:
            last_error = str(exc)
    raise RuntimeError(last_error or f"Unable to verify {reply_id}")


def publish() -> None:
    if not PREflight.exists():
        raise RuntimeError("PREFLIGHT_ARTIFACT_MISSING")
    pre = json.loads(PREflight.read_text(encoding="utf-8"))
    rows = targets()
    expected_ids = [row["comment_id"] for row in rows]
    if pre.get("status") != "Preflight_Pass" or pre.get("requested_count") != EXPECTED or pre.get("preflight_completed_count") != EXPECTED:
        raise RuntimeError(f"PREFLIGHT_NOT_PASS:{pre.get('status')}:{pre.get('preflight_completed_count')}")
    if [check.get("comment_id") for check in pre.get("checks", [])] != expected_ids:
        raise RuntimeError("PREFLIGHT_TARGET_ORDER_MISMATCH")
    token = page_token()
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results: list[dict[str, Any]] = []
    try:
        for check, row in zip(pre["checks"], rows):
            cid = row["comment_id"]
            existing = check.get("existing_exact")
            if existing:
                verified = fetch_verified(existing["id"], token)
                status = "already_published"
            else:
                created = request("POST", f"{cid}/comments", token, form={"message": row["proposed_reply"]})
                reply_id = created.get("id")
                if not reply_id:
                    raise RuntimeError(json.dumps({"missing_reply_id": cid}, ensure_ascii=False))
                verified = fetch_verified(reply_id, token)
                status = "published"
            returned_parent = (verified.get("parent") or {}).get("id")
            target_parent = check.get("target_parent_id")
            if returned_parent == cid:
                parent_semantics = "direct_target_parent"
                parent_ok = True
            elif target_parent and returned_parent == target_parent:
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
            result = {
                "status": status,
                "parent_comment_id": cid,
                "post_id": row.get("post_id"),
                "proposed_reply": row["proposed_reply"],
                "reply_id": verified.get("id"),
                "message": verified.get("message"),
                "from_id": (verified.get("from") or {}).get("id"),
                "parent_id_returned": returned_parent,
                "target_parent_id_from_meta": target_parent,
                "parent_semantics": parent_semantics,
                "created_time": verified.get("created_time"),
                "is_hidden": verified.get("is_hidden"),
                "verified": verified_ok,
            }
            results.append(result)
            if not verified_ok:
                raise RuntimeError(json.dumps({"verification_failed": result}, ensure_ascii=False))
    except Exception as exc:
        partial = {
            "title": "Facebook Additional Publication — partial evidence",
            "purpose": "Evidencia parcial de la publicación de las ocho respuestas aprobadas; no se reintenta automáticamente.",
            "status": "Partial_Review",
            "created_at": started,
            "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "version": "1.0",
            "author": "Manus AI",
            "organization": "Operations/Research",
            "related_documents": [
                "Operations/Research/2026-08-25_18-49-39_Facebook_Additional_Publication_Preflight.json",
                "Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
                "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            ],
            "source": "Meta Graph API v26.0",
            "page_id": PAGE_ID,
            "explicit_user_approval": True,
            "requested_count": EXPECTED,
            "published_or_found_count": len(results),
            "verified_count": sum(1 for result in results if result.get("verified")),
            "error": str(exc),
            "results": results,
        }
        PUBLICATION.write_text(json.dumps(partial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
    finished = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {
        "title": "Facebook Additional Publication — eight approved replies",
        "purpose": "Evidencia de publicación y verificación de exactamente las ocho respuestas aprobadas del lote adicional.",
        "status": "Active",
        "created_at": started,
        "updated_at": finished,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-49-39_Facebook_Additional_Publication_Preflight.json",
            "Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json",
            "Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "approval_source": "Fernando autorizó publicar las ocho respuestas aprobadas del lote adicional en conversación el 2026-08-25.",
        "requested_count": EXPECTED,
        "published_count": sum(1 for result in results if result["status"] == "published"),
        "already_published_count": sum(1 for result in results if result["status"] == "already_published"),
        "verified_count": sum(1 for result in results if result["verified"]),
        "strict_direct_parent_count": sum(1 for result in results if result["parent_semantics"] == "direct_target_parent"),
        "nested_target_parent_semantics_count": sum(1 for result in results if result["parent_semantics"] == "nested_reply_api_returns_target_parent"),
        "preflight_status": pre["status"],
        "results": results,
    }
    if payload["verified_count"] != EXPECTED:
        raise RuntimeError(f"EXPECTED_{EXPECTED}_VERIFIED_RESULTS:{payload['verified_count']}")
    PUBLICATION.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count", "strict_direct_parent_count", "nested_target_parent_semantics_count")}, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"preflight", "publish"}:
        raise SystemExit("usage: publish_additional_facebook_queue_2026_08_25_1849.py preflight|publish")
    if sys.argv[1] == "preflight":
        preflight()
    else:
        publish()
