"""Reclassify four misunderstood no-action cases plus both emoji chains for review."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Comment_Review_Post_Batch10.json"
PROPOSALS = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.json"
MD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.md"
RECORD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Review_Record.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"

CORRECTIONS = {
    "122151375549072582_1046418834638831": (
        "Amén, que el misterio siga abierto. 😅🤔",
        "“Eimen” se interpreta como “Amén”, una aprobación/reacción religiosa breve al meme.",
    ),
    "122151375549072582_1837178844383978": (
        "Jajaja, el “yo” se reconoció en el meme. 😂🤔",
        "“Yo” se refiere a que la persona se identifica con la frase o situación del meme.",
    ),
    "122151375549072582_2263197197773933": (
        "Tu papá ya pidió los créditos de la creación. 😂🤔",
        "“My Dad” funciona como respuesta humorística a quién creó al creador; merece una respuesta breve y específica.",
    ),
    "122151375549072582_1640754384339219": (
        "Esa reacción trae risa, corazón y sello de aprobación en un solo paquete. 😂👑",
        "La combinación de risa, afecto, corona y 100% comunica aprobación entusiasta del meme.",
    ),
    "122151375549072582_1383611429837958": (
        "Eso fue una reacción completa: misterio, crisis y clima cósmico incluidos. 😂🌌",
        "La cadena mezcla sorpresa, confusión, asombro y símbolos cósmicos/climáticos; se puede interpretar de forma juguetona sin atribuir un significado exacto.",
    ),
}


def display(text):
    text = (text or "").strip().replace("\n", " ")
    return text or "[comentario vacío]"


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
root_by_id = {item["comment_id"]: item for item in audit.get("unanswered", []) if item.get("comment_type") == "Comentario_Raiz"}
proposal_data = json.loads(PROPOSALS.read_text(encoding="utf-8"))
existing_proposals = {item["comment_id"]: item for item in proposal_data.get("proposals", [])}
existing_no_action = {item["comment_id"]: item for item in proposal_data.get("no_action", [])}

for cid, (reply, reason) in CORRECTIONS.items():
    raw = root_by_id[cid]
    item = {
        "comment_id": cid,
        "comment_message": display(raw.get("comment_message")),
        "comment_created_time": raw.get("comment_created_time"),
        "suggested_reply": reply,
        "reason": reason,
        "status": "Pendiente_Respuesta",
        "approval_status": "Pendiente_Fernando",
    }
    existing_proposals[cid] = item
    existing_no_action.pop(cid, None)

# Keep the 28 already published items and append the five corrected pending proposals.
proposal_items = list(existing_proposals.values())
no_action_items = list(existing_no_action.values())
proposal_items.sort(key=lambda item: item.get("comment_created_time") or "", reverse=True)
no_action_items.sort(key=lambda item: item.get("comment_created_time") or "", reverse=True)

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fields = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
for item in proposal_items:
    row = by_id.get(item["comment_id"])
    if row is None:
        continue
    if item["comment_id"] in CORRECTIONS:
        row.update({
            "Señal": "Post_☁️✨🤔_Reclasificación_Fernando",
            "Respuesta_Estado": "Pendiente_Respuesta",
            "Respuesta_Sugerida": item["suggested_reply"],
            "Aprobacion_Estado": "Pendiente_Fernando",
            "Respuesta_Fecha": "",
            "Respuesta_Meta_ID": "",
            "Insight_Anonimo": item["reason"],
            "Prioridad": "Media",
            "Fuente": "Meta Graph API v26.0 — reclasificación editorial de Fernando",
        })
for item in no_action_items:
    row = by_id.get(item["comment_id"])
    if row is None:
        continue
    row.update({
        "Respuesta_Estado": "No_Requiere_Respuesta",
        "Respuesta_Sugerida": "",
        "Aprobacion_Estado": "No_Aplica",
        "Insight_Anonimo": item["reason"],
        "Prioridad": "Baja",
    })
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

proposal_data.update({
    "status": "Review",
    "version": "1.2",
    "updated_at": "2026-08-24",
    "proposal_count": len(proposal_items),
    "no_action_count": len(no_action_items),
    "publication_performed": True,
    "published_count": 28,
    "verified_count": 28,
    "editorial_correction": "Fernando confirmó que “Eimen” significa “Amén”, “Yo” expresa identificación con el meme, “My Dad” merece revisión y las cadenas de emojis pueden contener una reacción interpretable.",
    "proposals": proposal_items,
    "no_action": no_action_items,
    "next_step": "Revisar las cinco propuestas reclasificadas; no publicar sin aprobación explícita.",
})
PROPOSALS.write_text(json.dumps(proposal_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = [
    "# Respuestas, reclasificaciones y casos sin acción — post ☁️✨🤔",
    "",
    "**Propósito:** conservar las 28 respuestas publicadas del Batch 11 y documentar cinco casos reclasificados tras el feedback de Fernando.",
    "**Estado:** Review",
    "**Fecha de creación:** 2026-08-24",
    "**Última actualización:** 2026-08-24",
    "**Versión:** 1.2",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_Comment_Publication_Batch_11.json`; `2026-08-24_Facebook_Comment_Publication_Record_Batch_11.json`; `2026-08-24_Facebook_USM_Philosophy_Post_Comment_Review_Post_Batch10.json`; `2026-08-15_Community_Engagement_Log.csv`",
    "**Organización:** Operations/Research",
    "",
    "Las primeras 28 propuestas fueron publicadas y verificadas en el Batch 11. Las cinco siguientes son reclasificaciones pendientes; no se han publicado.",
    "",
    "## Cinco casos reclasificados pendientes",
    "",
    "| Comentario | Lectura corregida | Respuesta propuesta |",
    "|---|---|---|",
]
for cid in CORRECTIONS:
    item = next(item for item in proposal_items if item["comment_id"] == cid)
    md.append(f"| {item['comment_message']} | {item['reason']} | **{item['suggested_reply']}** |")
md.extend([
    "",
    "## Casos que siguen sin acción",
    "",
    "| Caso | Motivo |",
    "|---|---|",
])
for item in no_action_items:
    md.append(f"| [comentario no textual o referencia aislada] | {item['reason']} |")
md.extend([
    "",
    "## Publicación y aprobación",
    "",
    "Las 28 respuestas del Batch 11 ya están publicadas y verificadas. Las cinco reclasificaciones quedan pendientes de nueva aprobación explícita; no publicar sin autorización.",
])
MD_OUT.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

record = json.loads(RECORD_OUT.read_text(encoding="utf-8"))
record.update({
    "updated_at": "2026-08-24",
    "version": "1.1",
    "proposal_count": len(proposal_items),
    "no_action_count": len(no_action_items),
    "reclassified_comment_ids": list(CORRECTIONS),
    "publication_performed": False,
})
RECORD_OUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"published_batch11": 28, "reclassified_pending": len(CORRECTIONS), "no_action": len(no_action_items)}, ensure_ascii=False))
