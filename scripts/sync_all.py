#!/usr/bin/env python3
"""CLI para snapshots seguros de evidencia local por tenant."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from growth.sync import list_tenants, sanitize_saved_snapshots, sync_tenant, write_snapshot
from growth.tenant_registry import get_registry


def main() -> None:
    parser = argparse.ArgumentParser(description="Growth OS - Sync seguro de evidencia local")
    parser.add_argument("--tenant", help="Tenant específico a sincronizar")
    parser.add_argument("--all", action="store_true", help="Sincronizar todos los tenants")
    parser.add_argument("--list", action="store_true", help="Listar tenants disponibles")
    parser.add_argument("--no-write", action="store_true", help="Solo mostrar el snapshot; no guardar archivos")
    parser.add_argument("--quiet", "-q", action="store_true", help="Salida JSON compacta")
    parser.add_argument("--live-whatsapp", action="store_true", help="Leer mensajes remotos del worker de WhatsApp")
    parser.add_argument("--live-meta", action="store_true", help="Capturar datos en vivo desde Meta Graph API (si no hay evidencia local)")
    parser.add_argument("--live-ads", action="store_true", help="Capturar métricas de campañas desde Meta Marketing API")
    parser.add_argument("--live-google", action="store_true", help="Capturar métricas de Google Search Console y Bing Webmaster")
    parser.add_argument("--sanitize-snapshots", action="store_true", help="Eliminar secretos de snapshots guardados")

    args = parser.parse_args()

    registry = get_registry()
    if args.list:
        tenants = list_tenants(registry)
        print(f"{'TENANT':<20} {'TYPE':<15} {'META':<6} {'GOOGLE':<8} {'BUSINESS'}")
        print("-" * 84)
        for tenant in tenants:
            print(
                f"{tenant['tenant_id']:<20} {tenant['type']:<15} "
                f"{'OK' if tenant['meta_configured'] else '-':<6} "
                f"{'OK' if tenant['google_configured'] else '-':<8} "
                f"{tenant['business_name']}"
            )
        return

    if not args.tenant and not args.all:
        parser.print_help()
        return

    tenant_ids = [args.tenant] if args.tenant else [tenant["tenant_id"] for tenant in list_tenants(registry)]
    results = []
    for tenant_id in tenant_ids:
        if args.sanitize_snapshots:
            updated = sanitize_saved_snapshots(registry.tenants_dir / tenant_id)
            results.append({"tenant_id": tenant_id, "snapshots_sanitized": updated})
            continue
        result = sync_tenant(tenant_id, registry=registry, args=args)
        if not args.no_write:
            paths = write_snapshot(result, registry.tenants_dir / tenant_id)
            result["saved"] = {key: str(path) for key, path in paths.items()}
        results.append(result)

    if args.quiet:
        print(json.dumps(results, ensure_ascii=False))
        return

    for result in results:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
