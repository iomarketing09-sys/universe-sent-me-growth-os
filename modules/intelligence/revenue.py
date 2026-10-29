"""Revenue Lite para tenants de producto.

El MVP usa un CSV por tenant para no mezclar PII con la base de contenido.
``amount`` es el monto cotizado y ``amount_collected`` es el dinero realmente
recibido. El ingreso se reconoce solo en ``anticipo`` y ``cobrado``; al pasar
de anticipo a cobrado se reemplaza el monto, nunca se suma dos veces.
"""

from __future__ import annotations

import csv
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import ValidationError

from growthos.core.enums import DealStage, LeadSource, PaymentStatus
from growthos.core.models import Deal


REVENUE_STATUSES = {PaymentStatus.ANTICIPO.value, PaymentStatus.COBRADO.value}

SOURCE_ALIASES = {
    "ig": LeadSource.INSTAGRAM.value,
    "instagram": LeadSource.INSTAGRAM.value,
    "fb": LeadSource.FACEBOOK.value,
    "facebook": LeadSource.FACEBOOK.value,
    "wa": LeadSource.WHATSAPP.value,
    "whatsapp": LeadSource.WHATSAPP.value,
    "meta": LeadSource.META_ADS.value,
    "meta_ads": LeadSource.META_ADS.value,
    "google": LeadSource.GOOGLE_ADS.value,
    "google_ads": LeadSource.GOOGLE_ADS.value,
    "referral": LeadSource.REFERRAL.value,
    "referido": LeadSource.REFERRAL.value,
    "direct": LeadSource.DIRECT.value,
    "directo": LeadSource.DIRECT.value,
    "tienda": LeadSource.STORE.value,
    "store": LeadSource.STORE.value,
}

STAGE_ALIASES = {
    "nuevo": DealStage.NEW.value,
    "new": DealStage.NEW.value,
    "calificado": DealStage.QUALIFIED.value,
    "qualified": DealStage.QUALIFIED.value,
    "cotizado": DealStage.PROPOSAL.value,
    "propuesta": DealStage.PROPOSAL.value,
    "proposal": DealStage.PROPOSAL.value,
    "negociacion": DealStage.NEGOTIATION.value,
    "negotiation": DealStage.NEGOTIATION.value,
    "ganado": DealStage.CLOSED_WON.value,
    "closed_won": DealStage.CLOSED_WON.value,
    "perdido": DealStage.CLOSED_LOST.value,
    "closed_lost": DealStage.CLOSED_LOST.value,
}

PAYMENT_ALIASES = {
    "pendiente": PaymentStatus.PENDIENTE.value,
    "sin_pago": PaymentStatus.PENDIENTE.value,
    "anticipo": PaymentStatus.ANTICIPO.value,
    "abono": PaymentStatus.ANTICIPO.value,
    "cobrado": PaymentStatus.COBRADO.value,
    "pagado": PaymentStatus.COBRADO.value,
    "cancelado": PaymentStatus.CANCELADO.value,
}

DATE_FIELDS = {"payment_date", "created_at", "updated_at", "closed_at"}


def _project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


def _value(value: Any) -> str:
    return value.value if hasattr(value, "value") else str(value or "")


