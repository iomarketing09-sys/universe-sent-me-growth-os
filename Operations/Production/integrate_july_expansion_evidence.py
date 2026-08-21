#!/usr/bin/env python3
"""Integrate confirmed July Meta→Drive evidence without creating CNT."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATCHES = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Matches.csv"
HISTORICAL = ROOT / "Operations/Research/Historical_Performance_Individuals.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def asset_ref(filename: str) -> str:
    found = re.search(r"(?:^|\s)(\d{3,7})(?:\.|\s|$)", filename)
    if not found:
        raise ValueError(f"No numeric Asset_Ref in filename: {filename}")
    return found.group(1)


def parse_date(local: str) -> str:
    return local[:10]


def parse_time(local: str) -> str:
    return local


def main() -> None:
    matches = read_csv(MATCHES)
    confirmed = []
    for row in matches:
        if row.get("Status") != "Visual_Candidate_High":
            continue
        ref = asset_ref(row["Drive_Filename_Candidate"])
        item = dict(row)
        item["Status"] = "Visual_Match_Confirmed"
        item["Asset_Ref_Candidate"] = ref
        item["Evidence_Note"] = "Visual match confirmed from Meta image and Drive thumbnail; filename used only after visual confirmation."
        confirmed.append(item)

    # Promote high-confidence rows in the evidence matrix, keep the borderline untouched.
    match_fields = list(matches[0].keys())
    promoted_by_id = {row["Meta_ID"]: row for row in confirmed}
    for row in matches:
        if row["Meta_ID"] in promoted_by_id:
            row.update(promoted_by_id[row["Meta_ID"]])
    with MATCHES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=match_fields)
        writer.writeheader()
        writer.writerows(matches)

    historical = read_csv(HISTORICAL)
    existing_ids = {row.get("meta_id", "") for row in historical}
    historical_fields = list(historical[0].keys())
    appended = []
    for row in confirmed:
        if row["Meta_ID"] in existing_ids:
            continue
        appended.append(
            {
                "period": "Julio_2026",
                "role": "July expansion lot 01",
                "asset_ref": row["Asset_Ref_Candidate"],
                "filename_or_concept": row["Drive_Filename_Candidate"],
                "meta_id": row["Meta_ID"],
                "date": parse_date(row["Fecha_Local"]),
                "local_time": parse_time(row["Fecha_Local"]),
                "format": "image",
                "metric_definition": "Reacciones + comentarios + shares",
                "metric_value": str(int(row["Interacciones"])),
                "reactions": str(int(row["Interacciones"]) - int(row["Comentarios"]) - int(row["Shares"])),
                "comments": row["Comentarios"],
                "shares": row["Shares"],
                "source": "2026-08-21_Julio_Expansion_Lote01_Visual_Matches.csv",
                "selection_note": "Selected by top shares/comments union; Meta→Drive visual match confirmed; no CNT created.",
                "personaje_principal_normalizado": "Pendiente_revision_visual",
                "personajes_secundarios_normalizados": "Pendiente_revision_visual",
                "rol_narrativo": "Pendiente_revision_visual",
                "tipo_humor_normalizado": "Pendiente_revision_visual",
                "potencial_etiquetado": "Pendiente_revision_visual",
                "confianza_taxonomia": "Pendiente",
                "fuente_taxonomia": "Pending visual taxonomy phase",
                "nota_taxonomia": "Do not infer identity from filename; taxonomy to be applied after evidence integration.",
            }
        )

    if appended:
        with HISTORICAL.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=historical_fields)
            writer.writerows(appended)

    print({"visual_matches_promoted": len(confirmed), "historical_rows_appended": len(appended), "borderline_retained": len(matches) - len(confirmed)})


if __name__ == "__main__":
    main()
