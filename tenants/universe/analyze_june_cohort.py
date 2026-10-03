#!/usr/bin/env python3
"""
Analizador de rendimiento histórico para la cohorte de Junio.
Consulta Meta Graph API y cruza con Content_Inventory.csv para clasificar los assets en Tiers.
"""

from __future__ import annotations
import csv
import json
import os
import re
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

def normalize_name(name: str) -> str:
    base = Path(name).stem.strip().lower()
    match = re.search(r'\b(260\d{3,4}|humor[\d\.]+)\b', base)
    return match.group(1) if match else base

def main():
    tenant_dir = Path(__file__).resolve().parent
    growth_root = Path("/home/universe-sent-me/growth-os")
    env = load_env(tenant_dir / ".env")
    
    page_id = env.get("FB_PAGE_ID")
    access_token = env.get("PAGE_ACCESS_TOKEN")
    
    if not page_id or not access_token:
        raise SystemExit("❌ FB_PAGE_ID o PAGE_ACCESS_TOKEN no encontrados en tenants/universe/.env")

    assets_june = Path("/home/universe-sent-me/GoogleDrive/Universe sent me/USM/Humor existencial/06 Junio")
    if not assets_june.exists():
        assets_june = Path.home() / "GoogleDrive" / "Universe sent me" / "USM" / "Humor existencial" / "06 Junio"

    local_assets = [f.name for f in assets_june.iterdir() if f.is_file() and f.suffix.lower() in [".png", ".jpeg", ".jpg"]]
    print(f"📁 Assets actuales en la raíz de '06 Junio/': {len(local_assets)}")

    # 1. Mapear Post IDs desde Content_Inventory.csv
    inventory_file = growth_root / "accounts" / "universe_sent_me" / "data" / "Content_Inventory.csv"
    asset_to_post = {}
    
    if inventory_file.exists():
        with inventory_file.open(encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                # Buscar post_id (formato tipo 1036844829507460_...)
                pid = next((c.strip() for c in row if re.search(r'^\d+_\d+$', c.strip())), None)
                if pid:
                    for col in row:
                        if any(ext in col.lower() for ext in [".png", ".jpeg", ".jpg"]):
                            asset_to_post[Path(col.strip()).name] = pid
                            asset_to_post[normalize_name(col.strip())] = pid

    print(f"🔗 Mapeo de inventario: {len(asset_to_post)} referencias vinculadas con Meta Post IDs.")
    print("📡 Consultando publicaciones históricas de Junio en Meta Graph API...")

    # 2. Consultar feed de Facebook de junio
    url = f"https://graph.facebook.com/v20.0/{page_id}/published_posts"
    params = {
        "since": "2026-06-01",
        "until": "2026-07-01",
        "fields": "id,created_time,message,reactions.limit(0).summary(true),comments.limit(0).summary(true),shares",
        "limit": 100,
        "access_token": access_token
    }
    
    resp = requests.get(url, params=params, timeout=30)
    if resp.status_code != 200:
        raise SystemExit(f"❌ Error consultando Meta Graph API: {resp.text}")

    posts_data = resp.json().get("data", [])
    print(f"📊 Publicaciones encontradas en Meta de Junio: {len(posts_data)}\n")

    posts_by_id = {}
    for p in posts_data:
        pid = p.get("id")
        reactions = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
        comments = p.get("comments", {}).get("summary", {}).get("total_count", 0)
        shares = p.get("shares", {}).get("count", 0)
        score = reactions + (comments * 2) + (shares * 3)
        posts_by_id[pid] = {
            "date": p.get("created_time", "")[:10],
            "reactions": reactions,
            "comments": comments,
            "shares": shares,
            "score": score,
            "message": (p.get("message") or "")[:40]
        }

    # 3. Cruzar métricas con los assets de junio
    results = []
    for asset in sorted(local_assets):
        norm = normalize_name(asset)
        post_id = asset_to_post.get(asset) or asset_to_post.get(norm)
        metrics = posts_by_id.get(post_id) if post_id else None
        
        if metrics:
            results.append({
                "asset": asset,
                "date": metrics["date"],
                "reactions": metrics["reactions"],
                "comments": metrics["comments"],
                "shares": metrics["shares"],
                "score": metrics["score"],
                "status": "Con métricas oficiales"
            })
        else:
            results.append({
                "asset": asset,
                "date": "2026-06-XX",
                "reactions": 0,
                "comments": 0,
                "shares": 0,
                "score": 0,
                "status": "Pendiente de mapeo"
            })

    # Ordenar de mayor a menor score
    results.sort(key=lambda x: x["score"], reverse=True)

    # Clasificar en Tiers
    scored = [r for r in results if r["score"] > 0]
    t1_cutoff = len(scored) // 4 if scored else 0

    print(f"{'#':<3} | {'Asset':<40} | {'Fecha':<10} | {'Likes':<6} | {'Comms':<6} | {'Shares':<6} | {'Tier'}")
    print("-" * 88)
    for i, r in enumerate(results, 1):
        if r["score"] > 0:
            tier = "Tier 1 (Top 🔥)" if i <= max(5, t1_cutoff) else "Tier 2 (Sólido 👍)"
        else:
            tier = "Tier 3 / Sin datos"
        print(f"{i:<3} | {r['asset'][:40]:<40} | {r['date']:<10} | {r['reactions']:<6} | {r['comments']:<6} | {r['shares']:<6} | {tier}")

    print("-" * 88)
    t1_assets = [r['asset'] for i, r in enumerate(results, 1) if r["score"] > 0 and i <= max(5, t1_cutoff)]
    if t1_assets:
        print(f"\n🏆 Piezas clasificadas como Tier 1 ({len(t1_assets)}):")
        for a in t1_assets:
            print(f"• {a}")
        print("\n¿Deseas que movamos estas piezas Tier 1 a '06 Junio/Top/' para priorizarlas en las parrilladas?")

if __name__ == "__main__":
    main()
