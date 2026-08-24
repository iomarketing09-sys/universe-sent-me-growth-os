"""Record linked-post review and nine approved-for-review proposals, never publish."""

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Comment_Review.json"
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Proposals.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Record.json"
FIELDS = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo",
    "Señal", "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado",
    "Respuesta_Fecha", "Respuesta_Meta_ID", "Insight_Anonimo", "Accion_Calendario",
    "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID", "Privacidad", "Fuente",
    "Ultima_Sincronizacion",
]
MODERATION_TERMS = ("pene", "verga", "chup", "ordeñ", "coger", "sexo", "sexual", "idiota", "puta", "puto")
WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+")


def no_action_reason(text, comment_type):
    text = (text or "").strip()
    lowered = text.lower()
    if not text:
        return "Comentario vacío; no requiere respuesta.", "Baja", "No_Accion"
    if any(term in lowered for term in MODERATION_TERMS):
        return "Lenguaje sexual u ofensivo; revisar contexto humano.", "Media", "Revisar"
    if comment_type == "Replica_Anidada":
        return "Réplica de usuario; no interrumpir conversación por defecto.", "Baja", "No_Accion"
    if len(WORD_RE.findall(text)) <= 3:
        return "Señal breve o mención; falta contexto para responder.", "Baja", "No_Accion"
    return "Sin propuesta en este corte; mantener fuera de la cola de publicación.", "Baja", "No_Accion"

review = json.loads(REVIEW.read_text(encoding="utf-8"))
proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
proposal_map = {row["comment_id"]: row["suggested_reply"] for row in proposal_data["proposals"]}
reviewed_at = review.get("reviewed_at", datetime.now(timezone.utc).isoformat(timespec="seconds"))
source = f"Meta Graph API v26.0 — auditoría del post {review.get('post_id')}"

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or FIELDS

by_id = {row.get("Comentario_ID"): row for row in rows}
appended = 0
updated = 0
proposal_updates = 0
for comment in review.get("unanswered", []):
    comment_id = comment.get("comment_id")
    if not comment_id:
        continue
    proposed = comment_id in proposal_map
    row = by_id.get(comment_id)
    if row is None:
        row = {field: "" for field in fieldnames}
        row.update({
            "Comentario_ID": comment_id,
            "Post_ID": comment.get("post_id", ""),
            "Fecha_Comentario": comment.get("comment_created_time", ""),
            "Plataforma": "Facebook",
            "Tipo": comment.get("comment_type", ""),
            "Privacidad": "Anonimizado",
            "Fuente": source,
            "Ultima_Sincronizacion": reviewed_at,
        })
        rows.append(row)
        by_id[comment_id] = row
        appended += 1
    if proposed:
        row.update({
            "Señal": "Propuesta_Respuesta",
            "Respuesta_Estado": "Pendiente_Respuesta",
            "Respuesta_Sugerida": proposal_map[comment_id],
            "Aprobacion_Estado": "Pendiente_Fernando",
            "Insight_Anonimo": "Propuesta específica del hilo; pendiente de aprobación, no publicada.",
            "Accion_Calendario": "Ninguna",
            "Prioridad": "Media",
            "Moderacion_Estado": "No_Accion",
            "Privacidad": "Anonimizado",
            "Fuente": source,
            "Ultima_Sincronizacion": reviewed_at,
        })
        if row.get("Respuesta_Estado") == "Pendiente_Respuesta":
            proposal_updates += 1
        updated += 1
    elif not row.get("Respuesta_Sugerida") and row.get("Respuesta_Estado") not in {"Respondido", "Pendiente_Respuesta"}:
        insight, priority, moderation = no_action_reason(comment.get("comment_message"), comment.get("comment_type"))
        row.update({
            "Señal": "Revisión_moderación" if moderation == "Revisar" else "Sin_Accion",
            "Respuesta_Estado": "Sin_Revisar" if moderation == "Revisar" else "No_Requiere_Respuesta",
            "Aprobacion_Estado": "No_Aplica",
            "Insight_Anonimo": insight,
            "Accion_Calendario": "Ninguna",
            "Prioridad": priority,
            "Moderacion_Estado": moderation,
            "Privacidad": "Anonimizado",
            "Fuente": source,
            "Ultima_Sincronizacion": reviewed_at,
        })
        updated += 1

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

payload = {
    "recorded_at": reviewed_at,
    "source": source,
    "post_id": review.get("post_id"),
    "reviewed_unanswered_units": len(review.get("unanswered", [])),
    "proposal_count": len(proposal_map),
    "ledger_rows_appended": appended,
    "ledger_rows_updated": updated,
    "proposal_rows_updated": proposal_updates,
    "no_publication_performed": True,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False))
