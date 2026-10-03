#!/usr/bin/env python3
"""
Despacho semanal completo - Ejecutar LOCAL en Xubuntu (tiene Internet)
1. Descarga Google Doc manifesto
2. Actualiza meta_import.csv con textos oficiales
3. Despacha slots pendientes a Meta Graph API real
"""
import os
import sys
import csv
import json
import requests
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================

GROWTH_ROOT = Path(__file__).parent
TENANT_ROOT = GROWTH_ROOT / "tenants" / "firma-bordados"
ENV_PATH = TENANT_ROOT / ".env"
META_IMPORT_PATH = TENANT_ROOT / "meta_import.csv"
DRYRUN_PATH = GROWTH_ROOT / "dryrun_output.json"
GOOGLE_DRIVE_ASSETS = Path("/home/universe-sent-me/GoogleDrive/01 - Firma Assets")

# Google Doc ID del manifesto
GOOGLE_DOC_ID = "1i3jrmwerVeKLHOE5hpLTaTiBWBvSasrYBPqEgByER0U"
GOOGLE_DOC_EXPORT_URL = f"https://docs.google.com/document/d/{GOOGLE_DOC_ID}/export?format=txt"

# Zona horaria local (America/Matamoros = UTC-5)
LOCAL_TZ = timezone(timedelta(hours=-5))

# Slots ya programados (omitir)
SKIP_SLOTS = {"firma-bordados-20260902-evening-13"}  # Slot #13

@dataclass
class MetaResponse:
    success: bool
    post_id: Optional[str] = None
    status: str = "scheduled"
    error: Optional[str] = None
    raw_response: Optional[Dict] = None

# ==============================================================================
# CARGA .ENV
# ==============================================================================

def load_env_file(env_path: Path):
    if not env_path.exists():
        raise FileNotFoundError(f".env no encontrado: {env_path}")
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

load_env_file(ENV_PATH)

FB_PAGE_ID = os.environ.get("FB_PAGE_ID") or os.environ.get("META_PAGE_ID")
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN") or os.environ.get("META_PAGE_ACCESS_TOKEN")
META_API_VERSION = os.environ.get("META_API_VERSION", "v20.0")
META_BASE_URL = f"https://graph.facebook.com/{META_API_VERSION}"

if not FB_PAGE_ID or not META_ACCESS_TOKEN:
    raise ValueError("FB_PAGE_ID y META_ACCESS_TOKEN requeridos en .env")

# ==============================================================================
# 1. DESCARGAR GOOGLE DOC Y PARSEAR CONTENIDO OFICIAL
# ==============================================================================

def fetch_google_doc() -> str:
    """Descarga el Google Doc como texto plano."""
    logger.info(f"Descargando Google Doc: {GOOGLE_DOC_ID}")
    response = requests.get(GOOGLE_DOC_EXPORT_URL, timeout=30)
    response.raise_for_status()
    return response.text

def parse_manifesto(content: str) -> List[Dict[str, Any]]:
    """
    Parsea el contenido del manifesto para extraer posts oficiales.
    Formato esperado: líneas con fecha, hora, tipo, archivo, caption, hashtags, etc.
    """
    lines = content.strip().split('\n')
    posts = []
    
    # Buscar patrones típicos en el documento
    current_post = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detectar fecha (YYYY-MM-DD o DD/MM/YYYY)
        import re
        date_match = re.match(r'^(\d{4}-\d{2}-\d{2})[,\s]+(\d{2}:\d{2})', line)
        if date_match:
            if current_post:
                posts.append(current_post)
            current_post = {
                "date": date_match.group(1),
                "time": date_match.group(2),
                "raw_line": line
            }
            continue
        
        # Detectar tipo de post
        if line.upper().startswith(('PHOTO', 'VIDEO', 'REEL', 'TEXT', 'TEXT_ONLY')):
            current_post["post_type"] = line.split()[0].upper()
            continue
            
        # Detectar Media URL / archivo
        if line.lower().startswith(('media url', 'archivo', 'file:', 'imagen:', 'video:')):
            parts = line.split(':', 1)
            if len(parts) > 1:
                current_post["media_url"] = parts[1].strip()
            continue
        
        # Detectar caption/texto
        if line.lower().startswith(('caption', 'texto', 'copy:', 'mensaje:')):
            parts = line.split(':', 1)
            if len(parts) > 1:
                current_post["caption"] = parts[1].strip()
            continue
            
        # Si no coincide con campos conocidos, tratar como continuación de caption
        if current_post and "caption" in current_post and not line.upper().startswith(('HASHTAG', 'LINK', 'URL')):
            current_post["caption"] += " " + line
    
    if current_post:
        posts.append(current_post)
    
    logger.info(f"Parseados {len(posts)} posts del manifesto")
    return posts

