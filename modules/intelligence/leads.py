"""Leads Lite: conversaciones y nivel de intención antes de que exista venta.

Un lead no es un deal. ``intent`` es una lectura humana de la conversación, no
una predicción del sistema. El objetivo es saber cuántas conversaciones entran,
de dónde vienen y qué tan cerca están de una cotización o cita.
"""

from __future__ import annotations

import csv
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import ValidationError

from growthos.core.enums import LeadIntent, LeadSource, LeadStatus
from growthos.core.models import Lead
from modules.intelligence.revenue import _project_root, normalize_source

INTENT_ALIASES = {
    "frio": LeadIntent.FRIO.value,
    "frío": LeadIntent.FRIO.value,
    "cold": LeadIntent.FRIO.value,
    "bajo": LeadIntent.FRIO.value,
    "baja": LeadIntent.FRIO.value,
    "tibio": LeadIntent.TIBIO.value,
    "warm": LeadIntent.TIBIO.value,
    "medio": LeadIntent.TIBIO.value,
    "media": LeadIntent.TIBIO.value,
    "caliente": LeadIntent.CALIENTE.value,
    "hot": LeadIntent.CALIENTE.value,
    "alto": LeadIntent.CALIENTE.value,
    "alta": LeadIntent.CALIENTE.value,
}

STATUS_ALIASES = {
    "nuevo": LeadStatus.NUEVO.value,
    "new": LeadStatus.NUEVO.value,
    "contactado": LeadStatus.CONTACTADO.value,
    "contacted": LeadStatus.CONTACTADO.value,
    "calificado": LeadStatus.CALIFICADO.value,
    "qualified": LeadStatus.CALIFICADO.value,
    "cotizado": LeadStatus.COTIZADO.value,
    "proposal": LeadStatus.COTIZADO.value,
    "cita": LeadStatus.CITA_AGENDADA.value,
    "cita_agendada": LeadStatus.CITA_AGENDADA.value,
    "appointment": LeadStatus.CITA_AGENDADA.value,
    "ganado": LeadStatus.GANADO.value,
    "won": LeadStatus.GANADO.value,
    "perdido": LeadStatus.PERDIDO.value,
    "lost": LeadStatus.PERDIDO.value,
}

DATE_FIELDS = {"created_at", "updated_at", "last_contact_at", "next_action_at"}
CLOSED_STATUSES = {LeadStatus.GANADO.value, LeadStatus.PERDIDO.value}


def _value(value: Any) -> str:
    return value.value if hasattr(value, "value") else str(value or "")


def _parse_date(value: Any) -> Optional[date]:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()


def normalize_intent(value: Any) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return LeadIntent.FRIO.value
    normalized = INTENT_ALIASES.get(text)
    if normalized:
        return normalized
    valid = {item.value for item in LeadIntent}
    if text in valid:
        return text
    raise ValueError(
        f"Intención inválida: {value}. Usa uno de: {', '.join(sorted(valid))}"
    )


def normalize_status(value: Any) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return LeadStatus.NUEVO.value
    normalized = STATUS_ALIASES.get(text)
    if normalized:
        return normalized
    valid = {item.value for item in LeadStatus}
    if text in valid:
        return text
    raise ValueError(
        f"Estado inválido: {value}. Usa uno de: {', '.join(sorted(valid))}"
    )


def _next_lead_id(leads: List[Lead]) -> str:
    numbers = []
    for lead in leads:
        match = re.fullmatch(r"L-(\d+)", lead.lead_id)
        if match:
            numbers.append(int(match.group(1)))
    return f"L-{max(numbers, default=0) + 1:04d}"


def _normalize_row(row: Dict[str, str]) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for name in Lead.model_fields:
        raw = row.get(name, "")
        if name in DATE_FIELDS:
            data[name] = _parse_date(raw)
        elif name == "lead_source":
            data[name] = raw or None
        elif name == "intent":
            data[name] = raw or LeadIntent.FRIO.value
        elif name == "status":
            data[name] = raw or LeadStatus.NUEVO.value
        else:
            data[name] = raw if raw is not None else ""
    return data


