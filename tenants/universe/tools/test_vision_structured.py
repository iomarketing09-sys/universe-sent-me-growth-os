#!/usr/bin/env python3
import os
import sys
import json
import base64
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    API_KEY = input("Pega tu API Key de OmniRoute: ").strip()

BASE_URL = "http://localhost:20128/v1"
MODEL = "nvidia/meta/llama-3.2-11b-vision-instruct"
IMAGE_PATH = "assets/Humor existencial/09 Septiembre/2609064 - Universe - Toco todo lo que rompo.jpeg"

with open(IMAGE_PATH, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

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

print(f"🚀 Solicitando JSON estructurado a OmniRoute ({MODEL})...")
try:
    r = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=60)
    if r.status_code == 200:
        content = r.json()["choices"][0]["message"]["content"]
        print("\n--- SALIDA DEL MODELO ---")
        print(content)
    else:
        print("❌ Error:", r.text)
except Exception as e:
    print("❌ Error de conexión:", e)
