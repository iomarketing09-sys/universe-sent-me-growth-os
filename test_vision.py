import os
import base64
import requests

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Ruta a la foto de monograma en tu Drive montado
foto_path = "/home/universe-sent-me/GoogleDrive/01 - Firma Assets/03_Fotos_Reales/Firma Bordados 006.jpeg"

if not os.path.exists(foto_path):
    print(f"❌ No se encontró la foto en: {foto_path}")
    exit(1)

print("📷 Codificando imagen y enviando a OmniRoute...")
base64_img = encode_image(foto_path)

# Enviamos la petición al puerto 20128 de OmniRoute
try:
    response = requests.post(
        "http://127.0.0.1:20128/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "nvidia/meta/llama-3.2-11b-vision-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Actúa como redactor publicitario para Firma Bordados en Piedras Negras. Describe brevemente el bordado de esta foto y escribe un copy atractivo para Facebook con llamada a la acción al WhatsApp 878 788 0735 (sin mencionar parches ni gorras)."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_img}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 400,
            "temperature": 0.7
        },
        timeout=60
    )
    
    data = response.json()
    if "choices" in data:
        print("\n✨ RESPUESTA DE LA IA (VISIÓN):\n")
        print(data["choices"][0]["message"]["content"])
    else:
        print(f"⚠️ Respuesta inesperada: {data}")

except Exception as e:
    print(f"❌ Error al conectar con OmniRoute: {e}")
