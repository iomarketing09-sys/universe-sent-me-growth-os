#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
OUTPUT = INPUT
APPROVAL_DATE = "2026-08-21"
APPROVER = "Fernando"

with INPUT.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

new_fields = ["approval_status", "approval_by", "approval_date", "approval_scope"]
fields = list(rows[0].keys())
for field in new_fields:
    if field not in fields:
        fields.append(field)

approved = 0
cell_pending = 0
reserve = 0
for row in rows:
    action = row.get("recommended_action")
    if action == "Analyze_Character_No_CNT":
        row["approval_status"] = "Approved_Character_Analysis"
        row["approval_by"] = APPROVER
        row["approval_date"] = APPROVAL_DATE
        row["approval_scope"] = "Selective_character_analysis_only; no CNT; no canon; no calendar"
        approved += 1
    elif action == "Cell_Candidate_Review":
        row["approval_status"] = "Pending_Cell_Validation"
        row["approval_by"] = ""
        row["approval_date"] = ""
        row["approval_scope"] = "Validation protocol required before comparable-cell denominator"
        cell_pending += 1
    else:
        row["approval_status"] = "Reserve_Not_Approved"
        row["approval_by"] = ""
        row["approval_date"] = ""
        row["approval_scope"] = "No character analysis until a concrete question reopens the case"
        reserve += 1

with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print({"rows": len(rows), "approved_character_analysis": approved, "pending_cell_validation": cell_pending, "reserve_not_approved": reserve, "approval_by": APPROVER, "approval_date": APPROVAL_DATE})
