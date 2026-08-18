import pandas as pd
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
queue = pd.read_csv(root / 'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv')
classifications = {
    '1036844829507460_122130196011072582': ('transformacion_visual', 'Transformación Universe explícita', 'Universe', 'Absurdo / relatable', 'Alta'),
    '1036844829507460_122129404893072582': ('dialogo_secuencial', 'Microhistoria de tres paneles', 'Hombre + hada visualmente compatible', 'Literalidad / absurdo romántico', 'Alta'),
    '1036844829507460_122129952933072582': ('escena_relacional_caption', 'Dúo con caption único', 'Dos humanos no identificados', 'Relatable / observacional', 'Alta'),
    '1036844829507460_122125520661072582': ('escena_personaje_caption', 'Universe en escena con caption', 'Universe', 'Relatable / espera', 'Alta'),
    '1036844829507460_122127189117072582': ('texto_sobre_fotografia', 'Texto sobre cielo real', 'Ninguno visible', 'Observacional / sexual', 'Alta'),
    '1036844829507460_122133424479072582': ('personaje_caption', 'Personaje con remate textual', 'Silvio visualmente compatible', 'Romántico / absurdo', 'Alta'),
    '1036844829507460_122134055109072582': ('escena_personaje_caption', 'Personaje en mundo astrológico', 'Mujer no identificada', 'Esotérico / reflexivo', 'Alta'),
    '1036844829507460_122130324285072582': ('transformacion_visual', 'Transformación de material/escena', 'Universe', 'Absurdo visual', 'Alta'),
    '1036844829507460_122130032151072582': ('dialogo_implicito', 'Dos líneas de remate en personaje', 'Wilfred visualmente compatible', 'Humor seco / absurdo', 'Alta'),
    '1036844829507460_122125894767072582': ('escena_relacional_caption', 'Dúo relacional con cinta', 'Dos humanos no identificados', 'Relatable / afectivo', 'Alta'),
    '1036844829507460_122126265063072582': ('metafora_visual_caption', 'Metáfora visual con caption', 'Hombre no identificado', 'Romántico / visual', 'Alta'),
    '1036844829507460_122126653755072582': ('escena_relacional_caption', 'Pareja fantástica con remate', 'Dos humanos no identificados', 'Romántico / posesivo', 'Alta'),
}
rows = []
for meta_id, (estructura, subgrupo, personajes, humor, confianza) in classifications.items():
    r = queue.loc[queue['meta_id'].eq(meta_id)].iloc[0].to_dict()
    rows.append({
        'meta_id': meta_id,
        'fecha': r['publication_date_local'],
        'interacciones': int(r['interactions']),
        'reacciones': int(r['reactions']),
        'comentarios': int(r['comments']),
        'shares': int(r['shares']),
        'estructura_narrativa': estructura,
        'subgrupo': subgrupo,
        'personajes_observables': personajes,
        'tipo_humor': humor,
        'nivel_confianza_visual': confianza,
        'asset_ref_conocido': r.get('asset_ref_known', ''),
    })
out = pd.DataFrame(rows).sort_values(['estructura_narrativa', 'interacciones'], ascending=[True, False])
out_path = root / 'Operations/Research/2026-08-19_Lote_Dialogo_Transformacion_Codificado.csv'
out.to_csv(out_path, index=False)
print(out.to_string(index=False))
