"""Reconcile all historically published Facebook replies with the community ledger.

Read-only by default. It treats the publication record files as the evidence
source, deduplicates by target comment ID, and reports missing or inconsistent
ledger fields without changing the CSV.
"""

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
OUT = RESEARCH / "2026-08-24_Facebook_All_Replies_Reconciliation.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def record_from_raw(raw, source_file, index, batch_label):
    if "comment_id" in raw:
        comment_id = raw.get("comment_id")
    else:
        comment_id = raw.get("target_comment_id") or raw.get("parent_comment_id")
    reply_id = raw.get("reply_id")
    if not reply_id:
        reply_id = ((raw.get("post_response") or {}).get("id"))
    verification = raw.get("verification") or {}
    verification_payload = verification.get("payload") or {}
    message = raw.get("message") or raw.get("response_message") or verification_payload.get("message")
    created_time = raw.get("reply_created_time") or raw.get("created_time") or verification_payload.get("created_time") or raw.get("run_at_utc")
    verified = raw.get("verified")
    if verified is None:
        checks = verification.get("checks") or {}
        verified = raw.get("status") in {"published_verified", "Respondido"} or (bool(checks) and all(checks.values()))
    return {
        "source_file": source_file.name,
        "source_index": index,
        "batch": batch_label,
        "comment_id": comment_id,
        "reply_id": reply_id,
        "message": message,
        "reply_created_time": created_time,
        "status": raw.get("status"),
        "verified": bool(verified),
    }


def batch_from_filename(path):
    stem = path.stem
    if "Batch_" in stem:
        return stem.split("Batch_")[-1]
    if "Batch" in stem:
        return stem.split("Batch")[-1].lstrip("_") or "01"
    return "initial"


# Canonical record files cover Batch 04–14. The three 2026-08-23 files cover
# the initial publication runs and are not duplicated in the record files.
paths = sorted(RESEARCH.glob("2026-08-24_Facebook_Comment_Publication_Record_Batch_*.json"))
paths += sorted(RESEARCH.glob("2026-08-23_Facebook_Comment_Publication_Batch*.json"))
raw_records = []
for path in paths:
    payload = load_json(path)
    items = payload.get("records") or payload.get("results") or []
    for index, item in enumerate(items):
        raw_records.append(record_from_raw(item, path, index, batch_from_filename(path)))

# Exclude records that do not identify both the target and the Page reply.
usable = [row for row in raw_records if row.get("comment_id") and row.get("reply_id")]
by_comment = defaultdict(list)
by_reply = defaultdict(list)
for row in usable:
    by_comment[row["comment_id"]].append(row)
    by_reply[row["reply_id"]].append(row)

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    ledger_rows = list(reader)
    ledger_fields = reader.fieldnames or []
ledger_by_comment = {row.get("Comentario_ID"): row for row in ledger_rows}
responded = {row.get("Comentario_ID"): row for row in ledger_rows if row.get("Respuesta_Estado") == "Respondido"}

duplicate_evidence_comments = {key: rows for key, rows in by_comment.items() if len(rows) > 1}
duplicate_evidence_replies = {key: rows for key, rows in by_reply.items() if len(rows) > 1}
missing_from_ledger = [row for row in usable if row["comment_id"] not in ledger_by_comment]
not_respondido = [row for row in usable if row["comment_id"] in ledger_by_comment and ledger_by_comment[row["comment_id"]].get("Respuesta_Estado") != "Respondido"]
meta_id_mismatches = [
    {"evidence": row, "ledger_meta_id": ledger_by_comment[row["comment_id"]].get("Respuesta_Meta_ID")}
    for row in usable
    if row["comment_id"] in ledger_by_comment and ledger_by_comment[row["comment_id"]].get("Respuesta_Meta_ID") != row["reply_id"]
]
ledger_responded_without_evidence = [
    row for comment_id, row in responded.items() if comment_id not in by_comment
]
field_issues = []
for row in responded.values():
    missing_fields = [field for field in ("Respuesta_Sugerida", "Aprobacion_Estado", "Respuesta_Fecha", "Respuesta_Meta_ID", "Fuente", "Privacidad") if not row.get(field)]
    wrong_fields = []
    if row.get("Aprobacion_Estado") != "Aprobada":
        wrong_fields.append("Aprobacion_Estado!=Aprobada")
    if row.get("Privacidad") != "Anonimizado":
        wrong_fields.append("Privacidad!=Anonimizado")
    if missing_fields or wrong_fields:
        field_issues.append({"comment_id": row.get("Comentario_ID"), "missing_fields": missing_fields, "wrong_fields": wrong_fields})

