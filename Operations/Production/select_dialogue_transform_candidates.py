import pandas as pd
from pathlib import Path

base = Path('/home/ubuntu/universe-sent-me-growth-os')
path = base / 'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv'
df = pd.read_csv(path)
# Only unresolved rows; use captions as a first-pass selector, not as visual truth.
unmatched = df[df['status'].eq('Needs_Asset_Match')].copy()
keywords = r'\?|\bpero\b|\by\b|\bte\b|\byo\b|\bsi\b|\bno\b|\bUniverse\b|\bligue|extrañ|esperando|dijo|dice|conmigo|a ver|dos|tres'
mask = unmatched['caption'].fillna('').str.contains(keywords, case=False, regex=True)
selected = unmatched[mask].copy().sort_values(['shares','interactions'], ascending=False)
print('unmatched total:', len(unmatched))
print('selected candidates:', len(selected))
print(selected[['priority_rank','meta_id','publication_date_local','caption','interactions','comments','shares']].head(40).to_string(index=False))
