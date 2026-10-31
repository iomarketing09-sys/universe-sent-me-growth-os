"""Monetization Lite: señales, periodos y payouts por tenant.

El módulo separa tres cosas que no deben mezclarse:

* ``MonetizationSignal``: observación diaria por publicación. Es una señal
  operativa (reacciones, comentarios, shares y un proxy de bonus), no ingreso.
* ``MonetizationPeriod``: estimado o aprobado por programa y periodo.
* ``Payout``: dinero realmente pagado, con bruto, fee y neto.

La única cifra que se reconoce como ingreso es el neto de un payout con estado
``paid``. El resto se reporta como pipeline o señal.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import statistics
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from zoneinfo import ZoneInfo

DEFAULT_PROGRAM = "meta_content_monetization"
DEFAULT_PLATFORM = "Facebook"
ACCOUNT_PUBLICATION_ID = "__account__"

SIGNAL_FIELDS = [
    "signal_id", "tenant_id", "platform", "program", "signal_date",
    "published_date", "captured_at_utc", "publication_id", "character",
    "series", "meme_text", "caption", "reactions", "comments", "shares",
    "bonus_points", "source", "evidence",
]

PERIOD_FIELDS = [
    "period_id", "tenant_id", "platform", "program", "period_start",
    "period_end", "currency", "estimated_net", "approved_net", "status",
    "source", "notes", "updated_at",
]

PAYOUT_FIELDS = [
    "payout_id", "tenant_id", "platform", "program", "period_start",
    "period_end", "paid_at", "currency", "gross", "fee", "net", "status",
    "source", "evidence", "notes", "created_at",
]

PERIOD_STATUSES = {"estimated", "approved", "paid", "reversed"}
PAYOUT_STATUSES = {"pending", "paid", "reversed"}


def _project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


def _money(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    return round(float(value), 2)


def _payout_threshold(config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Normaliza el umbral de payout configurado por tenant."""
    raw = (config.get("monetization") or {}).get("payout_threshold")
    if raw is None:
        raw = config.get("payout_threshold")
    if isinstance(raw, (int, float, str)):
        raw = {"amount": raw}
    if not isinstance(raw, dict):
        return None
    amount = _money(raw.get("amount"))
    if amount <= 0:
        return None
    return {
        "amount": amount,
        "currency": str(raw.get("currency") or "USD").upper(),
        "program": str(raw.get("program") or DEFAULT_PROGRAM),
        "platform": str(raw.get("platform") or DEFAULT_PLATFORM),
    }


def _to_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, dict):
        for key in ("value", "total_count", "count"):
            if key in value:
                return _to_int(value[key])
    try:
        return int(float(str(value or 0)))
    except (TypeError, ValueError):
        return 0


def _parse_datetime(value: Any) -> Optional[datetime]:
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value or "").strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            try:
                parsed = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _parse_date(value: Any) -> Optional[date]:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value).strip()[:10], "%Y-%m-%d").date()


def _stable_id(prefix: str, *parts: Any) -> str:
    key = "|".join(str(part or "") for part in parts)
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12].upper()
    return f"{prefix}-{digest}"


def _validate_status(value: str, valid: set[str], label: str) -> str:
    normalized = str(value or "").strip().lower()
    if normalized not in valid:
        raise ValueError(f"{label} inválido: {value}. Usa uno de: {', '.join(sorted(valid))}")
    return normalized


@dataclass
class MonetizationSignal:
    signal_id: str
    tenant_id: str
    platform: str
    program: str
    signal_date: str
    published_date: str = ""
    captured_at_utc: str = ""
    publication_id: str = ""
    character: str = ""
    series: str = ""
    meme_text: str = ""
    caption: str = ""
    reactions: int = 0
    comments: int = 0
    shares: int = 0
    bonus_points: int = 0
    source: str = ""
    evidence: str = ""


@dataclass
class MonetizationPeriod:
    period_id: str
    tenant_id: str
    platform: str
    program: str
    period_start: str
    period_end: str
    currency: str = "USD"
    estimated_net: float = 0.0
    approved_net: float = 0.0
    status: str = "estimated"
    source: str = "manual"
    notes: str = ""
    updated_at: str = ""


@dataclass
class Payout:
    payout_id: str
    tenant_id: str
    platform: str
    program: str
    period_start: str
    period_end: str
    paid_at: str
    currency: str = "USD"
    gross: float = 0.0
    fee: float = 0.0
    net: float = 0.0
    status: str = "paid"
    source: str = "manual"
    evidence: str = ""
    notes: str = ""
    created_at: str = ""


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.DictReader(handle) if any((v or "").strip() for v in row.values())]


