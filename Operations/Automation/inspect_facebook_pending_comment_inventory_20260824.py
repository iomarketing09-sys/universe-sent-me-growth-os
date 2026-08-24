"""Inspect pending Facebook comments by joining the broad API audit and ledger."""

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Broad_72h.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    ledger = {row["Comentario_ID"]: row for row in csv.DictReader(handle)}
audit = json.loads(AUDIT.read_text(encoding="utf-8"))
rows = []
for item in audit["unanswered_within_window"]:
    ledger_row = ledger.get(item["comment_id"], {})
    rows.append({
        **item,
        "ledger_response_status": ledger_row.get("Respuesta_Estado", "NO_LEDGER_ROW"),
        "ledger_approval_status": ledger_row.get("Aprobacion_Estado", ""),
        "ledger_suggested_reply": ledger_row.get("Respuesta_Sugerida", ""),
        "ledger_signal": ledger_row.get("Señal", ""),
    })
rows.sort(key=lambda row: row.get("comment_created_time") or "", reverse=True)
print(json.dumps({
    "total_unanswered_within_window": len(rows),
    "by_ledger_status": dict(Counter(row["ledger_response_status"] for row in rows)),
    "pending_with_suggestions": sum(1 for row in rows if row["ledger_response_status"] == "Pendiente_Respuesta" and row["ledger_suggested_reply"]),
    "music_keyword_matches": sum(1 for row in rows if any(word in (row.get("comment_message") or "").lower() for word in ("cancion", "canciones", "música", "musica", "rammstein", "journey", "beatles", "rock", "playlist", "banda"))),
}, ensure_ascii=False))
print("--- PENDING WITH SUGGESTION ---")
for row in rows:
    if row["ledger_response_status"] == "Pendiente_Respuesta" and row["ledger_suggested_reply"]:
        print(json.dumps({key: row.get(key) for key in ("comment_id", "comment_created_time", "comment_type", "comment_message", "post_message", "ledger_suggested_reply", "ledger_signal")}, ensure_ascii=False))
print("--- MUSIC KEYWORD MATCHES ---")
for row in rows:
    if any(word in (row.get("comment_message") or "").lower() for word in ("cancion", "canciones", "música", "musica", "rammstein", "journey", "beatles", "rock", "playlist", "banda")):
        print(json.dumps({key: row.get(key) for key in ("comment_id", "comment_created_time", "comment_type", "comment_message", "post_message", "ledger_response_status", "ledger_suggested_reply")}, ensure_ascii=False))
