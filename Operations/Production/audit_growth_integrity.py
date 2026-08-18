import pandas as pd
from pathlib import Path
import json
root=Path('/home/ubuntu/universe-sent-me-growth-os')
files={
'inventory':root/'GrowthOS/Content_Inventory.csv',
'historical':root/'Operations/Research/Historical_Performance_Individuals.csv',
'publication':root/'Operations/Research/2026-08-15_Publication_Log.csv',
'experiment':root/'Operations/Research/2026-08-15_ExperimentLog.csv',
'p0baseline':root/'Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv',
'calendar':root/'Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv',
'instagram':root/'Operations/Research/2026-08-17_Instagram_IDs_Duplicaciones_Confirmadas.json',
}
out={}
for k,p in files.items():
 if p.suffix=='.csv':
  d=pd.read_csv(p)
  out[k]={'rows':len(d),'cols':list(d.columns),'duplicates_all':int(d.duplicated().sum()),'nulls':{c:int(d[c].isna().sum()) for c in d.columns if d[c].isna().any()}}
  for c in ['CNT_ID','Asset_Ref','Meta_Post_ID','meta_id','Publication_ID','Experiment_ID','status','Status','Estado','Reuse_Status','Schedule_Status']:
   if c in d.columns:
    out[k][c+'_unique']=int(d[c].nunique(dropna=True))
    out[k][c+'_blank']=int(d[c].isna().sum())
 else:
  data=json.loads(p.read_text())
  out[k]={'json_type':type(data).__name__,'items':len(data) if isinstance(data,list) else len(data.keys()) if isinstance(data,dict) else None}
print(json.dumps(out,ensure_ascii=False,indent=2))
