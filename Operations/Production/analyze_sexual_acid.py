import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
df=pd.read_csv(root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv')
use=df[df.tipo_humor.ne('no_clasificar')]
summary=use.groupby('tipo_humor',as_index=False).agg(n=('meta_id','size'),mediana_interacciones=('interacciones','median'),mediana_comentarios=('comentarios','median'),mediana_shares=('shares','median'),total_interacciones=('interacciones','sum'),total_shares=('shares','sum'))
summary['veredicto']=summary.apply(lambda r:'inconclusa_muestra_pequena' if r.n<5 else 'exploratoria',axis=1)
out=root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Resumen.csv'; summary.to_csv(out,index=False); print(summary.to_string(index=False))
