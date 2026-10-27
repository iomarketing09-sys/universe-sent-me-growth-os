"""Google Webmaster Tools API adapter (Search Console + Bing Webmaster).

Este módulo captura métricas de Search Console y Bing Webmaster usando OAuth.
Solo lectura - no permite modificar nada.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
import json
import requests


# Configuración base
GSC_BASE = "https://searchconsole.googleapis.com/webmasters/v3"
BING_BASE = "https://ssl.bing.com/webmaster/api.svc/json"


def _load_gsc_credentials() -> Optional[Dict]:
    """Carga credenciales OAuth de Google desde .env o archivo token."""
    # Primero buscar token guardado
    token_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "gsc_token.json"),
        os.path.join(os.path.dirname(__file__), "..", "gsc_token.json"),
    ]
    for token_path in token_paths:
        if os.path.exists(token_path):
            try:
                with open(token_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
    return None


def _load_bing_api_key() -> Optional[str]:
    """Carga API key de Bing Webmaster desde .env."""
    try:
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if not os.path.exists(env_path):
            env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("BING_WEBMASTER_API_KEY="):
                    return line.split("=", 1)[1].strip('"')
    except Exception:
        pass
    return None


def _refresh_gsc_token_if_needed(token_data: Dict) -> Optional[str]:
    """Refresca el access token de GSC si expiró."""
    if not token_data:
        return None
    
    # Verificar si el token expira en menos de 5 minutos
    expires_at = token_data.get("expires_at", 0)
    if expires_at > (datetime.now().timestamp() + 300):
        return token_data.get("access_token")
    
    # Intentar refrescar
    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        return token_data.get("access_token")  # Devolver el que tenemos aunque pueda estar expirado
    
    try:
        client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            return token_data.get("access_token")
        
        r = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            },
            timeout=30
        )
        
        if r.status_code >= 400:
            return token_data.get("access_token")
        
        new_token = r.json()
        access_token = new_token.get("access_token")
        expires_in = new_token.get("expires_in", 3600)
        
        # Actualizar token_data
        token_data["access_token"] = access_token
        token_data["expires_at"] = datetime.now().timestamp() + expires_in
        
        # Guardar
        for token_path in token_paths:
            try:
                with open(token_path, "w") as f:
                    json.dump(token_data, f)
            except Exception:
                pass
        
        return access_token
    except Exception:
        return token_data.get("access_token")


def query_gsc_search_analytics(
    access_token: str,
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: List[str] = None,
    limit: int = 1000
) -> Dict:
    """Consulta Search Analytics de Google Search Console."""
    if dimensions is None:
        dimensions = ["query", "page", "country", "device"]
    
    url = f"{GSC_BASE}/sites/{site_url}/searchAnalytics/query"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": limit
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code >= 400:
            err = r.json() if r.content else {}
            return {
                "error": err.get("error", {}).get("message", f"HTTP {r.status_code}"),
                "status": "error",
                "code": err.get("error", {}).get("code", "")
            }
        return {"status": "success", "data": r.json()}
    except Exception as e:
        return {"error": str(e), "status": "error"}


def query_gsc_sitemaps(access_token: str, site_url: str) -> Dict:
    """Obtiene sitemaps enviados a Search Console."""
    url = f"{GSC_BASE}/sites/{site_url}/sitemaps"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code >= 400:
            err = r.json() if r.content else {}
            return {"error": err.get("error", {}).get("message", f"HTTP {r.status_code}"), "status": "error"}
        return {"status": "success", "data": r.json()}
    except Exception as e:
        return {"error": str(e), "status": "error"}


def query_bing_webmaster(
    api_key: str,
    method: str,
    site_url: str,
    params: Dict = None
) -> Dict:
    """Consulta Bing Webmaster Tools API."""
    params = params or {}
    params["apikey"] = api_key
    params["siteUrl"] = site_url
    
    url = f"{BING_BASE}/{method}"
    
    try:
        r = requests.post(url, json=params, timeout=30)
        if r.status_code >= 400:
            err = r.json() if r.content else {}
            return {"error": err.get("Message", f"HTTP {r.status_code}"), "status": "error"}
        return {"status": "success", "data": r.json()}
    except Exception as e:
        return {"error": str(e), "status": "error"}


def capture_google_webmaster(config: Dict) -> Dict:
    """
    Captura métricas de Google Search Console y Bing Webmaster.
    
    Args:
        config: Dict con keys:
            - google_business: {'place_id', 'website'}
            - search_console: {'site_url'}
            - bing_webmaster: {'site_url'}
    
    Returns:
        Dict con: status, search_console{}, bing_webmaster{}, summary{}
    """
    gsc_config = config.get("search_console") or config.get("google_business") or {}
    bing_config = config.get("bing_webmaster") or {}
    
    site_url = gsc_config.get("site_url") or gsc_config.get("website")
    if not site_url:
        return {"status": "not_configured", "note": "Falta site_url en search_console o google_business.website"}
    
    result = {
        "status": "success",
        "search_console": {"status": "not_configured"},
        "bing_webmaster": {"status": "not_configured"},
        "summary": {
            "total_clicks": 0,
            "total_impressions": 0,
            "avg_ctr": 0.0,
            "avg_position": 0.0,
            "indexed_pages": 0,
            "crawl_errors": 0
        }
    }
    
    # Fecha por defecto: últimos 30 días
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # === GOOGLE SEARCH CONSOLE ===
    gsc_credentials = _load_gsc_credentials()
    if gsc_credentials:
        access_token = _refresh_gsc_token_if_needed(gsc_credentials)
        if access_token:
            # Search Analytics
            analytics_result = query_gsc_search_analytics(access_token, site_url, start_date, end_date)
            if analytics_result.get("status") == "success":
                rows = analytics_result["data"].get("rows", [])
                total_clicks = sum(row.get("clicks", 0) for row in rows)
                total_impressions = sum(row.get("impressions", 0) for row in rows)
                avg_ctr = sum(row.get("ctr", 0) for row in rows) / len(rows) if rows else 0
                avg_position = sum(row.get("position", 0) for row in rows) / len(rows) if rows else 0
                
                result["search_console"] = {
                    "status": "success",
                    "period": {"start": start_date, "end": end_date},
                    "metrics": {
                        "clicks": total_clicks,
                        "impressions": total_impressions,
                        "ctr": round(avg_ctr, 4),
                        "position": round(avg_position, 2)
                    },
                    "top_queries": [
                        {"query": row["keys"][0], "clicks": row.get("clicks", 0), "impressions": row.get("impressions", 0), "ctr": row.get("ctr", 0), "position": row.get("position", 0)}
                        for row in sorted(rows, key=lambda x: x.get("clicks", 0), reverse=True)[:20]
                    ],
                    "top_pages": [
                        {"page": row["keys"][1] if len(row.get("keys", [])) > 1 else "", "clicks": row.get("clicks", 0), "impressions": row.get("impressions", 0)}
                        for row in sorted(rows, key=lambda x: x.get("clicks", 0), reverse=True)[:10]
                    ]
                }
                
                result["summary"]["total_clicks"] += total_clicks
                result["summary"]["total_impressions"] += total_impressions
                result["summary"]["avg_ctr"] = round(avg_ctr, 4)
                result["summary"]["avg_position"] = round(avg_position, 2)
            else:
                result["search_console"] = analytics_result
            
            # Sitemaps
            sitemaps_result = query_gsc_sitemaps(access_token, site_url)
            if sitemaps_result.get("status") == "success":
                sitemaps = sitemaps_result["data"].get("sitemap", [])
                result["search_console"]["sitemaps"] = [
                    {"path": s.get("path", ""), "type": s.get("type", ""), "last_submitted": s.get("lastSubmitted", ""), "urls_submitted": s.get("urlsSubmitted", 0), "urls_indexed": s.get("urlsIndexed", 0)}
                    for s in sitemaps
                ]
    else:
        result["search_console"] = {"status": "not_configured", "note": "No hay credenciales OAuth GSC (gsc_token.json)"}
    
    # === BING WEBMASTER TOOLS ===
    bing_api_key = _load_bing_api_key()
    bing_site_url = bing_config.get("site_url") or site_url
    
    if bing_api_key and bing_site_url:
        # GetUrlList - páginas indexadas
        url_list_result = query_bing_webmaster(bing_api_key, "GetUrlList", bing_site_url, {"limit": 100})
        if url_list_result.get("status") == "success":
            urls = url_list_result["data"].get("d", [])
            result["summary"]["indexed_pages"] = len(urls)
            result["bing_webmaster"]["indexed_pages"] = len(urls)
        
        # GetCrawlErrors - errores de rastreo
        crawl_result = query_bing_webmaster(bing_api_key, "GetCrawlErrors", bing_site_url, {"limit": 100})
        if crawl_result.get("status") == "success":
            errors = crawl_result["data"].get("d", [])
            result["summary"]["crawl_errors"] = len(errors)
            result["bing_webmaster"]["crawl_errors"] = len(errors)
            result["bing_webmaster"]["errors_sample"] = errors[:10]
        
        # GetSearchAnalytics - métricas de búsqueda (si disponible en la API)
        # Nota: Bing Webmaster API tiene funcionalidad limitada vs GSC
        result["bing_webmaster"]["status"] = "success"
        result["bing_webmaster"]["period"] = {"start": start_date, "end": end_date}
    else:
        result["bing_webmaster"] = {"status": "not_configured", "note": "Falta BING_WEBMASTER_API_KEY en .env"}
    
    return result


def capture_google_business(config: Dict) -> Dict:
    """
    Captura métricas de Google Business Profile (antiguo Google My Business).
    
    Args:
        config: Dict con keys 'google_business' | {'place_id'}
    
    Returns:
        Dict con: status, location{}, insights{}, reviews{}
    """
    gb_config = config.get("google_business") or {}
    place_id = gb_config.get("place_id")
    
    if not place_id:
        return {"status": "not_configured", "note": "Falta place_id en google_business"}
    
    # NOTA: Google Business Profile API requiere OAuth específico
    # y configuración en Google Cloud Console. Por ahora devolvemos
    # estado de configuración.
    return {
        "status": "not_implemented",
        "note": "Google Business Profile API requiere OAuth específico y configuración en GCP. Use GSC + Bing por ahora.",
        "place_id": place_id,
        "configured": True
    }