def _money(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    return round(float(value), 2)


def _parse_date(value: Any) -> Optional[date]:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()


def normalize_source(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return LeadSource.WHATSAPP.value
    normalized = SOURCE_ALIASES.get(text.lower())
    if normalized:
        return normalized
    valid = {item.value for item in LeadSource}
    if text in valid:
        return text
    raise ValueError(f"Origen inválido: {value}. Usa uno de: {', '.join(sorted(valid))}")


def normalize_stage(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    normalized = STAGE_ALIASES.get(text.lower())
    if normalized:
        return normalized
    valid = {item.value for item in DealStage}
    if text in valid:
        return text
    raise ValueError(f"Etapa inválida: {value}. Usa uno de: {', '.join(sorted(valid))}")


def normalize_payment_status(value: Any) -> str:
    text = str(value or "").strip().lower()
    normalized = PAYMENT_ALIASES.get(text)
    if normalized:
        return normalized
    valid = {item.value for item in PaymentStatus}
    if text in valid:
        return text
    raise ValueError(
        f"Estado de pago inválido: {value}. Usa uno de: {', '.join(sorted(valid))}"
    )


def _next_deal_id(deals: List[Deal]) -> str:
    numbers = []
    for deal in deals:
        match = re.fullmatch(r"D-(\d+)", deal.deal_id)
        if match:
            numbers.append(int(match.group(1)))
    return f"D-{max(numbers, default=0) + 1:04d}"


def _normalize_row(row: Dict[str, str]) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for name in Deal.model_fields:
        raw = row.get(name, "")
        if name == "amount_collected":
            data[name] = _money(raw)
        elif name == "amount":
            data[name] = None if raw in (None, "") else _money(raw)
        elif name in DATE_FIELDS:
            data[name] = _parse_date(raw)
        elif name in {"lead_source", "funnel_line"}:
            data[name] = raw or None
        elif name == "deal_stage":
            data[name] = raw or DealStage.NEW.value
        elif name == "payment_status":
            data[name] = raw or PaymentStatus.PENDIENTE.value
        elif name == "currency":
            data[name] = raw or "MXN"
        else:
            data[name] = raw if raw is not None else ""
    return data


class RevenueStore:
    """CSV-based deal store scoped to one tenant."""

    def __init__(self, tenant_id: str, base_path: Optional[Path] = None):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path) if base_path else _project_root()
        self.tenant_dir = self.base_path / "tenants" / tenant_id
        if not (self.tenant_dir / "config.json").is_file():
            raise FileNotFoundError(f"No existe tenants/{tenant_id}/config.json")
        self.path = self.tenant_dir / "data" / f"deals_{tenant_id}.csv"

    def load(self) -> List[Deal]:
        if not self.path.is_file():
            return []
        deals: List[Deal] = []
        with self.path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if not row.get("deal_id"):
                    continue
                try:
                    deals.append(Deal(**_normalize_row(row)))
                except (ValidationError, ValueError) as exc:
                    raise ValueError(f"Fila inválida en {self.path}: {exc}") from exc
        return deals

    def save(self, deals: List[Deal]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(Deal.model_fields)
        with self.path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for deal in deals:
                row = deal.model_dump(mode="json")
                writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})

    def add(
        self,
        *,
        client: str,
        product: str,
        quote: float,
        status: str = PaymentStatus.PENDIENTE.value,
        collected: float = 0.0,
        source: str = LeadSource.WHATSAPP.value,
        stage: Optional[str] = None,
        funnel_line: Optional[str] = None,
        payment_method: str = "",
        payment_date: Optional[date] = None,
        publication_id: str = "",
        campaign_id: str = "",
        conversation_id: str = "",
        notes: str = "",
        lost_reason: str = "",
        phone: str = "",
        email: str = "",
        currency: str = "MXN",
    ) -> Deal:
        quote = _money(quote)
        collected = _money(collected)
        if quote <= 0:
            raise ValueError("El monto cotizado debe ser mayor a 0.")
        if collected < 0:
            raise ValueError("El monto cobrado no puede ser negativo.")

        payment_status = normalize_payment_status(status)
        if payment_status in REVENUE_STATUSES and collected <= 0:
            raise ValueError("Para anticipo o cobrado indica un monto cobrado mayor a 0.")
        if payment_status == PaymentStatus.PENDIENTE.value and collected > 0:
            raise ValueError("Si ya recibiste dinero, usa anticipo o cobrado.")
        if payment_status == PaymentStatus.ANTICIPO.value and collected > quote:
            raise ValueError("El anticipo no puede ser mayor al monto cotizado.")

        today = date.today()
        normalized_stage = normalize_stage(stage) if stage else ""
        if not normalized_stage:
            normalized_stage = (
                DealStage.CLOSED_WON.value
                if payment_status in REVENUE_STATUSES
                else DealStage.CLOSED_LOST.value
                if payment_status == PaymentStatus.CANCELADO.value
                else DealStage.NEW.value
            )

        deals = self.load()
        deal = Deal(
            deal_id=_next_deal_id(deals),
            tenant_id=self.tenant_id,
            lead_source=normalize_source(source),
            deal_stage=normalized_stage,
            funnel_line=funnel_line or None,
            amount=quote,
            amount_collected=collected,
            payment_status=payment_status,
            payment_method=payment_method,
            payment_date=payment_date or (today if payment_status in REVENUE_STATUSES else None),
            product_ref=product.strip(),
            source_publication_id=publication_id,
            source_campaign_id=campaign_id,
            source_conversation_id=conversation_id,
            currency=currency,
            contact_name=client.strip(),
            contact_phone=phone,
            contact_email=email,
            notes=notes,
            lost_reason=lost_reason,
            created_at=today,
            updated_at=today,
            closed_at=today if normalized_stage in {DealStage.CLOSED_WON.value, DealStage.CLOSED_LOST.value} else None,
        )
        deals.append(deal)
        self.save(deals)
        return deal

    def update(
        self,
        deal_id: str,
        *,
        status: Optional[str] = None,
        collected: Optional[float] = None,
        stage: Optional[str] = None,
        payment_method: Optional[str] = None,
        payment_date: Optional[date] = None,
        notes: Optional[str] = None,
        lost_reason: Optional[str] = None,
        source: Optional[str] = None,
        publication_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
    ) -> Deal:
        deals = self.load()
        deal = next((item for item in deals if item.deal_id == deal_id), None)
        if deal is None:
            raise ValueError(f"No existe el deal {deal_id} para {self.tenant_id}.")

        new_status = normalize_payment_status(status) if status else _value(deal.payment_status)
        new_collected = _money(deal.amount_collected if collected is None else collected)
        if new_status == PaymentStatus.COBRADO.value and collected is None:
            raise ValueError("Para marcar cobrado indica el total cobrado con --collected.")
        if new_status in REVENUE_STATUSES and new_collected <= 0:
            raise ValueError("Para anticipo o cobrado el monto cobrado debe ser mayor a 0.")
        if new_status == PaymentStatus.PENDIENTE.value:
            new_collected = 0.0
        if new_status == PaymentStatus.ANTICIPO.value and deal.amount and new_collected > deal.amount:
            raise ValueError("El anticipo no puede ser mayor al monto cotizado.")

        deal.payment_status = new_status
        deal.amount_collected = new_collected
        if stage:
            deal.deal_stage = normalize_stage(stage)
        elif new_status in REVENUE_STATUSES:
            deal.deal_stage = DealStage.CLOSED_WON.value
        elif new_status == PaymentStatus.CANCELADO.value:
            deal.deal_stage = DealStage.CLOSED_LOST.value
        if payment_method is not None:
            deal.payment_method = payment_method
        if payment_date is not None:
            deal.payment_date = payment_date
        elif new_status in REVENUE_STATUSES and deal.payment_date is None:
            deal.payment_date = date.today()
        if notes is not None:
            deal.notes = notes
        if lost_reason is not None:
            deal.lost_reason = lost_reason
        if source is not None:
            deal.lead_source = normalize_source(source)
        if publication_id is not None:
            deal.source_publication_id = publication_id
        if campaign_id is not None:
            deal.source_campaign_id = campaign_id
        if conversation_id is not None:
            deal.source_conversation_id = conversation_id
        if deal.deal_stage in {DealStage.CLOSED_WON.value, DealStage.CLOSED_LOST.value}:
            deal.closed_at = deal.closed_at or date.today()
        deal.updated_at = date.today()

        self.save(deals)
        return deal

    def report(self) -> Dict[str, Any]:
        return summarize_deals(self.load(), tenant_id=self.tenant_id)


def summarize_deals(deals: List[Deal], tenant_id: Optional[str] = None) -> Dict[str, Any]:
    items = [deal for deal in deals if tenant_id is None or deal.tenant_id == tenant_id]
    totals = {
        "deals": len(items),
        "quoted_total": 0.0,
        "revenue_total": 0.0,
        "anticipos_total": 0.0,
        "cobrado_total": 0.0,
        "pending_total": 0.0,
        "cancelled_total": 0.0,
        "closed_won": 0,
        "closed_lost": 0,
        "paid_deals": 0,
    }
    by_status: Dict[str, Dict[str, Any]] = {}
    by_source: Dict[str, Dict[str, Any]] = {}
    by_product: Dict[str, Dict[str, Any]] = {}

    def bucket(target: Dict[str, Dict[str, Any]], key: str) -> Dict[str, Any]:
        return target.setdefault(key, {"deals": 0, "quoted": 0.0, "collected": 0.0})

    for deal in items:
        status = _value(deal.payment_status) or PaymentStatus.PENDIENTE.value
        stage = _value(deal.deal_stage)
        source = _value(deal.lead_source) or "sin_origen"
        product = deal.product_ref or "sin_producto"
        quoted = _money(deal.amount)
        collected = _money(deal.amount_collected)

        totals["quoted_total"] += quoted
        if status == PaymentStatus.ANTICIPO.value:
            totals["anticipos_total"] += collected
            totals["pending_total"] += max(quoted - collected, 0)
            totals["paid_deals"] += 1
        elif status == PaymentStatus.COBRADO.value:
            totals["cobrado_total"] += collected
            totals["paid_deals"] += 1
        elif status == PaymentStatus.PENDIENTE.value:
            totals["pending_total"] += max(quoted - collected, 0)
        elif status == PaymentStatus.CANCELADO.value:
            totals["cancelled_total"] += quoted

        if stage == DealStage.CLOSED_WON.value:
            totals["closed_won"] += 1
        elif stage == DealStage.CLOSED_LOST.value:
            totals["closed_lost"] += 1

        for target, key in ((by_status, status), (by_source, source), (by_product, product)):
            item = bucket(target, key)
            item["deals"] += 1
            item["quoted"] += quoted
            item["collected"] += collected if status in REVENUE_STATUSES else 0.0

    totals["revenue_total"] = round(totals["anticipos_total"] + totals["cobrado_total"], 2)
    for key in ("quoted_total", "anticipos_total", "cobrado_total", "pending_total", "cancelled_total"):
        totals[key] = round(totals[key], 2)
    closed = totals["closed_won"] + totals["closed_lost"]
    totals["close_rate"] = round(totals["closed_won"] / closed, 4) if closed else 0.0
    totals["average_ticket"] = (
        round(totals["revenue_total"] / totals["paid_deals"], 2) if totals["paid_deals"] else 0.0
    )
    for target in (by_status, by_source, by_product):
        for value in target.values():
            value["quoted"] = round(value["quoted"], 2)
            value["collected"] = round(value["collected"], 2)

    return {
        "tenant_id": tenant_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        **totals,
        "by_status": by_status,
        "by_source": by_source,
        "by_product": by_product,
    }
