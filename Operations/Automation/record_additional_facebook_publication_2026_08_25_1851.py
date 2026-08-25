#!/usr/bin/env python3
"""Record eight verified additional Facebook replies and close their queue."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
RAW = RESEARCH / "2026-08-25_17-58-20_Facebook_Comment_Review_GET_Only.json"
PUBLICATION = RESEARCH / "2026-08-25_18-49-39_Facebook_Additional_Publication.json"
PREFLIGHT = RESEARCH / "2026-08-25_18-49-39_Facebook_Additional_Publication_Preflight.json"
PUB_RECORD = RESEARCH / "2026-08-25_18-51-09_Facebook_Additional_Publication_Record.json"
PUB_RECORD_MD = RESEARCH / "2026-08-25_18-51-09_Facebook_Additional_Publication_Record.md"
QUEUE = RESEARCH / "2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json"
FOLLOWUP = RESEARCH / "2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json"
SYNCED_AT = "2026-08-25T18:51:09+00:00"
PAGE_ID = "1036844829507460"


def add_marker(existing: str) -> str:
    marker = "Respuesta adicional publicada y verificada mediante Meta Graph API v26.0 tras autorización explícita de Fernando."
    if marker in existing:
        return existing
    return (existing.rstrip(". ") + ". " if existing else "") + marker


def main() -> None:
    publication = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    preflight = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    results = publication.get("results", [])
    if publication.get("requested_count") != 8 or publication.get("published_count") != 8 or publication.get("verified_count") != 8 or len(results) != 8:
        raise SystemExit("PUBLICATION_NOT_EXACTLY_EIGHT_VERIFIED")
    if publication.get("preflight_status") != "Preflight_Pass" or preflight.get("conflict_count") != 0:
        raise SystemExit("PREFLIGHT_NOT_PASS_OR_CONFLICT")
    if any(result.get("verified") is not True for result in results):
        raise SystemExit("UNVERIFIED_RESULT")
    result_ids = [result.get("parent_comment_id") for result in results]
    if len(set(result_ids)) != 8:
        raise SystemExit("DUPLICATE_PUBLICATION_TARGETS")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    by_id = {row.get("Comentario_ID"): row for row in rows}
    if len(by_id) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS")

    for result in results:
        cid = result["parent_comment_id"]
        row = by_id.get(cid)
        if row is None:
            raise SystemExit(f"PUBLISHED_TARGET_NOT_IN_LEDGER:{cid}")
        if row.get("Respuesta_Estado") == "Respondido":
            if row.get("Respuesta_Meta_ID") != result.get("reply_id"):
                raise SystemExit(f"CONFLICTING_EXISTING_REPLY:{cid}")
        elif row.get("Respuesta_Estado") != "Pendiente_Respuesta":
            raise SystemExit(f"UNEXPECTED_STATE:{cid}:{row.get('Respuesta_Estado')}")
        row.update({
            "Respuesta_Estado": "Respondido",
            "Aprobacion_Estado": "Aprobada",
            "Respuesta_Sugerida": result.get("message", ""),
            "Respuesta_Fecha": result.get("created_time", ""),
            "Respuesta_Meta_ID": result.get("reply_id", ""),
            "Insight_Anonimo": add_marker(row.get("Insight_Anonimo", "")),
            "Accion_Calendario": "Ninguna",
            "Moderacion_Estado": "No_Accion",
            "Privacidad": "Anonimizado",
            "Fuente": "Meta Graph API v26.0 — publicación adicional tras autorización de Fernando verificada",
            "Ultima_Sincronizacion": SYNCED_AT,
        })

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    followup = json.loads(FOLLOWUP.read_text(encoding="utf-8"))
    followup.update({
        "updated_at": SYNCED_AT,
        "publication_executed_for_followup": False,
        "published_additional_count": 8,
        "verified_additional_count": 8,
        "pending_proposal_count": 0,
        "publication_record": str(PUB_RECORD.relative_to(ROOT)),
    })
    for item in followup.get("proposals", []):
        if item["comment_id"] in result_ids:
            item.update({
                "approval_state": "Aprobada",
                "publication_status": "Respondido",
                "response_status": "Respondido",
                "publication_count": 1,
            })
    FOLLOWUP.write_text(json.dumps(followup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    queue = {
        "title": "Facebook Pending Queue — after eight additional replies",
        "purpose": "Cola vigente posterior a la publicación y verificación de las ocho propuestas adicionales aprobadas.",
        "status": "Active",
        "created_at": SYNCED_AT,
        "updated_at": SYNCED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-51-09_Facebook_Additional_Publication_Record.json",
            "Operations/Research/2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json",
            "Operations/Research/2026-08-25_18-15-08_Facebook_Additional_Engagement_Approval.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0 publication verification",
        "published_additional_count": 8,
        "verified_additional_count": 8,
        "pending_response_count": 0,
        "pending_approval_count": 0,
        "context_review_count": len(followup.get("context_review", [])),
        "no_action_count": len(followup.get("no_action", [])),
        "published_from_this_review": 8,
        "pending_comments": [],
        "context_review": followup.get("context_review", []),
        "no_action": followup.get("no_action", []),
    }
    # Correct the historical approval artifact path if it has a different timestamp.
    queue["related_documents"][2] = "Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json"
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pub_record = {
        "title": "Facebook Additional Publication Record — eight approved replies",
        "purpose": "Registrar las ocho respuestas adicionales aprobadas por Fernando, publicadas y verificadas mediante Meta Graph API v26.0.",
        "status": "Active",
        "created_at": publication.get("created_at", SYNCED_AT),
        "updated_at": SYNCED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-49-39_Facebook_Additional_Publication_Preflight.json",
            "Operations/Research/2026-08-25_18-49-39_Facebook_Additional_Publication.json",
            "Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json",
            "Operations/Research/2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "approval_source": "Fernando autorizó publicar las ocho respuestas aprobadas del lote adicional en conversación el 2026-08-25.",
        "requested_count": 8,
        "published_count": publication.get("published_count"),
        "already_published_count": publication.get("already_published_count"),
        "verified_count": publication.get("verified_count"),
        "strict_direct_parent_count": publication.get("strict_direct_parent_count"),
        "nested_target_parent_semantics_count": publication.get("nested_target_parent_semantics_count"),
        "preflight_status": preflight.get("status"),
        "results": results,
    }
    PUB_RECORD.write_text(json.dumps(pub_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "---",
        'title: "Facebook Additional Publication Record — eight approved replies"',
        'purpose: "Evidencia normalizada de ocho respuestas adicionales publicadas y verificadas tras autorización explícita."',
        "status: Active",
        "created: 2026-08-25",
        "updated: 2026-08-25",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-25_18-49-39_Facebook_Additional_Publication_Preflight.json",
        "  - Operations/Research/2026-08-25_18-49-39_Facebook_Additional_Publication.json",
        "  - Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json",
        "  - Operations/Research/2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Publicación de ocho respuestas adicionales",
        "",
        "Fernando autorizó explícitamente publicar las ocho respuestas adicionales. El preflight GET-only comprobó los ocho comentarios y sus respuestas, encontró 0 duplicados y 0 conflictos. Meta Graph API v26.0 confirmó **8/8 publicadas y verificadas**, todas con parent directo, texto exacto, autoría de la Página e `is_hidden=false`.",
        "",
        "| Comentario ID | Respuesta Meta ID | Estado | Timestamp | Texto verificado |",
        "|---|---|---|---|---|",
    ]
    for result in results:
        lines.append(f"| `{result['parent_comment_id']}` | `{result['reply_id']}` | `{result['status']}` / verificado | `{result['created_time']}` | {result['message'].replace('|', '\\|')} |")
    lines += [
        "",
        "No se publicó ninguna respuesta fuera del conjunto autorizado. Los dos casos de contexto y las cinco no acciones permanecen fuera de esta publicación.",
        "",
        "## Referencias",
        "",
        "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
        "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
        "",
    ]
    PUB_RECORD_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"published": 8, "verified": 8, "ledger_rows": len(rows), "pending_queue": 0, "context_review": len(followup.get('context_review', [])), "no_action": len(followup.get('no_action', []))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
