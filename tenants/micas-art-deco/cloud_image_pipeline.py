#!/usr/bin/env python3
"""
cloud_image_pipeline.py — Mica's Art & Deco (CGO Pipeline)
Ruta origen: /home/universe-sent-me/GoogleDrive/MICAS/002 PRODUCTOS/02 - Pinturas Mica/
Pre-escalado de seguridad (<15MB RAM) + Cloudflare Images + Montaje de Galería.
"""
import os
import io
import sys
import json
import requests
from pathlib import Path
from PIL import Image, ImageFilter

ENV_PATH = Path("/home/universe-sent-me/growth-os/tenants/micas-art-deco/.env")
BASE_PRODUCTS_DIR = Path("/home/universe-sent-me/GoogleDrive/MICAS/002 PRODUCTOS/02 - Pinturas Mica")

def load_env():
    env = {}
    if ENV_PATH.exists():
        for line in open(ENV_PATH):
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    return env

def process_painting(input_image_path):
    env = load_env()
    account_id = env.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = env.get("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token:
        print("[-] Error: Faltan CLOUDFLARE_ACCOUNT_ID o CLOUDFLARE_API_TOKEN en el .env")
        return

    input_path = Path(input_image_path)
    if not input_path.exists():
        print(f"[-] Archivo no encontrado: {input_path}")
        return

    out_folder = input_path.parent / "processed_ecommerce"
    out_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("MICA'S ART & DECO — PIPELINE VISUAL CGO (CLOUDFLARE)")
    print(f"Lienzo: {input_path.name} ({input_path.stat().st_size / (1024*1024):.2f} MB)")
    print("=" * 65)

    # 1. PRE-ESCALADO DE SEGURIDAD (0% CPU en iMac)
    print("[1/3] Pre-escalando foto a 1500px para envío ultraligero...")
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        max_dim = 1500
        if max(img.size) > max_dim:
            scale = max_dim / max(img.size)
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        payload_bytes = buffer.getvalue()
        print(f"      Payload para Cloudflare: {len(payload_bytes)/1024:.1f} KB")

    # 2. REGISTRO EN CLOUDFLARE IMAGES API
    print("[2/3] Subiendo activo a Cloudflare Images API...")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1"
    headers = {"Authorization": f"Bearer {api_token}"}
    files = {"file": (input_path.name, payload_bytes, "image/jpeg")}

    resp = requests.post(url, headers=headers, files=files, timeout=30)
    data = resp.json()

    if not data.get("success"):
        print(f"[-] Error en Cloudflare: {json.dumps(data.get('errors'), indent=2)}")
        return

    res = data.get("result", {})
    image_id = res.get("id")
    variants = res.get("variants", [])
    print(f"[+] Activo subido a Cloudflare ID: {image_id}")
    if variants:
        print(f"[+] URL CDN pública: {variants[0]}")

    # 3. MONTAJE DE GALERÍA E-COMMERCE (#F8F7F4 + SOMBRA DIFUSA)
    print("[3/3] Generando mockup para Meta Commerce / Web...")
    canvas_size = (1200, 1200)
    canvas = Image.new("RGBA", canvas_size, (248, 247, 244, 255))
    
    img_aspect = img.width / img.height
    target_w = 900
    target_h = int(target_w / img_aspect)
    painting_resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS).convert("RGBA")

    # Sombra difusa suave de galería
    shadow = Image.new("RGBA", (target_w + 40, target_h + 40), (0, 0, 0, 0))
    shadow_box = Image.new("RGBA", (target_w, target_h), (30, 25, 20, 75))
    shadow.paste(shadow_box, (20, 20))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))

    pos_x = (canvas_size[0] - target_w) // 2
    pos_y = (canvas_size[1] - target_h) // 2
    canvas.paste(shadow, (pos_x - 10, pos_y - 5), shadow)
    canvas.paste(painting_resized, (pos_x, pos_y), painting_resized)

    out_file = out_folder / f"{input_path.stem}_ecommerce_mockup.jpg"
    canvas.convert("RGB").save(out_file, "JPEG", quality=95)
    print("=" * 65)
    print(f"¡ÉXITO! Mockup guardado en:\n{out_file}")
    print("=" * 65)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else str(BASE_PRODUCTS_DIR / "Manzana.jpg")
    process_painting(target)
