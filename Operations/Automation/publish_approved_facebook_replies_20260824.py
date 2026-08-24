"""Publish two explicitly approved Facebook replies and verify each result."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_04.json"
APPROVED = [
    {
        "parent_comment_id": "122151376539072582_1033595316219697",
        "message": "Maeve no miente… solo deja que cada quien saque sus conclusiones 😹",
        "approval": "Fernando aprobó la propuesta en la conversación del 24 de agosto de 2026.",
    },
    {
        "parent_comment_id": "122151376083072582_3309129972605548",
        "message": "Jajaja, aquí cada quien interpreta a su manera 😹🙈",
        "approval": "Fernando aprobó la propuesta en la conversación del 24 de agosto de 2026.",
    },
]

user_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not user_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")


def get(path, params, token):
    response = requests.get(
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def post(path, data, token):
    response = requests.post(
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        data=data,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

accounts = get("me/accounts", {"fields": "id,name,access_token", "limit": 100}, user_token)
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND")
page_token = page["access_token"]

published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for item in APPROVED:
    parent_id = item["parent_comment_id"]
    existing = get(f"{parent_id}/comments", {"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}, page_token).get("data", [])
    exact = next((reply for reply in existing if (reply.get("from") or {}).get("id") == PAGE_ID and reply.get("message") == item["message"]), None)
    if exact:
        verify = exact
        status = "already_published"
    else:
        created = post(f"{parent_id}/comments", {"message": item["message"]}, page_token)
        reply_id = created.get("id")
        verify = get(reply_id, {"fields": "id,from,message,created_time,parent,is_hidden"}, page_token)
        status = "published"
    parent = verify.get("parent") or {}
    verified = {
        "status": status,
        "parent_comment_id": parent_id,
        "reply_id": verify.get("id"),
        "message": verify.get("message"),
        "from_id": (verify.get("from") or {}).get("id"),
        "from_name": (verify.get("from") or {}).get("name"),
        "parent_id_returned": parent.get("id"),
        "is_hidden": verify.get("is_hidden"),
        "verified": (
            (verify.get("from") or {}).get("id") == PAGE_ID
            and verify.get("message") == item["message"]
            and parent.get("id") == parent_id
            and verify.get("is_hidden") is False
        ),
        "approval": item["approval"],
    }
    results.append(verified)

payload = {
    "published_at": published_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "read_only_precheck": True,
    "explicit_user_approval": True,
    "requested_count": len(APPROVED),
    "published_count": sum(1 for row in results if row["status"] == "published"),
    "already_published_count": sum(1 for row in results if row["status"] == "already_published"),
    "verified_count": sum(1 for row in results if row["verified"]),
    "results": results,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count")}, ensure_ascii=False))
for row in results:
    print(json.dumps(row, ensure_ascii=False))
