#!/usr/bin/env python3
"""
capture_micas_metrics.py — Telemetría multicanal de Mica's Art & Deco
Extrae señales nativas de Facebook Page e Instagram Business y guarda snapshot en CSV.
"""

from __future__ import annotations
import os
import sys
import json
import csv
from datetime import datetime, timezone
from pathlib import Path
import requests

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
METRICS_DIR = Path(__file__).resolve().parent
LOG_CSV = METRICS_DIR / "micas_metrics_log.csv"

def load_env() -> dict[str, str]:
    env = {}
    if ENV_PATH.exists():
        for line in open(ENV_PATH):
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    return env

def capture():
    env = load_env()
    token = env.get("PAGE_ACCESS_TOKEN")
    page_id = env.get("FB_PAGE_ID")
    ig_id = env.get("IG_USER_ID")

    if not token or not page_id:
        print("[-] Error: Faltan credenciales en tenants/micas-art-deco/.env")
        print("    Ejecuta primero: python3 tools/get_micas_tokens.py")
        sys.exit(1)

    now_iso = datetime.now(timezone.utc).isoformat()
    print("=" * 65)
    print(" MICA'S ART & DECO — CAPTURA DE TELEMETRÍA CGO (META GRAPH API)")
    print(f" Timestamp : {now_iso}")
    print(f" Page ID   : {page_id}")
    print("=" * 65)

    fb_url = f"https://graph.facebook.com/v20.0/{page_id}"
    fb_params = {
        "fields": "name,followers_count,fan_count,posts.limit(5){id,created_time,message,shares,reactions.summary(total_count),comments.summary(total_count)}",
        "access_token": token
    }
    
    fb_data = requests.get(fb_url, params=fb_params, timeout=20).json()
    if "error" in fb_data:
        print(f"[-] Error en Facebook: {fb_data['error'].get('message')}")
        return False

    followers = fb_data.get("followers_count", 0)
    fans = fb_data.get("fan_count", 0)
    print(f"[FB] Página: {fb_data.get('name')}")
    print(f"     Seguidores : {followers} | Me gusta: {fans}")

    recent_posts = fb_data.get("posts", {}).get("data", [])
    total_fb_reactions = 0
    total_fb_shares = 0
    total_fb_comments = 0

    for p in recent_posts:
        reactions = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
        comments = p.get("comments", {}).get("summary", {}).get("total_count", 0)
        shares = p.get("shares", {}).get("count", 0)
        total_fb_reactions += reactions
        total_fb_shares += shares
        total_fb_comments += comments

    print(f"     Interacciones (últimos {len(recent_posts)} posts): {total_fb_reactions} reactions | {total_fb_shares} shares | {total_fb_comments} comments")

    ig_followers = 0
    ig_media_count = 0
    if ig_id:
        ig_url = f"https://graph.facebook.com/v20.0/{ig_id}"
        ig_params = {
            "fields": "name,username,followers_count,media_count,media.limit(5){id,caption,media_type,like_count,comments_count}",
            "access_token": token
        }
        ig_data = requests.get(ig_url, params=ig_params, timeout=20).json()
        if "error" not in ig_data:
            ig_followers = ig_data.get("followers_count", 0)
            ig_media_count = ig_data.get("media_count", 0)
            print(f"[IG] Perfil: @{ig_data.get('username')} ({ig_data.get('name')})")
            print(f"     Seguidores : {ig_followers} | Publicaciones: {ig_media_count}")

    file_exists = LOG_CSV.exists()
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Timestamp_UTC", "FB_Followers", "FB_Fans", 
                "FB_Recent_Reactions", "FB_Recent_Shares", "FB_Recent_Comments",
                "IG_Followers", "IG_Media_Count"
            ])
        writer.writerow([
            now_iso, followers, fans,
            total_fb_reactions, total_fb_shares, total_fb_comments,
            ig_followers, ig_media_count
        ])

    print(f"\n[+] Snapshot de métricas registrado en {LOG_CSV.name}")
    return True

if __name__ == "__main__":
    capture()
