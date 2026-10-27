"""
Meta Graph API Publisher Adapter - Arquitectura desacoplada, modo dual.

Este módulo construye requests para Meta Graph API sin realizar llamadas de red
en modo dry-run (default). Listo para activar cuando se disponga de credenciales.
"""
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import json
import os
import argparse
import sys
import requests
from datetime import datetime, timezone
from dataclasses import dataclass
import csv


# ==============================================================================
# CARGA AUTOMÁTICA DE CREDENCIALES DESDE .ENV
# ==============================================================================

ENV_SEARCH_PATHS = [
    # Tenant .env específico
    "tenants/firma-bordados/.env",
    # .env local del proyecto
    ".env",
]

DEFAULT_ENV_NAME = ".env"


def load_env_file(env_path: str, project_root: Optional[str] = None) -> bool:
    """
    Carga variables de entorno desde un archivo .env y las establece en os.environ.
    
    Args:
        env_path: Ruta relativa o absoluta al archivo .env
        project_root: Directorio raíz del proyecto (para paths relativos)
    
    Returns:
        True si se cargó exitosamente, False en caso contrario
    """
    # Convertir a Path
    env_file = Path(env_path)
    
    # Si es ruta relativa y hay project_root, usarlo como base
    if not env_file.is_absolute() and project_root:
        env_file = Path(project_root) / env_path
    
    if not env_file.exists():
        logger.debug(f"Env file not found: {env_file}")
        return False
    
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Saltar líneas vacías y comentarios
                if not line or line.startswith("#"):
                    continue
                # Saltar líneas sin igual
                if "=" not in line:
                    continue
                
                # Dividir el nombre de la variable y el valor
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                
                # Detectar y reemplazar variables de entorno en el valor
                import re
                value = re.sub(r'\{\{(.*?)\}\}', lambda m: os.environ.get(m.group(1), ''), value)
                value = re.sub(r'\$(\w+)', lambda m: os.environ.get(m.group(1), ''), value)
                
                # Establecer en os.environ
                os.environ[key] = value
                
        logger.debug(f"Loaded env variables from: {env_file}")
        return True
        
    except Exception as e:
        logger.warning(f"Failed to load env file {env_file}: {e}")
        return False


def load_integration_env(project_root: Optional[str] = None) -> bool:
    """
    Carga las credenciales de Meta para despliegues remotos.
    
    Busca en orden:
    1. tenants/firma-bordados/.env (prioridad para tenant específico)
    2. .env (variables de configuración general)
    
    Establece las siguientes variables en os.environ:
    - FB_PAGE_ID
    - META_ACCESS_TOKEN
    - META_PAGE_ID (opcional, puede usarse como alternativa a FB_PAGE_ID)
    - META_PAGE_ACCESS_TOKEN (opcional, puede usarse como alternativa a META_ACCESS_TOKEN)
    - META_DRY_RUN
    - META_API_VERSION
    
    Args:
        project_root: Directorio raíz del proyecto (default: directorio actual)
    
    Returns:
        True si se cargó al menos un archivo .env válido, False en caso contrario
    """
    loaded = False
    
    # Buscar en tenant/firma-bordados/.env primero
    if load_env_file("tenants/firma-bordados/.env", project_root):
        loaded = True
    
    # Intentar cargar .env local (por si existe)
    if not loaded and load_env_file(".env", project_root):
        loaded = True
    
    # Si no se encontraron archivos, intentar buscar en directorios superiores
    if not loaded:
        current = Path.cwd()
        for parent in [current, current.parent, current.parent.parent]:
            for env_path in ENV_SEARCH_PATHS:
                env_file = parent / env_path
                if env_file.exists():
                    if load_env_file(str(env_file), str(parent)):
                        loaded = True
                        break
            if loaded:
                break
    
    # Si no se cargó nada, levantar advertencia
    if not loaded:
        logger.debug("No .env files found for Meta credentials")
    else:
        logger.debug(f"Loaded Meta credentials from {loaded} env file(s)")
    
    return loaded


# NO cargar automáticamente al importar - dejar que el caller decida
# load_integration_env()


# ==============================================================================
# CONFIGURACIÓN POR VARIABLES DE ENTORNO (con defaults seguros)
# ==============================================================================

