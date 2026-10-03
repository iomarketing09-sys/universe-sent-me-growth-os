import json
from pathlib import Path

contexts = {}
p_ctx = Path("publication_contexts.json")
if p_ctx.exists():
    try:
        with open(p_ctx) as f:
            raw = json.load(f)
            items = raw.values() if isinstance(raw, dict) else raw
            contexts = {c.get("publication_id"): (c.get("asset_ref") or c.get("character")) for c in items if c.get("publication_id")}
    except:
        pass

with open("comment_responses/facebook_comments/data/comments_log.json") as f:
    data = json.load(f)

# Filtrar baja señal y ordenar por fecha reciente
low = [c for c in data if not c.get("needs_response")]
low_recent = sorted(low, key=lambda x: x.get("created_time") or "", reverse=True)

print("\n=== LOS 12 COMENTARIOS DE BAJA SEÑAL RECIENTES ===")
for i, c in enumerate(low_recent[:12], 1):
    cid = c.get("comment_id", "")
    pid = cid.split("_")[0] if cid else ""
    meme = contexts.get(pid, f"Post ID: {pid}")
    txt = (c.get("comment_text") or "").strip()
    fecha = c.get("created_time", "Sin fecha")
    contenido = f'"{txt}"' if txt else "[Sticker / Imagen / GIF de Facebook]"
    print(f"[{i}] Fecha: {fecha} | Meme: {meme}")
    print(f"    ID: {cid} | Comentario: {contenido}\n")
