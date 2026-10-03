import os, json, requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

token = os.getenv("PAGE_ACCESS_TOKEN")
page_id = os.getenv("FB_PAGE_ID", "1036844829507460")

# Contextos de memes
contexts = {}
p_ctx = Path("publication_contexts.json")
if p_ctx.exists():
    try:
        with open(p_ctx) as f:
            raw = json.load(f)
            items = raw.values() if isinstance(raw, dict) else raw
            contexts = {c.get("publication_id"): (c.get("asset_ref") or c.get("character")) for c in items if c.get("publication_id")}
    except: pass

# Posts recientes
url_posts = f"https://graph.facebook.com/v19.0/{page_id}/posts?limit=15&fields=id,created_time&access_token={token}"
r_posts = requests.get(url_posts, timeout=30).json()
posts = r_posts.get("data", [])

now = datetime.now(timezone.utc)
cutoff = now - timedelta(hours=48)

print("\n" + "="*80)
print("📥 COMENTARIOS RECIBIDOS EN LAS ÚLTIMAS 48 HORAS (CON ADJUNTOS / STICKERS)")
print("="*80)

count = 0
for p in posts:
    pid = p.get("id")
    meme = contexts.get(pid, f"Post ID: {pid}")
    url_comms = f"https://graph.facebook.com/v19.0/{pid}/comments?limit=50&fields=id,message,created_time,attachment,comments&access_token={token}"
    r_comms = requests.get(url_comms, timeout=30).json()
    comms = r_comms.get("data", [])

    for c in comms:
        ctime_str = c.get("created_time")
        try:
            ctime = datetime.fromisoformat(ctime_str.replace("+0000", "+00:00"))
        except:
            continue

        if ctime >= cutoff:
            count += 1
            cid = c.get("id")
            txt = (c.get("message") or "").strip()
            att = c.get("attachment")
            tipo_att = f" [Usuario envió {att.get('type')}: {att.get('title', '')}]" if att else ""
            respuestas = len(c.get("comments", {}).get("data", []))
            estado_resp = "🟢 Ya tiene respuesta" if respuestas > 0 else "⚪ Sin responder"

            print(f"[{count}] {ctime_str} | Meme: {meme} | {estado_resp}")
            print(f"    ID: {cid}")
            print(f"    Texto: \"{txt}\"{tipo_att}")
            print("-" * 80)

print(f"\nTotal comentarios encontrados en las últimas 48 hrs: {count}\n")
