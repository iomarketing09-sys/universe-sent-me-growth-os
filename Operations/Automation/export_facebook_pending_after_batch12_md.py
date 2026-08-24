"""Export current pending queue and API audit into a readable Markdown report."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json"
AUDIT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12_Audit.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.md"

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
audit = json.loads(AUDIT.read_text(encoding="utf-8"))
by_id = {item.get("comment_id"): item for item in audit.get("results", [])}
rows = []
for item in queue.get("pending", []):
    api = by_id.get(item.get("comment_id"), {})
    rows.append({**item, **api})

lines = [
    "# Cola pendiente de Facebook después del Batch 12",
    "",
    "**Propósito:** mostrar qué comentarios siguen pendientes después de publicar y verificar las cinco respuestas reclasificadas.",
    "**Estado:** Active",
    "**Fecha de creación:** 2026-08-24",
    "**Última actualización:** 2026-08-24",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_Pending_Queue_After_Batch12.json`; `2026-08-24_Facebook_Pending_Queue_After_Batch12_Audit.json`; `2026-08-15_Community_Engagement_Log.csv`",
    "**Organización:** Operations/Research",
    "",
    f"El ledger contiene **{len(rows)} registros pendientes** con propuesta. La auditoría de API encontró **{audit.get('accessible_count')} accesibles**, **{audit.get('inaccessible_count')} inaccesible**, **{audit.get('exact_reply_exists_count')} con respuesta exacta existente** y **{audit.get('api_error_count')} errores adicionales**.",
    "",
    "## Pendientes agrupados",
    "",
    "| Grupo | Cantidad | Situación |",
    "|---|---:|---|",
    "| Post meme `😏🙈😂 #UniverseUSM #MemesUSM #UniverseSentMe` | 8 | Raíces accesibles, sin respuesta directa de la Página |",
    "| Post musical — comentario `El día que volviste a la Tierra` | 1 | Inaccesible en Meta; no forzar publicación |",
    "| Post filosófico — réplica de usuario | 1 | Revisar si corresponde intervenir; no responder automáticamente |",
    "| Post musical — réplica que menciona a la Página | 1 | Puede merecer respuesta contextual, sujeto a criterio editorial |",
    "| Post meme — `Jajaja si soy` | 1 | Raíz accesible con propuesta contextual |",
    "",
    "## Detalle",
    "",
    "| Comentario | Propuesta actual | Estado API | Tipo |",
    "|---|---|---|---|",
]
for item in rows:
    comment = (item.get("comment_message") or "[sin texto]").replace("\n", " ").replace("|", "\\|")
    suggested = (item.get("suggested_reply") or "").replace("|", "\\|")
    if item.get("accessible") is False:
        api_state = "Inaccesible"
    else:
        api_state = "Accesible; sin respuesta Página"
    lines.append(f"| {comment} | **{suggested}** | {api_state} | {item.get('comment_type','')} |")
lines.extend([
    "",
    "## Regla operativa",
    "",
    "Las propuestas del cuadro permanecen pendientes de aprobación o revisión editorial según su tipo. Las réplicas de usuario a usuario no deben recibir una respuesta automática de la Página. El comentario musical inaccesible debe reintentarse solo en una auditoría futura; no se debe forzar una escritura con un objeto que Meta no carga.",
])
OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"pending": len(rows), "accessible": audit.get("accessible_count"), "inaccessible": audit.get("inaccessible_count")}, ensure_ascii=False))
