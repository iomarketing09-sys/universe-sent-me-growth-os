#!/usr/bin/env python3
import csv
from pathlib import Path

inventory_path = Path("GrowthOS/Content_Inventory.csv")
taxonomy_path = Path("Operations/Research/2026-08-18_Junio_Lote_Priorizado_Taxonomia_Visual.csv")
priority_path = Path("Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion_Enriquecido.csv")

approved = ["2607823", "2607787", "2607816", "2607828", "260740", "2607837"]

with inventory_path.open(newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

with taxonomy_path.open(newline="", encoding="utf-8-sig") as f:
    taxonomy = {r["asset_ref"]: r for r in csv.DictReader(f)}
with priority_path.open(newline="", encoding="utf-8-sig") as f:
    priority = {r["asset_ref_normalized"]: r for r in csv.DictReader(f)}

existing_refs = {r.get("asset_ref_confirmado", "") for r in rows} | {r.get("Asset_Ref", "") for r in rows}
existing_ids = {r.get("id", "") for r in rows}
next_num = max(int(r[4:]) for r in existing_ids if r.startswith("CNT-") and r[4:].isdigit()) + 1
created = []
for ref in approved:
    if ref in existing_refs:
        raise SystemExit(f"Asset already exists in inventory: {ref}")
    t = taxonomy[ref]
    p = priority[ref]
    cnt = f"CNT-{next_num:03d}"
    next_num += 1
    main = t["personaje_principal_observado"]
    secondary = t["personajes_secundarios_observados"]
    row = {k: "" for k in fieldnames}
    row.update({
        "id": cnt,
        "titulo": p.get("filename_or_concept", f"Asset histórico {ref}"),
        "personaje_principal": f"@char_USM_{main.lower()}" if main in {"Universe", "Wilfred", "Fantasma", "Ganso"} else "No identificado",
        "personajes_secundarios": secondary,
        "tipo_contenido": "Meme imagen histórica / reuse",
        "plataforma": "Facebook; potencial Instagram bajo revisión",
        "objetivo": "Reuse selectivo basado en evidencia histórica",
        "hipotesis": "El rendimiento histórico y la legibilidad visual pueden sostener un reuse contextualizado",
        "estado": "Reuse_Candidate",
        "prioridad": "P1 histórico",
        "dificultad_produccion": "Baja (asset existente)",
        "reutilizable": "Sí — pendiente de calendario y distancia de 30 días",
        "fecha_ultima_publicacion": p.get("date", ""),
        "fuente": "Meta Graph API + Drive + revisión visual aprobada",
        "formato": "Imagen",
        "categoria": "Humor / Meme / Histórico",
        "bloqueado_canon": "No — revisión editorial separada",
        "estado_operacion_normalizado": "Historical_Integrated",
        "estado_canon_normalizado": "Canon_Clear_or_Unverified",
        "asset_ref_confirmado": ref,
        "reconciliacion_estado": "Resolved_Historical_Asset",
        "reconciliacion_confianza": "High",
        "reconciliacion_fuente": "Meta publication + Drive exact filename + visual review",
        "reconciliacion_nota": "Approved for CNT creation and reuse proposal; no publication scheduled.",
        "registro_relacionado": f"Historical_Performance_Individuals; 2026-08-18_Junio_Lote_Priorizado_Taxonomia_Visual",
        "drive_reference_id": t["drive_id"],
        "meta_publication_id": t["meta_id"],
        "asset_set": "06 Junio",
        "Asset_Ref": ref,
        "Asset_Filename": t["drive_filename"],
        "Drive_ID": t["drive_id"],
        "Estado_Canon": "Canon_Clear_or_Unverified",
        "Estado_Produccion": "Asset_Listo",
        "Estado_Publicacion": "Publicada_Historica",
        "Ultima_Sincronizacion": "2026-08-18",
        "Motivo_Revision_Normalizado": "Historical_Asset_Approved_For_Reuse",
        "personaje_principal_normalizado": main,
        "personajes_secundarios_normalizados": secondary,
        "rol_narrativo": t["rol_narrativo_observado"],
        "tipo_humor_normalizado": t["tipo_humor_observado"],
        "potencial_etiquetado": t["potencial_etiquetado_observado"],
        "confianza_taxonomia": t["confianza_visual"],
        "fuente_taxonomia": "Visual review 2026-08-18 + Meta/Drive reconciliation",
        "nota_taxonomia": t["nota_editorial"],
    })
    rows.append(row)
    created.append({"id": cnt, "asset_ref": ref, "meta_id": t["meta_id"], "drive_id": t["drive_id"]})

with inventory_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print(created)
