#!/usr/bin/env python3
import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[2] / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
TARGET_ID = "122151376083072582_1712631733280410"
REPLY_ID = "122151376083072582_1634044988141953"
REPLY_DATE = "2026-08-23T16:31:53+0000"
NOTE = "Respuesta publicada y visible; Meta devolvió parent de la respuesta previa de Universe Sent Me (122151376083072582_1093298379810084), no el ID de la réplica objetivo; no se reintentó para evitar duplicado."

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
    reader = csv.DictReader(source)
    fieldnames = reader.fieldnames
    rows = list(reader)

found = False
for row in rows:
    if row["Comentario_ID"] == TARGET_ID:
        if row["Respuesta_Estado"] != "Pendiente_Respuesta":
            raise SystemExit(f"Unexpected state: {row['Respuesta_Estado']}")
        row["Respuesta_Estado"] = "Respondido"
        row["Aprobacion_Estado"] = "Aprobada"
        row["Respuesta_Fecha"] = REPLY_DATE
        row["Respuesta_Meta_ID"] = REPLY_ID
        row["Insight_Anonimo"] = (row["Insight_Anonimo"] + " " + NOTE).strip()
        found = True
        break

if not found:
    raise SystemExit(f"Target not found: {TARGET_ID}")

with CSV_PATH.open("w", encoding="utf-8", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print(f"REGISTERED={TARGET_ID}")
print(f"REPLY_ID={REPLY_ID}")
