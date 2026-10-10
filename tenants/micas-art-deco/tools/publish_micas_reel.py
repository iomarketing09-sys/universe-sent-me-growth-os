#!/usr/bin/env python3
"""
Publicador Oficial de Reels/Videos para Mica's Art & Deco (Instagram + Facebook)
"""

import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
import requests

TENANT_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = TENANT_DIR / ".env"
LOG_DIR = TENANT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
PUB_LOG = TENANT_DIR / "publication_log_week2.csv"

def load_env(path: Path) -> dict:
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

def main():
    parser = argparse.ArgumentParser(description="Publicar Reel en Instagram y Facebook para Mica's Art & Deco")
    parser.add_argument("--file", help="Ruta al video MP4", default="/home/universe-sent-me/GoogleDrive/MICAS/004 PROYECTOS/01 - Taller de Hoja de Oro/VID_20261001_010559_347_bsl2781141578068773303.mp4")
    parser.add_argument("--caption", help="Texto del copy")
    parser.add_argument("--live", action="store_true", help="Publicar en vivo")
    args = parser.parse_args()

    default_caption = (
        "Una tarde para desconectar de la prisa, tomar café rico y crear algo hermoso con tus propias manos. ✨🌿\n\n"
        "Abrimos la preventa de nuestro Taller Presencial de Hoja de Oro en Piedras Negras (mediados de octubre).\n\n"
        "👉 Aparta tu lugar aquí: https://wa.link/06diqw o comenta ORO.\n\n"
        "#PiedrasNegras #MicasArtDeco #TallerHojaDeOro #ArteYDecoracion"
    )
    caption = args.caption or default_caption
    video_path = Path(args.file)

    if not video_path.exists():
        sys.exit(f"❌ Error: Archivo de video no encontrado en: {video_path}")

    env = load_env(ENV_PATH)
    fb_page_id = env.get("FB_PAGE_ID")
    ig_user_id = env.get("IG_USER_ID")
    access_token = env.get("PAGE_ACCESS_TOKEN") or env.get("META_ACCESS_TOKEN")

    if not access_token or not fb_page_id or not ig_user_id:
        sys.exit("❌ Error: Faltan credenciales (FB_PAGE_ID, IG_USER_ID o PAGE_ACCESS_TOKEN) en .env")

    file_size = os.path.getsize(video_path)
    print("=" * 65)
    print(f"MICA'S ART & DECO — Publicador de Video / Reel {'[LIVE 🚀]' if args.live else '[DRY-RUN 🔍]'}")
    print("=" * 65)
    print(f"📁 Video: {video_path.name} ({file_size / (1024*1024):.2f} MB)")
    print(f"📘 Facebook Page ID: {fb_page_id}")
    print(f"📸 Instagram User ID: {ig_user_id}")
    print(f"\n📝 Caption:\n{caption}\n")

    if not args.live:
        print("✅ Simulación completada con éxito. Agrega '--live' para publicar en ambas redes.")
        return

    # ----------------------------------------------------
    # 1. PUBLICAR EN FACEBOOK PAGE
    # ----------------------------------------------------
    print("\n1️⃣ Despachando a Facebook Page...")
    fb_url = f"https://graph-video.facebook.com/v21.0/{fb_page_id}/videos"
    with open(video_path, "rb") as vf:
        files = {"source": vf}
        data = {"description": caption, "access_token": access_token}
        fb_resp = requests.post(fb_url, data=data, files=files, timeout=300).json()

    if "id" in fb_resp:
        fb_video_id = fb_resp["id"]
        print(f"   ✅ Publicado en Facebook con éxito. Video ID: {fb_video_id}")
    else:
        print(f"   ❌ Error al publicar en Facebook: {fb_resp}")
        fb_video_id = None

    # ----------------------------------------------------
    # 2. PUBLICAR EN INSTAGRAM REELS (RUPLOAD)
    # ----------------------------------------------------
    print("\n2️⃣ Despachando a Instagram Reels...")
    init_url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media"
    init_params = {
        "media_type": "REELS",
        "upload_type": "resumable",
        "caption": caption,
        "access_token": access_token
    }
    init_resp = requests.post(init_url, data=init_params, timeout=30).json()

    if "id" not in init_resp or "uri" not in init_resp:
        print(f"   ❌ Fallo al inicializar contenedor en Instagram: {init_resp}")
        ig_media_id = None
    else:
        container_id = init_resp["id"]
        upload_uri = init_resp["uri"]
        print(f"   ➔ Contenedor creado: {container_id}")

        print("   ➔ Subiendo bytes a Meta...")
        headers = {
            "Authorization": f"OAuth {access_token}",
            "offset": "0",
            "file_size": str(file_size)
        }
        with open(video_path, "rb") as vf:
            up_resp = requests.post(upload_uri, headers=headers, data=vf, timeout=300)

        print("   ➔ Esperando procesamiento de video en Meta...")
        for _ in range(30):
            time.sleep(5)
            status_url = f"https://graph.facebook.com/v21.0/{container_id}?fields=status_code&access_token={access_token}"
            st_data = requests.get(status_url, timeout=30).json()
            code = st_data.get("status_code")
            print(f"      Estado actual: {code}...")
            if code == "FINISHED":
                break
            elif code == "ERROR":
                print(f"   ❌ Error en procesamiento de Meta: {st_data}")
                break

        print("   ➔ Publicando Reel en vivo...")
        pub_url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media_publish"
        pub_resp = requests.post(pub_url, data={"creation_id": container_id, "access_token": access_token}, timeout=30).json()

        if "id" in pub_resp:
            ig_media_id = pub_resp["id"]
            print(f"   ✅ Publicado en Instagram con éxito. Media ID: {ig_media_id}")
        else:
            print(f"   ❌ Error al publicar contenedor en Instagram: {pub_resp}")
            ig_media_id = None

    # Registrar en bitácora
    now_iso = datetime.now().isoformat()
    if PUB_LOG.exists():
        with open(PUB_LOG, "a", encoding="utf-8") as f:
            if fb_video_id:
                f.write(f"{now_iso[:10]},18:30,Facebook,\"Taller Hoja de Oro Reel\",{video_path.name},published,{fb_video_id},{now_iso},,,,\n")
            if ig_media_id:
                f.write(f"{now_iso[:10]},18:30,Instagram,\"Taller Hoja de Oro Reel\",{video_path.name},published,{ig_media_id},{now_iso},,,,\n")

    print("\n" + "=" * 65)
    print("✨ PROCESO DE PUBLICACIÓN CONCLUIDO")
    print("=" * 65)

if __name__ == "__main__":
    main()
