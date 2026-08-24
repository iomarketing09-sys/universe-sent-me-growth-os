"""Read-only diagnostic for the five approved music comment IDs."""

import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
POST_ID = "1036844829507460_122151376083072582"
TARGETS = {
    "122151376011072582_1720626909225543": "Unstoppable",
    "122151376011072582_1703056380925949": "El día que volviste a la tierra - Carlos Sadness",
    "122151376011072582_2110248423207879": "Con migo danza el que ama mí Alma",
    "122151376011072582_1622582352867257": "alguien como tú - Josean log",
    "122151376011072582_2033022903995271": "Las cuatro estaciones, Antonio Vivaldi.",
}
base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

def get(path, token, params):
    response = requests.get(f"{GRAPH}/{path.lstrip('/')}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=30)
    return {"status": response.status_code, "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text[:500]}

accounts = get("me/accounts", base_token, {"fields": "id,name,access_token", "limit": 100})
page = next(item for item in accounts["body"].get("data", []) if item.get("id") == PAGE_ID)
page_token = page["access_token"]
fields = "id,from,message,created_time,parent,is_hidden"
post_comments = get(f"{POST_ID}/comments", page_token, {"fields": fields, "limit": 100})
print(json.dumps({"post_comments_status": post_comments["status"], "post_comment_count": len(post_comments["body"].get("data", []))}, ensure_ascii=False))
current = {item.get("id"): item for item in post_comments["body"].get("data", [])}
for comment_id, expected in TARGETS.items():
    direct = get(comment_id, page_token, {"fields": fields})
    matches = [item for item in current.values() if (item.get("message") or "").strip().lower() == expected.strip().lower()]
    print(json.dumps({
        "target_id": comment_id,
        "expected": expected,
        "direct_get_status": direct["status"],
        "direct_get_body": direct["body"] if direct["status"] != 200 else {"id": direct["body"].get("id"), "message": direct["body"].get("message"), "created_time": direct["body"].get("created_time")},
        "fresh_root_matches": [{"id": item.get("id"), "message": item.get("message"), "created_time": item.get("created_time")} for item in matches],
    }, ensure_ascii=False))
