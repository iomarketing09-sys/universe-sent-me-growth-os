import csv
from pathlib import Path

base = Path('/home/ubuntu/universe-sent-me-growth-os')
paths = [
    base / 'Operations/Research/2026-08-18_Junio_Archivo_Fundacional_Top15.csv',
    base / 'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv',
]
for path in paths:
    print(f'--- {path.name} ---')
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        print('columns:', reader.fieldnames)
        for row in list(reader)[:8]:
            print(row)
