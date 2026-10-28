"""Tests de la evidencia histórica en el planner (aislada por tenant)."""

from __future__ import annotations

import json
from unittest.mock import patch

from modules.intelligence.planner import ScheduleItem, build_schedule


def _slot(tenant: str, date: str = "2099-01-15") -> dict:
    return {
        "slot_id": f"{tenant}-20990115-morning-01",
        "slot_type": "media",
        "date_local": date,
        "time_local": "08:30",
        "datetime_utc": f"{date}T13:30:00+00:00",
        "description": "Test post - Kael - Something",
        "source_filename": "123456 - Kael - Test.png",
        "asset_ref": "123456",
        "whatsapp_e164": None,
    }


def _write(tmp_path, slot):
    path = tmp_path / "dryrun.json"
    path.write_text(json.dumps({"schedule": [slot]}), encoding="utf-8")
    return path


@patch("modules.intelligence.planner.historical_baseline")
def test_universe_tenant_gets_historical_evidence(mock_baseline, tmp_path):
    mock_baseline.get_historical_reuse_info.return_value = {
        "asset_ref": "123456",
        "personaje_principal": "Kael",
        "evidence_level": "confirmed_descriptive",
    }

    items = build_schedule(
        tenant_id="universe", source="dryrun", dryrun_path=_write(tmp_path, _slot("universe"))
    )

    assert len(items) == 1
    item = items[0]
    assert isinstance(item, ScheduleItem)
    assert item._meta["historical_evidence"]["personaje_principal"] == "Kael"
    mock_baseline.get_historical_reuse_info.assert_called_once_with(
        "123456 - Kael - Test.png", tenant_id="universe"
    )


@patch("modules.intelligence.planner.historical_baseline")
def test_other_tenant_gets_uncertain_evidence(mock_baseline, tmp_path):
    mock_baseline.get_historical_reuse_info.return_value = None

    items = build_schedule(
        tenant_id="other", source="dryrun", dryrun_path=_write(tmp_path, _slot("other"))
    )

    assert len(items) == 1
    assert items[0]._meta["historical_evidence"] is None
    mock_baseline.get_historical_reuse_info.assert_called_once_with(
        "123456 - Kael - Test.png", tenant_id="other"
    )


def test_baseline_no_mezcla_tenants():
    from modules.intelligence import historical_baseline as hb

    assert hb.historical_base("universe") != hb.historical_base("flexi")
    assert hb.historical_base("flexi").name == "historical"
    assert hb.historical_base("flexi").parent.name == "flexi"
    assert hb.load_reuse_queue("flexi") == []
