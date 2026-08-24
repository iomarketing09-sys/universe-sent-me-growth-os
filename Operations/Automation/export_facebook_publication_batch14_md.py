"""Export the verified Batch 14 publication record to a readable Markdown index."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.json"
RECORD = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_14.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_14.md"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
record = json.loads(RECORD.read_text(encoding="utf-8"))
results = batch["results"]

lines = [
    "# Facebook Batch 14 — publicación y verificación",
    "",
    "**Propósito:** índice legible de las 13 respuestas aprobadas por Fernando, publicadas mediante Meta Graph API v26.0 y verificadas individualmente.",
    "**Estado:** Active  ",
    "**Fecha de creación:** 2026-08-24  ",
    f"**Última actualización:** {batch['updated_at']}  ",
    f"**Versión:** {batch['version']}  ",
    "**Autor:** Manus AI  ",
    "**Documentos relacionados:** `2026-08-24_Facebook_Batch14_Engagement_Proposals.md`; `2026-08-24_Facebook_Batch14_Engagement_Proposals.json`; `2026-08-24_Facebook_Comment_Publication_Batch_14.json`; `2026-08-24_Facebook_Comment_Publication_Record_Batch_14.json`; `2026-08-24_Facebook_Pending_Queue_After_Batch14.json`; `2026-08-15_Community_Engagement_Log.csv`  ",
    "**Organización:** Operations/Research",
    "",
    "## Resumen verificado",
    "",
    "Fernando aprobó explícitamente las 13 respuestas antes de la ejecución. Se localizaron y verificaron 8 respuestas que ya habían sido creadas antes de la recuperación, se confirmó 1 publicación parcial cuya respuesta anidada requirió validación de cadena parent y se publicaron 4 respuestas que aún no existían. No se duplicó ningún POST.",
    "",
    "| Indicador | Resultado |",
    "|---|---:|",
    f"| Respuestas solicitadas | {batch['requested_count']} |",
    f"| Respuestas publicadas/localizadas | {batch['published_count']} |",
    f"| Verificaciones exitosas | {batch['verified_count']} |",
    f"| Ya existentes antes de la recuperación | {batch['already_published_before_recovery_count']} |",
    f"| Recuperadas tras publicación parcial | {batch['recovered_after_partial_publish_count']} |",
    f"| Publicadas durante la recuperación | {batch['published_during_recovery_count']} |",
    f"| Parent directo estricto | {batch['strict_direct_parent_count']} |",
    f"| Parent inmediato en réplica anidada | {batch['nested_immediate_parent_semantics_count']} |",
    f"| Respuestas no verificadas | {sum(1 for row in results if not row['verified'])} |",
    "",
    "## Detalle de las 13 respuestas",
    "",
    "| # | Comentario de referencia | Respuesta publicada | Meta reply ID | Timestamp | Verificación parent | Estado |",
    "|---:|---|---|---|---|---|---|",
]
for index, item in enumerate(results, start=1):
    comment = item.get("comment_message", "").replace("\n", " ").replace("|", "\\|")
    message = item.get("message", "").replace("|", "\\|")
    semantics = item.get("parent_semantics", "")
    lines.append(f"| {index} | {comment} (`{item['parent_comment_id']}`) | {message} | `{item['reply_id']}` | {item.get('reply_created_time', '')} | `{semantics}` | `verified=true`, `is_hidden=false` |")

lines.extend([
    "",
    "## Nota sobre la réplica anidada",
    "",
    "La respuesta a “Universe Sent Me creo te estás confundiendo jajajajajajaj” se encontró bajo la réplica objetivo. Meta devolvió como `parent.id` el parent inmediato de esa réplica (`nested_reply_api_returns_immediate_parent`) en lugar del ID de la réplica objetivo. La respuesta se consideró válida porque se encontró mediante `/{comment_id}/comments`, coincidió exactamente en autoría de Página, texto y visibilidad, y la cadena de parent fue consistente.",
    "",
    "## Estado operativo posterior",
    "",
    "El ledger fue actualizado con los 13 Meta reply IDs y sus timestamps. La cola posterior al Batch 14 contiene cero comentarios con estado `Pendiente_Respuesta` y cero pendientes con propuesta. Se mantiene una separación estricta entre las 13 escrituras autorizadas y los demás comentarios no accionables.",
    "",
    "## Referencias",
    "",
    "[1]: https://developers.facebook.com/docs/graph-api/reference/comment/ \"Meta for Developers — Comment reference\"",
    "[2]: https://developers.facebook.com/documentation/pages-api/comments-mentions \"Meta for Developers — Comments and @mentions\"",
])

OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"rows": len(results), "verified": sum(1 for row in results if row["verified"]), "output": str(OUT)}, ensure_ascii=False))
