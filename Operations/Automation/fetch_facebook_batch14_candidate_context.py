"""Read-only context fetch for selected Batch 14 review candidates."""

import json
import os
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Candidate_Context.json"
GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
TIMEOUT = 30
CANDIDATE_ROOTS = [
    "122151376011072582_1844719709832925",  # Saturno — Rafa Espino
    "122151376539072582_1448883027065510",  # sexualized growth comment
    "122151376083072582_1875655376797902",  # explicit meme interpretation
    "122151376083072582_1216558461547643",  # perrito
    "122151376011072582_4579578845653974",  # parent of direct Page mention reply
    "122151376083072582_1539874414078742",  # chiquito
    "122151376083072582_28148795568072687",  # low-signal root
    "122151376539072582_1049776371233063",  # user-user reply thread
]

base_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not base_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {base_token}"})
accounts = session.get(f"{GRAPH}/me/accounts", params={"fields": "id,access_token", "limit": 100}, timeout=TIMEOUT)
accounts.raise_for_status()
page = next((item for item in accounts.json().get("data", []) if item.get("id") == PAGE_ID), None)
if not page or not page.get("access_token"):
    raise SystemExit("PAGE_ACCESS_TOKEN_NOT_FOUND_FOR_UNIVERSE_SENT_ME")
page_token = page["access_token"]
headers = {"Authorization": f"Bearer {page_token}"}

context = []
for root_id in CANDIDATE_ROOTS:
    root_response = session.get(f"{GRAPH}/{root_id}", headers=headers, params={"fields": "id,from,message,created_time,parent,is_hidden"}, timeout=TIMEOUT)
    root_response.raise_for_status()
    root = root_response.json()
    replies_response = session.get(f"{GRAPH}/{root_id}/comments", headers=headers, params={"fields": "id,from,message,created_time,parent,is_hidden", "limit": 100}, timeout=TIMEOUT)
    replies_response.raise_for_status()
    context.append({"root": root, "replies": replies_response.json().get("data", [])})

result = {
    "title": "Facebook Batch 14 Candidate Context",
    "purpose": "Contexto de solo lectura para evaluar oportunidades antiguas detectadas en el inventario Batch 14.",
    "status": "Review",
    "created_at": "2026-08-24",
    "updated_at": "2026-08-24",
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json",
        "Operations/Research/2026-08-24_Facebook_Batch14_Current_Unanswered_Inventory.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "read_only": True,
    "root_count": len(context),
    "context": context,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"root_count": len(context), "output": str(OUT)}, ensure_ascii=False))
