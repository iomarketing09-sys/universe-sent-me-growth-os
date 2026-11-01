"""Cliente compartido para el gateway OmniRoute compatible con OpenAI."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


DEFAULT_BASE_URL = "http://127.0.0.1:20128/v1"
DEFAULT_MODEL = "openai/gpt-4.1-mini"
DEFAULT_TIMEOUT = 45


class OmniRouteError(RuntimeError):
    """Error de OmniRoute sin incluir credenciales."""


@dataclass
class ChatResult:
    content: str
    model: str
    usage: Dict[str, Any] = field(default_factory=dict)
    latency_ms: int = 0
    data: Optional[Dict[str, Any]] = None


def extract_json(text: str) -> Dict[str, Any]:
    """Extrae un objeto JSON aunque el modelo añada texto o cercas Markdown."""
    value = str(text or "").strip()
    if not value:
        raise ValueError("Respuesta JSON vacía")
    if value.startswith("```"):
        parts = value.split("```")
        if len(parts) >= 2:
            value = parts[1].strip()
            if value.lower().startswith("json"):
                value = value[4:].strip()
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        payload = None

    if not isinstance(payload, dict):
        depth = 0
        start = -1
        payload = None
        for index, character in enumerate(value):
            if character == "{":
                if depth == 0:
                    start = index
                depth += 1
            elif character == "}" and depth:
                depth -= 1
                if depth == 0 and start >= 0:
                    try:
                        candidate = json.loads(value[start : index + 1])
                    except json.JSONDecodeError:
                        continue
                    if isinstance(candidate, dict):
                        payload = candidate
                        break
    if not isinstance(payload, dict):
        raise ValueError("No se encontró un objeto JSON válido")
    return payload


def _read_env_value(path: Path, keys: Iterable[str]) -> Optional[str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    wanted = set(keys)
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() in wanted:
            return value.strip().strip("'").strip('"') or None
    return None


def _omniroute_config(tenant_id: str) -> Dict[str, Any]:
    path = Path.home() / ".omniroute" / "config.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    contexts = payload.get("contexts")
    if not isinstance(contexts, dict):
        return {}
    context = contexts.get(tenant_id) or contexts.get("default") or {}
    return context if isinstance(context, dict) else {}


def resolve_credentials(
    tenant_id: str = "universe",
    base_path: Optional[Path] = None,
) -> tuple[Optional[str], Optional[str]]:
    """Resuelve API key y base URL sin imprimir ni persistir secretos."""
    keys = ("OPENAI_API_KEY", "OMNIROUTE_API_KEY")
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OMNIROUTE_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OMNIROUTE_BASE_URL")

    root = Path(base_path) if base_path else Path(__file__).resolve().parents[2]
    env_files = (root / ".env", root / "tenants" / tenant_id / ".env")
    for env_file in env_files:
        api_key = api_key or _read_env_value(env_file, keys)
        base_url = base_url or _read_env_value(env_file, ("OPENAI_BASE_URL", "OMNIROUTE_BASE_URL"))

    config = _omniroute_config(tenant_id)
    api_key = api_key or str(config.get("apiKey") or "").strip() or None
    base_url = base_url or str(config.get("baseUrl") or "").strip() or None
    return api_key, base_url


class OmniRouteClient:
    """Cliente mínimo y testeable para chat de OmniRoute."""

    def __init__(
        self,
        *,
        tenant_id: str = "universe",
        base_path: Optional[Path] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        resolved_key, resolved_url = resolve_credentials(tenant_id, base_path)
        self.tenant_id = tenant_id
        self.base_url = (base_url or resolved_url or DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or resolved_key
        self.timeout = timeout

    def _post(
        self,
        messages: List[Dict[str, str]],
        *,
        model: str,
        max_tokens: int,
        temperature: float,
        json_mode: bool,
    ) -> ChatResult:
        if not self.api_key:
            raise OmniRouteError(
                "Falta OPENAI_API_KEY/OMNIROUTE_API_KEY o la credencial del contexto OmniRoute."
            )

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        started = time.monotonic()
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise OmniRouteError(f"No se pudo conectar a OmniRoute: {type(exc).__name__}") from exc
        latency_ms = int((time.monotonic() - started) * 1000)

        if response.status_code != 200:
            try:
                body = response.json()
                message = body.get("error", {}).get("message") or body
            except ValueError:
                message = response.text[:300]
            raise OmniRouteError(f"OmniRoute HTTP {response.status_code}: {message}")

        try:
            body = response.json()
            content = body["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise OmniRouteError("OmniRoute devolvió una respuesta sin contenido válido") from exc
        if not isinstance(content, str) or not content.strip():
            raise OmniRouteError("OmniRoute devolvió contenido vacío")

        return ChatResult(
            content=content.strip(),
            model=str(body.get("model") or model),
            usage=body.get("usage") if isinstance(body.get("usage"), dict) else {},
            latency_ms=latency_ms,
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 300,
        temperature: float = 0.6,
    ) -> ChatResult:
        return self._post(
            messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            json_mode=False,
        )

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        *,
        model: str = DEFAULT_MODEL,
        max_tokens: int = 300,
        temperature: float = 0.4,
    ) -> ChatResult:
        result = self._post(
            messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            json_mode=True,
        )
        try:
            result.data = extract_json(result.content)
        except ValueError as exc:
            raise OmniRouteError(f"El modelo no devolvió JSON válido: {exc}") from exc
        return result
