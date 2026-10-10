#!/usr/bin/env python3
"""
Despachador Semanal a Facebook para Firma Bordados.
Lee directamente tenants/firma-bordados/meta_import.csv y programa los posts
en la Fanpage vía Meta Graph API (v20.0).
"""

import os
import sys
import csv
import time
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================
GROWTH_ROOT = Path(__file__).resolve().parent
TENANT_DIR = GROWTH_ROOT / "tenants" / "firma-bordados"
ENV_PATH = TENANT_DIR / ".env"
META_IMPORT_PATH = TENANT_DIR / "meta_import.csv"

# Directorios de búsqueda de assets
ASSET_DIRS = [
    Path("/home/universe-sent-me/GoogleDrive/01 - Firma Assets"),
    TENANT_DIR / "assets"
]

# Zona horaria local: America/Matamoros (UTC-5)
LOCAL_TZ = timezone(timedelta(hours=-5))

# ==============================================================================
# CARGA DE ENTORNO
# ==============================================================================
def load_env(env_path: Path):
    if not env_path.exists():
        print(f"❌ Archivo .env no encontrado en {env_path}")
        sys.exit(1)
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env(ENV_PATH)

PAGE_ID = os.environ.get("FB_PAGE_ID") or os.environ.get("PAGE_ID") or "100063732515596"
ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN") or os.environ.get("PAGE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("❌ Falta META_ACCESS_TOKEN en .env")
    sys.exit(1)

# ==============================================================================
# BÚSQUEDA DE ASSETS
# ==============================================================================
def find_asset(filename: str) -> Optional[Path]:
    if not filename:
        return None
    clean_name = Path(filename).name.strip()
    for root_dir in ASSET_DIRS:
        if not root_dir.exists():
            continue
        # Búsqueda directa
        direct = root_dir / clean_name
        if direct.exists() and direct.is_file():
            return direct
        # Búsqueda recursiva
        for p in root_dir.rglob(clean_name):
            if p.is_file():
                return p
    return None

# ==============================================================================
# PUBLICADOR META GRAPH API
# ==============================================================================
class FacebookPublisher:
    def __init__(self, page_id: str, access_token: str):
        self.page_id = page_id
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v20.0"

    def _post(self, endpoint: str, data: Dict[str, Any], files: Optional[Dict] = None) -> Dict[str, Any]:
        data["access_token"] = self.access_token
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = requests.post(url, data=data, files=files, timeout=60)
            return resp.json()
        except Exception as e:
            return {"error": {"message": str(e)}}

    def publish_text(self, message: str, publish_ts: Optional[int] = None) -> Dict[str, Any]:
        payload = {"message": message}
        if publish_ts:
            payload["published"] = "false"
            payload["scheduled_publish_time"] = str(publish_ts)
        else:
            payload["published"] = "true"
        return self._post(f"{self.page_id}/feed", payload)

    def publish_photo(self, photo_path: Path, caption: str, publish_ts: Optional[int] = None) -> Dict[str, Any]:
        payload = {"caption": caption}
        if publish_ts:
            payload["published"] = "false"
            payload["scheduled_publish_time"] = str(publish_ts)
        else:
            payload["published"] = "true"
        
        with open(photo_path, "rb") as f:
            files = {"source": (photo_path.name, f, "image/jpeg")}
            return self._post(f"{self.page_id}/photos", payload, files)

    def publish_video(self, video_path: Path, description: str, publish_ts: Optional[int] = None) -> Dict[str, Any]:
        payload = {"description": description}
        if publish_ts:
            payload["published"] = "false"
            payload["scheduled_publish_time"] = str(publish_ts)
        else:
            payload["published"] = "true"

        with open(video_path, "rb") as f:
            files = {"source": (video_path.name, f, "video/mp4")}
            return self._post(f"{self.page_id}/videos", payload, files)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    print("=" * 70)
    print("PROGRAMADOR SEMANAL FACEBOOK - FIRMA BORDADOS")
    print(f"Page ID: {PAGE_ID}")
    print("=" * 70)

    if not META_IMPORT_PATH.exists():
        print(f"❌ No se encontró {META_IMPORT_PATH}")
        sys.exit(1)

    publisher = FacebookPublisher(PAGE_ID, ACCESS_TOKEN)
    now_utc = datetime.now(timezone.utc)

    # Leer CSV
    rows = []
    with open(META_IMPORT_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for r in reader:
            if not r or len(r) < 5:
                continue
            rows.append({
                "date": r[0].strip(),
                "time": r[1].strip(),
                "post_type": r[2].strip().upper(),
                "media_url": r[3].strip(),
                "caption": r[4].strip()
            })

    print(f"\n📦 Se encontraron {len(rows)} slots en meta_import.csv\n")

    scheduled_count = 0
    published_now_count = 0
    skipped_count = 0
    errors = []

    for idx, item in enumerate(rows, 1):
        dt_str = f"{item['date']} {item['time']}"
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M").replace(tzinfo=LOCAL_TZ)
        dt_utc = dt_local.astimezone(timezone.utc)
        ts = int(dt_utc.timestamp())

        diff_seconds = (dt_utc - now_utc).total_seconds()

        print(f"[{idx:02d}/{len(rows):02d}] {dt_str} ({item['post_type']}) - {Path(item['media_url']).name or 'Texto'}")

        # Slot 1 de hoy por la mañana (ya pasó hace horas)
        if diff_seconds < -3600:
            print(f"    ⏭️ Omitido (pasado por más de 1 hora: {dt_str})")
            skipped_count += 1
            continue

        # Si está en el rango de hace menos de 60 min o dentro de los próximos 10 min:
        # Meta no permite programar a menos de 10 min en el futuro. Se publica en vivo.
        publish_live = diff_seconds < 600
        publish_ts = None if publish_live else ts

        media_path = None
        if item["post_type"] in ("PHOTO", "VIDEO", "REEL"):
            media_path = find_asset(item["media_url"])
            if not media_path:
                msg = f"Archivo no encontrado para slot {dt_str}: {item['media_url']}"
                print(f"    ❌ {msg}")
                errors.append(msg)
                continue

        # Despachar
        if item["post_type"] in ("VIDEO", "REEL"):
            res = publisher.publish_video(media_path, item["caption"], publish_ts)
        elif item["post_type"] == "PHOTO":
            res = publisher.publish_photo(media_path, item["caption"], publish_ts)
        else:
            res = publisher.publish_text(item["caption"], publish_ts)

        if "id" in res:
            action = "Publicado en vivo" if publish_live else f"Programado ({dt_str})"
            print(f"    ✅ {action} - ID: {res['id']}")
            if publish_live:
                published_now_count += 1
            else:
                scheduled_count += 1
        else:
            err_msg = res.get("error", {}).get("message", str(res))
            print(f"    ❌ Error de Meta: {err_msg}")
            errors.append(f"{dt_str}: {err_msg}")

        time.sleep(1.5)

    print("\n" + "=" * 70)
    print("RESUMEN DE DESPACHO:")
    print(f"  • Programados a futuro: {scheduled_count}")
    print(f"  • Publicados en vivo (hoy): {published_now_count}")
    print(f"  • Omitidos (pasados): {skipped_count}")
    print(f"  • Errores: {len(errors)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
