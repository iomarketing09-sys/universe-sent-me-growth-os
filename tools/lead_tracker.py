#!/usr/bin/env python3
"""CLI de Leads Lite: conversaciones y nivel de intención.

Ejemplos para Flexi:

    python3 tools/lead_tracker.py add --tenant flexi \
        --name "Cliente" --phone "8781234567" --source whatsapp \
        --intent caliente --interest "Botines Quirelli" \
        --campaign-id 2026-10_flexi_ads_500mxn

    python3 tools/lead_tracker.py update L-0001 --tenant flexi \
        --status cotizado --next-action-at 2026-10-31

    python3 tools/lead_tracker.py report --tenant flexi
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

from modules.intelligence.leads import LeadStore


def _date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def _print_lead(lead) -> None:
    print(
        f"{lead.lead_id} | {lead.contact_name or 'sin nombre'} | "
        f"{lead.contact_phone or lead.contact_email or 'sin contacto'} | "
        f"{lead.intent} | {lead.status} | {lead.lead_source or 'sin origen'} | "
        f"{lead.product_interest or 'sin interés'}"
    )


def _print_report(report: dict) -> None:
    print(f"Tenant: {report['tenant_id']}")
    print(f"Leads: {report['leads']}")
    print(
        f"Calientes: {report['hot']} | Tibios: {report['warm']} | Fríos: {report['cold']}"
    )
    print(f"Abiertos: {report['open']} | Ganados: {report['won']} | Perdidos: {report['lost']}")
    print(f"Nuevos últimos 7 días: {report['new_last_7d']}")
    print(f"Seguimientos vencidos: {report['followups_due']}")
    print(f"Contactados: {report['contact_rate']:.1%}")
    print(f"Cotizados: {report['quote_rate']:.1%}")
    print(f"Citas: {report['appointment_rate']:.1%}")
    print("\nPor intención:")
    for key, count in report["by_intent"].items():
        print(f"  {key}: {count}")
    print("\nPor origen:")
    for key, count in report["by_source"].items():
        print(f"  {key}: {count}")
    print("\nPor estado:")
    for key, count in report["by_status"].items():
        print(f"  {key}: {count}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Leads Lite por tenant")
    parser.add_argument("--base-path", default=None, help="Raíz del repo (para pruebas)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="Registrar un lead")
    add.add_argument("--tenant", required=True)
    add.add_argument("--name", default="")
    add.add_argument("--phone", default="")
    add.add_argument("--email", default="")
    add.add_argument("--source", default="whatsapp")
    add.add_argument("--intent", default="frio", help="frio|tibio|caliente")
    add.add_argument("--status", default="nuevo")
    add.add_argument("--interest", default="", help="Producto o tema de interés")
    add.add_argument("--budget", default="", help="Rango de presupuesto declarado")
    add.add_argument("--publication-id", default="")
    add.add_argument("--campaign-id", default="")
    add.add_argument("--conversation-id", default="")
    add.add_argument("--notes", default="")
    add.add_argument("--lost-reason", default="")
    add.add_argument("--assigned-to", default="")
    add.add_argument("--created-at", default=None, help="YYYY-MM-DD")
    add.add_argument("--last-contact-at", default=None, help="YYYY-MM-DD")
    add.add_argument("--next-action-at", default=None, help="YYYY-MM-DD")

    update = subparsers.add_parser("update", help="Actualizar intención o estado")
    update.add_argument("lead_id")
    update.add_argument("--tenant", required=True)
    update.add_argument("--intent", default=None)
    update.add_argument("--status", default=None)
    update.add_argument("--interest", default=None)
    update.add_argument("--budget", default=None)
    update.add_argument("--notes", default=None)
    update.add_argument("--lost-reason", default=None)
    update.add_argument("--assigned-to", default=None)
    update.add_argument("--source", default=None)
    update.add_argument("--publication-id", default=None)
    update.add_argument("--campaign-id", default=None)
    update.add_argument("--conversation-id", default=None)
    update.add_argument("--last-contact-at", default=None, help="YYYY-MM-DD")
    update.add_argument("--next-action-at", default=None, help="YYYY-MM-DD")

    list_cmd = subparsers.add_parser("list", help="Listar leads")
    list_cmd.add_argument("--tenant", required=True)
    list_cmd.add_argument("--intent", default=None)
    list_cmd.add_argument("--status", default=None)
    list_cmd.add_argument("--source", default=None)
    list_cmd.add_argument("--since", default=None, help="YYYY-MM-DD")
    list_cmd.add_argument("--json", action="store_true")

    report = subparsers.add_parser("report", help="Reporte agregado")
    report.add_argument("--tenant", required=True)
    report.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    base_path = Path(args.base_path) if args.base_path else None

    try:
        store = LeadStore(args.tenant, base_path=base_path)
        if args.command == "add":
            lead = store.add(
                contact_name=args.name,
                phone=args.phone,
                email=args.email,
                source=args.source,
                intent=args.intent,
                status=args.status,
                product_interest=args.interest,
                budget_range=args.budget,
                publication_id=args.publication_id,
                campaign_id=args.campaign_id,
                conversation_id=args.conversation_id,
                notes=args.notes,
                lost_reason=args.lost_reason,
                assigned_to=args.assigned_to,
                created_at=_date(args.created_at),
                last_contact_at=_date(args.last_contact_at),
                next_action_at=_date(args.next_action_at),
            )
            _print_lead(lead)
        elif args.command == "update":
            lead = store.update(
                args.lead_id,
                intent=args.intent,
                status=args.status,
                product_interest=args.interest,
                budget_range=args.budget,
                notes=args.notes,
                lost_reason=args.lost_reason,
                assigned_to=args.assigned_to,
                source=args.source,
                publication_id=args.publication_id,
                campaign_id=args.campaign_id,
                conversation_id=args.conversation_id,
                last_contact_at=_date(args.last_contact_at),
                next_action_at=_date(args.next_action_at),
            )
            _print_lead(lead)
        elif args.command == "list":
            leads = store.filtered(
                intent=args.intent,
                status=args.status,
                source=args.source,
                since=_date(args.since),
            )
            if args.json:
                print(json.dumps([lead.model_dump(mode="json") for lead in leads], ensure_ascii=False, indent=2))
            else:
                for lead in leads:
                    _print_lead(lead)
        elif args.command == "report":
            data = store.report()
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                _print_report(data)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
