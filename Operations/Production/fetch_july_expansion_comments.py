#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[2]
MATCHES = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Matches.csv"
OUTPUT = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Evidence.json"
BASE = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"


def page_token(session: requests.Session, user_token: str) -> str:
    response = session.get(f"{BASE}/me/accounts", params={"fields": "id,name,access_token", "limit": 100}, headers={"Authorization": f"Bearer {user_token}"}, timeout=30)
    response.raise_for_status()
    page = next((item for item in response.json().get("data", []) if item.get("id") == PAGE_ID), None)
    if not page or not page.get("access_token"):
        raise RuntimeError("Page access token for Universe Sent Me was not returned by /me/accounts")
    return page["access_token"]


def main() -> None:
    with MATCHES.open(newline="", encoding="utf-8-sig") as handle:
        matches = list(csv.DictReader(handle))
    ids = [row["Meta_ID"] for row in matches if row.get("Status") == "Visual_Match_Confirmed"]
    session = requests.Session()
    token = page_token(session, os.environ["META_PAGE_ACCESS_TOKEN"])
    fields = "id,from,message,created_time,like_count,comments.limit(50){id,from,message,created_time,like_count}"
    batch = [{"method": "GET", "relative_url": f"{quote(meta_id, safe='')} /comments?limit=100&fields={quote(fields, safe=',{}().') }".replace(" ", "")} for meta_id in ids]
    response = session.post(BASE, headers={"Authorization": f"Bearer {token}"}, data={"batch": json.dumps(batch)}, timeout=90)
    response.raise_for_status()
    raw = response.json()
    posts = []
    errors = []
    for meta_id, item in zip(ids, raw):
        body = json.loads(item.get("body", "{}")) if isinstance(item, dict) else {}
        if item.get("code", 200) >= 400 or body.get("error"):
            errors.append({"Meta_ID": meta_id, "result": item})
            continue
        comments = body.get("data", [])
        posts.append({"Meta_ID": meta_id, "comments_returned": len(comments), "comments": comments, "paging": body.get("paging", {})})
    payload = {
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "batch_size": len(batch),
        "fields": fields,
        "posts": posts,
        "errors": errors,
        "guardrails": ["Read-only retrieval", "No comment publication", "Comments are evidence, not a proxy for 24/72-hour metrics."]
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"posts": len(posts), "comments": sum(item["comments_returned"] for item in posts), "errors": len(errors), "output": str(OUTPUT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
