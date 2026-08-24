"""Build the current Facebook pending queue after the post-Batch-14 review."""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
EDITORIAL = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Batch14.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
OUT_JSON = RESEARCH / "2026-08-24_Facebook_Pending_Queue_After_Review.json"

editorial = json.loads(EDITORIAL.read_text(encoding="utf-8"))
records = editorial["records"]
proposals = [r for r in records if r["editorial_decision"] == "Pendiente_Respuesta"]
no_action = [r for r in records if r["editorial_decision"] == "No_Requiere_Respuesta"]
with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    ledger_rows = list(csv.DictReader(handle))

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
result = {
    "title": "Facebook Pending Queue After Post-Batch-14 Review",
    "purpose": "Estado actual de la cola después de registrar la revisión posterior al Batch 14; distingue propuestas que requieren aprobación de casos cerrados sin acción.",
    "status": "Review",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Batch14.md",
        "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Batch14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Community_Engagement_Log.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 / post-Batch-14 read-only review",
    "read_only_review": True,
    "approval_required_for_publication": True,
    "review_cursor": editorial["cursor"],
    "ledger_rows": len(ledger_rows),
    "review_candidate_count": len(records),
    "pending_response_count": len(proposals),
    "pending_response_with_proposal_count": len(proposals),
    "no_action_count_in_review": len(no_action),
    "publishable_without_new_approval": 0,
    "published_from_this_review": 0,
    "pending_comments": [
        {
            "comment_id": r["comment_id"],
            "post_id": r["post_id"],
            "comment_created_time": r["comment_created_time"],
            "comment_message": r["comment_message"],
            "post_message": r["post_message"],
            "proposed_reply": r["proposed_reply"],
            "priority": r["priority"],
            "insight": r["editorial_insight"],
            "approval_state": r["approval_state"],
        }
        for r in proposals
    ],
    "closed_without_action": [
        {
            "comment_id": r["comment_id"],
            "post_id": r["post_id"],
            "comment_created_time": r["comment_created_time"],
            "comment_message": r["comment_message"],
            "post_message": r["post_message"],
            "reason": r["editorial_insight"],
        }
        for r in no_action
    ],
}
OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("ledger_rows", "review_candidate_count", "pending_response_count", "no_action_count_in_review", "publishable_without_new_approval", "published_from_this_review")}, ensure_ascii=False))
