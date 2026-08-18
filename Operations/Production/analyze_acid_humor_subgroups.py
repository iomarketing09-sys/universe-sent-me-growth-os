import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
src=root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv'
df=pd.read_csv(src)
df=df[df.tipo_humor.eq('humor_acido')].copy()
df['interacciones']=pd.to_numeric(df.interacciones)
df['shares']=pd.to_numeric(df.shares)
df['comentarios']=pd.to_numeric(df.comentarios)
q1=df.interacciones.quantile(.25); q3=df.interacciones.quantile(.75); iqr=q3-q1
# Outlier convention: above Q3 + 1.5 IQR, reported transparently.
df['outlier_interacciones']=df.interacciones.gt(q3+1.5*iqr)
summary=df.groupby('subgrupo',as_index=False).agg(n=('meta_id','size'),mediana_interacciones=('interacciones','median'),media_interacciones=('interacciones','mean'),mediana_shares=('shares','median'),media_shares=('shares','mean'),mediana_comentarios=('comentarios','median'),total_interacciones=('interacciones','sum'))
summary=summary.sort_values(['mediana_interacciones','n'],ascending=[False,False])
summary.to_csv(root/'Operations/Research/2026-08-19_Humor_Acido_Subgrupos_Resumen.csv',index=False)
df.sort_values('interacciones',ascending=False).to_csv(root/'Operations/Research/2026-08-19_Humor_Acido_Subgrupos_Codificado.csv',index=False)
print('overall',len(df),'median',df.interacciones.median(),'mean',df.interacciones.mean(),'q1',q1,'q3',q3,'upper_fence',q3+1.5*iqr)
print(summary.to_string(index=False))
print('\nOutliers:')
print(df[df.outlier_interacciones][['meta_id','subgrupo','interacciones','shares','descripcion_humor']].to_string(index=False))
