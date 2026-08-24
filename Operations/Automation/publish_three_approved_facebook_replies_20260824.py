"""Publish three newly approved Facebook replies and verify each result."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
PROPOSALS_FILE = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Proposals.json"
BATCH_FILE = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_06.json"
TARGETS = [
    {
        "parent_comment_id": "122151376083072582_1747280716505079",
        "message": "Jajaja, ese papucho claramente no se puede quejar. 😂🙈",
    },
    {
        "parent_comment_id": "122151376083072582_1694103262232576",
        "message": "Jajaja, la imaginación ya hizo todo el trabajo por ti. 😂🙈",
    },
    {
        "parent_comment_id": "122151376083072582_1435662098773431",
        "message": "El universo ya tiene demasiadas especies involucradas en esto. 😂",
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
    response.raise_for_status()
    return response.json()

accounts = request("GET", "me/accounts", base_token, params={"fields": "id,name,access_token", "limit": 100})
page = next((row for row in accounts.get("data", []) if row.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND")
page_token = page["access_token"]

published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for target in TARGETS:
    parent_id = target["parent_comment_id"]
    message = target["message"]
    children = request(
        "GET",
        f"{parent_id}/comments",
        page_token,
        params={"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100},
    ).get("data", [])
    exact = next(
        (child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") == message),
        None,
    )
    other_page_replies = [child for child in children if (child.get("from") or {}).get("id") == PAGE_ID and child.get("message") != message]
    if exact:
        verified = exact
        status = "already_published"
    elif other_page_replies:
        raise SystemExit(json.dumps({
            "blocked_existing_page_reply": parent_id,
            "existing_page_reply_ids": [child.get("id") for child in other_page_replies],
        }, ensure_ascii=False))
    else:
        created = request("POST", f"{parent_id}/comments", page_token, data={"message": message})
        reply_id = created.get("id")
        verified = request("GET", reply_id, page_token, params={"fields": "id,from,message,created_time,parent,is_hidden"})
        status = "published"
    parent = verified.get("parent") or {}
    row = {
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
    results.append(row)

if any(not row["verified"] for row in results):
    raise SystemExit(json.dumps({"verification_failed": results}, ensure_ascii=False))

payload = {
    "published_at": published_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "post_id": "1036844829507460_122151376083072582",
    "explicit_user_approval": True,
    "requested_count": len(TARGETS),
    "published_count": sum(1 for row in results if row["status"] == "published"),
    "already_published_count": sum(1 for row in results if row["status"] == "already_published"),
    "verified_count": sum(1 for row in results if row["verified"]),
    "results": results,
}
BATCH_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

proposal_payload = json.loads(PROPOSALS_FILE.read_text(encoding="utf-8"))
for row in proposal_payload.get("safety_and_low_signal_proposals", []):
    result = next((item for item in results if item["parent_comment_id"] == row.get("comment_id")), None)
    if not result:
        continue
    row["suggested_reply"] = result["message"]
    row["status"] = "Respondido"
    row["approval_status"] = "Aprobada"
    row["published"] = True
    row["published_at"] = published_at
    row["reply_id"] = result["reply_id"]
proposal_payload["updated_at"] = published_at
proposal_payload["new_proposals_published"] = False
proposal_payload["publication_batch_06"] = BATCH_FILE.name
PROPOSALS_FILE.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count")}, ensure_ascii=False))
for row in results:
    print(json.dumps(row, ensure_ascii=False))
