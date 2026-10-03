#!/usr/bin/env python3
"""
Despachador Local Directo - Publica slots pendientes directamente a Meta Graph API
desde la terminal local (sin VM GCP).

Ejecuta: python3 deploy_local.py

NOTA: Usa growth.meta_publisher.MetaPublisher como implementación canónica.
"""

import os
import sys
import csv
import json
import logging
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Union

# Importar publisher unificado
from growth.meta_publisher import (
    MetaPublisher,
    MetaResponse,
    load_dryrun_schedule,
    load_meta_import_csv,
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==============================================================================
# CONFIGURACIÓN Y CARGA DE CREDENCIALES
# ==============================================================================

def load_env_file(env_path: Path) -> bool:
    """Carga variables de entorno desde .env."""
    if not env_path.exists():
        logger.warning(f"Env file no encontrado: {env_path}")
        return False
    
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                # Expandir variables ${VAR} o $VAR
                import re
                value = re.sub(r'\$\{(\w+)\}', lambda m: os.environ.get(m.group(1), ''), value)
                value = re.sub(r'\$(\w+)', lambda m: os.environ.get(m.group(1), ''), value)
                os.environ[key] = value
        logger.info(f"Cargado: {env_path}")
        return True
    except Exception as e:
        logger.error(f"Error cargando {env_path}: {e}")
        return False


# Cargar .env del tenant
TENANT_ENV = Path(__file__).parent / "tenants" / "firma-bordados" / ".env"
load_env_file(TENANT_ENV)

# Configuración
FB_PAGE_ID = os.environ.get("FB_PAGE_ID") or os.environ.get("META_PAGE_ID", "")
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN") or os.environ.get("META_PAGE_ACCESS_TOKEN", "")
META_API_VERSION = os.environ.get("META_API_VERSION", "v20.0")
META_BASE_URL = f"https://graph.facebook.com/{META_API_VERSION}"

# Zona horaria local (America/Matamoros = UTC-5)
LOCAL_TZ = timezone(timedelta(hours=-5))

# Rutas
GROWTH_ROOT = Path(__file__).parent
DRYRUN_PATH = GROWTH_ROOT / "dryrun_output.json"
META_IMPORT_PATH = GROWTH_ROOT / "tenants" / "firma-bordados" / "meta_import.csv"
GOOGLE_DRIVE_ASSETS = Path("/home/universe-sent-me/GoogleDrive/01 - Firma Assets")

# Slots a desplegar (omitir #13)
TARGET_SLOTS = [
    "firma-bordados-20260903-afternoon-11", # #11 PHOTO
    "firma-bordados-20260904-evening-12",   # #12 PHOTO
    "firma-bordados-20260904-afternoon-14", # #14 PHOTO
    "firma-bordados-20260905-evening-15",   # #15 VIDEO_REEL
    "firma-bordados-20260905-morning-16",   # #16 PHOTO
    "firma-bordados-20260905-afternoon-17", # #17 TEXT_ONLY
    "firma-bordados-20260906-morning-18",   # #18 TEXT_ONLY
    "firma-bordados-20260906-afternoon-19", # #19 TEXT_ONLY
    "firma-bordados-20260907-evening-20",   # #20 TEXT_ONLY
]


# ==============================================================================
# UTILIDADES
# ==============================================================================

def find_asset_recursive(base_dir: Path, filename: str) -> Optional[Path]:
    """Busca archivo recursivamente en base_dir."""
    if not base_dir.exists():
        return None
    for root, dirs, files in os.walk(base_dir):
        if filename in files:
            return Path(root) / filename
    return None


def get_slot_meta_data(slot: Dict[str, Any], meta_import: Dict[str, Dict]) -> Dict[str, Any]:
    """Obtiene datos oficiales del slot desde meta_import.csv."""
    source_filename = slot.get("source_filename")
    datetime_utc = slot.get("datetime_utc", "")
    
    if source_filename and source_filename in meta_import:
        return meta_import[source_filename]
    
    # Fallback para TEXT_ONLY: convertir UTC a local y buscar
    if not source_filename:
        local_key = utc_to_local_key(datetime_utc)
        if local_key in meta_import:
            return meta_import[local_key]
        logger.warning(f"Clave local no encontrada en meta_import: {local_key}")
    
    # Fallback a dryrun
    return {
        "caption": slot.get("description", ""),
        "link_url": slot.get("whatsapp_e164") and f"https://wa.me/{slot['whatsapp_e164']}",
        "post_type": "TEXT_ONLY" if not source_filename else "PHOTO",
    }


def resolve_asset(slot: Dict[str, Any], meta_import: Dict[str, Dict]) -> Optional[Path]:
    """Resuelve la ruta del asset en Google Drive."""
    source_filename = slot.get("source_filename")
    if not source_filename:
        return None
    
    # 1. Buscar directamente por filename en Google Drive
    found = find_asset_recursive(GOOGLE_DRIVE_ASSETS, source_filename)
    if found:
        return found
    
    # 2. Fallback: buscar por Media URL del meta_import
    if source_filename in meta_import:
        media_url = meta_import[source_filename].get("Media URL", "").strip()
        if media_url:
            media_name = Path(media_url).name
            found = find_asset_recursive(GOOGLE_DRIVE_ASSETS, media_name)
            if found:
                return found
    
    logger.warning(f"Asset no encontrado: {source_filename}")
    return None


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 70)
    print("DESPACHADOR LOCAL - Growth OS")
    print("=" * 70)
    print()
    
    # Validar credenciales
    if not FB_PAGE_ID or not META_ACCESS_TOKEN:
        print("❌ ERROR: Credenciales no configuradas en tenants/firma-bordados/.env")
        print("   FB_PAGE_ID y META_ACCESS_TOKEN son requeridos")
        sys.exit(1)
    
    if not DRYRUN_PATH.exists():
        print(f"❌ ERROR: {DRYRUN_PATH} no encontrado")
        sys.exit(1)
    
    if not META_IMPORT_PATH.exists():
        print(f"❌ ERROR: {META_IMPORT_PATH} no encontrado")
        sys.exit(1)
    
    if not GOOGLE_DRIVE_ASSETS.exists():
        print(f"❌ ERROR: Google Drive no montado en {GOOGLE_DRIVE_ASSETS}")
        sys.exit(1)
    
    print(f"📄 Page ID: {FB_PAGE_ID[:20]}...")
    print(f"🔑 Access Token: {META_ACCESS_TOKEN[:20]}...")
    print(f"📂 Google Drive: {GOOGLE_DRIVE_ASSETS}")
    print(f"📋 Slots objetivo: {len(TARGET_SLOTS)}")
    print()
    
    # Cargar datos
    schedule = load_dryrun_schedule(DRYRUN_PATH)
    meta_import = load_meta_import_csv(META_IMPORT_PATH)
    
    # Filtrar solo slots objetivo
    target_schedule = [s for s in schedule if s.get("slot_id") in TARGET_SLOTS]
    
    if len(target_schedule) != len(TARGET_SLOTS):
        found_ids = {s["slot_id"] for s in target_schedule}
        missing = [s for s in TARGET_SLOTS if s not in found_ids]
        print(f"⚠️  ADVERTENCIA: Slots no encontrados en dryrun: {missing}")
    
    # Inicializar publicador unificado
    publisher = MetaPublisher(
        page_id=FB_PAGE_ID,
        access_token=META_ACCESS_TOKEN,
        dry_run=False,  # Modo real
    )
    
    # Desplegar cada slot
    results = []
    
    for slot in target_schedule:
        slot_id = slot.get("slot_id")
        slot_type = slot.get("slot_type")
        datetime_utc = slot.get("datetime_utc")
        source_filename = slot.get("source_filename")
        
        print(f"\n{'='*70}")
        print(f"📤 Desplegando: {slot_id}")
        print(f"   Tipo: {slot_type} | Fecha UTC: {datetime_utc}")
        if source_filename:
            print(f"   Asset: {source_filename}")
        print(f"{'='*70}")
        
        # Obtener datos oficiales
        meta_data = get_slot_meta_data(slot, meta_import)
        caption = meta_data.get("caption", slot.get("description", ""))
        link = meta_data.get("link_url", "")
        
        try:
            if slot_type == "text":
                # TEXT_ONLY
                result = publisher.publish_text(
                    message=caption,
                    scheduled_publish_time=datetime_utc,
                    link=link if link else None,
                )
                
            elif slot_type == "media":
                asset_path = resolve_asset(slot, meta_import)
                is_video = source_filename and source_filename.endswith(".mp4")
                
                if not asset_path:
                    result = MetaResponse(
                        success=False,
                        error=f"Asset no encontrado en Google Drive: {source_filename}"
                    )
                elif is_video:
                    result = publisher.publish_video(
                        video_path=asset_path,
                        description=caption,
                        scheduled_publish_time=datetime_utc,
                        title=slot.get("asset_ref"),
                    )
                else:
                    result = publisher.publish_photo(
                        image_path=asset_path,
                        caption=caption,
                        scheduled_publish_time=datetime_utc,
                    )
            else:
                result = MetaResponse(
                    success=False,
                    error=f"Tipo desconocido: {slot_type}"
                )
            
            results.append((slot_id, result))
            
            if result.success:
                print(f"✅ ÉXITO - Post ID: {result.post_id}")
            else:
                print(f"❌ FALLO - {result.error}")
                if result.raw_response:
                    print(f"   Detalle: {json.dumps(result.raw_response, ensure_ascii=False)[:300]}")
        
        except Exception as e:
            result = MetaResponse(success=False, error=f"Excepción: {e}")
            results.append((slot_id, result))
            print(f"❌ EXCEPCIÓN - {e}")
        
        # Pausa entre publicaciones para no saturar API
        time.sleep(1)
    
    # Tabla final
    print("\n" + "=" * 70)
    print("RESULTADOS FINALES - Post IDs Confirmados")
    print("=" * 70)
    print()
    print(f"{'#':>2} | {'Slot ID':<42} | {'Post ID':<30} | {'Status'}")
    print("-" * 70)
    
    success_count = 0
    for i, (slot_id, result) in enumerate(results, 1):
        post_id = result.post_id or "N/A"
        status = "✅ OK" if result.success else "❌ FAIL"
        print(f"{i:>2} | {slot_id:<42} | {post_id:<30} | {status}")
        if result.success:
            success_count += 1
    
    print("-" * 70)
    print(f"\nTotal: {success_count}/{len(results)} publicados exitosamente")
    
    if success_count == len(results):
        print("\n🎉 ¡Todos los slots desplegados correctamente!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {len(results) - success_count} slots fallaron")
        sys.exit(1)


def utc_to_local_key(datetime_utc: str) -> str:
    """Convierte datetime UTC a key local (YYYY-MM-DD_HH:MM) para lookup en meta_import.csv."""
    dt = datetime.fromisoformat(datetime_utc.replace("Z", "+00:00"))
    local = dt.astimezone(LOCAL_TZ)
    return f"{local.date()}_{local.strftime('%H:%M')}"


if __name__ == "__main__":
    main()
