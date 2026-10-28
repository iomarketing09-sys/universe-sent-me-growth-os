"""Tests del guard de reutilización del IgScheduler.

Cubre dos políticas distintas:
- contenido (Universe): ventana de 30 días sobre la cola de reutilización;
- producto físico (Flexi): manda el inventario, no la ventana.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from modules.social.ig_scheduler import (
    REUSE_ALLOWED,
    REUSE_BLOCKED,
    REUSE_NOT_APPLICABLE,
    REUSE_UNKNOWN,
    IgScheduler,
    ScheduleItem,
)

ASSET = "123456 - Kael - Test.png"
TODAY = date(2026, 10, 28)


def _scheduler(tenant: str = "universe", baseline=None) -> IgScheduler:
    """Scheduler sin __init__: evita publishers y red en los tests."""
    scheduler = IgScheduler.__new__(IgScheduler)
    scheduler.tenant_ids = [tenant]
    scheduler._historical_baseline = baseline
    return scheduler


def _baseline(queue=None, inventory=None):
    baseline = MagicMock()
    baseline.load_reuse_queue.return_value = queue or []
    baseline.load_asset_inventory.return_value = inventory or []
    return baseline


def test_dentro_de_30_dias_bloquea():
    baseline = _baseline(
        queue=[{"asset_ref": "123456", "fecha_ultima_publicacion": (TODAY - timedelta(days=10)).isoformat()}]
    )
    report = _scheduler(baseline=baseline).historical_reuse_report(ASSET, today=TODAY)

    assert report["status"] == REUSE_BLOCKED
    assert report["days_since"] == 10
    assert report["window_days"] == 30


def test_fuera_de_30_dias_permite():
    baseline = _baseline(
        queue=[{"asset_ref": "123456", "fecha_ultima_publicacion": (TODAY - timedelta(days=40)).isoformat()}]
    )
    report = _scheduler(baseline=baseline).historical_reuse_report(ASSET, today=TODAY)

    assert report["status"] == REUSE_ALLOWED
    assert report["days_since"] == 40


def test_activo_en_inventario_sin_historial_es_unknown():
    baseline = _baseline(
        queue=[{"asset_ref": "999999", "fecha_ultima_publicacion": TODAY.isoformat()}],
        inventory=[{"asset_id": "123456"}],
    )
    report = _scheduler(baseline=baseline).historical_reuse_report(ASSET, today=TODAY)

    assert report["status"] == REUSE_UNKNOWN
    assert "inventario" in report["reason"].lower()


def test_activo_desconocido_es_unknown():
    baseline = _baseline(
        queue=[{"asset_ref": "999999", "fecha_ultima_publicacion": TODAY.isoformat()}],
        inventory=[{"asset_id": "888888"}],
    )
    assert _scheduler(baseline=baseline)._check_historical_reuse(ASSET) == REUSE_UNKNOWN


def test_excepcion_del_baseline_no_tumba_el_scheduler():
    baseline = MagicMock()
    baseline.load_reuse_queue.side_effect = RuntimeError("boom")
    assert _scheduler(baseline=baseline)._check_historical_reuse(ASSET) == REUSE_UNKNOWN


@pytest.mark.parametrize("value", ["", None])
def test_activo_vacio_es_unknown(value):
    assert _scheduler()._check_historical_reuse(value) == REUSE_UNKNOWN


def test_consulta_la_cola_del_tenant_correcto():
    baseline = _baseline()
    _scheduler("bam-in-a-can", baseline)._check_historical_reuse(ASSET)

    baseline.load_reuse_queue.assert_called_once_with("bam-in-a-can")


def test_main_all_tenants_sin_credenciales_no_falla(monkeypatch):
    import modules.social.ig_scheduler as scheduler

    monkeypatch.setattr(scheduler, "discover_tenants", lambda: [])

    assert scheduler.main(["--all-tenants"]) == 0


def test_tenant_de_producto_no_usa_la_ventana_de_30_dias():
    baseline = MagicMock()
    report = _scheduler("flexi", baseline).historical_reuse_report(
        "ISAURA_142801_BEIGE_OI26.jpg", today=TODAY
    )

    assert report["status"] == REUSE_NOT_APPLICABLE
    assert report["inventory"]["status"] == "IN_INVENTORY"
    baseline.load_reuse_queue.assert_not_called()


def test_inventario_parcial_de_flexi():
    scheduler = _scheduler("flexi")
    assert scheduler.inventory_status("142801")["status"] == "IN_INVENTORY"
    assert scheduler.inventory_status("142801")["model"] == "ISAURA"
    missing = scheduler.inventory_status("999999")
    assert missing["status"] == "NOT_IN_INVENTORY"
    assert "parcial" in missing["note"].lower()


def test_process_item_no_publica_si_esta_bloqueado():
    baseline = _baseline(
        queue=[{"asset_ref": "123456", "fecha_ultima_publicacion": date.today().isoformat()}]
    )
    scheduler = _scheduler("universe", baseline)
    publisher = MagicMock()
    scheduler.publishers = {"universe": publisher}

    item = ScheduleItem(
        tenant_id="universe",
        date_str="2026-10-28",
        time_str="08:30",
        media_filename=ASSET,
        caption="Hola",
        post_type="photo",
        datetime_local=datetime.now(timezone.utc),
        datetime_utc=datetime.now(timezone.utc),
    )

    assert scheduler.process_item(item) is None
    publisher.publish.assert_not_called()
