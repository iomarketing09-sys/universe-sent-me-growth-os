"""Read-only context enrichment for comments found after Batch 14."""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
INPUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Batch14.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Context_After_Batch14.json"
TIMEOUT = 30

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")


def get(path, token, params):
    r = requests.get(f"{GRAPH}/{path.lstrip('/')}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def safe_get(path, token, params):
    try:
        return {"data": get(path, token, params), "error": None}
    except requests.RequestException as exc:
        response = getattr(exc, "response", None)
        body = None
        if response is not None:
            try:
                body = response.json()
            except ValueError:
                body = response.text[:500]
        return {"data": None, "error": {"type": type(exc).__name__, "status": getattr(response, "status_code", None), "detail": str(exc), "body": body}}


review = json.loads(INPUT.read_text(encoding="utf-8"))
accounts = get("me/accounts", base_token, {"fields": "id,name,access_token", "limit": 100})
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

candidates = review["new_unanswered_not_in_ledger"]
parent_ids = sorted({row["parent_comment_id"] for row in candidates if row.get("parent_comment_id")})
parent_results = {}
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = {pool.submit(safe_get, parent_id, page_token, {"fields": "id,message,created_time,from,parent,is_hidden"}): parent_id for parent_id in parent_ids}
    for future in as_completed(futures):
        parent_results[futures[future]] = future.result()

records = []
for row in candidates:
    parent_id = row.get("parent_comment_id")
    parent_result = parent_results.get(parent_id, {"data": None, "error": None}) if parent_id else {"data": None, "error": None}
    parent_data = parent_result.get("data") or {}
    records.append({
        **row,
        "parent_message": parent_data.get("message") if parent_id else None,
        "parent_created_time": parent_data.get("created_time") if parent_id else None,
        "parent_is_hidden": parent_data.get("is_hidden") if parent_id else None,
        "parent_lookup_error": parent_result.get("error"),
    })

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
result = {
    "title": "Facebook Candidate Context After Batch 14",
    "purpose": "Contexto de solo lectura para evaluar comentarios nuevos sin respuesta y no interrumpir conversaciones usuario-a-usuario.",
    "status": "Review",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 / read-only parent context lookups",
    "read_only": True,
    "candidate_count": len(records),
    "parent_context_requests": len(parent_ids),
    "parent_context_errors": sum(1 for value in parent_results.values() if value.get("error")),
    "records": records,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"candidate_count": len(records), "parent_context_requests": len(parent_ids), "parent_context_errors": result["parent_context_errors"], "output": str(OUT)}, ensure_ascii=False))
