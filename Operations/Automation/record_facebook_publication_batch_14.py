"""Record verified Batch 14 Facebook replies and update project ledgers."""

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json"
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
RECORD = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_14.json"
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch14.json"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != 13 or batch.get("verified_count") != 13 or len(batch.get("results", [])) != 13:
    raise SystemExit("BATCH_NOT_EXACTLY_13_VERIFIED")
if any(result.get("verified") is not True for result in batch["results"]):
    raise SystemExit("UNVERIFIED_RESULT_PRESENT")

proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
proposal_by_id = {item.get("comment_id"): item for item in proposal_data.get("proposals", [])}
if len(proposal_by_id) != 13 or set(proposal_by_id) != {result["parent_comment_id"] for result in batch["results"]}:
    raise SystemExit("PROPOSAL_BATCH_ID_SET_MISMATCH")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fields = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
recorded_at = batch.get("updated_at") or datetime.now(timezone.utc).isoformat(timespec="seconds")
records = []
for result in batch["results"]:
    cid = result["parent_comment_id"]
    row = by_id.get(cid)
    if row is None:
        raise SystemExit(f"COMMENT_NOT_IN_LEDGER: {cid}")
    existing_insight = row.get("Insight_Anonimo", "")
    marker = "Batch 14 publicado y verificado"
    if marker not in existing_insight:
        existing_insight = (existing_insight.rstrip(". ") + ". " if existing_insight else "") + marker + " mediante Meta Graph API v26.0."
    row.update({
        "Respuesta_Estado": "Respondido",
        "Respuesta_Sugerida": result.get("message", ""),
        "Aprobacion_Estado": "Aprobada",
        "Respuesta_Fecha": result.get("reply_created_time", ""),
        "Respuesta_Meta_ID": result.get("reply_id", ""),
        "Insight_Anonimo": existing_insight,
        "Accion_Calendario": "Ninguna",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — Batch 14 publicación verificada",
        "Ultima_Sincronizacion": recorded_at,
    })
    proposal = proposal_by_id[cid]
    proposal.update({
        "status": "Respondido",
        "approval_status": "Aprobada",
        "reply_id": result.get("reply_id", ""),
        "published_at": result.get("reply_created_time", ""),
        "verified": True,
        "publication_parent_semantics": result.get("parent_semantics"),
    })
    records.append({
        "comment_id": cid,
        "reply_id": result.get("reply_id"),
        "reply_created_time": result.get("reply_created_time"),
        "status": "Respondido",
        "verified": True,
        "publication_status": result.get("status"),
        "parent_semantics": result.get("parent_semantics"),
    })

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

proposal_data.update({
    "status": "Active",
    "updated_at": recorded_at,
    "published": True,
    "published_at": batch.get("published_at"),
    "publication_record": "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_14.json",
    "authorization_required": True,
    "authorization_satisfied": True,
    "published_count": 13,
})
PROPOSALS.write_text(json.dumps(proposal_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state_counts = Counter(row.get("Respuesta_Estado", "") for row in rows)
queue = {
    "title": "Facebook Pending Queue After Batch 14",
    "purpose": "Estado del ledger después de publicar y verificar las 13 respuestas aprobadas del Batch 14.",
    "status": "Active",
    "created_at": "2026-08-24",
    "updated_at": recorded_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Community Engagement Log synchronized with verified Meta Graph API v26.0 publication record; no new broad API sweep after publication",
    "ledger_rows": len(rows),
    "facebook_pending_count": state_counts.get("Pendiente_Respuesta", 0),
    "facebook_pending_with_proposal": 0,
    "published_from_batch14": len(records),
    "verified_from_batch14": len(records),
    "no_action_count": state_counts.get("No_Requiere_Respuesta", 0),
    "archived_count": state_counts.get("Archivado", 0),
    "pending": [],
    "publication_summary": {
        "requested": batch.get("requested_count"),
        "verified": batch.get("verified_count"),
        "already_published_before_recovery": batch.get("already_published_before_recovery_count"),
        "recovered_after_partial_publish": batch.get("recovered_after_partial_publish_count"),
        "published_during_recovery": batch.get("published_during_recovery_count"),
        "strict_direct_parent": batch.get("strict_direct_parent_count"),
        "nested_immediate_parent_semantics": batch.get("nested_immediate_parent_semantics_count"),
    },
}
QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

record_payload = {
    "title": "Facebook Comment Publication Record Batch 14",
    "purpose": "Registrar las 13 respuestas aprobadas, publicadas y verificadas; conservar la recuperación idempotente de la ejecución parcial.",
    "status": "Active",
    "created_at": batch.get("published_at"),
    "updated_at": recorded_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json",
        "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json",
        "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.md",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch14.json",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "page_id": "1036844829507460",
    "explicit_user_approval": True,
    "approval_source": "Fernando aprobó las 13 respuestas del Batch 14 antes de la publicación.",
    "requested_count": 13,
    "published_count": 13,
    "verified_count": 13,
    "already_published_before_recovery_count": batch.get("already_published_before_recovery_count"),
    "recovered_after_partial_publish_count": batch.get("recovered_after_partial_publish_count"),
    "published_during_recovery_count": batch.get("published_during_recovery_count"),
    "strict_direct_parent_count": batch.get("strict_direct_parent_count"),
    "nested_immediate_parent_semantics_count": batch.get("nested_immediate_parent_semantics_count"),
    "nested_root_parent_semantics_count": batch.get("nested_root_parent_semantics_count"),
    "no_duplicate_posts": True,
    "records": records,
}
RECORD.write_text(json.dumps(record_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"updated_ledger_rows": len(records), "verified": len(records), "ledger_rows": len(rows), "ledger_pending": state_counts.get("Pendiente_Respuesta", 0), "queue_pending": 0}, ensure_ascii=False))
