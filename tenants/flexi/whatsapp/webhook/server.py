#!/usr/bin/env python3
"""Receptor de webhook de WhatsApp **solo-escucha** — tenant `flexi`.

⚠️ **Reemplazado por el Worker** `../webhook-worker/` (Cloudflare Worker + D1), que es la versión
de producción: URL fija y sin depender de que esta máquina esté prendida. Este archivo queda como
herramienta local/de respaldo (por ejemplo para depurar sin desplegar) y mantiene las mismas
garantías: no responde y no envía nada.


Fase de observación del plan `tenants/flexi/docs/PLAN_WHATSAPP_FLEXI.md`: registra lo
que llega al número para medir volumen, temas y tiempos de respuesta humana.
**No responde ni envía nada**: no existe ninguna llamada de escritura a la API de Meta.

    GET  /webhook   verificación de Meta (hub.challenge) con WHATSAPP_VERIFY_TOKEN
    POST /webhook   eventos → payload crudo + fila clasificada en `logs/`
    GET  /health    liveness

Uso:
    python3 server.py --port 8787 [--log-dir DIR]

El verify token se toma de `WHATSAPP_VERIFY_TOKEN` (entorno o `growth-os/.env`).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ENV_FILE = ROOT / ".env"
TENANT_ENV_FILE = ROOT / "tenants" / "flexi" / ".env"
DEFAULT_LOG_DIR = Path(__file__).resolve().parent / "logs"

# Orden = prioridad. Clasificación para el reporte, nunca para responder.
INTENTS: list[tuple[str, tuple[str, ...]]] = [
    ("ubicacion", ("ubicacion", "direccion", "donde", "llegar", "mapa", "sucursal",
                   "estacionamiento", "ubicados")),
    ("horario", ("horario", "abren", "cierran", "abierto", "cerrado", "hora",
                 "domingo", "sabado", "festivo")),
    ("talla", ("talla", "medida", "centimetros", "cm", "calza", "ancho", "horma")),
    ("precio", ("precio", "cuanto", "costo", "cuesta", "barato", "descuento")),
    ("disponibilidad", ("tienen", "hay", "disponible", "existencia", "stock",
                        "modelo", "color", "negro", "blanco", "cafe")),
    ("promocion", ("promo", "oferta", "meses sin intereses", "msi", "2x1",
                   "envio gratis", "bono")),
    ("pedido", ("pedido", "comprar", "apartar", "apartado", "pagar",
                "transferencia", "factura")),
    ("saludo", ("hola", "buenas", "buenos dias", "buenas tardes", "buenas noches",
                "que tal")),
]


def strip_accents(text: str) -> str:
    """Quita acentos para que 'ubicación' y 'ubicacion' clasifiquen igual."""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def classify(text: str) -> str:
    """Devuelve la intención estimada del mensaje (heurística por palabras clave)."""
    clean = strip_accents(text.lower())
    for intent, keywords in INTENTS:
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}", clean):
                return intent
    return "otro"


def contact_id(wa_id: str) -> tuple[str, str]:
    """Hash corto + últimos 4 dígitos: suficiente para agrupar sin guardar el número."""
    digest = hashlib.sha256(wa_id.encode("utf-8")).hexdigest()[:12]
    return digest, wa_id[-4:]


def read_env(name: str) -> str:
    """Lee una variable de entorno o, si no está, del `.env` del repo/tenant."""
    value = os.environ.get(name)
    if value:
        return value
    for candidate in (TENANT_ENV_FILE, ENV_FILE):
        if not candidate.exists():
            continue
        for line in candidate.read_text().splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip("\"'")
    return ""


class FlexiWebhookHandler(BaseHTTPRequestHandler):
    server_version = "FlexiWebhook/1.0"
    verify_token = ""
    log_dir = DEFAULT_LOG_DIR

    def log_message(self, fmt: str, *args) -> None:  # noqa: A002 - firma de la stdlib
        message = fmt % args
        # El verify token viaja en el query string: no debe quedar en los logs.
        message = re.sub(r"\?[^\s\"]*", "?***", message)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)

    def _respond(self, code: int, body: bytes = b"", ctype: str = "text/plain") -> None:
        self.send_response(code)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - firma de la stdlib
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/health":
            payload = {"status": "ok", "service": "flexi-whatsapp-webhook",
                       "listen_only": True}
            self._respond(200, json.dumps(payload).encode(), "application/json")
            return
        if parsed.path not in ("/webhook", "/"):
            self._respond(404, b"not found")
            return
        mode = (query.get("hub.mode") or [""])[0]
        token = (query.get("hub.verify_token") or [""])[0]
        challenge = (query.get("hub.challenge") or [""])[0]
        if mode == "subscribe" and token and token == self.verify_token:
            print(f"[verify] Meta verificó el webhook (challenge={challenge})", flush=True)
            self._respond(200, challenge.encode())
            return
        print("[verify] rechazado: verify token inválido o modo distinto", flush=True)
        self._respond(403, b"forbidden")

    def do_POST(self) -> None:  # noqa: N802 - firma de la stdlib
        if urllib.parse.urlparse(self.path).path not in ("/webhook", "/"):
            self._respond(404, b"not found")
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            print(f"[post] payload ilegible: {exc}", flush=True)
            self._respond(400, b"bad request")
            return
        try:
            rows = self.handle_payload(payload)
        except Exception as exc:  # nunca romper la recepción por un error de parseo
            print(f"[post] error procesando payload: {exc!r}", flush=True)
            rows = 0
        # Siempre 200: Meta reintenta si no recibe 200 y eso duplicaría el log.
        self._respond(200, json.dumps({"received": rows}).encode(), "application/json")

    def _append(self, name: str, obj: dict) -> None:
        self.log_dir.mkdir(parents=True, exist_ok=True)
        day = datetime.now().strftime("%Y-%m-%d")
        path = self.log_dir / f"{name}_{day}.jsonl"
        line = json.dumps(obj, ensure_ascii=False)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def handle_payload(self, payload: dict) -> int:
        """Registra el evento completo y devuelve cuántos mensajes se normalizaron."""
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._append("raw_events", {"received_at": now, "payload": payload})
        rows = 0
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {}) or {}
                rows += self._handle_messages(value, now)
                rows += self._handle_echoes(value, now)
                for status in value.get("statuses", []) or []:
                    self._append("statuses", {
                        "received_at": now,
                        "status": status.get("status"),
                        "message_id": status.get("id"),
                        "recipient_hash": contact_id(status.get("recipient_id", ""))[0],
                    })
        return rows

    def _handle_messages(self, value: dict, now: str) -> int:
        """Mensajes ENTRANTES del cliente (messages[])."""
        contacts = {c.get("wa_id"): c.get("profile", {}).get("name", "")
                    for c in value.get("contacts", []) or []}
        count = 0
        for message in value.get("messages", []) or []:
            wa_id = message.get("from", "")
            kind = message.get("type", "desconocido")
            text = ""
            if kind == "text":
                text = (message.get("text") or {}).get("body", "")
            elif kind == "interactive":
                interactive = message.get("interactive") or {}
                text = ((interactive.get("button_reply") or {}).get("title")
                        or (interactive.get("list_reply") or {}).get("title") or "")
            digest, last4 = contact_id(wa_id)
            timestamp = message.get("timestamp", "")
            row = {
                "received_at": now,
                "wa_ts": timestamp,
                "hour_local": _hour_local(timestamp),
                "direction": "in",
                "intent": classify(text),
                "type": kind,
                "text": text,
                "text_len": len(text),
                "has_media": kind in ("image", "audio", "video", "document", "sticker"),
                "is_reply_to_template": bool(
                    (message.get("context") or {}).get("id")),
                "contact_hash": digest,
                "contact_last4": last4,
                "contact_name": contacts.get(wa_id, ""),
            }
            self._append("messages", row)
            print(f"[in ] {row['intent']:15} {kind:11} \"{text[:48]}\"", flush=True)
            count += 1
        return count

    def _handle_echoes(self, value: dict, now: str) -> int:
        """Mensajes que la sucursal manda DESDE la app (coexistencia: smb_message_echoes)."""
        count = 0
        for echo in value.get("smb_message_echoes", []) or []:
            message = echo.get("message", echo) or {}
            text = ((message.get("text") or {}).get("body", "")
                    if message.get("type") == "text" else "")
            digest, last4 = contact_id(message.get("to", message.get("from", "")))
            row = {
                "received_at": now,
                "wa_ts": message.get("timestamp", ""),
                "hour_local": _hour_local(message.get("timestamp", "")),
                "direction": "out_app",
                "intent": classify(text),
                "type": message.get("type", "desconocido"),
                "text": text,
                "text_len": len(text),
                "contact_hash": digest,
                "contact_last4": last4,
            }
            self._append("messages", row)
            print(f"[out] (app)          \"{text[:48]}\"", flush=True)
            count += 1
        return count


def _hour_local(timestamp: str) -> str:
    """Hora local (America/Matamoros) aproximada a partir del epoch de WhatsApp."""
    if not timestamp.isdigit():
        return ""
    try:
        from zoneinfo import ZoneInfo
        return datetime.fromtimestamp(int(timestamp), ZoneInfo("America/Matamoros")
                                      ).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Webhook WhatsApp solo-escucha (flexi)")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR)
    args = parser.parse_args()

    verify_token = read_env("WHATSAPP_VERIFY_TOKEN")
    if not verify_token:
        print("ERROR: falta WHATSAPP_VERIFY_TOKEN (entorno o growth-os/.env)", file=sys.stderr)
        return 2

    FlexiWebhookHandler.verify_token = verify_token
    FlexiWebhookHandler.log_dir = args.log_dir
    server = ThreadingHTTPServer((args.host, args.port), FlexiWebhookHandler)
    print(f"Webhook solo-escucha en http://{args.host}:{args.port}/webhook", flush=True)
    print(f"Logs en {args.log_dir}  ·  listen_only=True (nunca responde)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\ndetenido por el usuario", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
