#!/usr/bin/env python3
"""Record five verified replies and the additional editorial proposals."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
RAW = RESEARCH / "2026-08-25_17-58-20_Facebook_Comment_Review_GET_Only.json"
PUBLICATION = RESEARCH / "2026-08-25_18-19-20_Facebook_Publication.json"
PUB_RECORD = RESEARCH / "2026-08-25_18-34-06_Facebook_Publication_Record.json"
PUB_RECORD_MD = RESEARCH / "2026-08-25_18-34-06_Facebook_Publication_Record.md"
QUEUE = RESEARCH / "2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json"
FOLLOWUP = RESEARCH / "2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json"
FOLLOWUP_MD = RESEARCH / "2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.md"
SYNCED_AT = "2026-08-25T18:34:06+00:00"
PAGE_ID = "1036844829507460"

ADDITIONAL = {
    "122151377109072582_1043788355242576": ("Eso ya suena a que el miedo presentó su renuncia. 👀😂", "Reflexión con personalidad; Fernando propuso abrir un ping-pong breve."),
    "122151377109072582_1522896686271901": ("Entonces estamos ante un empate emocional. 😂", "Comentario abstracto con una oportunidad de remate corto."),
    "122151376539072582_1416950633724431": ("Objeción aceptada. 😂", "Rechazo breve con tono de invitación al ping-pong."),
    "122151376083072582_1858563828450701": ("El problema no era la técnica… era el departamento de permanencia. 😂", "Identificación con el meme y mini-historia personal; remate no gráfico."),
    "122151376083072582_1751262112632205": ("Jajaja, la clase todavía no tiene fecha de inscripción. 😂", "Solicitud ambigua con oportunidad de interacción juguetona, sin explicar el doble sentido."),
    "122151376083072582_1044932481615070": ("Amén recibido. El universo toma nota. 😌✨", "Aprobación breve que Fernando considera apta para un remate cómplice."),
    "122151376011072582_1633124508149465": ("Y nosotros encantados de que lo ames. 😌✨", "Aprobación breve con oportunidad de reciprocidad de marca."),
    "122151376011072582_1382951430696782": ("Esa tiene pinta de ir directo a la playlist. ❤️🎶", "Referencia musical incompleta, pero con una respuesta que abre una segunda interacción."),
}
CONTEXT = {
    "122151376539072582_1787852502561437": ("Promesa recibida. Ahora falta ver si se cumple. 😂", "Revisar primero el contexto visual/copy del Reel de Maeve; no publicar ni convertir en propuesta hasta confirmar el juego de palabras."),
    "122151376083072582_2117668022157008": ("Jajaja, cada quien tiene su propia teoría. 🫢😂", "Revisar qué significa exactamente la referencia antes de responder; no inventar contexto."),
}
NO_ACTION = {
    "122151376539072582_1957098628471175": "Lenguaje sexualizado; no escalar ni competir desde la Página.",
    "122151376539072582_1032315632920234": "Reacción aislada sin conversación que abrir.",
    "122151376539072582_1794660225032096": "Reacción aislada sin conversación que abrir.",
    "122151376083072582_1507773138044678": "Reacción aislada sin conversación que abrir.",
    "122151376083072582_2252762218897901": "Reacción aislada sin conversación que abrir.",
}


def add_marker(existing: str, marker: str) -> str:
    if marker in existing:
        return existing
    return (existing.rstrip(". ") + ". " if existing else "") + marker


def load_raw() -> dict[str, dict]:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    return {item["comment_id"]: item for item in raw.get("new_unanswered_not_in_ledger", [])}


def main() -> None:
    publication = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    results = publication.get("results", [])
    if publication.get("requested_count") != 5 or publication.get("verified_count") != 5 or len(results) != 5:
        raise SystemExit("PUBLICATION_NOT_EXACTLY_FIVE_VERIFIED")
    if any(result.get("verified") is not True for result in results):
        raise SystemExit("UNVERIFIED_PUBLICATION_RESULT")
    raw_by_id = load_raw()
    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    by_id = {row.get("Comentario_ID"): row for row in rows}
    if len(by_id) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS")

    published_ids = []
    for result in results:
        cid = result["parent_comment_id"]
        row = by_id.get(cid)
        if row is None:
            raise SystemExit(f"PUBLISHED_PARENT_NOT_IN_LEDGER:{cid}")
        if row.get("Respuesta_Estado") == "Respondido":
            if row.get("Respuesta_Meta_ID") != result.get("reply_id"):
                raise SystemExit(f"CONFLICTING_REPLY_ID:{cid}")
        elif row.get("Respuesta_Estado") != "Pendiente_Respuesta":
            raise SystemExit(f"UNEXPECTED_PUBLICATION_STATE:{cid}:{row.get('Respuesta_Estado')}")
        marker = "Respuesta publicada y verificada mediante Meta Graph API v26.0 tras autorización explícita de Fernando."
        row.update({
            "Respuesta_Estado": "Respondido",
            "Aprobacion_Estado": "Aprobada",
            "Respuesta_Sugerida": result.get("message", ""),
            "Respuesta_Fecha": result.get("created_time", ""),
            "Respuesta_Meta_ID": result.get("reply_id", ""),
            "Insight_Anonimo": add_marker(row.get("Insight_Anonimo", ""), marker),
            "Accion_Calendario": "Ninguna",
            "Moderacion_Estado": "No_Accion",
            "Privacidad": "Anonimizado",
            "Fuente": "Meta Graph API v26.0 — publicación tras autorización de Fernando verificada",
            "Ultima_Sincronizacion": SYNCED_AT,
        })
        published_ids.append(cid)

    for cid, (reply, insight) in ADDITIONAL.items():
        row = by_id.get(cid)
        if row is None:
            raise SystemExit(f"ADDITIONAL_ID_NOT_IN_LEDGER:{cid}")
        current_reply = row.get("Respuesta_Sugerida", "")
        if row.get("Respuesta_Estado") == "Pendiente_Respuesta" and current_reply not in ("", reply):
            raise SystemExit(f"CONFLICTING_PROPOSAL:{cid}")
        row.update({
            "Respuesta_Estado": "Pendiente_Respuesta",
            "Respuesta_Sugerida": reply,
            "Aprobacion_Estado": "Pendiente_Fernando",
            "Respuesta_Fecha": "",
            "Respuesta_Meta_ID": "",
            "Insight_Anonimo": add_marker(row.get("Insight_Anonimo", ""), "Propuesta editorial de Fernando registrada desde el texto pegado; queda pendiente de aprobación."),
            "Accion_Calendario": "Ninguna",
            "Prioridad": "Media",
            "Moderacion_Estado": "Revisar",
            "Privacidad": "Anonimizado",
            "Fuente": "Fernando — propuesta editorial pegada; pendiente de aprobación",
            "Ultima_Sincronizacion": SYNCED_AT,
        })

    for cid, (reply, reason) in CONTEXT.items():
        row = by_id.get(cid)
        if row is None:
            raise SystemExit(f"CONTEXT_ID_NOT_IN_LEDGER:{cid}")
        row.update({
            "Respuesta_Estado": "No_Requiere_Respuesta",
            "Aprobacion_Estado": "No_Aplica",
            "Accion_Calendario": "Revisar_Contexto",
            "Moderacion_Estado": "Revisar",
            "Insight_Anonimo": add_marker(row.get("Insight_Anonimo", ""), "Fernando solicitó confirmar el contexto antes de considerar una respuesta candidata."),
            "Privacidad": "Anonimizado",
            "Fuente": "Fernando — propuesta editorial dependiente de contexto; no publicable",
            "Ultima_Sincronizacion": SYNCED_AT,
        })

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    def base(cid: str) -> dict:
        raw = raw_by_id[cid]
        return {
            "comment_id": cid,
            "post_id": raw.get("post_id"),
            "comment_created_time": raw.get("comment_created_time"),
            "comment_message": raw.get("comment_message"),
            "post_reference": raw.get("post_message"),
        }

    proposals = []
    for cid, (reply, insight) in ADDITIONAL.items():
        item = base(cid)
        item.update({"proposed_reply": reply, "insight": insight, "approval_state": "Pendiente_Fernando", "publication_status": "Pendiente_Aprobacion"})
        proposals.append(item)
    context_review = []
    for cid, (reply, reason) in CONTEXT.items():
        item = base(cid)
        item.update({"candidate_reply": reply, "decision": "Revisar_Contexto", "reason": reason, "publication_status": "No_Publicar_Sin_Contexto"})
        context_review.append(item)
    no_action = []
    for cid, reason in NO_ACTION.items():
        item = base(cid)
        item.update({"decision": "No_Requiere_Respuesta", "reason": reason})
        no_action.append(item)

    queue = {
        "title": "Facebook Pending Queue — after five current queue replies",
        "purpose": "Cola vigente posterior a la publicación verificable de cinco respuestas, con nuevas oportunidades pendientes de aprobación.",
        "status": "Review",
        "created_at": SYNCED_AT,
        "updated_at": SYNCED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-34-06_Facebook_Publication_Record.json",
            "Operations/Research/2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0 publication verification + Fernando pasted editorial review",
        "published_prior_queue_count": len(published_ids),
        "published_prior_queue_verified_count": len(published_ids),
        "pending_response_count": len(proposals),
        "pending_approval_count": len(proposals),
        "context_review_count": len(context_review),
        "published_from_this_review": 0,
        "pending_comments": proposals,
        "context_review": context_review,
    }
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pub_payload = {
        "title": "Facebook Comment Publication Record — current five queue replies",
        "purpose": "Registrar las cinco respuestas autorizadas por Fernando, publicadas y verificadas mediante Meta Graph API v26.0.",
        "status": "Active",
        "created_at": publication.get("created_at", SYNCED_AT),
        "updated_at": SYNCED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-19-20_Facebook_Publication_Preflight.json",
            "Operations/Research/2026-08-25_18-19-20_Facebook_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
        ],
        "source": "Meta Graph API v26.0",
        "page_id": PAGE_ID,
        "explicit_user_approval": True,
        "approval_source": "Fernando autorizó publicar las respuestas de la cola en conversación el 2026-08-25.",
        "requested_count": 5,
        "published_count": publication.get("published_count"),
        "already_published_count": publication.get("already_published_count"),
        "verified_count": publication.get("verified_count"),
        "strict_direct_parent_count": publication.get("strict_direct_parent_count"),
        "nested_target_parent_semantics_count": publication.get("nested_target_parent_semantics_count"),
        "results": results,
    }
    PUB_RECORD.write_text(json.dumps(pub_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_lines = [
        "---",
        'title: "Facebook Comment Publication Record — current five queue replies"',
        'purpose: "Evidencia normalizada de cinco respuestas de Facebook publicadas y verificadas tras autorización explícita."',
        "status: Active",
        "created: 2026-08-25",
        "updated: 2026-08-25",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-25_18-19-20_Facebook_Publication_Preflight.json",
        "  - Operations/Research/2026-08-25_18-19-20_Facebook_Publication.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "  - Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
        "organization: Operations/Research",
        "---",
        "",
        "# Publicación de las cinco respuestas de la cola",
        "",
        "Fernando autorizó explícitamente publicar las cinco respuestas actuales. El preflight GET-only encontró 0 duplicados y 0 conflictos; Meta Graph API v26.0 publicó y verificó **5/5** respuestas. Las cinco fueron respuestas directas a su comentario objetivo; no hubo réplicas anidadas en este conjunto.",
        "",
        "| Comentario ID | Respuesta Meta ID | Estado | Parent | Texto verificado |",
        "|---|---|---|---|---|",
    ]
    for result in results:
        md_lines.append(f"| `{result['parent_comment_id']}` | `{result['reply_id']}` | `{result['status']}` / verificado | `{result['parent_id_returned']}` | {result['message'].replace('|', '\\|')} |")
    md_lines += [
        "",
        "No se publicó ninguna respuesta fuera del conjunto autorizado. El ledger conserva la trazabilidad de cada `Respuesta_Meta_ID`, timestamp, estado `Respondido` y `Privacidad=Anonimizado`.",
        "",
        "## Referencias",
        "",
        "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
        "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
        "",
    ]
    PUB_RECORD_MD.write_text("\n".join(md_lines), encoding="utf-8")

    followup = {
        "title": "Facebook Additional Engagement Review — 2026-08-25 18:34 UTC",
        "purpose": "Registrar la propuesta editorial pegada por Fernando para reclasificar oportunidades de engagement sin publicar respuestas adicionales.",
        "status": "Review",
        "created_at": SYNCED_AT,
        "updated_at": SYNCED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
            "Operations/Research/2026-08-25_17-58-20_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-25_18-34-06_Facebook_Publication_Record.json",
        ],
        "source": "Fernando pasted editorial review",
        "publication_executed_for_followup": False,
        "new_proposal_count": len(proposals),
        "context_review_count": len(context_review),
        "no_action_count": len(no_action),
        "proposals": proposals,
        "context_review": context_review,
        "no_action": no_action,
    }
    FOLLOWUP.write_text(json.dumps(followup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    follow_lines = [
        "---",
        'title: "Facebook Additional Engagement Review — 2026-08-25 18:34 UTC"',
        'purpose: "Registrar la propuesta editorial de Fernando para reclasificar oportunidades sin publicar respuestas adicionales."',
        "status: Review",
        "created: 2026-08-25",
        "updated: 2026-08-25",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-25_18-34-06_Facebook_Pending_Queue_After_Current_Queue_Publication.json",
        "  - Operations/Research/2026-08-25_18-34-06_Facebook_Additional_Engagement_Review.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Propuesta editorial adicional de Facebook",
        "",
        "Después de publicar y verificar las cinco respuestas de la cola, Fernando pegó una reclasificación editorial de los comentarios restantes. Esta revisión **no autoriza publicaciones adicionales**: las ocho oportunidades se registran como `Pendiente_Fernando`, dos quedan para revisar contexto y cinco permanecen sin respuesta.",
        "",
        "## Ocho oportunidades propuestas",
        "",
        "| Comentario ID | Comentario | Respuesta propuesta | Estado |",
        "|---|---|---|---|",
    ]
    for item in proposals:
        follow_lines.append(f"| `{item['comment_id']}` | {str(item['comment_message']).replace('|', '\\|').replace(chr(10), '<br>')} | {item['proposed_reply'].replace('|', '\\|')} | `Pendiente_Fernando` |")
    follow_lines += [
        "",
        "## Dos casos para revisar contexto",
        "",
        "| Comentario ID | Comentario | Respuesta candidata | Condición |",
        "|---|---|---|---|",
    ]
    for item in context_review:
        follow_lines.append(f"| `{item['comment_id']}` | {str(item['comment_message']).replace('|', '\\|').replace(chr(10), '<br>')} | {item['candidate_reply'].replace('|', '\\|')} | {item['reason']} |")
    follow_lines += [
        "",
        "## Cinco que permanecen sin respuesta",
        "",
        "Los comentarios restantes de esta subcola son reacciones aisladas o lenguaje sexualizado que no conviene escalar desde la Página. La referencia completa y los motivos están en el JSON estructurado adjunto.",
        "",
        "## Referencias",
        "",
        "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
        "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
        "",
    ]
    FOLLOWUP_MD.write_text("\n".join(follow_lines), encoding="utf-8")

    print(json.dumps({"published": len(published_ids), "verified": publication.get("verified_count"), "new_proposals": len(proposals), "context_review": len(context_review), "no_action": len(no_action), "ledger_rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
