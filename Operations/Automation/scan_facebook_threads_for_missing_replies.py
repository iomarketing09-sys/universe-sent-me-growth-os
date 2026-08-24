"""Search a Facebook post's full comment threads for inaccessible reply IDs.

GET-only diagnostic. It follows root comments and nested comment connections,
looking for target reply IDs and exact approved messages. It never writes to
Meta or changes the ledger.
"""

import csv
import json
import os
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
VERIFICATION = RESEARCH / "2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json"
OUT = RESEARCH / "2026-08-24_Facebook_Missing_Replies_Thread_Scan.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30
FIELDS = "id,from,message,created_time,parent,is_hidden"

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    ledger_rows = list(csv.DictReader(handle))
ledger_by_id = {row.get("Comentario_ID"): row for row in ledger_rows}
verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
error_rows = [row for row in verification["results"] if not row.get("api_ok")]
if not error_rows:
    raise SystemExit("NO_INACCESSIBLE_REPLIES_TO_SCAN")

session = requests.Session()

def call(path, token, params=None):
    response = session.get(f"{GRAPH}/{path.lstrip('/')}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=TIMEOUT)
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text[:500]}
    return response.status_code, payload

status, accounts = call("me/accounts", base_token, {"fields": "id,access_token", "limit": 100})
if status != 200:
    raise SystemExit(f"ME_ACCOUNTS_FAILED: HTTP_{status}")
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

targets = {}
for row in error_rows:
    historical_post_id = ledger_by_id.get(row["comment_id"], {}).get("Post_ID", "")
    canonical_post_id = historical_post_id if historical_post_id.startswith(f"{PAGE_ID}_") else f"{PAGE_ID}_{historical_post_id}" if historical_post_id else ""
    targets[row["reply_id"]] = {
        "comment_id": row["comment_id"],
        "reply_id": row["reply_id"],
        "message": row.get("ledger_message", ""),
        "historical_post_id": historical_post_id,
        "canonical_post_id": canonical_post_id,
    }

search_posts = sorted({item["canonical_post_id"] for item in targets.values() if item["canonical_post_id"]})
visited = set()
found = {}
requests_log = []
max_objects = 2000

for post_id in search_posts:
    queue = deque([(post_id, 0)])
    while queue and len(visited) < max_objects:
        parent_id, depth = queue.popleft()
        if parent_id in visited:
            continue
        visited.add(parent_id)
        url = f"{parent_id}/comments"
        status_code, payload = call(url, page_token, {"fields": FIELDS, "limit": 100})
        requests_log.append({"parent_id": parent_id, "depth": depth, "status_code": status_code, "error": payload.get("error") if isinstance(payload, dict) else None})
        if status_code != 200:
            continue
        for item in payload.get("data", []):
            item_id = item.get("id")
            if item_id in targets:
                found[item_id] = {"found_under_parent_id": parent_id, "depth": depth + 1, "payload": item}
            # Follow all visible replies; a reply may still have a deeper child.
            if item_id and item_id not in visited:
                queue.append((item_id, depth + 1))
        next_url = (payload.get("paging") or {}).get("next")
        # Follow paging for each parent only when needed; construct a temporary
        # queue item whose ID is the next URL so the same GET helper is reused.
        page_count = 1
        while next_url and page_count < 25 and len(visited) < max_objects:
            response = session.get(next_url, headers={"Authorization": f"Bearer {page_token}"}, timeout=TIMEOUT)
            try:
                next_payload = response.json()
            except ValueError:
                next_payload = {"raw": response.text[:500]}
            requests_log.append({"parent_id": parent_id, "depth": depth, "status_code": response.status_code, "paging": True, "error": next_payload.get("error") if isinstance(next_payload, dict) else None})
            if response.status_code != 200:
                break
            for item in next_payload.get("data", []):
                item_id = item.get("id")
                if item_id in targets:
                    found[item_id] = {"found_under_parent_id": parent_id, "depth": depth + 1, "payload": item}
                if item_id and item_id not in visited:
                    queue.append((item_id, depth + 1))
            next_url = (next_payload.get("paging") or {}).get("next")
            page_count += 1

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for reply_id, target in targets.items():
    match = found.get(reply_id)
    results.append({**target, "found": bool(match), "match": match})
payload = {
    "title": "Facebook — escaneo recursivo de hilos para replies inaccesibles",
    "purpose": "Buscar los Meta reply IDs inaccesibles dentro de todos los comentarios y réplicas de sus publicaciones canónicas, sin escrituras.",
    "status": "Review",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json",
        "Operations/Research/2026-08-24_Facebook_Inaccessible_Replies_Recovery_Search.json",
        "Operations/Research/2026-08-24_Facebook_All_Replies_Reconciliation.json",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 GET only",
    "page_id": PAGE_ID,
    "searched_posts": search_posts,
    "visited_comment_objects": len(visited),
    "api_requests": len(requests_log),
    "target_reply_count": len(targets),
    "found_target_reply_count": len(found),
    "results": results,
    "requests_log": requests_log,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"searched_posts": search_posts, "visited_comment_objects": len(visited), "api_requests": len(requests_log), "target_reply_count": len(targets), "found_target_reply_count": len(found)}, ensure_ascii=False))
for item in results:
    print(json.dumps({"comment_id": item["comment_id"], "reply_id": item["reply_id"], "found": item["found"], "match": item["match"]}, ensure_ascii=False))
