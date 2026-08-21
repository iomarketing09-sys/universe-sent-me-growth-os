#!/usr/bin/env python3
from __future__ import annotations

import base64
import csv
import json
import os
from pathlib import Path
from urllib.parse import quote

import matplotlib.pyplot as plt
import requests
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv"
DRIVE_EXPORT = Path("/tmp/usm_june_drive_assets_with_thumbnails.json")
META_RAW = ROOT / "Operations/Research/2026-08-21_Junio_Priority_Queue_Meta_Raw.json"
MATCHES = ROOT / "Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Matches.csv"
CONTACT = ROOT / "Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Contact_Sheet.jpg"
META_DIR = Path("/tmp/usm_june_priority_meta_images")
DRIVE_DIR = Path("/tmp/usm_june_priority_drive_thumbnails")
BASE = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"


def ahash(path: Path, size: int = 32) -> tuple[int, ...]:
    with Image.open(path) as image:
        image = image.convert("L").resize((size, size))
        pixels = list(image.getdata())
    mean = sum(pixels) / len(pixels)
    return tuple(1 if value >= mean else 0 for value in pixels)


def distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b))


def page_token(session: requests.Session, user_token: str) -> str:
    r = session.get(f"{BASE}/me/accounts", params={"fields": "id,name,access_token", "limit": 100}, headers={"Authorization": f"Bearer {user_token}"}, timeout=30)
    r.raise_for_status()
    page = next((item for item in r.json().get("data", []) if item.get("id") == PAGE_ID), None)
    if not page or not page.get("access_token"):
        raise RuntimeError("Page access token unavailable")
    return page["access_token"]


with QUEUE.open(newline="", encoding="utf-8-sig") as handle:
    queue = list(csv.DictReader(handle))
priority = [row for row in queue if row.get("status") == "Needs_Asset_Match"][:3]
ids = [row["meta_id"] for row in priority]

with DRIVE_EXPORT.open(encoding="utf-8") as handle:
    drive_files = [item for item in json.load(handle).get("files", []) if item.get("thumbnailLink") and item.get("mimeType", "").startswith("image/")]

session = requests.Session()
token = page_token(session, os.environ["META_PAGE_ACCESS_TOKEN"])
fields = "id,created_time,message,full_picture,attachments.limit(10){media,type,url,target},shares,reactions.limit(0).summary(true),comments.limit(0).summary(true)"
batch = [{"method": "GET", "relative_url": f"{quote(meta_id, safe='')}?fields={quote(fields, safe=',{}().')}"} for meta_id in ids]
r = session.post(BASE, headers={"Authorization": f"Bearer {token}"}, data={"batch": json.dumps(batch)}, timeout=60)
r.raise_for_status()
results = r.json()
META_DIR.mkdir(parents=True, exist_ok=True)
meta_rows = []
for row, result in zip(priority, results):
    body = json.loads(result.get("body", "{}"))
    picture = body.get("full_picture")
    if picture:
        img = session.get(picture, headers={"Authorization": f"Bearer {token}"}, timeout=60)
        path = META_DIR / f"{row['meta_id']}.jpg"
        path.write_bytes(img.content)
        row = dict(row)
        row["meta_image_path"] = str(path)
        meta_rows.append(row)
META_RAW.write_text(json.dumps({"queue": priority, "batch": results, "fields": fields}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

DRIVE_DIR.mkdir(parents=True, exist_ok=True)
drive_hashes = []
for item in drive_files:
    target = DRIVE_DIR / f"{item['id']}.jpg"
    if not target.exists():
        resp = session.get(item["thumbnailLink"], timeout=30)
        if resp.status_code != 200 or not resp.content:
            continue
        target.write_bytes(resp.content)
    try:
        drive_hashes.append((item, target, ahash(target)))
    except Exception:
        pass

matches = []
contact_items = []
for row in meta_rows:
    meta_path = Path(row["meta_image_path"])
    ranked = sorted(((distance(ahash(meta_path), h), item, path) for item, path, h in drive_hashes), key=lambda item: (item[0], item[1].get("name", "")))
    best, second = ranked[0], ranked[1]
    status = "Visual_Candidate_High" if best[0] <= 80 and best[0] + 15 < second[0] else "Visual_Candidate_Review"
    matches.append({"Meta_ID": row["meta_id"], "priority_rank": row["priority_rank"], "interactions": row["interactions"], "shares": row["shares"], "Status": status, "distance": best[0], "second_distance": second[0], "Drive_ID_Candidate": best[1]["id"], "Drive_Filename_Candidate": best[1]["name"], "Asset_Ref_Candidate": "", "CNT_Editorial": "", "Evidence_Note": "Similarity shortlist; visual confirmation required."})
    contact_items.append((row, meta_path, best[1], best[2], best[0], status))

with MATCHES.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(matches[0].keys()))
    writer.writeheader()
    writer.writerows(matches)

cols = 3
fig, axes = plt.subplots(1, cols, figsize=(cols * 6, 6), squeeze=False)
for index, ax in enumerate(axes[0]):
    ax.axis("off")
    if index >= len(contact_items):
        continue
    row, meta_path, drive_item, drive_path, d, status = contact_items[index]
    meta_image = Image.open(meta_path).convert("RGB")
    drive_image = Image.open(drive_path).convert("RGB")
    canvas = Image.new("RGB", (900, 700), "white")
    meta_image.thumbnail((410, 610)); drive_image.thumbnail((410, 610))
    canvas.paste(meta_image, (20 + (410 - meta_image.width)//2, 20))
    canvas.paste(drive_image, (470 + (410 - drive_image.width)//2, 20))
    draw = ImageDraw.Draw(canvas)
    draw.text((20, 645), f"Meta rank {row['priority_rank']} | {status} | d={d}", fill="black")
    draw.text((20, 665), f"Drive: {drive_item['name'][:60]}", fill="black")
    ax.imshow(canvas)
plt.tight_layout()
fig.savefig(CONTACT, dpi=160, bbox_inches="tight")
plt.close(fig)
print(json.dumps({"priority_ids": ids, "drive_images": len(drive_files), "drive_hashed": len(drive_hashes), "matches": matches, "contact_sheet": str(CONTACT)}, ensure_ascii=False, indent=2))
