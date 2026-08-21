from pathlib import Path
import csv

root = Path('/home/ubuntu/universe-sent-me-growth-os')
candidates_path = root / 'Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv'
consolidated_path = root / 'Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv'

with consolidated_path.open(newline='', encoding='utf-8-sig') as f:
    metric_rows = {r['meta_id']: r for r in csv.DictReader(f)}
with candidates_path.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

for row in rows:
    if not (row.get('Interacciones') or '').strip():
        source = metric_rows.get(row['Meta_ID'])
        if source:
            row['Interacciones'] = str(int(float(source.get('reactions') or 0) + float(source.get('comments') or 0) + float(source.get('shares') or 0)))
            row['Comparability_Note'] = (row.get('Comparability_Note') or '') + ' Métrica total completada desde vista consolidada.'
            row['Source'] = (row.get('Source') or '') + ' + Historical_Performance_Individuals_Consolidated'

with candidates_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f'enriched_rows={len(rows)} metrics_completed={sum(1 for r in rows if "Métrica total completada" in r.get("Comparability_Note", ""))}')
