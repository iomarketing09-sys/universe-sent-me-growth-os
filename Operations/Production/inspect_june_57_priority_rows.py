#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Meta_Raw.json"
TARGET_RANKS = {61, 98, 108, 120, 126, 128, 149, 155, 161, 163, 169, 170, 174, 177, 179, 180, 181, 183, 184, 185, 191, 195, 205, 206, 208, 210, 211, 212, 215, 216, 218, 220, 221, 223, 229, 230}

data = json.loads(RAW.read_text(encoding="utf-8"))
selected = []
for row in data["records"]:
    rank = int(row["priority_rank"])
    if rank in TARGET_RANKS:
        selected.append({"rank": rank, "meta_id": row["meta_id"], "date": row["date"], "interactions": row["interactions_queue"], "shares": row["shares_queue"], "comments": row["comments_queue"], "caption": row["caption"], "has_image": bool(row["image_path"])})
for row in selected:
    print(json.dumps(row, ensure_ascii=False))
OUTPUT = ROOT / "Operations/Research/2026-08-21_Junio_57_Priority_Rows.json"
OUTPUT.write_text(json.dumps(selected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"saved={OUTPUT}")
