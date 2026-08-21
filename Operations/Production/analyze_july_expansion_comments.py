#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Evidence.json"
OUTPUT_JSON = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Analysis.json"
OUTPUT_MD = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Analysis.md"


def classify(text: str) -> list[str]:
    lower = text.lower()
    labels = []
    if "@" in text:
        labels.append("mention")
    if "?" in text or re.search(r"\b(qué|como|cómo|por qué|quien|quién)\b", lower):
        labels.append("question")
    if any(word in lower for word in ["jaj", "jeje", "😂", "🤣", "😆", "😅", "😹", "😝", "🤡"]):
        labels.append("laughter_or_play")
    if any(word in lower for word in ["yo", "soy", "me pasa", "igual", "x2", "literal", "así"]):
        labels.append("identification")
    if any(word in lower for word in ["etiquet", "tag", "menciona", "amig", "novi", "herman", "compa"]):
        labels.append("social_tagging")
    if not labels:
        labels.append("other")
    return labels


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    per_post = []
    all_comments = []
    for post in payload.get("posts", []):
        comments = post.get("comments", [])
        counts = Counter()
        comment_rows = []
        for comment in comments:
            text = comment.get("message") or ""
            labels = classify(text)
            counts.update(labels)
            comment_rows.append({"id": comment.get("id"), "message": text, "labels": labels, "like_count": comment.get("like_count", 0)})
            all_comments.append({"Meta_ID": post["Meta_ID"], "message": text, "labels": labels, "like_count": comment.get("like_count", 0)})
        per_post.append({"Meta_ID": post["Meta_ID"], "comments": len(comments), "categories": dict(counts), "top_liked_comments": sorted(comment_rows, key=lambda row: -int(row.get("like_count") or 0))[:5]})
    total_categories = Counter(label for row in all_comments for label in row["labels"])
    top_social = sorted((row for row in all_comments if any(label in row["labels"] for label in ["question", "social_tagging", "identification"])), key=lambda row: -int(row.get("like_count") or 0))[:20]
    result = {"input_posts": len(per_post), "comments_total": len(all_comments), "categories_total": dict(total_categories), "per_post": per_post, "top_social_comments": top_social, "decision": "Only extract deeper comment threads for posts whose comments add a concrete community-learning question; do not process all 16 as a moderation queue."}
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "---", "title: \"Análisis de conversación — ampliación individual de julio, lote 01\"", "purpose: \"Determinar si los comentarios de los 16 nuevos casos aportan una pregunta de aprendizaje o solo volumen descriptivo.\"", "status: Review", "created: 2026-08-21", "updated: 2026-08-21", "version: \"1.0\"", "author: \"Manus AI (CGO)\"", "related_documents:", "  - \"Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Evidence.json\"", "  - \"Operations/Research/2026-08-21_Julio_Expansion_Lote01_Analysis.md\"", "organization: \"Operations/Research\"", "---", "", "# Análisis de conversación — ampliación individual de julio, lote 01", "", f"Meta devolvió **{len(all_comments)} comentarios** en las 16 publicaciones nuevas. Esta extracción es descriptiva y no sustituye métricas de 24/72 horas. El objetivo fue detectar si alguna publicación requiere una lectura cualitativa más profunda, no crear una cola de respuestas comunitarias.", "", "| Señal | Conteo |", "|---|---:|"]
    for key, value in sorted(total_categories.items()):
        lines.append(f"| {key} | {value} |")
    lines += ["", "## Decisión", "", "La conversación del lote 01 se conserva como capa histórica. No se recomienda extraer o analizar manualmente los 284 comentarios uno por uno: la mayoría sirve como señal descriptiva de identificación, humor o etiquetado. Solo deben abrirse análisis cualitativos adicionales cuando una publicación combine comentarios altos con una pregunta editorial concreta, una conversación sostenida o una oportunidad real de aprendizaje comunitario.", "", "Los comentarios recuperados no autorizan respuestas ni publicaciones. Cualquier intervención en Meta permanece sujeta a aprobación humana explícita.", "", "## Publicaciones con mayor prioridad para revisión cualitativa", "", "| Meta_ID | Comentarios | Interacciones | Shares | Razón |", "|---|---:|---:|---:|---|"]
    # Use per-post comment count, lookup metrics from the source comments evidence is unavailable; keep only comment count and reason.
    for row in sorted(per_post, key=lambda item: -item["comments"])[:5]:
        reasons = ", ".join(f"{k}={v}" for k, v in sorted(row["categories"].items()) if k in {"question", "social_tagging", "identification"}) or "volumen descriptivo"
        lines.append(f"| `{row['Meta_ID']}` | {row['comments']} | — | — | {reasons} |")
    lines += ["", "## Referencias", "", "[1]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Comments_Evidence.json` — extracción batch de comentarios de Meta.", "[2]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Analysis.md` — análisis de rendimiento y taxonomía del lote."]
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"comments_total": len(all_comments), "categories": dict(total_categories), "output_md": str(OUTPUT_MD), "output_json": str(OUTPUT_JSON)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
