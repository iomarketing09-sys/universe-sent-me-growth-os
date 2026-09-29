#!/usr/bin/env python3
"""
get_micas_tokens.py — Extractor automático de Page ID, Token e Instagram ID para Mica's Art & Deco
Consulta el endpoint me/accounts de Meta Graph API usando el token existente en .env
"""

from __future__ import annotations
import os
import sys
import json
import requests
from pathlib import Path

ENV_PATHS = [
    Path("/home/universe-sent-me/growth-os/.env"),
    Path("/home/universe-sent-me/growth-os/tenants/universe/.env"),
    Path("/home/universe-sent-me/growth-os/tenants/firma-bordados/.env"),
    Path("/home/universe-sent-me/growth-os/tenants/micas-art-deco/.env"),
    Path(".env")
]

def load_token() -> str | None:
    for p in ENV_PATHS:
        if p.exists():
            for line in open(p):
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k in ["PAGE_ACCESS_TOKEN", "USER_ACCESS_TOKEN", "FB_ACCESS_TOKEN", "META_ACCESS_TOKEN"] and len(v) > 20:
                    return v
    return None

def main():
    token = load_token()
    if not token:
        print("[-] Error: No se encontró ningún token en los archivos .env.")
        print("    Asegúrate de tener un token en ~/growth-os/.env o tenants/universe/.env")
        sys.exit(1)

    print("=" * 65)
    print(" CONSULTANDO META GRAPH API (me/accounts) ")
    print("=" * 65)

    url = "https://graph.facebook.com/v20.0/me/accounts"
    params = {
        "fields": "id,name,category,access_token,instagram_business_account{id,username}",
        "access_token": token,
        "limit": 50
    }

    try:
        res = requests.get(url, params=params, timeout=20)
        data = res.json()

        if "error" in data:
            print(f"[-] Error de Meta API: {data['error'].get('message')}")
            me_res = requests.get(f"https://graph.facebook.com/v20.0/me?fields=id,name&access_token={token}").json()
            print(f"    Token actual pertenece a: {me_res.get('name')} (ID: {me_res.get('id')})")
            sys.exit(1)

        pages = data.get("data", [])
        if not pages:
            print("[-] No se encontraron páginas administradas con este token.")
            sys.exit(1)

        print(f"[+] Se encontraron {len(pages)} páginas administradas:\n")
        micas_info = None

        for idx, page in enumerate(pages, 1):
            p_name = page.get("name")
            p_id = page.get("id")
            p_token = page.get("access_token")
            ig_acc = page.get("instagram_business_account", {})
            ig_id = ig_acc.get("id", "No vinculado")
            ig_user = ig_acc.get("username", "")

            is_micas = "mica" in p_name.lower() or "art" in p_name.lower()
            tag = " ---> [MICA'S ART & DECO DETECTADA]" if is_micas else ""

            print(f"{idx}. {p_name} (ID: {p_id}){tag}")
            print(f"   Instagram Business ID : {ig_id} {f'(@{ig_user})' if ig_user else ''}")
            print(f"   Page Access Token     : {p_token[:15]}...{p_token[-10:]}")
            print("-" * 65)

            if is_micas:
                micas_info = {
                    "FB_PAGE_ID": p_id,
                    "FB_PAGE_NAME": p_name,
                    "PAGE_ACCESS_TOKEN": p_token,
                    "IG_USER_ID": ig_id if ig_id != "No vinculado" else "",
                    "IG_USERNAME": ig_user if ig_user else "micas.deco"
                }

        target_env = Path("/home/universe-sent-me/growth-os/tenants/micas-art-deco/.env")
        if micas_info and target_env.exists():
            print(f"\n[+] Actualizando automáticamente {target_env}...")
            lines = []
            for line in open(target_env):
                k = line.split("=")[0].strip() if "=" in line else ""
                if k == "FB_PAGE_ID":
                    lines.append(f"FB_PAGE_ID=\"{micas_info['FB_PAGE_ID']}\"\n")
                elif k == "PAGE_ACCESS_TOKEN":
                    lines.append(f"PAGE_ACCESS_TOKEN=\"{micas_info['PAGE_ACCESS_TOKEN']}\"\n")
                elif k == "IG_USER_ID":
                    lines.append(f"IG_USER_ID=\"{micas_info['IG_USER_ID']}\"\n")
                elif k == "FB_PAGE_NAME":
                    lines.append(f"FB_PAGE_NAME=\"{micas_info['FB_PAGE_NAME']}\"\n")
                else:
                    lines.append(line)
            with open(target_env, "w") as f:
                f.writelines(lines)
            print(f"[+] ¡Configuración de Mica's Art & Deco guardada en {target_env} con éxito!")

    except Exception as e:
        print(f"[-] Excepción consultando Meta Graph API: {e}")

if __name__ == "__main__":
    main()
