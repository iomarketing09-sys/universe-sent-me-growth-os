"""Export the remaining Facebook pending queue after music batch 09."""

import re
from collections import defaultdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_Remaining.md"

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
items = queue.get("all_pending_proposals", [])
remaining = [item for item in items if item.get("status") not in {"Respondido", "Bloqueado_API"} and item.get("comment_type") != "Replica_Anidada"]
blocked = [item for item in items if item.get("status") == "Bloqueado_API"]
groups = defaultdict(list)
for item in remaining:
    groups[item.get("post_message") or "Publicación sin caption recuperado"].append(item)
for values in groups.values():
    values.sort(key=lambda item: item.get("comment_created_time") or "", reverse=True)

def anonymize(text):
    text = (text or "").strip().replace("\n", " ")
    text = re.sub(r"^[A-ZÁÉÍÓÚÑ][^:]{0,45}:\s*", "", text)
    return text or "[comentario vacío]"

lines = [
    "# Cola restante de comentarios pendientes de Facebook",
    "",
    "**Propósito:** mostrar todos los comentarios que todavía tienen una propuesta pendiente después del Batch 09, sin limitarse a los hallazgos nuevos.",
    "**Estado:** Review  ",
    "**Fecha de creación:** 2026-08-24  ",
    "**Última actualización:** 2026-08-24  ",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_Pending_Queue_Reconciliation.json`; `2026-08-15_Community_Engagement_Log.csv`; `2026-08-24_Facebook_Comment_Publication_Batch_09.json`",
    "**Organización:** Operations/Research",
    "",
    f"Después del Batch 09 quedan **{len(remaining)} propuestas activas pendientes de aprobación**. Además, queda **{len(blocked)} comentario aprobado pero bloqueado** porque Meta ya no puede cargar su objeto. Las respuestas de esta lista no están publicadas.",
    "",
    "| Grupo | Cantidad |",
    "|---|---:|",
]
for post_message, values in sorted(groups.items(), key=lambda pair: (-len(pair[1]), pair[0])):
    lines.append(f"| {post_message} | {len(values)} |")
lines.extend(["", "## Pendientes agrupados por publicación", ""])
for post_message, values in sorted(groups.items(), key=lambda pair: (-len(pair[1]), pair[0])):
    lines.extend([f"### {post_message}", "", "| Comentario | Propuesta | Fecha |", "|---|---|---|"])
    for item in values:
        lines.append(f"| {anonymize(item.get('comment_excerpt'))} | **{item.get('suggested_reply', '')}** | {item.get('comment_created_time', '')} |")
    lines.append("")
if blocked:
    lines.extend(["## Comentario aprobado bloqueado por Meta", ""])
    lines.extend(["| Comentario | Propuesta | Estado |", "|---|---|---|"])
    for item in blocked:
        lines.append(f"| {anonymize(item.get('comment_excerpt'))} | **{item.get('suggested_reply', '')}** | `Bloqueado_API`; requiere nueva lectura antes de intentar publicar |")
    lines.append("")
lines.extend([
    "## Regla operativa",
    "",
    "Esta lista es una cola editorial, no una orden de publicación. Fernando puede aprobar un subconjunto por comentario o por respuesta. Cada aprobación deberá pasar por preconsulta anti-duplicado y verificación posterior en Meta Graph API v26.0.",
])
OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"remaining_active": len(remaining), "blocked": len(blocked), "groups": {key: len(value) for key, value in groups.items()}}, ensure_ascii=False))
