"""Read-only review of all comments on the user-linked Facebook Page Post."""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
POST_ID = "1036844829507460_122151375549072582"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Comment_Review_Post_Batch10.json"
TIMEOUT = 20
WORKERS = 8

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")


def get(path, params, token):
    response = requests.get(
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def paginate(path, params, token):
    rows = []
    payload = get(path, params, token)
    rows.extend(payload.get("data", []))
    next_url = (payload.get("paging") or {}).get("next")
    while next_url:
        response = requests.get(next_url, headers={"Authorization": f"Bearer {token}"}, timeout=TIMEOUT)
        response.raise_for_status()
        payload = response.json()
        rows.extend(payload.get("data", []))
        next_url = (payload.get("paging") or {}).get("next")
    return rows


def is_page_author(row):
    author = row.get("from") or {}
    return str(author.get("id") or "") == PAGE_ID or (author.get("name") or "").strip().lower() == "universe sent me"


def safe_replies(root_id, token):
    try:
        return {"data": paginate(f"{root_id}/comments", {"fields": COMMENT_FIELDS, "limit": 100}, token), "error": None}
    except requests.RequestException as exc:
        response = getattr(exc, "response", None)
        return {"data": [], "error": {"type": type(exc).__name__, "status": getattr(response, "status_code", None), "detail": str(exc)}}

accounts = get("me/accounts", {"fields": "id,name,access_token", "limit": 100}, base_token)
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND")
page_token = page["access_token"]

COMMENT_FIELDS = "id,from,message,created_time,like_count,message_tags,is_hidden,parent"
post = get(POST_ID, {"fields": "id,from,message,created_time,permalink_url"}, page_token)
roots = paginate(f"{POST_ID}/comments", {"fields": COMMENT_FIELDS, "limit": 100}, page_token)

reply_results = {}
with ThreadPoolExecutor(max_workers=WORKERS) as pool:
    futures = {pool.submit(safe_replies, root["id"], page_token): root["id"] for root in roots if root.get("id")}
    for future in as_completed(futures):
        reply_results[futures[future]] = future.result()

unanswered = []
responded = []
errors = []
all_ids = set()
for root in roots:
    root_id = root.get("id")
    if not root_id:
        continue
    all_ids.add(root_id)
    result = reply_results.get(root_id, {"data": [], "error": {"detail": "NO_RESULT"}})
    if result.get("error"):
        errors.append({"scope": "replies", "comment_id": root_id, "error": result["error"]})
    replies = result.get("data", [])
    page_replies = [reply for reply in replies if is_page_author(reply)]
    root_row = {
        "comment_id": root_id,
        "post_id": POST_ID,
        "post_permalink": post.get("permalink_url"),
        "comment_created_time": root.get("created_time"),
        "comment_message": root.get("message"),
        "comment_type": "Comentario_Raiz",
        "parent_comment_id": None,
        "is_hidden": root.get("is_hidden"),
        "has_direct_page_reply": bool(page_replies),
        "direct_page_reply_count": len(page_replies),
        "page_reply_ids": [reply.get("id") for reply in page_replies],
    }
    (responded if page_replies else unanswered).append(root_row)
    for reply in replies:
        reply_id = reply.get("id")
        if not reply_id or is_page_author(reply):
            continue
        all_ids.add(reply_id)
        reply_row = {
            "comment_id": reply_id,
            "post_id": POST_ID,
            "post_permalink": post.get("permalink_url"),
            "comment_created_time": reply.get("created_time"),
            "comment_message": reply.get("message"),
            "comment_type": "Replica_Anidada",
            "parent_comment_id": root_id,
            "is_hidden": reply.get("is_hidden"),
            "has_direct_page_reply": False,
            "direct_page_reply_count": 0,
            "page_reply_ids": [],
        }
        unanswered.append(reply_row)

reviewed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "reviewed_at": reviewed_at,
    "page_id": PAGE_ID,
    "post_id": POST_ID,
    "linked_comment_id": "2371700183567495",
    "source": "Meta Graph API v26.0 / direct Page Post comments + one-level nested replies",
    "read_only": True,
    "post": {"id": post.get("id"), "message": post.get("message"), "created_time": post.get("created_time"), "permalink_url": post.get("permalink_url")},
    "root_comments_seen": len(roots),
    "comment_ids_seen": len(all_ids),
    "root_comments_without_direct_page_reply": sum(1 for row in unanswered if row["comment_type"] == "Comentario_Raiz"),
    "root_comments_with_direct_page_reply": len(responded),
    "unanswered_units_including_replies": len(unanswered),
    "api_error_count": len(errors),
    "api_errors": errors,
    "unanswered": unanswered,
    "responded_roots": responded,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("reviewed_at", "post_id", "root_comments_seen", "comment_ids_seen", "root_comments_without_direct_page_reply", "root_comments_with_direct_page_reply", "unanswered_units_including_replies", "api_error_count")}, ensure_ascii=False))
for row in unanswered:
    print(json.dumps(row, ensure_ascii=False))
