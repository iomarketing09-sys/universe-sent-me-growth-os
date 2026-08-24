"""Reconcile the complete Facebook pending queue and register follow-up findings."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLLOWUP = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h_Followup.json"
BROAD = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
JSON_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json"
MD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.md"
RECORD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Followup_Review_Record.json"

NEW_PROPOSALS = {
    "122151376011072582_1703056380925949": {
        "reply": "“El día que volviste a la Tierra” de Carlos Sadness: una elección con nostalgia y regreso en el título. 🎶🌎",
        "reason": "Recomendación musical nueva; retoma el título y su tono de regreso sin responder con un elogio genérico.",
    },
    "122151376011072582_1720626909225543": {
        "reply": "“Unstoppable”: esa sí entra como himno para volver a ponerse de pie. 🎶🔥",
        "reason": "Recomendación musical nueva; responde al título con una lectura concreta de energía y determinación.",
    },
}


def clean_display(text):
    text = (text or "").strip().replace("\n", " ")
    if not text:
        return "[comentario vacío]"
    if ":" in text and len(text.split(":", 1)[0].split()) <= 5:
        prefix, remainder = text.split(":", 1)
        if any(char.isupper() for char in prefix):
            text = remainder.strip()
    return text


def update_ledger_row(row, item, reviewed_at):
    is_proposal = bool(item.get("suggested_reply"))
    row.update({
        "Señal": item.get("signal", "Recomendación musical" if is_proposal else "Conversación_Usuario_Usuario"),
        "Respuesta_Estado": "Pendiente_Respuesta" if is_proposal else "No_Requiere_Respuesta",
        "Respuesta_Sugerida": item.get("suggested_reply", ""),
        "Aprobacion_Estado": "Pendiente_Fernando" if is_proposal else "No_Aplica",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": item.get("reason", ""),
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media" if is_proposal else "Baja",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — auditoría amplia 72h (seguimiento)",
        "Ultima_Sincronizacion": reviewed_at,
    })

followup = json.loads(FOLLOWUP.read_text(encoding="utf-8"))
broad = json.loads(BROAD.read_text(encoding="utf-8"))
reviewed_at = followup["reviewed_at"]

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}

followup_items = []
for raw in followup.get("new_unanswered_not_in_ledger", []):
    item = {
        "comment_id": raw["comment_id"],
        "post_id": raw.get("post_id"),
        "post_message": raw.get("post_message"),
        "comment_created_time": raw.get("comment_created_time"),
        "comment_type": raw.get("comment_type"),
        "comment_excerpt": clean_display(raw.get("comment_message")),
        "signal": "Recomendación musical" if raw.get("post_message") == "😌 #UniverseSentMe" and raw.get("comment_type") == "Comentario_Raiz" else "Seguimiento_72h",
    }
    if raw["comment_id"] in NEW_PROPOSALS:
        item["suggested_reply"] = NEW_PROPOSALS[raw["comment_id"]]["reply"]
        item["reason"] = NEW_PROPOSALS[raw["comment_id"]]["reason"]
    elif raw.get("comment_type") == "Replica_Anidada":
        item["suggested_reply"] = ""
        item["reason"] = "Réplica de usuario o etiqueta; no interrumpir la conversación."
    elif not (raw.get("comment_message") or "").strip():
        item["suggested_reply"] = ""
        item["reason"] = "Comentario vacío; no existe señal textual a la que responder."
    else:
        item["suggested_reply"] = ""
        item["reason"] = "Comentario breve o de baja señal; no se fuerza un remate genérico."
    row = by_id.get(item["comment_id"])
    if row is None:
        row = {key: "" for key in fieldnames}
        row["Comentario_ID"] = item["comment_id"]
        row["Post_ID"] = item["post_id"] or ""
        row["CNT_ID"] = ""
        row["Fecha_Comentario"] = item["comment_created_time"] or ""
        row["Plataforma"] = "Facebook"
        row["Tipo"] = item["comment_type"] or "Comentario_Raiz"
        rows.append(row)
        by_id[item["comment_id"]] = row
    update_ledger_row(row, item, reviewed_at)
    followup_items.append(item)

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

# Build the complete pending queue from the broad audit plus the follow-up rows.
broad_by_id = {row["comment_id"]: row for row in broad.get("unanswered_within_window", [])}
followup_by_id = {row["comment_id"]: row for row in followup.get("new_unanswered_not_in_ledger", [])}
all_queue = []
for row in rows:
    if row.get("Respuesta_Estado") != "Pendiente_Respuesta" or not row.get("Respuesta_Sugerida"):
        continue
    audit_row = broad_by_id.get(row.get("Comentario_ID")) or followup_by_id.get(row.get("Comentario_ID"), {})
    source_comment_type = audit_row.get("comment_type") or row.get("Tipo", "")
    all_queue.append({
        "comment_id": row.get("Comentario_ID"),
        "post_id": row.get("Post_ID"),
        "post_message": audit_row.get("post_message", ""),
        "comment_created_time": row.get("Fecha_Comentario", ""),
        "comment_type": source_comment_type,
        "comment_excerpt": clean_display(audit_row.get("comment_message", "[comentario ya registrado; ver ledger]")),
        "suggested_reply": row.get("Respuesta_Sugerida", ""),
        "approval_status": row.get("Aprobacion_Estado", ""),
        "source": "Followup_72h" if row.get("Comentario_ID") in {item["comment_id"] for item in followup_items} else "Existing_Queue",
    })
all_queue.sort(key=lambda item: item.get("comment_created_time") or "", reverse=True)

music_queue = [
    item for item in all_queue
    if item.get("post_message") == "😌 #UniverseSentMe" and item.get("comment_type") == "Comentario_Raiz"
]
proposal_payload = {
    "title": "Facebook Pending Queue Reconciliation",
    "purpose": "Reconciliar la cola completa de comentarios pendientes y visibilizar propuestas musicales antiguas y nuevas.",
    "status": "Review",
    "created_at": reviewed_at,
    "updated_at": reviewed_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h_Followup.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_08.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 / 20 recent Page posts / rolling 72h plus follow-up",
    "reviewed_at": reviewed_at,
    "queue_counts": {
        "pending_proposals_existing_after_batch_08": len(all_queue) - sum(1 for item in all_queue if item["source"] == "Followup_72h"),
        "new_followup_proposals": sum(1 for item in followup_items if item.get("suggested_reply")),
        "total_pending_proposals": len(all_queue),
        "music_root_proposals": len(music_queue),
        "new_followup_findings": len(followup_items),
    },
    "publication_performed": False,
    "music_proposals": music_queue,
    "all_pending_proposals": all_queue,
    "followup_findings": followup_items,
    "next_step": "Fernando puede aprobar un subconjunto por IDs; no publicar sin autorización explícita.",
}
JSON_OUT.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = [
    "# Reconciliación de la cola pendiente de comentarios de Facebook",
    "",
    "**Propósito:** mostrar la cola completa, incluidos comentarios de varias horas atrás y recomendaciones musicales que ya estaban registradas pero no habían vuelto a aparecer como candidatos nuevos.",
    "**Estado:** Review  ",
    "**Fecha de creación:** 2026-08-24  ",
    "**Última actualización:** 2026-08-24  ",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_Comment_Review_Broad_72h.json`; `2026-08-24_Facebook_Comment_Review_Broad_72h_Followup.json`; `2026-08-24_Facebook_Comment_Publication_Batch_08.json`; `2026-08-15_Community_Engagement_Log.csv`",
    "**Organización:** Operations/Research",
    "",
    "## Qué estaba quedando fuera",
    "",
    f"El inventario anterior mostraba solo los hallazgos nuevos. Después del Batch 08, la cola completa contiene **{len(all_queue)} propuestas pendientes**, no solo los dos candidatos del último corte. De ellas, **{len(music_queue)} son recomendaciones musicales en el post `😌 #UniverseSentMe`**. Las dos nuevas del seguimiento son “El día que volviste a la tierra - Carlos Sadness” y “Unstoppable”; las demás ya estaban registradas y se vuelven a mostrar aquí.",
    "",
    "| Métrica | Resultado |",
    "|---|---:|",
    f"| Propuestas pendientes existentes | {len(all_queue) - sum(1 for item in all_queue if item['source'] == 'Followup_72h')} |",
    f"| Propuestas musicales en raíces | {len(music_queue)} |",
    f"| Hallazgos nuevos del seguimiento | {len(followup_items)} |",
    f"| Propuestas nuevas del seguimiento | {sum(1 for item in followup_items if item.get('suggested_reply'))} |",
    "| Respuestas publicadas en esta revisión | 0 |",
    "",
    "## Propuestas musicales pendientes",
    "",
    "| Comentario | Fecha | Respuesta propuesta | Estado |",
    "|---|---|---|---|",
]
for item in music_queue:
    md.append(f"| {item['comment_excerpt']} | {item['comment_created_time']} | **{item['suggested_reply']}** | `Pendiente_Fernando` |")
md.extend([
    "",
    "## Dos propuestas nuevas del seguimiento",
    "",
    "| Comentario | Publicación | Respuesta propuesta | Estado |",
    "|---|---|---|---|",
])
for item in followup_items:
    if item.get("suggested_reply"):
        md.append(f"| {item['comment_excerpt']} | `{item['post_id']}` | **{item['suggested_reply']}** | `Pendiente_Fernando` |")
md.extend([
    "",
    "## Cola restante ya registrada",
    "",
    f"Además de las propuestas musicales, permanecen **{len(all_queue) - len(music_queue) - sum(1 for item in followup_items if item.get('suggested_reply'))}** propuestas de otros hilos, conservadas en `all_pending_proposals` dentro del JSON. No se descartan por antigüedad: se separan de los hallazgos nuevos para que la revisión no vuelva a perderlas.",
    "",
    "## Regla de publicación",
    "",
    "No se publicó ninguna respuesta en esta reconciliación. Fernando puede aprobar un subconjunto indicando los comentarios o copiando las respuestas; cada autorización pasará por preconsulta anti-duplicado y verificación en Meta.",
    "",
    "## Fuentes internas",
    "",
    "La evidencia cruda está en `2026-08-24_Facebook_Comment_Review_Broad_72h_Followup.json`. La sincronización de los cinco hallazgos nuevos está en `2026-08-24_Facebook_Followup_Review_Record.json`.",
])
MD_OUT.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

record = {
    "title": "Facebook Follow-up Review Record",
    "purpose": "Registrar cinco hallazgos nuevos del seguimiento y su clasificación sin publicar.",
    "status": "Active",
    "created_at": reviewed_at,
    "updated_at": reviewed_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h_Followup.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "reviewed_at": reviewed_at,
    "new_rows_added": len(followup_items),
    "new_proposals": sum(1 for item in followup_items if item.get("suggested_reply")),
    "new_no_action": sum(1 for item in followup_items if not item.get("suggested_reply")),
    "publication_performed": False,
    "comment_ids": [item["comment_id"] for item in followup_items],
}
RECORD_OUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"new_rows_added": len(followup_items), "new_proposals": record["new_proposals"], "new_no_action": record["new_no_action"], "total_pending_proposals": len(all_queue), "music_root_proposals": len(music_queue)}, ensure_ascii=False))
