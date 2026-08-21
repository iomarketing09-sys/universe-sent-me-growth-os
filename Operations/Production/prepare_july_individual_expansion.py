#!/usr/bin/env python3
"""Prepare a small, reproducible July historical expansion queue.

The script selects posts from the homogeneous June/July comparison dataset,
excludes July posts already reconciled individually, and never assigns an
Asset_Ref or CNT. Visual matching remains a separate evidence step.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPARABLE = ROOT / "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
INDIVIDUAL = ROOT / "Operations/Research/Historical_Performance_Individuals.csv"
DRIVE_EXPORT = Path("/tmp/usm_july_drive_assets.ndjson")
OUTPUT = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
SUMMARY = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01_Summary.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def numeric(row: dict[str, str], field: str) -> float:
    value = (row.get(field) or "").strip()
    return float(value) if value else 0.0


def main() -> None:
    comparable = [r for r in read_csv(COMPARABLE) if r.get("month") == "2026-07"]
    individual = [r for r in read_csv(INDIVIDUAL) if r.get("period") == "Julio_2026"]
    reconciled_ids = {r.get("meta_id", "") for r in individual if r.get("meta_id")}

    with DRIVE_EXPORT.open(encoding="utf-8") as handle:
        drive_payload = json.load(handle)
    drive_files = [f for f in drive_payload.get("files", []) if f.get("mimeType", "").startswith("image/")]

    # Drive evidence is inventoried only for the next visual-matching phase.
    # No filename is assigned to a Meta post in this script.
    rows = []
    for row in comparable:
        if row.get("id") in reconciled_ids:
            continue
        rows.append(
            {
                "Meta_ID": row.get("id", ""),
                "Fecha_Local": row.get("local", ""),
                "Caption": row.get("message", ""),
                "Interacciones": int(numeric(row, "interactions")),
                "Reacciones": int(numeric(row, "reactions")),
                "Comentarios": int(numeric(row, "comments")),
                "Shares": int(numeric(row, "shares")),
                "Hora_Local": row.get("hour", ""),
                "Prioridad_Actual": "Needs_Visual_Match",
                "Asset_Ref": "",
                "Drive_ID": "",
                "CNT_Editorial": "",
                "Evidencia": "Selected from homogeneous July dataset; no visual match asserted.",
            }
        )

    by_shares = sorted(rows, key=lambda r: (-r["Shares"], -r["Interacciones"], -r["Comentarios"], r["Meta_ID"]))
    by_comments = sorted(rows, key=lambda r: (-r["Comentarios"], -r["Shares"], -r["Interacciones"], r["Meta_ID"]))

    selected: dict[str, dict[str, str]] = {}
    for rank, row in enumerate(by_shares[:12], start=1):
        item = dict(row)
        item["Motivo_Seleccion"] = "Top_12_Shares"
        item["Rank_Shares"] = str(rank)
        item["Rank_Comentarios"] = ""
        selected[row["Meta_ID"]] = item
    for rank, row in enumerate(by_comments[:12], start=1):
        if row["Meta_ID"] in selected:
            selected[row["Meta_ID"]]["Motivo_Seleccion"] += "+Top_12_Comentarios"
            selected[row["Meta_ID"]]["Rank_Comentarios"] = str(rank)
        else:
            item = dict(row)
            item["Motivo_Seleccion"] = "Top_12_Comentarios"
            item["Rank_Shares"] = ""
            item["Rank_Comentarios"] = str(rank)
            selected[row["Meta_ID"]] = item

    final_rows = sorted(
        selected.values(),
        key=lambda r: (-r["Shares"], -r["Comentarios"], -r["Interacciones"], r["Meta_ID"]),
    )
    fieldnames = [
        "Meta_ID", "Fecha_Local", "Caption", "Interacciones", "Reacciones", "Comentarios", "Shares",
        "Hora_Local", "Motivo_Seleccion", "Rank_Shares", "Rank_Comentarios", "Prioridad_Actual",
        "Asset_Ref", "Drive_ID", "CNT_Editorial", "Evidencia",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

    summary = {
        "created": "2026-08-21",
        "source_comparable_rows_july": len(comparable),
        "already_reconciled_individual_july": len(reconciled_ids),
        "remaining_july_rows_before_selection": len(rows),
        "selected_lote01_rows": len(final_rows),
        "selection_rule": "Union of top 12 by shares and top 12 by comments, excluding the six individually reconciled July posts.",
        "drive_folder_inventory": {
            "folder_id": "1apek-EqSsM5DI7wUcRkzJpbs9HUWQxeg",
            "image_files_available_for_visual_matching": len(drive_files),
            "note": "Drive files are not assigned to posts by filename or date in this phase.",
        },
        "guardrails": [
            "No Asset_Ref assigned automatically.",
            "No CNT created.",
            "Visual match required before taxonomy or inventory integration.",
            "Lifetime historical metrics remain separate from August 24/72-hour metrics.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
