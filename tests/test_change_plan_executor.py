"""Tests del ejecutor de planes de cambio de Ads."""

import json

from modules.intelligence.change_plan_executor import (
    ActionOutcome,
    ChangePlanExecutor,
    build_plan_from_capture,
)


def _plan(actions):
    return {
        "campaign_id": "120247658527630665",
        "campaign_slug": "2026-11_flexi_ads_560mxn",
        "checkpoint": "E72",
        "actions": actions,
    }


class FakeTransport:
    def __init__(self, status_after="PAUSED", success=True):
        self.calls = []
        self.status_after = status_after
        self.success = success

    def __call__(self, method, path, params):
        self.calls.append((method, path, dict(params)))
        if method == "POST":
            return {"success": self.success}
        return {"status": self.status_after}


class TestChangePlanExecutor:
    def test_dry_run_does_not_touch_transport(self, tmp_path):
        transport = FakeTransport()
        executor = ChangePlanExecutor(
            tenant_id="flexi",
            dry_run=True,
            base_path=tmp_path,
            transport=transport,
        )
        outcomes = executor.apply(
            _plan([{"target_id": "ad1", "target_name": "Amalia", "action": "pause_ad"}])
        )

        assert outcomes[0].result == "would_apply"
        assert transport.calls == []
        assert not (tmp_path / "tenants" / "flexi" / "ads" / "insights" / "actions.jsonl").exists()

    def test_applies_pause_and_verifies(self, tmp_path):
        transport = FakeTransport()
        executor = ChangePlanExecutor(
            tenant_id="flexi",
            dry_run=False,
            base_path=tmp_path,
            transport=transport,
        )
        outcomes = executor.apply(
            _plan([{"target_id": "ad1", "target_name": "Amalia", "action": "pause_ad"}])
        )

        assert [item.result for item in outcomes] == ["applied"]
        assert transport.calls == [
            ("POST", "ad1", {"status": "PAUSED"}),
            ("GET", "ad1", {"fields": "status"}),
        ]

        audit = tmp_path / "tenants" / "flexi" / "ads" / "insights" / "actions.jsonl"
        entry = json.loads(audit.read_text(encoding="utf-8").splitlines()[0])
        assert entry["result"] == "applied"
        assert entry["target_id"] == "ad1"
        assert entry["campaign_slug"] == "2026-11_flexi_ads_560mxn"

    def test_fails_when_status_does_not_stick(self, tmp_path):
        transport = FakeTransport(status_after="ACTIVE")
        executor = ChangePlanExecutor(
            tenant_id="flexi",
            dry_run=False,
            base_path=tmp_path,
            transport=transport,
        )
        outcomes = executor.apply(
            _plan([{"target_id": "ad1", "target_name": "Amalia", "action": "pause_ad"}])
        )

        assert outcomes[0].result == "failed"
        assert "ACTIVE" in outcomes[0].detail

    def test_unsupported_actions_are_not_executed(self, tmp_path):
        transport = FakeTransport()
        executor = ChangePlanExecutor(
            tenant_id="flexi",
            dry_run=False,
            base_path=tmp_path,
            transport=transport,
        )
        outcomes = executor.apply(
            _plan(
                [
                    {"target_id": "ad1", "target_name": "Amalia", "action": "scale_candidate"},
                    {"target_id": "ad2", "target_name": "Izadora", "action": "keep"},
                ]
            )
        )

        assert [item.result for item in outcomes] == ["unsupported"]
        assert transport.calls == []

    def test_only_filters_by_ad_id(self, tmp_path):
        transport = FakeTransport()
        executor = ChangePlanExecutor(
            tenant_id="flexi",
            dry_run=True,
            base_path=tmp_path,
            transport=transport,
            only=["ad1"],
        )
        outcomes = executor.apply(
            _plan(
                [
                    {"target_id": "ad1", "target_name": "Amalia", "action": "pause_ad"},
                    {"target_id": "ad2", "target_name": "Izadora", "action": "pause_ad"},
                ]
            )
        )

        assert len(outcomes) == 1
        assert outcomes[0].target_id == "ad1"

    def test_build_plan_from_capture(self, tmp_path):
        capture = {
            "tenant_id": "flexi",
            "campaign_id": "120247658527630665",
            "campaign_slug": "2026-11_flexi_ads_560mxn",
            "campaign_name": "Flexi OI26",
            "checkpoint": "E72",
            "elapsed_hours": 72.2,
            "scheduled_elapsed_hours": 72.0,
            "ads": [
                {
                    "ad_id": "ad1",
                    "ad_name": "Amalia",
                    "spend": 61.14,
                    "impressions": 1482,
                    "clicks": 94,
                    "ctr": 6.34,
                    "conversations": 6,
                    "cost_per_conversation": 10.19,
                }
            ],
        }
        path = tmp_path / "E72.json"
        path.write_text(json.dumps(capture), encoding="utf-8")

        plan = build_plan_from_capture(path, base_path=tmp_path)

        assert plan["checkpoint"] == "E72"
        assert plan["actions"][0]["action"] == "pause_ad"
        assert plan["actions"][0]["target_id"] == "ad1"


def test_plan_sin_aprobacion_no_escribe(tmp_path):
    transport = FakeTransport()
    plan = _plan([{"target_id": "ad1", "target_name": "Amalia", "action": "pause_ad"}])
    plan["approval"] = {"status": "pending"}

    outcomes = ChangePlanExecutor(
        tenant_id="flexi", dry_run=False, base_path=tmp_path, transport=transport
    ).apply(plan)

    assert outcomes[0].result == "not_approved"
    assert transport.calls == []


def test_aprobacion_parcial_limita_los_ads(tmp_path):
    transport = FakeTransport()
    plan = _plan(
        [
            {"target_id": "ad1", "target_name": "Amalia", "action": "pause_ad"},
            {"target_id": "ad2", "target_name": "ARISHA", "action": "pause_ad"},
        ]
    )
    plan["approval"] = {"status": "approved", "targets": ["ad2"]}

    outcomes = ChangePlanExecutor(
        tenant_id="flexi", dry_run=False, base_path=tmp_path, transport=transport
    ).apply(plan)

    assert [item.target_id for item in outcomes] == ["ad2"]
    assert transport.calls[0][1] == "ad2"
