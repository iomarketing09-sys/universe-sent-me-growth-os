"""Meta Graph API read-only adapter.

Este módulo captura métricas orgánicas de Meta (Facebook + Instagram) usando
solamente GET requests. No permite publicar ni modificar nada.
"""

import requests
from typing import Dict, List, Optional

# Configuración base de Graph API v26.0
GRAPH_BASE = "https://graph.facebook.com/v26.0"


def _load_user_token() -> Optional[str]:
    """Carga el token de usuario Meta desde .env (igual que metrics_snapshot.py)."""
    try:
        import os
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if not os.path.exists(env_path):
            # Fallback: intentar desde raíz
            env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("META_ACCESS_TOKEN="):
                    return line.split("=", 1)[1].strip('"')
    except Exception:
        pass
    return None


def _build_request_url(endpoint: str, params: Optional[Dict] = None) -> tuple:
    """Construye la URL completa y params con access_token."""
    params = params or {}
    params["access_token"] = _load_user_token()
    url = f"{GRAPH_BASE}/{endpoint}"
    return url, params


def query_instagram_media(
    user_token: str,
    ig_user_id: str,
    fields: List[str] = None,
    limit: int = 25
) -> Dict:
    """Consulta medios recientes de Instagram."""
    if fields is None:
        fields = [
            "id",
            "media_type",
            "thumbnail_url",
            "media_url",
            "permalink",
            "caption",
            "timestamp",
            "like_count",
            "comments_count"
        ]
    
    url, params = _build_request_url(f"{ig_user_id}/media", {
        "fields": ",".join(fields),
        "limit": limit,
        "order": "relevance desc"
    })
    
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code >= 400:
            err_data = r.json() if r.content else {}
            return {
                "status": "error",
                "source": "instagram_media",
                "http_status": r.status_code,
                "error": err_data.get("error", {}).get("message", f"HTTP {r.status_code}"),
                "code": err_data.get("error", {}).get("code", "")
            }
        return {"status": "success", "data": r.json()}
    except Exception as e:
        return {
            "status": "error",
            "source": "instagram_media",
            "error": str(e)
        }


def capture_organic(config: Dict) -> Dict:
    """
    Captura métricas orgánicas de una tenant usando Meta Graph API.

    Args:
        config: Dict con keys 'meta' | {'page_id', 'ig_user_id'}

    Returns:
        Dict con: status, Instagram, Facebook_Page, Messages_Viewer
        Si falla: error, note
    """
    meta = config.get("meta", {})
    page_id = meta.get("page_id")
    ig_user_id = meta.get("ig_user_id")
    
    if not page_id or not ig_user_id:
        return {
            "status": "not_configured",
            "note": "Faltan page_id o ig_user_id en config"
        }
    
    # Obtener token de página (reutiliza lógica de metrics_snapshot.py)
    user_token = _load_user_token()
    if not user_token:
        return {"status": "error", "note": "No se pudo cargar META_ACCESS_TOKEN"}
    
    result = {
        "status": "success",
        "Instagram": {},
        "Facebook_Page": {},
        "Messages_Viewer": {"status": "blocked_read_only"}
    }
    
    # Instagram (GET posts/mídia)
    ig_result = query_instagram_media(user_token, ig_user_id)
    if ig_result["status"] == "success":
        result["Instagram"] = {
            "data": ig_result["data"],
            "count": len(ig_result["data"].get("data", []))
        }
    else:
        result["Instagram"] = ig_result
    
    # Facebook Page (simple fields read-only)
    fb_url, fb_params = _build_request_url(f"{page_id}", {
        "fields": "id,name,followers_count,website"
    })
    try:
        r = requests.get(fb_url, params=fb_params, timeout=30)
        if r.status_code >= 400:
            err_data = r.json() if r.content else {}
            result["Facebook_Page"] = {
                "error": err_data.get("error", {}).get("message", f"HTTP {r.status_code}"),
                "status": "error",
                "code": err_data.get("error", {}).get("code", "")
            }
        else:
            result["Facebook_Page"] = r.json()
    except Exception as e:
        result["Facebook_Page"] = {"error": str(e), "status": "error"}
    
    return result
