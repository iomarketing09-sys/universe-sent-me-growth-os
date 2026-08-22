import csv,json,os,subprocess
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[2]
src=ROOT/'Operations/Research/2026-08-22_Reels_Tier2A_Visual_Review_Batch.csv'
with src.open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h))
meta={}; drive={}
for r in rows:
    meta.setdefault(r['Meta_Post_ID'],r); drive.setdefault(r['Meta_Post_ID'],r)
meta_dir=Path('/home/ubuntu/tier2a_meta_reels'); meta_dir.mkdir(exist_ok=True)
drive_dir=Path('/home/ubuntu/tier2a_drive_candidates'); drive_dir.mkdir(exist_ok=True)
BASE='https://graph.facebook.com/v26.0'; PAGE_ID='1036844829507460'; token=os.environ['META_PAGE_ACCESS_TOKEN']
a=requests.get(f'{BASE}/me/accounts',headers={'Authorization':f'Bearer {token}'},params={'fields':'id,name,access_token','limit':100},timeout=30); a.raise_for_status(); page=next(x for x in a.json()['data'] if x['id']==PAGE_ID); page_token=page['access_token']
fields='id,created_time,message,permalink_url,attachments{media_type,type,media,target}'
mr=[]
for i,r in enumerate(meta.values(),1):
    resp=requests.get(f'{BASE}/{r["Meta_Post_ID"]}',headers={'Authorization':f'Bearer {page_token}'},params={'fields':fields},timeout=40); payload=resp.json(); source=None
    for att in payload.get('attachments',{}).get('data',[]): source=(att.get('media') or {}).get('source') or source
    path=''
    if source:
        v=requests.get(source,timeout=60); v.raise_for_status(); path=str(meta_dir/f'{i:02d}_{r["Meta_Reel_ID"]}.mp4'); Path(path).write_bytes(v.content)
    mr.append({'row':r,'status_code':resp.status_code,'path':path})
dr=[]
for i,r in enumerate(drive.values(),1):
    ext='.mp4' if r['Drive_MimeType'].startswith('video/') else '.png'; out=drive_dir/f'{i:02d}_{r["Meta_Reel_ID"]}_{r["Drive_File_Name"][:50].replace("/","_")}{ext}'
    params=json.dumps({'fileId':r['Drive_File_ID'],'alt':'media'}); q=subprocess.run(['gws','drive','files','get','--params',params,'--output',str(out)],capture_output=True,text=True); dr.append({'row':r,'returncode':q.returncode,'path':str(out)})
Path('/home/ubuntu/tier2a_visual_batch_manifest.json').write_text(json.dumps({'meta':mr,'drive':dr},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'meta_selected':len(mr),'meta_downloaded':sum(bool(x['path']) for x in mr),'drive_selected':len(dr),'drive_downloaded':sum(x['returncode']==0 for x in dr),'manifest':'/home/ubuntu/tier2a_visual_batch_manifest.json'},ensure_ascii=False))
