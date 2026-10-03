#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
from pathlib import Path
from datetime import datetime

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
print("🔍 DIAGNÓSTICO DE MONETIZACIÓN: SEMANA 6 AL 16 DE SEPTIEMBRE")
print("=" * 65)

# Traer publicaciones de la ventana de mayores ingresos (6 al 16 de septiembre)
since_ts = int(datetime(2026, 9, 5).timestamp())
until_ts = int(datetime(2026, 9, 17).timestamp())

url_posts = (
    f"https://graph.facebook.com/v20.0/{page_id}/published_posts?"
    f"fields=id,created_time,message,shares,reactions.summary(true),comments.summary(true)"
    f"&since={since_ts}&until={until_ts}&limit=25&access_token={token}"
)

try:
    req = urllib.request.Request(url_posts)
    with urllib.request.urlopen(req) as resp:
        posts = json.loads(resp.read().decode()).get("data", [])
        print(f"📦 Publicaciones encontradas en esa ventana: {len(posts)}\n")

        for p in posts[:8]:
            pid = p.get("id")
            created = p.get("created_time")[:16].replace("T", " ")
            msg = p.get("message", "Sin texto")[:45].replace("\n", " ")
            reac = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
            comm = p.get("comments", {}).get("summary", {}).get("total_count", 0)
            shares = p.get("shares", {}).get("count", 0)

            # Probar extracción de insights del post
            url_ins = f"https://graph.facebook.com/v20.0/{pid}/insights?metric=post_impressions_unique,post_engaged_users,content_monetization_earnings&access_token={token}"
            ins_data = {}
            try:
                r_ins = urllib.request.Request(url_ins)
                with urllib.request.urlopen(r_ins) as r_resp:
                    ins_data = json.loads(r_resp.read().decode())
            except urllib.error.HTTPError as he:
                try:
                    ins_data = json.loads(he.read().decode())
                except Exception:
                    ins_data = {"error": str(he)}
            except Exception as ex:
                ins_data = {"error": str(ex)}

            print(f"📌 [{created}] ID: {pid}")
            print(f"   Copy: {msg}...")
            print(f"   Interacciones: 👍 {reac} | 💬 {comm} | 🔁 {shares}")
            
            # Revisar qué respondió la API de Insights
            if "error" in ins_data:
                err_msg = ins_data.get("error", {}).get("message", ins_data.get("error"))
                print(f"   ⚠️ Respuesta Insights: {err_msg}")
            else:
                metrics_found = [m.get("name") for m in ins_data.get("data", [])]
                print(f"   ✅ Métricas devueltas: {metrics_found}")
                for m in ins_data.get("data", []):
                    if m.get("name") == "content_monetization_earnings":
                        print(f"   💰 GANANCIA REGISTRADA: {m.get('values')}")
            print("-" * 65)

except Exception as e:
    print(f"❌ Error general: {e}")

print("=" * 65 + "\n")