def parse_manifesto_structured(content: str) -> List[Dict[str, Any]]:
    """
    Parser más robusto para formato tabla/CSV-like del documento.
    """
    import re
    posts = []
    
    # Buscar patrones de fila: fecha, hora, tipo, archivo, texto
    # El documento suele tener formato tabular
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Intentar parsear como CSV-like (separado por tabs o comas)
        # Formato típico: 2026-09-03\t14:30\tPHOTO\tarchivo.png\t"Caption..."
        parts = re.split(r'\t+|,{2,}', line)  # tabs o múltiples comas
        
        if len(parts) >= 4:
            date_str = parts[0].strip()
            time_str = parts[1].strip()
            post_type = parts[2].strip().upper()
            media_url = parts[3].strip() if len(parts) > 3 else ""
            caption = parts[4].strip() if len(parts) > 4 else ""
            
            # Validar fecha
            if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                posts.append({
                    "date": date_str,
                    "time": time_str,
                    "post_type": post_type,
                    "media_url": media_url,
                    "caption": caption,
                })
    
    # Si no funcionó, buscar patrón más simple línea por línea
    if not posts:
        # Buscar líneas con fecha y hora
        for line in lines:
            match = re.match(r'(\d{4}-\d{2}-\d{2})[\s,]+(\d{2}:\d{2})[\s,]+(\w+)[\s,]+(.+)', line)
            if match:
                posts.append({
                    "date": match.group(1),
                    "time": match.group(2),
                    "post_type": match.group(3).upper(),
                    "media_url": "",
                    "caption": match.group(4),
                })
    
    logger.info(f"Posts estructurados parseados: {len(posts)}")
    return posts

# ==============================================================================
# 2. ACTUALIZAR META_IMPORT.CSV CON CONTENIDO OFICIAL
# ==============================================================================

