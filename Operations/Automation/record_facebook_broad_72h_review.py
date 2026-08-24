"""Classify and record a broad 72-hour Facebook audit without publishing."""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
JSON_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Broad_72h_Reply_Proposals.json"
MD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Broad_72h_Reply_Proposals.md"
RECORD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Broad_72h_Review_Record.json"

PROPOSALS = {
    "122151376083072582_936442526178550": {
        "reply": "Ahí está: no era el producto, era la atención. 😂🔋",
        "reason": "Retoma literalmente la oposición producto/atención del comentario y la convierte en un remate breve.",
    },
    "122151376083072582_2041952303861577": {
        "reply": "Jajaja, ahí ya se necesita un plan de salida. 😂🙈",
        "reason": "Responde al giro concreto de quedar pegados como perros sin repetir ni ampliar el contenido sexual.",
    },
}

NO_ACTION_REASONS = {
    "empty": "Comentario vacío; no existe señal textual a la que responder.",
    "replica": "Réplica de usuario o etiqueta a terceros; no interrumpir la conversación.",
    "low_signal": "Reacción demasiado breve para construir una respuesta específica.",
    "context": "Comentario con contexto insuficiente para proponer un remate que no sea genérico.",
    "user_answer": "La persona ya está respondiendo a otro usuario o aportando una aclaración; la Página no necesita interrumpir.",
}


def classify(row):
    comment_id = row["comment_id"]
    message = (row.get("comment_message") or "").strip()
    if comment_id in PROPOSALS:
        item = PROPOSALS[comment_id]
        return {"disposition": "Propuesta_Pendiente_Fernando", "suggested_reply": item["reply"], "reason": item["reason"], "signal": "Contextual_Sustantivo"}
    if not message:
        return {"disposition": "No_Accion", "suggested_reply": "", "reason": NO_ACTION_REASONS["empty"], "signal": "Baja_señal"}
    if row.get("comment_type") == "Replica_Anidada":
        return {"disposition": "No_Accion", "suggested_reply": "", "reason": NO_ACTION_REASONS["replica"], "signal": "Conversación_Usuario_Usuario"}
    if message.lower() in {"jajaja", "jjj x2", "jjj   x2", "asi sea 🤭", "muchas gracias 😂😂😂"}:
        return {"disposition": "No_Accion", "suggested_reply": "", "reason": NO_ACTION_REASONS["low_signal"], "signal": "Baja_señal"}
    if "kegel" in message.lower() or "recomendados" in message.lower():
        return {"disposition": "No_Accion", "suggested_reply": "", "reason": NO_ACTION_REASONS["user_answer"], "signal": "Conversación_Usuario_Usuario"}
    if message.lower() in {"aun así me han abandonado", "la ia recaud", "no es malo es un comodín"}:
        return {"disposition": "No_Accion", "suggested_reply": "", "reason": NO_ACTION_REASONS["context"], "signal": "Contexto_Insuficiente"}
    if "lista completa" in message.lower() or "music.youtube.com" in message.lower():
        return {"disposition": "No_Accion", "suggested_reply": "", "reason": NO_ACTION_REASONS["user_answer"], "signal": "Conversación_Usuario_Usuario"}
    return {"disposition": "No_Accion", "suggested_reply": "", "reason": NO_ACTION_REASONS["context"], "signal": "Contexto_Insuficiente"}


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
reviewed_at = audit["reviewed_at"]
new_rows = []
for raw in audit["new_unanswered_not_in_ledger"]:
    decision = classify(raw)
    safe_message = raw.get("comment_message") or ""
    if raw.get("comment_type") == "Replica_Anidada":
        safe_message = "[réplica o etiqueta; texto omitido en el informe editorial]"
    elif not safe_message:
        safe_message = "[comentario vacío]"
    item = {
        "comment_id": raw["comment_id"],
        "post_id": raw["post_id"],
        "post_message": raw.get("post_message"),
        "comment_created_time": raw.get("comment_created_time"),
        "comment_type": raw.get("comment_type"),
        "comment_excerpt": safe_message,
        **decision,
        "published": False,
    }
    new_rows.append(item)

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
for item in new_rows:
    row = by_id.get(item["comment_id"])
    if row is None:
        row = {key: "" for key in fieldnames}
        row["Comentario_ID"] = item["comment_id"]
        row["Post_ID"] = item["post_id"]
        row["CNT_ID"] = ""
        row["Fecha_Comentario"] = item["comment_created_time"] or ""
        row["Plataforma"] = "Facebook"
        row["Tipo"] = item["comment_type"] or "Comentario_Raiz"
        rows.append(row)
        by_id[item["comment_id"]] = row
    row.update({
        "Señal": item["signal"],
        "Respuesta_Estado": "Pendiente_Respuesta" if item["disposition"].startswith("Propuesta") else "No_Requiere_Respuesta",
        "Respuesta_Sugerida": item["suggested_reply"],
        "Aprobacion_Estado": "Pendiente_Fernando" if item["disposition"].startswith("Propuesta") else "No_Aplica",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": item["reason"],
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media" if item["disposition"].startswith("Propuesta") else "Baja",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — auditoría amplia 72h",
        "Ultima_Sincronizacion": reviewed_at,
    })
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

