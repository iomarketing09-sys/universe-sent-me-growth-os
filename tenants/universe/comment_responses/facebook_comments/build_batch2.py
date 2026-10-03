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
    "En algún momento fui": "Todos fuimos cringe en alguna línea temporal, se perdona pero no se olvida 🐾⏳",
    "Un extra sístole salvaje": "Un clásico del menú nocturno de la ansiedad 🫀🫠",
    "si te ven inútil terminarás moldeado": "Por eso hay que fingir demencia antes de que te asignen responsabilidades cósmicas 🌌🫠",
    "ay si soy normie": "El primer paso es la aceptación cósmica 🪽😌"
}

approvals = []
matched_keys = set()

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
            print(f"  ✅ Vinculado: '{pattern}' -> ID: {c_id}")
            break

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump({"approvals": approvals}, f, ensure_ascii=False, indent=2)

print(f"\n📦 Archivo {OUTPUT_FILE.name} generado con {len(approvals)}/{len(targets)} respuestas.")
