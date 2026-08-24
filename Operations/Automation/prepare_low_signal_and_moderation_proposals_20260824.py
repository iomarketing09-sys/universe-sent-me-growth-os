"""Prepare safe moderation and low-signal proposals; do not publish them."""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Comment_Review.json"
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Proposals.json"
PROPOSALS_MD = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Proposals.md"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Safety_LowSignal_Proposals.json"

MODERATION = {
    "122151376083072582_1747280716505079": {
        "suggested_reply": "Jajaja, entendimos el doble sentido, pero mantengamos el hilo en tono juguetón y sin detalles explícitos 😅",
        "reason": "Doble sentido sexual explícito; redirigir sin repetir ni ampliar el contenido.",
    },
    "122151376083072582_1694103262232576": {
        "suggested_reply": "Vamos a dejar esa parte en la imaginación y mantener el hilo en tono juguetón, sin detalles explícitos 😅",
        "reason": "Solicitud sexual explícita; responder con límite amable y sin contenido gráfico.",
    },
}
LOW_SIGNAL = {
    "122151376083072582_2288087915279831": "Cangrejera oficial del universo 😂",
    "122151376083072582_1374303084841115": "Esa cara dice que el universo dejó más preguntas que respuestas 😅",
    "122151376083072582_2076744963209419": "Jajaja, el universo recomienda ir con calma 😅",
    "122151376083072582_1057397926935250": "Upps… el universo tomó nota 😅",
    "122151376083072582_2139372153647884": "El universo recibe ese amén 😅✨",
    "122151376083072582_1031789069652438": "La recomendación queda registrada 😅",
    "122151376083072582_1435662098773431": "El cangrejo también tiene su momento 😂",
    "122151376083072582_1800051157832910": "¡Gracias a ti por pasar por aquí! 🫂✨",
    "122151376083072582_886767890954566": "¡Gracias a ti por pasar por aquí! 🫂✨",
}

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
review = json.loads(REVIEW.read_text(encoding="utf-8"))
by_id = {row.get("comment_id"): row for row in review.get("unanswered", [])}
missing = [comment_id for comment_id in [*MODERATION, *LOW_SIGNAL] if comment_id not in by_id]
if missing:
    raise SystemExit(f"TARGET_NOT_IN_REVIEW: {missing}")

rows = []
for comment_id, meta in MODERATION.items():
    row = by_id[comment_id]
    rows.append({
        "comment_id": comment_id,
        "post_id": row.get("post_id"),
        "comment_message": row.get("comment_message"),
        "comment_type": row.get("comment_type"),
        "category": "Revisión_moderación",
        "suggested_reply": meta["suggested_reply"],
        "reason": meta["reason"],
        "status": "Sin_Revisar",
        "approval_status": "Pendiente_Fernando",
        "moderation_status": "Revisar",
        "publish_recommendation": "No publicar automáticamente",
        "published": False,
    })
for comment_id, suggested_reply in LOW_SIGNAL.items():
    row = by_id[comment_id]
    rows.append({
        "comment_id": comment_id,
        "post_id": row.get("post_id"),
        "comment_message": row.get("comment_message"),
        "comment_type": row.get("comment_type"),
        "category": "Baja_señal",
        "suggested_reply": suggested_reply,
        "reason": "Propuesta opcional para dar continuidad; no es necesario responder si se prioriza evitar ruido.",
        "status": "Pendiente_Respuesta",
        "approval_status": "Pendiente_Fernando",
        "moderation_status": "No_Accion",
        "publish_recommendation": "Opcional; no publicar sin aprobación",
        "published": False,
    })

proposal_payload = json.loads(PROPOSALS.read_text(encoding="utf-8"))
proposal_payload["updated_at"] = now
proposal_payload["safety_proposal_count"] = len(MODERATION)
proposal_payload["low_signal_proposal_count"] = len(LOW_SIGNAL)
proposal_payload["safety_and_low_signal_proposals"] = rows
proposal_payload["empty_comment_policy"] = "No preparar respuesta para comentarios vacíos; no hay contenido al que responder."
proposal_payload["new_proposals_published"] = False
PROPOSALS.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = PROPOSALS_MD.read_text(encoding="utf-8").rstrip() + "\n\n"
md += "## Propuestas adicionales: lenguaje sexual explícito\n\n"
md += "Estas propuestas son límites amables y no gráficas. No repiten ni desarrollan el contenido sexual del usuario y quedan pendientes de aprobación; no se han publicado.\n\n"
md += "| Comment ID | Comentario | Propuesta | Estado |\n|---|---|---|---|\n"
for row in rows[: len(MODERATION)]:
    md += f"| `{row['comment_id']}` | {row['comment_message']} | {row['suggested_reply']} | `Pendiente_Fernando` / `Revisar` |\n"
md += "\n## Propuestas opcionales: baja señal\n\n"
md += "Estas respuestas pueden generar continuidad, pero no son obligatorias. Para comentarios vacíos, nombres aislados o conversaciones entre usuarios se mantiene la recomendación de no responder.\n\n"
md += "| Comment ID | Comentario | Propuesta opcional | Estado |\n|---|---|---|---|\n"
for row in rows[len(MODERATION):]:
    md += f"| `{row['comment_id']}` | {row['comment_message']} | {row['suggested_reply']} | `Pendiente_Fernando` |\n"
md += "\n**Política de comentarios vacíos:** no se prepara respuesta porque no existe señal textual; se mantienen como `No_Requiere_Respuesta`. Ninguna propuesta de estas dos secciones ha sido publicada.\n"
PROPOSALS_MD.write_text(md, encoding="utf-8")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    ledger_rows = list(reader)
    fieldnames = reader.fieldnames or []
ledger_by_id = {row.get("Comentario_ID"): row for row in ledger_rows}
for row in rows:
    target = ledger_by_id.get(row["comment_id"])
    if target is None:
        continue
    target.update({
        "Señal": row["category"],
        "Respuesta_Estado": row["status"],
        "Respuesta_Sugerida": row["suggested_reply"],
        "Aprobacion_Estado": row["approval_status"],
        "Insight_Anonimo": row["reason"],
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media" if row["category"] == "Revisión_moderación" else "Baja",
        "Moderacion_Estado": row["moderation_status"],
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — propuesta segura de hilo enlazado",
        "Ultima_Sincronizacion": now,
    })
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(ledger_rows)

payload = {
    "created_at": now,
    "source": "Meta Graph API v26.0 / linked post review",
    "post_id": review.get("post_id"),
    "moderation_proposals": len(MODERATION),
    "low_signal_proposals": len(LOW_SIGNAL),
    "empty_comments_left_unanswered": sum(1 for row in review.get("unanswered", []) if not (row.get("comment_message") or "").strip()),
    "published": False,
    "records": rows,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("moderation_proposals", "low_signal_proposals", "empty_comments_left_unanswered", "published")}, ensure_ascii=False))
