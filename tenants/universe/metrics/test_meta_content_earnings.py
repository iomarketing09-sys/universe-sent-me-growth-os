#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
from pathlib import Path

ENV_PATH = Path("/home/universe-sent-me/growth-os/tenants/universe/.env")
creds = {}
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip().strip("'\"")

token = creds.get("PAGE_ACCESS_TOKEN")
page_id = creds.get("FB_PAGE_ID", "1036844829507460")

print("\n" + "=" * 65)
print("💰 CONSULTANDO INGRESOS DE CONTENIDO META GRAPH API")
print("=" * 65)

# 1. Consultar a nivel de Página
url_page = f"https://graph.facebook.com/v20.0/{page_id}/insights?metric=content_monetization_earnings&period=days_28&access_token={token}"
try:
    req = urllib.request.Request(url_page)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print("📊 Métrica de Página (content_monetization_earnings):")
        print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"⚠️ Nota en consulta de página: {e}")

# 2. Consultar publicaciones recientes
url_posts = f"https://graph.facebook.com/v20.0/{page_id}/published_posts?fields=id,created_time,message,insights.metric(content_monetization_earnings)&limit=10&access_token={token}"
try:
    req = urllib.request.Request(url_posts)
    with urllib.request.urlopen(req) as resp:
        posts = json.loads(resp.read().decode())
        print("\n🏆 Muestreo de Publicaciones Recientes:")
        for p in posts.get("data", []):
            pid = p.get("id")
            msg = p.get("message", "")[:40].replace("\n", " ")
            insights = p.get("insights", {}).get("data", [])
            earnings = "N/A"
            if insights:
                for item in insights:
                    if item.get("name") == "content_monetization_earnings":
                        earnings = item.get("values", [{}])[0].get("value", 0)
            print(f"• [{p.get('created_time')[:10]}] {pid} | Ganancia: {earnings} | {msg}...")
except Exception as e:
    print(f"❌ Error al consultar posts: {e}")

print("=" * 65 + "\n")
