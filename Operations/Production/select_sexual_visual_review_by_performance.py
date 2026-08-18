import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
q=pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
prev=pd.read_csv(root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv')
prev_ids=set(prev.meta_id.astype(str))
# Include unresolved/high-value rows not already visually coded; captions may hide sexual visual cues.
unmatched=q[q.status.eq('Needs_Asset_Match') & ~q.meta_id.astype(str).isin(prev_ids)].copy()
unmatched['score']=unmatched.interactions.fillna(0)+2*unmatched.shares.fillna(0)+3*unmatched.comments.fillna(0)
sel=unmatched.sort_values('score',ascending=False).head(20)
out=root/'Operations/Research/2026-08-19_Revision_Visual_Sexualidad_Alto_Rendimiento.csv'; sel.to_csv(out,index=False)
print('unmatched available:',len(unmatched),'selected:',len(sel))
print(sel[['meta_id','publication_date_local','caption','interactions','comments','shares']].to_string(index=False))
