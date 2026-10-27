"""WhatsApp Graph API adapter for pulling conversations and messages.

Usa el token de usuario para obtener token de página y luego consultar
conversaciones y mensajes via Graph API v26.0.

Solo lectura - no envía mensajes.
"""

import requests
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

GRAPH_BASE = "https://graph.facebook.com/v26.0"

def _load_user_token() -> Optional[str]:
    """Carga el token de usuario Meta desde el entorno o ``.env``."""
    from modules.communications.whatsapp.env import load_env_value

    return load_env_value("META_ACCESS_TOKEN")


def get_page_token(user_token: str, page_id: str) -> Optional[str]:
    """Obtiene el token de página a partir del token de usuario."""
    url = f"{GRAPH_BASE}/{page_id}"
    params = {"fields": "access_token", "access_token": user_token}
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code >= 400:
            return None
        return r.json().get("access_token")
    except Exception:
        return None

def get_whatsapp_business_account(page_token: str, waba_id: str) -> Dict:
    """Obtiene info de la WABA asociada a la página."""
    url = f"{GRAPH_BASE}/{waba_id}"
    params = {
        "fields": "id,name,owned_whatsapp_business_account{id,name}",
        "access_token": page_token
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code >= 400:
            return {"error": r.json().get("error", {}).get("message", f"HTTP {r.status_code}")}
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def get_conversations(page_token: str, page_id: str, limit: int = 100) -> Dict:
    """
    Obtiene conversaciones de WhatsApp Business.
    
    Usa el endpoint de conversaciones del PAGE_ID (no phone_number_id).
    """
    url = f"{GRAPH_BASE}/{page_id}/conversations"
    params = {
        "access_token": page_token,
        "limit": limit,
        "fields": "id,participants,updated_time,message_count,unread_count"
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code >= 400:
            err = r.json().get("error", {})
            return {"error": err.get("message", f"HTTP {r.status_code}"), "status": r.status_code}
        return {"data": r.json().get("data", []), "paging": r.json().get("paging", {})}
    except Exception as e:
        return {"error": str(e)}

def get_conversation_messages(page_token: str, conversation_id: str, limit: int = 100) -> Dict:
    """
    Obtiene mensajes de una conversación específica.
    
    Incluye mensajes entrantes Y salientes (de la sucursal).
    """
    url = f"{GRAPH_BASE}/{conversation_id}/messages"
    params = {
        "access_token": page_token,
        "limit": limit,
        "fields": "id,from,to,timestamp,text,type,status,direction"
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code >= 400:
            err = r.json().get("error", {})
            return {"error": err.get("message", f"HTTP {r.status_code}"), "status": r.status_code}
        return {"data": r.json().get("data", []), "paging": r.json().get("paging", {})}
    except Exception as e:
        return {"error": str(e)}

def get_phone_numbers(page_token: str, waba_id: str) -> Dict:
    """Obtiene números de teléfono asociados a la WABA."""
    url = f"{GRAPH_BASE}/{waba_id}/phone_numbers"
    params = {
        "access_token": page_token,
        "fields": "id,display_phone_number,verified_name,quality_rating,code_verification_status"
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code >= 400:
            err = r.json().get("error", {})
            return {"error": err.get("message", f"HTTP {r.status_code}"), "status": r.status_code}
        return {"data": r.json().get("data", [])}
    except Exception as e:
        return {"error": str(e)}

def pull_conversations_with_depth(config: Dict) -> Dict:
    """
    Pull completo: conversaciones + mensajes para medir profundidad.
    
    Args:
        config: Dict con keys 'meta' | {'page_id', 'phone_number_id', 'waba_id'}
    
    Returns:
        Dict con conversaciones, mensajes, métricas de profundidad
    """
    meta = config.get("meta", {})
    page_id = meta.get("page_id")
    phone_number_id = meta.get("phone_number_id") or meta.get("whatsapp_number_id")
    waba_id = meta.get("waba_id")
    
    if not page_id:
        return {"status": "not_configured", "note": "Falta page_id"}
    
    user_token = _load_user_token()
    if not user_token:
        return {"status": "error", "note": "No se pudo cargar META_ACCESS_TOKEN"}
    
    # Obtener token de página
    page_token = get_page_token(user_token, page_id)
    if not page_token:
        return {"status": "error", "note": "No se pudo obtener page access token"}
    
    result = {
        "status": "success",
        "conversations": [],
        "total_conversations": 0,
        "total_messages": 0,
        "depth_distribution": {},
        "direction_counts": {"in": 0, "out": 0},
        "by_conversation": []
    }
    
    # 1. Obtener conversaciones (usando page_id, no phone_number_id)
    conv_result = get_conversations(page_token, page_id, limit=200)
    if "error" in conv_result:
        return {"status": "error", "note": f"Conversaciones: {conv_result['error']}"}
    
    conversations = conv_result.get("data", [])
    result["total_conversations"] = len(conversations)
    
    # 2. Para cada conversación, obtener mensajes
    for conv in conversations:
        conv_id = conv["id"]
        msg_result = get_conversation_messages(page_token, conv_id, limit=200)
        if "error" in msg_result:
            continue
        
        messages = msg_result.get("data", [])
        
        # Analizar profundidad
        in_count = sum(1 for m in messages if m.get("direction") == "inbound")
        out_count = sum(1 for m in messages if m.get("direction") == "outbound")
        total = len(messages)
        
        depth = total
        depth_key = f"{total}_messages"
        result["depth_distribution"][depth_key] = result["depth_distribution"].get(depth_key, 0) + 1
        
        result["direction_counts"]["in"] += in_count
        result["direction_counts"]["out"] += out_count
        result["total_messages"] += total
        
        result["by_conversation"].append({
            "conversation_id": conv_id,
            "participants": conv.get("participants", []),
            "message_count": total,
            "inbound_count": in_count,
            "outbound_count": out_count,
            "depth": depth,
            "updated_time": conv.get("updated_time"),
            "messages": messages
        })
    
    # Resumen de profundidad
    depths = [c["depth"] for c in result["by_conversation"]]
    if depths:
        result["avg_depth"] = sum(depths) / len(depths)
        result["max_depth"] = max(depths)
        result["single_message_conversations"] = sum(1 for d in depths if d == 1)
    
    return result
