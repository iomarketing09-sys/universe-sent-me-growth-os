#!/usr/bin/env python3
"""
inspect_meta_token.py — Diagnóstico de Tokens, Permisos y Catálogo en Growth OS
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

ENV_SEARCH_PATHS = [
    Path.home() / "growth-os" / "tenants" / "micas-art-deco" / ".env",
    Path.home() / "growth-os" / ".env",
    Path.home() / "growth-os" / "tenants" / "universe" / ".env",
    Path.home() / "growth-os" / "tenants" / "firma-bordados" / ".env",
    Path(".env"),
]

def find_tokens():
    tokens = {}
    for p in ENV_SEARCH_PATHS:
        if p.exists():
            try:
                for line in open(p, "r", encoding="utf-8"):
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if ("TOKEN" in k or "KEY" in k) and len(v) > 25:
                        tokens[f"{p.parent.name}/{p.name}:{k}"] = v
            except Exception:
                pass
    return tokens

def query_graph(endpoint, token, params=None):
    params = params or {}
    params["access_token"] = token
    url = f"https://graph.facebook.com/v20.0/{endpoint}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GrowthOS-Inspector/1.0"})
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode())
        except:
            return {"error": {"message": f"HTTP {e.code}"}}
    except Exception as e:
        return {"error": {"message": str(e)}}

def main():
    print("=" * 70)
    print("  DIAGNÓSTICO DE TOKENS Y PERMISOS META (GROWTH OS)")
    print("=" * 70)
    
    found = find_tokens()
    print(f"\n[+] Se encontraron {len(found)} variables de token en tus archivos .env:\n")
    for name in found:
        print(f"    - {name}")
        
    for name, token in found.items():
        print("\n" + "-" * 70)
        print(f"  ANALIZANDO: {name}")
        print("-" * 70)
        
        # 1. Identidad
        me = query_graph("me", token, {"fields": "id,name"})
        if "error" in me:
            print(f"[-] No es un token válido de Meta o expiró: {me['error'].get('message')}")
            continue
        print(f"[+] Propietario del Token: {me.get('name')} (ID: {me.get('id')})")
        
        # 2. Permisos
        perms = query_graph("me/permissions", token)
        if "data" in perms:
            granted = [p["permission"] for p in perms["data"] if p.get("status") == "granted"]
            print(f"[+] Permisos concedidos ({len(granted)}):")
            print(f"    {', '.join(granted)}")
            has_cat = "catalog_management" in granted
            has_biz = "business_management" in granted
            print(f"    -> catalog_management : {'SÍ [OK]' if has_cat else 'NO [FALTANTE]'}")
            print(f"    -> business_management: {'SÍ [OK]' if has_biz else 'NO [FALTANTE]'}")
            
        # 3. Páginas que puede administrar
        accounts = query_graph("me/accounts", token, {"fields": "id,name,category"})
        if "data" in accounts:
            print(f"[+] Páginas vinculadas ({len(accounts['data'])}):")
            for page in accounts["data"]:
                print(f"    - {page.get('name')} (ID: {page.get('id')})")
                
        # 4. Probar nodo 1350743568880060 directamente
        cat = query_graph("1350743568880060", token, {"fields": "id,name,vertical,product_count"})
        print(f"[+] Prueba de consulta al Catálogo 1350743568880060:")
        if "error" in cat:
            print(f"    [-] Error: {cat['error'].get('message')}")
        else:
            print(f"    [+] Catálogo reconocido: {cat.get('name')} | Productos: {cat.get('product_count')}")

if __name__ == "__main__":
    main()
