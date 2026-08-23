#!/usr/bin/env python3
"""Apply the editorial refinements from pasted_content_3.txt to pending rows."""

import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parents[2] / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
UPDATES = {
    "122151376011072582_1576421464128022": "Hijo de hombre: nostalgia instantánea y ganas de volver a ver Tarzán. 🎶🥹",
    "122151376011072582_1017393391124351": "Viento… cortita la respuesta, pero bastante poderosa. 🌬️🎶",
    "122151376011072582_4579578845653974": "Frío frío… y de alguna manera Juan Luis Guerra consiguió que sonara todo lo contrario. 😂🎶",
    "122151375549072582_1755338779425523": "Jajaja, te metiste de lleno en una pregunta que lleva siglos dando dolores de cabeza: ¿qué significa realmente un ‘antes’ si el tiempo también tuvo un comienzo? 🤔✨",
    "122151376083072582_1345911810604525": "Anotado: Sandy Iris sí viene con el modo travesura activado. 😂🙈",
}

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
    rows = list(csv.DictReader(source))
    fieldnames = source.seek(0) or None

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
    reader = csv.DictReader(source)
    fieldnames = reader.fieldnames
    rows = list(reader)

seen = set()
for row in rows:
    comment_id = row["Comentario_ID"]
    if comment_id in UPDATES:
        if row["Respuesta_Estado"] != "Pendiente_Respuesta":
            raise SystemExit(f"Refusing to update non-pending row: {comment_id}")
        row["Respuesta_Sugerida"] = UPDATES[comment_id]
        seen.add(comment_id)

missing = set(UPDATES) - seen
if missing:
    raise SystemExit(f"Missing expected IDs: {sorted(missing)}")

with CSV_PATH.open("w", encoding="utf-8", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(f"UPDATED={len(seen)}")
for comment_id in sorted(seen):
    print(f"UPDATED_ID={comment_id}")
