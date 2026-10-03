#!/usr/bin/env python3
import json
from pathlib import Path

LOG_FILE = Path("data/comments_log.json")
OUTPUT_FILE = Path("aprobaciones.json")

if not LOG_FILE.exists():
    print(f"❌ No se encontró {LOG_FILE}")
    exit(1)

with open(LOG_FILE, "r", encoding="utf-8") as f:
    logs = json.load(f)

# Las 10 respuestas aprobadas vinculadas a patrones de texto del comentario
targets = {
    "Que significa cucharear": "Empezó como comer sopa y terminó en evento canónico 🥄👀",
    "Así también ya le dije": "Las mariposas en el estómago no pagan el internet 💅🧾",
    "Era mejor cobrar": "El amor pasa, pero las transferencias SPEI se quedan 💸😌",
    "No entendi jajajajaja": "Si no lo entendiste, el universo te acaba de ahorrar tres traumas y dos terapias 🧠✨",
    "Cuando me da la taqui nocturna": "El corazón queriendo correr un maratón a las 3 AM mientras tú solo querías dormir 🫀🏃💨",
    "Por no comer nada": "Café en ayunas y voluntad de vivir: la dieta oficial del universo ☕💀",
    "yo soy inútil y aún así insisten": "El truco es la incompetencia estratégica: si lo haces mal a la primera, no te vuelven a pedir nada 🐾🧠",
    "Me vale, vivan sus vidas y ya": "Ese es el nivel de paz mental al que todos aspiramos un domingo por la tarde 🧘‍♂️✨",
    "Creo que  yo soy una de esas personas": "Bienvenido al club, las reuniones son a las 3 AM sobrepensando en el techo 🛋️✨",
    "Te pones feliz o triste": "Me pongo a mimir, que es la solución neutral del universo 🐾💤"
}

approvals = []
matched_keys = set()

# Buscamos en reversa para tomar los comentarios más recientes
for entry in reversed(logs):
    text = entry.get("comment_text", "")
    c_id = entry.get("comment_id")
    for pattern, response in targets.items():
        if pattern in text and pattern not in matched_keys:
            matched_keys.add(pattern)
            approvals.append({
                "comment_id": c_id,
                "character": "Universe",
                "original_comment": text,
                "approved": True,
                "approved_response": response
            })
            print(f"  ✅ Vinculado: '{pattern[:30]}...' -> ID: {c_id}")
            break

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"approvals": approvals}, f, ensure_ascii=False, indent=2)

print(f"\n📦 Archivo {OUTPUT_FILE.name} generado con éxito con {len(approvals)}/{len(targets)} respuestas aprobadas.")
