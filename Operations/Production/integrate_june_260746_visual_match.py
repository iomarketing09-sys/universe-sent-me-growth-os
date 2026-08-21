#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META_ID = "1036844829507460_122129404893072582"
ASSET_REF = "260746"
FILENAME = "Universe - Existencial 260746.png"
DRIVE_ID = "1CYrpRf4KUOClP_Qvcc65yDx0Sq-JIguk"

QUEUE_FILES = [
    # Source-of-truth reconciliation queue only; derivative priority views are not rewritten.
    ROOT / "Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv",
]
INDEX = ROOT / "Operations/Research/June_Visual_Asset_Index.csv"
MATCHES = ROOT / "Operations/Research/2026-08-21_Junio_Priority_Queue_Visual_Matches.csv"
HISTORICAL = ROOT / "Operations/Research/Historical_Performance_Individuals.csv"


def read(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write(path, rows):
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

changed = {}
for path in QUEUE_FILES:
    rows = read(path)
    n = 0
    for row in rows:
        if row.get("meta_id") != META_ID:
            continue
        row["status"] = "Visual_Confirmed"
        row["asset_ref_known"] = f"{ASSET_REF} - {FILENAME}"
        row["next_evidence_needed"] = f"Photo object, Meta post and visual image match confirmed; Drive_ID={DRIVE_ID}; CNT assignment not created."
        n += 1
    write(path, rows)
    changed[str(path)] = n

rows = read(INDEX)
index_changed = 0
for row in rows:
    if row.get("asset_ref") != ASSET_REF:
        continue
    row["visual_status"] = "Asset_Indexed_Visual_Confirmed"
    row["meta_match_status"] = "Visual_Match_Confirmed"
    row["meta_post_id"] = META_ID
    row["publication_date_local"] = "2026-06-11T23:37:20-06:00"
    row["evidence_source"] = "Drive visual index + Meta image contact sheet 2026-08-21"
    row["last_analyzed_at"] = "2026-08-21"
    index_changed += 1
write(INDEX, rows)

matches = read(MATCHES)
match_changed = 0
for row in matches:
    if row.get("Meta_ID") != META_ID:
        continue
    row["Status"] = "Visual_Match_Confirmed"
    row["Drive_ID_Candidate"] = DRIVE_ID
    row["Drive_Filename_Candidate"] = FILENAME
    row["Asset_Ref_Candidate"] = ASSET_REF
    row["Evidence_Note"] = "Visual match confirmed from Meta image and Drive thumbnail; filename recorded only after visual confirmation; no CNT created."
    match_changed += 1
write(MATCHES, matches)

historical = read(HISTORICAL)
existing = {row.get("meta_id") for row in historical}
appended = 0
if META_ID not in existing:
    fields = list(historical[0].keys())
    historical.append({
        "period": "Junio_2026",
        "role": "June priority queue visual match",
        "asset_ref": ASSET_REF,
        "filename_or_concept": FILENAME,
        "meta_id": META_ID,
        "date": "2026-06-11",
        "local_time": "2026-06-11T23:37:20-06:00",
        "format": "image",
        "metric_definition": "Reacciones + comentarios + shares",
        "metric_value": "155",
        "reactions": "135",
        "comments": "1",
        "shares": "19",
        "source": "2026-08-21_Junio_Priority_Queue_Visual_Findings.md",
        "selection_note": f"Priority 26; Meta→Drive visual match confirmed; Drive_ID={DRIVE_ID}; no CNT created.",
        "personaje_principal_normalizado": "No identificado",
        "personajes_secundarios_normalizados": "Hada visualmente compatible",
        "rol_narrativo": "Microhistoria secuencial",
        "tipo_humor_normalizado": "Relatable cotidiano;Existencial o absurdo",
        "potencial_etiquetado": "Alto",
        "confianza_taxonomia": "Alta",
        "fuente_taxonomia": "Visual review + Lote A",
        "nota_taxonomia": "Diálogo de tres paneles; no mapear el hada a Kiri automáticamente.",
    })
    write(HISTORICAL, historical)
    appended = 1
print({"queue_files_changed": changed, "visual_index_changed": index_changed, "visual_matches_changed": match_changed, "historical_rows_appended": appended, "meta_id": META_ID, "asset_ref": ASSET_REF, "drive_id": DRIVE_ID})
