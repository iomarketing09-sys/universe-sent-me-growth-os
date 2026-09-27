#!/usr/bin/env python3
"""
Extractor automatizado de telemetría para Bam in a Can (Tenant #3).
Consulta nativamente YouTube Shorts, TikTok e Instagram Reels.
"""

import os
import sys
import re
import csv
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

LEDGER_PATH = os.path.join(os.path.dirname(__file__), "distribution_ledger.csv")
if not os.path.exists(LEDGER_PATH):
    LEDGER_PATH = os.path.join(os.path.dirname(__file__), "../distribution_ledger.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_youtube_metrics(video_id):
    """Extrae views y likes de YouTube Shorts por ID."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            views_match = re.search(r'"viewCount":\s*"(\d+)"', html)
            views = int(views_match.group(1)) if views_match else 0
            likes_match = re.search(r'"label":\s*"([\d,]+)\s+likes"', html, re.IGNORECASE)
            likes = int(likes_match.group(1).replace(",", "")) if likes_match else 0
            return {"views": views, "likes": likes, "status": "ok"}
    except Exception as e:
        return {"views": 0, "likes": 0, "status": f"error: {e}"}

def fetch_tiktok_metrics(video_id, handle="bam_in_a_can"):
    """Extrae playCount, diggCount, shares y comments de TikTok nativo."""
    url = f"https://www.tiktok.com/@{handle}/video/{video_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Buscar contadores en script JSON hidratado (__UNIVERSAL_DATA_FOR_REHYDRATION__ o SIGI_STATE)
            play_match = re.search(r'"playCount":\s*(\d+)', html)
            digg_match = re.search(r'"diggCount":\s*(\d+)', html)
            share_match = re.search(r'"shareCount":\s*(\d+)', html)
            comment_match = re.search(r'"commentCount":\s*(\d+)', html)

            views = int(play_match.group(1)) if play_match else 0
            likes = int(digg_match.group(1)) if digg_match else 0
            shares = int(share_match.group(1)) if share_match else 0
            comments = int(comment_match.group(1)) if comment_match else 0

            return {
                "views": views,
                "likes": likes,
                "shares": shares,
                "comments": comments,
                "status": "ok" if views > 0 else "active_pending_count"
            }
    except Exception as e:
        return {"views": 0, "likes": 0, "shares": 0, "comments": 0, "status": f"error: {e}"}

def run_telemetry(dry_run=True):
    mode_str = "DRY RUN (Solo lectura)" if dry_run else "LIVE (Actualizando ledger)"
    print("=" * 65)
    print(f"BAM IN A CAN — Telemetría Nativa Multiplataforma [{mode_str}]")
    print("=" * 65)

    if not os.path.exists(LEDGER_PATH):
        print(f"Error: Ledger no encontrado en {LEDGER_PATH}")
        return

    with open(LEDGER_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_views = 0

    for row in rows:
        cid = row.get("Content_ID")
        platform = row.get("Platform")
        nid = row.get("Native_Post_ID")
        if not nid:
            continue

        res = {"views": 0, "likes": 0, "status": "skipped"}
        if "YouTube" in platform:
            res = fetch_youtube_metrics(nid)
        elif "TikTok" in platform:
            res = fetch_tiktok_metrics(nid)

        v = res.get("views", 0)
        total_views += v
        print(f"[{cid}] {platform:<16} | Views: {v:<6} | Likes: {res.get('likes', 0):<4} | Status: {res.get('status')}")

    print("-" * 65)
    print(f"TOTAL REPRODUCCIONES AUDITADAS: {total_views:,} views")
    cpm_estimate = (total_views / 1000) * 1.50
    print(f"ESTIMADO CONTENT REWARDS (~$1.50 RPM): ${cpm_estimate:.2f} USD")
    print("=" * 65)

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    run_telemetry(dry_run=not is_live)
