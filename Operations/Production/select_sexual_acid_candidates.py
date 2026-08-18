import pandas as pd
import re
from pathlib import Path

root=Path('/home/ubuntu/universe-sent-me-growth-os')
q=pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
prev_ids=set()
for p in [root/'Operations/Research/2026-08-19_Lote_Dialogo_Transformacion_Codificado.csv', root/'Operations/Research/2026-08-19_Siguiente_Lote_Dialogo_Transformacion_Codificado.csv']:
    if p.exists(): prev_ids.update(pd.read_csv(p).meta_id.dropna())
df=q[~q.meta_id.isin(prev_ids)].copy()
sexual=re.compile(r'pene|sexo|sexual|calzon|besa|besar|amor|ligue|ligar|privad|dos|nalg|cuerpo|tetas|oral|masturb|eyacul|susurr|enamor|pareja|atracci|deseo|gusta',re.I)
acid=re.compile(r'pendej|vrg|ching|payaso|loco|ácido|acido|dislexia|malo|paz mental|psicolog|flojera|ridicul|mierd|no corras|desapende|oscuro|estoico|villano|batallar',re.I)
df['sexual_cue']=df.caption.fillna('').str.contains(sexual)
df['acid_cue']=df.caption.fillna('').str.contains(acid)
df['candidate_type']=df.apply(lambda r: 'sexual' if r.sexual_cue and not r.acid_cue else ('acid' if r.acid_cue and not r.sexual_cue else ('mixed' if r.sexual_cue and r.acid_cue else 'other')),axis=1)
df['score']=df.interactions.fillna(0)+2*df.shares.fillna(0)+3*df.comments.fillna(0)+30*(df.candidate_type!='other')
sel=df[df.candidate_type!='other'].sort_values(['candidate_type','score'],ascending=[True,False])
out=root/'Operations/Research/2026-08-19_Candidatos_Humor_Sexual_Acido.csv'; sel.to_csv(out,index=False)
print('candidates',len(sel))
print(sel[['meta_id','publication_date_local','caption','interactions','comments','shares','candidate_type','score']].head(40).to_string(index=False))
