"""Repair Respondido ledger rows using the read-only Meta verification report.

No Facebook writes. The script only corrects fields where the current Meta
GET evidence is decisive and preserves historical values in the repair report.
Three HTTP 400 reply IDs remain Respondido because historical publication
records exist; they are marked as currently inaccessible rather than retried.
"""

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
VERIFICATION = RESEARCH / "2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json"
OUT = RESEARCH / "2026-08-24_Facebook_Complete_Responded_Registration_Repair.json"

# Meta returned the actual parent ID for this historical reply; the old ledger
# value was a different, inaccessible object ID. This is a data correction,
# not a new publication.
COMMENT_ID_CORRECTIONS = {
    "122151374823072582_1041411610869463": "122151374823072582_1041411612075968",
}

verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fields = reader.fieldnames or []
if len(fields) != 20:
    raise SystemExit(f"EXPECTED_20_LEDGER_COLUMNS: {len(fields)}")
by_id = {row.get("Comentario_ID"): row for row in rows}
if len(by_id) != len(rows):
    raise SystemExit("LEDGER_COMMENT_ID_DUPLICATE_BEFORE_REPAIR")

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
corrections = []
historical_inaccessible = []
for result in verification.get("results", []):
    old_comment_id = result.get("comment_id")
    row = by_id.get(old_comment_id)
    if row is None:
        raise SystemExit(f"VERIFICATION_COMMENT_NOT_IN_LEDGER: {old_comment_id}")
    original = dict(row)
    current_comment_id = old_comment_id
    if old_comment_id in COMMENT_ID_CORRECTIONS:
        new_comment_id = COMMENT_ID_CORRECTIONS[old_comment_id]
        if new_comment_id in by_id and new_comment_id != old_comment_id:
            raise SystemExit(f"COMMENT_ID_CORRECTION_COLLISION: {new_comment_id}")
        row["Comentario_ID"] = new_comment_id
        by_id.pop(old_comment_id)
        by_id[new_comment_id] = row
        current_comment_id = new_comment_id
        row["Insight_Anonimo"] = (row.get("Insight_Anonimo", "").rstrip(". ") + ". " if row.get("Insight_Anonimo") else "") + f"Corrección de registro: Meta confirmó que el parent del reply es {new_comment_id}; se reemplazó el ID histórico {old_comment_id}."
        corrections.append({"type": "comment_id", "old_comment_id": old_comment_id, "new_comment_id": new_comment_id, "reply_id": result.get("reply_id")})

    if result.get("api_ok"):
        api_message = result.get("api_message")
        if api_message and row.get("Respuesta_Sugerida") != api_message:
            before = row.get("Respuesta_Sugerida", "")
            row["Respuesta_Sugerida"] = api_message
            row["Insight_Anonimo"] = (row.get("Insight_Anonimo", "").rstrip(". ") + ". " if row.get("Insight_Anonimo") else "") + "Texto de respuesta corregido para coincidir exactamente con Meta Graph API v26.0."
            corrections.append({"type": "response_text", "comment_id": current_comment_id, "reply_id": result.get("reply_id"), "before": before, "after": api_message})
        if result.get("api_created_time"):
            row["Respuesta_Fecha"] = result["api_created_time"]
        if result.get("parent_semantics") and result.get("parent_semantics") != "direct_parent":
            row["Insight_Anonimo"] = (row.get("Insight_Anonimo", "").rstrip(". ") + ". " if row.get("Insight_Anonimo") else "") + f"Verificación parent: {result['parent_semantics']}."
    else:
        row["Insight_Anonimo"] = (row.get("Insight_Anonimo", "").rstrip(". ") + ". " if row.get("Insight_Anonimo") else "") + "La publicación histórica se conserva como Respondido; la verificación actual del reply devuelve HTTP 400 y no se reintentará para evitar duplicados."
        historical_inaccessible.append({
            "comment_id": current_comment_id,
            "historical_comment_id": old_comment_id if current_comment_id != old_comment_id else None,
            "reply_id": result.get("reply_id"),
            "status_code": result.get("status_code"),
            "error": result.get("error"),
            "evidence_record_present_before_reconciliation": result.get("evidence_record_present_before_reconciliation"),
        })
    row["Ultima_Sincronizacion"] = now
    row["Privacidad"] = "Anonimizado"

# After all corrections, enforce unique comment IDs and preserve the original
# append-only row ordering by writing rows in their existing order.
final_ids = [row.get("Comentario_ID") for row in rows]
if any(not item for item in final_ids) or len(set(final_ids)) != len(final_ids):
    raise SystemExit("LEDGER_COMMENT_ID_DUPLICATE_AFTER_REPAIR")
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

payload = {
    "title": "Facebook — reparación completa del registro de comentarios respondidos",
    "purpose": "Corregir el Community Engagement Log con evidencia de Meta Graph API v26.0: dos textos de respuesta, un ID de comentario con alias histórico y tres respuestas históricas actualmente inaccesibles; sin publicar ni modificar Facebook.",
    "status": "Active",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json",
        "Operations/Research/2026-08-24_Facebook_Inaccessible_Replies_Recovery_Search.json",
        "Operations/Research/2026-08-24_Facebook_Missing_Replies_Thread_Scan.json",
        "Operations/Research/2026-08-24_Facebook_All_Replies_Reconciliation.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.md",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 GET-only verification plus historical publication evidence",
    "ledger_rows": len(rows),
    "ledger_respondido_rows": sum(1 for row in rows if row.get("Respuesta_Estado") == "Respondido"),
    "corrections_applied": len(corrections),
    "correction_details": corrections,
    "historical_inaccessible_count": len(historical_inaccessible),
    "historical_inaccessible": historical_inaccessible,
    "facebook_writes_performed": 0,
    "no_reply_retries": True,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"ledger_rows": len(rows), "ledger_respondido_rows": payload["ledger_respondido_rows"], "corrections_applied": len(corrections), "historical_inaccessible_count": len(historical_inaccessible), "facebook_writes_performed": 0}, ensure_ascii=False))
for correction in corrections:
    print(json.dumps(correction, ensure_ascii=False))
