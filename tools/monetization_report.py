#!/usr/bin/env python3
"""CLI de Monetization Lite para Growth OS.

Ejemplos:

    python3 tools/monetization_report.py import-signals --tenant universe
    python3 tools/monetization_report.py report --tenant universe --granularity weekly
    python3 tools/monetization_report.py add-period --tenant universe \\
        --platform Facebook --program meta_content_monetization \\
        --period-start 2026-10-01 --period-end 2026-10-31 \\
        --estimated-net 25 --status estimated
    python3 tools/monetization_report.py add-payout --tenant universe \\
        --platform Facebook --program meta_content_monetization \\
        --period-start 2026-10-01 --period-end 2026-10-31 \\
        --paid-at 2026-11-15 --gross 25 --fee 1.75 --net 23.25
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core" / "growthos-core"))

from modules.intelligence.monetization import DEFAULT_PLATFORM, DEFAULT_PROGRAM, MonetizationStore


def _money(value: float) -> str:
    return f"${value:,.2f}"


def _print_signal(signal) -> None:
    print(
        f"{signal.signal_date} | {signal.publication_id[:28]:<28} | "
        f"{signal.series or 'sin_serie':<14} | bonus {signal.bonus_points:>4} | "
        f"R{signal.reactions:>3} C{signal.comments:>2} S{signal.shares:>2}"
    )


def _print_report(report: dict) -> None:
    signals = report["signals"]
    money = report["money"]
    print(f"Tenant: {report['tenant_id']}")
    print(f"Señales: {signals['rows']} filas | {signals['unique_posts']} posts | {signals['date_start']} -> {signals['date_end']}")
    print(f"Última señal: {signals['date_end']} (hace {signals['latest_signal_age_days']} días)")
    print(
        f"Última señal de posts: {signals['latest_post_signal_date']} "
        f"(hace {signals['latest_post_signal_age_days']} días)"
    )
    account = signals.get("account") or {}
    if account.get("date_end"):
        print(
            f"Cuenta: {account['date_end']} | bonus diario {account['latest_bonus_points']:,} | "
            f"R{account['latest_reactions']:,} C{account['latest_comments']:,} S{account['latest_shares']:,}"
        )
    print(f"Bonus acumulado (último por post): {signals['latest_bonus_points']:,}")
    print(f"Bonus incremental (sin doble conteo): {signals['incremental_bonus_points']:,}")
    print(f"Interacciones: R{signals['latest_reactions']:,} C{signals['latest_comments']:,} S{signals['latest_shares']:,}")

    granularity = report.get("granularity", "daily")
    label = {"daily": "día", "weekly": "semana", "monthly": "mes"}.get(granularity, granularity)
    print(f"\nIncrementos por {label}")
    for row in signals["increments"].get(granularity, [])[-10:]:
        print(
            f"  {row['period']:<10} bonus={row['bonus_points']:>5} "
            f"R{row['reactions']:>4} C{row['comments']:>3} S{row['shares']:>4} "
            f"posts={row['publications']:>2} correcciones={row['corrections']:>2}"
        )
    if account.get("daily"):
        print("\nCuenta, últimos días")
        for row in account["daily"][-5:]:
            print(
                f"  {row['period']:<10} bonus={row['bonus_points']:>5} "
                f"R{row['reactions']:>4} C{row['comments']:>3} S{row['shares']:>4}"
            )
    print("\nDinero")
    print(f"  Estimado:          {_money(money['estimated_net'])}")
    print(f"  Aprobado sin pago: {_money(money['approved_unpaid_net'])}")
    print(f"  Pipeline:          {_money(money['pipeline_net'])}")
    print(f"  Pagado (neto):     {_money(money['paid_net'])}")
    print(f"  Reconocido:        {_money(money['recognized_net'])}")
    payouts = money["payouts"]
    print(f"  Payouts: {payouts['count']} | bruto {_money(payouts['gross'])} | fee {_money(payouts['fee'])} | neto {_money(payouts['net'])}")
    threshold = money.get("payout_threshold")
    if threshold:
        state = "alcanzado" if threshold["reached"] else f"faltan {_money(threshold['remaining'])}"
        print(
            f"  Umbral payout:     {_money(threshold['amount'])} {threshold['currency']} | "
            f"saldo {_money(threshold['current_balance'])} | {state}"
        )

    print("\nPor serie")
    for key, item in list(report["by_series"].items())[:8]:
        print(f"  {key:<20} posts={item['posts']:>2} bonus={item['bonus_points']:>5} mediana={item['median_bonus']:>6.1f} share_rate={item['share_rate']:.1%}")

    print("\nPor horario")
    for key, item in list(report["by_slot"].items())[:8]:
        print(f"  {key:<8} posts={item['posts']:>2} bonus={item['bonus_points']:>5} mediana={item['median_bonus']:>6.1f}")

    print("\nTop posts")
    for post in report["top_posts"][:8]:
        print(
            f"  {post['bonus_points']:>4} | {post['published_at'][:16]:<16} | "
            f"{(post['series'] or 'sin_serie'):<14} | {post['meme_text'][:55]}"
        )

    warnings = report["data_quality"]["warnings"]
    if warnings:
        print("\nAvisos")
        for warning in warnings:
            print(f"  - {warning}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Monetization Lite por tenant")
    parser.add_argument("--base-path", default=None, help="Raíz del repo (para pruebas)")
    sub = parser.add_subparsers(dest="command", required=True)

    import_signals = sub.add_parser("import-signals", help="Importar JSON históricos de señales")
    import_signals.add_argument("--tenant", required=True)
    import_signals.add_argument("--input-dir", default=None)
    import_signals.add_argument("--contexts", default=None)
    import_signals.add_argument("--program", default=DEFAULT_PROGRAM)
    import_signals.add_argument("--platform", default=DEFAULT_PLATFORM)

    import_account = sub.add_parser(
        "import-account-log", help="Importar log diario agregado de cuenta"
    )
    import_account.add_argument("--tenant", required=True)
    import_account.add_argument("--input", default=None)
    import_account.add_argument("--program", default=DEFAULT_PROGRAM)
    import_account.add_argument("--platform", default=DEFAULT_PLATFORM)

    report = sub.add_parser("report", help="Reporte de monetización")
    report.add_argument("--tenant", required=True)
    report.add_argument("--granularity", choices=["daily", "weekly", "monthly"], default="daily")
    report.add_argument("--since", default=None, help="YYYY-MM-DD")
    report.add_argument("--until", default=None, help="YYYY-MM-DD")
    report.add_argument("--json", action="store_true")

    list_signals = sub.add_parser("list-signals", help="Listar señales canónicas")
    list_signals.add_argument("--tenant", required=True)
    list_signals.add_argument("--limit", type=int, default=20)
    list_signals.add_argument("--json", action="store_true")

    add_period = sub.add_parser("add-period", help="Registrar estimado/aprobado")
    add_period.add_argument("--tenant", required=True)
    add_period.add_argument("--platform", default=DEFAULT_PLATFORM)
    add_period.add_argument("--program", default=DEFAULT_PROGRAM)
    add_period.add_argument("--period-start", required=True)
    add_period.add_argument("--period-end", required=True)
    add_period.add_argument("--currency", default="USD")
    add_period.add_argument("--estimated-net", type=float, default=0.0)
    add_period.add_argument("--approved-net", type=float, default=0.0)
    add_period.add_argument("--status", choices=["estimated", "approved", "paid", "reversed"], default="estimated")
    add_period.add_argument("--source", default="manual")
    add_period.add_argument("--notes", default="")

    list_periods = sub.add_parser("list-periods", help="Listar periodos")
    list_periods.add_argument("--tenant", required=True)
    list_periods.add_argument("--json", action="store_true")

    add_payout = sub.add_parser("add-payout", help="Registrar payout confirmado")
    add_payout.add_argument("--tenant", required=True)
    add_payout.add_argument("--platform", default=DEFAULT_PLATFORM)
    add_payout.add_argument("--program", default=DEFAULT_PROGRAM)
    add_payout.add_argument("--period-start", required=True)
    add_payout.add_argument("--period-end", required=True)
    add_payout.add_argument("--paid-at", required=True)
    add_payout.add_argument("--currency", default="USD")
    add_payout.add_argument("--gross", type=float, default=0.0)
    add_payout.add_argument("--fee", type=float, default=0.0)
    add_payout.add_argument("--net", type=float, default=None)
    add_payout.add_argument("--status", choices=["pending", "paid", "reversed"], default="paid")
    add_payout.add_argument("--source", default="manual")
    add_payout.add_argument("--evidence", default="")
    add_payout.add_argument("--notes", default="")

    list_payouts = sub.add_parser("list-payouts", help="Listar payouts")
    list_payouts.add_argument("--tenant", required=True)
    list_payouts.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    base_path = Path(args.base_path) if args.base_path else ROOT

    try:
        store = MonetizationStore(args.tenant, base_path=base_path)
        if args.command == "import-signals":
            result = store.import_signal_dir(
                input_dir=Path(args.input_dir) if args.input_dir else None,
                contexts_path=Path(args.contexts) if args.contexts else None,
                program=args.program,
                platform=args.platform,
            )
            print(json.dumps(result, ensure_ascii=False))
        elif args.command == "import-account-log":
            result = store.import_account_log(
                path=Path(args.input) if args.input else None,
                program=args.program,
                platform=args.platform,
            )
            print(json.dumps(result, ensure_ascii=False))
        elif args.command == "report":
            data = store.report(granularity=args.granularity, since=args.since, until=args.until)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                _print_report(data)
        elif args.command == "list-signals":
            items = store.load_signals()
            if args.limit:
                items = items[-args.limit:]
            if args.json:
                print(json.dumps([item.__dict__ for item in items], ensure_ascii=False, indent=2))
            else:
                for item in items:
                    _print_signal(item)
                print(f"Total: {len(store.load_signals())} señales")
        elif args.command == "add-period":
            period = store.add_period(
                platform=args.platform,
                program=args.program,
                period_start=args.period_start,
                period_end=args.period_end,
                currency=args.currency,
                estimated_net=args.estimated_net,
                approved_net=args.approved_net,
                status=args.status,
                source=args.source,
                notes=args.notes,
            )
            print(json.dumps(period.__dict__, ensure_ascii=False))
        elif args.command == "list-periods":
            items = store.load_periods()
            if args.json:
                print(json.dumps([item.__dict__ for item in items], ensure_ascii=False, indent=2))
            else:
                for item in items:
                    print(
                        f"{item.period_start} -> {item.period_end} | {item.program} | "
                        f"{item.status} | estimado {_money(item.estimated_net)} | "
                        f"aprobado {_money(item.approved_net)} | {item.currency}"
                    )
                print(f"Total: {len(items)} periodos")
        elif args.command == "add-payout":
            payout = store.add_payout(
                platform=args.platform,
                program=args.program,
                period_start=args.period_start,
                period_end=args.period_end,
                paid_at=args.paid_at,
                currency=args.currency,
                gross=args.gross,
                fee=args.fee,
                net=args.net,
                status=args.status,
                source=args.source,
                evidence=args.evidence,
                notes=args.notes,
            )
            print(json.dumps(payout.__dict__, ensure_ascii=False))
        elif args.command == "list-payouts":
            items = store.load_payouts()
            if args.json:
                print(json.dumps([item.__dict__ for item in items], ensure_ascii=False, indent=2))
            else:
                for item in items:
                    print(
                        f"{item.paid_at} | {item.program} | {item.status} | "
                        f"bruto {_money(item.gross)} | fee {_money(item.fee)} | neto {_money(item.net)} | {item.currency}"
                    )
                print(f"Total: {len(items)} payouts")
    except (ValueError, FileNotFoundError, OSError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
