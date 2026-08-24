"""Prepare, but do not publish, reply proposals for the linked Facebook post."""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Comment_Review.json"
JSON_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Proposals.json"
MD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Proposals.md"

PROPOSALS = {
    "122151376083072582_1870186187563324": "Eso ya sería pasar de la química a la logística 😅 Mejor disfrutar la escena sin quedar atorados.",
    "122151376083072582_1719326086024419": "Jajaja, ahí está el detalle: no todas las sorpresas vienen con manual de instrucciones 😅",
    "122151376083072582_1108096458452825": "Jajaja, hay cosas que se disfrutan más cuando vienen con buen sentido del humor 😏",
    "122151376083072582_1028237043539692": "Jajaja, la escena dejó más de una teoría en el aire 😅",
    "122151376083072582_1976584486379301": "Tú sabrás… nosotros solo estamos tomando nota 😏😂",
    "122151376083072582_1037906569213579": "El cangrejo también tiene su club de fans 😂",
    "122151376083072582_1387619540151231": "Con esa confianza, el universo ya te apartó lugar para los 120 🤗✨",
    "122151376083072582_2371700183567495": "Rikolino sabe lo que dice 😂",
    "122151376083072582_1620302366278351": "La clave está en saber hacerlo… y en no perder el sentido del humor 😂",
}

raw = json.loads(INPUT.read_text(encoding="utf-8"))
unanswered = {row.get("comment_id"): row for row in raw.get("unanswered", [])}
missing = sorted(set(PROPOSALS) - set(unanswered))
if missing:
    raise SystemExit(f"PROPOSAL_IDS_NOT_UNANSWERED: {missing}")

rows = []
for comment_id, suggested_reply in PROPOSALS.items():
    row = unanswered[comment_id]
    rows.append({
        "comment_id": comment_id,
        "post_id": row.get("post_id"),
        "comment_created_time": row.get("comment_created_time"),
        "comment_type": row.get("comment_type"),
        "comment_message": row.get("comment_message"),
        "suggested_reply": suggested_reply,
        "status": "Pendiente_Fernando",
        "published": False,
    })

payload = {
    "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "source_reviewed_at": raw.get("reviewed_at"),
    "source": "Meta Graph API v26.0 / direct Page Post comments + one-level nested replies",
    "post_id": raw.get("post_id"),
    "linked_comment_id": raw.get("linked_comment_id"),
    "proposal_count": len(rows),
    "unanswered_units_reviewed": len(raw.get("unanswered", [])),
    "not_proposed_count": len(raw.get("unanswered", [])) - len(rows),
    "not_proposed_reasons": {
        "low_signal_or_empty": "Vacíos, nombres aislados, emojis, agradecimientos o remates demasiado breves.",
        "user_to_user_or_tag": "Réplicas o menciones dirigidas a otras personas; no interrumpir ni asumir intención.",
        "moderation_review": "Lenguaje sexual explícito o potencialmente ofensivo; revisión humana, no respuesta automática.",
    },
    "proposals": rows,
    "read_only_preparation": True,
    "no_publication_performed": True,
}
JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# Propuestas de respuesta — hilo enlazado de Facebook",
    "",
    "**Propósito:** Preparar respuestas específicas para el post enlazado por Fernando sin publicarlas hasta su aprobación.",
    "**Estado:** Review",
    f"**Fecha de creación:** {payload['created_at'][:10]}",
    f"**Última actualización:** {payload['created_at'][:10]}",
    "**Versión:** 1.0",
    "**Autor:** Manus AI (CGO)",
    "**Documentos relacionados:** `Operations/Research/2026-08-24_Facebook_Linked_Post_Comment_Review.json`, `Operations/Research/2026-08-24_Facebook_Linked_Post_Comment_Review_Summary.md`, `Operations/Research/2026-08-15_Community_Engagement_Log.csv`, `Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md`",
    "**Organización:** Operations/Research",
    "",
    f"**Fuente:** revisión de `{payload['post_id']}` mediante Meta Graph API v26.0; se observaron {payload['unanswered_units_reviewed']} unidades sin respuesta directa, de las cuales {payload['proposal_count']} tienen propuesta y {payload['not_proposed_count']} quedan fuera de la cola de publicación.",
    "",
    "| Comment ID | Comentario | Propuesta | Estado |",
    "|---|---|---|---|",
]
for row in rows:
    comment = (row["comment_message"] or "(vacío)").replace("\n", " ").replace("|", "\\|")
    lines.append(f"| `{row['comment_id']}` | {comment} | {row['suggested_reply']} | `Pendiente_Fernando` |")
lines += [
    "",
    "## Fuera de la cola de respuesta",
    "",
    "No se prepararon respuestas para comentarios vacíos, emojis, nombres aislados, agradecimientos breves, réplicas de baja señal, menciones dirigidas a otras personas o conversaciones entre usuarios. Tampoco se prepararon respuestas para lenguaje sexual explícito o potencialmente ofensivo; esos casos quedan para revisión humana de moderación.",
    "",
    "Ninguna propuesta de este documento ha sido publicada. La publicación requiere aprobación explícita de Fernando y verificación posterior de autoría, comentario padre, texto exacto e `is_hidden=false`.",
    "",
]
MD_OUT.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"proposal_count": len(rows), "unanswered_units_reviewed": len(raw.get("unanswered", [])), "not_proposed_count": len(raw.get("unanswered", [])) - len(rows), "published": False}, ensure_ascii=False))
