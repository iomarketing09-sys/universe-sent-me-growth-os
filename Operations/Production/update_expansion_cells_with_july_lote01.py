#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"

NEW_ROWS = [
    {
        "Cell_ID": "MICRO-004",
        "Cell_Name": "Microhistoria secuencial",
        "Meta_ID": "1036844829507460_122135607981072582",
        "Fecha": "2026-07-03",
        "Interacciones": "2441",
        "Comentarios": "15",
        "Shares": "774",
        "Personaje_o_rol_observado": "No identificado",
        "Subgrupo_o_estructura": "microhistoria_dos_paneles",
        "Tipo_humor": "Relatable / observacional",
        "Estado_Candidato": "Candidate_Review",
        "Comparability_Note": "Secuencia visual de dos paneles; puede ampliar la subcelda de dos paneles, pero no cuenta en la microhistoria estricta de tres paneles.",
        "Caption_Treatment": "historical_unavailable",
        "Caption_Evidence": "El histórico no conserva tratamiento de caption separado",
        "Source": "2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv",
    },
    {
        "Cell_ID": "OBS-005",
        "Cell_Name": "Humor observacional",
        "Meta_ID": "1036844829507460_122141376093072582",
        "Fecha": "2026-07-24",
        "Interacciones": "3002",
        "Comentarios": "41",
        "Shares": "625",
        "Personaje_o_rol_observado": "No identificado",
        "Subgrupo_o_estructura": "composicion_mundo_conceptual",
        "Tipo_humor": "Observacional social / relatable",
        "Estado_Candidato": "Candidate_Review",
        "Comparability_Note": "Sistema solar como objeto de observación social; la celda ya alcanza n=3 y este caso se reserva para análisis de sensibilidad.",
        "Caption_Treatment": "historical_unavailable",
        "Caption_Evidence": "El histórico no conserva tratamiento de caption separado",
        "Source": "2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv",
    },
    {
        "Cell_ID": "SELF-006",
        "Cell_Name": "Autodesprecio / antihéroe",
        "Meta_ID": "1036844829507460_122139232911072582",
        "Fecha": "2026-07-16",
        "Interacciones": "3740",
        "Comentarios": "31",
        "Shares": "904",
        "Personaje_o_rol_observado": "Universe",
        "Subgrupo_o_estructura": "autopercepcion_aislamiento",
        "Tipo_humor": "Relatable / existencial",
        "Estado_Candidato": "Candidate_Review",
        "Comparability_Note": "Aislamiento y autopercepción como posible antihéroe; revisar si cumple el criterio de autodesprecio y no solo relatable cotidiano.",
        "Caption_Treatment": "historical_unavailable",
        "Caption_Evidence": "El histórico no conserva tratamiento de caption separado",
        "Source": "2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv",
    },
    {
        "Cell_ID": "SELF-007",
        "Cell_Name": "Autodesprecio / antihéroe",
        "Meta_ID": "1036844829507460_122138846193072582",
        "Fecha": "2026-07-13",
        "Interacciones": "1609",
        "Comentarios": "15",
        "Shares": "335",
        "Personaje_o_rol_observado": "Universe",
        "Subgrupo_o_estructura": "autopercepcion_solteria",
        "Tipo_humor": "Relatable / ácido",
        "Estado_Candidato": "Candidate_Review",
        "Comparability_Note": "La soltería se expresa como deseo/estado interno; puede ser autopercepción absurda, pero también humor relacional. No contar sin revisión funcional.",
        "Caption_Treatment": "historical_unavailable",
        "Caption_Evidence": "El histórico no conserva tratamiento de caption separado",
        "Source": "2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv",
    },
]

with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))
fieldnames = list(rows[0].keys())
existing_ids = {row["Meta_ID"] for row in rows}
appended = [row for row in NEW_ROWS if row["Meta_ID"] not in existing_ids]
if appended:
    with MATRIX.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerows(appended)
print({"appended": len(appended), "matrix_rows": len(rows) + len(appended), "new_meta_ids": [row["Meta_ID"] for row in appended]})
