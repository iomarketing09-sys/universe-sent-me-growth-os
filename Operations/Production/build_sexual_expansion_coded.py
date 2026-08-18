import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
base=pd.read_csv(root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv')
q=pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
ids={
'1036844829507460_122127661851072582':('humor_sexual_sugerente','doble_sentido_relacion','texto sexual sugerente'),
'1036844829507460_122128989885072582':('humor_sexual_sugerente','doble_sentido_corporal','remate corporal textual'),
'1036844829507460_122130216549072582':('humor_sexual_explicito','infografia_sexual','terminología sexual explícita'),
'1036844829507460_122130232503072582':('humor_sexual_sugerente','relacional_calzones','insinuación sexual relacional'),
'1036844829507460_122134147251072582':('humor_sexual_sugerente','doble_sentido_verbal','doble sentido textual'),
}
rows=[]
for mid,(tipo,sub,desc) in ids.items():
 r=q[q.meta_id.eq(mid)].iloc[0]
 rows.append({'meta_id':mid,'fecha':r.publication_date_local,'interacciones':int(r.interactions),'comentarios':int(r.comments),'shares':int(r.shares),'tipo_humor':tipo,'subgrupo':sub,'personajes_observables':'según imagen Meta','descripcion_humor':desc,'evidencia':'Meta image reviewed'})
new=pd.DataFrame(rows)
all_df=pd.concat([base, new], ignore_index=True).drop_duplicates('meta_id')
all_df.to_csv(root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Ampliado_Codificado.csv',index=False)
summary=all_df[all_df.tipo_humor.str.startswith('humor_sexual')].groupby(['tipo_humor'],as_index=False).agg(n=('meta_id','size'),mediana_interacciones=('interacciones','median'),mediana_comentarios=('comentarios','median'),mediana_shares=('shares','median'),total_interacciones=('interacciones','sum'),total_shares=('shares','sum'))
summary['veredicto']=summary.n.apply(lambda n:'exploratoria' if n>=4 else 'inconclusa')
summary.to_csv(root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Ampliado_Resumen.csv',index=False)
print(summary.to_string(index=False))
print(new[['meta_id','tipo_humor','subgrupo','interacciones','comentarios','shares']].to_string(index=False))