def _write_csv(path: Path, rows: Iterable[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.tmp")
    with temp.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    os.replace(temp, path)


def _signal_from_row(row: Dict[str, str]) -> MonetizationSignal:
    return MonetizationSignal(
        signal_id=row.get("signal_id", ""),
        tenant_id=row.get("tenant_id", ""),
        platform=row.get("platform", DEFAULT_PLATFORM),
        program=row.get("program", DEFAULT_PROGRAM),
        signal_date=row.get("signal_date", ""),
        published_date=row.get("published_date", ""),
        captured_at_utc=row.get("captured_at_utc", ""),
        publication_id=row.get("publication_id", ""),
        character=row.get("character", ""),
        series=row.get("series", ""),
        meme_text=row.get("meme_text", ""),
        caption=row.get("caption", ""),
        reactions=_to_int(row.get("reactions")),
        comments=_to_int(row.get("comments")),
        shares=_to_int(row.get("shares")),
        bonus_points=_to_int(row.get("bonus_points")),
        source=row.get("source", ""),
        evidence=row.get("evidence", ""),
    )


def _period_from_row(row: Dict[str, str]) -> MonetizationPeriod:
    return MonetizationPeriod(
        period_id=row.get("period_id", ""),
        tenant_id=row.get("tenant_id", ""),
        platform=row.get("platform", DEFAULT_PLATFORM),
        program=row.get("program", DEFAULT_PROGRAM),
        period_start=row.get("period_start", ""),
        period_end=row.get("period_end", ""),
        currency=row.get("currency", "USD") or "USD",
        estimated_net=_money(row.get("estimated_net")),
        approved_net=_money(row.get("approved_net")),
        status=row.get("status", "estimated") or "estimated",
        source=row.get("source", ""),
        notes=row.get("notes", ""),
        updated_at=row.get("updated_at", ""),
    )


def _payout_from_row(row: Dict[str, str]) -> Payout:
    return Payout(
        payout_id=row.get("payout_id", ""),
        tenant_id=row.get("tenant_id", ""),
        platform=row.get("platform", DEFAULT_PLATFORM),
        program=row.get("program", DEFAULT_PROGRAM),
        period_start=row.get("period_start", ""),
        period_end=row.get("period_end", ""),
        paid_at=row.get("paid_at", ""),
        currency=row.get("currency", "USD") or "USD",
        gross=_money(row.get("gross")),
        fee=_money(row.get("fee")),
        net=_money(row.get("net")),
        status=row.get("status", "paid") or "paid",
        source=row.get("source", ""),
        evidence=row.get("evidence", ""),
        notes=row.get("notes", ""),
        created_at=row.get("created_at", ""),
    )


def load_contexts(path: Path) -> Dict[str, Dict[str, Any]]:
    """Carga publication_contexts.json y acepta IDs completos o cortos."""
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    contexts: Dict[str, Dict[str, Any]] = {}
    for key, value in (raw.items() if isinstance(raw, dict) else []):
        if not isinstance(value, dict):
            continue
        full = str(value.get("publication_id") or key)
        contexts[full] = value
        if "_" in full:
            contexts.setdefault(full.split("_", 1)[1], value)
    return contexts


def _derive_series(context: Optional[Dict[str, Any]]) -> Tuple[str, str]:
    raw = str((context or {}).get("character") or "").strip()
    if raw.lower().startswith("existencial"):
        return "Existencial", "Universe"
    if raw.lower().startswith("si la memoria falla"):
        return "Si la memoria falla", "Universe"
    if not raw:
        return "sin_serie", "sin_personaje"
    return raw, raw


def _context_for(publication_id: str, contexts: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    context = contexts.get(publication_id)
    if context:
        return context
    if "_" in publication_id:
        return contexts.get(publication_id.split("_", 1)[1])
    return None


class MonetizationStore:
    """Ledger CSV aislado por tenant."""

    def __init__(self, tenant_id: str, base_path: Optional[Path] = None):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path) if base_path else _project_root()
        self.tenant_dir = self.base_path / "tenants" / tenant_id
        if not (self.tenant_dir / "config.json").is_file():
            raise FileNotFoundError(f"No existe tenants/{tenant_id}/config.json")
        self.data_dir = self.tenant_dir / "data" / "monetization"
        self.signals_path = self.data_dir / "signals.csv"
        self.periods_path = self.data_dir / "periods.csv"
        self.payouts_path = self.data_dir / "payouts.csv"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            return json.loads((self.tenant_dir / "config.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def load_signals(self) -> List[MonetizationSignal]:
        return [_signal_from_row(row) for row in _read_csv(self.signals_path) if row.get("signal_id")]

    def save_signals(self, signals: Iterable[MonetizationSignal]) -> None:
        rows = [asdict(item) for item in signals]
        rows.sort(key=lambda row: (row["signal_date"], row["publication_id"], row["signal_id"]))
        _write_csv(self.signals_path, rows, SIGNAL_FIELDS)

    def upsert_signals(self, signals: Iterable[MonetizationSignal]) -> Dict[str, int]:
        existing = {item.signal_id: item for item in self.load_signals()}
        inserted = updated = unchanged = 0
        for signal in signals:
            current = existing.get(signal.signal_id)
            if current is None:
                existing[signal.signal_id] = signal
                inserted += 1
            elif asdict(current) != asdict(signal):
                existing[signal.signal_id] = signal
                updated += 1
            else:
                unchanged += 1
        if inserted or updated:
            self.save_signals(existing.values())
        return {"inserted": inserted, "updated": updated, "unchanged": unchanged}

    def _signal_from_post(
        self,
        post: Dict[str, Any],
        signal_date: str,
        contexts: Dict[str, Dict[str, Any]],
        program: str,
        platform: str,
        evidence: str,
    ) -> MonetizationSignal:
        publication_id = str(post.get("post_id") or "").strip()
        context = _context_for(publication_id, contexts)
        series, character = _derive_series(context)
        reactions = _to_int(post.get("reactions"))
        comments = _to_int(post.get("comments"))
        shares = _to_int(post.get("shares"))
        bonus = _to_int(post.get("bonus_points"))
        if bonus == 0 and (reactions or comments or shares):
            bonus = reactions + comments * 2 + shares * 3
        published_date = str(post.get("date") or "")
        if context and context.get("published_at"):
            parsed = _parse_datetime(context.get("published_at"))
            if parsed:
                published_date = parsed.date().isoformat()
        return MonetizationSignal(
            signal_id=_stable_id("MS", self.tenant_id, platform, program, signal_date, publication_id),
            tenant_id=self.tenant_id,
            platform=platform,
            program=program,
            signal_date=signal_date,
            published_date=published_date,
            captured_at_utc=f"{signal_date}T00:00:00+00:00",
            publication_id=publication_id,
            character=character,
            series=series,
            meme_text=str((context or {}).get("meme_text") or post.get("preview") or ""),
            caption=str((context or {}).get("caption") or ""),
            reactions=reactions,
            comments=comments,
            shares=shares,
            bonus_points=bonus,
            source="meta_monetization_json",
            evidence=evidence,
        )

    def import_signal_file(
        self,
        path: Path,
        contexts: Optional[Dict[str, Dict[str, Any]]] = None,
        program: str = DEFAULT_PROGRAM,
        platform: str = DEFAULT_PLATFORM,
    ) -> Dict[str, int]:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        signal_date = str(payload.get("date") or "")
        if not signal_date:
            match = re.match(r"(\d{4}-\d{2}-\d{2})", Path(path).name)
            if not match:
                raise ValueError(f"No se pudo inferir la fecha de {path}")
            signal_date = match.group(1)
        context_map = contexts if contexts is not None else load_contexts(
            self.tenant_dir / "publication_contexts.json"
        )
        evidence = str(Path(path).resolve())
        try:
            evidence = str(Path(path).resolve().relative_to(self.base_path))
        except ValueError:
            pass
        signals = [
            self._signal_from_post(post, signal_date, context_map, program, platform, evidence)
            for post in payload.get("posts", [])
            if post.get("post_id")
        ]
        result = self.upsert_signals(signals)
        result["rows"] = len(signals)
        result["file"] = str(path)
        return result

    def import_signal_dir(
        self,
        input_dir: Optional[Path] = None,
        contexts_path: Optional[Path] = None,
        program: str = DEFAULT_PROGRAM,
        platform: str = DEFAULT_PLATFORM,
    ) -> Dict[str, int]:
        directory = Path(input_dir) if input_dir else self.tenant_dir / "metrics" / "monetization"
        context_path = Path(contexts_path) if contexts_path else self.tenant_dir / "publication_contexts.json"
        contexts = load_contexts(context_path)
        files = sorted(directory.glob("*.json"))
        signals: List[MonetizationSignal] = []
        for path in files:
            payload = json.loads(path.read_text(encoding="utf-8"))
            signal_date = str(payload.get("date") or "")
            if not signal_date:
                match = re.match(r"(\d{4}-\d{2}-\d{2})", path.name)
                if not match:
                    continue
                signal_date = match.group(1)
            evidence = str(path.resolve())
            try:
                evidence = str(path.resolve().relative_to(self.base_path))
            except ValueError:
                pass
            signals.extend(
                self._signal_from_post(post, signal_date, contexts, program, platform, evidence)
                for post in payload.get("posts", [])
                if post.get("post_id")
            )
        result = self.upsert_signals(signals)
        result.update({"files": len(files), "rows": len(signals)})
        return result

    def import_account_log(
        self,
        path: Optional[Path] = None,
        program: str = DEFAULT_PROGRAM,
        platform: str = DEFAULT_PLATFORM,
    ) -> Dict[str, int]:
        """Importa el log diario de cuenta sin confundirlo con posts.

        El log de Meta es un agregado diario de la cuenta, no un snapshot
        acumulado por publicación. Por eso cada fecha genera una sola señal de
        cuenta y las filas repetidas se colapsan conservando la última captura.
        """

        log_path = Path(path) if path else self.tenant_dir / "metrics" / "meta_monetization_log.csv"
        if not log_path.is_file():
            raise FileNotFoundError(f"No existe el log de cuenta: {log_path}")
        meta_config = self.config.get("meta") or {}
        business_id = str(
            meta_config.get("business_id") or self.config.get("business_id") or ""
        ).strip()
        with log_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))

        by_date: Dict[str, Dict[str, str]] = {}
        skipped = 0
        for row in rows:
            row_business = str(row.get("Business_ID") or "").strip()
            if business_id and row_business and row_business != business_id:
                skipped += 1
                continue
            signal_date = _parse_date(row.get("Fecha"))
            if signal_date is None:
                continue
            by_date[signal_date.isoformat()] = row

        evidence = str(log_path.resolve())
        try:
            evidence = str(log_path.resolve().relative_to(self.base_path))
        except ValueError:
            pass

        signals: List[MonetizationSignal] = []
        for signal_date, row in sorted(by_date.items()):
            reactions = _to_int(row.get("Reacciones"))
            comments = _to_int(row.get("Comentarios"))
            shares = _to_int(row.get("Shares"))
            bonus = _to_int(row.get("Interacciones_Bonus_Elegibles"))
            if bonus == 0 and (reactions or comments or shares):
                bonus = reactions + comments * 2 + shares * 3
            signals.append(MonetizationSignal(
                signal_id=_stable_id(
                    "MS", self.tenant_id, platform, program, signal_date, ACCOUNT_PUBLICATION_ID
                ),
                tenant_id=self.tenant_id,
                platform=platform,
                program=program,
                signal_date=signal_date,
                captured_at_utc=f"{signal_date}T00:00:00+00:00",
                publication_id=ACCOUNT_PUBLICATION_ID,
                character="Cuenta",
                series="Cuenta",
                meme_text="Agregado diario de cuenta",
                caption=f"Posts analizados: {_to_int(row.get('Posts_Analizados'))}",
                reactions=reactions,
                comments=comments,
                shares=shares,
                bonus_points=bonus,
                source="meta_monetization_log",
                evidence=evidence,
            ))

        result = self.upsert_signals(signals)
        result.update({
            "rows": len(signals),
            "source_rows": len(rows),
            "duplicates_collapsed": len(rows) - skipped - len(signals),
            "skipped_other_business": skipped,
        })
        return result

    def load_periods(self) -> List[MonetizationPeriod]:
        return [_period_from_row(row) for row in _read_csv(self.periods_path) if row.get("period_id")]

    def save_periods(self, periods: Iterable[MonetizationPeriod]) -> None:
        rows = [asdict(item) for item in periods]
        rows.sort(key=lambda row: (row["period_start"], row["period_end"], row["period_id"]))
        _write_csv(self.periods_path, rows, PERIOD_FIELDS)

    def add_period(
        self,
        *,
        platform: str,
        program: str,
        period_start: str,
        period_end: str,
        currency: str = "USD",
        estimated_net: float = 0.0,
        approved_net: float = 0.0,
        status: str = "estimated",
        source: str = "manual",
        notes: str = "",
    ) -> MonetizationPeriod:
        start = _parse_date(period_start)
        end = _parse_date(period_end)
        if start is None or end is None or start > end:
            raise ValueError("El periodo requiere fechas válidas y period_start <= period_end")
        normalized_status = _validate_status(status, PERIOD_STATUSES, "Estado del periodo")
        estimated_net = _money(estimated_net)
        approved_net = _money(approved_net)
        if estimated_net < 0 or approved_net < 0:
            raise ValueError("Los montos del periodo no pueden ser negativos")
        period = MonetizationPeriod(
            period_id=_stable_id(
                "MP", self.tenant_id, platform, program, start.isoformat(), end.isoformat()
            ),
            tenant_id=self.tenant_id,
            platform=platform,
            program=program,
            period_start=start.isoformat(),
            period_end=end.isoformat(),
            currency=currency or "USD",
            estimated_net=estimated_net,
            approved_net=approved_net,
            status=normalized_status,
            source=source,
            notes=notes,
            updated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        periods = {item.period_id: item for item in self.load_periods()}
        periods[period.period_id] = period
        self.save_periods(periods.values())
        return period

    def load_payouts(self) -> List[Payout]:
        return [_payout_from_row(row) for row in _read_csv(self.payouts_path) if row.get("payout_id")]

    def payout_threshold(self) -> Optional[Dict[str, Any]]:
        return _payout_threshold(self.config)

    def save_payouts(self, payouts: Iterable[Payout]) -> None:
        rows = [asdict(item) for item in payouts]
        rows.sort(key=lambda row: (row["paid_at"], row["payout_id"]))
        _write_csv(self.payouts_path, rows, PAYOUT_FIELDS)

    def add_payout(
        self,
        *,
        platform: str,
        program: str,
        period_start: str,
        period_end: str,
        paid_at: str,
        currency: str = "USD",
        gross: float = 0.0,
        fee: float = 0.0,
        net: Optional[float] = None,
        status: str = "paid",
        source: str = "manual",
        evidence: str = "",
        notes: str = "",
        payout_id: Optional[str] = None,
    ) -> Payout:
        start = _parse_date(period_start)
        end = _parse_date(period_end)
        paid = _parse_date(paid_at)
        if start is None or end is None or paid is None or start > end:
            raise ValueError("El payout requiere fechas válidas y period_start <= period_end")
        normalized_status = _validate_status(status, PAYOUT_STATUSES, "Estado del payout")
        gross = _money(gross)
        fee = _money(fee)
        if net is None:
            net = gross - fee
        net = _money(net)
        if min(gross, fee, net) < 0:
            raise ValueError("Los montos del payout no pueden ser negativos")
        payout = Payout(
            payout_id=payout_id or _stable_id(
                "PAY", self.tenant_id, platform, program, start.isoformat(),
                end.isoformat(), paid.isoformat(),
            ),
            tenant_id=self.tenant_id,
            platform=platform,
            program=program,
            period_start=start.isoformat(),
            period_end=end.isoformat(),
            paid_at=paid.isoformat(),
            currency=currency or "USD",
            gross=gross,
            fee=fee,
            net=net,
            status=normalized_status,
            source=source,
            evidence=evidence,
            notes=notes,
            created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        payouts = {item.payout_id: item for item in self.load_payouts()}
        payouts[payout.payout_id] = payout
        self.save_payouts(payouts.values())
        return payout

    def _publication_log(self) -> Dict[str, Dict[str, str]]:
        path = self.tenant_dir / "publication_log_week2.csv"
        if not path.is_file():
            return {}
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return {row.get("publication_id", ""): row for row in csv.DictReader(handle) if row.get("publication_id")}

    def _published_local(
        self,
        signal: MonetizationSignal,
        contexts: Dict[str, Dict[str, Any]],
        publication_log: Dict[str, Dict[str, str]],
    ) -> Optional[datetime]:
        tz = ZoneInfo(str(self.config.get("timezone") or "UTC"))
        context = _context_for(signal.publication_id, contexts)
        raw = (context or {}).get("published_at")
        parsed = _parse_datetime(raw)
        if parsed:
            return parsed.astimezone(tz)
        log = publication_log.get(signal.publication_id)
        if log and log.get("date") and log.get("time"):
            try:
                return datetime.fromisoformat(f"{log['date']}T{log['time']}").replace(tzinfo=tz)
            except ValueError:
                pass
        if signal.published_date:
            try:
                return datetime.fromisoformat(signal.published_date).replace(tzinfo=tz)
            except ValueError:
                pass
        return None

    def report(
        self,
        granularity: str = "daily",
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> Dict[str, Any]:
        signals = self.load_signals()
        if since:
            signals = [item for item in signals if item.signal_date >= since]
        if until:
            signals = [item for item in signals if item.signal_date <= until]
        periods = self.load_periods()
        payouts = self.load_payouts()
        if since:
            periods = [item for item in periods if item.period_end >= since]
            payouts = [item for item in payouts if item.period_end >= since]
        if until:
            periods = [item for item in periods if item.period_start <= until]
            payouts = [item for item in payouts if item.period_start <= until]
        contexts_path = self.tenant_dir / "publication_contexts.json"
        contexts = load_contexts(contexts_path)
        report = summarize_monetization(
            signals,
            periods=periods,
            payouts=payouts,
            contexts=contexts,
            publication_log=self._publication_log(),
            tenant_id=self.tenant_id,
            granularity=granularity,
            timezone_name=str(self.config.get("timezone") or "UTC"),
            payout_threshold=self.payout_threshold(),
        )
        report["paths"] = {
            "signals": str(self.signals_path),
            "periods": str(self.periods_path),
            "payouts": str(self.payouts_path),
        }
        return report


def _increments(signals: List[MonetizationSignal]) -> List[Dict[str, Any]]:
    by_publication: Dict[str, List[MonetizationSignal]] = defaultdict(list)
    for signal in signals:
        by_publication[signal.publication_id].append(signal)
    increments: List[Dict[str, Any]] = []
    for publication_id, items in by_publication.items():
        items.sort(key=lambda item: (item.signal_date, item.captured_at_utc, item.signal_id))
        previous: Optional[MonetizationSignal] = None
        for signal in items:
            if previous is None:
                delta_bonus = signal.bonus_points
                delta_reactions = signal.reactions
                delta_comments = signal.comments
                delta_shares = signal.shares
                initial = True
            else:
                delta_bonus = signal.bonus_points - previous.bonus_points
                delta_reactions = signal.reactions - previous.reactions
                delta_comments = signal.comments - previous.comments
                delta_shares = signal.shares - previous.shares
                initial = False
            increments.append({
                "signal_date": signal.signal_date,
                "publication_id": publication_id,
                "bonus_points": delta_bonus,
                "reactions": delta_reactions,
                "comments": delta_comments,
                "shares": delta_shares,
                "initial": initial,
                "correction": not initial and (
                    delta_bonus < 0 or delta_reactions < 0 or delta_comments < 0 or delta_shares < 0
                ),
            })
            previous = signal
    return increments


def _period_key(value: str, granularity: str) -> str:
    parsed = date.fromisoformat(value)
    if granularity == "weekly":
        iso = parsed.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"
    if granularity == "monthly":
        return parsed.strftime("%Y-%m")
    return parsed.isoformat()


def _aggregate_increments(rows: List[Dict[str, Any]], granularity: str) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        key = _period_key(row["signal_date"], granularity)
        entry = grouped.setdefault(key, {
            "period": key, "bonus_points": 0, "reactions": 0, "comments": 0,
            "shares": 0, "observations": 0, "initial_observations": 0,
            "corrections": 0,
            "publications": set(),
        })
        entry["bonus_points"] += row["bonus_points"]
        entry["reactions"] += row["reactions"]
        entry["comments"] += row["comments"]
        entry["shares"] += row["shares"]
        entry["observations"] += 1
        if row["initial"]:
            entry["initial_observations"] += 1
        if row["correction"]:
            entry["corrections"] += 1
        entry["publications"].add(row["publication_id"])
    result = []
    for key in sorted(grouped):
        entry = grouped[key]
        entry["publications"] = len(entry["publications"])
        result.append(entry)
    return result


def _group_latest(
    latest: List[MonetizationSignal],
    key_fn,
    timezone_name: str,
    contexts: Dict[str, Dict[str, Any]],
    publication_log: Dict[str, Dict[str, str]],
) -> Dict[str, Dict[str, Any]]:
    tz = ZoneInfo(timezone_name or "UTC")
    grouped: Dict[str, List[MonetizationSignal]] = defaultdict(list)
    for signal in latest:
        grouped[key_fn(signal, tz, contexts, publication_log)].append(signal)
    result: Dict[str, Dict[str, Any]] = {}
    for key, items in grouped.items():
        bonus = [item.bonus_points for item in items]
        reactions = sum(item.reactions for item in items)
        comments = sum(item.comments for item in items)
        shares = sum(item.shares for item in items)
        total_interactions = reactions + comments + shares
        result[key] = {
            "posts": len(items),
            "bonus_points": sum(bonus),
            "median_bonus": round(statistics.median(bonus), 2) if bonus else 0.0,
            "reactions": reactions,
            "comments": comments,
            "shares": shares,
            "share_rate": round(shares / total_interactions, 4) if total_interactions else 0.0,
        }
    return dict(sorted(result.items(), key=lambda item: item[1]["median_bonus"], reverse=True))


def _account_daily(signals: List[MonetizationSignal]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for signal in signals:
        entry = grouped.setdefault(signal.signal_date, {
            "period": signal.signal_date,
            "bonus_points": 0,
            "reactions": 0,
            "comments": 0,
            "shares": 0,
            "observations": 0,
        })
        entry["bonus_points"] += signal.bonus_points
        entry["reactions"] += signal.reactions
        entry["comments"] += signal.comments
        entry["shares"] += signal.shares
        entry["observations"] += 1
    return [grouped[key] for key in sorted(grouped)]


def summarize_monetization(
    signals: List[MonetizationSignal],
    *,
    periods: Optional[List[MonetizationPeriod]] = None,
    payouts: Optional[List[Payout]] = None,
    contexts: Optional[Dict[str, Dict[str, Any]]] = None,
    publication_log: Optional[Dict[str, Dict[str, str]]] = None,
    tenant_id: Optional[str] = None,
    granularity: str = "daily",
    timezone_name: str = "UTC",
    payout_threshold: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    periods = periods or []
    payouts = payouts or []
    contexts = contexts or {}
    publication_log = publication_log or {}
    tz = ZoneInfo(timezone_name or "UTC")

    account_signals = [
        signal for signal in signals if signal.publication_id == ACCOUNT_PUBLICATION_ID
    ]
    signals = [
        signal for signal in signals if signal.publication_id != ACCOUNT_PUBLICATION_ID
    ]
    total_signal_rows = len(signals) + len(account_signals)

    by_publication: Dict[str, List[MonetizationSignal]] = defaultdict(list)
    for signal in signals:
        by_publication[signal.publication_id].append(signal)
    latest = [
        max(items, key=lambda item: (item.signal_date, item.captured_at_utc, item.signal_id))
        for items in by_publication.values()
        if items
    ]
    increments = _increments(signals)
    daily = _aggregate_increments(increments, "daily")
    weekly = _aggregate_increments(increments, "weekly")
    monthly = _aggregate_increments(increments, "monthly")

    def published_at(signal: MonetizationSignal) -> Optional[datetime]:
        context = _context_for(signal.publication_id, contexts)
        parsed = _parse_datetime((context or {}).get("published_at"))
        if parsed:
            return parsed.astimezone(tz)
        log = publication_log.get(signal.publication_id)
        if log and log.get("date") and log.get("time"):
            try:
                return datetime.fromisoformat(f"{log['date']}T{log['time']}").replace(tzinfo=tz)
            except ValueError:
                pass
        if signal.published_date:
            try:
                return datetime.fromisoformat(signal.published_date).replace(tzinfo=tz)
            except ValueError:
                pass
        return None

    def series_key(signal, tz, contexts, log):
        return signal.series or "sin_serie"

    def character_key(signal, tz, contexts, log):
        return signal.character or "sin_personaje"

    def slot_key(signal, tz, contexts, log):
        value = published_at(signal)
        return value.strftime("%H:00") if value else "sin_hora"

    def weekday_key(signal, tz, contexts, log):
        value = published_at(signal)
        return value.strftime("%A") if value else "sin_fecha"

    latest_rows = []
    for signal in latest:
        value = published_at(signal)
        latest_rows.append({
            "publication_id": signal.publication_id,
            "series": signal.series,
            "character": signal.character,
            "meme_text": signal.meme_text,
            "published_at": value.isoformat(timespec="seconds") if value else "",
            "signal_date": signal.signal_date,
            "reactions": signal.reactions,
            "comments": signal.comments,
            "shares": signal.shares,
            "bonus_points": signal.bonus_points,
        })
    latest_rows.sort(key=lambda row: row["bonus_points"], reverse=True)

    signal_dates = sorted({signal.signal_date for signal in signals if signal.signal_date})
    all_signal_dates = sorted({
        signal.signal_date for signal in [*signals, *account_signals] if signal.signal_date
    })
    latest_signal_date = signal_dates[-1] if signal_dates else None
    latest_any_signal_date = all_signal_dates[-1] if all_signal_dates else None
    latest_age_days = None
    latest_post_age_days = None
    if latest_any_signal_date:
        latest_age_days = (date.today() - date.fromisoformat(latest_any_signal_date)).days
    if latest_signal_date:
        latest_post_age_days = (date.today() - date.fromisoformat(latest_signal_date)).days

    account_daily = _account_daily(account_signals)
    account_latest = max(
        account_signals,
        key=lambda item: (item.signal_date, item.captured_at_utc, item.signal_id),
        default=None,
    )
    account_age_days = None
    if account_latest:
        account_age_days = (date.today() - date.fromisoformat(account_latest.signal_date)).days

    estimated_net = round(sum(p.estimated_net for p in periods if p.status == "estimated"), 2)
    paid_by_period: Dict[Tuple[str, str, str, str, str], float] = defaultdict(float)
    for payout in payouts:
        if payout.status == "paid":
            paid_by_period[(
                payout.tenant_id, payout.platform, payout.program,
                payout.period_start, payout.period_end,
            )] += payout.net
    approved_net = round(
        sum(
            max(
                p.approved_net - paid_by_period.get(
                    (p.tenant_id, p.platform, p.program, p.period_start, p.period_end), 0.0
                ),
                0.0,
            )
            for p in periods
            if p.status == "approved"
        ),
        2,
    )
    paid_net = round(sum(p.net for p in payouts if p.status == "paid"), 2)
    pipeline_net = round(estimated_net + approved_net, 2)

    threshold_summary = None
    if payout_threshold:
        threshold_amount = _money(payout_threshold.get("amount"))
        threshold_currency = str(payout_threshold.get("currency") or "USD").upper()
        threshold_program = str(payout_threshold.get("program") or DEFAULT_PROGRAM)
        threshold_platform = str(payout_threshold.get("platform") or DEFAULT_PLATFORM)
        threshold_paid: Dict[Tuple[str, str, str, str, str, str], float] = defaultdict(float)
        for payout in payouts:
            if payout.status == "paid" and payout.currency.upper() == threshold_currency:
                threshold_paid[(
                    payout.tenant_id, payout.platform, payout.program,
                    payout.period_start, payout.period_end, payout.currency.upper(),
                )] += payout.net
        current_balance = 0.0
        for period in periods:
            if (
                period.platform != threshold_platform
                or period.program != threshold_program
                or period.currency.upper() != threshold_currency
            ):
                continue
            if period.status == "estimated":
                current_balance += period.estimated_net
            elif period.status == "approved":
                current_balance += max(
                    period.approved_net - threshold_paid.get((
                        period.tenant_id, period.platform, period.program,
                        period.period_start, period.period_end, period.currency.upper(),
                    ), 0.0),
                    0.0,
                )
        current_balance = round(current_balance, 2)
        remaining = round(max(threshold_amount - current_balance, 0.0), 2)
        threshold_summary = {
            "amount": threshold_amount,
            "currency": threshold_currency,
            "platform": threshold_platform,
            "program": threshold_program,
            "current_balance": current_balance,
            "remaining": remaining,
            "reached": remaining <= 0,
            "source": "config",
            "note": "Saldo pendiente = periodos estimados + aprobados sin pagar; excluye payouts ya pagados.",
        }

    by_program: Dict[str, Dict[str, Any]] = {}
    for period in periods:
        entry = by_program.setdefault(period.program, {"estimated_net": 0.0, "approved_unpaid_net": 0.0, "paid_net": 0.0})
        if period.status == "estimated":
            entry["estimated_net"] += period.estimated_net
        elif period.status == "approved":
            entry["approved_unpaid_net"] += max(
                period.approved_net - paid_by_period.get(
                    (period.tenant_id, period.platform, period.program, period.period_start, period.period_end), 0.0
                ),
                0.0,
            )
    for payout in payouts:
        entry = by_program.setdefault(payout.program, {"estimated_net": 0.0, "approved_unpaid_net": 0.0, "paid_net": 0.0})
        if payout.status == "paid":
            entry["paid_net"] += payout.net
    for entry in by_program.values():
        for key in entry:
            entry[key] = round(entry[key], 2)

    payout_rows = [p for p in payouts if p.status == "paid"]
    payout_summary = {
        "count": len(payout_rows),
        "gross": round(sum(p.gross for p in payout_rows), 2),
        "fee": round(sum(p.fee for p in payout_rows), 2),
        "net": round(sum(p.net for p in payout_rows), 2),
        "last_paid_at": max((p.paid_at for p in payout_rows), default=None),
        "by_status": {
            status: sum(1 for p in payouts if p.status == status)
            for status in sorted({p.status for p in payouts})
        },
    }

    period_ids_with_payout = {
        _stable_id("MP", p.tenant_id, p.platform, p.program, p.period_start, p.period_end)
        for p in payouts
        if p.status == "paid"
    }
    warnings: List[str] = []
    paid_without_payout = [
        p.period_id for p in periods
        if p.status == "paid" and p.period_id not in period_ids_with_payout
    ]
    if paid_without_payout:
        warnings.append(f"{len(paid_without_payout)} periodos marcados paid sin payout confirmado")
    if latest_age_days is not None and latest_age_days > 2:
        warnings.append(f"La última señal tiene {latest_age_days} días")
    if any(abs(p.net - (p.gross - p.fee)) > 0.01 for p in payouts):
        warnings.append("Hay payouts donde net != gross - fee")
    missing_series = sum(1 for item in latest if (item.series or "sin_serie") == "sin_serie")
    if missing_series:
        warnings.append(f"{missing_series} posts sin contexto/serie; el desglose por serie está incompleto")
    if not payout_rows:
        warnings.append("Sin payout confirmado: no hay ingreso reconocido")
    incremental_total = sum(row["bonus_points"] for row in increments)
    if incremental_total != sum(item.bonus_points for item in latest):
        warnings.append("El bonus incremental no reconcilia con el acumulado por post")

    signal_ids = [signal.signal_id for signal in [*signals, *account_signals]]
    return {
        "tenant_id": tenant_id,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "granularity": granularity,
        "signals": {
            "rows": total_signal_rows,
            "post_rows": len(signals),
            "account_rows": len(account_signals),
            "unique_posts": len(latest),
            "date_start": all_signal_dates[0] if all_signal_dates else None,
            "date_end": latest_any_signal_date,
            "latest_post_signal_date": latest_signal_date,
            "latest_post_signal_age_days": latest_post_age_days,
            "latest_signal_age_days": latest_age_days,
            "latest_bonus_points": sum(item.bonus_points for item in latest),
            "latest_reactions": sum(item.reactions for item in latest),
            "latest_comments": sum(item.comments for item in latest),
            "latest_shares": sum(item.shares for item in latest),
            "incremental_bonus_points": incremental_total,
            "increments": {"daily": daily, "weekly": weekly, "monthly": monthly},
            "account": {
                "date_start": account_daily[0]["period"] if account_daily else None,
                "date_end": account_daily[-1]["period"] if account_daily else None,
                "latest_signal_age_days": account_age_days,
                "latest_bonus_points": account_latest.bonus_points if account_latest else 0,
                "latest_reactions": account_latest.reactions if account_latest else 0,
                "latest_comments": account_latest.comments if account_latest else 0,
                "latest_shares": account_latest.shares if account_latest else 0,
                "daily_bonus_points": sum(row["bonus_points"] for row in account_daily),
                "daily": account_daily,
            },
        },
        "money": {
            "currency_note": "Los periodos y payouts pueden tener monedas distintas; no se convierten.",
            "estimated_net": estimated_net,
            "approved_unpaid_net": approved_net,
            "pipeline_net": pipeline_net,
            "paid_net": paid_net,
            "recognized_net": paid_net,
            "payouts": payout_summary,
            "payout_threshold": threshold_summary,
            "by_program": by_program,
        },
        "by_series": _group_latest(latest, series_key, timezone_name, contexts, publication_log),
        "by_character": _group_latest(latest, character_key, timezone_name, contexts, publication_log),
        "by_slot": _group_latest(latest, slot_key, timezone_name, contexts, publication_log),
        "by_weekday": _group_latest(latest, weekday_key, timezone_name, contexts, publication_log),
        "top_posts": latest_rows[:10],
        "bottom_posts": latest_rows[-5:],
        "data_quality": {
            "signal_is_proxy": True,
            "signals_without_publication_id": sum(1 for item in signals if not item.publication_id),
            "signals_without_character": sum(1 for item in signals if not item.character),
            "latest_posts_without_series": missing_series,
            "duplicate_signal_ids": len(signal_ids) - len(set(signal_ids)),
            "periods_paid_without_payout": paid_without_payout,
            "payout_net_mismatch": sum(1 for p in payouts if abs(p.net - (p.gross - p.fee)) > 0.01),
            "warnings": warnings,
        },
    }
