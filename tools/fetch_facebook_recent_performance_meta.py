#!/usr/bin/env python3
"""Read recent Facebook Page post performance from Meta Graph API."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

GRAPH = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Operations/Research/2026-08-23_Facebook_Performance_Meta_API.json"
POST_LIMIT = 20
INSIGHT_METRICS = [
    "post_impressions",
    "post_impressions_unique",
    "post_engaged_users",
    "post_clicks",
    "post_reactions_by_type_total",
    "post_video_views",
    "post_video_avg_time_watched",
]
PAGE_METRICS = [
    "page_impressions",
    "page_impressions_unique",
    "page_engaged_users",
    "page_post_engagements",
    "page_actions_post_reactions_total",
    "page_actions_post_comments",
    "page_actions_post_shares",
]


def request(session, method, path, token, params=None):
    response = session.request(
        method,
        f"{GRAPH}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {token}"},
        params=params or {},
        timeout=45,
    )
    try:
        payload = response.json()
    except Exception:
        payload = {"error": {"message": response.text[:1000]}}
    return response, payload


def latest_value(insight):
    values = insight.get("values") or []
    if not values:
        return None
    value = values[-1].get("value")
    return value


def read_metric(session, token, object_id, metric, period=None, since=None, until=None):
    params = {"metric": metric}
    if period:
        params["period"] = period
    if since is not None:
        params["since"] = str(since)
    if until is not None:
        params["until"] = str(until)
    response, payload = request(session, "GET", f"{object_id}/insights", token, params)
    if response.status_code >= 400 or "error" in payload:
        return {"metric": metric, "status_code": response.status_code, "error": payload.get("error", payload)}
    data = payload.get("data") or []
    if not data:
        return {"metric": metric, "status_code": response.status_code, "value": None, "raw": []}
    item = data[0]
    return {
        "metric": metric,
        "status_code": response.status_code,
        "name": item.get("name"),
        "period": item.get("period"),
        "values": item.get("values") or [],
        "value": latest_value(item),
    }


user_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
if not user_token:
    raise SystemExit("META_PAGE_ACCESS_TOKEN is not set")
session = requests.Session()
accounts_response, accounts = request(session, "GET", "me/accounts", user_token, {"fields": "id,name,access_token,tasks", "limit": 100})
if accounts_response.status_code >= 400:
    raise SystemExit(json.dumps(accounts, ensure_ascii=False))
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID and item.get("name") == "Universe Sent Me"), None)
if not page or not page.get("access_token"):
    raise SystemExit("Page token not found")
page_token = page["access_token"]

post_params = {
    "fields": "id,created_time,message,permalink_url,reactions.limit(0).summary(true),comments.limit(0).summary(true),shares,attachments.limit(10){media_type,type,url}",
    "limit": POST_LIMIT,
}
posts_response, posts_payload = request(session, "GET", f"{PAGE_ID}/posts", page_token, post_params)
if posts_response.status_code >= 400 or "error" in posts_payload:
    raise SystemExit(json.dumps(posts_payload, ensure_ascii=False))

retrieved_at = datetime.now(timezone.utc).isoformat()
post_records = []
for post in posts_payload.get("data", []):
    reactions = ((post.get("reactions") or {}).get("summary") or {}).get("total_count")
    comments = ((post.get("comments") or {}).get("summary") or {}).get("total_count")
    shares = (post.get("shares") or {}).get("count")
    attachments = (post.get("attachments") or {}).get("data") or []
    content_types = sorted({a.get("media_type") or a.get("type") for a in attachments if a.get("media_type") or a.get("type")})
    insights = {}
    for metric in INSIGHT_METRICS:
        insights[metric] = read_metric(session, page_token, post.get("id"), metric)
    record = {
        "id": post.get("id"),
        "created_time": post.get("created_time"),
        "message": post.get("message") or "",
        "permalink_url": post.get("permalink_url"),
        "content_types": content_types,
        "reactions": reactions,
        "comments": comments,
        "shares": shares,
        "engagement_public": sum(x or 0 for x in [reactions, comments, shares]),
        "insights": insights,
        "retrieved_at": retrieved_at,
    }
    post_records.append(record)

# Aggregate daily Page insights over the last 8 calendar days, if the account exposes them.
since = int(datetime(2026, 8, 16, tzinfo=timezone.utc).timestamp())
until = int(datetime(2026, 8, 24, tzinfo=timezone.utc).timestamp())
page_insights = {}
for metric in PAGE_METRICS:
    page_insights[metric] = read_metric(session, page_token, PAGE_ID, metric, period="day", since=since, until=until)

output = {
    "title": "Facebook recent performance — Meta Graph API read-only snapshot",
    "purpose": "Recent Page post engagement and exposed per-post/Page insight metrics for Growth OS review.",
    "status": "Active",
    "created_at": retrieved_at[:10],
    "last_updated": retrieved_at[:10],
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "GrowthOS/Integracion_Growth_OS.md",
        "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md",
        "Operations/Research/2026-08-22_Analisis_Semanal_20260816_20260822.md",
        "Operations/Research/2026-08-15_Publication_Log.csv",
        "Operations/Research/2026-08-15_ExperimentLog.csv",
    ],
    "source": "Meta Graph API v26.0",
    "page_id": PAGE_ID,
    "account_name": "Universe Sent Me",
    "retrieved_at": retrieved_at,
    "posts_requested": POST_LIMIT,
    "posts_returned": len(post_records),
    "insight_metrics_requested": INSIGHT_METRICS,
    "page_insight_window": {"since": "2026-08-16", "until_exclusive": "2026-08-24", "period": "day"},
    "page_insights": page_insights,
    "posts": post_records,
}
OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "retrieved_at": retrieved_at,
    "posts_returned": len(post_records),
    "post_ids": [p["id"] for p in post_records],
    "page_metrics_ok": [m for m, item in page_insights.items() if item.get("status_code") == 200],
    "page_metrics_errors": {m: item.get("error", {}).get("message", "") for m, item in page_insights.items() if item.get("status_code") != 200},
}, ensure_ascii=False, indent=2))
