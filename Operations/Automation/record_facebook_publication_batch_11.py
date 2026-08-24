"""Sync verified batch 11 replies into the ledger and proposal artifact."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_11.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_11.json"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != 28 or batch.get("verified_count") != 28:
    raise SystemExit("BATCH_NOT_EXACTLY_28_VERIFIED")
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

proposals = json.loads(PROPOSALS.read_text(encoding="utf-8"))
by_parent = {result["parent_comment_id"]: result for result in batch["results"]}
for item in proposals.get("proposals", []):
    result = by_parent.get(item.get("comment_id"))
    if result:
        item.update({"status": "Respondido", "published": True, "approval_status": "Aprobada", "reply_id": result.get("reply_id")})
proposals["publication_performed"] = True
proposals["published_count"] = 28
proposals["verified_count"] = 28
proposals["next_step"] = "Revisar los 9 casos sin acción; no publicar sin nueva aprobación explícita."
PROPOSALS.write_text(json.dumps(proposals, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

payload = {
    "title": "Facebook Comment Publication Record Batch 11 — ☁️✨🤔",
    "purpose": "Registrar la sincronización de las 28 respuestas aprobadas y verificadas del post ☁️✨🤔, manteniendo los 9 casos sin acción separados.",
    "status": "Active",
    "created_at": batch.get("published_at"),
    "updated_at": batch.get("published_at"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_11.json",
        "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.json",
        "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.md",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "recorded_at": batch.get("published_at"),
    "source": "Meta Graph API v26.0",
    "batch_file": str(BATCH.relative_to(ROOT)),
    "updated_rows": len(records),
    "verified_rows": len(records),
    "records": records,
    "no_action_count": 9,
    "new_proposals_published": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"updated_rows": len(records), "verified_rows": len(records), "no_action_count": 9}, ensure_ascii=False))
