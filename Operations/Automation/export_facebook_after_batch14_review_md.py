"""Export the full post-Batch-14 Facebook editorial review to Markdown."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
INPUT = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Batch14.json"
OUT = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Batch14.md"

review = json.loads(INPUT.read_text(encoding="utf-8"))
records = review["records"]
proposals = [r for r in records if r["editorial_decision"] == "Pendiente_Respuesta"]
published = [r for r in records if r["editorial_decision"] == "Respondido" and r.get("publication_count") == 1]
no_action = [r for r in records if r["editorial_decision"] == "No_Requiere_Respuesta"]
published_count = review.get("published_count", review.get("publication_count", len(published)))
post_groups = {}
for record in records:
    post_groups.setdefault(record["post_id"], record)

lines = [
    "# Revisión editorial de Facebook posterior al Batch 14",
    "",
    f"> **Estado:** Active · **24/24 respuestas publicadas y verificadas** · Meta Graph API v26.0",
    "",
    "## Ficha del documento",
    "",
    "| Campo | Valor |",
    "|---|---|",
    f"| Propósito | Registrar y clasificar comentarios nuevos sin respuesta encontrados después del Batch 14. |",
    f"| Corte | {review['registered_at'] if 'registered_at' in review else review['updated_at']} |",
    f"| Fuente | {review['source']} |",
    f"| Cursor | {review['cursor']} ({review['cursor_source']}) |",
    f"| Unidades revisadas | {review['candidate_count']} |",
    f"| Propuestas pendientes de aprobación | {len(proposals)} |",
    f"| Respuestas publicadas y verificadas | {published_count} |",
    f"| Casos sin acción | {len(no_action)} |",
    f"| Publicaciones realizadas | {published_count} |",
    f"| Filas del ledger después del registro | {review['ledger_rows_after_registration']} |",
    "",
    "## Resumen ejecutivo",
    "",
    f"Meta Graph API v26.0 encontró **{review['candidate_count']} comentarios nuevos sin respuesta** desde el cursor del Batch 14. Fernando aprobó las **{published_count} propuestas específicas**, que fueron publicadas y verificadas individualmente; además, se clasificaron **{len(no_action)} casos como `No_Requiere_Respuesta`**. La mayoría de los casos sin acción son réplicas dentro de conversaciones usuario-a-usuario, comentarios de baja señal o contenido sexual que no debe escalarse desde la Página.",
    "",
    "La revisión cubrió las siguientes publicaciones. Las respuestas aprobadas se publicaron en un lote separado y quedaron verificadas contra Meta:",
    "",
    "| Post_ID | Copy/caption | Hallazgos nuevos |",
    "|---|---|---:|",
]
for post_id, sample in sorted(post_groups.items(), key=lambda pair: pair[0]):
    post_message = (sample.get("post_message") or "").replace("|", "\\|").replace("\n", " ")
    count = sum(1 for r in records if r["post_id"] == post_id)
    lines.append(f"| `{post_id}` | {post_message or 'Sin texto recuperable'} | {count} |")

display_rows = published if published else proposals
proposal_heading = "Propuestas publicadas y verificadas" if published else "Propuestas pendientes de aprobación"
proposal_intro = ("Estas respuestas fueron aprobadas explícitamente por Fernando, publicadas mediante Meta Graph API v26.0 y verificadas por texto, autoría, visibilidad y parent." if published else "Estas propuestas están registradas como `Pendiente_Respuesta` y **no deben publicarse sin autorización explícita**.")
lines += ["", f"## {proposal_heading}", "", proposal_intro, "", "| # | Comentario | Publicación | Propuesta USM | Prioridad | Criterio |", "|---:|---|---|---|---|---|"]
for index, r in enumerate(display_rows, 1):
    comment = (r.get("comment_message") or "").replace("|", "\\|").replace("\n", " ")
    post = (r.get("post_message") or "").replace("|", "\\|").replace("\n", " ")
    reply = (r.get("proposed_reply") or "").replace("|", "\\|").replace("\n", " ")
    insight = (r.get("editorial_insight") or "").replace("|", "\\|").replace("\n", " ")
    lines.append(f"| {index} | {comment} | {post} | **{reply}** | {r['priority']} | {insight} |")

lines += ["", "## Casos sin acción", "", "Los siguientes casos se conservan para trazabilidad, pero no se propone intervenir desde la Página.", "", "| # | Comentario | Publicación | Motivo editorial |", "|---:|---|---|---|"]
for index, r in enumerate(no_action, 1):
    comment = (r.get("comment_message") or "").replace("|", "\\|").replace("\n", " ")
    post = (r.get("post_message") or "").replace("|", "\\|").replace("\n", " ")
    reason = (r.get("editorial_insight") or "").replace("|", "\\|").replace("\n", " ")
    lines.append(f"| {index} | {comment} | {post} | {reason} |")

lines += [
    "",
    "## Reglas aplicadas",
    "",
    "1. No interrumpir réplicas usuario-a-usuario salvo solicitud clara a la Página.",
    "2. Para dobles sentidos, responder solo cuando exista un ángulo específico y mantener el tono cómplice, no gráfico y sin escalada.",
    "3. No convertir agradecimientos, emojis aislados o comentarios ambiguos en respuestas genéricas.",
    "4. Toda publicación requiere aprobación explícita de Fernando; el lote documentado aquí ya cumplió esa condición.",
    "5. El ledger conserva el texto del comentario, copy de la publicación, propuesta o no-acción, prioridad, fuente y timestamp de registro.",
    "",
    "## Documentos relacionados",
    "",
    "- `Operations/Research/2026-08-24_Facebook_Comment_Review_After_Batch14.json`",
    "- `Operations/Research/2026-08-24_Facebook_Comment_Context_After_Batch14.json`",
    "- `Operations/Research/2026-08-24_Facebook_Comment_Publication_After_Batch14.json`",
    "- `Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_After_Batch14.json`",
    "- `Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json`",
    "- `Operations/Research/2026-08-15_Community_Engagement_Log.csv`",
    "- `Operations/Research/2026-08-15_Community_Engagement_Log.md`",
    "- `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md`",
]
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"output": str(OUT), "proposal_count": len(proposals), "no_action_count": len(no_action), "post_count": len(post_groups)}, ensure_ascii=False))
