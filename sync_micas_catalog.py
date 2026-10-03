#!/usr/bin/env python3
"""
sync_micas_catalog.py — Administrador y Sincronizador de Catálogo Meta Commerce
Tenant: Mica's Art & Deco (Growth OS)
Catalog ID: 1350743568880060
Business ID: 1940942776222567
"""

from __future__ import annotations
import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, List, Any, Optional

DEFAULT_CATALOG_ID = "1350743568880060"
DEFAULT_BUSINESS_ID = "1940942776222567"
GRAPH_VERSION = "v20.0"

ENV_SEARCH_PATHS = [
    Path.home() / "growth-os" / "tenants" / "micas-art-deco" / ".env",
    Path.home() / "growth-os" / ".env",
    Path.home() / "growth-os" / "tenants" / "universe" / ".env",
    Path(".env"),
]

def find_token() -> Optional[str]:
    for var in ["META_ACCESS_TOKEN", "PAGE_ACCESS_TOKEN", "FB_ACCESS_TOKEN", "USER_ACCESS_TOKEN"]:
        token = os.environ.get(var)
        if token and len(token) > 25:
            return token.strip()
    
    for p in ENV_SEARCH_PATHS:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k in ["META_ACCESS_TOKEN", "PAGE_ACCESS_TOKEN", "FB_ACCESS_TOKEN", "USER_ACCESS_TOKEN"] and len(v) > 25:
                            return v
            except Exception:
                continue
    return None

def make_meta_request(endpoint: str, method: str = "GET", params: Dict[str, Any] = None, data: Dict[str, Any] = None, token: str = "") -> Dict[str, Any]:
    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{endpoint}"
    params = params or {}
    params["access_token"] = token
    
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}" if query_string else url
    
    body = None
    headers = {"User-Agent": "MicasArtDeco-GrowthOS/1.0"}
    if data:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        
    req = urllib.request.Request(full_url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raw_error = e.read().decode("utf-8")
        try:
            return json.loads(raw_error)
        except Exception:
            return {"error": {"message": f"HTTP Error {e.code}: {e.reason}", "raw": raw_error}}
    except Exception as e:
        return {"error": {"message": str(e)}}

def audit_catalog(catalog_id: str, token: str):
    print("\n" + "=" * 75)
    print(f"  AUDITANDO CATÁLOGO META COMMERCE: {catalog_id}")
    print("=" * 75)
    
    fields = "id,retailer_id,name,description,availability,price,currency,url,image_url,category,visibility,review_status"
    res = make_meta_request(f"{catalog_id}/products", params={"fields": fields, "limit": 100}, token=token)
    
    if "error" in res:
        err = res["error"]
        print(f"\n[-] Error de Meta API al consultar catálogo:")
        print(f"    Mensaje: {err.get('message')}")
        print(f"    Tipo:    {err.get('type')}")
        print(f"    Código:  {err.get('code')}")
        print("\n[!] Asegúrate de que el token tenga el permiso 'catalog_management' y pertenezca al Business Manager.")
        return
        
    products = res.get("data", [])
    print(f"\n[+] Total de productos encontrados en el catálogo: {len(products)}\n")
    
    if not products:
        print("El catálogo no contiene productos activos.")
        return
        
    audit_data = []
    print(f"{'#':<3} | {'Nombre':<35} | {'Precio':<10} | {'Disp.':<10} | {'Estatus Review'}")
    print("-" * 75)
    for idx, p in enumerate(products, 1):
        name = p.get("name", "Sin Nombre")[:35]
        price = f"{p.get('currency', 'MXN')} {p.get('price', 'N/A')}"
        avail = p.get("availability", "N/A")
        review = p.get("review_status", "N/A")
        dest_url = p.get("url", "SIN_URL")
        img_url = p.get("image_url", "SIN_IMAGEN")
        ret_id = p.get("retailer_id", p.get("id"))
        
        print(f"{idx:<3} | {name:<35} | {price:<10} | {avail:<10} | {review}")
        print(f"    -> Retailer ID (SKU): {ret_id}")
        print(f"    -> URL Destino Actual: {dest_url}")
        print(f"    -> Imagen: {img_url[:65]}...")
        print("-" * 75)
        
        audit_data.append({
            "index": idx,
            "id": p.get("id"),
            "retailer_id": ret_id,
            "name": p.get("name"),
            "price": p.get("price"),
            "currency": p.get("currency"),
            "availability": avail,
            "url": dest_url,
            "image_url": img_url,
            "review_status": review
        })
        
    out_file = f"meta_catalog_audit_{catalog_id}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Auditoría exportada exitosamente a: {out_file}")

