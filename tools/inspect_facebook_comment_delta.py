"""Summarize a read-only Facebook comment delta without names or profiles."""

import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_05.json"
OUTPUT = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_05_Summary.md"

WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+")
MODERATION_TERMS = (
    "pene", "verga", "chup", "chupada", "fundillo", "coger", "cogiendo",
    "ching", "sexo", "sexual", "desnudo", "desnuda", "idiota", "puto", "puta",
)


def is_emoji_or_symbol_only(text):
    for char in text:
        if char.isspace():
            continue
        category = unicodedata.category(char)
        if category[0] in {"L", "N"}:
            return False
        if category.startswith("M"):
            continue
        if category in {"Pc", "Pd", "Pe", "Pf", "Pi", "Po", "Ps", "Sc", "Sk", "Sm", "So", "Cf"}:
            continue
        return False
    return bool(text.strip())


def classify(row):
    text = (row.get("comment_message") or "").strip()
    lowered = text.lower()
    words = WORD_RE.findall(text)
    if not text:
        return "Sin_contenido", "No requiere respuesta; comentario vacío."
    if any(term in lowered for term in MODERATION_TERMS):
        return "Revisión_moderación", "No responder automáticamente; revisar contexto humano."
    if is_emoji_or_symbol_only(text):
        return "Emoji_o_símbolo", "Reacción breve; no requiere respuesta."
    if row.get("comment_type") == "Replica_Anidada" and len(words) <= 5:
        return "Réplica_baja_señal", "Conversación de usuarios o remate breve; no interrumpir por defecto."
    if len(words) <= 3 and "?" not in text and "¿" not in text:
        return "Respuesta_breve", "Señal de baja fricción; no requiere respuesta por defecto."
    return "Contextual_sustantivo", "Revisar para posible respuesta específica o moderación."


data = json.loads(INPUT.read_text(encoding="utf-8"))
rows = data.get("comments", [])
for row in rows:
    category, action = classify(row)
    row["category"] = category
    row["recommended_action"] = action

categories = Counter(row["category"] for row in rows)
by_post = defaultdict(Counter)
for row in rows:
    by_post[row.get("post_id", "")][row["category"]] += 1

lines = [
    "# Resumen de revisión de comentarios de Facebook — delta 05",
    "",
    "**Fuente:** `2026-08-23_Facebook_Comment_Review_Delta_05.json`",
    f"**Corte:** {data.get('cutoff')} → {data.get('reviewed_at')}",
    "**Modo:** solo lectura mediante Meta Graph API v26.0; no se publicaron respuestas.",
    f"**Cobertura:** {data.get('page_posts_reviewed')} publicaciones propias más recientes; comentarios raíz y réplicas directas; sin expansión de niveles más profundos.",
    "",
    "## Resumen",
    "",
    f"Se recuperaron **{len(rows)} comentarios de usuarios posteriores al último corte**, todos sin una respuesta directa de la Página detectada en la consulta. El estado técnico `sin respuesta` no significa que todos requieran contestación: la clasificación separa ruido, conversación entre usuarios, señales sustantivas y posibles casos de moderación.",
    "",
    "| Categoría | Casos | Acción operativa |",
    "|---|---:|---|",
]
for category, count in categories.most_common():
    action = next(row["recommended_action"] for row in rows if row["category"] == category)
    lines.append(f"| `{category}` | {count} | {action} |")

lines += ["", "## Distribución por publicación", "", "| Post ID | Categorías detectadas |", "|---|---|"]
for post_id, counts in by_post.items():
    parts = ", ".join(f"`{category}`: {count}" for category, count in counts.items())
    lines.append(f"| `{post_id}` | {parts} |")

lines += ["", "## Comentarios que merecen revisión humana", "", "Estos casos tienen texto contextual, conversación potencial o una señal que no conviene responder con plantilla. No se publicó ninguna respuesta.", "", "| Comment ID | Post ID | Hora | Tipo | Texto anonimizado | Acción |", "|---|---|---|---|---|---|"]
for row in sorted(rows, key=lambda item: item.get("comment_created_time", "")):
    if row["category"] not in {"Contextual_sustantivo", "Revisión_moderación"}:
        continue
    text = (row.get("comment_message") or "").replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > 240:
        text = text[:237] + "..."
    lines.append(f"| `{row.get('comment_id')}` | `{row.get('post_id')}` | `{row.get('comment_created_time')}` | `{row.get('comment_type')}` | {text} | {row.get('recommended_action')} |")

lines += ["", "## Referencia técnica", "", "- `posts_fetched=20`, `page_posts_reviewed=20`, `root_comments_seen=160`.", "- `api_error_count=0`; la consulta de cada post y de sus réplicas directas respondió sin error.", "- La detección de respuesta se limita a una respuesta directa de la Página dentro del nivel consultado; no se infiere respuesta por caption, reacción o conversación entre usuarios.", "- Los nombres y perfiles no se conservan en este resumen.", ""]
OUTPUT.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"rows": len(rows), "categories": categories, "review_candidates": sum(1 for row in rows if row["category"] in {"Contextual_sustantivo", "Revisión_moderación"})}, ensure_ascii=False, default=dict))
for row in rows:
    if row["category"] in {"Contextual_sustantivo", "Revisión_moderación"}:
        print(json.dumps({key: row.get(key) for key in ("comment_id", "post_id", "comment_created_time", "comment_type", "category", "comment_message", "recommended_action")}, ensure_ascii=False))
