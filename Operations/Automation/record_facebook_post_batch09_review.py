"""Record the post-batch-09 read-only finding without publishing."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h_Post_Batch09.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Post_Batch09_Review_Record.json"

audit = json.loads(AUDIT.read_text(encoding="utf-8"))
new_rows = audit.get("new_unanswered_not_in_ledger", [])
if len(new_rows) != 1:
    raise SystemExit(f"EXPECTED_ONE_NEW_FINDING: {len(new_rows)}")
item = new_rows[0]
if item.get("comment_type") != "Replica_Anidada":
    raise SystemExit("NEW_FINDING_NOT_USER_REPLICA")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
comment_id = item["comment_id"]
row = by_id.get(comment_id)
if row is None:
    row = {key: "" for key in fieldnames}
    row["Comentario_ID"] = comment_id
    row["Post_ID"] = item.get("post_id", "")
    row["CNT_ID"] = ""
    row["Fecha_Comentario"] = item.get("comment_created_time", "")
    row["Plataforma"] = "Facebook"
    row["Tipo"] = "Replica_Anidada"
    rows.append(row)
    by_id[comment_id] = row
row.update({
    "Señal": "Conversación_Usuario_Usuario",
    "Respuesta_Estado": "No_Requiere_Respuesta",
    "Respuesta_Sugerida": "",
    "Aprobacion_Estado": "No_Aplica",
    "Respuesta_Fecha": "",
    "Respuesta_Meta_ID": "",
    "Insight_Anonimo": "Réplica de usuario a usuario; no interrumpir la conversación desde la Página.",
    "Accion_Calendario": "Ninguna",
    "Prioridad": "Baja",
    "Moderacion_Estado": "No_Accion",
    "Privacidad": "Anonimizado",
    "Fuente": "Meta Graph API v26.0 — auditoría posterior al Batch 09",
    "Ultima_Sincronizacion": audit.get("reviewed_at", ""),
})
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

payload = {
    "title": "Facebook Post-Batch 09 Review Record",
    "purpose": "Registrar un hallazgo nuevo de solo lectura clasificado como réplica usuario-a-usuario y fuera de la cola de respuesta.",
    "status": "Active",
    "created_at": audit.get("reviewed_at"),
    "updated_at": audit.get("reviewed_at"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h_Post_Batch09.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_Remaining.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "reviewed_at": audit.get("reviewed_at"),
    "new_rows_added": 1 if row.get("Comentario_ID") == comment_id and comment_id not in set() else 1,
    "no_action_rows": 1,
    "publication_performed": False,
    "comment_ids": [comment_id],
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"new_rows_added": 1, "no_action_rows": 1, "publication_performed": False}, ensure_ascii=False))
