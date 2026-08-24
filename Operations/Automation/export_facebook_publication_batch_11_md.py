"""Export all Batch 11 publication results into a readable Markdown table."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_11.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_11.md"

def clean(value):
    return (value or "").replace("\n", " ").replace("|", "\\|").strip()

data = json.loads(BATCH.read_text(encoding="utf-8"))
rows = data.get("results", [])
if len(rows) != 28 or any(not row.get("verified") for row in rows):
    raise SystemExit("BATCH_11_NOT_28_VERIFIED")
lines = [
    "# Facebook Comment Publication Batch 11 — ☁️✨🤔",
    "",
    "**Propósito:** índice legible de las 28 respuestas publicadas y verificadas del post ☁️✨🤔.",
    "**Estado:** Active",
    "**Fecha de creación:** 2026-08-24",
    "**Última actualización:** 2026-08-24",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_Comment_Publication_Batch_11.json`; `2026-08-24_Facebook_Comment_Publication_Record_Batch_11.json`; `2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.md`",
    "**Organización:** Operations/Research",
    "",
    f"El JSON contiene **{len(rows)} resultados**; los **{len(rows)} fueron verificados** con autoría de Universe Sent Me, `parent.id` correcto, texto exacto e `is_hidden=false`.",
    "",
    "| # | Comentario | Respuesta publicada | Respuesta Meta | Verificado |",
    "|---:|---|---|---|---|",
]
for index, row in enumerate(rows, 1):
    lines.append(f"| {index} | {clean(row.get('comment_excerpt'))} | {clean(row.get('message'))} | `{clean(row.get('reply_id'))}` | Sí |")
OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"results": len(rows), "verified": sum(1 for row in rows if row.get("verified"))}, ensure_ascii=False))
