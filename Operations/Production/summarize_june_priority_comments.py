#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

src = Path("Operations/Research/2026-08-18_Comentarios_Junio_Lote_Prioritario.json")
out = Path("Operations/Research/2026-08-18_Analisis_Comentarios_Junio_Lote_Prioritario.md")
data = json.loads(src.read_text(encoding="utf-8"))
lines = [
"---",
"title: \"Análisis de comentarios del lote prioritario de junio\"",
"purpose: \"Resumir la conversación pública de cinco posts prioritarios para orientar taxonomía, reuse y gestión comunitaria.\"",
"status: \"Review\"",
"created: 2026-08-18",
"updated: 2026-08-18",
"version: \"1.0\"",
"author: \"Manus AI (CGO)\"",
"related_documents:",
"  - \"Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion.md\"",
"  - \"Operations/Research/2026-08-18_Junio_Lote_Priorizado_Taxonomia_Visual.csv\"",
"  - \"Operations/Research/2026-08-18_Comentarios_Junio_Lote_Prioritario.json\"",
"  - \"Operations/Research/2026-08-17_Reporte_Final_Recopilacion_Junio.md\"",
"organization: \"Operations/Research\"",
"---",
"",
"# Análisis de comentarios del lote prioritario de junio",
"",
"La extracción se realizó mediante un lote de lectura usando el Page Access Token de Universe Sent Me. No se publicaron respuestas ni se modificaron comentarios.",
"",
"| Asset | Comentarios recuperados | Comentarios raíz esperados en ledger | Lectura inicial |",
"|---|---:|---:|---|",
]
labels = ["2607823", "260740", "260765", "2607837", "260731"]
all_comments = []
for label, item in zip(labels, data["batch_response"]):
    parsed = json.loads(item.get("body", "{}"))
    comments = parsed.get("comments", {}).get("data", [])
    all_comments.extend(comments)
    postmsg = parsed.get("message", "")
    lines.append(f"| `{label}` | {len(comments)} | — | Caption publicado: `{postmsg}` |")
lines += ["", "## Patrones observados", ""]
texts = [c.get("message", "").strip() for c in all_comments if c.get("message", "").strip()]
emoji_only = sum(1 for t in texts if not any(ch.isalnum() for ch in t))
questions = sum(1 for t in texts if "?" in t or "¿" in t)
mentions = sum(1 for t in texts if "@" in t)
lines += [
 f"Se recuperaron **{len(all_comments)} comentarios** en total. Hay **{emoji_only} respuestas compuestas únicamente por emojis**, **{questions} comentarios con forma de pregunta** y **{mentions} con menciones explícitas**. Estos conteos son descriptivos y no equivalen por sí solos a sentimiento o calidad de comunidad.",
 "",
 "| Tipo de señal | Conteo | Interpretación operativa |",
 "|---|---:|---|",
 f"| Emojis solamente | {emoji_only} | Reacción rápida; no usar como evidencia de conversación profunda |",
 f"| Preguntas | {questions} | Candidatos para medir identificación, debate o invitación a responder |",
 f"| Menciones | {mentions} | Señal de potencial de etiquetado; revisar manualmente para distinguir conversación entre usuarios |",
 "| Comentarios textuales | Variable | Revisar por contexto; no automatizar respuestas |",
 "",
 "## Decisión CGO",
 "",
 "El post `2607823`, con 27 comentarios registrados en el ledger y 26 recuperados en esta lectura, debe ser el primer caso de análisis cualitativo porque combina shares altos con conversación. `260740`, `260765`, `2607837` y `260731` completan un sublote útil para comparar pieza textual, humor sexual/ácido y conversación relacional.",
 "",
 "Los comentarios sirven para enriquecer el aprendizaje de comunidad y potencial de etiquetado, pero no autorizan respuestas públicas. Cualquier respuesta debe pasar por aprobación humana. Tampoco se eleva ninguna observación a canon.",
 "",
 "## Limitaciones",
 "",
 "Meta no garantiza que la respuesta devuelta sea la totalidad histórica si existen restricciones de paginación o permisos; este corte conserva la evidencia de la consulta realizada. El análisis de sentimiento, humor y calidad de conversación requiere revisión de los textos completos y no debe inferirse solo por conteos.",
]
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(out)
print('total_comments',len(all_comments),'emoji_only',emoji_only,'questions',questions,'mentions',mentions)
