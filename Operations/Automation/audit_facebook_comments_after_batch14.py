"""Read-only Facebook comment scan after Batch 14.

The scan never writes to Meta. It derives the Page token in memory, reviews the
20 most recent own Page posts, reads roots and one level of replies, and emits
new/unanswered candidates after the verified Batch 14 cursor.
"""

import csv
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
BATCH14 = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Batch14.json"
POST_LIMIT = 20
MAX_WORKERS = 8
TIMEOUT = 30

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")


def request(path, token, params):
    response = requests.get(
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def safe_request(path, token, params):
    try:
        return {"payload": request(path, token, params), "error": None}
    except requests.RequestException as exc:
        response = getattr(exc, "response", None)
        body = None
        if response is not None:
            try:
                body = response.json()
            except ValueError:
                body = response.text[:500]
        return {
            "payload": {"data": []},
            "error": {
                "type": type(exc).__name__,
                "status": getattr(response, "status_code", None),
                "detail": str(exc),
                "body": body,
            },
        }


def is_page_author(item):
    author = item.get("from") or {}
    return str(author.get("id") or "") == PAGE_ID or (author.get("name") or "").strip().lower() == "universe sent me"


def parse_dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00").replace("+0000", "+00:00"))


accounts = request("me/accounts", base_token, {"fields": "id,name,access_token", "limit": 100})
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

batch14 = json.loads(BATCH14.read_text(encoding="utf-8"))
cursor = parse_dt(batch14["published_at"])
reviewed_at = datetime.now(timezone.utc)
with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    existing_ids = {row.get("Comentario_ID", "") for row in csv.DictReader(handle)}

post_fields = "id,from,message,created_time,permalink_url"
feed = request(f"{PAGE_ID}/feed", page_token, {"fields": post_fields, "limit": POST_LIMIT}).get("data", [])
posts = [post for post in feed if is_page_author(post) and post.get("id")]
comment_fields = "id,from,message,created_time,like_count,message_tags,is_hidden,parent"

post_results = {}
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures = {
        pool.submit(safe_request, f"{post['id']}/comments", page_token, {"fields": comment_fields, "limit": 100}): post
        for post in posts
    }
    for future in as_completed(futures):
        post_results[futures[future]["id"]] = future.result()

roots = []
api_errors = []
for post in posts:
    result = post_results.get(post["id"], {"payload": {"data": []}, "error": {"detail": "NO_RESULT"}})
    if result.get("error"):
        api_errors.append({"scope": "post_comments", "post_id": post["id"], "error": result["error"]})
    for root in result["payload"].get("data", []):
        if root.get("id"):
            roots.append((post, root))

reply_results = {}
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures = {
        pool.submit(safe_request, f"{root['id']}/comments", page_token, {"fields": comment_fields, "limit": 100}): root
        for _, root in roots
    }
    for future in as_completed(futures):
        reply_results[futures[future]["id"]] = future.result()

all_seen_ids = set()
unanswered = []
new_since_cursor = []
new_unanswered_since_cursor = []
logged_unanswered_since_cursor = []
page_replied = []
for post, root in roots:
    root_id = root["id"]
    all_seen_ids.add(root_id)
    replies_result = reply_results.get(root_id, {"payload": {"data": []}, "error": {"detail": "NO_REPLY_RESULT"}})
    if replies_result.get("error"):
        api_errors.append({"scope": "root_replies", "comment_id": root_id, "error": replies_result["error"]})
    replies = replies_result["payload"].get("data", [])
    direct_page_replies = [reply for reply in replies if is_page_author(reply)]
    units = [(root, "Comentario_Raiz", None, len(direct_page_replies))]
    units.extend((reply, "Replica_Anidada", root_id, 0) for reply in replies if not is_page_author(reply))
    for comment, comment_type, parent_id, page_reply_count in units:
        comment_id = comment.get("id")
        if not comment_id or is_page_author(comment):
            continue
        all_seen_ids.add(comment_id)
        created_value = comment.get("created_time")
        if not created_value:
            continue
        created = parse_dt(created_value)
        row = {
            "comment_id": comment_id,
            "post_id": post.get("id"),
            "post_created_time": post.get("created_time"),
            "post_message": post.get("message") or "",
            "post_permalink": post.get("permalink_url") or "",
            "comment_created_time": created_value,
            "comment_message": comment.get("message") or "",
            "comment_type": comment_type,
            "parent_comment_id": parent_id,
            "is_hidden": comment.get("is_hidden"),
            "has_direct_page_reply": page_reply_count > 0,
            "direct_page_reply_count": page_reply_count,
            "already_logged": comment_id in existing_ids,
            "created_after_batch14_cursor": created >= cursor,
        }
        if created >= cursor:
            new_since_cursor.append(row)
        if page_reply_count > 0:
            page_replied.append(row)
            continue
        unanswered.append(row)
        if created >= cursor:
            if comment_id in existing_ids:
                logged_unanswered_since_cursor.append(row)
            else:
                new_unanswered_since_cursor.append(row)

result = {
    "title": "Facebook Comment Review After Batch 14",
    "purpose": "Revisión de solo lectura de comentarios nuevos y oportunidades potenciales de engagement después del Batch 14, incluyendo raíces y réplicas de las 20 publicaciones propias más recientes.",
    "status": "Review",
    "created_at": reviewed_at.isoformat(timespec="seconds"),
    "updated_at": reviewed_at.isoformat(timespec="seconds"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
    ],
    "organization": "Operations/Research",
    "reviewed_at": reviewed_at.isoformat(timespec="seconds"),
    "cursor_source": "2026-08-24_Facebook_Comment_Publication_Batch_14.json",
    "cursor": batch14["published_at"],
    "page_id": PAGE_ID,
    "source": "Meta Graph API v26.0 / Page feed + direct post comments + one-level nested replies",
    "read_only": True,
    "posts_fetched": len(feed),
    "page_posts_reviewed": len(posts),
    "root_comments_seen": len(roots),
    "comment_ids_seen": len(all_seen_ids),
    "current_unanswered_units": len(unanswered),
    "new_units_since_batch14_cursor": len(new_since_cursor),
    "new_unanswered_not_in_ledger_since_batch14_cursor": len(new_unanswered_since_cursor),
    "logged_unanswered_since_batch14_cursor": len(logged_unanswered_since_cursor),
    "page_replied_units_since_batch14_cursor": len([row for row in page_replied if row["created_after_batch14_cursor"]]),
    "api_error_count": len(api_errors),
    "api_errors": api_errors,
    "new_unanswered_not_in_ledger": new_unanswered_since_cursor,
    "logged_unanswered_since_batch14_cursor": logged_unanswered_since_cursor,
    "all_current_unanswered": unanswered,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: result[key] for key in ("reviewed_at", "cursor", "posts_fetched", "page_posts_reviewed", "root_comments_seen", "comment_ids_seen", "current_unanswered_units", "new_units_since_batch14_cursor", "new_unanswered_not_in_ledger_since_batch14_cursor", "logged_unanswered_since_batch14_cursor", "page_replied_units_since_batch14_cursor", "api_error_count")}, ensure_ascii=False))
for row in new_unanswered_since_cursor:
    print(json.dumps(row, ensure_ascii=False))
