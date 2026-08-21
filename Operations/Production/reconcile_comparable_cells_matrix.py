#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
ROUND2 = ROOT / "Operations/Research/2026-08-20_Expansion_Round2_Candidatos.csv"

with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))
fieldnames = list(rows[0].keys())

# Avoid the ID used by the excluded one-panel case in the round-2 source.
for row in rows:
    if row.get("Meta_ID") == "1036844829507460_122135607981072582":
        row["Cell_ID"] = "MICRO2-004"
        row["Cell_Name"] = "Microhistoria secuencial — dos paneles"

with ROUND2.open(newline="", encoding="utf-8-sig") as handle:
    round2_rows = list(csv.DictReader(handle))
existing_ids = {row["Meta_ID"] for row in rows}
append = [row for row in round2_rows if row.get("Estado_Candidato") == "Current_Comparable" and row.get("Meta_ID") not in existing_ids]
rows.extend(append)

with MATRIX.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print({"round2_comparables_added": len(append), "matrix_rows": len(rows), "new_ids": [row["Meta_ID"] for row in append]})
