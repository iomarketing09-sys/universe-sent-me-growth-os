#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
RAW = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Meta_Raw.json"
SHEETS = [ROOT / f"Operations/Research/2026-08-21_Junio_57_Unmatched_Contact_Sheet_{i:02d}.jpg" for i in range(1, 5)]
IMAGE_DIR = Path("/tmp/usm_june_57_unmatched_images")
BASE = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"


def page_token(session: requests.Session, user_token: str) -> str:
    r = session.get(
        f"{BASE}/me/accounts",
        params={"fields": "id,name,access_token", "limit": 100},
        headers={"Authorization": f"Bearer {user_token}"},
        timeout=30,
    )
    r.raise_for_status()
    page = next((x for x in r.json().get("data", []) if x.get("id") == PAGE_ID), None)
    if not page or not page.get("access_token"):
        raise RuntimeError("Universe Sent Me Page token was not returned by /me/accounts")
    return page["access_token"]


def chunks(items, size):
    for start in range(0, len(items), size):
        yield items[start:start + size]


def font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def shorten(text: str, length: int = 54) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= length else text[: length - 1] + "…"


def main():
    with QUEUE.open(newline="", encoding="utf-8-sig") as handle:
        queue = [r for r in csv.DictReader(handle) if r.get("status") == "Needs_Asset_Match"]
    queue.sort(key=lambda r: int(r.get("priority_rank") or 999))
    session = requests.Session()
    token = page_token(session, os.environ["META_PAGE_ACCESS_TOKEN"])
    fields = "id,created_time,message,permalink_url,full_picture,attachments.limit(10){media,type,url,target},shares,reactions.limit(0).summary(true),comments.limit(0).summary(true)"
    all_results = []
    for part in chunks(queue, 50):
        batch = [{"method": "GET", "relative_url": f"{quote(row['meta_id'], safe='')}?fields={quote(fields, safe=',{}().')}"} for row in part]
        response = session.post(BASE, headers={"Authorization": f"Bearer {token}"}, data={"batch": json.dumps(batch)}, timeout=60)
        response.raise_for_status()
        all_results.extend(response.json())
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for row, result in zip(queue, all_results):
        body = json.loads(result.get("body", "{}")) if isinstance(result, dict) else {}
        picture = body.get("full_picture")
        image_path = ""
        if picture:
            target = IMAGE_DIR / f"{row['meta_id']}.jpg"
            download = session.get(picture, headers={"Authorization": f"Bearer {token}"}, timeout=60)
            if download.status_code == 200 and download.content:
                target.write_bytes(download.content)
                image_path = str(target)
        records.append({
            "priority_rank": row.get("priority_rank"),
            "meta_id": row.get("meta_id"),
            "date": row.get("publication_date_local"),
            "caption": row.get("caption"),
            "interactions_queue": row.get("interactions"),
            "shares_queue": row.get("shares"),
            "comments_queue": row.get("comments"),
            "full_picture": bool(picture),
            "image_path": image_path,
            "meta_body": body,
            "fetch_error": result.get("code") if isinstance(result, dict) else None,
        })
    RAW.write_text(json.dumps({"extracted_at_utc": datetime.now(timezone.utc).isoformat(), "source": "Meta Graph API v26.0", "batch_count": (len(queue) + 49) // 50, "fields": fields, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    title_font = font(18)
    label_font = font(13)
    for sheet_index, part in enumerate([records[:15], records[15:30], records[30:45], records[45:]], start=1):
        cols, tile_w, tile_h, image_h = 3, 520, 450, 350
        rows_count = (len(part) + cols - 1) // cols
        canvas = Image.new("RGB", (cols * tile_w, rows_count * tile_h), "white")
        draw = ImageDraw.Draw(canvas)
        for idx, record in enumerate(part):
            x, y = (idx % cols) * tile_w, (idx // cols) * tile_h
            draw.rectangle((x, y, x + tile_w - 1, y + tile_h - 1), outline=(190, 190, 190), width=2)
            if record["image_path"]:
                try:
                    image = Image.open(record["image_path"]).convert("RGB")
                    image.thumbnail((tile_w - 30, image_h))
                    px = x + (tile_w - image.width) // 2
                    py = y + 12 + (image_h - image.height) // 2
                    canvas.paste(image, (px, py))
                except Exception:
                    draw.text((x + 20, y + 150), "Image load failed", fill="red", font=title_font)
            else:
                draw.text((x + 20, y + 150), "No full_picture", fill="red", font=title_font)
            meta_short = record["meta_id"].split("_")[-1]
            label = f"r{record['priority_rank']}  {meta_short}  I{record['interactions_queue']} S{record['shares_queue']} C{record['comments_queue']}"
            draw.text((x + 12, y + image_h + 20), label, fill="black", font=label_font)
            draw.text((x + 12, y + image_h + 44), shorten(record["caption"]), fill="black", font=label_font)
        canvas.save(SHEETS[sheet_index - 1], quality=92)
    print(json.dumps({"queue": len(queue), "records": len(records), "with_images": sum(bool(x["image_path"]) for x in records), "raw": str(RAW), "sheets": [str(x) for x in SHEETS]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
