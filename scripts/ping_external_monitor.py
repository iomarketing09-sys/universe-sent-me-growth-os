#!/usr/bin/env python3
"""Envía el latido del host a un monitor externo.

El monitor externo es un sensor del NOC: si el host deja de enviar el latido,
el proveedor alerta aunque el propio host ya no pueda ejecutar el watchdog.
La URL es un secreto operativo y nunca se imprime.
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any, Callable, Mapping, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.config.env import load_env_values  # noqa: E402


class HeartbeatError(RuntimeError):
    """No se pudo enviar el latido al monitor externo."""


Opener = Callable[..., Any]


def load_heartbeat_url(
    base_path: Path = ROOT,
    *,
    environ: Optional[Mapping[str, str]] = None,
) -> str:
    """Lee la URL del heartbeat sin modificar ``os.environ``."""
    values = load_env_values(
        (Path(base_path) / ".env",),
        environ=os.environ if environ is None else environ,
        keys=("EXTERNAL_MONITOR_HEARTBEAT_URL",),
    )
    return str(values.get("EXTERNAL_MONITOR_HEARTBEAT_URL") or "").strip()


def ping(url: str, *, timeout: int = 10, opener: Optional[Opener] = None) -> int:
    """Hace un GET al heartbeat y devuelve el HTTP status."""
    if not url:
        raise HeartbeatError("Falta EXTERNAL_MONITOR_HEARTBEAT_URL")
    request = urllib.request.Request(url, method="GET")
    try:
        if opener is None:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status = int(getattr(response, "status", 0) or 0)
        else:
            response = opener(request, timeout=timeout)
            try:
                status = int(getattr(response, "status", 0) or 0)
            finally:
                close = getattr(response, "close", None)
                if close is not None:
                    close()
    except Exception as exc:
        raise HeartbeatError(
            f"No se pudo enviar el latido: {type(exc).__name__}"
        ) from exc
    if status >= 400:
        raise HeartbeatError(f"El monitor respondió HTTP {status}")
    return status


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Latido del host al monitor externo")
    parser.add_argument(
        "--url",
        help="URL de heartbeat; si se omite, se lee EXTERNAL_MONITOR_HEARTBEAT_URL del .env",
    )
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Comprueba la configuración sin enviar el latido",
    )
    args = parser.parse_args(argv)

    url = args.url or load_heartbeat_url()
    if not url:
        print("EXTERNAL_MONITOR_HEARTBEAT_URL no configurado; latido omitido.")
        return 0
    if args.dry_run:
        print("Latido configurado; no se envió (dry-run).")
        return 0

    try:
        status = ping(url, timeout=max(1, args.timeout))
    except HeartbeatError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Latido enviado al monitor externo (HTTP {status}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
