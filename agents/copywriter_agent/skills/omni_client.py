"""Cliente mínimo para OmniRoute (OpenAI-compatible)."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


DEFAULT_BASE_URL = "http://localhost:20128/v1"
DEFAULT_MODEL = "groq/openai/gpt-oss-120b"
FALLBACK_MODELS = ("groq/openai/gpt-oss-20b", "gemini/gemini-3.5-flash")


class OmniRouteError(RuntimeError):
    """Error de OmniRoute sin exponer credenciales."""


@dataclass
class ChatResult:
    content: str
    model: str
    usage: Dict[str, Any]


def _parse_sse(text: str) -> Dict[str, Any]:
    chunks: List[str] = []
    usage: Dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if not payload or payload == "[DONE]":
            continue
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            continue
        usage = event.get("usage", usage) or usage
        for choice in event.get("choices", []):
            delta = choice.get("delta", {}) or {}
            if delta.get("content"):
                chunks.append(delta["content"])
    return {"content": "".join(chunks), "usage": usage}


class OmniRouteClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 180,
    ):
        self.base_url = (base_url or os.getenv("OMNIROUTE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or os.getenv("OMNIROUTE_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.timeout = timeout

    def chat_with_fallback(
        self,
        messages: List[Dict[str, str]],
        models: Iterable[str],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        reasoning_effort: Optional[str] = "low",
    ) -> ChatResult:
        last_error: Optional[Exception] = None
        for model in models:
            try:
                return self._chat_once(messages, model, max_tokens, temperature, reasoning_effort)
            except (OmniRouteError, requests.RequestException) as exc:
                last_error = exc
                continue
        raise OmniRouteError(f"Todos los modelos fallaron. Último error: {last_error}")

    def _chat_once(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int,
        temperature: float,
        reasoning_effort: Optional[str],
    ) -> ChatResult:
        if not self.api_key:
            raise OmniRouteError("Falta OMNIROUTE_API_KEY (o OPENAI_API_KEY) para llamar al modelo.")

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
        }
        if reasoning_effort and model.startswith("groq/openai/gpt-oss"):
            payload["reasoning_effort"] = reasoning_effort

        headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "text/event-stream"}
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=self.timeout,
            stream=True,
        )
        if response.status_code != 200:
            error_text = response.text[:500]
            raise OmniRouteError(f"HTTP {response.status_code}: {error_text}")

        result = _parse_sse(response.text)
        if not result["content"].strip():
            raise OmniRouteError("Respuesta vacía del modelo")
        return ChatResult(content=result["content"], model=model, usage=result["usage"])


def extract_json(text: str) -> Dict[str, Any]:
    """Extrae el primer objeto JSON válido del texto."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Buscar el primer objeto JSON balanceado
        depth = 0
        start = -1
        for i, ch in enumerate(text):
            if ch == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and start != -1:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        pass
    raise ValueError("No se encontró JSON válido en la respuesta")
