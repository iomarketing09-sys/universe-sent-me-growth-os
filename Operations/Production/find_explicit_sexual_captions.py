import pandas as pd
from pathlib import Path
import re
root=Path('/home/ubuntu/universe-sent-me-growth-os')
q=pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
pat=re.compile(r'sexo|pene|manose|calzon|tetas|culo|nalg|masturb|oral|eyacul|mamada|chup|desnud|coger|cogeme|penetr|orgia|porno|beso|besar|cuerpo',re.I)
sel=q[q.caption.fillna('').str.contains(pat)].copy().sort_values(['shares','interactions'],ascending=False)
path=root/'Operations/Research/2026-08-19_Captions_Sexualidad_Explicita_Junio.csv'; sel.to_csv(path,index=False)
print(sel[['meta_id','caption','interactions','comments','shares','status']].to_string(index=False))
