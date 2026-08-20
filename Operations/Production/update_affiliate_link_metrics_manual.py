import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Link_Ledger.csv')
with path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)
for row in rows:
    if row['Link_ID'] == 'ML-FB-AFF07-260540':
        row['Clicks'] = '1'
        row['Gross_Sales'] = '0'
        row['Approved_Sales'] = '0'
        row['Units_Sold'] = '0'
        row['Revenue_MXN'] = '0'
        row['Commission_MXN'] = '0'
        row['Confirmed_Commission_MXN'] = '0'
        row['Metrics_Cutoff_Local'] = '2026-08-20 20:51'
        row['Source'] = (row['Source'] + ' + Fernando screenshot').strip(' +')
        note = 'Manual snapshot: Últimos 7 días; 1 clic, 0 unidades, 0% conversión, $0 aumento estimado.'
        if note not in row['Notes']:
            row['Notes'] = row['Notes'].rstrip('.') + '. ' + note
    elif row['Link_ID'] == 'ML-FB-REALUNIVERSE-20260819-2210896633022235':
        note = 'Manual snapshot: etiqueta usmfb20260819p01 no visible en la tabla; estado Not_Visible_No_Inference; no se asigna cero.'
        if note not in row['Notes']:
            row['Notes'] = row['Notes'].rstrip('.') + '. ' + note
with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print('updated=AFF-07-and-REEL-note')
