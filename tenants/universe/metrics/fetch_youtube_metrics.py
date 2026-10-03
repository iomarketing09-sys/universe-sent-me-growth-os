#!/usr/bin/env python3
"""
Extractor oficial de métricas de YouTube Shorts / Videos para Universe Sent Me.
Usa YouTube Data API v3 y YouTube Analytics API v2.
Escribe evidencia JSON en video/ y consolida las filas en metrics_video_log.csv.
"""

from __future__ import annotations
import argparse
import csv
import json
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BRAND = "Universe Sent Me"
PERFORMANCE_METRICS = [
    "views",
    "engagedViews",
    "likes",
    "comments",
    "shares",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "subscribersGained",
]

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("brand") != BRAND:
        raise RuntimeError("Configuration brand must be exactly 'Universe Sent Me'.")
    return config

def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)

def parse_iso_duration(duration_str: str) -> int:
    match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration_str or '')
    if not match:
        return 0
    m = int(match.group(1) or 0)
    s = int(match.group(2) or 0)
    return m * 60 + s

def get_credentials(config: dict[str, Any]) -> Credentials:
    youtube = config["youtube"]
    scopes = list(youtube["scopes"])
    token_file = Path(str(youtube["token_file"])).expanduser()
    creds: Credentials | None = None

    if token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_file), scopes)
        except Exception:
            creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as err:
            creds = None

    if not creds or not creds.valid:
        client_secret_file = Path(str(youtube["client_secret_file"])).expanduser()
        if not client_secret_file.exists():
            raise RuntimeError(f"Falta el client secret en {client_secret_file}")
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_file), scopes)
        creds = flow.run_local_server(host="127.0.0.1", port=0, prompt="consent")
        write_private_json(token_file, json.loads(creds.to_json()))

    return creds

def as_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    headers = [column["name"] for column in payload.get("columnHeaders", [])]
    return [dict(zip(headers, row, strict=False)) for row in payload.get("rows", [])]

def query_report(analytics: Any, metrics: list[str], start_date: str, end_date: str) -> dict[str, Any]:
    params = {
        "ids": "channel==MINE",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": ",".join(metrics),
        "dimensions": "video",
        "sort": "-views",
        "maxResults": 200,
    }
    return analytics.reports().query(**params).execute()

def update_csv_ledger(csv_path: Path, new_yt_records: list[dict[str, Any]]) -> None:
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
    
    # Mapear por Video_ID
    existing_by_id = {r["Video_ID"]: r for r in existing_rows}
    
    for rec in new_yt_records:
        vid_id = rec["Video_ID"]
        existing_by_id[vid_id] = rec
        
    final_rows = list(existing_by_id.values())
    final_rows.sort(key=lambda x: x.get("Fecha", ""), reverse=True)
    
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)
        
    print(f"📊 metrics_video_log.csv actualizado con éxito: {len(final_rows)} registros totales.")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("~/.config/usm-metrics/config.json").expanduser())
    parser.add_argument("--days", type=int, default=30, help="Días hacia atrás para la ventana de análisis")
    args = parser.parse_args()

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=args.days)

    config = load_config(args.config)
    creds = get_credentials(config)
    analytics = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)

    channel = youtube.channels().list(part="id,snippet", mine=True).execute()
    channels = channel.get("items", [])
    if not channels:
        raise RuntimeError("No se encontró canal de YouTube autorizado.")
    channel_record = channels[0]

    print(f"📡 Conectado al canal: {channel_record['snippet']['title']} ({channel_record['id']})")
    print(f"📊 Consultando métricas desde {start_date} hasta {end_date}...")

    performance_payload = query_report(analytics, PERFORMANCE_METRICS, start_date.isoformat(), end_date.isoformat())
    rows = as_rows(performance_payload)

    video_ids = [r["video"] for r in rows if "video" in r]
    video_details = {}
    if video_ids:
        for i in range(0, len(video_ids), 50):
            chunk = video_ids[i:i+50]
            v_resp = youtube.videos().list(part="snippet,contentDetails", id=",".join(chunk)).execute()
            for v in v_resp.get("items", []):
                vid = v["id"]
                snip = v.get("snippet", {})
                cd = v.get("contentDetails", {})
                pub_date = snip.get("publishedAt", "")[:10]
                title = snip.get("title", "Sin título")
                duration_sec = parse_iso_duration(cd.get("duration", ""))
                video_details[vid] = {
                    "title": title,
                    "published_date": pub_date,
                    "duration_sec": duration_sec,
                }

    csv_records = []
    for r in rows:
        vid = r.get("video")
        det = video_details.get(vid, {})
        title = det.get("title", "Sin título")
        r["title"] = title
        
        # Clasificar si es Short (<60 seg) o Video estándar
        dur = det.get("duration_sec", 0)
        plataforma = "YouTube Shorts" if 0 < dur <= 60 else "YouTube"
        
        csv_records.append({
            "Fecha": det.get("published_date", str(end_date)),
            "Plataforma": plataforma,
            "Video_ID": vid,
            "Titulo_Concepto": title,
            "Duracion_Seg": str(dur) if dur > 0 else "",
            "Plays_Views": str(r.get("views", 0)),
            "Watch_Time_Prom_Seg": f"{r.get('averageViewDuration', 0):.1f}" if isinstance(r.get("averageViewDuration"), (int, float)) else str(r.get("averageViewDuration", 0)),
            "Reacciones": str(r.get("likes", 0)),
            "Shares": str(r.get("shares", 0)),
            "Comentarios": str(r.get("comments", 0)),
            "Permalink": f"https://www.youtube.com/watch?v=nb6om1LhOMc" if vid == "nb6om1LhOMc" else f"https://www.youtube.com/shorts/{vid}"
        })

    captured = utc_now()
    evidence = {
        "brand": BRAND,
        "platform": "YouTube",
        "captured_at_utc": captured,
        "channel_id": channel_record.get("id"),
        "channel_title": channel_record.get("snippet", {}).get("title"),
        "window_start": start_date.isoformat(),
        "window_end": end_date.isoformat(),
        "performance_rows": rows,
    }

    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "video"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{captured[:10]}_YouTube_Official_Metrics.json"
    write_private_json(output_file, evidence)

    print(f"✅ Evidencia guardada en: {output_file}")

    # Actualizar CSV unificado de métricas de video
    csv_file = script_dir / "metrics_video_log.csv"
    update_csv_ledger(csv_file, csv_records)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
