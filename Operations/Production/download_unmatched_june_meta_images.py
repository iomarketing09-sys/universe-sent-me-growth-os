#!/usr/bin/env python3
import json
from pathlib import Path
import requests

src=Path("Operations/Research/2026-08-18_Junio_Unmatched_Top15_Meta_Media.json")
out=Path("Operations/Research/June_Unmatched_Top15_Meta_Images")
out.mkdir(exist_ok=True)
d=json.loads(src.read_text(encoding="utf-8"))
for row,item in zip(d["selected_queue_rows"],d["batch_response"]):
    pid=row["meta_id"]
    body=json.loads(item.get("body","{}"))
    url=body.get("full_picture")
    if not url:
        try:
            url=body["attachments"]["data"][0]["media"]["image"]["src"]
        except Exception:
            url=None
    if not url:
        print('no image',pid); continue
    r=requests.get(url,timeout=45)
    r.raise_for_status()
    target=out/f"{pid.replace('/','_')}.jpg"
    target.write_bytes(r.content)
    print(pid,target,len(r.content))
print('done')