class LeadStore:
    """CSV de leads aislado por tenant."""

    def __init__(self, tenant_id: str, base_path: Optional[Path] = None):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path) if base_path else _project_root()
        self.tenant_dir = self.base_path / "tenants" / tenant_id
        if not (self.tenant_dir / "config.json").is_file():
            raise FileNotFoundError(f"No existe tenants/{tenant_id}/config.json")
        self.path = self.tenant_dir / "data" / f"leads_{tenant_id}.csv"

    def load(self) -> List[Lead]:
        if not self.path.is_file():
            return []
        leads: List[Lead] = []
        with self.path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if not row.get("lead_id"):
                    continue
                try:
                    leads.append(Lead(**_normalize_row(row)))
                except (ValidationError, ValueError) as exc:
                    raise ValueError(f"Fila inválida en {self.path}: {exc}") from exc
        return leads

    def save(self, leads: List[Lead]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(Lead.model_fields)
        with self.path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for lead in leads:
                row = lead.model_dump(mode="json")
                writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})

    def add(
        self,
        *,
        contact_name: str = "",
        phone: str = "",
        email: str = "",
        source: str = LeadSource.WHATSAPP.value,
        intent: str = LeadIntent.FRIO.value,
        status: str = LeadStatus.NUEVO.value,
        product_interest: str = "",
        budget_range: str = "",
        publication_id: str = "",
        campaign_id: str = "",
        conversation_id: str = "",
        notes: str = "",
        lost_reason: str = "",
        assigned_to: str = "",
        created_at: Optional[date] = None,
        last_contact_at: Optional[date] = None,
        next_action_at: Optional[date] = None,
    ) -> Lead:
        today = date.today()
        lead = Lead(
            lead_id=_next_lead_id(self.load()),
            tenant_id=self.tenant_id,
            contact_name=contact_name,
            contact_phone=phone,
            contact_email=email,
            lead_source=normalize_source(source),
            intent=normalize_intent(intent),
            status=normalize_status(status),
            product_interest=product_interest.strip(),
            budget_range=budget_range.strip(),
            source_publication_id=publication_id,
            source_campaign_id=campaign_id,
            source_conversation_id=conversation_id,
            notes=notes,
            lost_reason=lost_reason,
            assigned_to=assigned_to,
            created_at=created_at or today,
            updated_at=created_at or today,
            last_contact_at=last_contact_at,
            next_action_at=next_action_at,
        )
        leads = self.load()
        leads.append(lead)
        self.save(leads)
        return lead

    def update(
        self,
        lead_id: str,
        *,
        intent: Optional[str] = None,
        status: Optional[str] = None,
        product_interest: Optional[str] = None,
        budget_range: Optional[str] = None,
        notes: Optional[str] = None,
        lost_reason: Optional[str] = None,
        assigned_to: Optional[str] = None,
        source: Optional[str] = None,
        publication_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        last_contact_at: Optional[date] = None,
        next_action_at: Optional[date] = None,
    ) -> Lead:
        leads = self.load()
        lead = next((item for item in leads if item.lead_id == lead_id), None)
        if lead is None:
            raise ValueError(f"No existe el lead {lead_id} para {self.tenant_id}.")

        if intent is not None:
            lead.intent = normalize_intent(intent)
        if status is not None:
            lead.status = normalize_status(status)
        if product_interest is not None:
            lead.product_interest = product_interest
        if budget_range is not None:
            lead.budget_range = budget_range
        if notes is not None:
            lead.notes = notes
        if lost_reason is not None:
            lead.lost_reason = lost_reason
        if assigned_to is not None:
            lead.assigned_to = assigned_to
        if source is not None:
            lead.lead_source = normalize_source(source)
        if publication_id is not None:
            lead.source_publication_id = publication_id
        if campaign_id is not None:
            lead.source_campaign_id = campaign_id
        if conversation_id is not None:
            lead.source_conversation_id = conversation_id
        if last_contact_at is not None:
            lead.last_contact_at = last_contact_at
        if next_action_at is not None:
            lead.next_action_at = next_action_at

        lead.updated_at = date.today()
        self.save(leads)
        return lead

    def filtered(
        self,
        *,
        intent: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        since: Optional[date] = None,
    ) -> List[Lead]:
        items = self.load()
        if intent:
            wanted = normalize_intent(intent)
            items = [lead for lead in items if _value(lead.intent) == wanted]
        if status:
            wanted = normalize_status(status)
            items = [lead for lead in items if _value(lead.status) == wanted]
        if source:
            wanted = normalize_source(source)
            items = [lead for lead in items if _value(lead.lead_source) == wanted]
        if since:
            items = [lead for lead in items if lead.created_at and lead.created_at >= since]
        return items

    def report(self) -> Dict[str, Any]:
        return summarize_leads(self.load(), tenant_id=self.tenant_id)


