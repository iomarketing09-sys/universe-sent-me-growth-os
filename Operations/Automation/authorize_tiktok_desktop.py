#!/usr/bin/env python3
"""Authorize the official TikTok Desktop OAuth flow for Universe Sent Me.

This script is intentionally local-only. It binds a one-time callback to
127.0.0.1, uses PKCE and stores the returned tokens outside the repository.
It does not fetch metrics, write ledgers, publish content or contact OmniRoute.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sys
import time
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import requests

BRAND = "Universe Sent Me"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
AUTHORIZE_URL = "https://www.tiktok.com/v2/auth/authorize/"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def expand(value: str) -> Path:
    return Path(value).expanduser().resolve()


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("brand") != BRAND:
        raise RuntimeError("Configuration brand must be exactly 'Universe Sent Me'.")
    if not isinstance(config.get("tiktok"), dict):
        raise RuntimeError("Missing tiktok configuration block.")
    return config


def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(temp, 0o600)
    temp.replace(path)
    os.chmod(path, 0o600)


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class CallbackServer(HTTPServer):
    result: dict[str, str] | None = None


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        query = parse_qs(urlparse(self.path).query)
        self.server.result = {key: values[0] for key, values in query.items() if values}  # type: ignore[attr-defined]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<h1>Autorizacion recibida</h1><p>Ya puedes volver a la terminal de Xubuntu.</p>"
        )

    def log_message(self, _format: str, *_args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("~/.config/usm-metrics/config.json").expanduser(),
        help="Private local configuration file copied from official_metrics_config.example.json.",
    )
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()

    config = load_config(args.config.expanduser())
    tiktok = config["tiktok"]
    redirect_uri = str(tiktok["redirect_uri"])
    parsed = urlparse(redirect_uri)
    if parsed.hostname not in {"127.0.0.1", "localhost"} or not parsed.port:
        raise RuntimeError("TikTok Desktop redirect_uri must use localhost/127.0.0.1 and an explicit port.")

    client_key = os.environ.get(str(tiktok["client_key_env"]))
    client_secret = os.environ.get(str(tiktok["client_secret_env"]))
    if not client_key or not client_secret:
        raise SystemExit(
            "TikTok client values are missing from local environment variables. Do not paste them into chat or this repository."
        )

    scopes = list(tiktok.get("required_scopes", []))
    approved_scopes = {"user.info.basic", "video.list"}
    if set(scopes) != approved_scopes:
        raise RuntimeError("Only the approved TikTok scopes ['user.info.basic', 'video.list'] are permitted for this pilot.")

    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(72)[:96]
    challenge = sha256_hex(verifier)
    server = CallbackServer((parsed.hostname, parsed.port), CallbackHandler)
    server.timeout = 1
    params = {
        "client_key": client_key,
        "response_type": "code",
        "scope": ",".join(scopes),
        "redirect_uri": redirect_uri,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    authorize_url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    print("Se abrirá TikTok para autorizar únicamente la lectura de videos de Universe Sent Me.")
    print("Si el navegador no se abre, copia esta URL manualmente:")
    print(authorize_url)
    webbrowser.open(authorize_url, new=1)

    deadline = time.monotonic() + args.timeout_seconds
    while server.result is None and time.monotonic() < deadline:
        server.handle_request()
    server.server_close()
    result = server.result
    if result is None:
        raise SystemExit("OAuth timeout: no callback was received on the local endpoint.")
    if result.get("state") != state:
        raise SystemExit("OAuth state mismatch. Token exchange was aborted.")
    if result.get("error"):
        raise SystemExit(f"TikTok authorization failed: {result.get('error_description', result['error'])}")
    code = result.get("code")
    if not code:
        raise SystemExit("TikTok callback did not contain an authorization code.")

    response = requests.post(
        TOKEN_URL,
        data={
            "client_key": client_key,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    payload = response.json()
    if response.status_code != 200 or payload.get("error"):
        raise SystemExit(f"TikTok token exchange failed with HTTP {response.status_code}: {payload.get('error_description', payload.get('error'))}")
    granted = set(str(payload.get("scope", "")).split(","))
    if approved_scopes != granted:
        raise SystemExit("Granted scopes do not match the approved read-only scope. Token was not saved.")

    payload["brand"] = BRAND
    payload["obtained_at_utc"] = utc_now()
    payload["redirect_uri"] = redirect_uri
    token_file = expand(str(tiktok["token_file"]))
    write_private_json(token_file, payload)
    print(json.dumps({"status": "authorized", "brand": BRAND, "scope": payload["scope"], "token_file": str(token_file)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Authorization cancelled; no token was written.", file=sys.stderr)
        raise SystemExit(130)
