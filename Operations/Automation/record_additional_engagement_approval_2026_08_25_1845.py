#!/usr/bin/env python3
"""Record Fernando's explicit approval of the eight additional proposals.

No Meta write is performed by this script. It only updates the anonymized ledger
and editorial queue, and emits approval evidence for a later publication preflight.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
QUEUE = RESEARCH / "2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json"
FOLLOWUP = RESEARCH / "2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json"
APPROVAL = RESEARCH / "2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json"
APPROVAL_MD = RESEARCH / "2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.md"
APPROVAL_AT = "2026-08-25T18:45:08+00:00"
MARKER = "Fernando aprobó explícitamente esta propuesta editorial el 2026-08-25; queda pendiente de publicación."


def add_marker(existing: str) -> str:
    if MARKER in existing:
        return existing
    return (existing.rstrip(". ") + ". " if existing else "") + MARKER


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    followup = json.loads(FOLLOWUP.read_text(encoding="utf-8"))
    proposals = queue.get("pending_comments", [])
    if len(proposals) != 8:
        raise SystemExit(f"EXPECTED_EIGHT_PROPOSALS:{len(proposals)}")
    proposal_ids = [item["comment_id"] for item in proposals]
    if len(set(proposal_ids)) != 8:
        raise SystemExit("DUPLICATE_PROPOSAL_IDS")
    followup_ids = {item["comment_id"] for item in followup.get("proposals", [])}
    if set(proposal_ids) != followup_ids:
        raise SystemExit("QUEUE_FOLLOWUP_ID_SET_MISMATCH")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    by_id = {row.get("Comentario_ID"): row for row in rows}
    if len(by_id) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS")

    for item in proposals:
        cid = item["comment_id"]
        row = by_id.get(cid)
        if row is None:
            raise SystemExit(f"PROPOSAL_NOT_IN_LEDGER:{cid}")
        if row.get("Respuesta_Estado") != "Pendiente_Respuesta":
            raise SystemExit(f"UNEXPECTED_RESPONSE_STATE:{cid}:{row.get('Respuesta_Estado')}")
        if row.get("Respuesta_Meta_ID") or row.get("Respuesta_Fecha"):
            raise SystemExit(f"ALREADY_PUBLISHED_FIELDS:{cid}")
        if row.get("Respuesta_Sugerida") != item["proposed_reply"]:
            raise SystemExit(f"REPLY_TEXT_MISMATCH:{cid}")
        row.update({
            "Aprobacion_Estado": "Aprobada",
            "Insight_Anonimo": add_marker(row.get("Insight_Anonimo", "")),
            "Moderacion_Estado": "Revisar",
            "Privacidad": "Anonimizado",
            "Fuente": "Fernando — aprobación explícita de propuesta editorial; pendiente de publicación",
            "Ultima_Sincronizacion": APPROVAL_AT,
        })

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    approval_path = "Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json"
    for item in proposals:
        item.update({
            "approval_state": "Aprobada",
            "publication_status": "Pendiente_Publicacion",
            "approval_recorded_at": APPROVAL_AT,
            "approved_by": "Fernando",
        })
    related = list(queue.get("related_documents", []))
    if approval_path not in related:
        related.append(approval_path)
    queue.update({
        "updated_at": APPROVAL_AT,
        "version": "1.1",
        "approval_recorded": True,
        "approval_recorded_at": APPROVAL_AT,
        "approved_pending_publication_count": 8,
        "pending_approval_count": 0,
        "publishable_with_current_approval_count": 8,
        "published_from_this_review": 0,
        "related_documents": related,
        "pending_comments": proposals,
    })
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    follow_related = list(followup.get("related_documents", []))
    if approval_path not in follow_related:
        follow_related.append(approval_path)
    for item in followup.get("proposals", []):
        item.update({
            "approval_state": "Aprobada",
            "publication_status": "Pendiente_Publicacion",
            "approval_recorded_at": APPROVAL_AT,
            "approved_by": "Fernando",
        })
    followup.update({
        "status": "Active",
        "updated_at": APPROVAL_AT,
        "approval_recorded": True,
        "approved_pending_publication_count": 8,
        "publication_executed_for_followup": False,
        "related_documents": follow_related,
    })
    FOLLOWUP.write_text(json.dumps(followup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    approval_doc = {
        "title": "Facebook Additional Engagement Approval — 2026-08-25 18:45 UTC",
        "purpose": "Registrar la aprobación explícita de ocho propuestas editoriales adicionales, sin ejecutar publicación, y dejar separadas las revisiones de contexto.",
        "status": "Active",
        "created_at": APPROVAL_AT,
        "updated_at": APPROVAL_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json",
            "Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.md",
        ],
        "source": "Fernando — aprobación explícita en conversación",
        "approval_recorded": True,
        "approval_recorded_at": APPROVAL_AT,
        "approved_by": "Fernando",
        "approved_comment_ids": proposal_ids,
        "approved_pending_publication_count": 8,
        "pending_approval_count": 0,
        "context_review_count": len(followup.get("context_review", [])),
        "no_action_count": len(followup.get("no_action", [])),
        "publication_executed": False,
        "publication_status": "8 approved pending publication; 0 published in this step",
        "proposals": proposals,
    }
    APPROVAL.write_text(json.dumps(approval_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "---",
        'title: "Facebook Additional Engagement Approval — 2026-08-25 18:45 UTC"',
        'purpose: "Registrar la aprobación explícita de ocho propuestas editoriales adicionales sin publicar todavía."',
        "status: Active",
        "created: 2026-08-25",
        "updated: 2026-08-25",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-25_18-45-08_Facebook_Additional_Engagement_Approval.json",
        "  - Operations/Research/2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json",
        "  - Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Ocho propuestas aprobadas, pendientes de publicación",
        "",
        "Fernando aprobó explícitamente las ocho respuestas de este lote. Se registraron como `Aprobada / Pendiente_Publicacion`; no se ejecutó ninguna llamada de publicación en este paso. Los dos casos dependientes de contexto y las cinco no acciones permanecen fuera del lote.",
        "",
        "| # | Comentario | Respuesta aprobada | Estado |",
        "|---:|---|---|---|",
    ]
    for i, item in enumerate(proposals, start=1):
        comment = str(item.get("comment_message", "")).replace("|", "\\|").replace("\n", "<br>")
        reply = str(item.get("proposed_reply", "")).replace("|", "\\|")
        lines.append(f"| {i} | {comment} | {reply} | `Aprobada / Pendiente_Publicacion` |")
    lines += [
        "",
        "## Siguiente control",
        "",
        "Antes de publicar este lote se requiere un preflight GET-only actualizado por comentario, comprobación de respuestas existentes y verificación posterior de texto, autoría, visibilidad y parent. La aprobación no autoriza publicar los dos casos de contexto ni las cinco no acciones.",
        "",
        "## Referencias",
        "",
        "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
        "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
        "",
        "La fuente de la aprobación es la instrucción explícita de Fernando; la evidencia técnica de comentarios y publicación futura debe provenir de Meta Graph API v26.0 [1] [2].",
        "",
    ]
    APPROVAL_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"approved": 8, "published": 0, "context_review": len(followup.get("context_review", [])), "no_action": len(followup.get("no_action", [])), "ledger_rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
