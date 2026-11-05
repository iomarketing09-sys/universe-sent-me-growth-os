#!/usr/bin/env python3
import os
import sys
import json
import base64
from pathlib import Path
from typing import Dict, Optional, Any
import requests

GROWTH_ROOT = Path(__file__).resolve().parent
CONTEXTS_FILE = GROWTH_ROOT / "publication_contexts.json"
REPO_ROOT = GROWTH_ROOT.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.intelligence.publication_context import (  # noqa: E402
    load_contexts as _load_contexts,
    record_publication as _record_publication,
    save_contexts as _save_contexts,
)

BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:20128/v1")
MODEL = os.getenv("VISION_MODEL", "nvidia/meta/llama-3.2-11b-vision-instruct")

def load_contexts() -> Dict[str, Any]:
    return _load_contexts(GROWTH_ROOT)

def save_contexts(contexts: Dict[str, Any]):
    _save_contexts(GROWTH_ROOT, contexts)

def extract_visual_context(image_path: Path, api_key: Optional[str] = None) -> Dict[str, str]:
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY", "")
    
    if not image_path.exists():
        return {"character": "", "meme_text": "", "visual_context": ""}

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        "Analiza este meme de la marca 'Universe Sent Me'. "
        "Responde EXCLUSIVAMENTE en formato JSON válido con estas tres llaves:\n"
        "{\n"
        '  "character": "nombre del personaje principal (ej. Universe, Silvio, Elara, Maeve, Wilfred, Ganso, Evan, etc.)",\n'
        '  "meme_text": "transcripción literal del texto que aparece en la imagen",\n'
        '  "visual_context": "descripción de 1 o 2 oraciones de la escena visual y acción del personaje"\n'
        "}"
    )

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            }
        ],
        "max_tokens": 300,
        "stream": False
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        r = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            content = r.json()["choices"][0]["message"]["content"].strip()
            # Limpieza básica por si el modelo incluye markdown ```json
            if content.startswith("```"):
                content = content.split("```")
                if content.startswith("json"):
                    content = content[4:]
            return json.loads(content.strip())
    except Exception as e:
        print(f"Error en extracción visual para {image_path.name}: {e}")
    
    return {"character": "", "meme_text": "", "visual_context": ""}

def record_publication(
    post_id: str,
    asset_name: str,
    caption: str,
    published_at: str,
    visual_info: Optional[Dict[str, str]] = None
):
    visual_info = visual_info or {}
    merged = _record_publication(
        GROWTH_ROOT,
        post_id=post_id,
        asset_filename=asset_name,
        caption=caption,
        published_at=published_at,
        character=str(visual_info.get("character") or ""),
        meme_text=str(visual_info.get("meme_text") or ""),
        visual_context=str(visual_info.get("visual_context") or ""),
    )
    print(f"✅ Contexto acumulado guardado para post ID: {post_id}")
    return merged

if __name__ == "__main__":
    print("Módulo context_manager listo.")
