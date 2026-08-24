"""Sync the partially completed music batch and preserve the inaccessible parent."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_09.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_09.json"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != 5 or batch.get("verified_count") != 4:
    raise SystemExit("BATCH_NOT_EXPECTED_PARTIAL_RESULT")
verified_results = [result for result in batch.get("results", []) if result.get("verified")]
blocked_results = [result for result in batch.get("results", []) if result.get("status") == "unavailable"]
if len(verified_results) != 4 or len(blocked_results) != 1:
    raise SystemExit("BATCH_PARTIAL_RESULT_MISMATCH")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
records = []
for result in verified_results:
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
        "Insight_Anonimo": "Respuesta musical aprobada por Fernando y verificada en Meta.",
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — publicación verificada",
        "Ultima_Sincronizacion": batch.get("published_at", ""),
    })
    records.append({"comment_id": parent_id, "reply_id": result.get("reply_id"), "status": "Respondido", "verified": True})
for result in blocked_results:
    parent_id = result["parent_comment_id"]
    row = by_id.get(parent_id)
    if row is None:
        raise SystemExit(f"BLOCKED_PARENT_NOT_IN_LEDGER: {parent_id}")
    row.update({
        "Insight_Anonimo": "Aprobada por Fernando, pero no publicada: Meta devolvió objeto de comentario inaccesible (HTTP 400 / código 100).",
        "Fuente": "Meta Graph API v26.0 — publicación bloqueada por objeto inaccesible",
        "Ultima_Sincronizacion": batch.get("published_at", ""),
    })

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
result_by_parent = {result["parent_comment_id"]: result for result in batch["results"]}
for collection_name in ("music_proposals", "all_pending_proposals"):
    for item in queue.get(collection_name, []):
        result = result_by_parent.get(item.get("comment_id"))
        if not result:
            continue
        if result.get("verified"):
            item.update({"status": "Respondido", "published": True, "reply_id": result.get("reply_id"), "approval_status": "Aprobada"})
        elif result.get("status") == "unavailable":
            item.update({"status": "Bloqueado_API", "published": False, "api_error": result.get("error")})
queue["publication_performed"] = True
queue["published_from_queue"] = len(verified_results)
queue["inaccessible_from_queue"] = len(blocked_results)
queue["next_step"] = "Revisar la cola restante; el comentario inaccesible requiere una nueva lectura API antes de intentar cualquier respuesta."
QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

payload = {
    "title": "Facebook Comment Publication Record Batch 09 — Music Thread",
    "purpose": "Registrar cuatro respuestas musicales verificadas y un comentario aprobado bloqueado por inaccesibilidad en Meta.",
    "status": "Active",
    "created_at": batch.get("published_at"),
    "updated_at": batch.get("published_at"),
    "version": "1.1",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_09.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json",
    ],
    "organization": "Operations/Research",
    "recorded_at": batch.get("published_at"),
    "source": "Meta Graph API v26.0",
    "batch_file": str(BATCH.relative_to(ROOT)),
    "updated_rows": len(verified_results),
    "verified_rows": len(verified_results),
    "blocked_rows": len(blocked_results),
    "records": records,
    "blocked": [{"comment_id": result["parent_comment_id"], "status": "Bloqueado_API", "error": result.get("error")} for result in blocked_results],
    "new_proposals_published": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"updated_rows": len(verified_results), "verified_rows": len(verified_results), "blocked_rows": len(blocked_results)}, ensure_ascii=False))
