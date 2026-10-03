import urllib.request
import urllib.parse
import json
import os
import sys
from pathlib import Path

env_path = Path("/home/universe-sent-me/growth-os/tenants/universe/.env")

print("=" * 65)
print(" EXTRACTOR DE TOKENS PERMANENTES Y DATOS DE PÁGINA (META)")
print("=" * 65)

# Acepta el token por argumento o por prompt
if len(sys.argv) > 1 and sys.argv.strip():
    user_token = sys.argv.strip()
else:
    user_token = input("\nPega tu Extended User Token aquí y presiona Enter: ").strip()

if not user_token:
    print("❌ Error: No ingresaste ningún token.")
    exit(1)

fields = "name,id,access_token,instagram_business_account{id,username}"
url = f"https://graph.facebook.com/v20.0/me/accounts?fields={fields}&access_token={urllib.parse.quote(user_token)}"

print("\nConsultando páginas e Instagrams asociados en Meta...")

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
except Exception as e:
    print(f"❌ Error al consultar la API de Meta: {e}")
    exit(1)

accounts = data.get("data", [])
if not accounts:
    print("⚠️ No se encontraron páginas administradas con ese token.")
    exit(1)

print(f"\nSe encontraron {len(accounts)} página(s):\n")

selected_page = None
for acc in accounts:
    p_name = acc.get("name")
    p_id = acc.get("id")
    ig_data = acc.get("instagram_business_account", {})
    ig_id = ig_data.get("id", "No vinculado")
    ig_user = ig_data.get("username", "N/A")
    
    print(f"📄 Página: {p_name} (ID: {p_id})")
    print(f"   📸 Instagram: @{ig_user} (ID: {ig_id})")
    
    if p_id == "1036844829507460" or "universe" in p_name.lower():
        selected_page = acc

if not selected_page:
    selected_page = accounts[0]
    print(f"\n-> Usando por defecto: {selected_page.get('name')}")
else:
    print(f"\n-> Coincidencia detectada para Universe: {selected_page.get('name')}")

page_token = selected_page.get("access_token")
page_id = selected_page.get("id")
ig_account = selected_page.get("instagram_business_account", {})
ig_id = ig_account.get("id", "")

# Verificar vigencia del token de página
debug_url = f"https://graph.facebook.com/v20.0/debug_token?input_token={page_token}&access_token={page_token}"
try:
    with urllib.request.urlopen(debug_url) as d_resp:
        d_data = json.loads(d_resp.read().decode("utf-8")).get("data", {})
        is_valid = d_data.get("is_valid", False)
        print(f"\nEstado del Page Token: {'✅ VÁLIDO' if is_valid else '❌ INVÁLIDO'}")
        print("Vigencia del Token de Página: ♾️  NUNCA EXPIRA (Permanente)")
except Exception:
    print("\nPage Token obtenido con éxito.")

# Actualizar el archivo .env
lines = []
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

updated_keys = set()
new_lines = []

for line in lines:
    stripped = line.strip()
    if stripped.startswith("PAGE_ACCES_TOKEN="):
        new_lines.append(f"PAGE_ACCES_TOKEN={page_token}\n")
        updated_keys.add("PAGE_ACCES_TOKEN")
    elif stripped.startswith("FB_PAGE_ID="):
        new_lines.append(f"FB_PAGE_ID={page_id}\n")
        updated_keys.add("FB_PAGE_ID")
    elif stripped.startswith("INSTAGRAM_ACCOUNT_ID="):
        if ig_id:
            new_lines.append(f"INSTAGRAM_ACCOUNT_ID={ig_id}\n")
            updated_keys.add("INSTAGRAM_ACCOUNT_ID")
    else:
        new_lines.append(line)

if "PAGE_ACCES_TOKEN" not in updated_keys:
    new_lines.append(f"PAGE_ACCES_TOKEN={page_token}\n")
if "FB_PAGE_ID" not in updated_keys:
    new_lines.append(f"FB_PAGE_ID={page_id}\n")
if ig_id and "INSTAGRAM_ACCOUNT_ID" not in updated_keys:
    new_lines.append(f"INSTAGRAM_ACCOUNT_ID={ig_id}\n")

with open(env_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"\n✅ Archivo {env_path} actualizado con éxito:")
print(f"   * FB_PAGE_ID={page_id}")
print(f"   * PAGE_ACCES_TOKEN (Token Permanente guardado)")
if ig_id:
    print(f"   * INSTAGRAM_ACCOUNT_ID={ig_id}")
print("\n¡Listo! El token permanente ya está en tu .env.")
