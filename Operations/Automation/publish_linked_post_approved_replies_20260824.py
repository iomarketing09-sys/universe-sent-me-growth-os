"""Publish the nine explicitly approved replies for the linked Facebook post."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
PROPOSALS_FILE = ROOT / "Operations/Research/2026-08-24_Facebook_Linked_Post_Reply_Proposals.json"
BATCH_FILE = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_05.json"

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

proposal_payload = json.loads(PROPOSALS_FILE.read_text(encoding="utf-8"))
proposals = proposal_payload.get("proposals", [])
if len(proposals) != 9:
    raise SystemExit(f"EXPECTED_9_PROPOSALS_GOT_{len(proposals)}")

published_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
results = []
for proposal in proposals:
    parent_id = proposal["comment_id"]
    message = proposal["suggested_reply"]
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
        results.append({
            "status": "blocked_existing_page_reply",
            "parent_comment_id": parent_id,
            "message": message,
            "existing_page_reply_ids": [child.get("id") for child in other_page_replies],
            "verified": False,
        })
        continue
    else:
        created = request("POST", f"{parent_id}/comments", page_token, data={"message": message})
        reply_id = created.get("id")
        verified = request(
            "GET",
            reply_id,
            page_token,
            params={"fields": "id,from,message,created_time,parent,is_hidden"},
        )
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

if any(not row.get("verified") for row in results):
    raise SystemExit(json.dumps({"publication_verification_failed": results}, ensure_ascii=False))

payload = {
    "published_at": published_at,
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "post_id": proposal_payload.get("post_id"),
    "explicit_user_approval": True,
    "requested_count": len(proposals),
    "published_count": sum(1 for row in results if row["status"] == "published"),
    "already_published_count": sum(1 for row in results if row["status"] == "already_published"),
    "verified_count": sum(1 for row in results if row["verified"]),
    "results": results,
}
BATCH_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Keep the proposal artifact synchronized with the verified publication outcome.
by_id = {row["parent_comment_id"]: row for row in results}
for proposal in proposals:
    result = by_id[proposal["comment_id"]]
    proposal["status"] = "Respondido"
    proposal["published"] = True
    proposal["published_at"] = published_at
    proposal["reply_id"] = result["reply_id"]
proposal_payload["updated_at"] = published_at
proposal_payload["no_publication_performed"] = False
proposal_payload["publication_batch"] = BATCH_FILE.name
PROPOSALS_FILE.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps({key: payload[key] for key in ("requested_count", "published_count", "already_published_count", "verified_count")}, ensure_ascii=False))
for row in results:
    print(json.dumps(row, ensure_ascii=False))
