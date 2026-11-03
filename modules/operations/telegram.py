"""Notificador Telegram para la operación compartida."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path
from typing import Any, Callable, Mapping, Optional

from modules.config.env import load_env_values


class TelegramError(RuntimeError):
    """No se pudo configurar o enviar el mensaje de Telegram."""


Opener = Callable[..., Any]


def load_telegram_config(base_path: Path) -> tuple[str, str]:
    """Lee token y chat id sin modificar ``os.environ``."""
    values = load_env_values(
        (Path(base_path) / ".env",),
        environ=os.environ,
        keys=("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"),
    )
    token = str(values.get("TELEGRAM_BOT_TOKEN") or "").strip()
    chat_id = str(values.get("TELEGRAM_CHAT_ID") or "").strip()
    if not token or not chat_id:
        raise TelegramError(
            "Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en el .env raíz"
        )
    return token, chat_id


def send_message(
    text: str,
    *,
    token: str,
    chat_id: str,
    timeout: int = 10,
    opener: Optional[Opener] = None,
) -> Mapping[str, Any]:
    """Envía un mensaje de texto plano y valida la respuesta de Telegram."""
    if not token or not chat_id:
        raise TelegramError("Token o chat id de Telegram vacío")
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": True,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        if opener is None:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        else:
            response = opener(request, timeout=timeout)
            try:
                body = response.read().decode("utf-8")
            finally:
                close = getattr(response, "close", None)
                if close is not None:
                    close()
    except Exception as exc:
        raise TelegramError(f"No se pudo enviar a Telegram: {type(exc).__name__}") from exc

    try:
        result = json.loads(body)
    except ValueError as exc:
        raise TelegramError("Telegram devolvió una respuesta que no es JSON") from exc
    if not isinstance(result, Mapping) or result.get("ok") is not True:
        raise TelegramError("Telegram rechazó el mensaje")
    return result
