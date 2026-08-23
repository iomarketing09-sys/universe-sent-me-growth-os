"""Correct classification state for the just-recorded Facebook comment delta."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_05.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
RECORD = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Record_Delta_05.json"
FIELDS = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo",
    "Señal", "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado",
    "Respuesta_Fecha", "Respuesta_Meta_ID", "Insight_Anonimo", "Accion_Calendario",
    "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID", "Privacidad", "Fuente",
    "Ultima_Sincronizacion",
]

review = json.loads(INPUT.read_text(encoding="utf-8"))
review_ids = {row.get("comment_id") for row in review.get("comments", [])}
reviewed_at = review.get("reviewed_at", "")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or FIELDS

changed = 0
human_review = 0
moderation_review = 0
for row in rows:
    if row.get("Comentario_ID") not in review_ids or row.get("Ultima_Sincronizacion") != reviewed_at:
        continue
    if row.get("Respuesta_Estado") == "Pendiente_Respuesta":
        row["Respuesta_Estado"] = "Sin_Revisar"
        row["Respuesta_Sugerida"] = ""
        row["Aprobacion_Estado"] = "No_Aplica"
        changed += 1
    if row.get("Respuesta_Estado") == "Sin_Revisar":
        human_review += 1
    if row.get("Moderacion_Estado") == "Revisar":
        moderation_review += 1

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

record = json.loads(RECORD.read_text(encoding="utf-8"))
record["classification_correction"] = "Pendiente_Respuesta -> Sin_Revisar; no se redactan respuestas sin revisión humana"
record["corrected_rows"] = changed
record["human_review_count"] = human_review
record["moderation_review_count"] = moderation_review
record["no_publication_performed"] = True
RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"corrected_rows": changed, "human_review_count": human_review, "moderation_review_count": moderation_review}, ensure_ascii=False))
