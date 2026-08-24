"""Sync verified batch 10 replies into the ledger and pending queue."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_10.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_10.json"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != 25 or batch.get("verified_count") != 25:
    raise SystemExit("BATCH_NOT_EXACTLY_25_VERIFIED")
if any(not result.get("verified") for result in batch.get("results", [])):
    raise SystemExit("UNVERIFIED_RESULT_PRESENT")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
records = []
for result in batch["results"]:
    parent_id = result["parent_comment_id"]
    row = by_id.get(parent_id)
    if row is None:
        raise SystemExit(f"PARENT_NOT_IN_LEDGER: {parent_id}")
    row.update({
        "Respuesta_Estado": "Respondido",
        "Respuesta_Sugerida": result.get("message", ""),
        "Aprobacion_Estado": "Aprobada",
        "Respuesta_Fecha": batch.get("published_at", ""),
        "Respuesta_Meta_ID": result.get("reply_id", ""),
        "Insight_Anonimo": "Respuesta de personalidad USM aprobada por Fernando y verificada en Meta.",
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — publicación verificada",
        "Ultima_Sincronizacion": batch.get("published_at", ""),
    })
    records.append({"comment_id": parent_id, "reply_id": result.get("reply_id"), "status": "Respondido", "verified": True})
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
reply_by_parent = {result["parent_comment_id"]: result for result in batch["results"]}
for collection_name in ("all_pending_proposals", "music_proposals"):
    for item in queue.get(collection_name, []):
        result = reply_by_parent.get(item.get("comment_id"))
        if not result:
            continue
        item.update({
            "status": "Respondido",
            "published": True,
            "approval_status": "Aprobada",
            "reply_id": result.get("reply_id"),
        })
queue["published_from_queue"] = queue.get("published_from_queue", 0) + 25
queue["next_step"] = "Auditar de nuevo el hilo ☁️✨🤔 y preparar solo propuestas nuevas; no publicar sin nueva aprobación."
QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

payload = {
    "title": "Facebook Comment Publication Record Batch 10 — ☁️✨🤔",
    "purpose": "Registrar la sincronización de las 25 respuestas aprobadas y verificadas del post ☁️✨🤔.",
    "status": "Active",
    "created_at": batch.get("published_at"),
    "updated_at": batch.get("published_at"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_10.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_10.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json",
    ],
    "organization": "Operations/Research",
    "recorded_at": batch.get("published_at"),
    "source": "Meta Graph API v26.0",
    "batch_file": str(BATCH.relative_to(ROOT)),
    "updated_rows": len(records),
    "verified_rows": len(records),
    "records": records,
    "new_proposals_published": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"updated_rows": len(records), "verified_rows": len(records)}, ensure_ascii=False))
