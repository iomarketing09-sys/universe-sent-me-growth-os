from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
APPROVED = {
    "FUT-MICRO-005": "Aprobado para preflight únicamente; no autoriza generación final, calendario, publicación ni CNT.",
    "FUT-MICRO-006": "Aprobado para preflight únicamente; no autoriza generación final, calendario, publicación ni CNT.",
    "FUT-TRANS-003": "Aprobado para preflight únicamente; verificar gafas y marcadores antes de cualquier generación final; no autoriza calendario, publicación ni CNT.",
    "FUT-ACID-003": "Aprobado para preflight únicamente; verificar objetivo ácido, voces y salvaguardas; no autoriza calendario, publicación ni CNT.",
}

with PATH.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

for row in rows:
    brief_id = row["Brief_ID"]
    if brief_id in APPROVED:
        row["Status"] = "Approved_for_Preflight"
        row["Requested_Decision"] = "Approve_Preflight_Only"
        row["Decision_By"] = "Fernando"
        row["Decision_Date"] = "2026-08-21"
        row["Decision_Notes"] = APPROVED[brief_id]

if set(APPROVED) != {row["Brief_ID"] for row in rows if row["Status"] == "Approved_for_Preflight"}:
    raise RuntimeError("La matriz no contiene exactamente los cuatro briefs aprobados para preflight.")

with PATH.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

print(f"approved_for_preflight={len(APPROVED)}")
print(f"path={PATH}")
for row in rows:
    if row["Brief_ID"] in APPROVED:
        print(row["Brief_ID"], row["Status"], row["Requested_Decision"], row["Decision_By"], row["Decision_Date"])
