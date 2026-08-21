#!/usr/bin/env python3
"""Classify confirmed July expansion images with a vision model.

The model is an assistive taxonomist. It must use visible evidence only and
can return No_identificado/Pendiente when identity is not visually confirmed.
"""
from __future__ import annotations

import base64
import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]
MATCHES = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Matches.csv"
QUEUE = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
IMAGE_DIR = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Meta_Images"
OUTPUT = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Assist.json"
MODEL = "gemini-3-flash-preview"

SCHEMA = {
    "type": "object",
    "properties": {
        "personaje_principal_observado": {"type": "string", "enum": ["Universe", "Wilfred", "Elara", "Kiri", "Fantasma", "Silvio", "Maeve", "Evan", "Ganso", "No_identificado"]},
        "personajes_secundarios_observados": {"type": "array", "items": {"type": "string"}},
        "rol_narrativo": {"type": "string", "enum": ["Protagonista", "Duo_o_pareja", "Reparto_coral", "Escena_observacional", "No_determinado"]},
        "tipo_humor_normalizado": {"type": "array", "items": {"type": "string", "enum": ["Existencial_o_absurdo", "Relatable_cotidiano", "Observacional_social", "Humor_acido_o_negro", "Sexual_o_insinuacion", "Fandom_o_referencia", "Reaccion_o_emoji", "Conversacional", "No_determinado"]}},
        "potencial_etiquetado": {"type": "string", "enum": ["Alto", "Medio", "Bajo", "No_determinado"]},
        "estructura_narrativa": {"type": "string", "enum": ["Texto_simple", "Escena_unica", "Dialogo_secuencial", "Microhistoria_dos_paneles", "Transformacion_visual", "Composicion_mundo", "Collage_multiple", "No_determinada"]},
        "caption_treatment": {"type": "string", "enum": ["caption_minimo", "caption_refuerzo", "caption_conversacional", "historical_unavailable"]},
        "preserva_marcadores_identidad": {"type": "string", "enum": ["Yes", "No", "Not_applicable", "Unclear"]},
        "confianza_taxonomia": {"type": "string", "enum": ["Alta", "Media", "Baja"]},
        "evidencia_visual_breve": {"type": "string"},
        "cautela": {"type": "string"}
    },
    "required": ["personaje_principal_observado", "personajes_secundarios_observados", "rol_narrativo", "tipo_humor_normalizado", "potencial_etiquetado", "estructura_narrativa", "caption_treatment", "preserva_marcadores_identidad", "confianza_taxonomia", "evidencia_visual_breve", "cautela"],
    "additionalProperties": False,
}

SYSTEM = """Eres un taxonomista visual riguroso para Universe Sent Me. Clasifica solo lo que se ve en la imagen y lo que aporta el caption de Meta. Nunca uses el filename, el número de asset o una apariencia genérica para asignar un personaje canónico. Si no hay evidencia visual suficiente, devuelve No_identificado o No_determinado. El objetivo es análisis histórico, no canonización. No confundas una escena de pareja con microhistoria secuencial: exige turnos o paneles claros. No confundas cualquier cambio de ropa con transformación de Universe. Para caption_treatment, usa historical_unavailable porque esta fase no reconstruye de forma verificable si el caption fue mínimo, de refuerzo o conversacional."""


def image_data(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def classify(row: dict[str, str]) -> dict:
    meta_id = row["Meta_ID"]
    path = IMAGE_DIR / f"{meta_id}.jpg"
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": [
                {"type": "text", "text": f"Meta_ID: {meta_id}\nCaption: {row.get('Caption', '')}\nMétricas lifetime: {row.get('Interacciones')} interacciones, {row.get('Shares')} shares, {row.get('Comentarios')} comentarios. Devuelve únicamente el JSON solicitado."},
                {"type": "image_url", "image_url": {"url": image_data(path), "detail": "auto"}},
            ]},
        ],
        response_format={"type": "json_schema", "json_schema": {"name": "usm_taxonomy", "strict": True, "schema": SCHEMA}},
        max_tokens=1200,
    )
    content = response.choices[0].message.content
    result = json.loads(content)
    result["Meta_ID"] = meta_id
    result["Caption"] = row.get("Caption", "")
    result["Interacciones"] = row.get("Interacciones", "")
    result["Shares"] = row.get("Shares", "")
    result["Comentarios"] = row.get("Comentarios", "")
    result["model"] = MODEL
    return result


def main() -> None:
    with MATCHES.open(newline="", encoding="utf-8-sig") as handle:
        matches = list(csv.DictReader(handle))
    with QUEUE.open(newline="", encoding="utf-8-sig") as handle:
        queue = {row["Meta_ID"]: row for row in csv.DictReader(handle)}
    confirmed = [queue[row["Meta_ID"]] for row in matches if row.get("Status") == "Visual_Match_Confirmed" and row["Meta_ID"] in queue]
    results = []
    errors = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(classify, row): row["Meta_ID"] for row in confirmed}
        for future in as_completed(futures):
            meta_id = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                errors.append({"Meta_ID": meta_id, "error": repr(exc)})
    results.sort(key=lambda row: row["Meta_ID"])
    payload = {"model": MODEL, "confirmed_input_rows": len(confirmed), "results": results, "errors": errors, "guardrail": "Assistive taxonomy only; human/evidence review remains authoritative."}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"input_rows": len(confirmed), "results": len(results), "errors": errors, "output": str(OUTPUT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