def update_meta_import_from_manifesto(manifesto_posts: List[Dict]) -> int:
    """
    Actualiza meta_import.csv con los posts del manifesto oficial.
    Mantiene formato CSV compatible con deploy_local.py.
    """
    # Cargar schedule actual para saber qué slots existen
    with open(DRYRUN_PATH, "r", encoding="utf-8") as f:
        dryrun = json.load(f)
    
    schedule = dryrun.get("schedule", [])
    
    # Crear mapeo de slots por fecha/hora local
    slot_by_datetime = {}
    for slot in schedule:
        dt_local = slot.get("datetime_local", "")
        if dt_local:
            # datetime_local viene como "2026-09-03T14:00:00+00:00" (en realidad es local sin offset)
            # Extraer fecha y hora
            try:
                dt = datetime.fromisoformat(dt_local.replace("Z", "+00:00"))
                key = f"{dt.date()}_{dt.strftime('%H:%M')}"
                slot_by_datetime[key] = slot
            except:
                pass
    
    # Preparar filas para CSV
    csv_rows = []
    whatsapp = "878 788 0735"
    whatsapp_e164 = "5218787880735"
    hashtags = "#FirmaBordados #BordadoPersonalizado #UniformesCorporativos #PiedrasNegras #EaglePass #Bordados #Embroidery"
    location = "Piedras Negras, Coahuila, México"
    link_url = f"https://wa.me/{whatsapp_e164}"
    first_comment = f"Cotiza por WhatsApp: {whatsapp}"
    
    for post in manifesto_posts:
        date_str = post.get("date", "")
        time_str = post.get("time", "")
        post_type = post.get("post_type", "PHOTO")
        media_url = post.get("media_url", "")
        caption = post.get("caption", "")
        
        # Normalizar tipo
        if post_type in ("VIDEO", "REEL"):
            post_type = "VIDEO"
        elif post_type in ("TEXT", "TEXT_ONLY"):
            post_type = "TEXT_ONLY"
            media_url = ""
        else:
            post_type = "PHOTO"
        
        # Buscar slot correspondiente para obtener source_filename si no hay media_url
        key = f"{date_str}_{time_str}"
        slot = slot_by_datetime.get(key)
        if slot and not media_url:
            media_url = slot.get("source_filename", "")
        
        # Si aún no hay media_url para PHOTO/VIDEO, buscar en assets por fecha
        if post_type in ("PHOTO", "VIDEO") and not media_url:
            # Intentar inferir nombre de archivo
            pass
        
        csv_rows.append({
            "Date (YYYY-MM-DD)": date_str,
            "Time (HH:MM, 24h)": time_str,
            "Timezone": "America/Matamoros",
            "Post Type": post_type,
            "Media URL": media_url,
            "Caption": caption,
            "Link URL": link_url,
            "Hashtags": hashtags,
            "Location": location,
            "First Comment": first_comment,
        })
    
    # Escribir CSV
    fieldnames = ["Date (YYYY-MM-DD)", "Time (HH:MM, 24h)", "Timezone", "Post Type", 
                  "Media URL", "Caption", "Link URL", "Hashtags", "Location", "First Comment"]
    
    with open(META_IMPORT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    logger.info(f"meta_import.csv actualizado con {len(csv_rows)} posts oficiales")
    return len(csv_rows)

# ==============================================================================
# 3. FUNCIONES DE DESPACHO (COPIADAS DE deploy_local.py)
# ==============================================================================

def build_scheduled_time(datetime_utc: str) -> int:
    dt = datetime.fromisoformat(datetime_utc.replace("Z", "+00:00"))
    return int(dt.timestamp())

def utc_to_local_key(datetime_utc: str) -> str:
    dt = datetime.fromisoformat(datetime_utc.replace("Z", "+00:00"))
    local = dt.astimezone(LOCAL_TZ)
    return f"{local.date()}_{local.strftime('%H:%M')}"

def load_dryrun_schedule(path: Path) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f).get("schedule", [])

def load_meta_import_csv(path: Path) -> Dict[str, Dict]:
    result = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            media_url = row.get("Media URL", "").strip()
            if media_url:
                result[media_url] = {
                    "caption": row.get("Caption", "").strip(),
                    "hashtags": row.get("Hashtags", "").strip(),
                    "link_url": row.get("Link URL", "").strip(),
                    "post_type": row.get("Post Type", "").strip(),
                    "date": row.get("Date (YYYY-MM-DD)", "").strip(),
                    "time": row.get("Time (HH:MM, 24h)", "").strip(),
                    "timezone": row.get("Timezone", "America/Matamoros").strip(),
                    "first_comment": row.get("First Comment", "").strip(),
                }
            else:
                key = f"{row.get('Date (YYYY-MM-DD)', '').strip()}_{row.get('Time (HH:MM, 24h)', '').strip()}"
                result[key] = {
                    "caption": row.get("Caption", "").strip(),
                    "hashtags": row.get("Hashtags", "").strip(),
                    "link_url": row.get("Link URL", "").strip(),
                    "post_type": row.get("Post Type", "").strip(),
                    "date": row.get("Date (YYYY-MM-DD)", "").strip(),
                    "time": row.get("Time (HH:MM, 24h)", "").strip(),
                    "timezone": row.get("Timezone", "America/Matamoros").strip(),
                    "first_comment": row.get("First Comment", "").strip(),
                }
    return result

def find_asset_recursive(base_dir: Path, filename: str) -> Optional[Path]:
    if not base_dir.exists():
        return None
    for root, dirs, files in os.walk(base_dir):
        if filename in files:
            return Path(root) / filename
    return None

