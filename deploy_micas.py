#!/usr/bin/env python3
"""
Despachador Local para Mica's Art & Deco - Facebook Meta Scheduler
Lee future_schedule.csv y programa publicaciones en Meta Graph API.
"""

import os
import sys
import csv
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta

from growth.meta_publisher import MetaPublisher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GROWTH_ROOT = Path(__file__).resolve().parent
TENANT_DIR = GROWTH_ROOT / "tenants" / "micas-art-deco"
ENV_PATH = TENANT_DIR / ".env"
ASSETS_DIR = TENANT_DIR / "assets"

env_vars = {}
if ENV_PATH.exists():
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip().strip("'\"")

PAGE_ID = env_vars.get("FB_PAGE_ID")
ACCESS_TOKEN = env_vars.get("PAGE_ACCESS_TOKEN") or env_vars.get("META_ACCESS_TOKEN")
LOCAL_TZ = timezone(timedelta(hours=-5))

def find_asset_recursive(base_dir: Path, filename: str):
    for root, dirs, files in os.walk(base_dir, followlinks=True):
        if filename in files:
            return Path(root) / filename
    return None

def main():
    dry_run = "--live" not in sys.argv
    csv_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    
    if csv_args:
        csv_file = Path(csv_args[0])
    else:
        csv_file = TENANT_DIR / "future_schedule.csv"

    print("=" * 65)
    print(" DESPACHADOR MICA'S ART & DECO - FACEBOOK SCHEDULER")
    print("=" * 65)
    print(f"Modo: {'🔍 DRY-RUN (Simulación)' if dry_run else '🚀 EN VIVO (Programación real en Meta)'}")
    print(f"Página ID: {PAGE_ID}")
    print(f"CSV de entrada: {csv_file}")
    print(f"Directorio de Assets: {ASSETS_DIR}\n")

    if not PAGE_ID or not ACCESS_TOKEN:
        print("❌ ERROR: Credenciales FB_PAGE_ID o PAGE_ACCESS_TOKEN no encontradas en .env")
        sys.exit(1)

    if not csv_file.exists():
        print(f"❌ ERROR: Archivo CSV no encontrado: {csv_file}")
        sys.exit(1)

    slots = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slots.append(row)

    print(f"Se procesarán {len(slots)} publicaciones:\n")

    publisher = MetaPublisher(
        page_id=PAGE_ID,
        access_token=ACCESS_TOKEN,
        dry_run=dry_run
    )

    for i, s in enumerate(slots, 1):
        fecha_str = s.get("Date (YYYY-MM-DD)", "").strip()
        hora_str = s.get("Time (HH:MM, 24h)", "").strip()
        asset_name = s.get("Media URL", "").strip()
        caption = s.get("Caption", "").strip()
        link_url = s.get("Link URL", "").strip()
        hashtags = s.get("Hashtags", "").strip()
        
        # En Facebook el link de compra sí es cliqueable en el cuerpo del post
        parts = [caption]
        if link_url:
            parts.append(f"🛒 Adquiere esta pieza en línea aquí: {link_url}")
        if hashtags:
            parts.append(hashtags)
        full_caption = "\n\n".join(parts).strip()

        dt_local = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M")
        dt_local = dt_local.replace(tzinfo=LOCAL_TZ)
        dt_utc = dt_local.astimezone(timezone.utc)
        scheduled_ts = int(dt_utc.timestamp())

        asset_path = find_asset_recursive(ASSETS_DIR, asset_name)

        print(f"[{i}/{len(slots)}] {fecha_str} {hora_str} (Local) -> {dt_utc.strftime('%H:%M')} UTC")
        print(f"   Asset: {'✅ ' + str(asset_path.name) if asset_path else '❌ NO ENCONTRADO: ' + asset_name}")

        if not asset_path:
            print("   ⚠️  Omitiendo por falta de asset...")
            print("-" * 65)
            continue

        if dry_run:
            print("   🔍 [DRY-RUN] Validación correcta de parámetros y fechas.")
        else:
            print("   📤 Programando en Fan Page de Facebook...")
            res = publisher.publish_photo(
                image_path=asset_path,
                caption=full_caption,
                scheduled_publish_time=scheduled_ts
            )
            if res.success:
                print(f"   ✅ Programado con éxito! Post ID: {res.post_id}")
            else:
                print(f"   ❌ Error al programar: {res.error}")
        print("-" * 65)

if __name__ == "__main__":
    main()
