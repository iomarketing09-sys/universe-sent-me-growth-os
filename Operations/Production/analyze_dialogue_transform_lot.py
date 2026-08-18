import pandas as pd
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
src = root / 'Operations/Research/2026-08-19_Lote_Dialogo_Transformacion_Codificado.csv'
df = pd.read_csv(src)
metrics = ['interacciones', 'comentarios', 'shares']
summary = df.groupby('estructura_narrativa', as_index=False)[metrics].median()
counts = df.groupby('estructura_narrativa').size().rename('n').reset_index()
summary = counts.merge(summary, on='estructura_narrativa')
summary['comparabilidad'] = summary.apply(lambda r: 'inconclusa_n<3' if r['n'] < 3 else 'exploratoria', axis=1)
out = root / 'Operations/Research/2026-08-19_Lote_Dialogo_Transformacion_Resumen.csv'
summary.to_csv(out, index=False)
print(summary.to_string(index=False))
