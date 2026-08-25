#!/usr/bin/env python3
"""Record the 2026-08-25 22:11 UTC Facebook GET-only review."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
RAW = RESEARCH / "2026-08-25_22-11-14_Facebook_Comment_Review_GET_Only.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
EDITORIAL = RESEARCH / "2026-08-25_22-11-14_Facebook_Editorial_Review_GET_Only.json"
REPORT = RESEARCH / "2026-08-25_22-11-14_Facebook_Comment_Review_Report.md"
QUEUE_SNAPSHOT = RESEARCH / "2026-08-25_22-11-14_Facebook_Pending_Queue_No_Change.json"
QUEUE = RESEARCH / "2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json"
REVIEWED_AT = "2026-08-25T22:11:14+00:00"
PAGE_ID = "1036844829507460"

REASONS = {
    "122151377385072582_1753033795844005": "Reacción breve de baja señal; no contiene pregunta ni solicitud dirigida a la Página.",
    "122151377385072582_1072530798834362": "Comentario sin texto accesible; no hay contenido interpretable para responder.",
    "122151377301072582_2233461917418378": "Etiqueta/nombre con emojis; no es una solicitud dirigida a Universe Sent Me.",
    "122151377109072582_1581171727014332": "Opinión religiosa o moral sin pregunta ni petición concreta; no abrir debate desde la Página.",
    "122151376539072582_2804834033251416": "Réplica dentro de una conversación entre usuarios; no intervenir por defecto.",
    "122151376539072582_1293408720519748": "Réplica dentro de una conversación entre usuarios; no intervenir por defecto.",
    "122151376539072582_1415363663991025": "Lenguaje íntimo/sexualizado sin solicitud dirigida a la Página; no escalar ni competir con el comentario.",
}


def add_reason(existing: str, reason: str) -> str:
    marker = f"Clasificación GET-only: No_Requiere_Respuesta — {reason}"
    if marker in existing:
        return existing
    return (existing.rstrip(". ") + ". " if existing else "") + marker


def load_rows() -> list[dict]:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    rows = raw.get("new_unanswered_not_in_ledger", [])
    if len(rows) != 7:
        raise SystemExit(f"EXPECTED_SEVEN_NEW_UNANSWERED:{len(rows)}")
    ids = [row.get("comment_id") for row in rows]
    if len(set(ids)) != 7 or set(ids) != set(REASONS):
        raise SystemExit("UNEXPECTED_NEW_ID_SET")
    return rows


def main() -> None:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    rows_to_record = load_rows()
    if raw.get("new_unanswered_not_in_ledger_since_latest_cursor") != 7 or raw.get("api_error_count") != 0:
        raise SystemExit("RAW_SUMMARY_MISMATCH")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    by_id = {row.get("Comentario_ID"): row for row in rows}
    if len(by_id) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS")

    for item in rows_to_record:
        cid = item["comment_id"]
        row = by_id.get(cid)
        if row is None:
            row = {field: "" for field in fields}
            row.update({
                "Comentario_ID": cid,
                "Post_ID": item.get("post_id") or "",
                "CNT_ID": item.get("parent_comment_id") or "",
                "Fecha_Comentario": item.get("comment_created_time") or "",
                "Plataforma": "Facebook",
                "Tipo": item.get("comment_type") or "Comentario_Raiz",
                "Señal": "No_Requiere_Respuesta",
                "Respuesta_Estado": "No_Requiere_Respuesta",
                "Respuesta_Sugerida": "No responder",
                "Aprobacion_Estado": "No_Aplica",
                "Respuesta_Fecha": "",
                "Respuesta_Meta_ID": "",
                "Insight_Anonimo": f"Clasificación GET-only: No_Requiere_Respuesta — {REASONS[cid]}",
                "Accion_Calendario": "Ninguna",
                "Prioridad": "Baja",
                "Moderacion_Estado": "No_Accion",
                "Asset_Respuesta_ID": "",
                "Privacidad": "Anonimizado",
                "Fuente": "Meta Graph API v26.0 — revisión GET-only 2026-08-25T22:11:14Z",
                "Ultima_Sincronizacion": REVIEWED_AT,
            })
            rows.append(row)
            by_id[cid] = row
        else:
            if row.get("Respuesta_Estado") not in ("", "Sin_Revisar", "No_Requiere_Respuesta"):
                raise SystemExit(f"UNEXPECTED_EXISTING_RESPONSE_STATE:{cid}:{row.get('Respuesta_Estado')}")
            row.update({
                "Respuesta_Estado": "No_Requiere_Respuesta",
                "Aprobacion_Estado": "No_Aplica",
                "Respuesta_Sugerida": "No responder",
                "Respuesta_Fecha": "",
                "Respuesta_Meta_ID": "",
                "Moderacion_Estado": "No_Accion",
                "Privacidad": "Anonimizado",
                "Fuente": "Meta Graph API v26.0 — revisión GET-only 2026-08-25T22:11:14Z",
                "Ultima_Sincronizacion": REVIEWED_AT,
                "Accion_Calendario": "Ninguna",
                "Prioridad": "Baja",
                "Insight_Anonimo": add_reason(row.get("Insight_Anonimo", ""), REASONS[cid]),
            })

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    roots = [item for item in rows_to_record if item.get("comment_type") == "Comentario_Raiz"]
    replies = [item for item in rows_to_record if item.get("comment_type") == "Replica_Anidada"]
    decisions = []
    for item in rows_to_record:
        cid = item["comment_id"]
        decisions.append({
            "comment_id": cid,
            "post_id": item.get("post_id"),
            "comment_created_time": item.get("comment_created_time"),
            "comment_type": item.get("comment_type"),
            "parent_comment_id": item.get("parent_comment_id"),
            "comment_message": item.get("comment_message"),
            "post_reference": item.get("post_message"),
            "decision": "No_Requiere_Respuesta",
            "reason": REASONS[cid],
            "proposed_reply": None,
            "already_logged": item.get("already_logged"),
        })

    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    editorial = {
        "title": "Facebook Editorial Review — 2026-08-25 22:11 UTC",
        "purpose": "Clasificar todos los IDs nuevos del corte GET-only sin generar propuestas ni modificar la cola.",
        "status": "Active",
        "created_at": REVIEWED_AT,
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-25_22-11-14_Facebook_Comment_Review_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json",
            "Operations/Research/2026-08-25_22-11-14_Facebook_Comment_Review_Report.md",
        ],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "read_only": True,
        "reviewed_at": REVIEWED_AT,
        "cursor": raw.get("cursor"),
        "cursor_source": raw.get("cursor_source"),
        "page_id": PAGE_ID,
        "new_units": len(rows_to_record),
        "new_root_count": len(roots),
        "new_nested_reply_count": len(replies),
        "proposal_count": 0,
        "no_action_count": len(decisions),
        "api_error_count": raw.get("api_error_count"),
        "queue_changed": False,
        "decisions": decisions,
    }
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    queue_snapshot = {
        "title": "Facebook Pending Queue — no change after 2026-08-25 22:11 UTC review",
        "purpose": "Evidencia de que el corte produjo solo casos No_Requiere_Respuesta y no alteró la cola de publicación.",
        "status": "Unchanged",
        "created_at": REVIEWED_AT,
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-25_22-11-14_Facebook_Comment_Review_GET_Only.json",
            "Operations/Research/2026-08-25_22-11-14_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "organization": "Operations/Research",
        "source_queue": "Operations/Research/2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json",
        "source_queue_updated_at": queue.get("updated_at"),
        "pending_response_count_before": queue.get("pending_response_count"),
        "pending_response_count_after": queue.get("pending_response_count"),
        "context_review_count": queue.get("context_review_count"),
        "no_action_count": queue.get("no_action_count"),
        "new_proposal_count": 0,
        "queue_changed": False,
        "reason": "Los 7 IDs nuevos se clasificaron como No_Requiere_Respuesta; no se añadieron propuestas.",
    }
    QUEUE_SNAPSHOT.write_text(json.dumps(queue_snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report_lines = [
        "---",
        'title: "Facebook Comment Review Report — 2026-08-25 22:11 UTC"',
        'purpose: "Reporte compacto de la revisión GET-only de comentarios recientes de Universe Sent Me."',
        "status: Active",
        "created: 2026-08-25",
        "updated: 2026-08-25",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-25_22-11-14_Facebook_Comment_Review_GET_Only.json",
        "  - Operations/Research/2026-08-25_22-11-14_Facebook_Editorial_Review_GET_Only.json",
        "  - Operations/Research/2026-08-25_22-11-14_Facebook_Pending_Queue_No_Change.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Revisión reciente de comentarios de Facebook",
        "",
        f"El auditor reusable revisó exclusivamente la Página de Facebook Universe Sent Me mediante Meta Graph API v26.0. Usó como cursor el último review GET-only exitoso (`{raw.get('cursor')}`), cubrió {raw.get('page_posts_reviewed')} publicaciones propias, hasta 100 comentarios por colección y una profundidad de réplica. No se consultaron otras redes y no se ejecutaron operaciones de escritura.",
        "",
        "## Resultado",
        "",
        "| Métrica | Resultado |",
        "|---|---:|",
        f"| IDs nuevos desde el cursor | **{raw.get('new_units_since_latest_cursor')}** |",
        f"| IDs nuevos pendientes sin registrar | **{raw.get('new_unanswered_not_in_ledger_since_latest_cursor')}** |",
        f"| Comentarios raíz nuevos | **{len(roots)}** |",
        f"| Réplicas anidadas nuevas | **{len(replies)}** |",
        "| Propuestas nuevas | **0** |",
        f"| No requiere respuesta | **{len(decisions)}** |",
        f"| Errores API | **{raw.get('api_error_count')}** |",
        "| Cola de publicación | **Sin cambios** |",
        "| Publicaciones / modificaciones Meta | **0** |",
        "",
        "## Clasificación de los 7 IDs nuevos",
        "",
        "| Tipo | Comentario | Decisión | Motivo |",
        "|---|---|---|---|",
    ]
    for item in decisions:
        message = (item.get("comment_message") or "[sin texto]").replace("|", "\\|").replace("\n", "<br>")
        report_lines.append(f"| `{item['comment_type']}` | {message} | `No_Requiere_Respuesta` | {item['reason']} |")
    report_lines += [
        "",
        "## Conclusión operativa",
        "",
        "El delta contiene 7 comentarios nuevos, pero ninguno representa una oportunidad de respuesta para la Página bajo las reglas vigentes: 2 son réplicas entre usuarios, 1 es una etiqueta/nombre, 1 no tiene texto, 2 son reacciones u opiniones de baja señal y 1 contiene lenguaje íntimo/sexualizado. Por tanto, la cola no se modificó y no quedó ninguna propuesta pendiente de aprobación.",
        "",
        "## Límites y referencias",
        "",
        "El corte cubre las 20 publicaciones propias más recientes, la primera página de hasta 100 comentarios por colección y una profundidad de una réplica. Los IDs estructurales completos están preservados en el artefacto JSON; no se conservaron nombres, URLs de perfil ni IDs personales de autores.",
        "",
        "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
        "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
        "",
        "Fuentes técnicas: Meta Graph API v26.0 [1] [2] y el ledger anonimizado validado del proyecto.",
        "",
    ]
    REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    print(json.dumps({"new_units": len(rows_to_record), "roots": len(roots), "replies": len(replies), "proposals": 0, "no_action": len(decisions), "queue_changed": False, "ledger_rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
