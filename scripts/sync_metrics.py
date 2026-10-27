#!/usr/bin/env python3
"""
Sync Metrics - Sincronización de métricas cross-tenant
Consolida métricas de Meta, Google, TikTok, YouTube para reporting
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from growth.tenant_registry import get_registry


def collect_meta_metrics(tenant_id: str) -> dict:
    """Recolecta métricas de Meta para un tenant"""
    print(f"[{tenant_id}] 📊 Collecting Meta metrics...")
    # TODO: from growthos.integrations.meta_graph import get_metrics
    return {"source": "meta", "tenant": tenant_id, "status": "placeholder"}


def collect_google_metrics(tenant_id: str) -> dict:
    """Recolecta métricas de Google (GBP + GSC)"""
    print(f"[{tenant_id}] 📊 Collecting Google metrics...")
    return {"source": "google", "tenant": tenant_id, "status": "placeholder"}


def collect_video_metrics(tenant_id: str) -> dict:
    """Recolecta métricas de video (TikTok, YouTube, Reels)"""
    print(f"[{tenant_id}] 📊 Collecting Video metrics...")
    return {"source": "video", "tenant": tenant_id, "status": "placeholder"}


def consolidate_all(quiet: bool = False) -> dict:
    """Consolida métricas de todos los tenants"""
    registry = get_registry()
    tenants = registry.list_tenants()
    
    consolidated = {
        "generated_at": datetime.now().isoformat(),
        "tenants": {}
    }
    
    for tid in tenants:
        if not quiet:
            print(f"\n=== {tid} ===")
        consolidated["tenants"][tid] = {
            "meta": collect_meta_metrics(tid),
            "google": collect_google_metrics(tid),
            "video": collect_video_metrics(tid),
        }
    
    return consolidated


def main():
    parser = argparse.ArgumentParser(description="Sync Metrics - Cross-tenant metrics consolidation")
    parser.add_argument("--tenant", help="Tenant específico")
    parser.add_argument("--all", action="store_true", help="Todos los tenants")
    parser.add_argument("--consolidate", action="store_true", help="Generar reporte consolidado")
    parser.add_argument("--output", help="Archivo de salida JSON")
    parser.add_argument("--quiet", "-q", action="store_true", help="Salida mínima")
    
    args = parser.parse_args()
    
    if args.consolidate or args.all:
        result = consolidate_all(quiet=args.quiet)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Consolidado guardado en {args.output}")
        elif not args.quiet:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.tenant:
        result = {
            "meta": collect_meta_metrics(args.tenant),
            "google": collect_google_metrics(args.tenant),
            "video": collect_video_metrics(args.tenant),
        }
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
