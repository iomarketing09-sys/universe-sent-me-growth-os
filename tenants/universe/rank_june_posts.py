#!/usr/bin/env python3
"""
Extrae las 100 publicaciones de Junio desde Meta Graph API, las ordena por
impacto real (Reacciones + Shares + Comentarios) y genera el Leaderboard oficial.
"""

import json
from pathlib import Path
import requests

def load_env(env_path: Path) -> dict[str, str]:
    env = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

def main():
    tenant_dir = Path(__file__).resolve().parent
    env = load_env(tenant_dir / ".env")
    
    page_id = env.get("FB_PAGE_ID")
    access_token = env.get("PAGE_ACCESS_TOKEN")
    
    if not page_id or not access_token:
        raise SystemExit("❌ FB_PAGE_ID o PAGE_ACCESS_TOKEN faltan en .env")

    print("📡 Consultando publicaciones de Junio en Meta Graph API...")
    url = f"https://graph.facebook.com/v20.0/{page_id}/published_posts"
    params = {
        "since": "2026-06-01",
        "until": "2026-07-01",
        "fields": "id,created_time,message,reactions.limit(0).summary(true),comments.limit(0).summary(true),shares,permalink_url",
        "limit": 100,
        "access_token": access_token
    }
    
    resp = requests.get(url, params=params, timeout=30)
    if resp.status_code != 200:
        raise SystemExit(f"❌ Error de Meta Graph API: {resp.text}")

    posts = resp.json().get("data", [])
    print(f"📊 Total publicaciones analizadas en Junio: {len(posts)}\n")

    ranked = []
    for p in posts:
        reactions = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
        comments = p.get("comments", {}).get("summary", {}).get("total_count", 0)
        shares = p.get("shares", {}).get("count", 0)
        # Score ponderado: shares valen más por viralidad
        score = reactions + (comments * 2) + (shares * 3)
        
        ranked.append({
            "id": p.get("id"),
            "date": p.get("created_time", "")[:10],
            "time": p.get("created_time", "")[11:16],
            "reactions": reactions,
            "comments": comments,
            "shares": shares,
            "score": score,
            "message": (p.get("message") or "Sin caption").replace("\n", " ")[:35],
            "permalink": p.get("permalink_url", f"https://facebook.com/{p.get('id')}")
        })

    # Ordenar por impacto de mayor a menor
    ranked.sort(key=lambda x: x["score"], reverse=True)

    print(f"{'#':<3} | {'Fecha':<10} | {'Hora':<5} | {'Likes':<6} | {'Shares':<6} | {'Comms':<6} | {'Copy / Caption':<35} | {'Enlace Post'}")
    print("-" * 115)
    for i, p in enumerate(ranked[:20], 1):
        print(f"{i:<3} | {p['date']:<10} | {p['time']:<5} | {p['reactions']:<6} | {p['shares']:<6} | {p['comments']:<6} | {p['message']:<35} | {p['permalink']}")

    print("-" * 115)
    print(f"Total evaluadas: {len(ranked)} publicaciones.")

if __name__ == "__main__":
    main()
