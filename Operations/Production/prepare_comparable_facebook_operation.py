from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

BASE = "https://graph.facebook.com"
API_VERSION = "v26.0"
PAGE_ID = "1036844829507460"
TIMEZONE = ZoneInfo("America/Matamoros")
STAGING = Path("Operations/Research/2026-08-21_Comparable_Experiment_Publication_Staging.csv")
PUBLICATION_LOG = Path("Operations/Research/2026-08-15_Publication_Log.csv")

TOKEN = os.environ["META_PAGE_ACCESS_TOKEN"]
headers = {"Authorization": f"Bearer {TOKEN}"}

def get(path: str, params: dict | None = None) -> dict:
    response = requests.get(f"{BASE}/{API_VERSION}/{path}", headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

identity = get("me", {"fields": "id,name"})
accounts = get("me/accounts", {"fields": "id,name,tasks"})
page = next((item for item in accounts.get("data", []) if item.get("id") == PAGE_ID or item.get("name") == "Universe Sent Me"), None)
if not page:
    raise RuntimeError("Universe Sent Me Page was not found in /me/accounts")

with STAGING.open(encoding="utf-8-sig", newline="") as handle:
    staging_rows = list(csv.DictReader(handle))
assert len(staging_rows) == 3
assert all(row["Meta_Action"] == "Not_Executed" for row in staging_rows)
assert all(row["CNT_Status"] == "Not_Created" for row in staging_rows)
assert all(row["Affiliate_Attachment"] == "No" for row in staging_rows)

old_assets = {row["Original_Slot_Asset"] for row in staging_rows}
with PUBLICATION_LOG.open(encoding="utf-8-sig", newline="") as handle:
    publication_rows = list(csv.DictReader(handle))

old_rows = []
for row in publication_rows:
    if row.get("Asset_Ref") in old_assets and row.get("Plataforma") == "Facebook":
        key = (row.get("Fecha_Planeada_Local"), row.get("Hora_Planeada_Local"))
        if key in {(item["Fecha_Planeada_Local"], item["Hora_Planeada_Local"]) for item in staging_rows}:
            old_rows.append(row)

if len(old_rows) != 3:
    raise RuntimeError(f"Expected 3 old Facebook schedule rows, found {len(old_rows)}")

prepared = []
for row in staging_rows:
    local_dt = datetime.fromisoformat(f"{row['Fecha_Planeada_Local']}T{row['Hora_Planeada_Local']}:00").replace(tzinfo=TIMEZONE)
    old = next(item for item in old_rows if item["Fecha_Planeada_Local"] == row["Fecha_Planeada_Local"] and item["Hora_Planeada_Local"] == row["Hora_Planeada_Local"])
    prepared.append({
        "brief_id": row["Brief_ID"],
        "hypothesis_id": row["Hypothesis_ID"],
        "asset_ref": row["Asset_Ref"],
        "caption": row["Caption_Propuesto"],
        "date_local": row["Fecha_Planeada_Local"],
        "time_local": row["Hora_Planeada_Local"],
        "timezone": "America/Matamoros",
        "scheduled_publish_time": int(local_dt.timestamp()),
        "old_asset": row["Original_Slot_Asset"],
        "old_meta_post_id": old.get("Meta_Post_ID"),
        "old_meta_photo_id": old.get("Meta_Photo_ID"),
    })

print(json.dumps({
    "user_identity": identity,
    "page": {"id": page.get("id"), "name": page.get("name"), "tasks": page.get("tasks")},
    "prepared": prepared,
    "authorization_scope": "cancel_old_schedule_then_schedule_and_publish_facebook_only",
    "instagram": "excluded",
    "cnt": "excluded",
    "affiliates": "excluded",
}, ensure_ascii=False, indent=2))
