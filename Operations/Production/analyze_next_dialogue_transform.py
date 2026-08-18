import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
df=pd.read_csv(root/'Operations/Research/2026-08-19_Siguiente_Lote_Dialogo_Transformacion_Codificado.csv')
summary=df.groupby('estructura_narrativa',as_index=False).agg(n=('meta_id','size'),mediana_interacciones=('interacciones','median'),mediana_comentarios=('comentarios','median'),mediana_shares=('shares','median'))
summary['veredicto']=summary.apply(lambda r: 'inconclusa' if r.n<3 else 'exploratoria',axis=1)
out=root/'Operations/Research/2026-08-19_Siguiente_Lote_Dialogo_Transformacion_Resumen.csv'; summary.to_csv(out,index=False)
print(summary.to_string(index=False))