# Variables de entorno globales (se pueden sobrescribir manualmente)
# Default dry_run = True para seguridad (tests y uso por defecto)
META_DRY_RUN = os.environ.get("META_DRY_RUN", "true").lower() == "true"
FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "")
META_PAGE_ID = os.environ.get("META_PAGE_ID", "")  # Alternativa a FB_PAGE_ID
META_PAGE_ACCESS_TOKEN = os.environ.get("META_PAGE_ACCESS_TOKEN", "")  # Alternativa a META_ACCESS_TOKEN
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN", "")
META_API_VERSION = os.environ.get("META_API_VERSION", "v20.0")
META_BASE_URL = f"https://graph.facebook.com/{META_API_VERSION}"


# ==============================================================================
# CLASES Y TIPOS
# ==============================================================================

@dataclass
class MetaResponse:
    """Respuesta estandarizada de Meta Graph API."""
    success: bool
    post_id: Optional[str] = None
    status: str = "scheduled"
    error: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


class MetaPublisher:
    """
    Publicador para Meta Graph API con modo dry-run.
    
    En dry-run (default): no hace llamadas HTTP, devuelve respuestas mock.
    En modo real: requiere META_PAGE_ID o FB_PAGE_ID y META_ACCESS_TOKEN o META_PAGE_ACCESS_TOKEN.
    """
    
    def __init__(
        self,
        page_id: Optional[str] = None,
        access_token: Optional[str] = None,
        dry_run: Optional[bool] = None,
        api_version: Optional[str] = None,
    ):
        """
        Inicializa el publicador de Meta.
        
        Prioridad de credenciales:
        1. Parámetros pasados al constructor
        2. META_PAGE_ID o FB_PAGE_ID
        3. META_PAGE_ACCESS_TOKEN o META_ACCESS_TOKEN
        
        Args:
            page_id: Page ID (usa META_PAGE_ID o FB_PAGE_ID si no se proporciona)
            access_token: Access token (usa META_PAGE_ACCESS_TOKEN o META_ACCESS_TOKEN si no se proporciona)
            dry_run: Forzar modo dry-run (usa META_DRY_RUN si no se proporciona)
            api_version: Versión de la API de Meta (usa META_API_VERSION si no se proporciona)
        """
        # Prioridad de page_id: parámetro > META_PAGE_ID > FB_PAGE_ID
        self.page_id = (page_id or 
                       os.getenv("META_PAGE_ID") or 
                       os.getenv("FB_PAGE_ID"))
        
        # Prioridad de access_token: parámetro > META_PAGE_ACCESS_TOKEN > META_ACCESS_TOKEN
        self.access_token = (access_token or 
                            os.getenv("META_PAGE_ACCESS_TOKEN") or 
                            os.getenv("META_ACCESS_TOKEN"))
        
        # Determinar modo dry-run - default True para seguridad
        dry_run_str = os.getenv("META_DRY_RUN", "true").lower() in ("true", "1", "yes", "on")
        self.dry_run = dry_run if dry_run is not None else dry_run_str
        
        self.api_version = api_version or os.environ.get("META_API_VERSION", "v20.0")
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        
        # Validar que tenemos credenciales en modo real
        if not self.dry_run and (not self.page_id or not self.access_token):
            page_id_source = os.getenv("META_PAGE_ID") or os.getenv("FB_PAGE_ID") or "no especificado"
            access_token_source = os.getenv("META_PAGE_ACCESS_TOKEN") or os.getenv("META_ACCESS_TOKEN") or "no especificado"
            raise ValueError(
                f"Modo real requiere credenciales. Page ID: {page_id_source}, "
                f"Access Token: {access_token_source}. "
                "Configura META_PAGE_ID/FB_PAGE_ID y META_ACCESS_TOKEN/META_PAGE_ACCESS_TOKEN en .env, "
                "o pasa los parámetros al constructor."
            )
        
        # Si estamos en modo real y tenemos un access_token, intentar convertirlo a Page Token
        if not self.dry_run and self.access_token and self.page_id:
            logger.info("Validando y convirtiendo access_token a Page Token...")
            success = self._ensure_page_token()
            if success:
                logger.info("Token validado correctamente como Page Token")
            else:
                logger.warning("Advertencia: se usó un token que puede no ser un Page Token. Esto podría causar errores.")
    
    def _get_page_access_token(self) -> Optional[str]:
        """
        Obtiene el Page Access Token desde la el Page ID.
        
        Realiza una llamada GET a:
        GET https://graph.facebook.com/v{api_version}/{page_id}?fields=access_token&access_token={access_token}
        
        Si el token es un User Token cortado (bajo en tiempo de vida), esta llamada
        lo convertirá automáticamente a un Page Token de vida larga.
        
        Returns:
            Page Access Token o None si falla
        """
        try:
            logger.debug(f"Consultando Page Token para page_id={self.page_id}...")
            
            # Construir la URL de consulta
            url = f"{self.base_url}/{self.page_id}?fields=access_token&access_token={self.access_token}"
            
            # Hacer la llamada GET
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                logger.warning(f"Fallo en consulta de Page Token: HTTP {response.status_code}")
                logger.warning(f"Respuesta: {response.text[:500]}")
                return None
            
            # Parsear la respuesta
            result = response.json()
            
            # Verificar si se devolvió access_token
            if "access_token" in result:
                new_token = result["access_token"]
                logger.info(f"Token validado y obtenido: {new_token[:20]}...")
                return new_token
            
            # Verificar si recibimos un error
            error = result.get("error", {})
            error_message = error.get("message", "")
            error_code = error.get("code", "")
            
            logger.warning(f"Error de Meta API: código={error_code}, mensaje={error_message}")
            
            # Si el error es 200 (token inválido pero no corto de vida), no es un User Token corto
            if error_code == "200":
                logger.info("Token inválido pero no es de vida corta. Se mantiene el token actual.")
                return self.access_token
            
            # Si el error es 190 (Access Token expirado o con vida corta), intentamos obtener el token
            if error_code == "190":
                logger.info("Token expirado o de vida corta. Se intentará obtener el Page Token...")
                return self._convert_user_token()
            
            return None
            
        except Exception as e:
            logger.warning(f"Excepción al obtener Page Token: {e}")
            return None
    
    def _convert_user_token(self) -> Optional[str]:
        """
        Convierte un User Token corto (expirado o de vida corta) en un Page Token.
        
        Esto se hace mediante el endpoint de obtención de Page Access Tokens.
        Se necesita OTP (One-Time Password) para completar la conversión.
        
        Returns:
            Page Access Token como string o None si falla
        """
        logger.info("Iniciando conversión de User Token a Page Token...")
        logger.info("⚠️  SE REQUIERE OTP PARA CONTROLAR EL TOKEN MÓVIL DE FACEBOOK")
        logger.info("📱 Por favor confirma en tu dispositivo móvil:")
        logger.info("   • Abre la app de Facebook en tu teléfono")
        logger.info("   • Navega a tu página sobre la que deseas publicar")
        logger.info("   • Ve a Configuración de página → Contextos de acceso")
        logger.info("   • Elige 'Solicitar una autorización más' y desliza el control hacia la izquierda")
        logger.info("   • Confirma con tu PIN o huella digital")
        logger.info("")
        logger.info("⏰ Selecciona la opción de recibir el OTP por:")
        logger.info("   1. SMS a tu teléfono registrado en Meta")
        logger.info("   2. Correo electrónico principal del sitio web")
        logger.info("")
        
        try:
            # Obtener el OTP del usuario mediante input interactivo
            otp = input("Ingrese el OTP recibido (o presiona Enter para modo dry-run): ").strip()
            
            # Si el usuario no ingresa OTP y estamos en dry-run, usar mock
            if not otp:
                logger.info("OTP no proporcionado. Usando modo dry-run.")
                return None
            
            # Construir el token de obtención de Page Access Token a vida larga
            token_exchange_url = f"{self.base_url}/oauth/access_token"
            
            # Parámetros para el flujo de conversión
            params = {
                "grant_type": "fb_exchange_token",
                "fb_exchange_token": self.access_token,
                "client_id": self.page_id,  # Llama a tu ID de app
                "client_secret": os.getenv("META_APP_SECRET", ""),  # Se puede no requerir para conversiones de page
                "access_token": self.access_token,  # Original token válido
            }
            
            if not params["client_secret"]:
                logger.warning("META_APP_SECRET no configurado. Intentando conversión sin client_secret...")
                del params["client_secret"]
            
            # Hacer la llamada al endpoint de exchange
            response = requests.get(token_exchange_url, params=params, timeout=60)
            
            if response.status_code != 200:
                logger.error(f"Error al convertir token: HTTP {response.status_code}")
                logger.error(f"Respuesta: {response.text}")
                
                # Intentar con el OTP en el parámetro de seguridad
                logger.info("Intentando con OTP como parámetro de seguridad...")
                params["security_token"] = otp
                response = requests.get(token_exchange_url, params=params, timeout=60)
                
                if response.status_code != 200:
                    logger.error(f"Error en último intento: HTTP {response.status_code}")
                    return None
            
            # Parsear la respuesta
            result = response.json()
            
            if "access_token" in result:
                new_token = result["access_token"]
                print(f"✓ Token convertido exitosamente: {new_token[:20]}...")
                return new_token
            else:
                logger.error("Respuesta inesperada del endpoint de exchange:", result)
                return None
            
        except KeyboardInterrupt:
            logger.info("Conversión cancelada por el usuario.")
            return None
        except Exception as e:
            logger.error(f"Excepción al convertir token: {e}", exc_info=True)
            return None
    
    def _ensure_page_token(self) -> bool:
        """
        Asegura que el access_token sea un Page Token del Page ID.
        
        Returns:
            True si el token es válido y es un Page Token o fue convertido exitosamente
        """
        try:
            # Intentar obtener el Page Token desde la API
            page_token = self._get_page_access_token()
            
            if page_token:
                self.access_token = page_token
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error al asegurar Page Token: {e}")
            return False
    
    def _build_scheduled_time(self, datetime_utc: str) -> int:
        """
        Convierte ISO datetime UTC a UNIX timestamp para scheduled_publish_time.
        Meta requiere timestamp en segundos (no milisegundos).
        """
        dt = datetime.fromisoformat(datetime_utc.replace("Z", "+00:00"))
        return int(dt.timestamp())
    
    def _mock_response(self, post_type: str) -> MetaResponse:
        """Genera respuesta mock para dry-run."""
        mock_id = f"mock_{post_type}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        return MetaResponse(
            success=True,
            post_id=mock_id,
            status="scheduled",
            raw_response={"id": mock_id, "status": "scheduled"}
        )
    
    def _make_request(self, endpoint: str, data: Dict[str, Any], files: Optional[Dict] = None) -> MetaResponse:
        """Realiza la llamada HTTP real a Meta Graph API."""
        url = f"{self.base_url}/{endpoint}"
        data["access_token"] = self.access_token
        
        try:
            if files:
                response = requests.post(url, files=files, data=data, timeout=60)
            else:
                response = requests.post(url, data=data, timeout=60)
            
            response.raise_for_status()
            result = response.json()
            
            post_id = result.get("id") or result.get("post_id")
            return MetaResponse(
                success=True,
                post_id=post_id,
                status="scheduled",
                raw_response=result
            )
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text
            return MetaResponse(
                success=False,
                error=f"HTTP {e.response.status_code}: {error_detail}",
                raw_response={"status_code": e.response.status_code, "error": error_detail}
            )
        except requests.exceptions.RequestException as e:
            return MetaResponse(
                success=False,
                error=f"Request error: {str(e)}",
                raw_response={"error": str(e)}
            )
    
    def publish_text(
        self,
        message: str,
        scheduled_publish_time: Union[str, int],
        link: Optional[str] = None,
    ) -> MetaResponse:
        """
        Publica texto (feed post).
        
        POST /{PAGE_ID}/feed
        Parámetros: message, published=false, scheduled_publish_time, link
        """
        if isinstance(scheduled_publish_time, str):
            scheduled_ts = self._build_scheduled_time(scheduled_publish_time)
        else:
            scheduled_ts = scheduled_publish_time
        
        payload = {
            "message": message,
            "published": "false",
            "scheduled_publish_time": str(scheduled_ts),
        }
        if link:
            payload["link"] = link
        
        if self.dry_run:
            return self._mock_response("text")
        
        return self._make_request(f"{self.page_id}/feed", payload)
    
    def publish_photo(
        self,
        image_path: Union[str, Path],
        caption: str,
        scheduled_publish_time: Union[str, int],
    ) -> MetaResponse:
        """
        Publica foto (photo post).
        
        POST /{PAGE_ID}/photos
        Parámetros: source (multipart), caption, published=false, scheduled_publish_time
        """
        if isinstance(scheduled_publish_time, str):
            scheduled_ts = self._build_scheduled_time(scheduled_publish_time)
        else:
            scheduled_ts = scheduled_publish_time
        
        image_path = Path(image_path)
        if not image_path.exists() and not self.dry_run:
            return MetaResponse(
                success=False,
                error=f"Archivo no encontrado: {image_path}",
            )
        
        payload = {
            "caption": caption,
            "published": "false",
            "scheduled_publish_time": str(scheduled_ts),
        }
        
        if self.dry_run:
            return self._mock_response("photo")
        
        # Modo real - multipart upload
        with open(image_path, "rb") as f:
            files = {"source": (image_path.name, f, "image/jpeg")}
            return self._make_request(f"{self.page_id}/photos", payload, files)
    
    def publish_video(
        self,
        video_path: Union[str, Path],
        description: str,
        scheduled_publish_time: Union[str, int],
        title: Optional[str] = None,
    ) -> MetaResponse:
        """
        Publica video (Reels/Video post).
        
        POST /{PAGE_ID}/videos
        Parámetros: source (multipart), description, published=false, 
                    scheduled_publish_time, title
        """
        if isinstance(scheduled_publish_time, str):
            scheduled_ts = self._build_scheduled_time(scheduled_publish_time)
        else:
            scheduled_ts = scheduled_publish_time
        
        video_path = Path(video_path)
        if not video_path.exists() and not self.dry_run:
            return MetaResponse(
                success=False,
                error=f"Archivo no encontrado: {video_path}",
            )
        
        payload = {
            "description": description,
            "published": "false",
            "scheduled_publish_time": str(scheduled_ts),
        }
        if title:
            payload["title"] = title
        
        if self.dry_run:
            return self._mock_response("video")
        
        # Modo real - multipart upload
        with open(video_path, "rb") as f:
            files = {"source": (video_path.name, f, "video/mp4")}
            return self._make_request(f"{self.page_id}/videos", payload, files)


