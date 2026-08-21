#!/usr/bin/env python3
"""Fetch Meta evidence for the July individual expansion queue in one batch."""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
RAW = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Meta_Raw.json"
IMAGE_DIR = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Meta_Images"
BASE = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"


def read_queue() -> list[dict[str, str]]:
    with QUEUE.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def page_token(session: requests.Session, user_token: str) -> str:
    response = session.get(
        f"{BASE}/me/accounts",
        params={"fields": "id,name,access_token", "limit": 100},
        headers={"Authorization": f"Bearer {user_token}"},
        timeout=30,
    )
    response.raise_for_status()
    page = next((item for item in response.json().get("data", []) if item.get("id") == PAGE_ID), None)
    if not page or not page.get("access_token"):
        raise RuntimeError("Page access token for Universe Sent Me was not returned by /me/accounts")
    return page["access_token"]


def main() -> None:
    user_token = os.environ["META_PAGE_ACCESS_TOKEN"]
    queue = read_queue()
    ids = [row["Meta_ID"] for row in queue if row.get("Meta_ID")]
    session = requests.Session()
    token = page_token(session, user_token)
    fields = "id,created_time,message,permalink_url,full_picture,attachments.limit(10){media,type,url,target},shares,reactions.limit(0).summary(true),comments.limit(0).summary(true)"
    batch = [{"method": "GET", "relative_url": f"{quote(meta_id, safe='') }?fields={quote(fields, safe=',{}().') }"} for meta_id in ids]
    response = session.post(
        BASE,
        headers={"Authorization": f"Bearer {token}"},
        data={"batch": json.dumps(batch, ensure_ascii=False)},
        timeout=60,
    )
    response.raise_for_status()
    batch_results = response.json()
    RAW.write_text(
        json.dumps(
            {
                "extraction_meta": {
                    "extracted_at_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
                    "endpoint": BASE,
                    "page_id": PAGE_ID,
                    "batch_size": len(batch),
                    "fields": fields,
                    "source": "Meta Graph API v26.0",
                },
                "data": batch_results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for row, item in zip(queue, batch_results):
        body = json.loads(item.get("body", "{}")) if isinstance(item, dict) else {}
        picture = body.get("full_picture")
        if not picture:
            downloaded.append({"meta_id": row["Meta_ID"], "status": "No_full_picture"})
            continue
        image_response = session.get(picture, headers={"Authorization": f"Bearer {token}"}, timeout=60)
        if image_response.status_code != 200 or not image_response.content:
            downloaded.append({"meta_id": row["Meta_ID"], "status": f"Download_HTTP_{image_response.status_code}"})
            continue
        safe_id = row["Meta_ID"].replace("/", "_")
        target = IMAGE_DIR / f"{safe_id}.jpg"
        target.write_bytes(image_response.content)
        downloaded.append({"meta_id": row["Meta_ID"], "status": "Downloaded", "path": str(target), "bytes": len(image_response.content)})

    print(json.dumps({"batch_size": len(batch), "raw_output": str(RAW), "downloaded": downloaded}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
