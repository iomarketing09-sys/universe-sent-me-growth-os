#!/usr/bin/env python3
"""Match July expansion Meta images against the July Drive folder.

This is an evidence aid, not a filename-to-CNT assigner. It uses thumbnail
perceptual similarity to shortlist exact visual candidates, then produces a
contact sheet for visual confirmation.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
DRIVE_EXPORT = Path("/tmp/usm_july_drive_assets.ndjson")
META_IMAGE_DIR = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Meta_Images"
DRIVE_INDEX = ROOT / "Operations/Research/2026-08-21_Julio_Drive_Asset_Index.json"
CACHE_DIR = Path("/tmp/usm_july_drive_thumbnails")
MATCHES = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Matches.csv"
CONTACT = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Contact_Sheet.jpg"
FOLDER_ID = "1apek-EqSsM5DI7wUcRkzJpbs9HUWQxeg"


def average_hash(path: Path, size: int = 32) -> tuple[int, ...]:
    with Image.open(path) as image:
        image = image.convert("L").resize((size, size))
        pixels = list(image.getdata())
    mean = sum(pixels) / len(pixels)
    return tuple(1 if value >= mean else 0 for value in pixels)


def hamming(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b))


def download_thumb(session: requests.Session, file_id: str, url: str) -> Path | None:
    target = CACHE_DIR / f"{file_id}.jpg"
    if target.exists() and target.stat().st_size > 0:
        return target
    response = session.get(url, timeout=30)
    if response.status_code != 200 or not response.content:
        return None
    target.write_bytes(response.content)
    return target


def load_queue() -> list[dict[str, str]]:
    with QUEUE.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    with DRIVE_EXPORT.open(encoding="utf-8") as handle:
        drive_payload = json.load(handle)
    drive_files = [f for f in drive_payload.get("files", []) if f.get("mimeType", "").startswith("image/") and f.get("thumbnailLink")]
    DRIVE_INDEX.write_text(
        json.dumps({"folder_id": FOLDER_ID, "extracted_from": str(DRIVE_EXPORT), "files": drive_files}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    drive_hashes = []
    for index, file in enumerate(drive_files, start=1):
        thumb = download_thumb(session, file["id"], file["thumbnailLink"])
        if not thumb:
            continue
        try:
            drive_hashes.append((file, thumb, average_hash(thumb)))
        except Exception:
            continue
        if index % 100 == 0:
            print(f"downloaded_drive_thumbnails={index}")

    queue = load_queue()
    match_rows = []
    contact_items = []
    for row in queue:
        meta_id = row["Meta_ID"]
        meta_path = META_IMAGE_DIR / f"{meta_id}.jpg"
        if not meta_path.exists():
            match_rows.append({"Meta_ID": meta_id, "Status": "Meta_image_missing"})
            continue
        meta_hash = average_hash(meta_path)
        ranked = sorted(((hamming(meta_hash, h), file, thumb) for file, thumb, h in drive_hashes), key=lambda item: item[0])
        best_distance, best_file, best_thumb = ranked[0]
        second_distance = ranked[1][0] if len(ranked) > 1 else ""
        status = "Visual_Candidate_High" if best_distance <= 80 and (second_distance == "" or best_distance + 15 < second_distance) else "Visual_Candidate_Review"
        match_rows.append(
            {
                "Meta_ID": meta_id,
                "Fecha_Local": row.get("Fecha_Local", ""),
                "Interacciones": row.get("Interacciones", ""),
                "Shares": row.get("Shares", ""),
                "Comentarios": row.get("Comentarios", ""),
                "Status": status,
                "Distance": best_distance,
                "Second_Best_Distance": second_distance,
                "Drive_ID_Candidate": best_file.get("id", ""),
                "Drive_Filename_Candidate": best_file.get("name", ""),
                "Drive_Thumbnail": best_file.get("thumbnailLink", ""),
                "Asset_Ref_Candidate": "",
                "CNT_Editorial": "",
                "Evidence_Note": "Perceptual similarity shortlist only; requires visual confirmation before inventory integration.",
            }
        )
        contact_items.append((row, meta_path, best_file, best_thumb, best_distance, status))

    fieldnames = list(match_rows[0].keys()) if match_rows else ["Meta_ID"]
    with MATCHES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(match_rows)

    cols = 4
    cell_w, cell_h = 480, 360
    rows_n = (len(contact_items) + cols - 1) // cols
    fig, axes = plt.subplots(rows_n, cols, figsize=(cols * 4.8, rows_n * 3.6), squeeze=False)
    for index, ax in enumerate(axes.flat):
        ax.axis("off")
        if index >= len(contact_items):
            continue
        row, meta_path, drive_file, drive_thumb, distance, status = contact_items[index]
        with Image.open(meta_path) as meta_image:
            meta_image = meta_image.convert("RGB")
        with Image.open(drive_thumb) as drive_image:
            drive_image = drive_image.convert("RGB")
        combined = Image.new("RGB", (cell_w, cell_h), "white")
        meta_image.thumbnail((cell_w // 2 - 10, cell_h - 80))
        drive_image.thumbnail((cell_w // 2 - 10, cell_h - 80))
        combined.paste(meta_image, (10 + (cell_w // 2 - meta_image.width) // 2, 10))
        combined.paste(drive_image, (cell_w // 2 + (cell_w // 2 - drive_image.width) // 2, 10))
        draw = ImageDraw.Draw(combined)
        draw.text((10, cell_h - 65), f"Meta {row['Meta_ID'].split('_')[-1]} | {status} | d={distance}", fill="black")
        draw.text((10, cell_h - 42), f"Drive: {drive_file.get('name', '')[:66]}", fill="black")
        draw.text((10, cell_h - 20), "Izq. Meta / Der. Drive — confirmar visualmente", fill="black")
        ax.imshow(combined)

    plt.tight_layout()
    fig.savefig(CONTACT, dpi=160, bbox_inches="tight")
    plt.close(fig)

    counts = {}
    for row in match_rows:
        counts[row.get("Status", "Unknown")] = counts.get(row.get("Status", "Unknown"), 0) + 1
    print(json.dumps({"drive_images": len(drive_files), "drive_thumbnails_hashed": len(drive_hashes), "queue_rows": len(queue), "matches": counts, "matches_csv": str(MATCHES), "contact_sheet": str(CONTACT), "drive_index": str(DRIVE_INDEX)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
