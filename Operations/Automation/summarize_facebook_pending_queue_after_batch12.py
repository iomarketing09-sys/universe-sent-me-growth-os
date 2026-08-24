"""Summarize current Facebook pending rows after Batch 12."""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch12.json"

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

pending = [row for row in rows if row.get("Plataforma") == "Facebook" and row.get("Respuesta_Estado") == "Pendiente_Respuesta"]
no_action = [row for row in rows if row.get("Plataforma") == "Facebook" and row.get("Respuesta_Estado") == "No_Requiere_Respuesta"]
proposed = [row for row in pending if (row.get("Respuesta_Sugerida") or "").strip()]
without_proposal = [row for row in pending if not (row.get("Respuesta_Sugerida") or "").strip()]
by_post = defaultdict(list)
for row in pending:
    by_post[row.get("Post_ID") or "(sin post)"] .append(row)

payload = {
    "title": "Facebook Pending Queue After Batch 12",
    "purpose": "Estado actual de la cola del ledger después de publicar y verificar el Batch 12.",
    "status": "Active",
    "created_at": "2026-08-24",
    "updated_at": "2026-08-24",
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_12.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_12.json",
    ],
    "organization": "Operations/Research",
    "source": "Community Engagement Log synchronized with Meta Graph API v26.0 publication records",
    "ledger_rows": len(rows),
    "facebook_pending_count": len(pending),
    "facebook_pending_with_proposal": len(proposed),
    "facebook_pending_without_proposal": len(without_proposal),
    "facebook_no_action_count": len(no_action),
    "groups": {post_id: len(items) for post_id, items in sorted(by_post.items())},
    "pending": [
        {
            "comment_id": row.get("Comentario_ID"),
            "post_id": row.get("Post_ID"),
            "comment_date": row.get("Fecha_Comentario"),
            "comment_type": row.get("Tipo"),
            "suggested_reply": row.get("Respuesta_Sugerida"),
            "approval_status": row.get("Aprobacion_Estado"),
            "priority": row.get("Prioridad"),
            "source": row.get("Fuente"),
        }
        for row in sorted(pending, key=lambda row: (row.get("Post_ID") or "", row.get("Fecha_Comentario") or ""), reverse=False)
    ],
    "no_action": [
        {"comment_id": row.get("Comentario_ID"), "post_id": row.get("Post_ID"), "reason": row.get("Insight_Anonimo")} for row in no_action
    ],
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("ledger_rows", "facebook_pending_count", "facebook_pending_with_proposal", "facebook_pending_without_proposal", "facebook_no_action_count", "groups")}, ensure_ascii=False))
