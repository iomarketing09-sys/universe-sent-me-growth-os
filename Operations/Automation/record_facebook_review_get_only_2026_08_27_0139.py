#!/usr/bin/env python3
"""Classify and record the 2026-08-27 01:39 UTC Facebook GET-only delta."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
REVIEW = RESEARCH / "2026-08-27_01-39-36_Facebook_Comment_Review_GET_Only.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
QUEUE_PREVIOUS = RESEARCH / "2026-08-26_18-49-09_Facebook_Pending_Queue_After_Low_Signal_Publication.json"
EDITORIAL_OUT = RESEARCH / "2026-08-27_01-39-36_Facebook_Editorial_Review_GET_Only.json"
QUEUE_OUT = RESEARCH / "2026-08-27_01-39-36_Facebook_Pending_Queue_GET_Only.json"
REPORT_OUT = RESEARCH / "2026-08-27_01-39-36_Facebook_Comment_Review_Report.md"
REVIEWED_AT = "2026-08-27T01:39:36+00:00"

DECISIONS = {
    "122151377979072582_1070301415584151": {
        "decision": "No_Requiere_Respuesta",
        "category": "Vacio",
        "reason": "Comentario raíz sin texto accesible; no hay contenido interpretable para responder.",
        "response": "No responder.",
    },
    "122151377913072582_1752145479428744": {
        "decision": "No_Requiere_Respuesta",
        "category": "Vacio",
        "reason": "Comentario raíz sin texto accesible; no hay contenido interpretable para responder.",
        "response": "No responder.",
    },
    "122151377733072582_2551031535343040": {
        "decision": "No_Requiere_Respuesta",
        "category": "Lenguaje_Sensible",
        "reason": "Lenguaje íntimo/sexualizado sin una solicitud dirigida a la Página; no escalar ni competir con el comentario.",
        "response": "No responder.",
    },
    "122151377553072582_1053616500644270": {
        "decision": "No_Requiere_Respuesta",
        "category": "Lenguaje_Sensible",
        "reason": "Remate de doble sentido con referencia a limpieza, pero sin solicitud inequívoca; no intervenir por defecto en lenguaje íntimo o ambiguo.",
        "response": "No responder.",
    },
    "122151377109072582_903939745742789": {
        "decision": "Propuesta",
        "category": "Contextual_Sustantivo",
        "reason": "Reflexión directa sobre el personaje villano y el peso de las opiniones; admite un remate específico y breve desde Kael.",
        "response": "Kael lo tiene claro: no toda opinión merece convertirse en insomnio. 😈🌙",
    },
}


def main() -> None:
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    new_items = [item for item in review.get("new_unanswered_not_in_ledger", []) if item.get("created_after_latest_cursor")]
    ids = {item.get("comment_id") for item in new_items}
    if ids != set(DECISIONS):
        raise SystemExit(f"REVIEW_ID_SET_MISMATCH:{sorted(ids)}")
    if len(new_items) != 5:
        raise SystemExit(f"EXPECTED_FIVE_NEW_ITEMS:{len(new_items)}")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    existing_ids = {row.get("Comentario_ID") for row in rows}
    if existing_ids & ids:
        raise SystemExit("TARGET_ALREADY_IN_LEDGER")
    if len(existing_ids) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS_BEFORE_APPEND")

    by_id = {item["comment_id"]: item for item in new_items}
    for cid, decision in DECISIONS.items():
        item = by_id[cid]
        rows.append({
            "Comentario_ID": cid,
            "Post_ID": item.get("post_id", ""),
            "CNT_ID": "",
            "Fecha_Comentario": item.get("comment_created_time", ""),
            "Plataforma": "Facebook",
            "Tipo": "Comentario_Raiz" if item.get("comment_type") == "Comentario_Raiz" else item.get("comment_type", "Comentario_Raiz"),
            "Señal": "Conversación_Contextual" if decision["decision"] == "Propuesta" else ("Lenguaje_Sensible" if decision["category"] == "Lenguaje_Sensible" else "Baja_señal"),
            "Respuesta_Estado": "Pendiente_Respuesta" if decision["decision"] == "Propuesta" else "No_Requiere_Respuesta",
            "Respuesta_Sugerida": decision["response"],
            "Aprobacion_Estado": "Pendiente_Fernando" if decision["decision"] == "Propuesta" else "No_Aplica",
            "Respuesta_Fecha": "",
            "Respuesta_Meta_ID": "",
            "Insight_Anonimo": decision["reason"],
            "Accion_Calendario": "Revisar con Fernando" if decision["decision"] == "Propuesta" else "Ninguna",
            "Prioridad": "Media" if decision["decision"] == "Propuesta" else "Baja",
            "Moderacion_Estado": "Revisar" if decision["decision"] == "Propuesta" else "No_Accion",
            "Asset_Respuesta_ID": "",
            "Privacidad": "Anonimizado",
            "Fuente": "Meta Graph API v26.0 — review GET-only 2026-08-27T01:39:36Z",
            "Ultima_Sincronizacion": REVIEWED_AT,
        })
    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    decisions = []
    for item in new_items:
        cid = item["comment_id"]
        d = DECISIONS[cid]
        decisions.append({
            "comment_id": cid,
            "post_id": item.get("post_id"),
            "post_created_time": item.get("post_created_time"),
            "post_message": item.get("post_message", ""),
            "comment_created_time": item.get("comment_created_time"),
            "comment_message": item.get("comment_message", ""),
            "comment_type": item.get("comment_type"),
            "parent_comment_id": item.get("parent_comment_id"),
            "decision": d["decision"],
            "category": d["category"],
            "response_state": "Pendiente_Respuesta" if d["decision"] == "Propuesta" else "No_Requiere_Respuesta",
            "approval_state": "Pendiente_Fernando" if d["decision"] == "Propuesta" else "No_Aplica",
            "reason": d["reason"],
            "proposed_reply": d["response"],
            "publication_status": "No_Publicar_Sin_Autorizacion_Posterior" if d["decision"] == "Propuesta" else "No_Publicar",
        })
    proposal_count = sum(1 for d in decisions if d["decision"] == "Propuesta")
    no_action_count = len(decisions) - proposal_count
    editorial = {
        "title": "Facebook Editorial Review — GET-only delta 2026-08-27 01:39 UTC",
        "purpose": "Clasificar los cinco IDs nuevos de la revisión Facebook GET-only, separar raíz/réplica y preparar solo las propuestas respondibles.",
        "status": "Review",
        "created_at": REVIEWED_AT,
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-27_01-39-36_Facebook_Comment_Review_GET_Only.json",
            "Operations/Research/2026-08-27_01-39-36_Facebook_Comment_Review_Report.md",
            "Operations/Research/2026-08-27_01-39-36_Facebook_Pending_Queue_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0 GET-only",
        "reviewed_at": review.get("reviewed_at"),
        "cursor": review.get("cursor"),
        "new_units": len(new_items),
        "new_roots": sum(1 for d in decisions if d["comment_type"] == "Comentario_Raiz"),
        "new_replies": sum(1 for d in decisions if d["comment_type"] != "Comentario_Raiz"),
        "proposal_count": proposal_count,
        "no_action_count": no_action_count,
        "api_error_count": review.get("api_error_count", 0),
        "publication_count": 0,
        "decisions": decisions,
    }
    EDITORIAL_OUT.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    previous = json.loads(QUEUE_PREVIOUS.read_text(encoding="utf-8"))
    context_review = previous.get("context_review", [])
    no_action = list(previous.get("no_action", []))
    pending_comments = list(previous.get("pending_comments", []))
    if pending_comments:
        raise SystemExit("EXPECTED_PREVIOUS_QUEUE_TO_HAVE_NO_PENDING_PROPOSALS")
    for item in decisions:
        if item["decision"] == "Propuesta":
            pending_comments.append({
                "comment_id": item["comment_id"],
                "post_id": item["post_id"],
                "comment_message": item["comment_message"],
                "post_reference": item["post_message"],
                "candidate_reply": item["proposed_reply"],
                "decision": "Propuesta",
                "approval_status": "Pendiente_Fernando",
                "publication_status": "No_Publicar_Sin_Autorizacion_Posterior",
                "reason": item["reason"],
            })
        else:
            no_action.append({
                "comment_id": item["comment_id"],
                "post_id": item["post_id"],
                "comment_created_time": item["comment_created_time"],
                "comment_message": item["comment_message"] if item["comment_message"] else "[comentario vacío]",
                "post_reference": item["post_message"],
                "decision": "No_Requiere_Respuesta",
                "reason": item["reason"],
            })
    queue = dict(previous)
    queue.update({
        "title": "Facebook Pending Queue — after GET-only delta 2026-08-27 01:39 UTC",
        "updated_at": REVIEWED_AT,
        "related_documents": list(dict.fromkeys((previous.get("related_documents") or []) + [
            "Operations/Research/2026-08-27_01-39-36_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-27_01-39-36_Facebook_Comment_Review_Report.md",
        ])),
        "pending_response_count": len(pending_comments),
        "pending_approval_count": len(pending_comments),
        "context_review_count": len(context_review),
        "no_action_count": len(no_action),
        "published_from_this_review": 0,
        "pending_comments": pending_comments,
        "context_review": context_review,
        "no_action": no_action,
    })
    QUEUE_OUT.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "---",
        'title: "Facebook Comment Review Report — GET-only delta 2026-08-27 01:39 UTC"',
        'purpose: "Reporte compacto de comentarios nuevos, clasificación editorial y cola pendiente de aprobación."',
        "status: Review",
        "created: 2026-08-27",
        "updated: 2026-08-27",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-27_01-39-36_Facebook_Comment_Review_GET_Only.json",
        "  - Operations/Research/2026-08-27_01-39-36_Facebook_Editorial_Review_GET_Only.json",
        "  - Operations/Research/2026-08-27_01-39-36_Facebook_Pending_Queue_GET_Only.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Revisión Facebook GET-only",
        "",
        f"Corte realizado a las `{review.get('reviewed_at')}` con cursor `{review.get('cursor')}`. Se revisaron 20 publicaciones propias. El auditor devolvió 5 unidades nuevas sin respuesta: 5 comentarios raíz y 0 réplicas. No hubo errores de API ni escrituras en Meta.",
        "",
        "| Resultado | Casos |",
        "|---|---:|",
        f"| Nuevos IDs sin respuesta | {len(new_items)} |",
        f"| Comentarios raíz | {sum(1 for d in decisions if d['comment_type'] == 'Comentario_Raiz')} |",
        f"| Réplicas | {sum(1 for d in decisions if d['comment_type'] != 'Comentario_Raiz')} |",
        f"| Propuestas | {proposal_count} |",
        f"| No requiere respuesta | {no_action_count} |",
        f"| Errores de API | {review.get('api_error_count', 0)} |",
        "| Publicaciones | 0 |",
        "",
        "## Propuesta pendiente",
        "",
        "| Comentario | Publicación | Respuesta propuesta | Estado |",
        "|---|---|---|---|",
    ]
    for item in decisions:
        if item["decision"] == "Propuesta":
            lines.append(f"| {item['comment_message']} | {item['post_message']} | {item['proposed_reply']} | `Pendiente_Fernando` |")
    lines += [
        "",
        "## No requiere respuesta",
        "",
        "Los otros cuatro comentarios fueron clasificados como `No_Requiere_Respuesta`: dos comentarios vacíos y dos casos de lenguaje íntimo o doble sentido sin solicitud dirigida a la Página. Se conservan sus IDs estructurales en el artefacto editorial y en el ledger, sin guardar datos personales de autores.",
        "",
        "## Estado operativo",
        "",
        f"La cola pasa a {len(pending_comments)} propuesta pendiente y conserva {len(context_review)} casos de contexto. No se publicó ninguna respuesta y no se reutilizaron aprobaciones previas.",
    ]
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"new_ids": len(new_items), "roots": sum(1 for d in decisions if d['comment_type'] == 'Comentario_Raiz'), "replies": sum(1 for d in decisions if d['comment_type'] != 'Comentario_Raiz'), "proposals": proposal_count, "no_action": no_action_count, "ledger_rows": len(rows), "pending_queue": len(pending_comments)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