proposal_items = [item for item in new_rows if item["disposition"].startswith("Propuesta")]
no_action_items = [item for item in new_rows if item["disposition"] == "No_Accion"]
json_payload = {
    "title": "Facebook Broad 72h Reply Proposals",
    "purpose": "Clasificar los 23 hallazgos nuevos de una auditoría amplia y preparar propuestas específicas sin publicar automáticamente.",
    "status": "Review",
    "created_at": reviewed_at,
    "updated_at": reviewed_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 / rolling 72-hour window / 20 recent Page posts",
    "reviewed_at": reviewed_at,
    "audit_counts": {
        "new_unanswered_not_in_ledger": len(new_rows),
        "proposal_candidates": len(proposal_items),
        "no_action": len(no_action_items),
        "previously_logged_unanswered_within_window": audit["previously_logged_unanswered_within_window"],
        "current_unanswered_units": audit["current_unanswered_units"],
    },
    "publication_performed": False,
    "proposals": proposal_items,
    "no_action_findings": no_action_items,
    "next_step": "Esperar aprobación explícita de Fernando para los candidatos; no publicar desde este artefacto.",
}
JSON_OUT.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md_lines = [
    "# Auditoría amplia de Facebook — comentarios de las últimas 72 horas",
    "",
    "**Propósito:** clasificar comentarios nuevos sin respuesta directa, incluyendo comentarios de varias horas atrás, y preparar propuestas sin publicar.",
    "**Estado:** Review  ",
    "**Fecha de creación:** 2026-08-24  ",
    "**Última actualización:** 2026-08-24  ",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_Comment_Review_Broad_72h.json`; `2026-08-15_Community_Engagement_Log.csv`; `2026-08-15_Auditoria_Comentarios_Facebook.md`",
    "**Organización:** Operations/Research",
    "",
    "## Resultado del corte",
    "",
    f"La auditoría cubrió las 20 publicaciones propias más recientes y una ventana móvil de 72 horas, desde `{audit['cutoff']}` hasta `{reviewed_at}`. Encontró **{audit['current_unanswered_units']} unidades sin respuesta actualmente**, de las cuales **{audit['unanswered_units_within_window']}** están dentro de la ventana; **{audit['previously_logged_unanswered_within_window']}** ya estaban registradas y **{len(new_rows)}** son nuevas para el ledger. No hubo errores de API.",
    "",
    "| Métrica | Resultado |",
    "|---|---:|",
    f"| Publicaciones propias revisadas | {audit['page_posts_reviewed']} |",
    f"| Comentarios raíz observados | {audit['root_comments_seen']} |",
    f"| IDs de comentarios/réplicas observados | {audit['comment_ids_seen']} |",
    f"| Unidades sin respuesta dentro de 72 h | {audit['unanswered_units_within_window']} |",
    f"| Ya registradas previamente | {audit['previously_logged_unanswered_within_window']} |",
    f"| Hallazgos nuevos añadidos al ledger | {len(new_rows)} |",
    f"| Candidatos con propuesta específica | {len(proposal_items)} |",
    "| Respuestas publicadas en este corte | 0 |",
    "",
    "## Candidatos para la siguiente aprobación",
    "",
    "Estos candidatos tienen suficiente contexto para una respuesta específica. Ninguno fue publicado.",
    "",
    "| Comentario | Publicación | Propuesta | Estado |",
    "|---|---|---|---|",
]
for item in proposal_items:
    md_lines.append(f"| {item['comment_excerpt']} | `{item['post_id']}` / `{item['comment_created_time']}` | **{item['suggested_reply']}** | `Pendiente_Fernando` |")
md_lines.extend([
    "",
    "## Hallazgos sin acción",
    "",
    f"Los otros **{len(no_action_items)}** hallazgos nuevos quedaron como `No_Requiere_Respuesta` por ser comentarios vacíos, réplicas/etiquetas, respuestas entre usuarios, reacciones demasiado breves o comentarios sin contexto suficiente. Los 136 comentarios ya registrados dentro de la ventana siguen separados en el ledger para su revisión histórica; esta auditoría no los duplica.",
    "",
    "## Regla de publicación",
    "",
    "No se publicó ninguna respuesta. Las propuestas requieren aprobación explícita de Fernando y, si se aprueban, deberán pasar por preconsulta anti-duplicado y verificación de autoría, padre, texto exacto e `is_hidden=false`.",
    "",
    "## Referencia de fuente",
    "",
    "La evidencia cruda del corte está en `2026-08-24_Facebook_Comment_Review_Broad_72h.json`; el registro idempotente queda en `2026-08-24_Facebook_Broad_72h_Review_Record.json`.",
])
MD_OUT.write_text("\n".join(md_lines).rstrip() + "\n", encoding="utf-8")

record_payload = {
    "title": "Facebook Broad 72h Review Record",
    "purpose": "Registrar la clasificación e incorporación idempotente de los hallazgos nuevos de la auditoría amplia de 72 horas.",
    "status": "Active",
    "created_at": reviewed_at,
    "updated_at": reviewed_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h.json",
        "Operations/Research/2026-08-24_Facebook_Broad_72h_Reply_Proposals.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "reviewed_at": reviewed_at,
    "new_rows_added": len(new_rows),
    "proposal_candidates": len(proposal_items),
    "no_action_rows": len(no_action_items),
    "publication_performed": False,
    "comment_ids_added": [item["comment_id"] for item in new_rows],
}
RECORD_OUT.write_text(json.dumps(record_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"new_rows_added": len(new_rows), "proposal_candidates": len(proposal_items), "no_action_rows": len(no_action_items), "publication_performed": False}, ensure_ascii=False))
