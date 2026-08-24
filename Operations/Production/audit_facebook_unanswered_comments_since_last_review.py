"""Read-only audit of new Facebook comments without a direct Page reply.

The script intentionally reviews a bounded set of recent Page posts and one
level of nested replies. It never publishes, hides, deletes, or edits content.
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
LAST_REVIEW = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_07.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Delta_08.json"
POST_LIMIT = 20
REQUEST_TIMEOUT_SECONDS = 20
MAX_WORKERS = 8

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")


def request_json(path, params, token):
    response = requests.get(
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def safe_request(path, params, token):
    try:
        return {"payload": request_json(path, params, token), "error": None}
    except requests.RequestException as exc:
        response = getattr(exc, "response", None)
        body = None
        status = None
        if response is not None:
            status = response.status_code
            try:
                body = response.json()
            except ValueError:
                body = response.text[:500]
        return {"payload": {"data": []}, "error": {"type": type(exc).__name__, "status": status, "detail": str(exc), "body": body}}


def is_page_author(comment):
    author = comment.get("from") or {}
    return str(author.get("id") or "") == PAGE_ID or (author.get("name") or "").strip().lower() == "universe sent me"


def parse_dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00").replace("+0000", "+00:00"))


def sanitize(comment, post, comment_type, parent_id, direct_page_reply_count):
    has_page_reply = direct_page_reply_count > 0
    return {
        "comment_id": comment.get("id"),
        "post_id": post.get("id"),
        "post_created_time": post.get("created_time"),
        "post_message": post.get("message"),
        "post_permalink": post.get("permalink_url"),
        "comment_created_time": comment.get("created_time"),
        "comment_message": comment.get("message"),
        "comment_type": comment_type,
        "parent_comment_id": parent_id,
        "is_hidden": comment.get("is_hidden"),
        "has_direct_page_reply": has_page_reply,
        "direct_page_reply_count": direct_page_reply_count,
        "response_status": "Respondido" if has_page_reply else "Pendiente_Respuesta",
        "approval_status": "No_Aplica" if has_page_reply else "Pendiente_Fernando",
        "privacy": "Anonimizado",
    }


accounts_result = request_json(
    "me/accounts",
    {"fields": "id,name,access_token", "limit": 100},
    base_token,
)
page = next((row for row in accounts_result.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

if LAST_REVIEW.exists():
    previous = json.loads(LAST_REVIEW.read_text(encoding="utf-8"))
    cutoff = previous.get("reviewed_at") or previous.get("cutoff")
else:
    cutoff = "1970-01-01T00:00:00+0000"
cutoff_dt = parse_dt(cutoff)
reviewed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    existing_ids = {row.get("Comentario_ID", "") for row in csv.DictReader(handle)}

post_fields = "id,from,message,created_time,permalink_url"
posts_result = request_json(f"{PAGE_ID}/feed", {"fields": post_fields, "limit": POST_LIMIT}, page_token)
feed_posts = posts_result.get("data", [])
page_posts = [post for post in feed_posts if is_page_author(post)]

comment_fields = "id,from,message,created_time,like_count,message_tags,is_hidden,parent"
post_comment_results = {}
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures = {
        pool.submit(safe_request, f"{post['id']}/comments", {"fields": comment_fields, "limit": 100}, page_token): post
        for post in page_posts
        if post.get("id")
    }
    for future in as_completed(futures):
        post_comment_results[futures[future]["id"]] = future.result()

root_records = []
for post in page_posts:
    result = post_comment_results.get(post.get("id"), {"payload": {"data": []}, "error": {"detail": "NO_RESULT"}})
    for root in result["payload"].get("data", []):
        if root.get("id"):
            root_records.append((post, root, result.get("error")))

reply_results = {}
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures = {
        pool.submit(safe_request, f"{root['id']}/comments", {"fields": comment_fields, "limit": 100}, page_token): root
        for _, root, _ in root_records
    }
    for future in as_completed(futures):
        reply_results[futures[future]["id"]] = future.result()

new_user_comments = []
unanswered = []
all_seen_ids = set()
api_errors = []
for post, root, root_error in root_records:
    root_id = root["id"]
    all_seen_ids.add(root_id)
    replies_result = reply_results.get(root_id, {"payload": {"data": []}, "error": {"detail": "NO_REPLY_RESULT"}})
    if root_error:
        api_errors.append({"scope": "post_comments", "post_id": post.get("id"), "error": root_error})
    if replies_result.get("error"):
        api_errors.append({"scope": "root_replies", "comment_id": root_id, "error": replies_result["error"]})
    replies = replies_result["payload"].get("data", [])
    direct_page_replies = [reply for reply in replies if is_page_author(reply)]

    for comment, comment_type, parent_id, page_reply_count in [
        (root, "Comentario_Raiz", None, len(direct_page_replies)),
        *[(reply, "Replica_Anidada", root_id, 0) for reply in replies if not is_page_author(reply)],
    ]:
        comment_id = comment.get("id")
        if not comment_id:
            continue
        all_seen_ids.add(comment_id)
        if is_page_author(comment):
            continue
        created = comment.get("created_time")
        if not created or parse_dt(created) <= cutoff_dt:
            continue
        row = sanitize(comment, post, comment_type, parent_id, page_reply_count)
        row["already_logged"] = comment_id in existing_ids
        new_user_comments.append(row)
        if not row["has_direct_page_reply"]:
            unanswered.append(row)

new_unanswered = [row for row in unanswered if not row["already_logged"]]
result = {
    "reviewed_at": reviewed_at,
    "cutoff": cutoff,
    "page_id": PAGE_ID,
    "source": "Meta Graph API v26.0 / Page feed + direct post comments + one-level nested replies",
    "read_only": True,
    "coverage_note": "Bounded to the 20 most recent Page-authored feed posts; replies deeper than one nested level are not expanded.",
    "posts_fetched": len(feed_posts),
    "page_posts_reviewed": len(page_posts),
    "root_comments_seen": len(root_records),
    "user_comments_after_cutoff": len(new_user_comments),
    "unanswered_after_cutoff": len(unanswered),
    "new_unanswered_not_in_ledger": len(new_unanswered),
    "already_logged_after_cutoff": sum(1 for row in new_user_comments if row["already_logged"]),
    "reply_lookup_count": len(reply_results),
    "comment_ids_seen": len(all_seen_ids),
    "api_error_count": len(api_errors),
    "api_errors": api_errors,
    "comments": new_user_comments,
    "unanswered": new_unanswered,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: result[key] for key in ("reviewed_at", "cutoff", "posts_fetched", "page_posts_reviewed", "root_comments_seen", "user_comments_after_cutoff", "unanswered_after_cutoff", "new_unanswered_not_in_ledger", "reply_lookup_count", "api_error_count")}, ensure_ascii=False))
for row in new_unanswered:
    print(json.dumps(row, ensure_ascii=False))
