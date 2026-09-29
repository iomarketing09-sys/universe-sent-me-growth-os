#!/usr/bin/env python3
"""
audit_historical_content.py — Auditoría Profunda de Contenido (Últimos 90 días)
Extrae y rankea las publicaciones de Facebook e Instagram de Mica's Art & Deco
para identificar arquetipos ganadores, formatos con mayor retención y outliers.
"""

from __future__ import annotations
import os
import sys
import json
import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path
import requests

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
METRICS_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = METRICS_DIR / "historical_top_posts.csv"

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

def audit_facebook(page_id: str, token: str, since_ts: int) -> list[dict]:
    print("[*] Consultando historial de Facebook (últimos 90 días)...")
    posts = []
    url = f"https://graph.facebook.com/v20.0/{page_id}/posts"
    params = {
        "fields": "id,created_time,message,shares,reactions.summary(total_count),comments.summary(total_count),attachments{media_type,type,title}",
        "access_token": token,
        "since": str(since_ts),
        "limit": 100
    }

    while url:
        res = requests.get(url, params=params, timeout=25).json()
        if "error" in res:
            print(f"[-] Error en Facebook API: {res['error'].get('message')}")
            break
        
        batch = res.get("data", [])
        for p in batch:
            reactions = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
            comments = p.get("comments", {}).get("summary", {}).get("total_count", 0)
            shares = p.get("shares", {}).get("count", 0)
            score = reactions + (comments * 2) + (shares * 3)
            
            att = p.get("attachments", {}).get("data", [{}])[0]
            m_type = att.get("media_type") or att.get("type") or "status"

            posts.append({
                "platform": "Facebook",
                "id": p.get("id"),
                "created_time": p.get("created_time"),
                "message": (p.get("message") or "").replace("\n", " ")[:120],
                "reactions": reactions,
                "comments": comments,
                "shares": shares,
                "score": score,
                "media_type": m_type
            })

        url = res.get("paging", {}).get("next")
        params = {}

    return posts

def audit_instagram(ig_id: str, token: str, since_ts: int) -> list[dict]:
    if not ig_id:
        return []
    print("[*] Consultando historial de Instagram Business (últimos 90 días)...")
    posts = []
    url = f"https://graph.facebook.com/v20.0/{ig_id}/media"
    params = {
        "fields": "id,caption,media_type,media_product_type,timestamp,like_count,comments_count,permalink",
        "access_token": token,
        "since": str(since_ts),
        "limit": 100
    }

    while url:
        res = requests.get(url, params=params, timeout=25).json()
        if "error" in res:
            print(f"[-] Error en Instagram API: {res['error'].get('message')}")
            break

        batch = res.get("data", [])
        for p in batch:
            likes = p.get("like_count", 0)
            comments = p.get("comments_count", 0)
            score = likes + (comments * 2)

            posts.append({
                "platform": "Instagram",
                "id": p.get("id"),
                "created_time": p.get("timestamp"),
                "message": (p.get("caption") or "").replace("\n", " ")[:120],
                "reactions": likes,
                "comments": comments,
                "shares": 0,
                "score": score,
                "media_type": p.get("media_type") or p.get("media_product_type", "POST")
            })

        url = res.get("paging", {}).get("next")
        params = {}

    return posts

def main():
    env = load_env()
    token = env.get("PAGE_ACCESS_TOKEN")
    page_id = env.get("FB_PAGE_ID")
    ig_id = env.get("IG_USER_ID")

    if not token or not page_id:
        print("[-] Error: Faltan credenciales en tenants/micas-art-deco/.env")
        sys.exit(1)

    now = datetime.now(timezone.utc)
    since_dt = now - timedelta(days=90)
    since_ts = int(since_dt.timestamp())

    print("=" * 70)
    print(" MICA'S ART & DECO — AUDITORÍA PROFUNDA DE RENDIMIENTO (90 DÍAS)")
    print(f" Ventana de Análisis : {since_dt.strftime('%Y-%m-%d')} a {now.strftime('%Y-%m-%d')}")
    print("=" * 70)

    fb_posts = audit_facebook(page_id, token, since_ts)
    ig_posts = audit_instagram(ig_id, token, since_ts)

    all_posts = fb_posts + ig_posts

    fb_sorted = sorted(fb_posts, key=lambda x: x["score"], reverse=True)
    ig_sorted = sorted(ig_posts, key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 70)
    print(f" RESUMEN EJECUTIVO DE PUBLICACIONES AUDITADAS (Total: {len(all_posts)})")
    print(f" • Facebook  : {len(fb_posts)} posts encontrados en 90 días")
    print(f" • Instagram : {len(ig_posts)} posts encontrados en 90 días")
    print("=" * 70)

    print("\n🏆 TOP 5 PUBLICACIONES CON MAYOR ENGAGEMENT EN FACEBOOK:")
    print("-" * 70)
    for i, p in enumerate(fb_sorted[:5], 1):
        dt = p["created_time"][:10] if p["created_time"] else "N/A"
        print(f"#{i} [{dt}] Tipo: {p['media_type'].upper()} | Score Ponderado: {p['score']}")
        print(f"   Reacciones: {p['reactions']} | Comentarios: {p['comments']} | Shares: {p['shares']}")
        print(f"   Texto: \"{p['message']}...\"")
        print("-" * 70)

    if ig_sorted:
        print("\n📸 TOP 5 PUBLICACIONES CON MAYOR ENGAGEMENT EN INSTAGRAM:")
        print("-" * 70)
        for i, p in enumerate(ig_sorted[:5], 1):
            dt = p["created_time"][:10] if p["created_time"] else "N/A"
            print(f"#{i} [{dt}] Tipo: {p['media_type'].upper()} | Score Ponderado: {p['score']}")
            print(f"   Likes: {p['reactions']} | Comentarios: {p['comments']}")
            print(f"   Texto: \"{p['message']}...\"")
            print("-" * 70)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["platform", "id", "created_time", "media_type", "reactions", "comments", "shares", "score", "message"])
        writer.writeheader()
        writer.writerows(fb_sorted + ig_sorted)

    print(f"\n[+] Datos consolidados guardados en: {OUTPUT_CSV.name}")

if __name__ == "__main__":
    main()
