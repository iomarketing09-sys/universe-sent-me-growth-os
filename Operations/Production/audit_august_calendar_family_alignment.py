from pathlib import Path
import csv, json, re
from collections import Counter, defaultdict

root = Path('/home/ubuntu/universe-sent-me-growth-os')
cal = root / 'Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv'
out = root / 'Operations/Research/2026-08-20_Auditoria_Alineacion_Calendario_17_30_Familias.json'

with cal.open(newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

issues = []
clean = []
for idx, r in enumerate(rows, start=2):
    if not r.get('Fecha') or not r.get('Hora') or not r.get('Archivo'):
        issues.append({'line': idx, 'type': 'missing_core_field', 'row': r})
        continue
    clean.append(r)


def classify(r):
    text = ' '.join([r.get('Archivo',''), r.get('Contexto_Nota',''), r.get('Caption_Propuesto','')]).lower()
    reuse = r.get('Tipo_Contenido','') in {'Reuse_Top', 'Reuse_Reserve'}
    if reuse:
        return 'REUSE_NOT_EXPERIMENTAL'
    if 'pregunta' in text or 'convers' in text or 'beso' in text or 'amor' in text or 'romance' in text or '+' in r.get('Archivo',''):
        return 'FAM-03_CONVERSACION_RELACIONAL'
    if 'ácid' in text or 'chisme' in text or 'contexto' in text or 'averg' in text or 'cafe' in text:
        return 'FAM-04_ACIDO_INTERPERSONAL'
    if re.search(r'fantasma|wilfred|elara|kiri|maeve|silvio|ganso|evan|kael', r.get('Archivo',''), re.I):
        return 'FAM-05_PERSONAJE_MARCADOR'
    if 'relatable' in text or 'automejora' in text or 'situacional' in text or 'rutina' in text:
        return 'FAM-02_RELATABLE_SOCIAL'
    return 'UNCLASSIFIED_NEW'

for r in clean:
    r['Alignment_Class'] = classify(r)
    r['Experiment_Status'] = 'Not_Eligible_If_P0_or_Reuse' if r['Alignment_Class'] == 'REUSE_NOT_EXPERIMENTAL' else 'Candidate_For_Overlay'

by_date = defaultdict(list)
for r in clean: by_date[r['Fecha']].append(r)
summary = {
    'source': str(cal.relative_to(root)),
    'rows_read': len(rows),
    'clean_rows': len(clean),
    'issues': issues,
    'type_counts': dict(Counter(r.get('Tipo_Contenido','') for r in clean)),
    'alignment_counts': dict(Counter(r['Alignment_Class'] for r in clean)),
    'caption_counts': dict(Counter(r.get('Tipo_Copy','') for r in clean)),
    'experiment_ids': dict(Counter(r.get('Experiment_ID','') for r in clean)),
    'dates': {d: {'slots': len(rs), 'types': dict(Counter(r.get('Tipo_Contenido','') for r in rs)), 'families': dict(Counter(r['Alignment_Class'] for r in rs)), 'hours': [r['Hora'] for r in rs]} for d, rs in sorted(by_date.items())},
    'guardrail_findings': {
        'reuse_rows_must_not_enter_wave1': sum(r['Alignment_Class'] == 'REUSE_NOT_EXPERIMENTAL' for r in clean),
        'new_rows_candidate_overlay': sum(r['Alignment_Class'] != 'REUSE_NOT_EXPERIMENTAL' for r in clean),
        'all_rows_share_single_calendar_experiment': len({r.get('Experiment_ID','') for r in clean}) == 1,
        'calendar_has_no_caption_treatment_field': 'Caption_Treatment' not in (clean[0] if clean else {}),
    }
}
out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(summary, indent=2, ensure_ascii=False))
