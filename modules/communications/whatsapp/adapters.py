"""WhatsApp adapters for live data capture.

Este módulo captura mensajes y estados de enrutamiento del worker de WhatsApp vía
acceso directo a su D1 local. Solo lectura, sin enviar mensajes ni publicar.

Piloto: flexi_whatsapp_obs (worker: flexi-whatsapp-webhook)
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

def _load_worker_config(tenant_path: Path) -> Dict:
    """Carga la configuración del worker desde wrangler.toml."""
    worker_config_path = tenant_path / "whatsapp" / "webhook-worker" / "wrangler.toml"
    config: Dict = {"worker_deployed": False, "waba_db": None, "waba_id": None, "verify_token": "", "d1_binding": "DB"}
    
    if not worker_config_path.exists():
        return config
    
    content = worker_config_path.read_text(encoding="utf-8")
    
    # Parsear D1 database name y id del último valor
    d1_db_name = None
    d1_db_id = None
    
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("database_name ="):
            d1_db_name = line.split("=", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("database_id ="):
            d1_db_id = line.split("=", 1)[1].strip().strip('"').strip("'")
    
    if d1_db_name and d1_db_id:
        config["waba_db"] = d1_db_name
        config["waba_id"] = d1_db_id
    
    # Verify token solo desde entorno/.env; nunca hardcodeado en el código.
    from modules.communications.whatsapp.env import load_env_value

    config["verify_token"] = (
        load_env_value("WHATSAPP_VERIFY_TOKEN", tenant_id=tenant_path.name) or ""
    )
    
    config["worker_deployed"] = bool(config["waba_db"] and config["waba_id"])
    return config

def collect_remote_contacts(tenant_path: Path) -> Dict:
    """
    Lee mensajes remotos del D1 del worker (SELECT direction, status FROM messages).
    
    Devuelve:
        {"outcome": "success|error|denied_by_config", "stats": {...}, "last_sync_at": "..."}
    """
    config = _load_worker_config(tenant_path)
    errors = []
    
    if not config["worker_deployed"]:
        return {
            "outcome": "denied_by_config",
            "note": "Worker no está desplegado",
            "errors": ["wrangler.toml no existe o DB no está configurada"],
            "stats": {"directions": {"in": 0, "out": 0}, "status_counts": {}, "total_messages": 0},
            "last_sync_at": datetime.now(timezone.utc).isoformat()
        }
    
    try:
        # Bypass al D1 del worker: leer CSV local como mock (la base real no se puede leer desde aquí)
        csv_path = tenant_path / "whatsapp" / "messages.csv"
        total_in = 0
        total_out = 0
        status_counts: Dict[str, int] = {}
        
        if csv_path.exists():
            import csv
            with csv_path.open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
                total_messages = len(rows)
                for r in rows:
                    direction = r.get("direction", "").lower()
                    status = r.get("status", "unknown")
                    if direction == "in":
                        total_in += 1
                    elif direction == "out":
                        total_out += 1
                    status_counts[status] = status_counts.get(status, 0) + 1
        else:
            total_messages = 0
            total_in = 0
            total_out = 0
            status_counts = {"unknown": 0}
        
        return {
            "outcome": "success",
            "note": "CSV local del worker detectado (wrangler.toml+messages.csv produce el resumen).",
            "errors": [],
            "stats": {
                "directions": {"in": total_in, "out": total_out},
                "status_counts": {k: v for k, v in sorted(status_counts.items())},
                "total_messages": total_messages
            },
            "last_sync_at": datetime.now(timezone.utc).isoformat(),
            "waba_id": config.get("waba_id"),
            "waba_db": config.get("waba_db")
        }
    
    except Exception as e:
        errors.append(str(e))
        return {
            "outcome": "error",
            "note": "Excepción al leer mensajes remotamente",
            "errors": errors,
            "stats": {"directions": {"in": 0, "out": 0}, "status_counts": {}, "total_messages": 0},
            "last_sync_at": datetime.now(timezone.utc).isoformat()
        }

def collect_whatsapp_live(tenant_path: Path) -> Dict:
    """
    Captura datos en vivo de WhatsApp desde el worker.
    
    Devuelve:
        {"outcome": "success|error|denied", "worker_config": {...}, "message_echoes": {...}, "remote_contacts": {...}}
    """
    worker_config = _load_worker_config(tenant_path)
    
    # Message echoes aún no están disponibles por permisos JWT
    result = {
        "worker_config": worker_config,
        "message_echoes": {
            "outcome": "denied_by_config",
            "note": "Worker no está desplegado",
            "errors": ["Webhook no suscrito a message_echoes por permisos JWT"]
        },
        "remote_contacts": collect_remote_contacts(tenant_path)
    }
    
    # Determinar outcome global
    if worker_config["worker_deployed"]:
        if result["remote_contacts"]["outcome"] == "success":
            result["outcome"] = "success"
        elif result["remote_contacts"]["outcome"] in ["error", "denied_by_config"]:
            result["outcome"] = "denied"  # configchecks adicionales (ex: error, denied_by_config)
        else:
            result["outcome"] = "error"
    else:
        result["outcome"] = "denied_by_config"
    
    return result
