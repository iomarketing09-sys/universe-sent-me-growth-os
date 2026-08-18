#!/usr/bin/env python3
import csv, json, os
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://graph.facebook.com/v26.0"
USER_TOKEN = os.environ["META_PAGE_ACCESS_TOKEN"]
accounts = requests.get(f"{BASE}/me/accounts", headers={"Authorization": f"Bearer {USER_TOKEN}"}, params={"fields":"id,name,access_token,tasks", "limit":100}, timeout=30)
accounts.raise_for_status()
page = next(x for x in accounts.json().get("data", []) if x.get("name") == "Universe Sent Me")
TOKEN = page["access_token"]
queue = list(csv.DictReader(open("Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv", encoding="utf-8-sig")))
unmatched = [r for r in queue if r.get("status") == "Needs_Asset_Match"]
unmatched.sort(key=lambda r: float(r.get("interactions") or 0), reverse=True)
selected = unmatched[:15]
fields = "id,created_time,message,full_picture,attachments{media_type,media{image{src,width,height}}}"
batch = [{"method":"GET","relative_url":f"{r['meta_id']}?fields={fields}"} for r in selected]
resp = requests.post(BASE, headers={"Authorization": f"Bearer {TOKEN}"}, data={"batch": json.dumps(batch)}, timeout=60)
resp.raise_for_status()
out = {"extracted_at_utc":datetime.now(timezone.utc).isoformat(),"selection_basis":"Top 15 unmatched June cases by recorded interactions; read-only.","selected_queue_rows":selected,"batch_response":resp.json()}
path=Path("Operations/Research/2026-08-18_Junio_Unmatched_Top15_Meta_Media.json")
path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"status":resp.status_code,"selected":len(selected),"output":str(path)}))
for r,item in zip(selected,out["batch_response"]): print(r.get("row_id"),r.get("meta_id"),item.get("code"))
