import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
q=pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
labels={
'1036844829507460_122134136793072582':('humor_acido','relacional/antihéroe','Humano + demonio','cinismo / autodesprecio'),
'1036844829507460_122134161303072582':('humor_acido','relacional/dialogo','Universe + humano','ácido / absurdo'),
'1036844829507460_122132350563072582':('humor_acido','insulto/autodesprecio','Humano','pendejada / absurdo'),
'1036844829507460_122132375181072582':('humor_acido','observacional','Universe','social / mordaz'),
'1036844829507460_122134157199072582':('humor_acido','relacional','Universe','absurdo / existencial'),
'1036844829507460_122132371125072582':('humor_acido','observacional','Universe','ácido / social'),
'1036844829507460_122130330195072582':('humor_acido','infografia_absurda','varios personajes','absurdo / ácido'),
'1036844829507460_122126291157072582':('humor_acido','relacional','Mujer con sombrero','romántico / mordaz'),
'1036844829507460_122132711259072582':('humor_acido','autocuidado_irónico','Silvio','relacional / ácido'),
'1036844829507460_122132714559072582':('humor_acido','insulto_relacional','Humano + bruja','insulto / tarot'),
'1036844829507460_122132695779072582':('humor_acido','ansiedad_relacional','Humano + musculoso + Wilfred','ansiedad / absurdo'),
'1036844829507460_122126647605072582':('humor_acido','romantico_absurdo','Universe + humano','enamoramiento / combate'),
'1036844829507460_122126656881072582':('humor_acido','ciclos_relacionales','Humano','casi algo / enemigos'),
'1036844829507460_122131787067072582':('humor_sexual_explicito','contacto_sexual','Hada + humano','manoseo / insinuación explícita'),
'1036844829507460_122134032159072582':('humor_sexual_sugerente','cuerpo/atracción','Universe','sugerente / bienestar'),
'1036844829507460_122131071243072582':('no_clasificar','escena_de_mundo','Ensemble Universe','caption de seguidores'),
}
rows=[]
for mid,(tipo,subgrupo,chars,humor) in labels.items():
 r=q.loc[q.meta_id.eq(mid)].iloc[0]
 rows.append({'meta_id':mid,'fecha':r.publication_date_local,'interacciones':int(r.interactions),'comentarios':int(r.comments),'shares':int(r.shares),'tipo_humor':tipo,'subgrupo':subgrupo,'personajes_observables':chars,'descripcion_humor':humor,'evidencia':'Meta image reviewed'})
out=pd.DataFrame(rows)
outpath=root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Codificado.csv'; out.to_csv(outpath,index=False); print(out.to_string(index=False))
