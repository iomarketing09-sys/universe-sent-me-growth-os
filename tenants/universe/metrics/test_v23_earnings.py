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
post_id = "1036844829507460_122167031919072582"  # Post de Maeve & Kael ($0.66 USD)

print("\n" + "=" * 65)
print(f"💰 CONSULTANDO GANANCIA NATIVA EN GRAPH API v23.0")
print(f"📌 Post ID: {post_id} (Maeve & Kael - 16 Sep)")
print("=" * 65)

for ver in ["v23.0", "v22.0", "v21.0"]:
    url = f"https://graph.facebook.com/{ver}/{post_id}/insights?metric=content_monetization_earnings&access_token={token}"
    print(f"\n📡 Probando con versión {ver}...")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"✅ Respuesta exitosa ({ver}):")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            break
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"⚠️ Error {e.code} en {ver}: {err[:150]}")
    except Exception as ex:
        print(f"⚠️ Excepción en {ver}: {ex}")

print("\n" + "=" * 65 + "\n")
