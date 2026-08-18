import pandas as pd
from pathlib import Path

base = Path('/home/ubuntu/universe-sent-me-growth-os')
source = base / 'Operations/Research/2026-08-18_Lote_A_Estructuras_Narrativas.csv'
out = base / 'Operations/Research/2026-08-18_Lote_A_Resumen_Comparativo.csv'
df = pd.read_csv(source)
metrics = ['interacciones','reacciones','comentarios','shares']
summary = df.groupby('grupo_comparable', as_index=False)[metrics].median()
counts = df.groupby('grupo_comparable').size().rename('n').reset_index()
summary = counts.merge(summary, on='grupo_comparable')
summary.to_csv(out, index=False)
print(summary.to_string(index=False))
print('\nAll rows:')
print(df[['meta_id','grupo_comparable','interacciones','shares']].to_string(index=False))
