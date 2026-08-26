#!/usr/bin/env python3
"""Record the 2026-08-26 18:15 UTC Facebook GET-only review."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
RAW = RESEARCH / "2026-08-26_18-15-41_Facebook_Comment_Review_GET_Only.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
EDITORIAL = RESEARCH / "2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json"
REPORT = RESEARCH / "2026-08-26_18-15-41_Facebook_Comment_Review_Report.md"
QUEUE_OUT = RESEARCH / "2026-08-26_18-15-41_Facebook_Pending_Queue_GET_Only.json"
QUEUE_IN = RESEARCH / "2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json"
REVIEWED_AT = "2026-08-26T18:15:41+00:00"
PAGE_ID = "1036844829507460"

PROPOSAL_ID = "122151377553072582_1857148135657699"
PROPOSAL_REPLY = "Wilfred ya tomó nota: un guiño y un toque de canela. 🌲😂"
PROPOSAL_REASON = "Sugerencia creativa dirigida al personaje Wilfred; permite responder con un remate específico sin intervenir en una conversación lateral."

REASONS = {
    "122151377829072582_28383172787961275": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151377829072582_1825215598636287": ("Comentario sin texto accesible; no hay contenido interpretable para responder.", "empty"),
    "122151377733072582_1844462750268067": ("Comentario sin texto accesible; no hay contenido interpretable para responder.", "empty"),
    "122151377649072582_2511249876017099": ("Reacción breve y ambigua al meme, sin pregunta ni solicitud dirigida a la Página.", "low_signal"),
    "122151377649072582_2227921178135227": ("Reacción breve y ambigua al meme, sin pregunta ni solicitud dirigida a la Página.", "low_signal"),
    "122151377553072582_2082749602339096": ("Comentario sin texto accesible; no hay contenido interpretable para responder.", "empty"),
    "122151377385072582_1381340473484974": ("Nombre o etiqueta aislada; no es una solicitud dirigida a Universe Sent Me.", "mention_or_name"),
    "122151377301072582_1868276244144629": ("Nombre o etiqueta aislada; no es una solicitud dirigida a Universe Sent Me.", "mention_or_name"),
    "122151377301072582_2057068651589277": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151377301072582_4610302405963159": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151377301072582_2196303134278820": ("Referencia o etiqueta aislada sin solicitud inequívoca para la Página.", "mention_or_name"),
    "122151377109072582_1103053779073759": ("Reacción breve de baja señal, sin pregunta ni solicitud dirigida a la Página.", "low_signal"),
    "122151377109072582_28380292711566338": ("Reacción breve de baja señal, sin pregunta ni solicitud dirigida a la Página.", "low_signal"),
    "122151376539072582_1698756234550097": ("Conversación lateral entre usuarios; además contiene una corrección personal que la Página no debe arbitrar.", "lateral_conversation"),
    "122151376539072582_1046777111597787": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151376539072582_1011631161908869": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151376539072582_1765878984462569": ("Conversación lateral con lenguaje sexualizado; no competir ni escalar desde la Página.", "lateral_conversation"),
    "122151376539072582_1052637797681413": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151376539072582_4526764267583952": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151376539072582_1435118931792085": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151376539072582_1606238507792353": ("Lenguaje íntimo/sexualizado sin solicitud dirigida a la Página; no escalar ni competir con el comentario.", "sexualized"),
    "122151376539072582_1575231017429884": ("Lenguaje íntimo/sexualizado y reacción de baja señal; no escalar desde la Página.", "sexualized"),
    "122151376539072582_1581587120130496": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
    "122151376539072582_1677598369999299": ("Conversación lateral entre usuarios; no intervenir por defecto.", "lateral_conversation"),
}


def load_raw() -> tuple[dict, list[dict]]:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    items = raw.get("new_unanswered_not_in_ledger", [])
    if len(items) != 25:
        raise SystemExit(f"EXPECTED_25_NEW_UNANSWERED:{len(items)}")
    ids = {item.get("comment_id") for item in items}
    if PROPOSAL_ID not in ids or len(ids - {PROPOSAL_ID}) != 24 or set(REASONS) != ids - {PROPOSAL_ID}:
        raise SystemExit("UNEXPECTED_NEW_ID_SET")
    if raw.get("new_unanswered_not_in_ledger_since_latest_cursor") != 25 or raw.get("api_error_count") != 0:
        raise SystemExit("RAW_SUMMARY_MISMATCH")
    return raw, items


def privacy_safe_message(item: dict) -> str:
    if item.get("comment_id") == PROPOSAL_ID:
        return item.get("comment_message") or ""
    return "[contenido preservado en el artefacto crudo; omitido aquí por privacidad y/o conversación lateral]"


def classify(item: dict) -> dict:
    cid = item["comment_id"]
    if cid == PROPOSAL_ID:
        return {
            "comment_id": cid,
            "post_id": item.get("post_id"),
            "comment_created_time": item.get("comment_created_time"),
            "comment_type": item.get("comment_type"),
            "parent_comment_id": item.get("parent_comment_id"),
            "comment_message": privacy_safe_message(item),
            "post_reference": item.get("post_message"),
            "decision": "Propuesta",
            "response_state": "Pendiente_Respuesta",
            "approval_state": "Pendiente_Fernando",
            "reason": PROPOSAL_REASON,
            "proposed_reply": PROPOSAL_REPLY,
        }
    reason, category = REASONS[cid]
    return {
        "comment_id": cid,
        "post_id": item.get("post_id"),
        "comment_created_time": item.get("comment_created_time"),
        "comment_type": item.get("comment_type"),
        "parent_comment_id": item.get("parent_comment_id"),
        "comment_message": privacy_safe_message(item),
        "post_reference": item.get("post_message"),
        "decision": "No_Requiere_Respuesta",
        "response_state": "No_Requiere_Respuesta",
        "approval_state": "No_Aplica",
        "reason": reason,
        "category": category,
        "proposed_reply": None,
    }


def main() -> None:
    raw, items = load_raw()
    decisions = [classify(item) for item in items]

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    by_id = {row.get("Comentario_ID"): row for row in rows}
    if len(by_id) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS_BEFORE_APPEND")

    for item, decision in zip(items, decisions):
        cid = item["comment_id"]
        if cid in by_id:
            raise SystemExit(f"ID_ALREADY_REGISTERED:{cid}")
        row = {field: "" for field in fields}
        if decision["decision"] == "Propuesta":
            response_state = "Pendiente_Respuesta"
            approval_state = "Pendiente_Fernando"
            suggested = PROPOSAL_REPLY
            signal = "Sugerencia_Creativa"
            priority = "Media"
            moderation = "Pendiente_Revision"
            insight = PROPOSAL_REASON
        else:
            response_state = "No_Requiere_Respuesta"
            approval_state = "No_Aplica"
            suggested = "No responder"
            signal = "No_Requiere_Respuesta"
            priority = "Baja"
            moderation = "No_Accion"
            insight = f"Clasificación GET-only: No_Requiere_Respuesta — {decision['reason']}"
        row.update({
            "Comentario_ID": cid,
            "Post_ID": item.get("post_id") or "",
            "CNT_ID": item.get("parent_comment_id") or "",
            "Fecha_Comentario": item.get("comment_created_time") or "",
            "Plataforma": "Facebook",
            "Tipo": item.get("comment_type") or "Comentario_Raiz",
            "Señal": signal,
            "Respuesta_Estado": response_state,
            "Respuesta_Sugerida": suggested,
            "Aprobacion_Estado": approval_state,
            "Respuesta_Fecha": "",
            "Respuesta_Meta_ID": "",
            "Insight_Anonimo": insight,
            "Accion_Calendario": "Revisar con Fernando" if decision["decision"] == "Propuesta" else "Ninguna",
            "Prioridad": priority,
            "Moderacion_Estado": moderation,
            "Asset_Respuesta_ID": "",
            "Privacidad": "Anonimizado",
            "Fuente": "Meta Graph API v26.0 — revisión GET-only 2026-08-26T18:15:41Z",
            "Ultima_Sincronizacion": REVIEWED_AT,
        })
        rows.append(row)
        by_id[cid] = row

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    roots = [item for item in items if item.get("comment_type") == "Comentario_Raiz"]
    replies = [item for item in items if item.get("comment_type") == "Replica_Anidada"]
    category_counts = Counter(decision.get("category", "proposal") for decision in decisions)
    proposal_decisions = [decision for decision in decisions if decision["decision"] == "Propuesta"]
    no_action_decisions = [decision for decision in decisions if decision["decision"] == "No_Requiere_Respuesta"]

    editorial = {
        "title": "Facebook Editorial Review — 2026-08-26 18:15 UTC",
        "purpose": "Clasificar todos los IDs nuevos del corte GET-only, separar raíces y réplicas y preparar solo las propuestas que requieren aprobación humana.",
        "status": "Review",
        "created_at": REVIEWED_AT,
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-26_18-15-41_Facebook_Comment_Review_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-25_18-51-09_Facebook_Pending_Queue_After_Additional_Publication.json",
            "Operations/Research/2026-08-26_18-15-41_Facebook_Comment_Review_Report.md",
        ],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "read_only": True,
        "reviewed_at": REVIEWED_AT,
        "cursor": raw.get("cursor"),
        "cursor_source": raw.get("cursor_source"),
        "page_id": PAGE_ID,
        "new_units": len(items),
        "new_root_count": len(roots),
        "new_nested_reply_count": len(replies),
        "proposal_count": len(proposal_decisions),
        "no_action_count": len(no_action_decisions),
        "api_error_count": raw.get("api_error_count"),
        "decisions_by_category": dict(category_counts),
        "queue_changed": True,
        "decisions": decisions,
    }
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prior_queue = json.loads(QUEUE_IN.read_text(encoding="utf-8"))
    pending = list(prior_queue.get("pending_comments", []))
    context_review = list(prior_queue.get("context_review", []))
    no_action = list(prior_queue.get("no_action", []))
    pending.append({
        "comment_id": PROPOSAL_ID,
        "post_id": next(item.get("post_id") for item in items if item.get("comment_id") == PROPOSAL_ID),
        "comment_created_time": next(item.get("comment_created_time") for item in items if item.get("comment_id") == PROPOSAL_ID),
        "comment_message": "Sugerencia dirigida a Wilfred para un guiño y un toque de canela.",
        "post_reference": "Wilfred sabe. 🌲 #UniverseSentMe",
        "candidate_reply": PROPOSAL_REPLY,
        "decision": "Propuesta",
        "approval_status": "Pendiente_Fernando",
        "publication_status": "No_Publicar_Sin_Autorizacion_Posterior",
        "reason": PROPOSAL_REASON,
    })
    for decision in no_action_decisions:
        no_action.append({
            "comment_id": decision["comment_id"],
            "post_id": decision.get("post_id"),
            "comment_created_time": decision.get("comment_created_time"),
            "comment_message": decision["comment_message"],
            "post_reference": decision.get("post_reference"),
            "decision": "No_Requiere_Respuesta",
            "reason": decision["reason"],
        })
    queue = {
        "title": "Facebook Pending Queue — after 2026-08-26 GET-only review",
        "purpose": "Cola vigente posterior al corte GET-only de comentarios recientes; solo contiene propuestas que requieren aprobación humana y conserva casos de contexto/no acción.",
        "status": "Active",
        "created_at": prior_queue.get("created_at"),
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-26_18-15-41_Facebook_Comment_Review_GET_Only.json",
            "Operations/Research/2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-26_18-15-41_Facebook_Comment_Review_Report.md",
        ],
        "source": "Meta Graph API v26.0 GET-only review",
        "published_additional_count": prior_queue.get("published_additional_count"),
        "verified_additional_count": prior_queue.get("verified_additional_count"),
        "pending_response_count": len(pending),
        "pending_approval_count": len(pending),
        "context_review_count": len(context_review),
        "no_action_count": len(no_action),
        "published_from_this_review": 0,
        "pending_comments": pending,
        "context_review": context_review,
        "no_action": no_action,
    }
    QUEUE_OUT.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = [
        "---",
        'title: "Facebook Comment Review Report — 2026-08-26 18:15 UTC"',
        'purpose: "Reporte compacto de la revisión GET-only de comentarios recientes de Universe Sent Me."',
        "status: Review",
        "created: 2026-08-26",
        "updated: 2026-08-26",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-26_18-15-41_Facebook_Comment_Review_GET_Only.json",
        "  - Operations/Research/2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json",
        "  - Operations/Research/2026-08-26_18-15-41_Facebook_Pending_Queue_GET_Only.json",
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
        f"| IDs nuevos sin respuesta y no registrados | **{raw.get('new_unanswered_not_in_ledger_since_latest_cursor')}** |",
        f"| Comentarios raíz nuevos | **{len(roots)}** |",
        f"| Réplicas anidadas nuevas | **{len(replies)}** |",
        "| Propuestas nuevas | **1** |",
        "| No requiere respuesta | **24** |",
        f"| Errores API | **{raw.get('api_error_count')}** |",
        "| Publicaciones / modificaciones Meta | **0** |",
        "",
        "## Propuesta para aprobación de Fernando",
        "",
        "| Referencia | Comentario | Respuesta propuesta | Estado |",
        "|---|---|---|---|",
        f"| Wilfred sabe. 🌲 | Sugerencia para que Wilfred guiñe y lleve un toque de canela. | {PROPOSAL_REPLY} | `Pendiente_Fernando` |",
        "",
        "## No requiere respuesta",
        "",
        "Los 24 casos restantes se clasificaron sin acción: **12 conversaciones laterales entre usuarios**, **3 comentarios sin texto**, **3 etiquetas o referencias aisladas**, **4 reacciones/comentarios de baja señal** y **2 comentarios raíz con lenguaje íntimo o sexualizado**. Los IDs y la relación raíz/réplica están completos en el artefacto editorial y en el artefacto crudo; los nombres y datos personales de autores no se incorporaron al reporte.",
        "",
        "## Conclusión operativa",
        "",
        "La cola cambia únicamente para añadir una propuesta nueva en `Pendiente_Fernando`. Los dos casos de contexto existentes permanecen intactos. No se reutilizaron aprobaciones previas y no se publicó ninguna respuesta.",
        "",
        "## Límites y referencias",
        "",
        "El corte cubre las 20 publicaciones propias más recientes, la primera página de hasta 100 comentarios por colección y una profundidad de una réplica. Los IDs estructurales completos se conservan en el JSON; no se guardaron nombres, URLs de perfil ni IDs personales de autores.",
        "",
        "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
        "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
        "",
        "Fuentes técnicas: Meta Graph API v26.0 [1] [2] y el ledger anonimizado validado del proyecto.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"new_units": len(items), "roots": len(roots), "replies": len(replies), "proposals": 1, "no_action": 24, "queue_pending_after": len(pending), "ledger_rows": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
