"""Record the 24 verified replies published after the Batch 14 review."""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Batch14.json"
REVIEW = ROOT / "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
RECORD = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Batch14.json"
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Approved_Publication.json"
EXPECTED = 24

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != EXPECTED or batch.get("verified_count") != EXPECTED:
    raise SystemExit(f"BATCH_NOT_EXACTLY_{EXPECTED}_VERIFIED: {batch.get('requested_count')} requested, {batch.get('verified_count')} verified")
if len(batch.get("results", [])) != EXPECTED or any(row.get("verified") is not True for row in batch["results"]):
    raise SystemExit("UNVERIFIED_OR_MISSING_PUBLICATION_RESULT")

review_data = json.loads(REVIEW.read_text(encoding="utf-8"))
review_by_id = {row.get("comment_id"): row for row in review_data.get("records", [])}
if len(review_by_id) != len(review_data.get("records", [])):
    raise SystemExit("DUPLICATE_REVIEW_COMMENT_IDS")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fields = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
if len(by_id) != len(rows):
    raise SystemExit("DUPLICATE_LEDGER_COMMENT_IDS")

recorded_at = batch.get("updated_at") or datetime.now(timezone.utc).isoformat(timespec="seconds")
records: list[dict[str, Any]] = []
for result in batch["results"]:
    cid = result["parent_comment_id"]
    row = by_id.get(cid)
    if row is None:
        raise SystemExit(f"COMMENT_NOT_IN_LEDGER: {cid}")
    review_row = review_by_id.get(cid)
    if review_row is None:
        raise SystemExit(f"COMMENT_NOT_IN_REVIEW: {cid}")
    if row.get("Respuesta_Estado") == "Respondido" and row.get("Respuesta_Meta_ID") not in ("", result.get("reply_id", "")):
        raise SystemExit(f"CONFLICTING_EXISTING_REPLY_ID: {cid}")

    existing_insight = row.get("Insight_Anonimo", "")
    marker = "Post-Batch 14: respuesta publicada y verificada mediante Meta Graph API v26.0."
    if marker not in existing_insight:
        existing_insight = (existing_insight.rstrip(". ") + ". " if existing_insight else "") + marker
    row.update(
        {
            "Respuesta_Estado": "Respondido",
            "Respuesta_Sugerida": result.get("message", ""),
            "Aprobacion_Estado": "Aprobada",
            "Respuesta_Fecha": result.get("created_time", ""),
            "Respuesta_Meta_ID": result.get("reply_id", ""),
            "Insight_Anonimo": existing_insight,
            "Accion_Calendario": "Ninguna",
            "Moderacion_Estado": "No_Accion",
            "Privacidad": "Anonimizado",
            "Fuente": "Meta Graph API v26.0 — publicación posterior al Batch 14 verificada",
            "Ultima_Sincronizacion": recorded_at,
        }
    )

    review_row.update(
        {
            "prior_editorial_decision": review_row.get("editorial_decision"),
            "prior_approval_state": review_row.get("approval_state"),
            "editorial_decision": "Respondido",
            "approval_state": "Aprobada",
            "response_status": "Respondido",
            "publication_count": 1,
            "reply_id": result.get("reply_id", ""),
            "published_at": result.get("created_time", ""),
            "verified": True,
            "publication_parent_semantics": result.get("parent_semantics"),
        }
    )
    records.append(
        {
            "comment_id": cid,
            "reply_id": result.get("reply_id"),
            "reply_created_time": result.get("created_time"),
            "status": "Respondido",
            "verified": True,
            "publication_status": result.get("status"),
            "parent_semantics": result.get("parent_semantics"),
        }
    )

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

review_data.update(
    {
        "status": "Active",
        "updated_at": recorded_at,
        "publication_status": "24/24 published and verified",
        "publication_record": "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Batch14.json",
        "published_count": EXPECTED,
        "verified_count": EXPECTED,
        "approval_required_for_future_writes": True,
    }
)
REVIEW.write_text(json.dumps(review_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state_counts = Counter(row.get("Respuesta_Estado", "") for row in rows)
queue = {
    "title": "Facebook Pending Queue After Approved Publication — Post-Batch 14 Review",
    "purpose": "Estado del ledger después de publicar y verificar las 24 respuestas aprobadas del corte posterior al Batch 14.",
    "status": "Active",
    "created_at": batch.get("created_at", recorded_at),
    "updated_at": recorded_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Batch14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Community Engagement Log synchronized with verified Meta Graph API v26.0 publication record; no additional comments included",
    "ledger_rows": len(rows),
    "facebook_pending_count": state_counts.get("Pendiente_Respuesta", 0),
    "facebook_pending_with_proposal": state_counts.get("Pendiente_Respuesta", 0),
    "published_from_approved_review": len(records),
    "verified_from_approved_review": len(records),
    "no_action_count": state_counts.get("No_Requiere_Respuesta", 0),
    "archived_count": state_counts.get("Archivado", 0),
    "pending": [],
    "publication_summary": {
        "requested": batch.get("requested_count"),
        "published": batch.get("published_count"),
        "already_published": batch.get("already_published_count"),
        "verified": batch.get("verified_count"),
        "direct_target_parent": batch.get("strict_direct_parent_count"),
        "nested_target_parent_semantics": batch.get("nested_target_parent_semantics_count"),
    },
}
QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

record_payload = {
    "title": "Facebook Comment Publication Record — 24 Approved Replies After Batch 14",
    "purpose": "Registrar las 24 respuestas aprobadas explícitamente por Fernando, publicadas y verificadas mediante Meta Graph API v26.0.",
    "status": "Active",
    "created_at": batch.get("created_at", recorded_at),
    "updated_at": recorded_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.md",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Approved_Publication.json",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "page_id": "1036844829507460",
    "explicit_user_approval": True,
    "approval_source": "Fernando aprobó las 24 respuestas en conversación antes de la publicación.",
    "requested_count": EXPECTED,
    "published_count": batch.get("published_count"),
    "already_published_count": batch.get("already_published_count"),
    "verified_count": EXPECTED,
    "strict_direct_parent_count": batch.get("strict_direct_parent_count"),
    "nested_target_parent_semantics_count": batch.get("nested_target_parent_semantics_count"),
    "no_duplicate_posts": True,
    "records": records,
}
RECORD.write_text(json.dumps(record_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"updated_ledger_rows": len(records), "verified": len(records), "ledger_rows": len(rows), "ledger_pending": state_counts.get("Pendiente_Respuesta", 0), "queue_pending": 0}, ensure_ascii=False))
