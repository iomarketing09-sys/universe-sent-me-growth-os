"""Escrituras puntuales a D1 (backfill). Separado de ``d1.py`` a propósito.

``d1.py`` garantiza solo lectura para todo el módulo. Este archivo existe solo
para reparar datos ya recibidos (por ejemplo, ecos que el worker descartó) y
solo acepta ``INSERT OR IGNORE``/``UPDATE``/``DELETE`` con parámetros.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

import requests

from modules.communications.whatsapp.d1 import API_BASE, D1Error, load_d1_config

ALLOWED = re.compile(r"^\s*(insert\s+or\s+ignore|insert|delete|update)\b", re.IGNORECASE)
FORBIDDEN = re.compile(
    r"\b(drop|alter|create|replace|attach|vacuum|pragma)\b", re.IGNORECASE
)


def execute(
    sql: str,
    params: Optional[List[Any]] = None,
    tenant_id: str = "flexi",
    base_path: Optional[str] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    """Ejecuta una escritura controlada y devuelve la metadata de D1."""
    from modules.communications.whatsapp.env import load_env_value

    if not ALLOWED.match(sql) or FORBIDDEN.search(sql):
        raise D1Error("Consulta de escritura no permitida por d1_write.")

    config = load_d1_config(tenant_id, base_path)
    if not config["account_id"] or not config["database_id"]:
        raise D1Error(
            f"Falta cloudflare.account_id/d1_database_id en tenants/{tenant_id}/whatsapp/config.json"
        )
    token = load_env_value("CF_API_TOKEN", tenant_id=tenant_id) or load_env_value(
        "CLOUDFLARE_API_TOKEN", tenant_id=tenant_id
    )
    if not token:
        raise D1Error("Falta CF_API_TOKEN en el entorno o en .env.")

    url = (
        f"{API_BASE}/accounts/{config['account_id']}"
        f"/d1/database/{config['database_id']}/query"
    )
    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            json={"sql": sql, "params": params or []},
            timeout=timeout,
        )
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise D1Error(f"No se pudo ejecutar la escritura en D1: {exc}") from exc

    if response.status_code >= 400 or not payload.get("success", False):
        errors = payload.get("errors") or []
        message = "; ".join(str(e.get("message", e)) for e in errors) or f"HTTP {response.status_code}"
        raise D1Error(f"D1 rechazó la escritura: {message}")

    results = payload.get("result") or []
    return (results[0] if results else {}).get("meta") or {}
