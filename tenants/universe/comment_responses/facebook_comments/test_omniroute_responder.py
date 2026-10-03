#!/usr/bin/env python3
import os
import sys
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    # Intentar leerla del .env del tenant si existe
    env_path = os.path.expanduser("~/growth-os/tenants/universe/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("OMNIROUTE_API_KEY=") or line.startswith("OPENAI_API_KEY="):
                    API_KEY = line.strip().split("=", 1).strip("'\"")

if not API_KEY:
    API_KEY = input("Pega tu API Key de OmniRoute: ").strip()

BASE_URL = "http://localhost:20128/v1"
MODEL = "nvidia/meta/llama-3.2-11b-vision-instruct"

system_prompt = (
    "Eres el generador de respuestas de 'Universe Sent Me'.\n"
    "Estás respondiendo desde la voz de Elara (lectora de tarot del universo, relajada, misteriosa y con humor cotidiano).\n"
    "Reglas estrictas de tono:\n"
    "- Humor cálido, breve y con remate divertido.\n"
    "- Máximo 140 caracteres.\n"
    "- PROHIBIDO sonar corporativo (NUNCA digas 'gracias por comentar', 'gracias por ser parte de la comunidad', 'saludos').\n"
    "- Ríete con el usuario, siguiendo el juego de la comida o el tarot."
)

user_prompt = (
    "Contexto del meme de Elara:\n"
    "Texto: 'El tarot dice que el amor de tu vida está con otra porque ni sabes qué cenar'\n\n"
    "Comentario del seguidor:\n"
    "'Claro que si sé que quiero cenar, y es una deliciosa hmaburgruesa con papas :3'\n\n"
    "Genera una respuesta en personaje para responder a este seguidor:"
)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "max_tokens": 80,
    "temperature": 0.7,
    "stream": False
}

print(f"🚀 Generando respuesta con OmniRoute ({MODEL})...")
try:
    r = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=30)
    print("HTTP Status:", r.status_code)
    if r.status_code == 200:
        content = r.json()["choices"][0]["message"]["content"].strip()
        print("\n--- PROPUESTA DE RESPUESTA DE ELARA ---")
        print(content)
    else:
        print("❌ Error de OmniRoute:", r.text)
except Exception as e:
    print("❌ Error:", e)
