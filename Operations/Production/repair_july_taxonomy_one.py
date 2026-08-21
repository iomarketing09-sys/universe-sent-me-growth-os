#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

from openai import OpenAI
from classify_july_expansion_taxonomy import SCHEMA, SYSTEM, image_data, MODEL, IMAGE_DIR, OUTPUT

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
TARGET = "1036844829507460_122135016567072582"

with QUEUE.open(newline="", encoding="utf-8-sig") as handle:
    rows = {row["Meta_ID"]: row for row in csv.DictReader(handle)}
row = rows[TARGET]
client = OpenAI()
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": [
            {"type": "text", "text": f"Meta_ID: {TARGET}\nCaption: {row.get('Caption', '')}\nMétricas lifetime: {row.get('Interacciones')} interacciones, {row.get('Shares')} shares, {row.get('Comentarios')} comentarios. Devuelve únicamente el JSON solicitado y no incluyas texto fuera del JSON."},
            {"type": "image_url", "image_url": {"url": image_data(IMAGE_DIR / f"{TARGET}.jpg"), "detail": "high"}},
        ]},
    ],
    response_format={"type": "json_schema", "json_schema": {"name": "usm_taxonomy", "strict": True, "schema": SCHEMA}},
    max_tokens=3000,
)
result = json.loads(response.choices[0].message.content)
result.update({"Meta_ID": TARGET, "Caption": row.get("Caption", ""), "Interacciones": row.get("Interacciones", ""), "Shares": row.get("Shares", ""), "Comentarios": row.get("Comentarios", ""), "model": MODEL})
payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
payload["results"] = [item for item in payload["results"] if item.get("Meta_ID") != TARGET] + [result]
payload["results"].sort(key=lambda item: item["Meta_ID"])
payload["errors"] = [item for item in payload.get("errors", []) if item.get("Meta_ID") != TARGET]
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"repaired": TARGET, "results": len(payload["results"]), "errors": len(payload["errors"])}, ensure_ascii=False))
