#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
TARGET = "1036844829507460_122127951885072582"

with PATH.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

new_fields = ["validation_status", "validation_date", "validated_by", "validation_cell", "validation_notes"]
fields = list(rows[0].keys())
for field in new_fields:
    if field not in fields:
        fields.append(field)

found = 0
for row in rows:
    for field in new_fields:
        row.setdefault(field, "")
    if row.get("meta_id") != TARGET:
        continue
    row["validation_status"] = "Excluded_3P_Retain_4P_Candidate"
    row["validation_date"] = "2026-08-21"
    row["validated_by"] = "Manus"
    row["validation_cell"] = "MICRO-STRICT-3P"
    row["validation_notes"] = "Four panels confirmed; passes visual sequence, turn clarity and provisional remate; fails exact three-panel rule; retain only for a future MICRO-SEQ-4P definition."
    found += 1

if found != 1:
    raise RuntimeError(f"Expected exactly one target row, found {found}")

with PATH.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print({"target": TARGET, "validation_status": "Excluded_3P_Retain_4P_Candidate", "cell": "MICRO-STRICT-3P"})
