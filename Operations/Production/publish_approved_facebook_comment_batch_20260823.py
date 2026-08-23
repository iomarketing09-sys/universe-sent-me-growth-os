#!/usr/bin/env python3
"""Publish and verify the explicitly approved Facebook comment batch."""

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
CSV_PATH = Path(__file__).resolve().parents[2] / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT_PATH = Path(__file__).resolve().parents[2] / "Operations/Research/2026-08-23_Facebook_Comment_Publication_Batch.json"
TARGET_IDS = [
    "122151376083072582_1033379579457116",
    "122151376083072582_1534062764662566",
    "122151376011072582_1350675507083697",
    "122151376011072582_1576421464128022",
    "122151376011072582_1017393391124351",
    "122151376011072582_1693775178399393",
    "122151376011072582_4579578845653974",
    "122151376011072582_1726492438602303",
    "122151375549072582_1755338779425523",
    "122151376083072582_1712631733280410",
    "122151376083072582_1345911810604525",
]


def api(session, method, path, token, **kwargs):
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    response = session.request(method, f"{GRAPH}/{path.lstrip('/')}", headers=headers, timeout=30, **kwargs)
    try:
        payload = response.json()
    except Exception:
        payload = {"raw": response.text[:1000]}
    return response, payload


def page_name(reply):
    return (reply.get("from") or {}).get("name", "")


def verify_reply(session, page_token, reply_id, target_id, message):
    response, payload = api(session, "GET", reply_id, page_token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
    if response.status_code >= 400:
        return False, {"status_code": response.status_code, "payload": payload}
    parent_id = (payload.get("parent") or {}).get("id")
    checks = {
        "author_is_page": page_name(payload) == "Universe Sent Me",
        "parent_matches": parent_id == target_id,
        "message_matches": payload.get("message") == message,
        "is_hidden_false": payload.get("is_hidden") is False,
    }
    return all(checks.values()), {"status_code": response.status_code, "payload": payload, "checks": checks}


user_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not user_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
    reader = csv.DictReader(source)
    fieldnames = reader.fieldnames
    rows = list(reader)
rows_by_id = {row["Comentario_ID"]: row for row in rows}
missing = [comment_id for comment_id in TARGET_IDS if comment_id not in rows_by_id]
if missing:
    raise SystemExit(f"Missing target rows: {missing}")
for comment_id in TARGET_IDS:
    row = rows_by_id[comment_id]
    if row["Respuesta_Estado"] not in {"Pendiente_Respuesta", "Respondido"}:
        raise SystemExit(f"Unexpected state for {comment_id}: {row['Respuesta_Estado']}")

session = requests.Session()
accounts_response, accounts_payload = api(session, "GET", "me/accounts", user_token, params={"fields": "id,name,access_token,tasks", "limit": 100})
if accounts_response.status_code >= 400:
    raise SystemExit(f"Could not derive page token: {accounts_payload}")
page = next((item for item in accounts_payload.get("data", []) if item.get("id") == PAGE_ID and item.get("name") == "Universe Sent Me"), None)
if not page or not page.get("access_token"):
    raise SystemExit("Page token not found for Universe Sent Me")
page_token = page["access_token"]

run_at = datetime.now(timezone.utc).isoformat()
results = []
for target_id in TARGET_IDS:
    row = rows_by_id[target_id]
    message = row["Respuesta_Sugerida"]
    result = {
        "target_comment_id": target_id,
        "message": message,
        "run_at_utc": run_at,
    }

    replies_response, replies_payload = api(
        session,
        "GET",
        f"{target_id}/comments",
        page_token,
        params={"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100},
    )
    result["preflight_status_code"] = replies_response.status_code
    if replies_response.status_code >= 400:
        result["status"] = "preflight_failed"
        result["error"] = replies_payload
        results.append(result)
        continue

    existing = [reply for reply in replies_payload.get("data", []) if page_name(reply) == "Universe Sent Me"]
    exact_existing = next((reply for reply in existing if reply.get("message") == message), None)
    if exact_existing:
        reply_id = exact_existing.get("id")
        verified, verification = verify_reply(session, page_token, reply_id, target_id, message)
        result.update({"status": "already_present_verified" if verified else "existing_verification_failed", "reply_id": reply_id, "verification": verification})
        if verified:
            row["Respuesta_Estado"] = "Respondido"
            row["Aprobacion_Estado"] = "Aprobada"
            row["Respuesta_Fecha"] = (verification["payload"].get("created_time") or run_at)
            row["Respuesta_Meta_ID"] = reply_id
        results.append(result)
        continue

    post_response, post_payload = api(session, "POST", f"{target_id}/comments", page_token, data={"message": message})
    result["post_status_code"] = post_response.status_code
    result["post_response"] = post_payload
    if post_response.status_code >= 400 or not post_payload.get("id"):
        result["status"] = "publish_failed"
        results.append(result)
        continue

    reply_id = post_payload["id"]
    verified, verification = verify_reply(session, page_token, reply_id, target_id, message)
    result.update({"status": "published_verified" if verified else "published_verification_failed", "reply_id": reply_id, "verification": verification})
    if verified:
        row["Respuesta_Estado"] = "Respondido"
        row["Aprobacion_Estado"] = "Aprobada"
        row["Respuesta_Fecha"] = (verification["payload"].get("created_time") or run_at)
        row["Respuesta_Meta_ID"] = reply_id
    results.append(result)

with CSV_PATH.open("w", encoding="utf-8", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

summary = {
    "executed_at_utc": run_at,
    "page_id": PAGE_ID,
    "source": "Meta Graph API v26.0",
    "approved_batch_size": len(TARGET_IDS),
    "published_verified": sum(item["status"] == "published_verified" for item in results),
    "already_present_verified": sum(item["status"] == "already_present_verified" for item in results),
    "verification_failures": sum("verification_failed" in item["status"] for item in results),
    "publish_failures": sum(item["status"] in {"publish_failed", "preflight_failed"} for item in results),
    "results": results,
}
OUT_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: summary[key] for key in summary if key != "results"}, ensure_ascii=False))
if summary["publish_failures"] or summary["verification_failures"]:
    raise SystemExit(1)
