import pandas as pd
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
q=pd.read_csv(root/'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
classes={
'1036844829507460_122125547121072582':('metafora_visual_caption','Flor rompe piedra','Sin personaje','Metáfora / crecimiento'),
'1036844829507460_122130309663072582':('personaje_caption','Wilfred con remate','Wilfred visualmente compatible','Humor seco'),
'1036844829507460_122134060641072582':('escena_personaje_caption','Humano en mundo fantástico','Humano no identificado','Ácido / motivacional'),
'1036844829507460_122126267355072582':('personaje_caption','Wilfred con remate','Wilfred visualmente compatible','Ácido / literal'),
'1036844829507460_122126305443072582':('escena_relacional_caption','Dúo en nubes','Humanos no identificados','Relatable / afectivo'),
'1036844829507460_122134147251072582':('texto_composicion_mundo','Texto sobre nubes','Ninguno visible','Relatable / ácido'),
'1036844829507460_122125528653072582':('texto_sobre_fotografia','Fotografía de arroyo','Ninguno visible','Ácido'),
'1036844829507460_122130216549072582':('infografia_composicion','Guía de emojis','Ninguno visible','Sexual / informativo'),
'1036844829507460_122130232503072582':('escena_relacional_globo','Dúo con globo único','Hombre + hada visualmente compatible','Relatable / sexual'),
'1036844829507460_122134608507072582':('transformacion_vestuario','Ganso siendo vestido','Ganso visualmente compatible','Absurdista / social'),
'1036844829507460_122128512777072582':('texto_sobre_fotografia','Consejo sobre cielo','Ninguno visible','Ácido'),
'1036844829507460_122127661851072582':('texto_sobre_fotografia','Texto sobre carretera','Ninguno visible','Sexual'),
'1036844829507460_122125544019072582':('personaje_caption','Wilfred con hechizo','Wilfred visualmente compatible','Ácido / fantástico'),
'1036844829507460_122129015739072582':('texto_sobre_fotografia','Tres bloques sobre calle','Ninguno visible','Relatable / social'),
'1036844829507460_122127916017072582':('composicion_mundo','Cartel espiritual','Hada + Wilfred + tarot','Esotérico / comunitario'),
}
rows=[]
for mid,(structure,subgroup,chars,humor) in classes.items():
 r=q.loc[q.meta_id.eq(mid)].iloc[0]
 rows.append({'meta_id':mid,'fecha':r.publication_date_local,'interacciones':int(r.interactions),'comentarios':int(r.comments),'shares':int(r.shares),'estructura_narrativa':structure,'subgrupo':subgroup,'personajes_observables':chars,'tipo_humor':humor,'evidencia_visual':'Meta image reviewed'})
out=pd.DataFrame(rows)
outpath=root/'Operations/Research/2026-08-19_Siguiente_Lote_Dialogo_Transformacion_Codificado.csv'
out.to_csv(outpath,index=False)
print(out.to_string(index=False))
