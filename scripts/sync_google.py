#!/usr/bin/env python3
"""
Sync Google - Google Business Profile + Search Console + Bing Webmaster
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from growth.tenant_registry import get_registry


def sync_gbp(tenant_id: str) -> dict:
    """Google Business Profile"""
    print(f"[{tenant_id}] 🔄 GBP sync...")
    # TODO: from growthos.integrations.google_business import sync_gbp
    return {"status": "configured_only", "note": "Requiere OAuth refresh token"}


def sync_gsc(tenant_id: str) -> dict:
    """Google Search Console"""
    print(f"[{tenant_id}] 🔄 GSC sync...")
    # TODO: from growthos.integrations.google_business import sync_gsc
    return {"status": "blocked", "note": "Requiere sitio verificado"}


def sync_bing(tenant_id: str) -> dict:
    """Bing Webmaster"""
    print(f"[{tenant_id}] 🔄 Bing sync...")
    # TODO: from growthos.integrations.google_business import sync_bing
    return {"status": "blocked", "note": "Requiere API key + sitio verificado"}


def main():
    parser = argparse.ArgumentParser(description="Sync Google services")
    parser.add_argument("--tenant", required=True, help="Tenant ID")
    parser.add_argument("--gbp-only", action="store_true", help="Solo GBP")
    parser.add_argument("--gsc-only", action="store_true", help="Solo Search Console")
    parser.add_argument("--bing-only", action="store_true", help="Solo Bing")
    
    args = parser.parse_args()
    
    registry = get_registry()
    config = registry.load_config(args.tenant)
    
    if not config:
        print(f"❌ Tenant {args.tenant} no encontrado")
        return
    
    results = {}
    if args.gbp_only or not (args.gsc_only or args.bing_only):
        results["gbp"] = sync_gbp(args.tenant)
    if args.gsc_only or not (args.gbp_only or args.bing_only):
        results["gsc"] = sync_gsc(args.tenant)
    if args.bing_only or not (args.gbp_only or args.gsc_only):
        results["bing"] = sync_bing(args.tenant)
    
    print(f"✅ Google sync para {args.tenant}: {results}")


if __name__ == "__main__":
    main()
