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

payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Analiza esta imagen de meme para un sistema de redes sociales:\n"
                        "1. Transcribe el texto exacto que está impreso en la imagen.\n"
                        "2. Describe brevemente la escena, personajes y situación visual.\n"
                        "Sé conciso y responde en español."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 300,
    "stream": False
}

print(f"🚀 Enviando imagen a OmniRoute ({MODEL})...")
try:
    r = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=60)
    print("HTTP Status:", r.status_code)
    
    if r.status_code == 200:
        try:
            data = r.json()
            print("\n--- RESULTADO DE VISIÓN ---")
            print(data["choices"][0]["message"]["content"])
        except Exception:
            print("\n--- RESPUESTA TEXTUAL DE OMNIROUTE ---")
            print(r.text)
    else:
        print("❌ Error de OmniRoute:", r.text)
except Exception as e:
    print("❌ Error:", e)
