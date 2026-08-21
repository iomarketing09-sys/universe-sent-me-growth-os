from __future__ import annotations

import csv
import json
from pathlib import Path

CALENDAR = Path("Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv")
STAGING = Path("Operations/Research/2026-08-21_Comparable_Experiment_Publication_Staging.csv")
PUBLICATION_LOG = Path("Operations/Research/2026-08-15_Publication_Log.csv")
CANCELLED = Path("/tmp/comparable_cancelled.json")
SCHEDULED = Path("/tmp/comparable_scheduled.json")

with CANCELLED.open(encoding="utf-8") as handle:
    cancelled = {item["old_meta_post_id"]: item for item in json.load(handle)["cancelled"]}
with SCHEDULED.open(encoding="utf-8") as handle:
    scheduled = {item["brief_id"]: item for item in json.load(handle)["scheduled"]}

assert len(cancelled) == 3
assert len(scheduled) == 3

# Update calendar rows with Meta-verified scheduled state.
with CALENDAR.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    calendar_rows = list(reader)
    calendar_fields = reader.fieldnames
assert calendar_fields is not None
calendar_keys = {
    ("2026-08-24", "10:00"): "FUT-MICRO-006",
    ("2026-08-24", "13:30"): "FUT-MICRO-005",
    ("2026-08-27", "16:00"): "FUT-ACID-003",
}
for row in calendar_rows:
    brief = calendar_keys.get((row["Fecha"], row["Hora"]))
    if brief:
        meta = scheduled[brief]
        row["Estado"] = "Programado_Meta_Verificado"
        row["Contexto_Nota"] = f"Facebook programado y verificado vía Meta Graph API v26; reemplazo autorizado de slot anterior; post={meta['post_id']}; foto={meta['photo_id']}."
        row["Asset_Estado_Operativo"] = "Programado_FB_Verificado"
with CALENDAR.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=calendar_fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(calendar_rows)

# Update staging with IDs and verified Meta state.
with STAGING.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    staging_rows = list(reader)
    staging_fields = reader.fieldnames
assert staging_fields is not None
for row in staging_rows:
    meta = scheduled[row["Brief_ID"]]
    row["Estado_Operativo"] = "Programado_Meta_Verificado"
    row["Meta_Action"] = "Scheduled_Verified"
    row["Caption_Status"] = "Approved_By_Fernando"
    row["Meta_Photo_ID"] = meta["photo_id"] if "Meta_Photo_ID" in staging_fields else ""
    row["Meta_Post_ID"] = meta["post_id"] if "Meta_Post_ID" in staging_fields else ""
    row["Meta_Permalink"] = meta["verification"].get("permalink_url", "") if "Meta_Permalink" in staging_fields else ""
    row["Scheduled_Publish_Time_Unix"] = str(meta["scheduled_publish_time"]) if "Scheduled_Publish_Time_Unix" in staging_fields else ""
# Add ID fields if the staging file predates the scheduling result.
for field in ["Meta_Photo_ID", "Meta_Post_ID", "Meta_Permalink", "Scheduled_Publish_Time_Unix"]:
    if field not in staging_fields:
        staging_fields.append(field)
for row in staging_rows:
    meta = scheduled[row["Brief_ID"]]
    row["Meta_Photo_ID"] = meta["photo_id"]
    row["Meta_Post_ID"] = meta["post_id"]
    row["Meta_Permalink"] = meta["verification"].get("permalink_url", "")
    row["Scheduled_Publish_Time_Unix"] = str(meta["scheduled_publish_time"])
with STAGING.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=staging_fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(staging_rows)

# Preserve cancelled rows and append new scheduled rows in Publication_Log.
with PUBLICATION_LOG.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    publication_rows = list(reader)
    publication_fields = reader.fieldnames
assert publication_fields is not None
old_post_ids = set(cancelled)
for row in publication_rows:
    if row.get("Meta_Post_ID") in old_post_ids:
        row["Estado_Publicacion"] = "Cancelada_Autorizada"
        row["Eliminada"] = "Sí"
        row["Notas"] = (row.get("Notas", "") + " Cancelación autorizada por Fernando; DELETE verificado en Meta antes de sustituir el slot.").strip()

by_brief = {
    "FUT-MICRO-006": {
        "asset": "FUT-MICRO-006_HB-007_Microhistoria_Cotidiana_3P_v3.png",
        "date": "2026-08-24", "time": "10:00", "hypothesis": "HB-007",
        "caption": "A veces uno llega tarde y todavía quiere tener la razón. 😭",
    },
    "FUT-MICRO-005": {
        "asset": "FUT-MICRO-005_HB-006_Microhistoria_Romantico_Absurd_3P_v3.png",
        "date": "2026-08-24", "time": "13:30", "hypothesis": "HB-006",
        "caption": "Bueno… tampoco era para tanto. 🤭",
    },
    "FUT-ACID-003": {
        "asset": "FUT-ACID-003_HB-009_Dialogo_Acido_Situacional_v3.png",
        "date": "2026-08-27", "time": "16:00", "hypothesis": "HB-009",
        "caption": "No era una opinión, era evidencia. 😮‍💨",
    },
}
for brief, spec in by_brief.items():
    meta = scheduled[brief]
    publication_rows.append({
        "Publicacion_ID": f"PUB-FB-COMP-{spec['date'].replace('-', '')}-{spec['time'].replace(':', '')}",
        "ID_Pieza": brief,
        "Asset_Ref": spec["asset"],
        "Plataforma": "Facebook",
        "Cuenta_ID": "1036844829507460",
        "Fecha_Planeada_Local": spec["date"],
        "Hora_Planeada_Local": spec["time"],
        "Fecha_Publicacion_Local": "",
        "Hora_Publicacion_Local": "",
        "Meta_Post_ID": meta["post_id"],
        "Meta_Photo_ID": meta["photo_id"],
        "IG_Container_ID": "",
        "IG_Media_ID": "",
        "Permalink": meta["verification"].get("permalink_url", ""),
        "Estado_Publicacion": "Programada",
        "Eliminada": "No",
        "Drive_Archivado": "No — generated asset remains in production repo",
        "Experiment_ID": "EXP-2026-08-COMP-GAPS-01",
        "Hypothesis_ID": spec["hypothesis"],
        "Interacciones_24h": "",
        "Interacciones_72h": "",
        "Notas": f"Caption aprobado por Fernando: {spec['caption']} Meta Graph API v26; is_published=false; scheduled_publish_time verified. Instagram/CNT/affiliates excluded.",
        "Fuente": "2026-08-21_Comparable_Experiment_Publication_Staging.csv; Meta Graph API v26; approval Fernando 2026-08-21",
    })

with PUBLICATION_LOG.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=publication_fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(publication_rows)

print("cancelled_rows_updated=3")
print("scheduled_rows_added=3")
print("metrics_recorded=0")
print("instagram_rows_added=0")
print("cnt_created=0")
