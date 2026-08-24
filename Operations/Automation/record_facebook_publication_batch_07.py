"""Sync verified batch 07 replies into the community ledger and proposal report."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_07.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Expanded_Audit_Reply_Proposals.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_07.json"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != 7 or batch.get("verified_count") != 7:
    raise SystemExit("BATCH_NOT_EXACTLY_SEVEN_VERIFIED")
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
        "Insight_Anonimo": "Respuesta aprobada por Fernando y verificada en Meta.",
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — publicación verificada",
        "Ultima_Sincronizacion": batch.get("published_at", ""),
    })
    records.append({
        "comment_id": parent_id,
        "reply_id": result.get("reply_id"),
        "status": "Respondido",
        "verified": True,
    })

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

proposal_payload = json.loads(PROPOSALS.read_text(encoding="utf-8"))
result_by_parent = {result["parent_comment_id"]: result for result in batch["results"]}
updated_findings = 0
for finding in proposal_payload.get("findings", []):
    result = result_by_parent.get(finding.get("comment_id"))
    if not result:
        continue
    finding.update({
        "disposition": "Respondido",
        "proposed_reply": result.get("message", ""),
        "published": True,
        "published_at": batch.get("published_at", ""),
        "reply_id": result.get("reply_id", ""),
        "verified": result.get("verified", False),
    })
    updated_findings += 1
if updated_findings != 7:
    raise SystemExit(f"PROPOSALS_NOT_UPDATED: {updated_findings}")
proposal_payload["updated_at"] = batch.get("published_at", "")
proposal_payload["publication_scope"]["additional_replies_published_from_this_audit"] = 7
proposal_payload["next_step"] = "Realizar un nuevo corte de solo lectura para identificar comentarios posteriores; no publicar sin autorización explícita."
PROPOSALS.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

payload = {
    "title": "Facebook Comment Publication Record Batch 07",
    "purpose": "Registrar la sincronización de las siete respuestas aprobadas y verificadas en el Community Engagement Log.",
    "status": "Active",
    "created_at": batch.get("published_at"),
    "updated_at": batch.get("published_at"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_07.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Expanded_Audit_Reply_Proposals.json",
    ],
    "organization": "Operations/Research",
    "recorded_at": batch.get("published_at"),
    "source": "Meta Graph API v26.0",
    "batch_file": str(BATCH.relative_to(ROOT)),
    "updated_rows": len(records),
    "verified_rows": len(records),
    "records": records,
    "new_audit_proposals_published": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "updated_rows": len(records),
    "verified_rows": len(records),
    "proposal_findings_updated": updated_findings,
}, ensure_ascii=False))
