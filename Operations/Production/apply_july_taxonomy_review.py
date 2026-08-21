#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSIST = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Assist.json"
HISTORICAL = ROOT / "Operations/Research/Historical_Performance_Individuals.csv"
REVIEWED_JSON = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.json"
REVIEWED_CSV = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv"

PRINCIPAL_OVERRIDES = {
    # Generic human or resource visuals are not assigned to canon by appearance.
    "1036844829507460_122138831577072582": ("No identificado", "Media", "Solo se observan manos y accesorios; no hay evidencia suficiente para asignar personaje."),
    "1036844829507460_122135016567072582": ("No identificado", "Media", "La secuencia contiene figuras humanas y un gato, pero no confirma un personaje canónico por marcadores visuales."),
    # A white cat with the recurring glasses marker is treated as Universe.
    "1036844829507460_122137968789072582": ("Universe", "Alta", "Las gafas y la morfología del gato aportan un marcador visual suficiente para Universe."),
}

PRINCIPAL_CONFIDENCE = {
    "1036844829507460_122135577327072582": ("No identificado", "Media"),
    "1036844829507460_122135607981072582": ("No identificado", "Media"),
    "1036844829507460_122139161997072582": ("No identificado", "Alta"),
    "1036844829507460_122141376093072582": ("No identificado", "Alta"),
    "1036844829507460_122135586723072582": ("No identificado", "Media"),
    "1036844829507460_122142625983072582": ("No identificado", "Alta"),
}

ROLE_MAP = {
    "Protagonista": "Protagonista",
    "Duo_o_pareja": "Dúo o pareja",
    "Reparto_coral": "Reparto coral",
    "Escena_observacional": "Escena observacional",
    "No_determinado": "No determinado",
}
HUMOR_MAP = {
    "Existencial_o_absurdo": "Existencial o absurdo",
    "Relatable_cotidiano": "Relatable cotidiano",
    "Observacional_social": "Observacional social",
    "Humor_acido_o_negro": "Humor ácido o negro",
    "Sexual_o_insinuacion": "Sexual o insinuación",
    "Fandom_o_referencia": "Fandom o referencia",
    "Reaccion_o_emoji": "Reacción o emoji",
    "Conversacional": "Conversacional",
    "No_determinado": "No determinado",
}


def main() -> None:
    payload = json.loads(ASSIST.read_text(encoding="utf-8"))
    reviewed = []
    by_id = {}
    for result in payload["results"]:
        item = dict(result)
        meta_id = item["Meta_ID"]
        if meta_id in PRINCIPAL_OVERRIDES:
            principal, confidence, note = PRINCIPAL_OVERRIDES[meta_id]
            item["personaje_principal_observado"] = principal
            item["confianza_taxonomia"] = confidence
            item["cautela"] = note
        elif meta_id in PRINCIPAL_CONFIDENCE:
            principal, confidence = PRINCIPAL_CONFIDENCE[meta_id]
            item["personaje_principal_observado"] = principal
            item["confianza_taxonomia"] = confidence
        item["review_status"] = "Reviewed_Conservative"
        item["review_note"] = "Vision model used as assistive evidence; final identity labels follow visual markers and the TAX-01 process rule."
        reviewed.append(item)
        by_id[meta_id] = item
    reviewed.sort(key=lambda row: row["Meta_ID"])
    REVIEWED_JSON.write_text(json.dumps({"source": str(ASSIST), "results": reviewed, "canon_status": "No canon change"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with HISTORICAL.open(newline="", encoding="utf-8-sig") as handle:
        historical = list(csv.DictReader(handle))
    for row in historical:
        item = by_id.get(row.get("meta_id"))
        if not item:
            continue
        principal = item["personaje_principal_observado"]
        if principal == "No_identificado":
            principal = "No identificado"
        secondary = item.get("personajes_secundarios_observados") or []
        secondary_values = [value for value in secondary if value not in ("No_identificado", "Ninguno")]
        if row.get("meta_id") == "1036844829507460_122135586723072582":
            secondary_values = []
        row["personaje_principal_normalizado"] = principal
        item["personaje_principal_observado"] = principal
        row["personajes_secundarios_normalizados"] = ";".join(secondary_values) if secondary_values else "Ninguno"
        row["rol_narrativo"] = ROLE_MAP[item["rol_narrativo"]]
        row["tipo_humor_normalizado"] = ";".join(HUMOR_MAP[value] for value in item["tipo_humor_normalizado"])
        row["potencial_etiquetado"] = item["potencial_etiquetado"]
        row["confianza_taxonomia"] = item["confianza_taxonomia"]
        row["fuente_taxonomia"] = "Visual_Meta_Drive_Review + Vision_Assist_2026-08-21"
        row["nota_taxonomia"] = item["cautela"] or item["review_note"]

    fieldnames = list(historical[0].keys())
    with HISTORICAL.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(historical)

    # A compact reviewed table is useful for audits and does not duplicate the ledger.
    compact_fields = ["Meta_ID", "personaje_principal_observado", "personajes_secundarios_observados", "rol_narrativo", "tipo_humor_normalizado", "potencial_etiquetado", "estructura_narrativa", "caption_treatment", "confianza_taxonomia", "evidencia_visual_breve", "cautela", "review_status"]
    with REVIEWED_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=compact_fields)
        writer.writeheader()
        for item in reviewed:
            writer.writerow({key: ";".join(item[key]) if isinstance(item[key], list) else item.get(key, "") for key in compact_fields})

    print(json.dumps({"reviewed_rows": len(reviewed), "historical_ledger": str(HISTORICAL), "reviewed_json": str(REVIEWED_JSON), "reviewed_csv": str(REVIEWED_CSV)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