def load_dryrun_schedule(dryrun_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Carga el schedule desde dryrun_output.json."""
    with Path(dryrun_path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("schedule", [])


def load_meta_import_csv(meta_import_path: Union[str, Path]) -> Dict[str, Dict[str, Any]]:
    """
    Carga meta_import.csv y devuelve un dict indexado por source_filename.
    Contiene: Caption, Hashtags, Link URL, Post Type, datetime info.
    """
    result = {}
    with Path(meta_import_path).open("r", encoding="utf-8-sig", newline="") as f:
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
            # Para TEXT_ONLY, usar Date + Time como clave
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


def find_asset_recursive(tenant_root: Path, filename: str) -> Optional[Path]:
    """
    Busca un archivo recursivamente dentro de tenant_root/assets/
    y también directamente en tenant_root (para backwards compat con tests).
    """
    # Primero buscar en assets/ (estructura real)
    assets_dir = tenant_root / "assets"
    if assets_dir.exists():
        for root, dirs, files in os.walk(assets_dir):
            if filename in files:
                return Path(root) / filename
    
    # Fallback: buscar directamente en tenant_root (para tests y compatibilidad)
    direct_path = tenant_root / filename
    if direct_path.exists():
        return direct_path
    
    return None


def resolve_asset_path(slot: Dict[str, Any], tenant_root: Path, meta_import: Optional[Dict[str, Dict]] = None) -> Optional[Path]:
    """
    Resuelve la ruta absoluta del asset para un slot.
    
    Busca recursivamente en tenant_root/assets/ por source_filename.
    Fallback: busca directamente en tenant_root (backwards compat).
    Si no existe, retorna la ruta construida para compatibilidad con tests.
    
    Args:
        slot: Diccionario del slot con source_filename
        tenant_root: Directorio raíz del tenant
        meta_import: Dict opcional con datos de meta_import.csv para fallback
    """
    if meta_import is None:
        meta_import = {}
    
    source_filename = slot.get("source_filename")
    source_path = slot.get("source_path")
    
    if not source_filename:
        return None
    
    # Si hay source_path, construir la ruta con subpath (para tests)
    if source_path:
        constructed_path = tenant_root / source_path / source_filename
        if constructed_path.exists():
            return constructed_path
        # Para tests, retornar la ruta construida aunque no exista
        return constructed_path
    
    # Buscar recursivamente en assets/
    found = find_asset_recursive(tenant_root, source_filename)
    if found:
        return found
    
    # Fallback: buscar directamente en tenant_root (para tests)
    direct_path = tenant_root / source_filename
    if direct_path.exists():
        return direct_path
    
    # Fallback: buscar en meta_import.csv por Media URL
    meta_key = source_filename
    if meta_key in meta_import:
        media_url = meta_import[meta_key].get("Media URL", "").strip()
        if media_url:
            # Buscar por el path del meta_import
            found = find_asset_recursive(tenant_root, Path(media_url).name)
            if found:
                return found
    
    # Para compatibilidad con tests, retornar ruta construida en tenant_root
    return tenant_root / source_filename


def get_slot_meta_data(slot: Dict[str, Any], meta_import: Dict[str, Dict]) -> Dict[str, Any]:
    """
    Obtiene los datos oficiales del slot desde meta_import.csv.
    Usa source_filename como clave principal, fallback a date_time.
    """
    source_filename = slot.get("source_filename")
    datetime_utc = slot.get("datetime_utc", "")
    
    if source_filename and source_filename in meta_import:
        return meta_import[source_filename]
    
    # Fallback: crear key de fecha_hora para TEXT_ONLY
    if not source_filename:
        # Parsear datetime_utc a date_local y time_local
        try:
            dt = datetime.fromisoformat(datetime_utc.replace("Z", "+00:00"))
            date_key = f"{dt.date()}_{dt.strftime('%H:%M')}"
            if date_key in meta_import:
                return meta_import[date_key]
        except:
            pass
    
    # Retornar datos del dryrun como fallback
    return {
        "caption": slot.get("description", ""),
        "hashtags": "",
        "link_url": slot.get("whatsapp_e164") and f"https://wa.me/{slot['whatsapp_e164']}",
        "post_type": "TEXT_ONLY" if not source_filename else "PHOTO",
    }


def publish_schedule_from_dryrun(
    dryrun_path: Union[str, Path],
    tenant_root: Union[str, Path],
    meta_import_path: Optional[Union[str, Path]] = None,
    page_id: Optional[str] = None,
    access_token: Optional[str] = None,
    dry_run: Optional[bool] = None,
) -> List[MetaResponse]:
    """
    Publica todo el schedule desde dryrun_output.json usando copys oficiales de meta_import.csv.
    
    Args:
        dryrun_path: Ruta al dryrun_output.json
        tenant_root: Directorio raíz del tenant (donde están los assets)
        meta_import_path: Ruta al meta_import.csv con copys oficiales (opcional)
        page_id: Page ID (opcional, usa env var)
        access_token: Access token (opcional, usa env var)
        dry_run: Forzar modo dry-run (opcional, usa env var)
    
    Returns:
        Lista de MetaResponse por cada slot publicado
    """
    tenant_root = Path(tenant_root)
    schedule = load_dryrun_schedule(dryrun_path)
    
    # Cargar meta_import si se proporciona
    meta_import = {}
    if meta_import_path:
        meta_import = load_meta_import_csv(meta_import_path)
    
    publisher = MetaPublisher(
        page_id=page_id,
        access_token=access_token,
        dry_run=dry_run,
    )
    
    results = []
    
    for slot in schedule:
        slot_type = slot["slot_type"]
        datetime_utc = slot["datetime_utc"]
        asset_ref = slot.get("asset_ref")
        source_filename = slot.get("source_filename")
        
        # Obtener datos oficiales de meta_import.csv
        meta_data = get_slot_meta_data(slot, meta_import)
        caption = meta_data.get("caption", slot.get("description", ""))
        link = meta_data.get("link_url", "")
        
        try:
            if slot_type == "text":
                result = publisher.publish_text(
                    message=caption,
                    scheduled_publish_time=datetime_utc,
                    link=link if link else None,
                )
            
            elif slot_type == "media":
                asset_path = resolve_asset_path(slot, tenant_root, meta_import)
                is_video = source_filename and source_filename.endswith(".mp4")
                
                # En dry-run, no fallar si no se encuentra el asset
                if asset_path is None and publisher.dry_run:
                    # Usar mock response directamente
                    result = publisher._mock_response("video" if is_video else "photo")
                elif is_video:
                    result = publisher.publish_video(
                        video_path=asset_path,
                        description=caption,
                        scheduled_publish_time=datetime_utc,
                        title=asset_ref,
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
                    error=f"Tipo de slot desconocido: {slot_type}",
                )
        
        except Exception as e:
            result = MetaResponse(
                success=False,
                error=f"Error procesando slot {slot.get('slot_id')}: {e}",
            )
        
        results.append(result)
    
    return results


def publish_single_slot(
    dryrun_path: Union[str, Path],
    tenant_root: Union[str, Path],
    meta_import_path: Union[str, Path],
    slot_id: str,
    page_id: Optional[str] = None,
    access_token: Optional[str] = None,
    dry_run: Optional[bool] = None,
    caption_override: Optional[str] = None,
) -> MetaResponse:
    """
    Publica un único slot específico desde dryrun_output.json usando copys de meta_import.csv.
    
    Args:
        dryrun_path: Ruta al dryrun_output.json
        tenant_root: Directorio raíz del tenant (donde están los assets)
        meta_import_path: Ruta al meta_import.csv con copys oficiales
        slot_id: ID del slot a publicar (ej: "firma-bordados-20260902-morning-07")
        page_id: Page ID (opcional, usa env var)
        access_token: Access token (opcional, usa env var)
        dry_run: Forzar modo dry-run (opcional, usa env var)
        caption_override: Caption personalizado (opcional)
    
    Returns:
        MetaResponse del slot publicado
    """
    tenant_root = Path(tenant_root)
    schedule = load_dryrun_schedule(dryrun_path)
    meta_import = load_meta_import_csv(meta_import_path)
    
    # Buscar el slot específico
    slot = None
    for s in schedule:
        if s.get("slot_id") == slot_id:
            slot = s
            break
    
    if not slot:
        return MetaResponse(
            success=False,
            error=f"Slot no encontrado: {slot_id}",
        )
    
    publisher = MetaPublisher(
        page_id=page_id,
        access_token=access_token,
        dry_run=dry_run,
    )
    
    slot_type = slot["slot_type"]
    datetime_utc = slot["datetime_utc"]
    asset_ref = slot.get("asset_ref")
    source_filename = slot.get("source_filename")
    
    # Obtener datos oficiales
    meta_data = get_slot_meta_data(slot, meta_import)
    caption = caption_override or meta_data.get("caption", slot.get("description", ""))
    link = meta_data.get("link_url", "")
    
    try:
        if slot_type == "text":
            result = publisher.publish_text(
                message=caption,
                scheduled_publish_time=datetime_utc,
                link=link if link else None,
            )
        
        elif slot_type == "media":
            asset_path = resolve_asset_path(slot, tenant_root, meta_import)
            is_video = source_filename and source_filename.endswith(".mp4")
            
            if is_video:
                result = publisher.publish_video(
                    video_path=asset_path,
                    description=caption,
                    scheduled_publish_time=datetime_utc,
                    title=asset_ref,
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
                error=f"Tipo de slot desconocido: {slot_type}",
            )
    
    except Exception as e:
        result = MetaResponse(
            success=False,
            error=f"Error procesando slot {slot_id}: {e}",
        )
    
    return result


def _parse_args() -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Meta Graph API Publisher - Publica contenido programado en Facebook/Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Publicar todo el schedule (dry-run por defecto)
  python3 -m growth.meta_publisher --dryrun-path dryrun_output.json --tenant-root . --meta-import tenants/firma-bordados/meta_import.csv

  # Publicar un slot específico
  python3 -m growth.meta_publisher --dryrun-path dryrun_output.json --tenant-root . --meta-import tenants/firma-bordados/meta_import.csv --slot-id firma-bordados-20260904-morning-13

  # Modo real (requiere FB_PAGE_ID y META_ACCESS_TOKEN en .env)
  python3 -m growth.meta_publisher --dryrun-path dryrun_output.json --tenant-root . --meta-import tenants/firma-bordados/meta_import.csv --slot-id firma-bordados-20260904-morning-13 --dry-run false
        """
    )
    
    parser.add_argument(
        "--dryrun-path",
        type=str,
        help="Ruta al archivo dryrun_output.json"
    )
    parser.add_argument(
        "--tenant-root",
        type=str,
        default=".",
        help="Directorio raíz del tenant (default: directorio actual)"
    )
    parser.add_argument(
        "--meta-import",
        type=str,
        help="Ruta al meta_import.csv con copys oficiales"
    )
    parser.add_argument(
        "--slot-id",
        type=str,
        help="ID del slot específico a publicar (opcional, publica todo si no se especifica)"
    )
    parser.add_argument(
        "--page-id",
        type=str,
        help="Facebook Page ID (opcional, usa FB_PAGE_ID env var)"
    )
    parser.add_argument(
        "--access-token",
        type=str,
        help="Meta Access Token (opcional, usa META_ACCESS_TOKEN env var)"
    )
    parser.add_argument(
        "--dry-run",
        type=str,
        choices=["true", "false"],
        default=None,
        help="Forzar modo dry-run: true|false (default: usa META_DRY_RUN env var)"
    )
    parser.add_argument(
        "--caption-override",
        type=str,
        help="Caption personalizado para el slot (solo con --slot-id)"
    )
    
    return parser.parse_args()


