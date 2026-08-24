"""Locate currently inaccessible Facebook replies by post and exact message.

Read-only recovery helper. It searches the owning post's comments connection
with stream and default filters, following pagination, for a visible reply from
the USM Page whose text exactly matches the ledger. It does not write to Meta.
"""

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
VERIFICATION = RESEARCH / "2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json"
OUT = RESEARCH / "2026-08-24_Facebook_Inaccessible_Replies_Recovery_Search.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    ledger_rows = list(csv.DictReader(handle))
ledger_by_id = {row.get("Comentario_ID"): row for row in ledger_rows}
verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
error_ids = {row["comment_id"] for row in verification["results"] if not row.get("api_ok")}

session = requests.Session()

def get_url(url, token, params=None):
    response = session.get(url, headers={"Authorization": f"Bearer {token}"}, params=params, timeout=TIMEOUT)
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text[:500]}
    return response.status_code, payload

status, accounts = get_url(f"{GRAPH}/me/accounts", base_token, {"fields": "id,access_token", "limit": 100})
if status != 200:
    raise SystemExit(f"ME_ACCOUNTS_FAILED: HTTP_{status}")
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

post_cache = {}
fields = "id,from,message,created_time,parent,is_hidden"

def search_post(post_id):
    if post_id in post_cache:
        return post_cache[post_id]
    matches = []
    requests_log = []
    for filter_name in ("stream", None):
        url = f"{GRAPH}/{post_id}/comments"
        params = {"fields": fields, "limit": 100}
        if filter_name:
            params["filter"] = filter_name
        pages = 0
        while url and pages < 25:
            status_code, payload = get_url(url, page_token, params)
            requests_log.append({"url": url, "filter": filter_name, "status_code": status_code, "error": payload.get("error") if isinstance(payload, dict) else None})
            if status_code != 200:
                break
            for item in payload.get("data", []):
                if (item.get("from") or {}).get("id") == PAGE_ID and item.get("is_hidden") is False:
                    matches.append(item)
            url = (payload.get("paging") or {}).get("next")
            params = None
            pages += 1
        if matches:
            break
    post_cache[post_id] = {"matches": matches, "requests": requests_log}
    return post_cache[post_id]

results = []
for comment_id in sorted(error_ids):
    row = ledger_by_id.get(comment_id, {})
    historical_post_id = row.get("Post_ID", "")
    candidate_post_ids = []
    if historical_post_id:
        candidate_post_ids.append(historical_post_id)
        canonical_post_id = historical_post_id if historical_post_id.startswith(f"{PAGE_ID}_") else f"{PAGE_ID}_{historical_post_id}"
        if canonical_post_id not in candidate_post_ids:
            candidate_post_ids.append(canonical_post_id)
    searched_by_post = {post_id: search_post(post_id) for post_id in candidate_post_ids}
    exact = None
    exact_post_id = None
    for candidate_post_id in candidate_post_ids:
        exact = next((item for item in searched_by_post[candidate_post_id]["matches"] if item.get("message") == row.get("Respuesta_Sugerida")), None)
        if exact:
            exact_post_id = candidate_post_id
            break
    results.append({
        "ledger_comment_id": comment_id,
        "ledger_reply_id": row.get("Respuesta_Meta_ID"),
        "historical_post_id": historical_post_id,
        "candidate_post_ids": candidate_post_ids,
        "located_post_id": exact_post_id,
        "ledger_message": row.get("Respuesta_Sugerida"),
        "search_match": exact,
        "search_match_count_for_page": sum(len(searched["matches"]) for searched in searched_by_post.values()),
        "requests": {post_id: searched["requests"] for post_id, searched in searched_by_post.items()},
    })

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "title": "Facebook — recuperación de respuestas actualmente inaccesibles",
    "purpose": "Buscar mediante GET en las publicaciones de Facebook las respuestas del ledger cuyo Meta reply ID devuelve HTTP 400, sin realizar escrituras.",
    "status": "Review",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json",
        "Operations/Research/2026-08-24_Facebook_All_Replies_Reconciliation.json",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 GET only",
    "page_id": PAGE_ID,
    "searched_error_rows": len(results),
    "located_exact_visible_page_replies": sum(1 for item in results if item.get("search_match")),
    "results": results,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"searched_error_rows": len(results), "located_exact_visible_page_replies": payload["located_exact_visible_page_replies"]}, ensure_ascii=False))
for item in results:
    print(json.dumps({key: item[key] for key in ("ledger_comment_id", "ledger_reply_id", "historical_post_id", "located_post_id", "search_match", "search_match_count_for_page")}, ensure_ascii=False))
