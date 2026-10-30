#!/usr/bin/env python3
"""CLI de Revenue Lite para tenants de producto.

Ejemplos para Mica's:

    python3 tools/revenue_tracker.py add --tenant micas-art-deco \\
        --client "Ana" --product "Tulipán en Flor" --quote 500 \\
        --status anticipo --collected 250 --source instagram

    python3 tools/revenue_tracker.py update D-0001 --tenant micas-art-deco \\
        --status cobrado --collected 500

    python3 tools/revenue_tracker.py report --tenant micas-art-deco
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core" / "growthos-core"))

from modules.intelligence.revenue import RevenueStore


def _date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def _money(value: float) -> str:
    return f"${value:,.2f}"


def _print_deal(deal) -> None:
    print(
        f"{deal.deal_id} | {deal.contact_name or 'sin cliente'} | "
        f"{deal.product_ref or 'sin producto'} | cotizado {_money(deal.amount or 0)} | "
        f"cobrado {_money(deal.amount_collected or 0)} | {deal.payment_status} | "
        f"{deal.deal_stage} | {deal.lead_source or 'sin origen'}"
    )


def _print_report(report: dict) -> None:
    print(f"Tenant: {report['tenant_id']}")
    print(f"Deals: {report['deals']}")
    print(f"Cotizado: {_money(report['quoted_total'])}")
    print(f"Ingreso reconocido: {_money(report['revenue_total'])}")
    print(f"  Anticipos: {_money(report['anticipos_total'])}")
    print(f"  Cobrado:   {_money(report['cobrado_total'])}")
    print(f"Por cobrar: {_money(report['pending_total'])}")
    print(f"Cancelado:  {_money(report['cancelled_total'])}")
    print(f"Tasa de cierre: {report['close_rate']:.1%}")
    print(f"Ticket promedio: {_money(report['average_ticket'])}")
    print("\nPor origen:")
    for key, item in sorted(report["by_source"].items()):
        print(f"  {key}: {item['deals']} deals | cobrado {_money(item['collected'])}")
    print("\nPor producto:")
    for key, item in sorted(report["by_product"].items()):
        print(f"  {key}: {item['deals']} deals | cobrado {_money(item['collected'])}")
    print("\nPor estado de pago:")
    for key, item in sorted(report["by_status"].items()):
        print(f"  {key}: {item['deals']} deals | cobrado {_money(item['collected'])}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Revenue Lite por tenant")
    parser.add_argument("--base-path", default=None, help="Raíz del repo (para pruebas)")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Registrar un deal")
    add.add_argument("--tenant", required=True)
    add.add_argument("--client", required=True)
    add.add_argument("--product", required=True)
    add.add_argument("--quote", type=float, required=True, help="Monto cotizado")
    add.add_argument("--status", default="pendiente", help="pendiente|anticipo|cobrado|cancelado")
    add.add_argument("--collected", type=float, default=0.0, help="Dinero realmente recibido")
    add.add_argument("--source", default="whatsapp", help="instagram|facebook|whatsapp|meta_ads|referral|direct|store")
    add.add_argument("--stage", default=None, help="nuevo|cotizado|negociacion|ganado|perdido")
    add.add_argument("--funnel-line", default=None, help="TOFU|MOFU|BOFU")
    add.add_argument("--payment-method", default="")
    add.add_argument("--payment-date", default=None, help="YYYY-MM-DD")
    add.add_argument("--appointment-at", default=None, help="Fecha de montaje/cita: YYYY-MM-DD")
    add.add_argument("--publication-id", default="")
    add.add_argument("--campaign-id", default="")
    add.add_argument("--conversation-id", default="")
    add.add_argument("--notes", default="")
    add.add_argument("--phone", default="")
    add.add_argument("--email", default="")
    add.add_argument("--currency", default="MXN")

    update = sub.add_parser("update", help="Actualizar un deal")
    update.add_argument("deal_id")
    update.add_argument("--tenant", required=True)
    update.add_argument("--status", default=None)
    update.add_argument("--collected", type=float, default=None)
    update.add_argument("--stage", default=None)
    update.add_argument("--payment-method", default=None)
    update.add_argument("--payment-date", default=None, help="YYYY-MM-DD")
    update.add_argument("--appointment-at", default=None, help="Fecha de montaje/cita: YYYY-MM-DD")
    update.add_argument("--notes", default=None)
    update.add_argument("--lost-reason", default=None)
    update.add_argument("--source", default=None)
    update.add_argument("--publication-id", default=None)
    update.add_argument("--campaign-id", default=None)
    update.add_argument("--conversation-id", default=None)

    list_cmd = sub.add_parser("list", help="Listar deals")
    list_cmd.add_argument("--tenant", required=True)
    list_cmd.add_argument("--json", action="store_true")

    report = sub.add_parser("report", help="Reporte de revenue")
    report.add_argument("--tenant", required=True)
    report.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    base_path = Path(args.base_path) if args.base_path else ROOT

    try:
        store = RevenueStore(args.tenant, base_path=base_path)
        if args.command == "add":
            deal = store.add(
                client=args.client,
                product=args.product,
                quote=args.quote,
                status=args.status,
                collected=args.collected,
                source=args.source,
                stage=args.stage,
                funnel_line=args.funnel_line,
                payment_method=args.payment_method,
                payment_date=_date(args.payment_date),
                appointment_at=_date(args.appointment_at),
                publication_id=args.publication_id,
                campaign_id=args.campaign_id,
                conversation_id=args.conversation_id,
                notes=args.notes,
                phone=args.phone,
                email=args.email,
                currency=args.currency,
            )
            _print_deal(deal)
        elif args.command == "update":
            deal = store.update(
                args.deal_id,
                status=args.status,
                collected=args.collected,
                stage=args.stage,
                payment_method=args.payment_method,
                payment_date=_date(args.payment_date),
                appointment_at=_date(args.appointment_at),
                notes=args.notes,
                lost_reason=args.lost_reason,
                source=args.source,
                publication_id=args.publication_id,
                campaign_id=args.campaign_id,
                conversation_id=args.conversation_id,
            )
            _print_deal(deal)
        elif args.command == "list":
            deals = store.load()
            if args.json:
                print(json.dumps([deal.model_dump(mode="json") for deal in deals], ensure_ascii=False, indent=2))
            else:
                for deal in deals:
                    _print_deal(deal)
                print(f"Total: {len(deals)} deals")
        elif args.command == "report":
            data = store.report()
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                _print_report(data)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
