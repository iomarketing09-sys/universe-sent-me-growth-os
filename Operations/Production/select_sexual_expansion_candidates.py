import pandas as pd
import re
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
queue = pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
prev = pd.read_csv(root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv')
prev_ids = set(prev['meta_id'].astype(str))
q = queue[~queue['meta_id'].astype(str).isin(prev_ids)].copy()
# Candidate cues only; these are not classifications.
pat = re.compile(r'\b(sexo|sexual|pene|manose|mamada|tetas|nalg|culo|calzon|cuerpo|besa|besar|beso|desnud|coger|cog|oral|masturb|eyacul|porno|placer|deseo|caliente|atracc|touch|follar|ligar|ligue|enamor|amor|pareja|privad|dos|pueblo|pueblo)\b', re.I)
q['cue'] = q['caption'].fillna('').str.contains(pat, regex=True)
sel = q[q['cue']].sort_values(['shares','interactions'], ascending=False)
out = root/'Operations/Research/2026-08-19_Ampliacion_Candidatos_Humor_Sexual.csv'
sel.to_csv(out, index=False)
print('candidates:', len(sel))
print(sel[['meta_id','publication_date_local','caption','interactions','comments','shares','status']].to_string(index=False))
