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
print("💰 PROBANDO ENDPOINT NATIVO CREATOR MONETIZATION")
print("=" * 65)

# Probar GET y POST sobre monetization_approximate_earnings
endpoints = [
    ("GET /monetization_approximate_earnings", "GET", f"https://graph.facebook.com/v23.0/{page_id}/monetization_approximate_earnings?access_token={token}"),
    ("POST /monetization_approximate_earnings", "POST", f"https://graph.facebook.com/v23.0/{page_id}/monetization_approximate_earnings?access_token={token}")
]

for label, method, url in endpoints:
    print(f"\n📡 Probando {label}...")
    try:
        req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"✅ Respuesta exitosa:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:800])
    except urllib.error.HTTPError as e:
        print(f"⚠️ HTTPError {e.code}: {e.read().decode()[:250]}")
    except Exception as ex:
        print(f"⚠️ Error: {ex}")

print("\n" + "=" * 65 + "\n")
