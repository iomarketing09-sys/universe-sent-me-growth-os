#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
SUMMARY = ROOT / "Operations/Research/2026-08-21_Expansion_Celdas_Comparables_Post_Julio_Lote01.json"

PROMOTIONS = {
    "1036844829507460_122135607981072582": {
        "Cell_ID": "MICRO2-003",
        "Cell_Name": "Microhistoria secuencial — dos paneles",
        "Estado_Candidato": "Current_Comparable",
        "Comparability_Note": "Promovido a la subcelda de dos paneles: dos momentos visuales con cambio funcional claro. No cuenta en la microhistoria estricta de tres paneles.",
    },
    "1036844829507460_122134169481072582": {
        "Estado_Candidato": "Current_Comparable",
        "Comparability_Note": "Promovido como subvariante antihéroe/autopercepción dentro de la celda amplia. Debe reportarse por separado de autodesprecio directo; la discrepancia asset_ref se conserva y Meta_ID es la clave primaria.",
    },
}

with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))
fieldnames = list(rows[0].keys())
changed = []
for row in rows:
    patch = PROMOTIONS.get(row.get("Meta_ID"))
    if not patch:
        continue
    row.update(patch)
    changed.append(row["Meta_ID"])
with MATRIX.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Summary is intentionally based on the candidate matrix, not on inferred taxonomy.
by_cell = {}
for row in rows:
    cell = row["Cell_Name"]
    bucket = by_cell.setdefault(cell, {"current_comparable": [], "candidate_review": [], "excluded_or_borderline": []})
    status = row["Estado_Candidato"]
    if status == "Current_Comparable":
        bucket["current_comparable"].append(row)
    elif status == "Candidate_Review":
        bucket["candidate_review"].append(row)
    else:
        bucket["excluded_or_borderline"].append(row)

def ints(rows, field):
    return [int(float(row[field] or 0)) for row in rows]

def stats(rows):
    import statistics
    interactions = ints(rows, "Interacciones")
    shares = ints(rows, "Shares")
    return {"n": len(rows), "interactions": interactions, "shares": shares, "median_interactions": statistics.median(interactions) if interactions else 0, "median_shares": statistics.median(shares) if shares else 0}

summary = {"created": "2026-08-21", "changed_meta_ids": changed, "cells": {cell: {"current": stats(bucket["current_comparable"]), "candidates": stats(bucket["candidate_review"]), "excluded_or_borderline": len(bucket["excluded_or_borderline"])} for cell, bucket in by_cell.items()}, "guardrails": ["Microhistoria estricta de tres paneles permanece n=1.", "Microhistoria de dos paneles se mantiene separada.", "Autodesprecio directo y antihéroe/autopercepción se reportan con sensibilidad.", "No se promovieron transformación ni diálogo ácido.", "No canon, no calendario, no CNT."]}
SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"promoted": changed, "summary": str(SUMMARY)}, ensure_ascii=False, indent=2))
