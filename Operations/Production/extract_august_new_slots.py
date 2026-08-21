from pathlib import Path
import csv

root = Path('/home/ubuntu/universe-sent-me-growth-os')
cal = root / 'Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv'
out = root / 'Operations/Research/2026-08-20_Agosto_17_30_New_Slots_For_Experiment_Overlay.csv'
with cal.open(newline='', encoding='utf-8-sig') as f:
    rows = [r for r in csv.DictReader(f) if r.get('Tipo_Contenido') == 'Nueva']
fields = ['Fecha','Día','Hora','Archivo','Estado','Contexto_Nota','Caption_Propuesto','Tipo_Copy','Experiment_ID','Asset_Estado_Operativo']
with out.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows({k:r.get(k,'') for k in fields} for r in rows)
print(out)
for r in rows:
    print(f"{r.get('Fecha')} {r.get('Hora')} | {r.get('Archivo')} | {r.get('Contexto_Nota')} | caption={r.get('Caption_Propuesto')}")
