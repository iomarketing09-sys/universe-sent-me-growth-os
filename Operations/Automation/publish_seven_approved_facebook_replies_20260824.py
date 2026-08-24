"""Publish the seven explicitly approved Facebook replies and verify each result."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
POST_ID = "1036844829507460_122151376083072582"
BATCH_FILE = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_07.json"
TARGETS = [
    {
        "parent_comment_id": "122151376083072582_2218476525601574",
        "message": "El universo escuchó ese “yes yes yes”. 😂🙈",
    },
    {
        "parent_comment_id": "122151376083072582_1461910735802563",
        "message": "No todas recibieron el mismo manual del universo. 😂",
    },
    {
        "parent_comment_id": "122151376083072582_2136675140593360",
        "message": "Jajaja, el universo también contempla ese pequeño detalle. 😂",
    },
    {
        "parent_comment_id": "122151376083072582_2013957549234314",
        "message": "Eso ya no fue problema de técnica; fue falta de criterio. 😂",
    },
    {
        "parent_comment_id": "122151376083072582_1046993968083177",
        "message": "Son los ejercicios de Kegel; para hacerlos bien, mejor revisa una guía profesional. 😅",
    },
    {
        "parent_comment_id": "122151376083072582_1777381266626241",
        "message": "Jajaja, el universo ya puso sus requisitos. 😂🙈",
    },
    {
        "parent_comment_id": "122151376011072582_1379392830310327",
        "message": "Sí, esa lectura de una mujer con tantos pretendientes le pone otra capa a la canción. 👀 Rammstein no deja precisamente las cosas en la superficie.",
    },
]

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
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND")
page_token = page["access_token"]

children_by_parent = {}
precheck_results = []
for target in TARGETS:
    parent_id = target["parent_comment_id"]
    message = target["message"]
    children = request(
        "GET",
        f"{parent_id}/comments",
        page_token,
        params={"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100},
    ).get("data", [])
    children_by_parent[parent_id] = children
    exact = next(
        (child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") == message),
        None,
    )
    other_page_replies = [
        child for child in children
        if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") != message
    ]
    precheck_results.append({
        "parent_comment_id": parent_id,
        "message": message,
        "exact_existing_reply": exact,
        "other_page_replies": other_page_replies,
    })

conflicts = [
    row for row in precheck_results
    if row["other_page_replies"] and not row["exact_existing_reply"]
]
if conflicts:
    raise SystemExit(json.dumps({
        "blocked_existing_page_replies": [
            {
                "parent_comment_id": row["parent_comment_id"],
                "existing_reply_ids": [child.get("id") for child in row["other_page_replies"]],
            }
            for row in conflicts
        ]
    }, ensure_ascii=False))

published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for row in precheck_results:
    parent_id = row["parent_comment_id"]
    message = row["message"]
    verified = row["exact_existing_reply"]
    status = "already_published"
    if verified is None:
        created = request("POST", f"{parent_id}/comments", page_token, data={"message": message})
        reply_id = created.get("id")
        if not reply_id:
            raise SystemExit(json.dumps({"missing_reply_id": parent_id}, ensure_ascii=False))
        verified = request(
            "GET",
            reply_id,
            page_token,
            params={"fields": "id,from,message,created_time,parent,is_hidden"},
        )
        status = "published"
    parent = verified.get("parent") or {}
    result = {
        "status": status,
        "parent_comment_id": parent_id,
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
    }
    results.append(result)

if any(not row["verified"] for row in results):
    raise SystemExit(json.dumps({"verification_failed": results}, ensure_ascii=False))

payload = {
    "title": "Facebook Comment Publication Batch 07",
    "purpose": "Evidencia de la publicación y verificación de las siete respuestas aprobadas por Fernando.",
    "status": "Active",
    "created_at": published_at,
    "updated_at": published_at,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_07.json",
        "Operations/Research/2026-08-24_Facebook_Expanded_Audit_Reply_Proposals.json",
    ],
    "organization": "Operations/Research",
    "published_at": published_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "post_id": POST_ID,
    "explicit_user_approval": True,
    "requested_count": len(TARGETS),
    "published_count": sum(1 for row in results if row["status"] == "published"),
    "already_published_count": sum(1 for row in results if row["status"] == "already_published"),
    "verified_count": sum(1 for row in results if row["verified"]),
    "results": results,
}
BATCH_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count")}, ensure_ascii=False))
for row in results:
    print(json.dumps(row, ensure_ascii=False))
