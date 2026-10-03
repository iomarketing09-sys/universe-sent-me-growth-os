import os, requests, json

token = os.getenv("PAGE_ACCESS_TOKEN")

# Los 4 comentarios detectados con sticker o foto
comentarios = [
    {"id": "122170619001072582_2021843231849741", "meme": "Existencial 2607913", "tipo": "Sticker"},
    {"id": "122170618929072582_1083526124428829", "meme": "Universe - pudimos serlo todo", "tipo": "Sticker"},
    {"id": "122170156449072582_3014681488870412", "meme": "Existencial 2607954", "tipo": "Foto"},
    {"id": "122170573779072582_1351946393448649", "meme": "Reel Depresión Sonora", "tipo": "Sticker"}
]

print("\n" + "="*80)
print("🔍 INSPECCIÓN VISUAL DE COMENTARIOS (META GRAPH API + OMNIROUTE)")
print("="*80)

for c in comentarios:
    cid = c["id"]
    url = f"https://graph.facebook.com/v19.0/{cid}?fields=id,attachment{{type,title,description,media,url}}&access_token={token}"
    r = requests.get(url, timeout=30).json()
    att = r.get("attachment", {})
    
    img_url = att.get("media", {}).get("image", {}).get("src") or att.get("url") or "(Sin enlace directo)"
    titulo_att = att.get("title") or att.get("description") or ""

    # Intento de descripción con OmniRoute si está activo
    desc_ia = ""
    if img_url.startswith("http"):
        try:
            payload = {
                "model": "meta/llama-3.2-11b-vision-instruct",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe en una sola frase breve qué sticker o imagen es esta y qué emoción expresa:"},
                        {"type": "image_url", "image_url": {"url": img_url}}
                    ]
                }],
                "max_tokens": 60
            }
            omni_r = requests.post("http://localhost:20128/v1/chat/completions", json=payload, timeout=12).json()
            desc_ia = omni_r.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        except Exception:
            pass

    print(f"📌 Meme: {c['meme']} | Tipo: {c['tipo']}")
    print(f"   Comentario ID: {cid}")
    if titulo_att:
        print(f"   Título de Facebook: {titulo_att}")
    print(f"   🔗 Ver imagen: {img_url}")
    if desc_ia:
        print(f"   🤖 Descripción IA: {desc_ia}")
    print("-" * 80)
