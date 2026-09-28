#!/usr/bin/env python3
"""
upload_tiktok_draft.py — Bam in a Can
Sube videos a Borradores (Inbox) de TikTok mediante la Content Posting API de TikTok.
Permite enlazar audio nativo y publicar desde la app móvil.
"""

from __future__ import annotations
import os
import sys
import json
import argparse
from pathlib import Path
import requests

CONFIG_PATH = Path("~/.config/usm-metrics/config.json").expanduser()
BAM_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

def expand(p: str) -> Path:
    return Path(p).expanduser().resolve()

def get_tiktok_token() -> str:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            token_file = expand(config.get("tiktok", {}).get("token_file", "~/.config/usm-metrics/tiktok-token.json"))
            if token_file.exists():
                with open(token_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                token = data.get("access_token")
                if token:
                    return token
        except Exception:
            pass

    direct_token_file = Path("~/.config/usm-metrics/tiktok-token.json").expanduser()
    if direct_token_file.exists():
        try:
            with open(direct_token_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            token = data.get("access_token")
            if token:
                return token
        except Exception:
            pass

    if BAM_ENV_PATH.exists():
        try:
            for line in open(BAM_ENV_PATH):
                if line.startswith("TIKTOK_ACCESS_TOKEN="):
                    return line.strip().split("=", 1)[1].strip(" \"'")
        except Exception:
            pass

    print("[-] Error: No se encontró token válido de TikTok en ~/.config/usm-metrics/tiktok-token.json")
    print("    Asegúrate de que la autorización OAuth de TikTok esté activa.")
    sys.exit(1)

def upload_draft(file_path: Path, caption: str, dry_run: bool = True) -> bool:
    if not file_path.exists():
        print(f"[-] Error: Archivo de video no encontrado: {file_path}")
        return False

    file_size = file_path.stat().st_size
    size_mb = file_size / (1024 * 1024)

    print("=" * 65)
    print(" BAM IN A CAN — SUBIDA A BORRADORES DE TIKTOK (INBOX API)")
    print(f" Modo    : {'EN VIVO (--live)' if not dry_run else 'SIMULACIÓN (dry-run)'}")
    print(f" Archivo : {file_path.name} ({size_mb:.2f} MB)")
    if caption:
        print(f" Caption : {caption.splitlines()[0]}...")
    print("=" * 65)

    if dry_run:
        print("\n[+] [DRY-RUN OK] Simulación exitosa. Pasa --live para subir el borrador.")
        return True

    token = get_tiktok_token()
    url_init = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8",
    }
    payload = {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": file_size,
            "total_chunk_count": 1,
        }
    }

    try:
        print("[*] Inicializando subida con TikTok Content Posting API...")
        res = requests.post(url_init, headers=headers, json=payload, timeout=30)
        data = res.json()

        if data.get("error", {}).get("code") == "ok":
            upload_url = data["data"]["upload_url"]
            publish_id = data["data"]["publish_id"]
            print(f"[*] Transfiriendo archivo ({size_mb:.2f} MB) a servidores de TikTok...")
            
            with open(file_path, "rb") as vf:
                upload_headers = {
                    "Content-Type": "video/mp4",
                    "Content-Length": str(file_size),
                    "Content-Range": f"bytes 0-{file_size-1}/{file_size}",
                }
                up_res = requests.put(upload_url, headers=upload_headers, data=vf, timeout=300)

            if up_res.status_code in [200, 201]:
                print(f"\n[+] ¡BORRADOR ENVIADO CON ÉXITO A TIKTOK!")
                print(f"    Publish ID: {publish_id}")
                print(f"    📲 Abre la app de TikTok > Inbox/Actividad > Notificación de TikTok.")
                print(f"    Toca la notificación para añadir tu audio nativo, ajustar volumen y publicar.")
                return True
            else:
                print(f"[-] Error al transferir binario: HTTP {up_res.status_code} - {up_res.text}")
                return False
        elif data.get("error", {}).get("code") == "scope_not_authorized":
            print("[-] Error: El token no cuenta con el permiso 'video.upload'.")
            return False
        else:
            print(f"[-] Error devuelto por TikTok: {data}")
            return False
    except Exception as e:
        print(f"[-] Excepción durante la subida: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Subir video de Bam in a Can a Borradores de TikTok")
    parser.add_argument("--file", required=True, help="Ruta al video MP4")
    parser.add_argument("--caption", default="", help="Texto de pie de video")
    parser.add_argument("--live", action="store_true", help="Ejecutar subida en vivo")
    args = parser.parse_args()

    file_path = Path(args.file)
    upload_draft(file_path=file_path, caption=args.caption, dry_run=not args.live)

if __name__ == "__main__":
    main()
