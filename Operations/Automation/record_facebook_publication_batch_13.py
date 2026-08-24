"""Sync verified Batch 13 replies and preserve explicit exclusions."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_13.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_13.json"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != 10 or batch.get("verified_count") != 10:
    raise SystemExit("BATCH_NOT_EXACTLY_10_VERIFIED")
if any(not result.get("verified") for result in batch.get("results", [])):
    raise SystemExit("UNVERIFIED_RESULT_PRESENT")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fields = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
records = []
for result in batch["results"]:
    cid = result["parent_comment_id"]
    row = by_id.get(cid)
    if row is None:
        raise SystemExit(f"PARENT_NOT_IN_LEDGER: {cid}")
    row.update({
        "Respuesta_Estado": "Respondido",
        "Respuesta_Sugerida": result.get("message", ""),
        "Aprobacion_Estado": "Aprobada",
        "Respuesta_Fecha": batch.get("published_at", ""),
        "Respuesta_Meta_ID": result.get("reply_id", ""),
        "Insight_Anonimo": "Respuesta aprobada por Fernando y verificada en Meta Graph API v26.0.",
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — publicación verificada",
        "Ultima_Sincronizacion": batch.get("published_at", ""),
    })
    records.append({"comment_id": cid, "reply_id": result.get("reply_id"), "status": "Respondido", "verified": True})
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
result_by_parent = {result["parent_comment_id"]: result for result in batch["results"]}
for item in queue.get("pending", []):
    result = result_by_parent.get(item.get("comment_id"))
    if not result:
        continue
    item.update({"status": "Respondido", "published": True, "approval_status": "Aprobada", "reply_id": result.get("reply_id")})
queue["published_from_batch13"] = 10
queue["excluded_from_batch13"] = batch.get("excluded_comment_ids", [])
queue["next_step"] = "Revisar solo los dos excluidos: L Roberto no responder y comentario inaccesible sin texto no forzar."
QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

payload = {
    "title": "Facebook Comment Publication Record Batch 13",
    "purpose": "Registrar diez respuestas aprobadas y verificadas; conservar explícitamente fuera del lote a L Roberto y el comentario inaccesible.",
    "status": "Active",
    "created_at": batch.get("published_at"),
    "updated_at": batch.get("published_at"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_13.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "recorded_at": batch.get("published_at"),
    "source": "Meta Graph API v26.0",
    "updated_rows": len(records),
    "verified_rows": len(records),
    "excluded_comment_ids": batch.get("excluded_comment_ids", []),
    "records": records,
    "new_proposals_published": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"updated_rows": len(records), "verified_rows": len(records), "excluded": len(batch.get("excluded_comment_ids", []))}, ensure_ascii=False))
