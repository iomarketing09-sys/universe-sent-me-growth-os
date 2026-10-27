"""Cliente D1 de solo lectura para el worker de WhatsApp de un tenant.

Usa la API REST de Cloudflare (``/d1/database/<id>/query``). No usa ``wrangler``
y nunca imprime credenciales. Solo acepta consultas de lectura.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from modules.communications.whatsapp.env import project_root

API_BASE = "https://api.cloudflare.com/client/v4"
READ_ONLY = re.compile(r"^\s*(select|with|pragma)\b", re.IGNORECASE)
FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|replace|attach|vacuum)\b",
    re.IGNORECASE,
)


class D1Error(RuntimeError):
    """Error legible al consultar D1 (sin exponer el token)."""


def _tenant_dir(tenant_id: str, base_path: Optional[str] = None) -> Path:
    root = Path(base_path) if base_path else project_root()
    return root / "tenants" / tenant_id


def load_d1_config(tenant_id: str, base_path: Optional[str] = None) -> Dict[str, str]:
    """Lee ``account_id`` y ``d1_database_id`` del config o del wrangler.toml."""
    tenant_dir = _tenant_dir(tenant_id, base_path)
    config_path = tenant_dir / "whatsapp" / "config.json"
    account_id = ""
    database_id = ""

    if config_path.is_file():
        data = json.loads(config_path.read_text(encoding="utf-8"))
        cloudflare = data.get("cloudflare") or {}
        account_id = str(cloudflare.get("account_id") or "")
        database_id = str(cloudflare.get("d1_database_id") or "")

    wrangler = tenant_dir / "whatsapp" / "webhook-worker" / "wrangler.toml"
    if wrangler.is_file() and not database_id:
        for line in wrangler.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("database_id ="):
                database_id = line.split("=", 1)[1].strip().strip('"').strip("'")

    return {"account_id": account_id, "database_id": database_id}


def _validate(sql: str) -> str:
    if not READ_ONLY.match(sql) or FORBIDDEN.search(sql):
        raise D1Error("Este módulo es de solo lectura: se rechazó una consulta de escritura.")
    return sql


def query(
    sql: str,
    params: Optional[List[Any]] = None,
    tenant_id: str = "flexi",
    base_path: Optional[str] = None,
    timeout: int = 30,
) -> List[Dict[str, Any]]:
    """Ejecuta una consulta de lectura y devuelve las filas como dicts."""
    from modules.communications.whatsapp.env import load_env_value

    sql = _validate(sql)
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
    except requests.RequestException as exc:
        raise D1Error(f"No se pudo conectar con Cloudflare: {exc}") from exc

    try:
        payload = response.json()
    except ValueError:
        raise D1Error(f"Cloudflare devolvió HTTP {response.status_code} sin JSON.") from None

    if response.status_code >= 400 or not payload.get("success", False):
        errors = payload.get("errors") or []
        message = "; ".join(str(e.get("message", e)) for e in errors) or f"HTTP {response.status_code}"
        raise D1Error(f"D1 rechazó la consulta: {message}")

    results = payload.get("result") or []
    if isinstance(results, dict):
        results = [results]
    rows: List[Dict[str, Any]] = []
    for block in results:
        for row in (block or {}).get("results") or []:
            rows.append(row)
    return rows


def scalar(sql: str, params: Optional[List[Any]] = None, **kwargs: Any) -> Any:
    rows = query(sql, params=params, **kwargs)
    if not rows:
        return None
    return next(iter(rows[0].values()))
