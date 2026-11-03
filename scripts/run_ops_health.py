#!/usr/bin/env python3
"""CLI de salud y alertas de la operación compartida de Growth OS."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.operations.health import (  # noqa: E402
    DEFAULT_REGISTRY,
    DEFAULT_STATE_FILE,
    RegistryError,
    check_registry,
    format_alert,
    format_recovery,
    load_alert_state,
    load_registry,
    problem_fingerprint,
    save_alert_state,
    should_send_alert,
    status_exit_code,
)
from modules.operations.telegram import (  # noqa: E402
    TelegramError,
    load_telegram_config,
    send_message,
)


def _print_report(report: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print(f"Growth OS · Operación compartida: {str(report['status']).upper()}")
    for service in report["services"]:
        marker = {"ok": "OK", "warning": "WARN", "critical": "CRIT"}[service["status"]]
        print(f"[{marker}] {service['id']} · {service['name']}")
        for issue in service["issues"]:
            print(f"       - {issue['message']}")


def _notify(text: str) -> None:
    token, chat_id = load_telegram_config(ROOT)
    send_message(text, token=token, chat_id=chat_id)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Watchdog de operación compartida")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    parser.add_argument(
        "--notify",
        action="store_true",
        help="Envía alertas por Telegram cuando hay problemas",
    )
    parser.add_argument(
        "--test-telegram",
        action="store_true",
        help="Envía un mensaje de prueba y termina",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=DEFAULT_STATE_FILE,
        help="Estado local para cooldown de alertas",
    )
    parser.add_argument(
        "--cooldown-minutes",
        type=int,
        default=60,
        help="Tiempo mínimo entre alertas idénticas",
    )
    parser.add_argument(
        "--no-recovery",
        action="store_true",
        help="No envía aviso cuando el sistema se recupera",
    )
    args = parser.parse_args(argv)

    if args.test_telegram:
        try:
            _notify(
                "✅ Growth OS · Operación compartida\n"
                "Mensaje de prueba del canal de alertas. "
                "Si lo recibes, Telegram está configurado."
            )
        except TelegramError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print("Mensaje de prueba enviado a Telegram.")
        return 0

    try:
        registry = load_registry(args.registry)
    except RegistryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    report = check_registry(registry)
    _print_report(report, args.json)

    if args.notify:
        state = load_alert_state(args.state_file)
        if report["status"] == "ok":
            if state.get("active") and not args.no_recovery:
                try:
                    _notify(format_recovery(report))
                except TelegramError as exc:
                    print(f"ERROR al enviar recuperación: {exc}", file=sys.stderr)
                else:
                    save_alert_state(args.state_file, {})
        else:
            fingerprint = problem_fingerprint(report)
            now = datetime.now(timezone.utc)
            if should_send_alert(
                state,
                fingerprint,
                now=now,
                cooldown_minutes=max(0, args.cooldown_minutes),
            ):
                try:
                    _notify(format_alert(report))
                except TelegramError as exc:
                    print(f"ERROR al enviar alerta: {exc}", file=sys.stderr)
                else:
                    save_alert_state(
                        args.state_file,
                        {
                            "active": True,
                            "fingerprint": fingerprint,
                            "last_sent_at": now.isoformat(),
                        },
                    )
            else:
                print("Alerta idéntica en cooldown; no se reenvió.", file=sys.stderr)

    return status_exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main())