def summarize_leads(
    leads: List[Lead],
    tenant_id: Optional[str] = None,
    today: Optional[date] = None,
) -> Dict[str, Any]:
    today = today or date.today()
    items = [lead for lead in leads if tenant_id is None or lead.tenant_id == tenant_id]

    totals: Dict[str, Any] = {
        "leads": len(items),
        "hot": 0,
        "warm": 0,
        "cold": 0,
        "open": 0,
        "won": 0,
        "lost": 0,
        "followups_due": 0,
        "new_last_7d": 0,
        "contacted_or_beyond": 0,
        "quoted_or_beyond": 0,
        "appointments": 0,
    }
    by_intent: Dict[str, int] = {}
    by_source: Dict[str, int] = {}
    by_status: Dict[str, int] = {}

    week_ago = today - timedelta(days=7)
    quoted_statuses = {LeadStatus.COTIZADO.value, LeadStatus.CITA_AGENDADA.value, LeadStatus.GANADO.value}
    contacted_statuses = {
        LeadStatus.CONTACTADO.value,
        LeadStatus.CALIFICADO.value,
        *quoted_statuses,
    }

    for lead in items:
        intent = _value(lead.intent) or LeadIntent.FRIO.value
        status = _value(lead.status) or LeadStatus.NUEVO.value
        source = _value(lead.lead_source) or "sin_origen"

        by_intent[intent] = by_intent.get(intent, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        by_source[source] = by_source.get(source, 0) + 1

        if intent == LeadIntent.CALIENTE.value:
            totals["hot"] += 1
        elif intent == LeadIntent.TIBIO.value:
            totals["warm"] += 1
        else:
            totals["cold"] += 1

        if status == LeadStatus.GANADO.value:
            totals["won"] += 1
        elif status == LeadStatus.PERDIDO.value:
            totals["lost"] += 1
        else:
            totals["open"] += 1

        if status in contacted_statuses:
            totals["contacted_or_beyond"] += 1
        if status in quoted_statuses:
            totals["quoted_or_beyond"] += 1
        if status in {LeadStatus.CITA_AGENDADA.value, LeadStatus.GANADO.value}:
            totals["appointments"] += 1
        if lead.created_at and lead.created_at >= week_ago:
            totals["new_last_7d"] += 1
        if (
            lead.next_action_at
            and lead.next_action_at <= today
            and status not in CLOSED_STATUSES
        ):
            totals["followups_due"] += 1

    total = totals["leads"]
    totals["contact_rate"] = round(totals["contacted_or_beyond"] / total, 4) if total else 0.0
    totals["quote_rate"] = round(totals["quoted_or_beyond"] / total, 4) if total else 0.0
    totals["appointment_rate"] = round(totals["appointments"] / total, 4) if total else 0.0
    totals["hot_rate"] = round(totals["hot"] / total, 4) if total else 0.0
    totals["win_rate"] = round(totals["won"] / total, 4) if total else 0.0

    return {
        "tenant_id": tenant_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        **totals,
        "by_intent": dict(sorted(by_intent.items())),
        "by_source": dict(sorted(by_source.items())),
        "by_status": dict(sorted(by_status.items())),
    }
