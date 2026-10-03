#!/usr/bin/env python3
"""
Universe Sent Me - Growth OS
Captura de métricas E0/E24/E72 vía Meta Graph API.
Ubicación: tenants/universe/metrics/
"""

import os
import sys
import csv
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

METRICS_DIR = Path(__file__).resolve().parent
TENANT_DIR = METRICS_DIR.parent

ENV_PATH = TENANT_DIR / ".env"
CONTEXTS_PATH = TENANT_DIR / "publication_contexts.json"
LOG_PATH = METRICS_DIR / "metrics_snapshot_log.csv"
RAW_DIR = METRICS_DIR / "raw"

def load_env():
    env = {}
    if not ENV_PATH.exists():
        print(f"❌ Error: No se encontró {ENV_PATH}")
        sys.exit(1)
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                clean_k = k.replace("export ", "").strip()
                env[clean_k] = v.strip().strip("'\"")
    return env

def get_snapshot_type(hours_alive):
    if hours_alive < 6:
        return "E0"
    elif 18 <= hours_alive <= 36:
        return "E24"
    elif 60 <= hours_alive <= 84:
        return "E72"
    else:
        return f"E{int(hours_alive)}h"

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    env = load_env()
    page_id = env.get("FB_PAGE_ID")
    token = env.get("PAGE_ACCES_TOKEN") or env.get("PAGE_ACCESS_TOKEN") or env.get("META_ACCESS_TOKEN")

    if not page_id:
        print("❌ Error: Falta FB_PAGE_ID en .env")
        sys.exit(1)
    if not token:
        print("❌ Error: Falta PAGE_ACCES_TOKEN o META_ACCESS_TOKEN en .env")
        sys.exit(1)

    contexts = {}
    if CONTEXTS_PATH.exists():
        try:
            with open(CONTEXTS_PATH, "r", encoding="utf-8") as f:
                contexts = json.load(f)
        except Exception:
            pass

    print(f"📡 Conectando a Meta Graph API para Page ID: {page_id}...")
    url = f"https://graph.facebook.com/v21.0/{page_id}/posts"
    params = {
        "access_token": token,
        "fields": "id,message,created_time,permalink_url,reactions.summary(true),comments.summary(true),shares",
        "limit": 25
    }

    resp = requests.get(url, params=params, timeout=20)
    if resp.status_code != 200:
        print(f"❌ Error de Graph API ({resp.status_code}): {resp.text}")
        sys.exit(1)

    payload = resp.json()
    data = payload.get("data", [])
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # Guardar evidencia JSON cruda fechada
    raw_file = RAW_DIR / f"{now.strftime('%Y-%m-%d_%H%M%S')}_facebook_raw.json"
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    rows_to_save = []
    summary_table = []

    for post in data:
        post_id = post.get("id")
        created_str = post.get("created_time")
        created_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
        hours_alive = round((now - created_dt).total_seconds() / 3600.0, 1)
        snapshot_window = get_snapshot_type(hours_alive)

        reactions = post.get("reactions", {}).get("summary", {}).get("total_count", 0)
        comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)
        shares_data = post.get("shares")
        shares = shares_data.get("count", 0) if isinstance(shares_data, dict) else 0
        total_interactions = reactions + comments + shares

        ctx = contexts.get(post_id, {})
        character = ctx.get("character") or ctx.get("personaje") or "General"
        caption = post.get("message", "").replace("\n", " ")[:38]
        permalink = post.get("permalink_url", "")

        record = {
            "captured_at": now_iso,
            "post_id": post_id,
            "created_time": created_str,
            "hours_alive": hours_alive,
            "snapshot_window": snapshot_window,
            "character": character,
            "reactions": reactions,
            "comments": comments,
            "shares": shares,
            "total_interactions": total_interactions,
            "caption_preview": caption,
            "permalink": permalink
        }
        rows_to_save.append(record)
        summary_table.append(record)

    file_exists = LOG_PATH.exists()
    fields = [
        "captured_at", "post_id", "created_time", "hours_alive", "snapshot_window",
        "character", "reactions", "comments", "shares", "total_interactions",
        "caption_preview", "permalink"
    ]

    with open(LOG_PATH, "a" if file_exists else "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows_to_save)

    summary_table.sort(key=lambda x: x["total_interactions"], reverse=True)
    print("\n" + "=" * 80)
    print(f"📊 CORTE DE MÉTRICAS — {len(summary_table)} POSTS | LOG: metrics/{LOG_PATH.name}")
    print("=" * 80)
    print(f"{'Ventana':<8} {'Horas':<6} {'Personaje':<12} {'Reac':<6} {'Comm':<6} {'Share':<6} {'Total':<6} {'Caption'}")
    print("-" * 80)
    for r in summary_table[:10]:
        print(f"{r['snapshot_window']:<8} {r['hours_alive']:<6.1f} {r['character']:<12} {r['reactions']:<6} {r['comments']:<6} {r['shares']:<6} {r['total_interactions']:<6} {r['caption_preview']}")
    print("=" * 80)
    print(f"✅ Evidencia guardada en: {raw_file.relative_to(TENANT_DIR)}")
    print(f"✅ Snapshot actualizado en: {LOG_PATH.relative_to(TENANT_DIR)}\n")

if __name__ == "__main__":
    main()
