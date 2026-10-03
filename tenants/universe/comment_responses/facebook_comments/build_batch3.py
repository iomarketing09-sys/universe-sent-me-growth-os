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

targets = {
    "Y agrega pobreza": "Esa ya venía incluida por defecto en el paquete básico de la existencia 📦💸",
    "500 mas y se te acaban": "Ahorrando latidos para no gastar el presupuesto biológico antes del lunes 🫀📉",
    "Así que esto es todo": "Sí, esto es la adultez: dolor de espalda y dudas cósmicas a las 3 AM 🛋️✨",
    "Asta que dios quiera": "El universo mandándote sueño y tú pidiéndole explicaciones al destino 😴✨",
    "Para tu todo": "Mucho 'para ti todo' hasta que llega la hora de pagar la cuenta 🧾👀"
}

approvals = []
matched_keys = set()

for entry in reversed(logs):
    text = entry.get("comment_text", "")
    c_id = entry.get("comment_id")
    for pattern, response in targets.items():
        if pattern.lower() in text.lower() and pattern not in matched_keys:
            matched_keys.add(pattern)
            approvals.append({
                "comment_id": c_id,
                "character": "Universe",
                "original_comment": text,
                "approved": True,
                "approved_response": response
            })
            print(f"  ✅ Vinculado: '{pattern}' -> ID: {c_id}")
            break

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"approvals": approvals}, f, ensure_ascii=False, indent=2)

print(f"\n📦 Archivo {OUTPUT_FILE.name} generado con {len(approvals)}/{len(targets)} respuestas.")
