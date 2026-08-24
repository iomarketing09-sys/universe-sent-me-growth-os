"""Refetch verified Batch 14 replies to persist Meta-created timestamps."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

session = requests.Session()

def get(path, token, params):
    response = session.get(f"{GRAPH}/{path.lstrip('/')}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=TIMEOUT)
    if not response.ok:
        raise RuntimeError(f"META_HTTP_{response.status_code}: {response.text[:500]}")
    return response.json()

accounts = get("me/accounts", base_token, {"fields": "id,access_token", "limit": 100})
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]
batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("verified_count") != 13 or len(batch.get("results", [])) != 13:
    raise SystemExit("EXPECTED_13_VERIFIED_RESULTS_BEFORE_ENRICHMENT")

refetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
for result in batch["results"]:
    reply = get(result["reply_id"], page_token, {"fields": "id,from,message,created_time,parent,is_hidden"})
    if reply.get("id") != result["reply_id"] or (reply.get("from") or {}).get("id") != PAGE_ID or reply.get("message") != result.get("message") or reply.get("is_hidden") is not False:
        raise SystemExit(f"REFETCH_VERIFICATION_MISMATCH: {result['reply_id']}")
    result["reply_created_time"] = reply.get("created_time")
    result["refetched_at"] = refetched_at

batch["updated_at"] = refetched_at
batch["version"] = "1.2"
batch["timestamp_enrichment"] = "Meta Graph API v26.0 GET of each verified reply"
BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"refetched": len(batch["results"]), "refetched_at": refetched_at, "missing_timestamps": sum(1 for row in batch["results"] if not row.get("reply_created_time"))}, ensure_ascii=False))
