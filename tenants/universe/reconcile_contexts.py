#!/usr/bin/env python3
import os
import glob
import csv
import json
from pathlib import Path
import requests

TENANT_DIR = Path(__file__).resolve().parent
ENV_PATH = TENANT_DIR / ".env"
CONTEXTS_PATH = TENANT_DIR / "publication_contexts.json"

# Cargar credenciales desde .env
env_vars = {}
with open(ENV_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip().strip("'\"")

PAGE_ID = env_vars.get("FB_PAGE_ID")
TOKEN = env_vars.get("PAGE_ACCES_TOKEN") or env_vars.get("PAGE_ACCESS_TOKEN") or env_vars.get("META_ACCESS_TOKEN")

if not PAGE_ID or not TOKEN:
    print("❌ Error: no se encontraron credenciales en .env")
    exit(1)

# 1. Cargar catálogo de los CSVs diarios
csv_catalog = []
for csv_file in sorted(glob.glob(str(TENANT_DIR / "imports" / "meta_import_*.csv")) + glob.glob(str(TENANT_DIR / "meta_import_*.csv"))):
    try:
        with open(csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                caption = row.get("Caption", "").strip()
                asset = row.get("Media URL", "").strip()
                if not caption or not asset:
                    continue
                
                clean_name = asset.replace(".jpeg", "").replace(".jpg", "").replace(".png", "")
                clean_parts = clean_name.split(" - ")
                
                if len(clean_parts) >= 3:
                    clean_parts.pop(0)  # Remueve el ID numérico
                    character = clean_parts.pop(0).strip()
                    concept = " - ".join(clean_parts).strip()
                elif len(clean_parts) == 2:
                    clean_parts.pop(0)
                    character = clean_parts.pop(0).strip()
                    concept = clean_name
                else:
                    character = "Universe"
                    concept = clean_name

                csv_catalog.append({
                    "caption": caption,
                    "asset": asset,
                    "character": character,
                    "concept": concept
                })
    except Exception as e:
        print(f"Aviso leyendo {csv_file}: {e}")

print(f"📋 Cargadas {len(csv_catalog)} publicaciones desde archivos meta_import_*.csv")

# 2. Consultar posts recientes de Meta Graph API
url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/posts"
params = {"fields": "id,message,created_time", "limit": 50, "access_token": TOKEN}
try:
    res = requests.get(url, params=params, timeout=30).json()
except Exception as e:
    print(f"❌ Error al consultar Meta Graph API: {e}")
    exit(1)

posts = res.get("data", [])
print(f"📡 Obtenidos {len(posts)} posts recientes desde Meta Graph API")

# 3. Cargar acumulador actual
contexts = {}
if CONTEXTS_PATH.exists():
    try:
        with open(CONTEXTS_PATH, "r", encoding="utf-8") as f:
            contexts = json.load(f)
    except Exception:
        contexts = {}

# 4. Vincular por coincidencia de caption
matches = 0
for post in posts:
    post_id = post.get("id")
    fb_msg = post.get("message", "")
    created_time = post.get("created_time")
    
    if not fb_msg:
        continue
        
    for item in csv_catalog:
        # Coincidencia si el caption del CSV está en el mensaje de Facebook o coincide en los primeros 25 caracteres
        cap_clean = item["caption"].strip()
        if cap_clean in fb_msg or fb_msg.strip().startswith(cap_clean[:25]):
            entry = {
                "publication_id": post_id,
                "asset_ref": item["asset"],
                "character": item["character"],
                "meme_text": item["concept"],
                "visual_context": f"{item['character']} en {item['concept']}",
                "caption": fb_msg,
                "published_at": created_time
            }
            contexts[post_id] = entry
            short_id = post_id.split("_")[-1]
            contexts[short_id] = entry
            matches += 1
            print(f"  ✅ Post vinculado: {post_id} -> {item['character']} ({item['asset']})")
            break

with open(CONTEXTS_PATH, "w", encoding="utf-8") as f:
    json.dump(contexts, f, ensure_ascii=False, indent=2)

print(f"\n🎉 Total vinculados en esta ejecución: {matches}")
print(f"💾 Total registros en {CONTEXTS_PATH.name}: {len(contexts)}")
