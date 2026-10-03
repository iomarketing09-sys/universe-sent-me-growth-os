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
print("💰 CONSULTANDO INGRESOS DE CONTENIDO A NIVEL PÁGINA (LAST_28D)")
print("=" * 65)

# 1. Probar content_monetization_earnings a nivel de Página con date_preset
urls = [
    ("content_monetization_earnings (last_28d)", f"https://graph.facebook.com/v23.0/{page_id}/insights?metric=content_monetization_earnings&date_preset=last_28d&access_token={token}"),
    ("content_monetization_earnings (period=days_28)", f"https://graph.facebook.com/v23.0/{page_id}/insights?metric=content_monetization_earnings&period=days_28&access_token={token}"),
    ("monetization_approximate_earnings", f"https://graph.facebook.com/v23.0/{page_id}/insights?metric=monetization_approximate_earnings&date_preset=last_28d&access_token={token}")
]

for label, url in urls:
    print(f"\n📡 Probando: {label}...")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("✅ Respuesta:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:600])
    except urllib.error.HTTPError as e:
        print(f"⚠️ HTTPError {e.code}: {e.read().decode()[:200]}")
    except Exception as ex:
        print(f"⚠️ Error: {ex}")

print("\n" + "=" * 65 + "\n")
