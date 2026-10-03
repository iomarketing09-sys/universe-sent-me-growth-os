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
BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:20128/v1")
MODEL = os.getenv("VISION_MODEL", "nvidia/meta/llama-3.2-11b-vision-instruct")

def load_contexts() -> Dict[str, Any]:
    if CONTEXTS_FILE.exists():
        try:
            with open(CONTEXTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Aviso al leer {CONTEXTS_FILE}: {e}")
    return {}

def save_contexts(contexts: Dict[str, Any]):
    with open(CONTEXTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contexts, f, ensure_ascii=False, indent=2)

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
    contexts = load_contexts()
    if not visual_info:
        visual_info = {"character": "", "meme_text": "", "visual_context": ""}

    contexts[post_id] = {
        "publication_id": post_id,
        "asset_ref": asset_name,
        "character": visual_info.get("character", ""),
        "meme_text": visual_info.get("meme_text", ""),
        "visual_context": visual_info.get("visual_context", ""),
        "caption": caption,
        "published_at": published_at
    }
    save_contexts(contexts)
    print(f"✅ Contexto acumulado guardado para post ID: {post_id}")

if __name__ == "__main__":
    print("Módulo context_manager listo.")
