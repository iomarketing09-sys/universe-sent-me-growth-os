"""Publish the 25 approved root-comment proposals for the ☁️✨🤔 post."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
POST_ID = "1036844829507460_122151375549072582"
QUEUE_FILE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json"
BATCH_FILE = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_10.json"

queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
TARGETS = [
    {
        "parent_comment_id": item["comment_id"],
        "message": item["suggested_reply"],
        "comment_excerpt": item.get("comment_excerpt", ""),
    }
    for item in queue.get("all_pending_proposals", [])
    if item.get("post_message") == "☁️✨🤔"
    and item.get("comment_type") == "Comentario_Raiz"
    and item.get("suggested_reply")
    and item.get("status") not in {"Respondido", "Bloqueado_API"}
]
if len(TARGETS) != 25:
    raise SystemExit(f"EXPECTED_25_USM_PHILOSOPHY_TARGETS: {len(TARGETS)}")

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")


def request(method, path, token, *, params=None, data=None):
    response = requests.request(
        method,
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        data=data,
        timeout=30,
    )
    if not response.ok:
        raise RuntimeError(f"META_HTTP_{response.status_code}: {response.text[:500]}")
    return response.json()


accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]

prechecks = []
for target in TARGETS:
    parent_id = target["parent_comment_id"]
    message = target["message"]
    try:
        children = request(
            "GET",
            f"{parent_id}/comments",
            page_token,
            params={"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100},
        ).get("data", [])
    except RuntimeError as exc:
        prechecks.append({**target, "verified": None, "unavailable_error": str(exc)})
        continue
    exact = next(
        (child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") == message),
        None,
    )
    other_page = [
        child for child in children
        if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") != message
    ]
    if other_page and exact is None:
        raise SystemExit(json.dumps({"blocked_parent": parent_id, "existing_page_reply_ids": [item.get("id") for item in other_page]}, ensure_ascii=False))
    prechecks.append({**target, "verified": exact})

published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for item in prechecks:
    parent_id = item["parent_comment_id"]
    message = item["message"]
    if item.get("unavailable_error"):
        results.append({"status": "unavailable", "parent_comment_id": parent_id, "comment_excerpt": item.get("comment_excerpt"), "reply_id": None, "message": message, "error": item["unavailable_error"], "verified": False})
        continue
    verified = item["verified"]
    status = "already_published"
    if verified is None:
        created = request("POST", f"{parent_id}/comments", page_token, data={"message": message})
        reply_id = created.get("id")
        if not reply_id:
            raise SystemExit(json.dumps({"missing_reply_id": parent_id}, ensure_ascii=False))
        verified = request("GET", reply_id, page_token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
        status = "published"
    parent = verified.get("parent") or {}
    results.append({
        "status": status,
        "parent_comment_id": parent_id,
        "comment_excerpt": item.get("comment_excerpt"),
        "reply_id": verified.get("id"),
        "message": verified.get("message"),
        "from_id": (verified.get("from") or {}).get("id"),
        "from_name": (verified.get("from") or {}).get("name"),
        "parent_id_returned": parent.get("id"),
        "is_hidden": verified.get("is_hidden"),
        "verified": (
            (verified.get("from") or {}).get("id") == PAGE_ID
            and verified.get("message") == message
            and parent.get("id") == parent_id
            and verified.get("is_hidden") is False
        ),
    })

if any(result["status"] not in {"published", "already_published", "unavailable"} for result in results):
    raise SystemExit(json.dumps({"unexpected_result": results}, ensure_ascii=False))

payload = {
    "title": "Facebook Comment Publication Batch 10 — ☁️✨🤔",
    "purpose": "Evidencia de la publicación y verificación de las 25 respuestas aprobadas para comentarios raíz del post ☁️✨🤔.",
    "status": "Active",
    "created_at": published_at,
    "updated_at": published_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_Reconciliation.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_10.json",
    ],
    "organization": "Operations/Research",
    "published_at": published_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "post_id": POST_ID,
    "explicit_user_approval": True,
    "requested_count": len(TARGETS),
    "published_count": sum(1 for result in results if result["status"] == "published"),
    "already_published_count": sum(1 for result in results if result["status"] == "already_published"),
    "inaccessible_count": sum(1 for result in results if result["status"] == "unavailable"),
    "verified_count": sum(1 for result in results if result["verified"]),
    "results": results,
}
BATCH_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "inaccessible_count", "verified_count")}, ensure_ascii=False))
for result in results:
    print(json.dumps(result, ensure_ascii=False))