def get_slot_meta_data(slot: Dict, meta_import: Dict) -> Dict:
    source_filename = slot.get("source_filename")
    datetime_utc = slot.get("datetime_utc", "")
    
    if source_filename and source_filename in meta_import:
        return meta_import[source_filename]
    
    if not source_filename:
        local_key = utc_to_local_key(datetime_utc)
        if local_key in meta_import:
            return meta_import[local_key]
        logger.warning(f"Clave local no encontrada: {local_key}")
    
    return {
        "caption": slot.get("description", ""),
        "link_url": slot.get("whatsapp_e164") and f"https://wa.me/{slot['whatsapp_e164']}",
        "post_type": "TEXT_ONLY" if not source_filename else "PHOTO",
    }

def resolve_asset(slot: Dict, meta_import: Dict) -> Optional[Path]:
    source_filename = slot.get("source_filename")
    if not source_filename:
        return None
    
    found = find_asset_recursive(GOOGLE_DRIVE_ASSETS, source_filename)
    if found:
        return found
    
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
# 4. PUBLICADOR META REAL
# ==============================================================================

class LocalMetaPublisher:
    def __init__(self, page_id: str, access_token: str):
        self.page_id = page_id
        self.access_token = access_token
        self.base_url = META_BASE_URL
        self._ensure_page_token()
    
    def _ensure_page_token(self):
        try:
            logger.info("Validando Page Token...")
            url = f"{self.base_url}/{self.page_id}?fields=access_token&access_token={self.access_token}"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if "access_token" in result:
                    self.access_token = result["access_token"]
                    logger.info("✅ Page Token validado")
                    return
            logger.warning(f"Token validation: {response.status_code}")
        except Exception as e:
            logger.warning(f"Excepción validando token: {e}")
    
    def _make_request(self, endpoint: str, data: Dict, files: Optional[Dict] = None) -> MetaResponse:
        url = f"{self.base_url}/{endpoint}"
        data["access_token"] = self.access_token
        try:
            if files:
                response = requests.post(url, files=files, data=data, timeout=120)
            else:
                response = requests.post(url, data=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            post_id = result.get("id") or result.get("post_id")
            return MetaResponse(success=True, post_id=post_id, status="scheduled", raw_response=result)
        except requests.exceptions.HTTPError as e:
            error_detail = e.response.json() if e.response.headers.get('content-type','').startswith('application/json') else e.response.text
            return MetaResponse(success=False, error=f"HTTP {e.response.status_code}: {error_detail}", raw_response={"status_code": e.response.status_code, "error": error_detail})
        except Exception as e:
            return MetaResponse(success=False, error=f"Request error: {str(e)}", raw_response={"error": str(e)})
    
    def publish_text(self, message: str, scheduled_publish_time: str, link: Optional[str] = None) -> MetaResponse:
        scheduled_ts = build_scheduled_time(scheduled_publish_time)
        payload = {"message": message, "published": "false", "scheduled_publish_time": str(scheduled_ts)}
        if link: payload["link"] = link
        return self._make_request(f"{self.page_id}/feed", payload)
    
    def publish_photo(self, image_path: Path, caption: str, scheduled_publish_time: str) -> MetaResponse:
        scheduled_ts = build_scheduled_time(scheduled_publish_time)
        if not image_path.exists():
            return MetaResponse(success=False, error=f"Archivo no encontrado: {image_path}")
        payload = {"caption": caption, "published": "false", "scheduled_publish_time": str(scheduled_ts)}
        with open(image_path, "rb") as f:
            files = {"source": (image_path.name, f, "image/jpeg")}
            return self._make_request(f"{self.page_id}/photos", payload, files)
    
    def publish_video(self, video_path: Path, description: str, scheduled_publish_time: str, title: Optional[str] = None) -> MetaResponse:
        scheduled_ts = build_scheduled_time(scheduled_publish_time)
        if not video_path.exists():
            return MetaResponse(success=False, error=f"Archivo no encontrado: {video_path}")
        payload = {"description": description, "published": "false", "scheduled_publish_time": str(scheduled_ts)}
        if title: payload["title"] = title
        with open(video_path, "rb") as f:
            files = {"source": (video_path.name, f, "video/mp4")}
            return self._make_request(f"{self.page_id}/videos", payload, files)

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 70)
    print("DESPACHO SEMANAL COMPLETO - Growth OS (Ejecución Local)")
    print("=" * 70)
    print()
    
    # Validar credenciales
    if not FB_PAGE_ID or not META_ACCESS_TOKEN:
        print("❌ Credenciales faltantes en .env")
        sys.exit(1)
    
    # 1. Descargar y parsear manifesto
    print("[1/4] Descargando manifesto oficial desde Google Docs...")
    try:
        doc_content = fetch_google_doc()
        manifesto_posts = parse_manifesto_structured(doc_content)
        if not manifesto_posts:
            # Intentar parser simple
            manifesto_posts = parse_manifesto(doc_content)
        
        if not manifesto_posts:
            print("⚠️  No se pudieron parsear posts del manifesto. Usando meta_import.csv actual.")
        else:
            print(f"    ✅ {len(manifesto_posts)} posts extraídos del manifesto")
            print("[2/4] Actualizando meta_import.csv con textos oficiales...")
            update_meta_import_from_manifesto(manifesto_posts)
    except Exception as e:
        logger.warning(f"No se pudo descargar manifesto: {e}. Usando meta_import.csv actual.")
    
    # 2. Cargar datos
    print("[3/4] Cargando schedule y meta_import...")
    schedule = load_dryrun_schedule(DRYRUN_PATH)
    meta_import = load_meta_import_csv(META_IMPORT_PATH)
    
    # Filtrar slots futuros (desde hoy 20:00 en adelante) - omitir #13
    now_utc = datetime.now(timezone.utc)
    target_schedule = []
    for slot in schedule:
        slot_id = slot.get("slot_id", "")
        if slot_id in SKIP_SLOTS:
            continue
        dt_utc = datetime.fromisoformat(slot["datetime_utc"].replace("Z", "+00:00"))
        if dt_utc >= now_utc:
            target_schedule.append(slot)
    
    print(f"    Slots a despachar: {len(target_schedule)}")
    for s in target_schedule:
        print(f"      - {s['slot_id']} ({s['slot_type']}) @ {s['datetime_local']}")
    
    # 3. Desplegar
    print("[4/4] Despachando a Meta Graph API (MODO REAL)...")
    publisher = LocalMetaPublisher(FB_PAGE_ID, META_ACCESS_TOKEN)
    
    results = []
    for slot in target_schedule:
        slot_id = slot.get("slot_id")
        slot_type = slot.get("slot_type")
        datetime_utc = slot.get("datetime_utc")
        source_filename = slot.get("source_filename")
        
        print(f"\n{'='*70}")
        print(f"📤 {slot_id} | {slot_type} | {datetime_utc}")
        if source_filename:
            print(f"   Asset: {source_filename}")
        
        meta_data = get_slot_meta_data(slot, meta_import)
        caption = meta_data.get("caption", slot.get("description", ""))
        link = meta_data.get("link_url", "")
        
        try:
            if slot_type == "text":
                result = publisher.publish_text(caption, datetime_utc, link if link else None)
            elif slot_type == "media":
                asset_path = resolve_asset(slot, meta_import)
                is_video = source_filename and source_filename.endswith(".mp4")
                if not asset_path:
                    result = MetaResponse(success=False, error=f"Asset no encontrado: {source_filename}")
                elif is_video:
                    result = publisher.publish_video(asset_path, caption, datetime_utc, slot.get("asset_ref"))
                else:
                    result = publisher.publish_photo(asset_path, caption, datetime_utc)
            else:
                result = MetaResponse(success=False, error=f"Tipo desconocido: {slot_type}")
            
            results.append((slot_id, result))
            if result.success:
                print(f"   ✅ Post ID: {result.post_id}")
            else:
                print(f"   ❌ {result.error}")
        except Exception as e:
            result = MetaResponse(success=False, error=str(e))
            results.append((slot_id, result))
            print(f"   ❌ Excepción: {e}")
        
        import time
        time.sleep(1)  # Rate limit
    
    # Tabla final
    print("\n" + "=" * 70)
    print("RESULTADOS FINALES - Post IDs Confirmados")
    print("=" * 70)
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
        print("\n🎉 ¡Semana completa despachada!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {len(results) - success_count} slots fallaron")
        sys.exit(1)

if __name__ == "__main__":
    main()
