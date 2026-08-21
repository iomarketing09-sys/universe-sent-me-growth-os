from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-21_Autorizacion_Generacion_Briefs_Comparables.csv"
EXPECTED = {"FUT-MICRO-005", "FUT-MICRO-006", "FUT-TRANS-003", "FUT-ACID-003"}

with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

if {row["Brief_ID"] for row in rows} != EXPECTED:
    raise RuntimeError("La matriz no contiene exactamente los cuatro briefs aprobados.")

for row in rows:
    row["Generation_Authorization"] = "Approved_Generation_Only"
    row["Decision"] = "Approved"
    row["Decision_By"] = "Fernando"
    row["Decision_Date"] = "2026-08-21"
    row["Decision_Notes"] = "Fernando aprobó los cuatro briefs para generación únicamente; no autoriza calendario, CNT, reuse, afiliados ni publicación."

with MATRIX.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(f"generation_approval_registered={len(rows)}/{len(EXPECTED)}")
print("scope=Approved_Generation_Only")
print("calendar_change=No cnt_creation=No publication=No affiliate_attachment=No")
print("decision_by=Fernando decision_date=2026-08-21")
