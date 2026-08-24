"""Export the Batch 14 review and engagement proposals to Markdown."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json"
REVIEW = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.md"

proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
review = json.loads(REVIEW.read_text(encoding="utf-8"))
proposals = proposal_data["proposals"]
no_action = proposal_data["no_action"]
new_rows = review["new_unanswered_not_in_ledger"]

lines = [
    "# Facebook Batch 14 — oportunidades de engagement",
    "",
    "**Propósito:** documentar el escaneo de comentarios de Facebook, reconciliar oportunidades nuevas y antiguas y preparar respuestas específicas para aprobación humana, sin publicar.",
    "**Estado:** Review  ",
    "**Fecha de creación:** 2026-08-24  ",
    f"**Última actualización:** {review['reviewed_at']}  ",
    "**Versión:** 1.0  ",
    "**Autor:** Manus AI  ",
    "**Documentos relacionados:** `2026-08-24_Facebook_Comment_Review_Batch_14.json`; `2026-08-24_Facebook_Batch14_Current_Unanswered_Inventory.json`; `2026-08-24_Facebook_Batch14_Candidate_Context.json`; `2026-08-24_Facebook_Batch14_Engagement_Proposals.json`; `2026-08-24_Facebook_Pending_Queue_After_Batch13.json`; `2026-08-15_Community_Engagement_Log.csv`  ",
    "**Organización:** Operations/Research",
    "",
    "## Resumen ejecutivo",
    "",
    f"La revisión exclusiva mediante Meta Graph API v26.0 cubrió **{review['page_posts_reviewed']} publicaciones propias**, **{review['root_comments_seen']} comentarios raíz** y **{review['comment_ids_seen']} IDs de comentarios/réplicas**. Se detectaron **{review['current_unanswered_units']} unidades actuales sin respuesta directa**, pero **69 ya tenían clasificación histórica** y no se reabrieron. Las **37 unidades nuevas o Sin_Revisar** recibieron una decisión editorial: **{len(proposals)} propuestas** quedan `Pendiente_Fernando` y **{len(no_action)}** quedan `No_Requiere_Respuesta`.",
    "",
    f"Después del cursor del Batch 13 (`{review['cursor']}`) apareció **un comentario nuevo**. Es una réplica dirigida a otra persona dentro de una conversación usuario-a-usuario, así que no se propone intervenir. No hubo errores de API y no se publicó nada.",
    "",
    "| Indicador | Resultado |",
    "|---|---:|",
    f"| Publicaciones propias revisadas | {review['page_posts_reviewed']} |",
    f"| Comentarios raíz | {review['root_comments_seen']} |",
    f"| IDs de comentarios/réplicas | {review['comment_ids_seen']} |",
    f"| Unidades actuales sin respuesta directa | {review['current_unanswered_units']} |",
    f"| Unidades nuevas desde Batch 13 | {review['new_units_since_batch13_cursor']} |",
    f"| Unidades nuevas no registradas desde Batch 13 | {review['new_unanswered_not_in_ledger_since_batch13_cursor']} |",
    f"| Unidades nuevas o Sin_Revisar clasificadas ahora | {len(proposals) + len(no_action)} |",
    f"| Propuestas pendientes de aprobación | {len(proposals)} |",
    f"| Casos sin acción | {len(no_action)} |",
    f"| Errores de API | {review['api_error_count']} |",
    "",
    "## Propuestas pendientes de aprobación",
    "",
    "Estas 13 respuestas son propuestas, no publicaciones. Requieren aprobación explícita de Fernando antes de cualquier escritura en Facebook.",
    "",
    "| # | Referencia del comentario | Comentario | Propuesta | Prioridad | Motivo editorial |",
    "|---:|---|---|---|---|---|",
]
for index, item in enumerate(proposals, start=1):
    comment = item.get("comment_message", "").replace("\n", " ").replace("|", "\\|").strip()
    reason = item.get("insight", "").replace("|", "\\|")
    reply = item["suggested_reply"].replace("|", "\\|")
    reference = item["reference"].replace("|", "\\|")
    lines.append(f"| {index} | {reference} (`{item['comment_id']}`) | {comment} | {reply} | {item['priority']} | {reason} |")

lines.extend([
    "",
    "## Único hallazgo posterior al Batch 13",
    "",
    "| Comentario | Publicación | Lectura editorial | Decisión |",
    "|---|---|---|---|",
])
for item in new_rows:
    comment = item.get("comment_message", "").replace("|", "\\|").replace("\n", " ")
    lines.append(f"| {comment} (`{item['comment_id']}`) | `{item['post_id']}` | Réplica dentro de conversación usuario-a-usuario; no dirigida a la Página. | `No_Requiere_Respuesta` |")

lines.extend([
    "",
    "## Casos revisados sin acción",
    "",
    "Los siguientes 24 casos se conservaron como `No_Requiere_Respuesta`. Se excluyen por ser réplicas entre usuarios, nombres o etiquetas aisladas, reacciones breves, baja señal o debates sensibles sin petición dirigida a la Página.",
    "",
    "| # | Tipo de señal | Referencia | Estado | Motivo |",
    "|---:|---|---|---|---|",
])
for index, item in enumerate(no_action, start=1):
    reason = item.get("reason", "").replace("|", "\\|")
    reference = item.get("reference", "").replace("|", "\\|")
    lines.append(f"| {index} | {item['signal']} | {reference} (`{item['comment_id']}`) | `No_Requiere_Respuesta` | {reason} |")

lines.extend([
    "",
    "## Criterio de tono USM",
    "",
    "Las propuestas musicales responden al título, artista o carga emocional concreta de cada comentario. Las respuestas de doble sentido se mantienen cómplices y no gráficas; no compiten con el contenido explícito ni añaden instrucciones. Las réplicas entre usuarios no se interrumpen por defecto, incluso cuando contienen material que podría permitir un remate, porque la prioridad es no convertir a la Página en árbitro de conversaciones ajenas.",
    "",
    "## Estado operativo",
    "",
    "No se ejecutaron POST, ocultamientos, eliminaciones ni otras escrituras en Facebook. El Batch 14 queda preparado para revisión humana. Si Fernando aprueba un subconjunto, deberá publicarse con preconsulta anti-duplicado, verificación posterior de autoría, texto exacto, relación parent y `is_hidden=false`.",
    "",
    "## Limitación del corte",
    "",
    "El escaneo revisó las 20 publicaciones propias más recientes disponibles y una profundidad de réplicas. El conteo de 106 unidades sin respuesta directa no equivale a 106 oportunidades de engagement: incluye conversaciones antiguas, réplicas entre usuarios y casos ya clasificados. La propuesta de este Batch 14 no pretende ser una nueva auditoría histórica completa fuera de ese alcance.",
    "",
    "## Referencias",
    "",
    "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions \"Meta for Developers — Comments and @mentions\"",
    "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/ \"Meta for Developers — Graph API Comment reference\"",
])

OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"proposals": len(proposals), "no_action": len(no_action), "new_since_batch13": len(new_rows)}, ensure_ascii=False))
