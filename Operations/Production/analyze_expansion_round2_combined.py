from pathlib import Path
import csv, json, statistics

root = Path('/home/ubuntu/universe-sent-me-growth-os')
main_path = root / 'Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv'
round2_path = root / 'Operations/Research/2026-08-20_Expansion_Round2_Candidatos.csv'
out_path = root / 'Operations/Research/2026-08-20_Expansion_Round2_Combined_Summary.json'

def read(p):
    with p.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))
main = read(main_path)
round2 = read(round2_path)

def vals(rows, field):
    return [float(r[field]) for r in rows]

def stats(rows):
    inter = vals(rows, 'Interacciones')
    shares = vals(rows, 'Shares')
    return {
        'n': len(rows),
        'median_interactions': statistics.median(inter) if inter else None,
        'mean_interactions': statistics.mean(inter) if inter else None,
        'median_shares': statistics.median(shares) if shares else None,
        'mean_shares': statistics.mean(shares) if shares else None,
        'interactions': inter,
        'shares': shares,
    }

# Strict primary cells from the main matrix.
primary_cells = {}
for cell in ['Microhistoria secuencial', 'Transformación visual', 'Humor observacional', 'Diálogo ácido', 'Autodesprecio / antihéroe']:
    rows = [r for r in main if r['Cell_Name'] == cell and r['Estado_Candidato'] == 'Current_Comparable']
    primary_cells[cell] = stats(rows)

# Secondary subcells from round 2.
secondary_cells = {}
for cell in sorted({r['Cell_Name'] for r in round2}):
    rows = [r for r in round2 if r['Cell_Name'] == cell and r['Estado_Candidato'] == 'Current_Comparable']
    if rows:
        secondary_cells[cell] = stats(rows)

# Explicit sensitivity checks for the current outlier-labelled cells.
def non_outlier(rows, ids):
    return [r for r in rows if r['Meta_ID'] not in ids]

sensitivity = {}
for cell, ids in {
    'Diálogo ácido': {'1036844829507460_122134161303072582'},
    'Autodesprecio / antihéroe': {'1036844829507460_122134136793072582'},
}.items():
    rows = [r for r in main if r['Cell_Name'] == cell and r['Estado_Candidato'] == 'Current_Comparable']
    sensitivity[cell] = {'all': stats(rows), 'excluding_flagged_outlier': stats(non_outlier(rows, ids))}

caption_counts = {}
for label, rows in [('primary_matrix', main), ('round2', round2)]:
    caption_counts[label] = {}
    for treatment in sorted({r['Caption_Treatment'] for r in rows}):
        caption_counts[label][treatment] = sum(r['Caption_Treatment'] == treatment for r in rows)

result = {
    'primary_cells': primary_cells,
    'secondary_cells': secondary_cells,
    'sensitivity': sensitivity,
    'caption_counts': caption_counts,
    'interpretation': {
        'microstory': 'Keep strict three-panel and two-panel subcells separate; do not pool yet.',
        'transformation': 'Universe transformation remains n=2; Ganso vestuario is a separate exploratory subcell and not evidence for Universe.',
        'observational': 'Reaches preliminary n=3, but the 924-interaction candidate remains under sensitivity/editorial review.',
        'dialogue_acid': 'Reaches n=2 only; the signal is highly sensitive to the 521-interaction outlier.',
        'self_antih ero': 'Reaches n=2 only; the signal is highly sensitive to the 1,308-interaction outlier and Ganso is not yet included.',
        'captions': 'Historical caption treatments remain unavailable for the round2 cases; no effect is estimated.'
    }
}
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(result, indent=2, ensure_ascii=False))
