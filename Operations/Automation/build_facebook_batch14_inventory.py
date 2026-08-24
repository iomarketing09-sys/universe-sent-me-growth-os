"""Join Batch 14 read-only findings with the anonymized engagement ledger."""

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Current_Unanswered_Inventory.json"

review = json.loads(REVIEW.read_text(encoding="utf-8"))
with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    ledger = {row["Comentario_ID"]: row for row in csv.DictReader(handle)}

rows = []
for item in review.get("all_current_unanswered", []):
    ledger_row = ledger.get(item["comment_id"], {})
    rows.append({
        "comment_id": item["comment_id"],
        "post_id": item.get("post_id"),
        "post_message": item.get("post_message", ""),
        "post_permalink": item.get("post_permalink", ""),
        "comment_created_time": item.get("comment_created_time"),
        "comment_message": item.get("comment_message", ""),
        "comment_type": item.get("comment_type"),
        "parent_comment_id": item.get("parent_comment_id"),
        "is_hidden": item.get("is_hidden"),
        "already_logged": item.get("already_logged"),
        "ledger_status": ledger_row.get("Respuesta_Estado", "Not_In_Ledger"),
        "ledger_approval": ledger_row.get("Aprobacion_Estado", "Not_In_Ledger"),
        "ledger_signal": ledger_row.get("Señal", "Not_In_Ledger"),
        "ledger_suggested_reply": ledger_row.get("Respuesta_Sugerida", ""),
        "created_after_batch13_cursor": item.get("created_after_batch13_cursor", False),
    })
rows.sort(key=lambda row: row.get("comment_created_time") or "", reverse=True)

new_rows = [row for row in rows if row["created_after_batch13_cursor"]]
state_counts = Counter(row["ledger_status"] for row in rows)
type_counts = Counter(row["comment_type"] for row in rows)
result = {
    "title": "Facebook Batch 14 Current Unanswered Inventory",
    "purpose": "Inventario de unidades sin respuesta directa detectadas en las 20 publicaciones propias más recientes, unido al estado existente del ledger para no perder oportunidades antiguas.",
    "status": "Review",
    "created_at": review["reviewed_at"],
    "updated_at": review["reviewed_at"],
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch13.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 scan joined to Community Engagement Log",
    "read_only": True,
    "current_unanswered_count": len(rows),
    "new_since_batch13_cursor_count": len(new_rows),
    "state_counts": dict(state_counts),
    "type_counts": dict(type_counts),
    "new_since_batch13_cursor": new_rows,
    "current_unanswered": rows,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"current_unanswered": len(rows), "new_since_batch13_cursor": len(new_rows), "state_counts": state_counts}, ensure_ascii=False, default=dict))
