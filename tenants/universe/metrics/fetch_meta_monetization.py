#!/usr/bin/env python3
"""
fetch_meta_monetization.py
Extractor de señales de monetización y payouts de Meta para Universe Sent Me.
Aprovecha el token de Meta con scope business_management.
"""
import os
import json
import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.parse
import urllib.error

SCRIPT_DIR = Path(__file__).resolve().parent
TENANT_DIR = SCRIPT_DIR.parent
ENV_PATH = TENANT_DIR / ".env"
OUTPUT_DIR = SCRIPT_DIR / "monetization"
CSV_LOG = SCRIPT_DIR / "meta_monetization_log.csv"
DRIVE_DIR = Path("/home/universe-sent-me/GoogleDrive/Growth OS")

def load_env():
    creds = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    creds[k.strip()] = v.strip().strip("'\"")
    return creds

def api_get(endpoint, params):
    base_url = "https://graph.facebook.com/v20.0"
    url = f"{base_url}/{endpoint}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return json.loads(err_body)
        except Exception:
            return {"error": {"message": err_body, "code": e.code}}
    except Exception as e:
        return {"error": {"message": str(e)}}

def main():
    print("\n" + "=" * 60)
    print("💰 EXTRACTOR DE MONETIZACIÓN Y SEÑALES META")
    print("=" * 60)

    creds = load_env()
    token = creds.get("PAGE_ACCESS_TOKEN")
    page_id = creds.get("FB_PAGE_ID", "1036844829507460")

    if not token:
        print("❌ Error: No se encontró PAGE_ACCESS_TOKEN en .env")
        return 1

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Consultar información de la Página y Business Manager
    print(f"📡 Consultando Página ID: {page_id} y Business Manager...")
    page_info = api_get(page_id, {
        "fields": "id,name,business,is_eligible_for_branded_content",
        "access_token": token
    })

    business_data = page_info.get("business", {})
    business_id = creds.get("UNIVERSE_ACCOUNT_ID", "2294927867461766")
    business_name = business_data.get("name", "N/A")
    print(f"🏢 Business Manager: {business_name} (ID: {business_id})")

    # 2. Consultar publicaciones recientes para señales de Bonus y Clics
    print("📊 Analizando publicaciones para cálculo de Performance Bonus...")
    posts_data = api_get(f"{page_id}/published_posts", {
        "fields": "id,created_time,message,shares,reactions.summary(true),comments.summary(true)",
        "limit": 30,
        "access_token": token
    })

    posts = posts_data.get("data", [])
    total_bonus_interactions = 0
    total_shares = 0
    total_reactions = 0
    total_comments = 0
    processed_posts = []

    for p in posts:
        pid = p.get("id")
        created = p.get("created_time", "")[:10]
        msg = p.get("message", "")[:40].replace("\n", " ")
        reactions = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
        comments = p.get("comments", {}).get("summary", {}).get("total_count", 0)
        shares = p.get("shares", {}).get("count", 0)
        
        # Interacciones que componen el Performance Bonus
        bonus_points = reactions + (comments * 2) + (shares * 3)
        total_bonus_interactions += (reactions + comments + shares)
        total_reactions += reactions
        total_comments += comments
        total_shares += shares

        processed_posts.append({
            "post_id": pid,
            "date": created,
            "preview": msg,
            "reactions": reactions,
            "comments": comments,
            "shares": shares,
            "bonus_points": bonus_points
        })

    print(f"✅ {len(posts)} publicaciones analizadas.")
    print(f"   • Reacciones totales: {total_reactions:,}")
    print(f"   • Comentarios totales: {total_comments:,}")
    print(f"   • Compartidos totales: {total_shares:,}")
    print(f"   • Interacciones elegibles para Bonus: {total_bonus_interactions:,}")

    # 3. Guardar evidencia JSON
    evidence = {
        "date": today,
        "page_id": page_id,
        "business_id": business_id,
        "total_posts_analyzed": len(posts),
        "total_bonus_interactions": total_bonus_interactions,
        "metrics": {
            "reactions": total_reactions,
            "comments": total_comments,
            "shares": total_shares
        },
        "posts": processed_posts
    }

    evidence_file = OUTPUT_DIR / f"{today}_Meta_Monetization_Signals.json"
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)
    print(f"💾 Evidencia guardada en: {evidence_file}")

    # 4. Actualizar Ledger CSV de Monetización
    csv_exists = CSV_LOG.exists()
    with open(CSV_LOG, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not csv_exists:
            writer.writerow(["Fecha", "Plataforma", "Business_ID", "Posts_Analizados", "Reacciones", "Comentarios", "Shares", "Interacciones_Bonus_Elegibles"])
        writer.writerow([today, "Facebook Page", business_id, len(posts), total_reactions, total_comments, total_shares, total_bonus_interactions])

    print(f"📊 Ledger local actualizado: {CSV_LOG}")

    # 5. Respaldar a Google Drive
    if DRIVE_DIR.exists():
        try:
            shutil.copy2(CSV_LOG, DRIVE_DIR / "meta_monetization_log.csv")
            print(f"☁️  Ledger respaldado en Drive: {DRIVE_DIR / 'meta_monetization_log.csv'}")
        except Exception as e:
            print(f"⚠️  No se pudo copiar a Drive: {e}")

    print("=" * 60 + "\n")
    return 0

if __name__ == "__main__":
    main()
