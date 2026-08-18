import pandas as pd
from pathlib import Path
import re

root = Path('/home/ubuntu/universe-sent-me-growth-os')
queue = pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
prev = pd.read_csv(root/'Operations/Research/2026-08-19_Lote_Dialogo_Transformacion_Codificado.csv')
prev_ids = set(prev.meta_id)
# Keep unresolved rows only, excluding the previous batch.
df = queue[queue.status.eq('Needs_Asset_Match') & ~queue.meta_id.isin(prev_ids)].copy()
# Prioritize likely narrative/contrast cues, but retain high-performing candidates without cues for visual review.
cue = re.compile(r'\?|\bpero\b|\by\b|\bte\b|\byo\b|\bno\b|\bdos\b|\bUniverse\b|\basi\b|\ba ver\b|\bfrente\b|\bantes\b|\bdespués\b|\bconvert|\btransform|\bmuscul|\bpayaso\b', re.I)
df['cue'] = df.caption.fillna('').str.contains(cue)
df['score'] = df.interactions.fillna(0) + df.shares.fillna(0)*2 + df.comments.fillna(0)*3 + df.cue.astype(int)*20
selected = df.sort_values(['cue','score'], ascending=False).head(20)
out = root/'Operations/Research/2026-08-19_Siguiente_Lote_Candidatos_Dialogo_Transformacion.csv'
selected.to_csv(out, index=False)
print('unresolved remaining:', len(df))
print(selected[['meta_id','publication_date_local','caption','interactions','comments','shares','cue','score']].to_string(index=False))
