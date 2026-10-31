#!/usr/bin/env python3
"""Entrypoint del timer periódico de Growth OS.

El timer de Instagram ya corre cada 15 minutos y se usa como latido para los
cortes de campañas mientras no se instale el timer dedicado de Ads. La captura
de métricas es local y no hace red si no hay un checkpoint vencido; además corre
antes de Instagram para no retrasarla si la API de Meta falla.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.social.ig_scheduler import main


def _run_ads_capture() -> int:
    # Si el timer dedicado está instalado, él es el dueño de la captura y este
    # latido no debe duplicar la llamada a Meta.
    if Path("/etc/systemd/system/growth-os-ads.timer").is_file():
        return 0
    try:
        from modules.intelligence.campaign_capture import run_due_captures

        result = run_due_captures()
        if result["status"] == "captured":
            print("[ads] cortes capturados:")
            for tenant in result["tenants"]:
                if tenant["status"] == "captured":
                    print(
                        f"  {tenant['tenant_id']}: {', '.join(tenant['checkpoints'])} "
                        f"({', '.join(tenant['campaigns'])})"
                    )
        elif result["status"] == "error":
            for tenant in result["tenants"]:
                if tenant["status"] == "error":
                    print(f"[ads] {tenant['tenant_id']}: {tenant.get('note')}", file=sys.stderr)
            return 1
        else:
            next_due = next(
                (
                    tenant.get("next_due_at")
                    for tenant in result["tenants"]
                    if tenant.get("next_checkpoint")
                ),
                None,
            )
            print(f"[ads] sin cortes pendientes{(' · próximo ' + next_due) if next_due else ''}")
        return 0
    except Exception as exc:
        print(f"[ads] error inesperado: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


def _run_universe_metrics() -> int:
    try:
        from modules.intelligence.metrics_snapshot import run_capture_cycle
        from tenants.universe.metrics.sync_publication_log import sync_publication_log

        sync_code = sync_publication_log()
        if sync_code != 0:
            return sync_code
        result = run_capture_cycle("universe")
        if result.get("error"):
            print(f"[metrics] universe: {result['error']}", file=sys.stderr)
            return 1
        print(f"[metrics] universe: {result}")
        return 0
    except Exception as exc:
        print(f"[metrics] universe error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    capture_code = _run_ads_capture()
    metrics_code = _run_universe_metrics()
    scheduler_code = main() or 0
    raise SystemExit(scheduler_code or capture_code or metrics_code)
