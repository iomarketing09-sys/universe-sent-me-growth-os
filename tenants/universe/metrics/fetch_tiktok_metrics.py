#!/usr/bin/env python3
"""
Extractor oficial de métricas de TikTok para Universe Sent Me.
Usa TikTok Display API v2 (/v2/video/list/).
Lee credenciales desde tenants/universe/.env y actualiza metrics_video_log.csv.
"""

from __future__ import annotations
import argparse
import csv
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
VIDEO_LIST_URL = "https://open.tiktokapis.com/v2/video/list/"
FIELDS = "id,create_time,share_url,title,like_count,comment_count,share_count,view_count"
APPROVED_SCOPES = ["user.info.basic", "video.list"]

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_env(env_path: Path) -> dict[str, str]:
    env = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)

def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

class CallbackServer(HTTPServer):
    result: dict[str, str] | None = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        query = parse_qs(urlparse(self.path).query)
        self.server.result = {k: v[0] for k, v in query.items() if v}
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h1>Autorizacion de TikTok recibida con exito</h1><p>Ya puedes volver a la terminal.</p>")

    def log_message(self, _format: str, *_args: object) -> None:
        return

def run_oauth_flow(client_key: str, client_secret: str, redirect_uri: str, token_file: Path) -> dict[str, Any]:
    parsed = urlparse(redirect_uri)
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(72)[:96]
    challenge = sha256_hex(verifier)
    
    server = CallbackServer((parsed.hostname, parsed.port or 8765), CallbackHandler)
    server.timeout = 1
    
    params = {
        "client_key": client_key,
        "response_type": "code",
        "scope": ",".join(APPROVED_SCOPES),
        "redirect_uri": redirect_uri,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    print("\n🌐 Se abrirá TikTok en tu navegador para autorizar la lectura de videos.")
    print(f"Si no se abre automáticamente, entra a este enlace:\n{auth_url}\n")
    webbrowser.open(auth_url, new=1)
    
    deadline = time.monotonic() + 300
    while server.result is None and time.monotonic() < deadline:
        server.handle_request()
    server.server_close()
    
    res = server.result
    if not res or res.get("state") != state or not res.get("code"):
        raise RuntimeError("Fallo o tiempo de espera agotado en la autorización de TikTok.")
        
    code = res["code"]
    token_resp = requests.post(
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
    payload = token_resp.json()
    if token_resp.status_code != 200 or payload.get("error"):
        err = payload.get("error_description", payload.get("error"))
        raise RuntimeError(f"Error al canjear código de TikTok: {err}")
        
    payload["brand"] = BRAND
    payload["obtained_at_utc"] = utc_now()
    payload["redirect_uri"] = redirect_uri
    write_private_json(token_file, payload)
    print("✅ Nuevo token de TikTok obtenido y guardado.")
    return payload

def get_valid_token(client_key: str, client_secret: str, token_file: Path, redirect_uri: str) -> dict[str, Any]:
    token: dict[str, Any] | None = None
    if token_file.exists():
        try:
            token = json.loads(token_file.read_text(encoding="utf-8"))
        except Exception:
            token = None

    if token and token.get("refresh_token"):
        print("🔄 Renovando token de acceso de TikTok mediante refresh token...")
        resp = requests.post(
            TOKEN_URL,
            data={
                "client_key": client_key,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": token["refresh_token"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        data = resp.json()
        if resp.status_code == 200 and not data.get("error"):
            data["brand"] = BRAND
            data["obtained_at_utc"] = utc_now()
            data["redirect_uri"] = redirect_uri
            write_private_json(token_file, data)
            print("✅ Token de TikTok renovado con éxito.")
            return data
        else:
            print(f"⚠️ No se pudo refrescar el token ({data.get('error_description', data.get('error'))}). Iniciando nuevo login...")

    return run_oauth_flow(client_key, client_secret, redirect_uri, token_file)

def list_videos(access_token: str, max_pages: int = 5) -> list[dict[str, Any]]:
    cursor: int | None = None
    videos: list[dict[str, Any]] = []
    for _ in range(max_pages):
        body: dict[str, Any] = {"max_count": 20}
        if cursor is not None:
            body["cursor"] = cursor
        response = requests.post(
            VIDEO_LIST_URL,
            params={"fields": FIELDS},
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
            json=body,
            timeout=30,
        )
        payload = response.json()
        if response.status_code != 200 or payload.get("error", {}).get("code") not in {None, "ok"}:
            err = payload.get("error", {})
            raise RuntimeError(f"Error listando videos de TikTok: {err}")
        data = payload.get("data", {})
        videos.extend(data.get("videos", []))
        if not data.get("has_more"):
            break
        cursor = data.get("cursor")
        if not isinstance(cursor, int):
            break
    return videos

def update_csv_ledger(csv_path: Path, new_tt_records: list[dict[str, Any]]) -> None:
    fieldnames = [
        "Fecha", "Plataforma", "Video_ID", "Titulo_Concepto",
        "Duracion_Seg", "Plays_Views", "Watch_Time_Prom_Seg",
        "Reacciones", "Shares", "Comentarios", "Permalink"
    ]
    
    existing_rows = []
    if csv_path.exists():
        with csv_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing_rows.append(r)
    
    existing_by_id = {r["Video_ID"]: r for r in existing_rows}
    for rec in new_tt_records:
        existing_by_id[rec["Video_ID"]] = rec
        
    final_rows = list(existing_by_id.values())
    final_rows.sort(key=lambda x: x.get("Fecha", ""), reverse=True)
    
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)
        
    print(f"📊 metrics_video_log.csv actualizado con éxito: {len(final_rows)} registros totales.")

def main() -> int:
    script_dir = Path(__file__).resolve().parent
    tenant_dir = script_dir.parent
    env = load_env(tenant_dir / ".env")
    
    client_key = env.get("TIKTOK_CLIENT_KEY") or env.get("USM_TIKTOK_CLIENT_KEY") or os.environ.get("TIKTOK_CLIENT_KEY") or os.environ.get("USM_TIKTOK_CLIENT_KEY")
    client_secret = env.get("TIKTOK_CLIENT_SECRET") or env.get("USM_TIKTOK_CLIENT_SECRET") or os.environ.get("TIKTOK_CLIENT_SECRET") or os.environ.get("USM_TIKTOK_CLIENT_SECRET")
    
    if not client_key or not client_secret:
        raise SystemExit("❌ TIKTOK_CLIENT_KEY o TIKTOK_CLIENT_SECRET no fueron encontrados en tenants/universe/.env")

    token_file = Path("~/.config/usm-metrics/tiktok-token.json").expanduser()
    redirect_uri = "http://127.0.0.1:8765/callback/"

    token = get_valid_token(client_key, client_secret, token_file, redirect_uri)
    access_token = token.get("access_token")
    if not access_token:
        raise SystemExit("❌ No se encontró access_token válido de TikTok.")

    print("📡 Conectado a TikTok API. Consultando lista de videos públicos...")
    videos = list_videos(access_token, max_pages=5)
    print(f"🎬 Videos obtenidos de TikTok: {len(videos)}")

    csv_records = []
    for v in videos:
        vid_id = str(v.get("id"))
        create_ts = v.get("create_time", 0)
        pub_date = datetime.fromtimestamp(create_ts, timezone.utc).strftime("%Y-%m-%d") if create_ts else datetime.now().strftime("%Y-%m-%d")
        title = v.get("title", "Sin título")
        views = v.get("view_count", 0)
        likes = v.get("like_count", 0)
        shares = v.get("share_count", 0)
        comments = v.get("comment_count", 0)
        share_url = v.get("share_url", f"https://www.tiktok.com/@universe_sent_me/video/{vid_id}")

        csv_records.append({
            "Fecha": pub_date,
            "Plataforma": "TikTok",
            "Video_ID": vid_id,
            "Titulo_Concepto": title,
            "Duracion_Seg": "",
            "Plays_Views": str(views),
            "Watch_Time_Prom_Seg": "",
            "Reacciones": str(likes),
            "Shares": str(shares),
            "Comentarios": str(comments),
            "Permalink": share_url
        })

    # Guardar evidencia JSON
    captured = utc_now()
    evidence = {
        "brand": BRAND,
        "platform": "TikTok",
        "captured_at_utc": captured,
        "total_videos": len(videos),
        "videos": videos
    }
    output_dir = script_dir / "video"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{captured[:10]}_TikTok_Official_Metrics.json"
    write_private_json(output_file, evidence)
    print(f"💾 Evidencia guardada en: {output_file}")

    # Actualizar CSV
    update_csv_ledger(script_dir / "metrics_video_log.csv", csv_records)

    if csv_records:
        print("\n--- Top Videos de TikTok por Vistas ---")
        sorted_tt = sorted(csv_records, key=lambda x: int(x["Plays_Views"]) if x["Plays_Views"].isdigit() else 0, reverse=True)
        for r in sorted_tt[:5]:
            print(f"• [{r['Video_ID']}] {r['Titulo_Concepto'][:40]}...: {r['Plays_Views']} vistas, {r['Reacciones']} likes, {r['Shares']} shares")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
