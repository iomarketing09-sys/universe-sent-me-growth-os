"""Sync verified Batch 13 replies and explicit editorial exclusions."""

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_13.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
QUEUE_SOURCE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json"
QUEUE_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch13.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_13.json"

EXCLUSION_DECISIONS = {
    "122151375549072582_1817089682764579": {
        "status": "No_Requiere_Respuesta",
        "reason": "Fernando indicó no contestar esta réplica de usuario a usuario; no interrumpir el intercambio.",
        "source": "Meta Graph API v26.0 — exclusión editorial explícita de Fernando",
    },
    "122151376011072582_1703056380925949": {
        "status": "Archivado",
        "reason": "Objeto de comentario inaccesible para Meta (HTTP 400 / código 100); Fernando indicó no forzar una respuesta no verificable.",
        "source": "Meta Graph API v26.0 — objeto inaccesible; exclusión explícita de Fernando",
    },
}

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != 10 or batch.get("verified_count") != 10:
    raise SystemExit("BATCH_NOT_EXACTLY_10_VERIFIED")
if any(not result.get("verified") for result in batch.get("results", [])):
    raise SystemExit("UNVERIFIED_RESULT_PRESENT")
if set(batch.get("excluded_comment_ids", [])) != set(EXCLUSION_DECISIONS):
    raise SystemExit("EXCLUSION_SET_MISMATCH")

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

excluded_records = []
for cid, decision in EXCLUSION_DECISIONS.items():
    row = by_id.get(cid)
    if row is None:
        raise SystemExit(f"EXCLUDED_COMMENT_NOT_IN_LEDGER: {cid}")
    row.update({
        "Respuesta_Estado": decision["status"],
        "Aprobacion_Estado": "No_Aplica",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": decision["reason"],
        "Accion_Calendario": "Ninguna",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": decision["source"],
        "Ultima_Sincronizacion": batch.get("published_at", ""),
    })
    excluded_records.append({"comment_id": cid, "status": decision["status"], "reason": decision["reason"], "published": False})

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

source_queue = json.loads(QUEUE_SOURCE.read_text(encoding="utf-8"))
result_by_parent = {result["parent_comment_id"]: result for result in batch["results"]}
resolved = []
for item in source_queue.get("pending", []):
    cid = item.get("comment_id")
    result = result_by_parent.get(cid)
    if result:
        resolved.append({"comment_id": cid, "outcome": "Respondido", "reply_id": result.get("reply_id"), "verified": True})
        continue
    decision = EXCLUSION_DECISIONS.get(cid)
    if decision:
        resolved.append({"comment_id": cid, "outcome": decision["status"], "reason": decision["reason"], "verified": False})
        source_queue.setdefault("no_action", []).append({"comment_id": cid, "post_id": item.get("post_id", ""), "reason": decision["reason"]})

if len(resolved) != 12:
    raise SystemExit(f"EXPECTED_12_RECONCILED_ITEMS: {len(resolved)}")

state_counts = Counter(row.get("Respuesta_Estado", "") for row in rows)
queue = {
    "title": "Facebook Pending Queue After Batch 13",
    "purpose": "Estado actual de la cola del ledger después de publicar y verificar el Batch 13; las diez propuestas autorizadas fueron respondidas y los dos casos restantes fueron excluidos explícitamente.",
    "status": "Active",
    "created_at": "2026-08-24",
    "updated_at": "2026-08-24",
    "version": "1.2",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_13.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_13.json",
    ],
    "organization": "Operations/Research",
    "source": "Community Engagement Log synchronized with Meta Graph API v26.0 publication records; current queue calculated after verified Batch 13 without a new broad API sweep",
    "ledger_rows": len(rows),
    "facebook_pending_count": state_counts.get("Pendiente_Respuesta", 0),
    "facebook_pending_with_proposal": 0,
    "facebook_pending_without_proposal": 0,
    "facebook_no_action_count": state_counts.get("No_Requiere_Respuesta", 0) + state_counts.get("Archivado", 0),
    "published_from_batch13": len(records),
    "excluded_from_batch13": [item["comment_id"] for item in excluded_records],
    "responded_from_batch13": [item["comment_id"] for item in records],
    "reconciled_batch13": resolved,
    "pending": [],
    "no_action": source_queue.get("no_action", []),
}
QUEUE_OUT.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

payload = {
    "title": "Facebook Comment Publication Record Batch 13",
    "purpose": "Registrar diez respuestas aprobadas y verificadas y dos exclusiones editoriales explícitas; conservar la trazabilidad sin repetir publicaciones.",
    "status": "Active",
    "created_at": batch.get("published_at"),
    "updated_at": batch.get("published_at"),
    "version": "1.1",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_13.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch13.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "recorded_at": batch.get("published_at"),
    "source": "Meta Graph API v26.0",
    "updated_rows": len(records),
    "verified_rows": len(records),
    "excluded_rows": len(excluded_records),
    "excluded_comment_ids": batch.get("excluded_comment_ids", []),
    "records": records,
    "excluded_records": excluded_records,
    "new_proposals_published": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"updated_rows": len(records), "verified_rows": len(records), "excluded_rows": len(excluded_records), "ledger_pending": state_counts.get("Pendiente_Respuesta", 0)}, ensure_ascii=False))
