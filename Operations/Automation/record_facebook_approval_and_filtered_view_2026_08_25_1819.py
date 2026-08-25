#!/usr/bin/env python3
"""Record explicit approval without publishing and emit the requested filtered view."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
QUEUE = RESEARCH / "2026-08-25_17-58-20_Facebook_Pending_Queue_GET_Only.json"
EDITORIAL = RESEARCH / "2026-08-25_17-58-20_Facebook_Editorial_Review_GET_Only.json"
APPROVAL = RESEARCH / "2026-08-25_18-19-20_Facebook_Approval_and_Filtered_Review.json"

APPROVED_IDS = {
    "122151376011072582_1436559848285776",
    "122151376011072582_1714779139616049",
    "122151376011072582_2114188339514417",
}
APPROVED_AT = "2026-08-25T18:19:20+00:00"
APPROVAL_MARKER = "Fernando aprobó explícitamente esta respuesta en conversación el 2026-08-25; no se publicó en este paso."


def main() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    editorial = json.loads(EDITORIAL.read_text(encoding="utf-8"))
    pending = queue["pending_comments"]
    if len(pending) != 5:
        raise SystemExit(f"QUEUE_EXPECTED_FIVE:{len(pending)}")
    if not APPROVED_IDS.issubset({x["comment_id"] for x in pending}):
        raise SystemExit("APPROVED_IDS_NOT_IN_QUEUE")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    by_id = {row.get("Comentario_ID"): row for row in rows}
    if len(by_id) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS")

    changed = []
    for cid in sorted(APPROVED_IDS):
        row = by_id.get(cid)
        if row is None:
            raise SystemExit(f"APPROVED_ID_NOT_IN_LEDGER:{cid}")
        if row.get("Respuesta_Estado") != "Pendiente_Respuesta":
            raise SystemExit(f"UNEXPECTED_RESPONSE_STATE:{cid}:{row.get('Respuesta_Estado')}")
        if row.get("Aprobacion_Estado") not in ("Pendiente_Fernando", "Aprobada"):
            raise SystemExit(f"UNEXPECTED_APPROVAL_STATE:{cid}:{row.get('Aprobacion_Estado')}")
        if row.get("Aprobacion_Estado") != "Aprobada":
            row["Aprobacion_Estado"] = "Aprobada"
            existing = row.get("Insight_Anonimo", "").rstrip(". ")
            row["Insight_Anonimo"] = (existing + ". " if existing else "") + APPROVAL_MARKER
            row["Ultima_Sincronizacion"] = APPROVED_AT
            row["Privacidad"] = "Anonimizado"
            row["Fuente"] = "Meta Graph API v26.0 — aprobación humana registrada; pendiente de publicación"
            changed.append(cid)
        elif APPROVAL_MARKER not in row.get("Insight_Anonimo", ""):
            raise SystemExit(f"APPROVAL_MARKER_MISSING:{cid}")

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    for item in pending:
        if item["comment_id"] in APPROVED_IDS:
            item["approval_state"] = "Aprobada"
            item["publication_status"] = "Pendiente_Publicacion"
            item["approval_recorded_at"] = APPROVED_AT
            item["approved_by"] = "Fernando"
    approval_path = "Operations/Research/2026-08-25_18-19-20_Facebook_Approval_and_Filtered_Review.json"
    queue_related = list(queue["related_documents"])
    if approval_path not in queue_related:
        queue_related.append(approval_path)
    queue.update({
        "updated_at": APPROVED_AT,
        "version": "1.1",
        "approval_recorded": True,
        "approval_recorded_at": APPROVED_AT,
        "approved_pending_publication_count": 3,
        "pending_fernando_count": 2,
        "publishable_with_current_approval_count": 3,
        "published_from_this_review": 0,
        "related_documents": queue_related,
    })
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    editorial_ids = {item["comment_id"] for item in editorial["items"]}
    if not APPROVED_IDS.issubset(editorial_ids):
        raise SystemExit("APPROVED_IDS_NOT_IN_EDITORIAL")
    for item in editorial["items"]:
        if item["comment_id"] in APPROVED_IDS:
            item["decision"] = "Aprobada_Pendiente_Publicacion"
            item["approval_state"] = "Aprobada"
            item["publication_status"] = "Pendiente_Publicacion"
            item["approval_recorded_at"] = APPROVED_AT
            item["approved_by"] = "Fernando"
    editorial_related = list(editorial["related_documents"])
    if approval_path not in editorial_related:
        editorial_related.append(approval_path)
    editorial.update({
        "updated_at": APPROVED_AT,
        "approval_recorded": True,
        "approved_pending_publication_count": 3,
        "published_from_this_review": 0,
        "related_documents": editorial_related,
    })
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    filtered_roots = [
        {
            "comment_id": item["comment_id"],
            "post_id": item["post_id"],
            "comment_created_time": item["comment_created_time"],
            "comment_type": item["comment_type"],
            "post_reference": item["post_reference"],
            "comment_message": item.get("message_for_editor"),
            "signal": item["signal"],
            "reason": item["reason"],
        }
        for item in editorial["items"]
        if item["response_state"] == "No_Requiere_Respuesta"
        and item["comment_type"] == "Comentario_Raiz"
        and item["signal"] != "Etiqueta_o_nombre_aislado"
    ]
    if len(filtered_roots) != 15:
        raise SystemExit(f"FILTERED_ROOT_COUNT:{len(filtered_roots)}")
    proposals_view = [
        {
            "comment_id": item["comment_id"],
            "post_id": item["post_id"],
            "comment_created_time": item["comment_created_time"],
            "comment_message": item.get("message_for_editor"),
            "proposed_reply": item["proposed_reply"],
            "approval_state": item.get("approval_state"),
            "publication_status": item.get("publication_status", "Pendiente_Publicacion" if item["comment_id"] in APPROVED_IDS else "Pendiente_Aprobacion"),
        }
        for item in editorial["items"]
        if item["response_state"] == "Pendiente_Respuesta"
    ]
    previous_pending = [
        {
            "comment_id": x["comment_id"],
            "post_id": x["post_id"],
            "comment_created_time": x["comment_created_time"],
            "comment_message": x["comment_message"],
            "proposed_reply": x["proposed_reply"],
            "approval_state": x["approval_state"],
            "publication_status": x.get("publication_status", "Pendiente_Aprobacion"),
        }
        for x in pending
        if x["comment_id"] not in {p["comment_id"] for p in proposals_view}
    ]
    # Use queue ordering and combine historical + new proposals exactly once.
    by_proposal = {x["comment_id"]: x for x in proposals_view + previous_pending}
    all_proposals = [by_proposal[x["comment_id"]] for x in pending]
    approval_doc = {
        "title": "Facebook Approval and Filtered Review — 2026-08-25 18:19 UTC",
        "purpose": "Registrar la aprobación explícita de tres propuestas sin publicarlas y conservar la vista de comentarios No_Requiere_Respuesta excluyendo réplicas laterales y etiquetas o nombres aislados.",
        "status": "Active",
        "created_at": APPROVED_AT,
        "updated_at": APPROVED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_17-58-20_Facebook_Pending_Queue_GET_Only.json",
            "Operations/Research/2026-08-25_17-58-20_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-25_17-58-20_Facebook_Comment_Review_Report.md",
        ],
        "source": "Fernando — aprobación explícita en conversación; revisión original Meta Graph API v26.0 GET-only",
        "read_only_review": True,
        "publication_executed": False,
        "approval_recorded": True,
        "approval_recorded_at": APPROVED_AT,
        "approved_comment_ids": sorted(APPROVED_IDS),
        "approved_pending_publication_count": 3,
        "pending_approval_count": 2,
        "current_proposal_count": len(all_proposals),
        "filtered_no_action_root_count": len(filtered_roots),
        "excluded_lateral_reply_count": sum(1 for item in editorial["items"] if item["response_state"] == "No_Requiere_Respuesta" and item["comment_type"] == "Replica_Anidada"),
        "excluded_tag_or_name_count": sum(1 for item in editorial["items"] if item["response_state"] == "No_Requiere_Respuesta" and item["signal"] == "Etiqueta_o_nombre_aislado"),
        "proposals": all_proposals,
        "filtered_no_action_roots": filtered_roots,
        "publication_status": "0 published; explicit approval recorded for 3, publication not requested",
    }
    APPROVAL.write_text(json.dumps(approval_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"approved": len(APPROVED_IDS), "already_recorded": len(APPROVED_IDS) - len(changed), "published": 0, "filtered_no_action_roots": len(filtered_roots), "queue_proposals": len(all_proposals)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
