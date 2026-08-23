#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESEARCH=ROOT/'Operations/Research'
TARGETS={
 '1036844829507460_122154842337072582',
 '1036844829507460_122154017667072582',
 '1036844829507460_122153750763072582',
}

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f)
        return r.fieldnames,list(r)

def dup(rows,key):
    seen={}
    for row in rows:
        value=(row.get(key) or '').strip()
        if value: seen.setdefault(value,0); seen[value]+=1
    return {k:v for k,v in seen.items() if v>1}

pub_fields,pub=read(RESEARCH/'2026-08-15_Publication_Log.csv')
exp_fields,exp=read(RESEARCH/'2026-08-15_ExperimentLog.csv')
reel_fields,reels=read(RESEARCH/'2026-08-21_Reels_Publication_Inventory.csv')

target_pub={pid:sum((row.get('Meta_Post_ID') or '').strip()==pid for row in pub) for pid in TARGETS}
target_exp={pid:sum(pid in (row.get('Meta_ID') or '').split('|') for row in exp) for pid in TARGETS}
target_reels={pid:sum((row.get('Platform_Content_ID') or '').strip()==pid for row in reels) for pid in TARGETS}
checks={
 'target_publication_log_count':target_pub,
 'target_experiment_log_count':target_exp,
 'target_reels_inventory_count':target_reels,
 'duplicate_publication_ids':dup(pub,'Publicacion_ID'),
 'duplicate_observation_ids':dup(exp,'Observacion_ID'),
 'duplicate_reel_record_ids':dup(reels,'Reel_Record_ID'),
 'experiment_24h_empty':sum(bool((row.get('Interacciones_24h') or '').strip()) for row in exp if any(pid in (row.get('Meta_ID') or '').split('|') for pid in TARGETS))==0,
 'experiment_72h_empty':sum(bool((row.get('Interacciones_72h') or '').strip()) for row in exp if any(pid in (row.get('Meta_ID') or '').split('|') for pid in TARGETS))==0,
}
valid=(all(value==1 for value in target_pub.values()) and all(value==1 for value in target_exp.values()) and all(value==1 for value in target_reels.values()) and not checks['duplicate_publication_ids'] and not checks['duplicate_observation_ids'] and not checks['duplicate_reel_record_ids'] and checks['experiment_24h_empty'] and checks['experiment_72h_empty'])
print(json.dumps({'rows':{'publication_log':len(pub),'experiment_log':len(exp),'reels_inventory':len(reels)},'checks':checks,'VALIDATION':'PASS' if valid else 'FAIL'},ensure_ascii=False,indent=2))
if not valid: raise SystemExit(1)