def generate_batch_payload_from_sheet_data(catalog_id: str, base_url: str = "https://wa.me/528781234567") -> List[Dict[str, Any]]:
    new_items = [
        {
            "retailer_id": "MCA-OLE-001",
            "name": "Mica's Art & Deco - Virgen de Guadalupe #1 con Hoja de Oro",
            "description": "Obra sacra de la Virgen de Guadalupe pintada al óleo sobre lienzo de 28 x 35 cm con aplicaciones manuales de auténtica hoja de oro texturizada.",
            "availability": "in stock",
            "condition": "new",
            "price": 200000,
            "currency": "MXN",
            "url": f"{base_url}?text=Hola%20Mica,%20me%20interesa%20la%20obra%20MCA-OLE-001%20Virgen%20de%20Guadalupe%20%231",
            "image_url": "https://lh3.googleusercontent.com/d/1mZhlycYP-iS96aYLaKB6W-l9w-EpgeNw",
            "brand": "Mica's Art & Deco"
        },
        {
            "retailer_id": "MCA-OLE-002",
            "name": "Mica's Art & Deco - Virgen de Guadalupe #2 con Hoja de Oro",
            "description": "Pintura al óleo de la Virgen sobre lienzo de 28 x 35 cm con detalles sutiles en hoja de oro y tonos cálidos.",
            "availability": "in stock",
            "condition": "new",
            "price": 150000,
            "currency": "MXN",
            "url": f"{base_url}?text=Hola%20Mica,%20me%20interesa%20la%20obra%20MCA-OLE-002%20Virgen%20de%20Guadalupe%20%232",
            "image_url": "https://lh3.googleusercontent.com/d/193Xx8Cu_YnMlmHrYJ3nOMzlTr0FEfOZY",
            "brand": "Mica's Art & Deco"
        },
        {
            "retailer_id": "MCA-BOT-001",
            "name": "Mica's Art & Deco - Limas Frescas al Óleo",
            "description": "Bodegón botánico de limas con pincelada visible, estudio de luz natural y textura sobre lienzo de 20 x 25 cm.",
            "availability": "in stock",
            "condition": "new",
            "price": 50000,
            "currency": "MXN",
            "url": f"{base_url}?text=Hola%20Mica,%20me%20interesa%20la%20obra%20MCA-BOT-001%20Limas%20Frescas",
            "image_url": "https://lh3.googleusercontent.com/d/1-wWNqFNNmBKEtX13pzDmFKBoBHBlt6mI",
            "brand": "Mica's Art & Deco"
        },
        {
            "retailer_id": "MCA-BOT-002",
            "name": "Mica's Art & Deco - Manzana en Repisa al Óleo",
            "description": "Bodegón clásico de manzana con textura al óleo y paleta cálida sobre lienzo de 20 x 25 cm.",
            "availability": "in stock",
            "condition": "new",
            "price": 50000,
            "currency": "MXN",
            "url": f"{base_url}?text=Hola%20Mica,%20me%20interesa%20la%20obra%20MCA-BOT-002%20Manzana%20en%20Repisa",
            "image_url": "https://lh3.googleusercontent.com/d/1-zgu90ZLMUtjqmkMOTXsPROOk7HA6Hqw",
            "brand": "Mica's Art & Deco"
        },
        {
            "retailer_id": "MCA-PAI-001",
            "name": "Mica's Art & Deco - Atardecer Sereno al Óleo",
            "description": "Paisaje atmosférico al óleo capturando la caída de la luz natural sobre bastidor de 20 x 25 cm.",
            "availability": "in stock",
            "condition": "new",
            "price": 50000,
            "currency": "MXN",
            "url": f"{base_url}?text=Hola%20Mica,%20me%20interesa%20la%20obra%20MCA-PAI-001%20Atardecer%20Sereno",
            "image_url": "https://lh3.googleusercontent.com/d/1RBHdfuR4ye5r5WvAqoRTJ9HRIDJDIbcy",
            "brand": "Mica's Art & Deco"
        },
        {
            "retailer_id": "MCA-BOT-003",
            "name": "Mica's Art & Deco - Tulipán en Flor al Óleo",
            "description": "Composición botánica de tulipán con tonos vivos y elegancia floral sobre lienzo de 20 x 25 cm.",
            "availability": "in stock",
            "condition": "new",
            "price": 50000,
            "currency": "MXN",
            "url": f"{base_url}?text=Hola%20Mica,%20me%20interesa%20la%20obra%20MCA-BOT-003%20Tulipán%20en%20Flor",
            "image_url": "https://lh3.googleusercontent.com/d/1nCmh0d6KDzUmuHePxJK8OmQ-uxVlM8uC",
            "brand": "Mica's Art & Deco"
        },
        {
            "retailer_id": "MCA-SOB-001",
            "name": "Mica's Art & Deco - Sobres Artesanales Pintados a Mano (Pack de 4)",
            "description": "Juego de 4 sobres de papel artesanal decorados a mano en acuarela botánica para obsequios monetarios en bodas y graduaciones.",
            "availability": "in stock",
            "condition": "new",
            "price": 10000,
            "currency": "MXN",
            "url": f"{base_url}?text=Hola%20Mica,%20me%20interesa%20el%20Pack%20de%20Sobres%20MCA-SOB-001",
            "image_url": "https://lh3.googleusercontent.com/d/1QhqjLP9wVdYx9mgR-hGniozGGmyV7Aoj",
            "brand": "Mica's Art & Deco"
        }
    ]
    
    requests = []
    for it in new_items:
        requests.append({
            "method": "UPDATE",
            "retailer_id": it["retailer_id"],
            "data": it
        })
    return requests

