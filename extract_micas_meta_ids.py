#!/usr/bin/env python3
"""
Extractor de IDs y Page Access Token de Meta para Mica's Art & Deco.
"""
import os
import sys
import argparse
from pathlib import Path
import requests

GRAPH_API_VERSION = "v21.0"
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def main():
    parser = argparse.ArgumentParser(description="Extraer IDs de FB e IG para Mica's Art & Deco")
    parser.add_argument(
        "--token",
        help="Meta User Access Token",
        default=os.environ.get("USM_META_USER_ACCESS_TOKEN")
    )
    parser.add_argument(
        "--save-env",
        action="store_true",
        help="Guarda el archivo .env en ~/growth-os/tenants/micas-art-deco/.env"
    )
    args = parser.parse_args()

    token = args.token
    if not token:
        print("❌ Error: No se proporcionó ningún token.")
        print("Usa: python3 extract_micas_meta_ids.py --token 'TU_TOKEN' --save-env")
        sys.exit(1)

    print("🔍 Consultando cuentas y páginas vinculadas en Meta Graph API...")
    url = f"{GRAPH_BASE_URL}/me/accounts"
    params = {
        "fields": "id,name,access_token,instagram_business_account{id,username}",
        "limit": 100,
        "access_token": token
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        data = response.json()
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        sys.exit(1)

    if "error" in data:
        err = data["error"]
        print(f"❌ Error de Meta API [{err.get('code')}]: {err.get('message')}")
        sys.exit(1)

    pages = data.get("data", [])
    if not pages:
        print("⚠️ No se encontraron páginas asociadas a este token.")
        sys.exit(0)

    print(f"\nSe encontraron {len(pages)} página(s):\n")
    micas_page = None

    for page in pages:
        p_id = page.get("id")
        p_name = page.get("name")
        p_token = page.get("access_token")
        ig_data = page.get("instagram_business_account", {})
        ig_id = ig_data.get("id") if isinstance(ig_data, dict) else None
        ig_username = ig_data.get("username") if isinstance(ig_data, dict) else None

        print(f"📄 Página: {p_name} (ID: {p_id})")
        if ig_id:
            print(f"   📸 Instagram: @{ig_username} (ID: {ig_id})")
        else:
            print("   ⚠️ Sin cuenta de Instagram Business vinculada.")

        if "mica" in p_name.lower() or "art & deco" in p_name.lower() or "micasdeco" in str(ig_username).lower():
            micas_page = {
                "name": p_name,
                "page_id": p_id,
                "page_token": p_token,
                "ig_id": ig_id,
                "ig_username": ig_username
            }

    print("\n" + "="*60)
    if micas_page:
        print("🎯 PÁGINA DETECTADA PARA EL TENANT:")
        print(f"   Página: {micas_page['name']}")
        print(f"   FB_PAGE_ID: {micas_page['page_id']}")
        print(f"   IG_BUSINESS_ACCOUNT_ID: {micas_page['ig_id']}")
        print(f"   IG_USERNAME: @{micas_page['ig_username']}")
        print("="*60)

        env_content = (
            f"# Credenciales locales para Mica's Art & Deco\n"
            f"FB_PAGE_ID={micas_page['page_id']}\n"
            f"IG_BUSINESS_ACCOUNT_ID={micas_page['ig_id'] or ''}\n"
            f"PAGE_ACCESS_TOKEN={micas_page['page_token']}\n"
        )

        if args.save_env:
            tenant_dir = Path.home() / "growth-os" / "tenants" / "micas-art-deco"
            tenant_dir.mkdir(parents=True, exist_ok=True)
            env_file = tenant_dir / ".env"
            env_file.write_text(env_content, encoding="utf-8")
            os.chmod(env_file, 0o600)
            print(f"\n✅ Archivo .env creado con éxito en:\n   {env_file}")
        else:
            print("\n📋 Contenido generado (usa --save-env para guardarlo automáticamente):")
            print(env_content.strip())
    else:
        print("⚠️ No se identificó automáticamente 'Mica'. Revisa los IDs listados arriba.")

if __name__ == "__main__":
    main()
