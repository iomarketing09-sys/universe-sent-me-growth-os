import os, requests
from pathlib import Path

token = os.getenv("PAGE_ACCESS_TOKEN")
comment_id = "122169880395072582_1431737092356378"

posibles_rutas = [
    Path("/home/universe-sent-me/GoogleDrive/Universe sent me/Respuestas/toma este corazon.jpeg"),
    Path("/home/universe-sent-me/growth-os/tenants/universe/assets/stickers/toma este corazon.jpeg"),
]

sticker_path = next((p for p in posibles_rutas if p.exists()), None)

if not sticker_path:
    print("❌ No se encontró el archivo 'toma este corazon.jpeg' en las rutas esperadas.")
    exit(1)

print(f"🚀 Publicando sticker en comentario {comment_id}...")
print(f"📁 Usando archivo: {sticker_path}")
url = f"https://graph.facebook.com/v19.0/{comment_id}/comments"

with open(sticker_path, "rb") as img:
    r = requests.post(url, data={"access_token": token}, files={"source": img}, timeout=30)
    res = r.json()
    if "id" in res:
        print(f"✅ Publicado con éxito! Meta Reply ID: {res.get('id')}")
    else:
        print(f"❌ Error de Meta: {res}")
