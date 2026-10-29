"""Revenue MVP: anticipo/cobrado, no double counting, tenant isolation."""

import json
from datetime import date
from pathlib import Path

import pytest

from growthos.core.enums import DealStage, LeadSource, PaymentStatus
from growthos.core.models import Deal
from growthos.storage.database import Database
from growthos.storage.repositories import DealRepository
from modules.intelligence.revenue import RevenueStore, summarize_deals


def _tenant(root: Path, tenant_id: str) -> Path:
    tenant = root / "tenants" / tenant_id
    tenant.mkdir(parents=True)
    (tenant / "config.json").write_text(
        json.dumps(
            {
                "tenant_id": tenant_id,
                "client_name": tenant_id,
                "timezone": "America/Matamoros",
                "contact_channel": "WhatsApp",
                "tenant_type": "physical_cro",
            }
        ),
        encoding="utf-8",
    )
    return tenant


def test_anticipo_to_cobrado_does_not_double_count(tmp_path: Path):
    _tenant(tmp_path, "micas-art-deco")
    store = RevenueStore("micas-art-deco", base_path=tmp_path)

    deal = store.add(
        client="Ana",
        product="Tulipán en Flor",
        quote=500,
        status="anticipo",
        collected=250,
        source="instagram",
        payment_method="transferencia",
    )
    assert deal.deal_id == "D-0001"

    report = store.report()
    assert report["revenue_total"] == 250
    assert report["anticipos_total"] == 250
    assert report["cobrado_total"] == 0
    assert report["pending_total"] == 250
    assert report["by_source"]["Instagram"]["collected"] == 250

    store.update("D-0001", status="cobrado", collected=500)
    report = store.report()
    assert report["revenue_total"] == 500
    assert report["anticipos_total"] == 0
    assert report["cobrado_total"] == 500
    assert report["pending_total"] == 0


def test_pending_and_cancelled_are_not_revenue(tmp_path: Path):
    _tenant(tmp_path, "micas-art-deco")
    store = RevenueStore("micas-art-deco", base_path=tmp_path)
    store.add(client="Luis", product="Sobres pack 4", quote=100, status="pendiente")
    cancelled = store.add(
        client="Marta",
        product="Virgen de Guadalupe",
        quote=2000,
        status="cancelado",
        lost_reason="precio",
    )
    report = store.report()
    assert report["deals"] == 2
    assert report["revenue_total"] == 0
    assert report["pending_total"] == 100
    assert report["cancelled_total"] == 2000
    assert cancelled.deal_stage == DealStage.CLOSED_LOST.value


def test_tenant_isolation(tmp_path: Path):
    _tenant(tmp_path, "micas-art-deco")
    _tenant(tmp_path, "flexi")
    micas = RevenueStore("micas-art-deco", base_path=tmp_path)
    flexi = RevenueStore("flexi", base_path=tmp_path)
    micas.add(client="Ana", product="Tulipán", quote=500, status="cobrado", collected=500)
    flexi.add(client="Pedro", product="142601", quote=1200, status="anticipo", collected=600)

    assert micas.report()["revenue_total"] == 500
    assert flexi.report()["revenue_total"] == 600
    assert len(micas.load()) == 1
    assert len(flexi.load()) == 1


def test_invalid_payment_state_and_amounts(tmp_path: Path):
    _tenant(tmp_path, "micas-art-deco")
    store = RevenueStore("micas-art-deco", base_path=tmp_path)
    with pytest.raises(ValueError):
        store.add(client="Ana", product="Tulipán", quote=500, status="anticipo", collected=0)
    with pytest.raises(ValueError):
        store.add(client="Ana", product="Tulipán", quote=0, status="pendiente")
    with pytest.raises(ValueError):
        store.add(client="Ana", product="Tulipán", quote=500, status="pagado_parcial", collected=100)


def test_csv_roundtrip_preserves_fields(tmp_path: Path):
    _tenant(tmp_path, "micas-art-deco")
    store = RevenueStore("micas-art-deco", base_path=tmp_path)
    store.add(
        client="Ana",
        product="Tulipán en Flor",
        quote=500,
        status="anticipo",
        collected=250,
        source="facebook",
        payment_method="efectivo",
        payment_date=date(2026, 10, 29),
        publication_id="post-123",
        campaign_id="camp-1",
        conversation_id="wa-1",
    )
    loaded = store.load()[0]
    assert loaded.lead_source == LeadSource.FACEBOOK.value
    assert loaded.payment_status == PaymentStatus.ANTICIPO.value
    assert loaded.payment_date == date(2026, 10, 29)
    assert loaded.source_publication_id == "post-123"
    assert loaded.source_campaign_id == "camp-1"
    assert loaded.source_conversation_id == "wa-1"


def test_deal_repository_uses_new_schema(tmp_path: Path):
    db = Database(db_path=tmp_path / "deals.db")
    db.init_schema()
    repo = DealRepository(db)
    deal = Deal(
        deal_id="D-0001",
        tenant_id="micas-art-deco",
        lead_source=LeadSource.INSTAGRAM.value,
        deal_stage=DealStage.CLOSED_WON.value,
        product_ref="Tulipán en Flor",
        amount=500,
        amount_collected=250,
        payment_status=PaymentStatus.ANTICIPO.value,
        payment_method="transferencia",
    )
    repo.save(deal)
    loaded = repo.get_by_id("D-0001")
    assert loaded is not None
    assert loaded.amount_collected == 250
    assert loaded.payment_status == PaymentStatus.ANTICIPO.value
    assert loaded.product_ref == "Tulipán en Flor"
    db.close()


def test_summarize_empty():
    report = summarize_deals([], tenant_id="micas-art-deco")
    assert report["deals"] == 0
    assert report["revenue_total"] == 0
    assert report["close_rate"] == 0
