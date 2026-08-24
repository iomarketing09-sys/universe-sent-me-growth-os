"""Fetch read-only context for the direct Page mention found after Batch 14."""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Direct_Page_Mention_Context_After_Batch14.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TARGET_ID = "122151376083072582_1036099909244517"
PARENT_ID = "122151376083072582_1054911050596272"
TOKEN = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

def get(path, token, params):
    r = requests.get(f"{GRAPH}/{path.lstrip('/')}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

accounts = get("me/accounts", TOKEN, {"fields":"id,name,access_token", "limit":100})
page = next((x for x in accounts.get("data",[]) if x.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND")
page_token = page["access_token"]
fields = "id,from,message,created_time,parent,is_hidden,permalink_url"
target = get(TARGET_ID, page_token, {"fields":fields})
parent = get(PARENT_ID, page_token, {"fields":fields})
def strip_author_fields(value):
    if isinstance(value, dict):
        return {k: strip_author_fields(v) for k, v in value.items() if k not in {"from", "from_id", "from_name"}}
    if isinstance(value, list):
        return [strip_author_fields(v) for v in value]
    return value

related = {"target":strip_author_fields(target), "parent":strip_author_fields(parent)}
payload = {
    "title":"Facebook direct Page mention context after Batch 14",
    "purpose":"Contexto de solo lectura del único reply nuevo que menciona directamente a Universe Sent Me; no publica ni modifica Facebook.",
    "status":"Review",
    "created_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "updated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "version":"1.0",
    "author":"Manus AI",
    "organization":"Operations/Research",
    "source":"Meta Graph API v26.0",
    "page_id":PAGE_ID,
    "target_id":TARGET_ID,
    "parent_id":PARENT_ID,
    "read_only":True,
    "context":related,
}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"target_id":TARGET_ID,"target_message":target.get("message"),"parent_id":PARENT_ID,"parent_message":parent.get("message"),"parent_of_target":(target.get("parent") or {}).get("id")},ensure_ascii=False))