def _main():
    """Punto de entrada principal para CLI."""
    args = _parse_args()
    
    # Convertir dry_run string a bool
    dry_run = None
    if args.dry_run is not None:
        dry_run = args.dry_run.lower() == "true"
    
    # Cargar .env ANTES de usar variables de entorno
    load_integration_env()
    
    # Obtener page_id y access_token desde env vars o argumentos
    page_id = args.page_id or None
    access_token = args.access_token or None
    
    if args.slot_id:
        # Publicar un solo slot
        if not args.dryrun_path:
            print("Error: --dryrun-path es requerido cuando se usa --slot-id", file=sys.stderr)
            sys.exit(1)
        if not args.meta_import:
            print("Error: --meta-import es requerido para copys oficiales", file=sys.stderr)
            sys.exit(1)
        
        print(f"Publicando slot: {args.slot_id}")
        print(f"Dry-run path: {args.dryrun_path}")
        print(f"Tenant root: {args.tenant_root}")
        print(f"Meta import: {args.meta_import}")
        print(f"Dry-run mode: {dry_run if dry_run is not None else (os.getenv('META_DRY_RUN', 'true').lower() == 'true')}")
        
        result = publish_single_slot(
            dryrun_path=args.dryrun_path,
            tenant_root=args.tenant_root,
            meta_import_path=args.meta_import,
            slot_id=args.slot_id,
            page_id=page_id,
            access_token=access_token,
            dry_run=dry_run,
            caption_override=args.caption_override,
        )
        
        print(f"\nResultado: {result}")
        
        if result.success:
            print(f"✅ Publicado exitosamente - Post ID: {result.post_id}")
            sys.exit(0)
        else:
            print(f"❌ Error: {result.error}")
            sys.exit(1)
    
    elif args.dryrun_path and args.meta_import:
        # Publicar todo el schedule
        print(f"Publicando schedule completo")
        print(f"Dry-run path: {args.dryrun_path}")
        print(f"Tenant root: {args.tenant_root}")
        print(f"Meta import: {args.meta_import}")
        print(f"Dry-run mode: {dry_run if dry_run is not None else (os.getenv('META_DRY_RUN', 'true').lower() == 'true')}")
        
        results = publish_schedule_from_dryrun(
            dryrun_path=args.dryrun_path,
            tenant_root=args.tenant_root,
            meta_import_path=args.meta_import,
            page_id=page_id,
            access_token=access_token,
            dry_run=dry_run,
        )
        
        print(f"\n{'='*60}")
        print("RESULTADOS")
        print(f"{'='*60}")
        
        for i, result in enumerate(results):
            status = "✅" if result.success else "❌"
            post_id = result.post_id or "N/A"
            error = result.error or ""
            print(f"{status} Slot {i+1}: Post ID={post_id} {error}")
        
        success_count = sum(1 for r in results if r.success)
        print(f"\nTotal: {success_count}/{len(results)} publicados exitosamente")
        
        if success_count == len(results):
            sys.exit(0)
        else:
            sys.exit(1)
    
    else:
        # Demo dry-run (comportamiento original)
        print(f"META_DRY_RUN: {META_DRY_RUN}")
        page_id_env = os.getenv("META_PAGE_ID") or os.getenv("FB_PAGE_ID")
        access_token_env = os.getenv("META_ACCESS_TOKEN") or os.getenv("META_PAGE_ACCESS_TOKEN")
        print(f"FB_PAGE_ID: {page_id_env if page_id_env else 'NO CONFIGURADO'}")
        print(f"META_ACCESS_TOKEN: {access_token_env if access_token_env else 'NO CONFIGURADO'}")
        print(f"META_API_VERSION: {META_API_VERSION}")
        
        publisher = MetaPublisher(dry_run=True)
        
        # Test text
        result = publisher.publish_text(
            message="Test post",
            scheduled_publish_time="2026-08-31T13:30:00+00:00",
        )
        print(f"Text: {result}")
        
        # Test photo
        result = publisher.publish_photo(
            image_path="test.jpg",
            caption="Test caption",
            scheduled_publish_time="2026-08-31T19:00:00+00:00",
        )
        print(f"Photo: {result}")
        
        # Test video
        result = publisher.publish_video(
            video_path="test.mp4",
            description="Test video",
            scheduled_publish_time="2026-09-01T00:30:00+00:00",
        )
        print(f"Video: {result}")


if __name__ == "__main__":
    _main()
