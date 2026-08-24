"""Verify every Respondido Facebook ledger row against Meta Graph API v26.0.

Read-only: this script performs GET requests only and never publishes, edits,
hides, or deletes Facebook content. It is intended to close gaps between the
append-only ledger and older batch evidence files.
"""

import csv
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
OUT = RESEARCH / "2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30


def request(session, method, path, token, *, params=None):
    response = session.request(
        method,
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=TIMEOUT,
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text[:500]}
    return response.status_code, payload


def evidence_comment_ids():
    ids = set()
    for path in sorted(RESEARCH.glob("2026-08-24_Facebook_Comment_Publication_Record_Batch_*.json")) + sorted(RESEARCH.glob("2026-08-23_Facebook_Comment_Publication_Batch*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in (payload.get("records") or payload.get("results") or []):
            cid = item.get("comment_id") or item.get("target_comment_id") or item.get("parent_comment_id")
            if cid:
                ids.add(cid)
    return ids


with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    ledger_rows = list(reader)
    fields = reader.fieldnames or []
responded_rows = [row for row in ledger_rows if row.get("Respuesta_Estado") == "Respondido"]
if not responded_rows:
    raise SystemExit("NO_RESPONDIDO_ROWS_FOUND")
if len(fields) != 20:
    raise SystemExit(f"EXPECTED_20_LEDGER_COLUMNS: {len(fields)}")

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

session = requests.Session()
status, accounts = request(session, "GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
if status != 200:
    raise SystemExit(f"ME_ACCOUNTS_FAILED: HTTP_{status}")
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

fields_api = "id,from,message,created_time,parent,is_hidden"
existing_ids = evidence_comment_ids()
verified_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for row in responded_rows:
    comment_id = row.get("Comentario_ID", "")
    reply_id = row.get("Respuesta_Meta_ID", "")
    ledger_message = row.get("Respuesta_Sugerida", "")
    result = {
        "comment_id": comment_id,
        "reply_id": reply_id,
        "ledger_tipo": row.get("Tipo", ""),
        "ledger_message": ledger_message,
        "ledger_respuesta_fecha": row.get("Respuesta_Fecha", ""),
        "evidence_record_present_before_reconciliation": comment_id in existing_ids,
    }
    if not reply_id:
        result.update({"api_ok": False, "verified": False, "error": "MISSING_LEDGER_REPLY_ID"})
        results.append(result)
        continue
    status_code, payload = request(session, "GET", reply_id, page_token, params={"fields": fields_api})
    result["status_code"] = status_code
    result["api_payload"] = payload
    if status_code != 200 or not payload.get("id"):
        result.update({"api_ok": False, "verified": False, "error": f"META_HTTP_{status_code}"})
        results.append(result)
        continue
    returned_parent = (payload.get("parent") or {}).get("id")
    author_is_page = (payload.get("from") or {}).get("id") == PAGE_ID
    message_matches = payload.get("message") == ledger_message
    is_hidden_false = payload.get("is_hidden") is False
    parent_semantics = "direct_parent" if returned_parent == comment_id else "unexpected_parent"
    parent_matches = returned_parent == comment_id
    target_parent_id = None
    if not parent_matches:
        # Meta can return the parent of the target comment for a reply in a
        # nested thread. Query the target itself regardless of the historical
        # ledger type; older rows were not always typed as Replica_Anidada.
        target_status, target_payload = request(session, "GET", comment_id, page_token, params={"fields": fields_api})
        result["target_comment_status_code"] = target_status
        result["target_comment_payload"] = target_payload
        target_parent_id = (target_payload.get("parent") or {}).get("id") if target_status == 200 else None
        if target_parent_id and returned_parent == target_parent_id:
            parent_semantics = "nested_reply_api_returns_immediate_parent"
            parent_matches = True
        elif target_parent_id and returned_parent == (target_payload.get("parent") or {}).get("parent", {}).get("id"):
            parent_semantics = "nested_reply_api_returns_root_parent"
            parent_matches = True
        elif target_status == 200:
            # Some older Meta comment IDs have an alias in parent.id. Confirm
            # it is the same target by fetching the returned parent and
            # matching both message and created_time, not just a suffix.
            alias_status, alias_payload = request(session, "GET", returned_parent, page_token, params={"fields": fields_api})
            result["parent_alias_status_code"] = alias_status
            result["parent_alias_payload"] = alias_payload
            same_message = alias_payload.get("message") == target_payload.get("message")
            same_created = alias_payload.get("created_time") == target_payload.get("created_time")
            if alias_status == 200 and same_message and same_created:
                parent_semantics = "parent_id_alias_matches_target_comment"
                parent_matches = True
    result.update({
        "api_ok": True,
        "api_created_time": payload.get("created_time"),
        "api_from_id": (payload.get("from") or {}).get("id"),
        "api_from_name": (payload.get("from") or {}).get("name"),
        "api_message": payload.get("message"),
        "api_parent_id": returned_parent,
        "target_parent_id": target_parent_id,
        "api_is_hidden": payload.get("is_hidden"),
        "author_is_page": author_is_page,
        "message_matches": message_matches,
        "is_hidden_false": is_hidden_false,
        "parent_semantics": parent_semantics,
        "parent_matches": parent_matches,
        "verified": bool(author_is_page and message_matches and is_hidden_false and parent_matches),
    })
    results.append(result)

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
payload = {
    "title": "Facebook — verificación completa de comentarios respondidos",
    "purpose": "Verificar contra Meta Graph API v26.0 todos los comentarios del ledger con Respuesta_Estado=Respondido y cerrar las brechas de evidencia histórica sin realizar escrituras.",
    "status": "Active",
    "created_at": verified_at,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Community_Engagement_Log.md",
        "Operations/Research/2026-08-24_Facebook_All_Replies_Reconciliation.json",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
        "GrowthOS/00_01_Changelog_GrowthOS.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 GET only",
    "page_id": PAGE_ID,
    "ledger_rows_total": len(ledger_rows),
    "ledger_respondido_rows": len(responded_rows),
    "preexisting_publication_evidence_rows": sum(1 for row in results if row.get("evidence_record_present_before_reconciliation")),
    "rows_without_preexisting_publication_evidence": sum(1 for row in results if not row.get("evidence_record_present_before_reconciliation")),
    "api_ok_rows": sum(1 for row in results if row.get("api_ok")),
    "verified_rows": sum(1 for row in results if row.get("verified")),
    "unverified_rows": sum(1 for row in results if not row.get("verified")),
    "author_mismatch_rows": sum(1 for row in results if row.get("api_ok") and not row.get("author_is_page")),
    "message_mismatch_rows": sum(1 for row in results if row.get("api_ok") and not row.get("message_matches")),
    "visibility_mismatch_rows": sum(1 for row in results if row.get("api_ok") and not row.get("is_hidden_false")),
    "parent_mismatch_rows": sum(1 for row in results if row.get("api_ok") and not row.get("parent_matches")),
    "api_error_rows": sum(1 for row in results if not row.get("api_ok")),
    "parent_semantics_counts": {
        "direct_parent": sum(1 for row in results if row.get("parent_semantics") == "direct_parent"),
        "nested_reply_api_returns_immediate_parent": sum(1 for row in results if row.get("parent_semantics") == "nested_reply_api_returns_immediate_parent"),
        "nested_reply_api_returns_root_parent": sum(1 for row in results if row.get("parent_semantics") == "nested_reply_api_returns_root_parent"),
        "parent_id_alias_matches_target_comment": sum(1 for row in results if row.get("parent_semantics") == "parent_id_alias_matches_target_comment"),
        "unexpected_parent": sum(1 for row in results if row.get("parent_semantics") == "unexpected_parent"),
    },
    "results": results,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("ledger_rows_total", "ledger_respondido_rows", "preexisting_publication_evidence_rows", "rows_without_preexisting_publication_evidence", "api_ok_rows", "verified_rows", "unverified_rows", "api_error_rows", "author_mismatch_rows", "message_mismatch_rows", "visibility_mismatch_rows", "parent_mismatch_rows", "parent_semantics_counts")}, ensure_ascii=False))
