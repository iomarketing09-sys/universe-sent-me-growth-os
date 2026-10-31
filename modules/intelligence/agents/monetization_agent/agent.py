"""Monetization Agent: reporte y conciliación read-only por tenant.

El agente no captura dinero ni cambia estados contables. Lee el ledger de
Monetization Lite, resume el umbral y cruza la evidencia de Meta disponible.
La aprobación de periodos y el registro de payouts siguen siendo manuales.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from modules.intelligence.monetization import MonetizationStore


def _project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[4]


def _money(value: Any) -> float:
    return round(float(value or 0), 2)


def _overlaps(
    start: Optional[str],
    end: Optional[str],
    since: Optional[str],
    until: Optional[str],
) -> bool:
    if since and end and end < since:
        return False
    if until and start and start > until:
        return False
    return True


class MonetizationAgent:
    """Resume y concilia la monetización de un tenant sin escribir en Meta."""

    def __init__(
        self,
        tenant_id: str = "universe",
        base_path: Optional[str] = None,
        store: Optional[MonetizationStore] = None,
    ):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path) if base_path else _project_root()
        self.tenant_path = self.base_path / "tenants" / tenant_id
        self.store = store or MonetizationStore(tenant_id, base_path=self.base_path)

    @property
    def evidence_dir(self) -> Path:
        return self.tenant_path / "metrics" / "monetization"

    def _periods(self, since: Optional[str], until: Optional[str]) -> List[Dict[str, Any]]:
        periods = [
            asdict(item)
            for item in self.store.load_periods()
            if _overlaps(item.period_start, item.period_end, since, until)
        ]
        return sorted(periods, key=lambda item: (item["period_end"], item["updated_at"]))

    def _payouts(self, since: Optional[str], until: Optional[str]) -> List[Dict[str, Any]]:
        payouts = [
            asdict(item)
            for item in self.store.load_payouts()
            if _overlaps(item.period_start, item.period_end, since, until)
        ]
        return sorted(payouts, key=lambda item: (item["paid_at"], item["payout_id"]))

    @staticmethod
    def _safe_json(path: Path) -> Dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        return payload if isinstance(payload, dict) else {}

    def _evidence_path(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.base_path))
        except ValueError:
            return str(path)

    def reconciliation(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Cruza app, API de página y suma por publicación cuando hay evidencia."""
        content_rows: List[Tuple[str, str, Dict[str, Any], Path]] = []
        post_rows: List[Tuple[str, str, Dict[str, Any], Path]] = []

        if self.evidence_dir.is_dir():
            for path in sorted(self.evidence_dir.glob("*.json")):
                payload = self._safe_json(path)
                start = str(payload.get("period_start") or "")
                end = str(payload.get("period_end") or "")
                if not _overlaps(start, end, since, until):
                    continue
                generated = str(payload.get("generated_at") or "")
                if payload.get("total_content_monetization_usd") is not None:
                    content_rows.append((end, generated, payload, path))
                if payload.get("post_level_content_earnings_usd") is not None:
                    post_rows.append((end, generated, payload, path))

        content = max(content_rows, key=lambda item: (item[0], item[1]), default=None)
        posts = max(post_rows, key=lambda item: (item[0], item[1]), default=None)
        if content is None and posts is None:
            return {
                "available": False,
                "content_earnings": None,
                "post_earnings": None,
                "differences": {},
                "warnings": [],
            }

        content_payload = content[2] if content else {}
        post_payload = posts[2] if posts else {}
        page_content = content_payload.get("total_content_monetization_usd")
        approximate = content_payload.get("total_approximate_earnings_usd")
        post_level = post_payload.get("post_level_content_earnings_usd")
        app_reported = (
            post_payload.get("app_reported_earnings_usd")
            or content_payload.get("app_reported_earnings_usd")
        )

        differences: Dict[str, float] = {}
        if app_reported is not None and page_content is not None:
            differences["app_vs_page_content"] = _money(float(app_reported) - float(page_content))
        if app_reported is not None and approximate is not None:
            differences["app_vs_approximate"] = _money(float(app_reported) - float(approximate))
        if page_content is not None and post_level is not None:
            differences["page_vs_post_level"] = _money(float(page_content) - float(post_level))

        warnings: List[str] = []
        app_gap = differences.get("app_vs_page_content", 0.0)
        if abs(app_gap) >= 0.01:
            warnings.append(
                f"App vs content_monetization_earnings difiere en ${abs(app_gap):.2f}."
            )
        post_gap = differences.get("page_vs_post_level", 0.0)
        if abs(post_gap) >= 0.01:
            warnings.append(
                f"El total de página vs suma por publicación difiere en ${abs(post_gap):.2f}."
            )

        return {
            "available": True,
            "content_earnings": (
                {
                    "path": self._evidence_path(content[3]),
                    "period_start": content_payload.get("period_start"),
                    "period_end": content_payload.get("period_end"),
                    "page_content_usd": page_content,
                    "approximate_usd": approximate,
                    "generated_at": content_payload.get("generated_at"),
                }
                if content
                else None
            ),
            "post_earnings": (
                {
                    "path": self._evidence_path(posts[3]),
                    "period_start": post_payload.get("period_start"),
                    "period_end": post_payload.get("period_end"),
                    "post_level_usd": post_level,
                    "app_reported_usd": app_reported,
                    "generated_at": post_payload.get("generated_at"),
                }
                if posts
                else None
            ),
            "differences": differences,
            "warnings": warnings,
        }

    def import_local_signals(self) -> Dict[str, Any]:
        """Importa JSON de señales y el log de cuenta sin salir a la red."""
        result: Dict[str, Any] = {"signals": {}, "account": {}, "errors": []}
        try:
            result["signals"] = self.store.import_signal_dir()
        except (OSError, ValueError) as exc:
            result["errors"].append(f"signals: {type(exc).__name__}: {exc}")
        try:
            result["account"] = self.store.import_account_log()
        except FileNotFoundError:
            result["account"] = {"rows": 0, "status": "not_configured"}
        except (OSError, ValueError) as exc:
            result["errors"].append(f"account: {type(exc).__name__}: {exc}")
        return result

    def report(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
        granularity: str = "monthly",
    ) -> Dict[str, Any]:
        report = self.store.report(granularity=granularity, since=since, until=until)
        report["periods"] = self._periods(since, until)
        report["payouts"] = self._payouts(since, until)
        report["reconciliation"] = self.reconciliation(since=since, until=until)
        report["agent"] = {
            "name": "monetization_agent",
            "mode": "read_only",
            "approval_required_for": ["approved", "paid", "payout"],
        }
        return report

    def summary(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> Dict[str, Any]:
        report = self.report(since=since, until=until)
        periods = report["periods"]
        payouts = report["payouts"]
        reconciliation = report["reconciliation"]
        warnings = list(report["data_quality"]["warnings"])
        warnings.extend(item for item in reconciliation["warnings"] if item not in warnings)
        threshold = report["money"].get("payout_threshold")
        configured = bool(
            periods or payouts or report["signals"]["rows"] or threshold
        )
        latest_period = periods[-1] if periods else None

        next_actions: List[str] = []
        if threshold:
            if threshold.get("reached"):
                next_actions.append("Revisar liberación del payout con Meta.")
            else:
                next_actions.append(
                    f"Faltan ${threshold['remaining']:.2f} {threshold['currency']} para el umbral."
                )
        if latest_period and latest_period["status"] == "estimated":
            next_actions.append(
                "Mantener el periodo como estimado hasta recibir statement o confirmación de pago."
            )
        if reconciliation["warnings"]:
            next_actions.append("Revisar la conciliación entre app, API y publicaciones.")

        return {
            "tenant_id": self.tenant_id,
            "configured": configured,
            "periods": len(periods),
            "payouts": len(payouts),
            "latest_period": latest_period,
            "money": report["money"],
            "signals": {
                "rows": report["signals"]["rows"],
                "unique_posts": report["signals"]["unique_posts"],
                "date_start": report["signals"]["date_start"],
                "date_end": report["signals"]["date_end"],
            },
            "reconciliation": reconciliation,
            "warnings": warnings,
            "next_actions": next_actions,
            "boundary": report["agent"],
            "paths": report.get("paths") or {},
        }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Monetization Agent (solo lectura)")
    parser.add_argument("tenant", nargs="?", default="universe")
    parser.add_argument("--since", default=None)
    parser.add_argument("--until", default=None)
    parser.add_argument("--full", action="store_true", help="Incluye el reporte completo")
    parser.add_argument("--base-path", default=None)
    args = parser.parse_args()

    agent = MonetizationAgent(args.tenant, base_path=args.base_path)
    payload = (
        agent.report(since=args.since, until=args.until)
        if args.full
        else agent.summary(since=args.since, until=args.until)
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
