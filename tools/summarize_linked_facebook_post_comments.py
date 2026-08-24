"""Classify unanswered units from the linked Facebook Page Post for human review."""

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Comment_Review.json"
OUTPUT = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Comment_Review_Summary.md"
WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+")
MODERATION_TERMS = (
    "pene", "verga", "chup", "chupada", "fundillo", "ordeñe", "ordeñar", "coger",
    "cogiendo", "ching", "sexo", "sexual", "desnudo", "desnuda", "idiota", "puto", "puta",
)


def classify(row):
    text = (row.get("comment_message") or "").strip()
    lowered = text.lower()
    words = WORD_RE.findall(text)
    if not text:
        return "Sin_contenido", "No responder; comentario vacío.", "Baja"
    if any(term in lowered for term in MODERATION_TERMS):
        return "Revisión_moderación", "No responder automáticamente; revisar contexto humano.", "Media"
    if len(words) <= 1:
        return "Baja_señal", "No responder por defecto; falta contexto.", "Baja"
    if lowered.startswith(("gracias", "perfecto", "amén")) and len(words) <= 4:
        return "Cortesía_breve", "No requiere respuesta por defecto.", "Baja"
    if len(words) <= 3 and not ("?" in text or "¿" in text):
        return "Remate_breve", "Respuesta opcional; priorizar solo si aporta al hilo.", "Baja"
    if row.get("comment_type") == "Replica_Anidada" and any(name in text for name in (" ",)):
        return "Conversación_usuario", "No interrumpir conversación de usuarios por defecto.", "Baja"
    return "Contextual_sustantivo", "Revisar para respuesta específica; no publicar sin aprobación.", "Media"


data = json.loads(INPUT.read_text(encoding="utf-8"))
rows = data.get("unanswered", [])
for row in rows:
    category, action, priority = classify(row)
    row["category"] = category
    row["recommended_action"] = action
    row["priority"] = priority

counts = Counter(row["category"] for row in rows)
lines = [
    "# Resumen de comentarios sin respuesta — post enlazado",
    "",
    f"**Fuente:** `2026-08-24_Facebook_Linked_Post_Comment_Review.json`  ",
    f"**Post:** `{data.get('post_id')}` — {data.get('post', {}).get('permalink_url')}  ",
    f"**Revisión:** `{data.get('reviewed_at')}` mediante Meta Graph API v26.0, solo lectura  ",
    f"**Cobertura:** {data.get('root_comments_seen')} comentarios raíz, {data.get('comment_ids_seen')} IDs observados; un nivel de réplicas directas.",
    "",
    f"Meta detectó **{data.get('root_comments_without_direct_page_reply')} raíces sin respuesta directa** y **{data.get('unanswered_units_including_replies')} unidades sin respuesta incluyendo réplicas**. La falta de respuesta técnica no significa que cada unidad requiera una contestación.",
    "",
    "| Clasificación | Casos | Tratamiento |",
    "|---|---:|---|",
]
for category, count in counts.most_common():
    action = next(row["recommended_action"] for row in rows if row["category"] == category)
    lines.append(f"| `{category}` | {count} | {action} |")

lines += ["", "## Casos que merecen revisión humana", "", "| Comment ID | Hora | Tipo | Texto | Acción |", "|---|---|---|---|---|"]
for row in sorted(rows, key=lambda r: r.get("comment_created_time", "")):
    if row["category"] not in {"Contextual_sustantivo", "Revisión_moderación"}:
        continue
    text = (row.get("comment_message") or "").replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > 260:
        text = text[:257] + "..."
    lines.append(f"| `{row.get('comment_id')}` | `{row.get('comment_created_time')}` | `{row.get('comment_type')}` | {text} | {row.get('recommended_action')} |")

lines += ["", "## Casos sin acción recomendada", "", "Los comentarios vacíos, nombres aislados, agradecimientos breves, emojis y remates de baja señal no se convierten en respuesta automática. Las réplicas entre usuarios tampoco se contestan por defecto.", "", "| Comment ID | Texto |", "|---|---|"]
for row in sorted(rows, key=lambda r: r.get("comment_created_time", "")):
    if row["category"] in {"Contextual_sustantivo", "Revisión_moderación"}:
        continue
    text = (row.get("comment_message") or "").replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > 180:
        text = text[:177] + "..."
    lines.append(f"| `{row.get('comment_id')}` | {text or '(vacío)'} |")

lines += ["", "## Límite operativo", "", "La revisión de respuesta directa se basa en las respuestas de la Página devueltas dentro de cada raíz. Los comentarios profundos posteriores a la primera réplica no se expandieron. No se publicaron respuestas en esta revisión.", ""]
OUTPUT.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"unanswered_units": len(rows), "categories": dict(counts), "review_candidates": sum(1 for row in rows if row["category"] in {"Contextual_sustantivo", "Revisión_moderación"})}, ensure_ascii=False))
for row in rows:
    if row["category"] in {"Contextual_sustantivo", "Revisión_moderación"}:
        print(json.dumps({key: row.get(key) for key in ("comment_id", "comment_created_time", "comment_type", "category", "comment_message", "recommended_action")}, ensure_ascii=False))
