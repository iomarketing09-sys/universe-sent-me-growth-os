"""Meta Ads adapters for live data capture.

Este módulo captura métricas de campañas publicitarias usando Meta Marketing API.
Solo lectura, sin crear/modificar campañas.

Piloto: Flexi (ad_account_id pendiente de configuración)
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
import os

# Configuración base de Marketing API v26.0
GRAPH_BASE = "https://graph.facebook.com/v26.0"

def _project_root() -> Path:
    """Raíz del repo, sin importar en qué módulo viva este archivo."""
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


def _load_user_token() -> Optional[str]:
    """Carga el token de usuario Meta del entorno o de ``.env`` (sin imprimirlo)."""
    token = os.environ.get("META_ACCESS_TOKEN")
    if token:
        return token
    try:
        with ( _project_root() / ".env").open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("META_ACCESS_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return None

def _build_request(endpoint: str, params: Optional[Dict] = None) -> tuple:
    """Construye la URL completa y params con access_token."""
    params = params or {}
    params["access_token"] = _load_user_token()
    url = f"{GRAPH_BASE}/{endpoint}"
    return url, params

def get_page_token(user_token: str, page_id: str) -> Optional[str]:
    """Obtiene el token de página a partir del token de usuario."""
    try:
        import requests
        url = f"{GRAPH_BASE}/{page_id}?fields=access_token&access_token={user_token}"
        r = requests.get(url, timeout=30)
        if r.status_code >= 400:
            return None
        return r.json().get("access_token")
    except Exception:
        return None


MESSAGING_ACTION_KEYS = (
    "onsite_conversion.messaging_conversation_started_7d",
    "messaging_conversation_started_7d",
    "messaging_conversation_started",
    "onsite_conversion.messaging_first_reply",
    "onsite_conversion.total_messaging_connection",
    "onsite_conversion.messaging_user_depth_2_message_send",
    "onsite_conversion.messaging_user_depth_3_message_send",
    "onsite_conversion.messaging_welcome_message_view",
    "onsite_conversion.messaging_block",
    "onsite_conversion.messaging_conversation_replied_7d",
)


def _messaging_actions(actions: Optional[List[Dict]]) -> Dict[str, int]:
    """Agrupa las acciones de mensajería de un bloque de insights."""
    totals = {key: 0 for key in MESSAGING_ACTION_KEYS}
    for action in actions or []:
        action_type = action.get("action_type", "")
        try:
            value = int(float(action.get("value", 0)))
        except (TypeError, ValueError):
            value = 0
        for key in MESSAGING_ACTION_KEYS:
            if action_type == key or key in action_type:
                totals[key] += value
    return totals


def _started_conversations(totals: Dict[str, int]) -> int:
    return (
        totals.get("onsite_conversion.messaging_conversation_started_7d", 0)
        or totals.get("messaging_conversation_started_7d", 0)
        or totals.get("messaging_conversation_started", 0)
    )


def _metric_row(insight: Dict, name: str, campaign_id: str, campaign_name: str) -> Dict:
    """Normaliza un bloque de insights de campaña o anuncio."""
    spend = float(insight.get("spend", 0) or 0)
    totals = _messaging_actions(insight.get("actions"))
    conversations = _started_conversations(totals)
    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign_name,
        "name": name,
        "spend": round(spend, 2),
        "impressions": int(float(insight.get("impressions", 0) or 0)),
        "clicks": int(float(insight.get("clicks", 0) or 0)),
        "reach": int(float(insight.get("reach", 0) or 0)),
        "ctr": round(float(insight.get("ctr", 0) or 0), 2),
        "cpc": round(float(insight.get("cpc", 0) or 0), 2),
        "conversations": conversations,
        "cost_per_conversation": round(spend / conversations, 2) if conversations else 0.0,
        "messaging_metrics": totals,
    }

def capture_ads_insights(config: Dict) -> Dict:
    """
    Captura insights de campañas publicitarias usando Meta Marketing API.
    
    Args:
        config: Dict con keys 'ads' | {'ad_account_id'}
    
    Returns:
        Dict con: status, campaigns[], ad_sets[], ads[], summary{}
        Si falla: error, note
    """
    ads_config = config.get("ads", {})
    ad_account_id = ads_config.get("ad_account_id")
    
    if not ad_account_id:
        return {
            "status": "not_configured",
            "note": "Falta ad_account_id en config['ads']"
        }
    
    user_token = _load_user_token()
    if not user_token:
        return {"status": "error", "note": "No se pudo cargar META_ACCESS_TOKEN"}
    
    result = {
        "status": "success",
        "campaigns": [],
        "ad_sets": [],
        "ads": [],
        "summary": {
            "total_spend": 0,
            "total_impressions": 0,
            "total_clicks": 0,
            "total_conversations": 0
        }
    }
    
    # Query campaigns
    # El ad_account_id ya puede venir con prefijo act_
    account_endpoint = ad_account_id if ad_account_id.startswith("act_") else f"act_{ad_account_id}"
    url, params = _build_request(f"{account_endpoint}/campaigns", {
        "fields": "id,name,objective,status,effective_status,daily_budget,lifetime_budget",
        "limit": 100
    })
    
    try:
        import requests
        r = requests.get(url, params=params, timeout=30)
        if r.status_code >= 400:
            err_data = r.json() if r.content else {}
            return {
                "status": "error",
                "note": f"Error querying campaigns: {err_data.get('error', {}).get('message', f'HTTP {r.status_code}')}",
                "code": err_data.get("error", {}).get("code", "")
            }
        
        campaigns_data = r.json().get("data", [])
        
        # Para cada campaña, obtener insights
        for campaign in campaigns_data:
            campaign_id = campaign["id"]
            
            # Query insights for this campaign
            insights_url, insights_params = _build_request(f"{campaign_id}/insights", {
                "fields": "spend,impressions,clicks,reach,frequency,ctr,cpm,cpp,cpc,actions",
                "date_preset": "maximum",
                "limit": 100
            })
            
            r2 = requests.get(insights_url, params=insights_params, timeout=30)
            if r2.status_code >= 400:
                continue  # Skip this campaign
            
            insights = r2.json().get("data", [])
            
            if insights:
                insight = insights[0]
                spend = float(insight.get("spend", 0))
                impressions = int(insight.get("impressions", 0))
                clicks = int(insight.get("clicks", 0))
                reach = int(insight.get("reach", 0))
                frequency = float(insight.get("frequency", 0))
                ctr = float(insight.get("ctr", 0))
                cpm = float(insight.get("cpm", 0))
                cpc = float(insight.get("cpc", 0))
                
                # Conversaciones - buscar todas las variantes de messaging
                conversations = 0
                messaging_actions = {
                    "messaging_conversation_started": 0,
                    "messaging_conversation_started_7d": 0,
                    "onsite_conversion.messaging_conversation_started_7d": 0,
                    "onsite_conversion.messaging_first_reply": 0,
                    "onsite_conversion.total_messaging_connection": 0
                }
                for action in insight.get("actions", []):
                    action_type = action.get("action_type", "")
                    value = int(action.get("value", 0))
                    
                    # Buscar claves exactas o por substring
                    for key in messaging_actions:
                        if key == action_type or key in action_type:
                            messaging_actions[key] += value
                
                # Usar la métrica principal de conversaciones iniciadas (7 días)
                conversations = (
                    messaging_actions.get("onsite_conversion.messaging_conversation_started_7d", 0) or
                    messaging_actions.get("messaging_conversation_started_7d", 0) or
                    messaging_actions.get("messaging_conversation_started", 0)
                )
                
                campaign_data = {
                    "id": campaign_id,
                    "name": campaign.get("name", ""),
                    "objective": campaign.get("objective", ""),
                    "status": campaign.get("effective_status", ""),
                    "spend": spend,
                    "impressions": impressions,
                    "clicks": clicks,
                    "reach": reach,
                    "frequency": frequency,
                    "ctr": ctr,
                    "cpm": cpm,
                    "cpc": cpc,
                    "conversations": conversations,
                    "cost_per_conversation": spend / conversations if conversations > 0 else 0,
                    "messaging_metrics": {
                        "conversations_started_7d": messaging_actions.get("onsite_conversion.messaging_conversation_started_7d", 0),
                        "messaging_first_reply": messaging_actions.get("onsite_conversion.messaging_first_reply", 0),
                        "total_messaging_connection": messaging_actions.get("onsite_conversion.total_messaging_connection", 0),
                        "messaging_user_depth_2": messaging_actions.get("onsite_conversion.messaging_user_depth_2_message_send", 0),
                        "messaging_user_depth_3": messaging_actions.get("onsite_conversion.messaging_user_depth_3_message_send", 0),
                        "welcome_message_views": messaging_actions.get("onsite_conversion.messaging_welcome_message_view", 0),
                        "messaging_block": messaging_actions.get("onsite_conversion.messaging_block", 0),
                        "messaging_conversation_replied_7d": messaging_actions.get("onsite_conversion.messaging_conversation_replied_7d", 0)
                    }
                }
                result["campaigns"].append(campaign_data)
                
                # Actualizar summary
                result["summary"]["total_spend"] += spend
                result["summary"]["total_impressions"] += impressions
                result["summary"]["total_clicks"] += clicks
                result["summary"]["total_conversations"] += conversations

            # Insights por anuncio (mismo nivel de detalle que Ads Manager)
            ads_url, ads_params = _build_request(f"{campaign_id}/ads", {
                "fields": "id,name,status,effective_status,adset_id,"
                          "insights{spend,impressions,clicks,reach,ctr,cpc,actions}",
                "date_preset": "maximum",
                "limit": 100,
            })
            r3 = requests.get(ads_url, params=ads_params, timeout=30)
            if r3.status_code >= 400:
                continue

            for ad in r3.json().get("data", []):
                blocks = (ad.get("insights") or {}).get("data") or []
                if not blocks:
                    continue
                row = _metric_row(blocks[0], ad.get("name", ""), campaign_id, campaign.get("name", ""))
                row.update({
                    "id": ad.get("id", ""),
                    "adset_id": ad.get("adset_id", ""),
                    "status": ad.get("effective_status", ad.get("status", "")),
                })
                result["ads"].append(row)
    
    except Exception as e:
        return {
            "status": "error",
            "note": f"Excepción capturando insights: {str(e)}"
        }
    
    return result