def sync_batch(catalog_id: str, token: str, dry_run: bool = True):
    print("\n" + "=" * 75)
    print(f"  SINCRONIZACIÓN BATCH AL CATÁLOGO META: {catalog_id}")
    print(f"  Modo: {'DRY-RUN (Simulación sin escrituras)' if dry_run else 'LIVE (Actualización real en Meta)'}")
    print("=" * 75)
    
    requests_payload = generate_batch_payload_from_sheet_data(catalog_id)
    print(f"\n[+] Total de solicitudes preparadas: {len(requests_payload)} productos")
    for r in requests_payload:
        data = r["data"]
        print(f"    - [{r['method']}] {data['retailer_id']}: {data['name']} ({data['currency']} {data['price']/100:.2f})")
        print(f"      Destino: {data['url']}")
        
    if dry_run:
        print("\n[i] Para ejecutar la subida real a Meta Commerce Manager, ejecuta:")
        print(f"    python3 sync_micas_catalog.py --sync --live\n")
        return
        
    payload = {"requests": requests_payload}
    res = make_meta_request(f"{catalog_id}/batch", method="POST", data=payload, token=token)
    
    if "error" in res:
        print(f"\n[-] Error al ejecutar Batch API en Meta:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"\n[+] ¡Éxito! Lote procesado por Meta Commerce Manager:")
        print(json.dumps(res, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description="Gestor de Catálogo Meta Commerce para Mica's Art & Deco")
    parser.add_argument("--catalog-id", default=DEFAULT_CATALOG_ID, help="ID del Catálogo de Meta")
    parser.add_argument("--token", default=None, help="Meta Access Token (si no se proporciona, busca en .env)")
    parser.add_argument("--audit", action="store_true", help="Inspecciona los productos actuales del catálogo")
    parser.add_argument("--sync", action="store_true", help="Sincroniza los nuevos productos al catálogo")
    parser.add_argument("--live", action="store_true", help="Aplica cambios reales en Meta (por defecto es dry-run)")
    args = parser.parse_args()
    
    token = args.token or find_token()
    if not token and (args.audit or (args.sync and args.live)):
        print("\n[-] Error: No se encontró ningún token de acceso de Meta.")
        print("    Pasa el token con el argumento: --token <TU_TOKEN>")
        print("    O guárdalo en tu archivo .env como META_ACCESS_TOKEN o PAGE_ACCESS_TOKEN.\n")
        sys.exit(1)
        
    if args.audit:
        audit_catalog(args.catalog_id, token)
    elif args.sync:
        sync_batch(args.catalog_id, token, dry_run=not args.live)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
