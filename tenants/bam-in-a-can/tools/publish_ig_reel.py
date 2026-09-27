#!/usr/bin/env python3
"""
Publicador oficial de Instagram Reels para Bam in a Can (Tenant #3).
Sube archivos MP4 locales directamente a los servidores de Meta mediante RUPLOAD.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
import requests

def load_env(env_path: Path) -> dict:
    env = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

def publish_reel(video_path: Path, caption: str, dry_run: bool = False):
    tenant_dir = Path(__file__).resolve().parents[1]
    env = load_env(tenant_dir / ".env")

    ig_user_id = env.get("IG_USER_ID")
    page_token = env.get("PAGE_ACCESS_TOKEN")

    if not ig_user_id or not page_token:
        raise SystemExit("❌ Error: IG_USER_ID o PAGE_ACCESS_TOKEN no encontrados en tenants/bam-in-a-can/.env")

    if not video_path.exists():
        raise SystemExit(f"❌ Error: Archivo de video no encontrado: {video_path}")

    file_size = os.path.getsize(video_path)
    print("=" * 60)
    print(f"BAM IN A CAN — Publicador de Instagram Reels {'[DRY RUN]' if dry_run else '[LIVE]'}")
    print("=" * 60)
    print(f"📁 Video: {video_path.name} ({file_size / (1024*1024):.2f} MB)")
    print(f"👤 Cuenta: @bam_inacan (ID: {ig_user_id})")
    print(f"📝 Caption: {caption[:50]}...")

    if dry_run:
        print("\n✅ Verificación exitosa en DRY RUN. Todo listo para publicar en modo LIVE.")
        return

    # PASO 1: Iniciar sesión de subida resumable en Meta
    print("\n1️⃣ Creando sesión de subida RUPLOAD en Meta...")
    init_url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media"
    init_params = {
        "media_type": "REELS",
        "upload_type": "resumable",
        "caption": caption,
        "access_token": page_token
    }
    r = requests.post(init_url, data=init_params, timeout=30).json()
    if "id" not in r or "uri" not in r:
        raise RuntimeError(f"Fallo al inicializar contenedor: {r}")

    container_id = r["id"]
    upload_uri = r["uri"]
    print(f"   ➔ Contenedor creado: {container_id}")
    print(f"   ➔ Endpoint de subida recibido.")

    # PASO 2: Enviar el archivo binario del video
    print("2️⃣ Subiendo bytes de video a Meta...")
    with open(video_path, "rb") as f:
        video_bytes = f.read()

    upload_headers = {
        "Authorization": f"OAuth {page_token}",
        "offset": "0",
        "file_size": str(file_size),
        "Content-Type": "application/octet-stream"
    }
    upload_res = requests.post(upload_uri, headers=upload_headers, data=video_bytes, timeout=120).json()
    if not upload_res.get("success"):
        raise RuntimeError(f"Fallo en la subida binaria: {upload_res}")
    print("   ➔ Video cargado en los servidores de Instagram con éxito.")

    # PASO 3: Esperar a que Instagram procese el video
    print("3️⃣ Esperando procesamiento de video en Instagram...")
    status_url = f"https://graph.facebook.com/v21.0/{container_id}?fields=status_code,status&access_token={page_token}"
    max_retries = 30
    for i in range(max_retries):
        time.sleep(5)
        status_data = requests.get(status_url, timeout=20).json()
        status_code = status_data.get("status_code")
        print(f"   ➔ Estado [{i+1}/{max_retries}]: {status_code}")
        if status_code == "FINISHED":
            break
        elif status_code == "ERROR":
            raise RuntimeError(f"Instagram rechazó el procesamiento del video: {status_data}")
    else:
        raise TimeoutError("Tiempo de espera agotado mientras Instagram procesaba el Reel.")

    # PASO 4: Publicar el Reel
    print("4️⃣ Publicando Reel en el feed de @bam_inacan...")
    publish_url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media_publish"
    pub_res = requests.post(publish_url, data={"creation_id": container_id, "access_token": page_token}, timeout=30).json()
    if "id" not in pub_res:
        raise RuntimeError(f"Fallo al publicar el Reel: {pub_res}")

    post_id = pub_res["id"]
    print("\n" + "=" * 60)
    print(f"🎉 ¡REEL PUBLICADO CON ÉXITO!")
    print(f"🆔 Post ID: {post_id}")
    print(f"🔗 Revisa tu perfil: https://www.instagram.com/bam_inacan/")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publicar un Reel en Instagram directamente desde Ubuntu")
    parser.add_argument("--file", required=True, help="Ruta al archivo MP4")
    parser.add_argument("--caption", required=True, help="Texto del copy")
    parser.add_argument("--live", action="store_true", help="Publicar en vivo (por defecto corre en dry-run)")
    args = parser.parse_args()

    publish_reel(video_path=Path(args.file).expanduser().resolve(), caption=args.caption, dry_run=not args.live)
