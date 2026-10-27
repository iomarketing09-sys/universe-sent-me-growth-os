"""Lectura de credenciales por variable de entorno, sin exponerlas.

Busca primero en el entorno del proceso y después en ``.env`` del repo y del
tenant. Nunca imprime ni registra valores.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


def _read_env_file(path: Path, name: str) -> Optional[str]:
    if not path.is_file():
        return None
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == name:
                return value.strip().strip('"').strip("'")
    except OSError:
        return None
    return None


def load_env_value(name: str, tenant_id: Optional[str] = None) -> Optional[str]:
    """Valor de ``name`` o ``None``. No lanza si falta."""
    value = os.environ.get(name)
    if value:
        return value

    root = project_root()
    candidates = []
    if tenant_id:
        candidates.append(root / "tenants" / tenant_id / ".env")
    candidates.append(root / ".env")

    for path in candidates:
        value = _read_env_file(path, name)
        if value:
            return value
    return None


def require_env_value(name: str, tenant_id: Optional[str] = None) -> str:
    value = load_env_value(name, tenant_id)
    if not value:
        raise RuntimeError(
            f"Falta la variable {name}. Agrégala al entorno o a .env (no se muestra su valor)."
        )
    return value