# Message comparison is possible for the recent evidence files and for early
# evidence that embeds the verification payload. Older minimal records are
# still reconciled by comment ID, Meta reply ID, status, and required fields.
message_mismatches = []
for row in usable:
    ledger_row = ledger_by_comment.get(row["comment_id"])
    if ledger_row and row.get("message") and ledger_row.get("Respuesta_Sugerida") != row["message"]:
        message_mismatches.append({"evidence": row, "ledger_message": ledger_row.get("Respuesta_Sugerida")})

batch_summary = []
for batch in sorted({row["batch"] for row in usable}, key=lambda value: (len(value), value)):
    rows = [row for row in usable if row["batch"] == batch]
    batch_summary.append({
        "batch": batch,
        "evidence_records": len(rows),
        "unique_comment_ids": len({row["comment_id"] for row in rows}),
        "unique_reply_ids": len({row["reply_id"] for row in rows}),
        "verified_records": sum(1 for row in rows if row["verified"]),
        "matched_respondido_rows": sum(1 for row in rows if row["comment_id"] in responded),
    })

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "title": "Facebook — reconciliación completa de comentarios respondidos",
    "purpose": "Conciliar todos los registros históricos de publicación de respuestas de Facebook con el Community Engagement Log, sin realizar escrituras en Meta ni modificar el ledger.",
    "status": "Review",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Community_Engagement_Log.md",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
        "GrowthOS/00_01_Changelog_GrowthOS.md",
    ],
    "organization": "Operations/Research",
    "source": "Publication record JSONs stored in Operations/Research",
    "ledger_fields": len(ledger_fields),
    "ledger_rows": len(ledger_rows),
    "ledger_unique_comment_ids": len(ledger_by_comment),
    "ledger_respondido_rows": len(responded),
    "evidence_files": [path.name for path in paths],
    "evidence_records_raw": len(raw_records),
    "evidence_records_usable": len(usable),
    "evidence_unique_comment_ids": len(by_comment),
    "evidence_unique_reply_ids": len(by_reply),
    "verified_evidence_records": sum(1 for row in usable if row["verified"]),
    "duplicate_evidence_comment_ids": len(duplicate_evidence_comments),
    "duplicate_evidence_reply_ids": len(duplicate_evidence_replies),
    "missing_from_ledger_count": len(missing_from_ledger),
    "not_respondido_count": len(not_respondido),
    "meta_id_mismatch_count": len(meta_id_mismatches),
    "ledger_responded_without_evidence_count": len(ledger_responded_without_evidence),
    "required_field_issue_count": len(field_issues),
    "message_mismatch_count": len(message_mismatches),
    "status_counts": dict(Counter(row.get("Respuesta_Estado", "") for row in ledger_rows)),
    "batch_summary": batch_summary,
    "mismatches": {
        "missing_from_ledger": missing_from_ledger,
        "not_respondido": not_respondido,
        "meta_id_mismatches": meta_id_mismatches,
        "ledger_responded_without_evidence": ledger_responded_without_evidence,
        "required_field_issues": field_issues,
        "message_mismatches": message_mismatches,
    },
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "ledger_rows": payload["ledger_rows"],
    "ledger_respondido_rows": payload["ledger_respondido_rows"],
    "evidence_records_raw": payload["evidence_records_raw"],
    "evidence_records_usable": payload["evidence_records_usable"],
    "evidence_unique_comment_ids": payload["evidence_unique_comment_ids"],
    "evidence_unique_reply_ids": payload["evidence_unique_reply_ids"],
    "verified_evidence_records": payload["verified_evidence_records"],
    "duplicate_evidence_comment_ids": payload["duplicate_evidence_comment_ids"],
    "duplicate_evidence_reply_ids": payload["duplicate_evidence_reply_ids"],
    "missing_from_ledger_count": payload["missing_from_ledger_count"],
    "not_respondido_count": payload["not_respondido_count"],
    "meta_id_mismatch_count": payload["meta_id_mismatch_count"],
    "ledger_responded_without_evidence_count": payload["ledger_responded_without_evidence_count"],
    "required_field_issue_count": payload["required_field_issue_count"],
    "message_mismatch_count": payload["message_mismatch_count"],
}, ensure_ascii=False))
