"""Resolución no destructiva de variables de entorno para los módulos Meta."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional


META_ENV_KEYS = (
    "FB_PAGE_ID",
    "META_PAGE_ID",
    "PAGE_ACCESS_TOKEN",
    "PAGE_ACCES_TOKEN",
    "META_ACCESS_TOKEN",
    "META_APP_SECRET",
    "META_PAGE_ACCESS_TOKEN",
    "META_GRAPH_VERSION",
    "META_API_VERSION",
    "META_DRY_RUN",
    "UNIVERSE_ACCOUNT_ID",
)

_ENV_REFERENCE = re.compile(
    r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"
    r"|\$([A-Za-z_][A-Za-z0-9_]*)"
    r"|\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}"
)


def _clean_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_env_file(path: Path) -> Dict[str, str]:
    """Lee un archivo .env y devuelve sus valores sin tocar ``os.environ``."""
    env_path = Path(path)
    if not env_path.is_file():
        return {}

    values: Dict[str, str] = {}
    try:
        with env_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                key = key.strip()
                if key:
                    values[key] = _clean_value(value)
    except OSError:
        return {}
    return values


def _expand_value(
    value: str,
    context: Mapping[str, str],
    seen: frozenset[str] = frozenset(),
) -> str:
    def replace(match: re.Match[str]) -> str:
        name = next(group for group in match.groups() if group is not None)
        if name in seen or name not in context:
            return match.group(0)
        return _expand_value(context[name], context, seen | {name})

    return _ENV_REFERENCE.sub(replace, value)


def load_env_values(
    env_files: Iterable[Path],
    *,
    environ: Optional[Mapping[str, str]] = None,
    keys: Optional[Iterable[str]] = None,
) -> Dict[str, str]:
    """Resuelve archivos .env con precedencia raíz, tenant y proceso.

    Los archivos se aplican en el orden recibido. El entorno del proceso tiene
    la prioridad final. La función nunca modifica ``os.environ``.
    """
    raw_values: Dict[str, str] = {}
    for env_file in env_files:
        raw_values.update(parse_env_file(Path(env_file)))

    process_values = dict(os.environ if environ is None else environ)
    context = {**raw_values, **process_values}
    resolved = {
        key: _expand_value(value, context)
        for key, value in raw_values.items()
    }
    resolved.update(process_values)

    if keys is None:
        return resolved
    selected = set(keys)
    return {
        key: value
        for key, value in resolved.items()
        if key in selected
    }
