import csv
import json
import os
import subprocess
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
next_path = ROOT / 'Operations/Research/2026-08-22_Reels_Next10_Visual_Review_Batch.csv'
with next_path.open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle))
meta_unique = {}
for row in rows:
    meta_unique.setdefault(row['Meta_Post_ID'], row)
meta_rows = list(meta_unique.values())
drive_top = {}
for row in rows:
    drive_top.setdefault(row['Meta_Post_ID'], row)

meta_dir = Path('/home/ubuntu/next10_meta_reels'); meta_dir.mkdir(exist_ok=True)
drive_dir = Path('/home/ubuntu/next10_drive_candidates'); drive_dir.mkdir(exist_ok=True)
BASE='https://graph.facebook.com/v26.0'; PAGE_ID='1036844829507460'; token=os.environ['META_PAGE_ACCESS_TOKEN']
accounts=requests.get(f'{BASE}/me/accounts',headers={'Authorization':f'Bearer {token}'},params={'fields':'id,name,access_token','limit':100},timeout=30); accounts.raise_for_status(); page=next(x for x in accounts.json()['data'] if x['id']==PAGE_ID); page_token=page['access_token']
fields='id,created_time,message,permalink_url,attachments{media_type,type,media,target}'
meta_results=[]
for idx,row in enumerate(meta_rows,1):
    resp=requests.get(f'{BASE}/{row["Meta_Post_ID"]}',headers={'Authorization':f'Bearer {page_token}'},params={'fields':fields},timeout=40); payload=resp.json(); source=None
    for a in payload.get('attachments',{}).get('data',[]): source=(a.get('media') or {}).get('source') or source
    path=''
    if source:
        r=requests.get(source,timeout=60); r.raise_for_status(); path=str(meta_dir/f'{idx:02d}_{row["Meta_Reel_ID"]}.mp4'); Path(path).write_bytes(r.content)
    meta_results.append({'rank':idx,'row':row,'status_code':resp.status_code,'path':path})

drive_results=[]
for idx,row in enumerate(drive_top.values(),1):
    ext='.mp4' if row['Drive_MimeType'].startswith('video/') else '.png'; path=drive_dir/f'{idx:02d}_{row["Meta_Reel_ID"]}_{row["Drive_File_Name"][:50].replace("/","_")}{ext}'
    params=json.dumps({'fileId':row['Drive_File_ID'],'alt':'media'}); r=subprocess.run(['gws','drive','files','get','--params',params,'--output',str(path)],capture_output=True,text=True)
    drive_results.append({'rank':idx,'row':row,'returncode':r.returncode,'path':str(path)})
Path('/home/ubuntu/next10_visual_batch_manifest.json').write_text(json.dumps({'meta':meta_results,'drive':drive_results},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'meta_selected':len(meta_rows),'meta_downloaded':sum(bool(x['path']) for x in meta_results),'drive_selected':len(drive_results),'drive_downloaded':sum(x['returncode']==0 for x in drive_results),'manifest':'/home/ubuntu/next10_visual_batch_manifest.json'},ensure_ascii=False))
