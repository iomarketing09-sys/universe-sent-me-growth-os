from __future__ import annotations

import csv
from collections import Counter
from datetime import date
from pathlib import Path

CALENDAR = Path("Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv")
CUTOFF = date(2026, 8, 21)

with CALENDAR.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

future = []
for row in rows:
    try:
        row_date = date.fromisoformat(row["Fecha"])
    except ValueError:
        continue
    if row_date > CUTOFF:
        future.append(row)

print(f"total_rows={len(rows)}")
print(f"future_rows_after={CUTOFF.isoformat()}={len(future)}")
print(f"future_by_type={dict(Counter(row['Tipo_Contenido'] for row in future))}")
print(f"future_by_status={dict(Counter(row['Estado'] for row in future))}")
print("\nCANDIDATE_NEW_SLOTS")
for row in future:
    if row["Tipo_Contenido"] == "Nueva":
        print("\t".join([
            row["Fecha"], row["Día"], row["Hora"], row["Archivo"],
            row["Contexto_Nota"], row["Instagram_Decision"], row["Drive_ID"],
        ]))

print("\nSAME_TIME_DISTRIBUTION")
print(dict(Counter(row["Hora"] for row in future)))

print("\nSELECTED_EXPERIMENT_REQUIREMENTS")
print("FUT-MICRO-005=3-panel romantic-absurd; preferred test window=13:30 or 16:00; Caption_Treatment=caption_minimo; Caption_Function=reaccion")
print("FUT-MICRO-006=3-panel everyday; preferred test window=10:00 or 16:00; Caption_Treatment=caption_refuerzo; Caption_Function=refuerzo_semantico")
print("FUT-ACID-003=dialogue acidic situational; preferred test window=19:00 or 22:00; Caption_Treatment=caption_minimo; Caption_Function=reaccion")
