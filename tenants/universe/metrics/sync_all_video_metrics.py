#!/usr/bin/env python3
"""
sync_all_video_metrics.py
Orquestador maestro para sincronizar métricas de video (Meta Reels, YouTube Shorts, TikTok)
y señales de monetización de Meta en Universe Sent Me.
"""
import subprocess
import sys
import csv
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VIDEO_DIR = SCRIPT_DIR / "video"
CSV_PATH = SCRIPT_DIR / "metrics_video_log.csv"
DRIVE_DIR = Path("/home/universe-sent-me/GoogleDrive/Growth OS")

def find_script(keywords):
    """Busca dinámicamente el script en metrics/ y metrics/video/ por palabras clave."""
    for folder in [VIDEO_DIR, SCRIPT_DIR]:
        if not folder.exists():
            continue
        for kw in keywords:
            exact = folder / kw
            if exact.exists():
                return exact
        for p in folder.glob("*.py"):
            if p.name == "sync_all_video_metrics.py":
                continue
            name_lower = p.name.lower()
            if any(kw.lower() in name_lower for kw in keywords):
                return p
    return None

def run_extractor(title, keywords):
    print(f"\n{'='*60}")
    print(f"▶️  Iniciando extracción: {title}")
    print(f"{'='*60}")
    script_path = find_script(keywords)
    if not script_path:
        print(f"⚠️  No se encontró ningún script para {keywords}")
        return False
    
    print(f"🔍 Script detectado: {script_path}")
    try:
        res = subprocess.run([sys.executable, str(script_path)], cwd=str(script_path.parent), check=False)
        return res.returncode == 0
    except Exception as e:
        print(f"❌ Error al ejecutar {script_path.name}: {e}")
        return False

def summarize_and_sync():
    if DRIVE_DIR.exists() and CSV_PATH.exists():
        dest_csv = DRIVE_DIR / "metrics_video_log.csv"
        try:
            shutil.copy2(CSV_PATH, dest_csv)
            print(f"\n☁️  Ledger de video sincronizado con Google Drive: {dest_csv}")
        except Exception as e:
            print(f"⚠️  No se pudo copiar video log a Drive: {e}")

    if not CSV_PATH.exists():
        print("❌ No se encontró metrics_video_log.csv")
        return

    total_videos = 0
    total_views = 0
    total_reactions = 0
    total_shares = 0
    platform_counts = {}

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_videos += 1
            p = row.get("Plataforma", "Desconocida")
            platform_counts[p] = platform_counts.get(p, 0) + 1
            
            views = row.get("Plays_Views", "")
            if views and views.replace(".", "", 1).isdigit():
                total_views += int(float(views))
                
            reac = row.get("Reacciones", "")
            if reac and reac.replace(".", "", 1).isdigit():
                total_reactions += int(float(reac))
                
            shares = row.get("Shares", "")
            if shares and shares.replace(".", "", 1).isdigit():
                total_shares += int(float(shares))

    print(f"\n{'='*60}")
    print("🏆 RESUMEN MAESTRO MULTIPLATAFORMA & MONETIZACIÓN")
    print(f"{'='*60}")
    print(f"Total Videos Consolidados: {total_videos}")
    for plat, count in sorted(platform_counts.items(), key=lambda x: -x[1]):
        print(f"  • {plat}: {count} videos")
    print(f"{'-'*60}")
    print(f"👀 Reproducciones Totales: {total_views:,}")
    print(f"❤️  Reacciones Totales: {total_reactions:,}")
    print(f"🔁 Compartidos Totales: {total_shares:,}")
    print(f"{'='*60}\n")

def main():
    # 1. Meta Reels (Facebook & Instagram)
    run_extractor("Meta Reels (Facebook & Instagram)", ["fetch_reels_insights.py", "reels"])

    # 2. YouTube Shorts
    run_extractor("YouTube Shorts", ["fetch_youtube_metrics.py", "youtube"])

    # 3. TikTok Videos
    run_extractor("TikTok Videos", ["fetch_tiktok_metrics.py", "tiktok"])

    # 4. Meta Creator & Performance Bonus Signals (Nativo)
    run_extractor("Meta Monetization & Creator Signals", ["fetch_meta_monetization.py", "monetization"])

    # 5. Consolidado final y copia a Google Drive
    summarize_and_sync()

if __name__ == "__main__":
    main()
