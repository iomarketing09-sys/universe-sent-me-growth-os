#!/usr/bin/env python3
"""Classify one GET-only Facebook review without retaining author metadata."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW_PATH = ROOT / "Operations/Research/2026-08-25_17-58-20_Facebook_Comment_Review_GET_Only.json"
PREVIOUS_QUEUE_PATH = ROOT / "Operations/Research/2026-08-25_Facebook_Pending_Queue_After_Five_Approved_Replies.json"
EDITORIAL_PATH = ROOT / "Operations/Research/2026-08-25_17-58-20_Facebook_Editorial_Review_GET_Only.json"
QUEUE_PATH = ROOT / "Operations/Research/2026-08-25_17-58-20_Facebook_Pending_Queue_GET_Only.json"
REPORT_PATH = ROOT / "Operations/Research/2026-08-25_17-58-20_Facebook_Comment_Review_Report.md"

SOURCE = "Meta Graph API v26.0 — revisión GET-only"
NO_ACTION_STATE = {
    "decision": "No_Requiere_Respuesta",
    "response_state": "No_Requiere_Respuesta",
    "approval_state": "No_Aplica",
    "proposed_reply": None,
    "priority": "Baja",
    "calendar_action": "Ninguna",
    "moderation_state": "No_Accion",
}

# Deliberate editorial decisions for the 20 new root comments.
ROOT_DECISIONS = {
    "122151377301072582_1276962297774135": {
        "signal": "Etiqueta_o_nombre_aislado",
        "reason": "Texto equivalente a un nombre o mención aislada; no hay intención interpretable ni solicitud a la Página.",
        "message_for_editor": "[nombre o mención aislada]",
    },
    "122151377199072582_1039680955702689": {
        "signal": "Etiqueta_o_nombre_aislado",
        "reason": "Texto fragmentario equivalente a una mención o nombre aislado; no hay intención interpretable ni solicitud a la Página.",
        "message_for_editor": "[texto fragmentario]",
    },
    "122151377109072582_1043788355242576": {
        "signal": "Reflexion_breve_sobre_el_miedo",
        "reason": "Reflexión autónoma relacionada con el reel, sin pregunta ni mención directa a Universe Sent Me.",
        "message_for_editor": "¡A mí me da miedo ya no tenerle miedo a nada!",
    },
    "122151377109072582_1522896686271901": {
        "signal": "Comentario_autonomo_de_baja_senal",
        "reason": "Comentario autónomo y abstracto, sin una solicitud inequívoca a la Página.",
        "message_for_editor": "Igual eso no me suma y ni me resta.",
    },
    "122151376539072582_1787852502561437": {
        "signal": "Juego_de_palabras_de_baja_senal",
        "reason": "Frase breve con posible juego de palabras, pero sin contexto suficiente para una respuesta específica y sin solicitud directa.",
        "message_for_editor": "Te lo pro meto.",
    },
    "122151376539072582_1957098628471175": {
        "signal": "Lenguaje_sexualizado_o_afirmacion_no_verificable",
        "reason": "Comentario sexualizado que formula una afirmación no verificable; no escalar ni competir desde la Página.",
        "message_for_editor": "[comentario sexualizado; no se reproduce]",
    },
    "122151376539072582_1416950633724431": {
        "signal": "Rechazo_breve_del_meme",
        "reason": "Rechazo breve del chiste acompañado de risa; no requiere defensa ni discusión desde la Página.",
        "message_for_editor": "Falso 😂",
    },
    "122151376539072582_1032315632920234": {
        "signal": "Reaccion_de_emoji",
        "reason": "Reacción de emoji sin una solicitud dirigida a Universe Sent Me.",
        "message_for_editor": "🙂",
    },
    "122151376539072582_1794660225032096": {
        "signal": "Reaccion_de_emoji",
        "reason": "Reacción de emoji sin una solicitud dirigida a Universe Sent Me.",
        "message_for_editor": "🥵🥵",
    },
    "122151376083072582_1858563828450701": {
        "signal": "Identificacion_con_el_meme_sin_solicitud",
        "reason": "Identificación personal con el meme y tono emocional, pero sin una petición concreta a la Página.",
        "message_for_editor": "[identificación personal con el meme]",
    },
    "122151376083072582_1751262112632205": {
        "signal": "Solicitud_ambigua_no_dirigida",
        "reason": "Expresa deseo de aprender o probar, pero no formula una solicitud inequívoca a Universe Sent Me.",
        "message_for_editor": "Deberían de enseñarme jajaja.",
    },
    "122151376083072582_2117668022157008": {
        "signal": "Experiencia_personal_sin_solicitud",
        "reason": "Comentario anecdótico sobre una experiencia personal, sin una solicitud inequívoca a la Página.",
        "message_for_editor": "[comentario anecdótico sobre experiencia personal]",
    },
    "122151376083072582_1507773138044678": {
        "signal": "Reaccion_de_emoji",
        "reason": "Reacción de emoji sin una solicitud dirigida a Universe Sent Me.",
        "message_for_editor": "🥵",
    },
    "122151376083072582_2252762218897901": {
        "signal": "Reaccion_de_emoji",
        "reason": "Reacción de emoji sin una solicitud dirigida a Universe Sent Me.",
        "message_for_editor": "😮‍💨💜",
    },
    "122151376083072582_1044932481615070": {
        "signal": "Aprobacion_breve_del_meme",
        "reason": "Aprobación breve del meme; no requiere una réplica de la Página.",
        "message_for_editor": "Amén 💝",
    },
    "122151376011072582_1633124508149465": {
        "signal": "Aprobacion_breve_del_meme",
        "reason": "Aprobación breve sin una pregunta ni solicitud dirigida a la Página.",
        "message_for_editor": "Amo.",
    },
    "122151376011072582_1382951430696782": {
        "signal": "Referencia_musical_incompleta",
        "reason": "Parece una referencia o título musical, pero no incluye artista; la regla aprobada exige título y artista para proponer respuesta.",
        "message_for_editor": "Un solo cuerpo ❤️",
    },
    "122151376011072582_1436559848285776": {
        "signal": "Referencia_musical_titulo_artista",
        "reason": "Título y artista identificables; se propone una respuesta específica y queda pendiente de aprobación de Fernando.",
        "message_for_editor": "She's gone — Steelheart.",
        "proposed_reply": "«She's Gone» de Steelheart: esa sí llega con guitarra y nostalgia a la mesa. 🎶🌙",
        "priority": "Media",
    },
    "122151376011072582_1714779139616049": {
        "signal": "Referencia_musical_titulo_artista",
        "reason": "Título y artista identificables; se propone una respuesta específica y queda pendiente de aprobación de Fernando.",
        "message_for_editor": "El amor acaba — José José.",
        "proposed_reply": "«El amor acaba» de José José: cuando el corazón pide una verdad cantada en voz alta. 🎶🌙",
        "priority": "Media",
    },
    "122151376011072582_2114188339514417": {
        "signal": "Referencia_musical_con_historia_de_duelo",
        "reason": "Título, artista y contexto afectivo identificables; la propuesta reconoce la memoria de Lukas sin inventar datos adicionales.",
        "message_for_editor": "«Cuando te acuerdes de mí» — Marco Antonio Solís; dedicado a Lukas.",
        "proposed_reply": "«Cuando te acuerdes de mí» de Marco Antonio Solís: para Lukas, una canción que se queda trotando en la memoria. 🐾🎶",
        "priority": "Media",
    },
}


def post_reference(message: str) -> str:
    if message.startswith("😵‍💫"):
        label = "Publicación de contexto breve"
    elif message.startswith("🧚‍♀️"):
        label = "Reel de Kiri"
    elif message.startswith("😈"):
        label = "Reel de Kael"
    elif message.startswith("😳"):
        label = "Reel de Maeve"
    elif message.startswith("😏"):
        label = "Meme de doble sentido"
    elif message.startswith("😌"):
        label = "Publicación de contexto breve"
    else:
        label = "Publicación de Facebook"
    return f"{label} — caption visible: `{message}`"


def base_item(row: dict) -> dict:
    return {
        "comment_id": row["comment_id"],
        "post_id": row["post_id"],
        "parent_comment_id": row.get("parent_comment_id"),
        "comment_created_time": row["comment_created_time"],
        "comment_type": row["comment_type"],
        "post_reference": post_reference(row["post_message"]),
        "source": SOURCE,
    }


def main() -> None:
    review = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))
    previous_queue = json.loads(PREVIOUS_QUEUE_PATH.read_text(encoding="utf-8"))
    rows = review["new_unanswered_not_in_ledger"]
    items = []
    for row in rows:
        item = base_item(row)
        if row["comment_type"] == "Replica_Anidada":
            decision = {
                **NO_ACTION_STATE,
                "signal": "Conversacion_lateral_en_replica",
                "reason": "Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte.",
            }
        else:
            decision = ROOT_DECISIONS.get(row["comment_id"])
            if decision is None:
                raise SystemExit(f"Missing editorial decision for root {row['comment_id']}")
            if "proposed_reply" in decision:
                decision = {
                    "decision": "Pendiente_de_aprobacion",
                    "response_state": "Pendiente_Respuesta",
                    "approval_state": "Pendiente_Fernando",
                    "proposed_reply": decision["proposed_reply"],
                    "priority": decision.get("priority", "Media"),
                    "calendar_action": "Ninguna",
                    "moderation_state": "Revisar",
                    "signal": decision["signal"],
                    "reason": decision["reason"],
                    "message_for_editor": decision["message_for_editor"],
                }
            else:
                decision = {**NO_ACTION_STATE, **decision}
        item.update(decision)
        # Do not copy author names, profile URLs, PSIDs, or full lateral-thread text.
        if "message_for_editor" not in item:
            item["message_for_editor"] = None
        items.append(item)

    proposals = [x for x in items if x["response_state"] == "Pendiente_Respuesta"]
    no_actions = [x for x in items if x["response_state"] == "No_Requiere_Respuesta"]
    no_action_reasons = Counter(x["signal"] for x in no_actions)
    post_counts = Counter(x["post_id"] for x in items)
    previous_pending = previous_queue.get("pending_comments", [])
    pending_comments = previous_pending + [
        {
            "comment_id": x["comment_id"],
            "post_id": x["post_id"],
            "comment_created_time": x["comment_created_time"],
            "comment_message": x["message_for_editor"],
            "post_reference": x["post_reference"],
            "proposed_reply": x["proposed_reply"],
            "priority": x["priority"],
            "insight": x["reason"],
            "approval_state": x["approval_state"],
        }
        for x in proposals
    ]
    closed_without_action = [
        {
            "comment_id": x["comment_id"],
            "post_id": x["post_id"],
            "parent_comment_id": x["parent_comment_id"],
            "comment_created_time": x["comment_created_time"],
            "comment_type": x["comment_type"],
            "post_reference": x["post_reference"],
            "signal": x["signal"],
            "reason": x["reason"],
        }
        for x in no_actions
    ]

    editorial = {
        "title": "Facebook Editorial Review — GET-only cut 2026-08-25 17:58 UTC",
        "purpose": "Clasificación completa del delta no registrado detectado por Meta Graph API v26.0, conservando cada ID estructural y preparando únicamente propuestas para aprobación.",
        "status": "Review",
        "created_at": review["reviewed_at"],
        "updated_at": review["reviewed_at"],
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_17-58-20_Facebook_Comment_Review_GET_Only.json",
            "Operations/Research/2026-08-25_17-58-20_Facebook_Pending_Queue_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md",
        ],
        "source": SOURCE,
        "read_only_review": True,
        "approval_required_for_publication": True,
        "review_cursor": review["cursor"],
        "new_comment_count": len(items),
        "new_root_count": sum(x["comment_type"] == "Comentario_Raiz" for x in items),
        "new_nested_reply_count": sum(x["comment_type"] == "Replica_Anidada" for x in items),
        "proposal_count": len(proposals),
        "no_action_count": len(no_actions),
        "published_from_this_review": 0,
        "api_error_count": review.get("api_error_count", 0),
        "no_action_signal_distribution": dict(sorted(no_action_reasons.items())),
        "post_distribution": dict(sorted(post_counts.items())),
        "items": items,
    }
    queue = {
        "title": "Facebook Pending Queue — GET-only cut 2026-08-25 17:58 UTC",
        "purpose": "Cola vigente de propuestas que requieren aprobación posterior de Fernando y registro de casos nuevos cerrados sin acción.",
        "status": "Review",
        "created_at": review["reviewed_at"],
        "updated_at": review["reviewed_at"],
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_17-58-20_Facebook_Comment_Review_GET_Only.json",
            "Operations/Research/2026-08-25_17-58-20_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-25_Facebook_Pending_Queue_After_Five_Approved_Replies.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": SOURCE,
        "read_only_review": True,
        "approval_required_for_publication": True,
        "review_cursor": review["cursor"],
        "current_unanswered_units_in_scope": review.get("current_unanswered_units"),
        "review_candidate_count": len(items),
        "pending_response_count": len(pending_comments),
        "pending_response_with_proposal_count": len(pending_comments),
        "new_pending_response_count": len(proposals),
        "no_action_count_in_review": len(no_actions),
        "historical_closed_without_action_count": previous_queue.get("no_action_count_in_review", 0),
        "publishable_without_new_approval": 0,
        "published_from_this_review": 0,
        "pending_comments": pending_comments,
        "closed_without_action": closed_without_action,
    }
    report_lines = [
        "# Revisión de comentarios de Facebook — corte GET-only",
        "",
        f"> **Fecha del corte:** `{review['reviewed_at']}` · **Cursor:** `{review['cursor']}` · **Fuente:** Meta Graph API v26.0",
        "",
        "## Propósito y alcance",
        "",
        "Se revisó exclusivamente la Página propia de Facebook de Universe Sent Me mediante operaciones GET. El escaneo cubrió las publicaciones propias dentro del límite operativo del auditor (hasta 20 publicaciones y hasta 100 comentarios por colección, con una profundidad de réplica anidada); no hubo navegador, otras redes ni operaciones de escritura en Meta.",
        "",
        "## Resultado",
        "",
        f"El delta no registrado contiene **{len(items)} comentarios**: **{len(proposals)} propuestas** y **{len(no_actions)} casos No_Requiere_Respuesta**. Se distinguieron **{editorial['new_root_count']} comentarios raíz** y **{editorial['new_nested_reply_count']} réplicas anidadas**. Se registraron **0 publicaciones**, **0 modificaciones** y **0 errores de API**.",
        "",
        "| Indicador | Resultado |",
        "|---|---:|",
        f"| IDs nuevos preservados | {len(items)} |",
        f"| Comentarios raíz | {editorial['new_root_count']} |",
        f"| Réplicas anidadas | {editorial['new_nested_reply_count']} |",
        f"| Propuestas pendientes de Fernando | {len(proposals)} |",
        f"| No_Requiere_Respuesta | {len(no_actions)} |",
        "| Publicado o modificado en Meta | 0 |",
        "| Errores de API | 0 |",
        "",
        "## Propuestas nuevas — Pendiente_Fernando",
        "",
        "| Referencia | Propuesta | Estado |",
        "|---|---|---|",
    ]
    for x in proposals:
        report_lines.append(f"| {x['message_for_editor']} | {x['proposed_reply']} | `Pendiente_Fernando` |")
    report_lines += [
        "",
        "Estas tres propuestas se agregan a las dos propuestas musicales que ya estaban pendientes; la cola vigente queda en **cinco propuestas**, todas sin autorización reutilizada y sin publicar.",
        "",
        "## Criterio de no acción",
        "",
        "Las réplicas anidadas se conservaron por ID, pero se dejaron sin acción por ser conversación lateral entre usuarios sin mención directa a la Página. También se dejaron sin acción las reacciones aisladas, nombres o fragmentos, referencias musicales incompletas, comentarios anecdóticos sin solicitud inequívoca y lenguaje sexualizado que no debe escalarse desde la cuenta.",
        "",
        "| Señal editorial | Casos |",
        "|---|---:|",
    ]
    for signal, count in sorted(no_action_reasons.items()):
        report_lines.append(f"| `{signal}` | {count} |")
    report_lines += [
        "",
        "## Estado de publicación y documentación",
        "",
        "No se publicó ninguna respuesta. La cola requiere una autorización explícita, posterior y específica de Fernando para cada propuesta. El ledger se actualizará con el registrador idempotente de este corte; los documentos canónicos de reglas y auditoría se actualizarán después de validar el append-only y el estado del schedule.",
        "",
        "### Documentos relacionados",
        "",
        "- [Artefacto crudo GET-only](2026-08-25_17-58-20_Facebook_Comment_Review_GET_Only.json)",
        "- [Clasificación editorial completa](2026-08-25_17-58-20_Facebook_Editorial_Review_GET_Only.json)",
        "- [Cola vigente](2026-08-25_17-58-20_Facebook_Pending_Queue_GET_Only.json)",
        "- [Ledger de engagement](2026-08-15_Community_Engagement_Log.csv)",
    ]
    EDITORIAL_PATH.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QUEUE_PATH.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(json.dumps({"editorial": str(EDITORIAL_PATH), "queue": str(QUEUE_PATH), "report": str(REPORT_PATH), "new": len(items), "proposals": len(proposals), "no_action": len(no_actions)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
