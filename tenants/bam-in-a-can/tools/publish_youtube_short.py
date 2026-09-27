#!/usr/bin/env python3
"""
Publicador oficial de YouTube Shorts para Bam in a Can (Tenant #3).
Usa la YouTube Data API v3 con subida resumible y soporte para publicación programada (publishAt).
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = Path("~/.config/usm-metrics/youtube-client-secret.json").expanduser()
TOKEN_FILE = Path("~/.config/growth-metrics/bam-youtube-token.json").expanduser()

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

def get_authenticated_service():
    if not CLIENT_SECRET_FILE.exists():
        raise SystemExit(f"❌ Error: No se encontró {CLIENT_SECRET_FILE}")

    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    creds = None

    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception:
            creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        except Exception:
            creds = None

    if not creds or not creds.valid:
        print("\n🌐 Se abrirá tu navegador para autorizar la cuenta de YouTube de @Bam_in_a_can...")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
        creds = flow.run_local_server(port=0, prompt="consent")
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        print("✅ Token de YouTube guardado con éxito.")

    return build("youtube", "v3", credentials=creds, cache_discovery=False)

def upload_short(video_path: Path, title: str, description: str, publish_at_iso: str = None, dry_run: bool = False):
    if not video_path.exists():
        raise SystemExit(f"❌ Error: No existe el archivo {video_path}")

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print("=" * 65)
    print(f"BAM IN A CAN — Publicador de YouTube Shorts {'[DRY RUN]' if dry_run else '[LIVE]'}")
    print("=" * 65)
    print(f"📁 Video: {video_path.name} ({file_size_mb:.2f} MB)")
    print(f"🎬 Título: {title}")
    if publish_at_iso:
        print(f"⏰ Programación para: {publish_at_iso} (UTC)")
    else:
        print("⚡ Publicación: Inmediata (Pública)")

    if dry_run:
        print("\n✅ DRY RUN exitoso. Archivo y parámetros listos para subida en modo LIVE.")
        return

    youtube = get_authenticated_service()

    status_dict = {
        "selfDeclaredMadeForKids": False
    }

    if publish_at_iso:
        status_dict["privacyStatus"] = "private"
        status_dict["publishAt"] = publish_at_iso
    else:
        status_dict["privacyStatus"] = "public"

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["BamInACan", "Shorts", "RetroCGI", "CultFilm", "AnalogHorror"],
            "categoryId": "1"  # Film & Animation
        },
        "status": status_dict
    }

    print("\n🚀 Subiendo video a YouTube por bloques resumibles...")
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True, chunksize=1024*1024*5)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   ➔ Progreso de subida: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    print("\n" + "=" * 65)
    print(f"🎉 ¡SHORT SUBIDO A YOUTUBE CON ÉXITO!")
    print(f"🆔 Video ID: {video_id}")
    print(f"🔗 Enlace: https://youtube.com/shorts/{video_id}")
    if publish_at_iso:
        print(f"📅 Estado: Programado para publicarse automáticamente a las {publish_at_iso}")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subir y programar un Short a YouTube")
    parser.add_argument("--file", required=True, help="Ruta al archivo MP4")
    parser.add_argument("--title", required=True, help="Título del Short")
    parser.add_argument("--description", default="", help="Descripción del Short")
    parser.add_argument("--publish-at", help="Fecha/hora ISO UTC para programar (ej: 2026-09-26T17:30:00Z)")
    parser.add_argument("--live", action="store_true", help="Ejecutar subida en vivo")
    args = parser.parse_args()

    upload_short(
        video_path=Path(args.file).expanduser().resolve(),
        title=args.title,
        description=args.description,
        publish_at_iso=args.publish_at,
        dry_run=not args.live
    )
