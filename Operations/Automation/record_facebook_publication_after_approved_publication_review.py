"""Record exactly five published and verified Facebook replies.

This script does not call Meta. It consumes the publication evidence produced by
the one-shot publisher, updates the anonymized Community Engagement Log
idempotently, closes the matching editorial queue, and writes a normalized
publication record plus Markdown evidence.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
BATCH = RESEARCH / "2026-08-24_Facebook_Comment_Publication_After_Approved_Publication_Review.json"
REVIEW = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
RECORD = RESEARCH / "2026-08-24_Facebook_Comment_Publication_Record_After_Approved_Publication_Review.json"
RECORD_MD = RESEARCH / "2026-08-24_Facebook_Comment_Publication_Record_After_Approved_Publication_Review.md"
QUEUE = RESEARCH / "2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json"
EXPECTED = 5
EXPECTED_IDS = {
    "122151376539072582_1063233976446841",
    "122151376539072582_2056563468318334",
    "122151376539072582_1406586844746099",
    "122151376083072582_1036099909244517",
    "122151376083072582_1620854262795787",
}

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("requested_count") != EXPECTED or batch.get("verified_count") != EXPECTED:
    raise SystemExit(f"BATCH_NOT_EXACTLY_{EXPECTED}_VERIFIED: {batch.get('requested_count')} requested, {batch.get('verified_count')} verified")
if len(batch.get("results", [])) != EXPECTED or any(result.get("verified") is not True for result in batch["results"]):
    raise SystemExit("UNVERIFIED_OR_MISSING_PUBLICATION_RESULT")
if {result.get("parent_comment_id") for result in batch["results"]} != EXPECTED_IDS:
    raise SystemExit("PUBLICATION_RESULT_ID_SET_MISMATCH")

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
    if row.get("Respuesta_Estado") == "Respondido":
        if row.get("Respuesta_Meta_ID") not in ("", result.get("reply_id", "")):
            raise SystemExit(f"CONFLICTING_EXISTING_REPLY_ID: {cid}")
        if row.get("Respuesta_Meta_ID") == result.get("reply_id", "") and row.get("Respuesta_Sugerida") != result.get("message", ""):
            raise SystemExit(f"CONFLICTING_EXISTING_REPLY_TEXT: {cid}")
    elif row.get("Respuesta_Estado") != "Pendiente_Respuesta" or row.get("Aprobacion_Estado") != "Pendiente_Fernando":
        raise SystemExit(f"UNEXPECTED_LEDGER_STATE_FOR_APPROVED_REPLY: {cid}: {row.get('Respuesta_Estado')}/{row.get('Aprobacion_Estado')}")

    existing_insight = row.get("Insight_Anonimo", "")
    marker = "Respuesta publicada y verificada mediante Meta Graph API v26.0 tras autorización explícita de Fernando."
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
            "Fuente": "Meta Graph API v26.0 — publicación tras autorización de Fernando verificada",
            "Ultima_Sincronizacion": recorded_at,
        }
    )

    prior_decision = review_row.get("editorial_decision")
    prior_approval = review_row.get("approval_state")
    review_row.update(
        {
            "prior_editorial_decision": prior_decision,
            "prior_approval_state": prior_approval,
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
            "post_id": result.get("post_id"),
            "post_reference": result.get("post_reference"),
            "approved_reply": result.get("message"),
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
        "publication_status": "5/5 published and verified",
        "publication_record": str(RECORD.relative_to(ROOT)),
        "published_count": EXPECTED,
        "verified_count": EXPECTED,
        "approval_required_for_future_writes": True,
    }
)
REVIEW.write_text(json.dumps(review_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state_counts = Counter(row.get("Respuesta_Estado", "") for row in rows)
queue = {
    "title": "Facebook Pending Queue After Approved Publication Review — Closed",
    "purpose": "Estado de la cola después de publicar y verificar las cinco respuestas aprobadas del corte posterior a la última publicación aprobada.",
    "status": "Active",
    "created_at": batch.get("created_at", recorded_at),
    "updated_at": recorded_at,
    "version": "1.1",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Approved_Publication_Review.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Approved_Publication_Review.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Community Engagement Log synchronized with verified Meta Graph API v26.0 publication record",
    "ledger_rows": len(rows),
    "review_candidate_count": EXPECTED,
    "facebook_pending_count": state_counts.get("Pendiente_Respuesta", 0),
    "facebook_pending_with_proposal": state_counts.get("Pendiente_Respuesta", 0),
    "published_from_approved_review": EXPECTED,
    "verified_from_approved_review": EXPECTED,
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
    "title": "Facebook Comment Publication Record — five Approved Replies After Approved Publication Review",
    "purpose": "Registrar las cinco respuestas aprobadas explícitamente por Fernando, publicadas y verificadas mediante Meta Graph API v26.0.",
    "status": "Active",
    "created_at": batch.get("created_at", recorded_at),
    "updated_at": recorded_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Approved_Publication_Review.json",
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json",
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.md",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "page_id": "1036844829507460",
    "explicit_user_approval": True,
    "approval_source": "Fernando autorizó explícitamente las cinco respuestas propuestas en conversación antes de la publicación.",
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


def md(value: object) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|").replace("\n", "<br>")

lines = [
    "---",
    'title: "Facebook Comment Publication Record After Approved Publication Review"',
    'purpose: "Evidencia normalizada de cinco respuestas de Facebook publicadas y verificadas tras autorización explícita."',
    "status: Active",
    f"created: {batch.get('created_at', recorded_at)[:10]}",
    f"updated: {recorded_at[:10]}",
    'version: "1.0"',
    'author: "Manus AI"',
    "related_documents:",
    "  - Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Approved_Publication_Review.json",
    "  - Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json",
    "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    "  - Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json",
    "organization: Operations/Research",
    "---",
    "",
    "# Registro de publicación de cinco respuestas aprobadas",
    "",
    f"Fernando autorizó explícitamente las cinco respuestas. Meta Graph API v26.0 publicó y verificó **{EXPECTED}/{EXPECTED}** respuestas a las `{recorded_at}`. Se confirmaron autoría de Page ID `1036844829507460`, texto exacto, `is_hidden=false` y relación parent. Cuatro respuestas tuvieron parent directo y una réplica anidada fue validada mediante la semántica de parent inmediato devuelta por Meta.",
    "",
    "| Control | Resultado |\n|---|---:|\n"
    f"| Respuestas solicitadas | {EXPECTED} |\n"
    f"| Publicadas nuevas | {batch.get('published_count')} |\n"
    f"| Ya existentes antes del POST | {batch.get('already_published_count')} |\n"
    f"| Verificadas | {batch.get('verified_count')} |\n"
    f"| Parent directo | {batch.get('strict_direct_parent_count')} |\n"
    f"| Réplica anidada | {batch.get('nested_target_parent_semantics_count')} |\n"
    "| Duplicados | 0 |\n"
    "| Errores de verificación | 0 |",
    "",
    "## Detalle",
    "",
    "| Comentario_ID | Respuesta_Meta_ID | Estado | Timestamp Meta | Semántica parent | Texto aprobado |\n|---|---|---|---|---|---|\n"
    + "\n".join(
        f"| `{md(r['comment_id'])}` | `{md(r['reply_id'])}` | `{r['status']}` / verificado | `{md(r['reply_created_time'])}` | `{md(r['parent_semantics'])}` | {md(r['approved_reply'])} |"
        for r in records
    ),
    "",
    "La publicación se limitó al conjunto autorizado. La cola quedó sin pendientes de respuesta de este corte y las futuras escrituras siguen requiriendo autorización explícita.",
    "",
    "## Referencias",
    "",
    "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
    "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
    "",
]
RECORD_MD.write_text("\n".join(lines), encoding="utf-8")

print(json.dumps({"updated_ledger_rows": EXPECTED, "published": batch.get("published_count"), "verified": batch.get("verified_count"), "ledger_rows": len(rows), "ledger_pending": state_counts.get("Pendiente_Respuesta", 0), "queue_pending": 0}, ensure_ascii=False))
