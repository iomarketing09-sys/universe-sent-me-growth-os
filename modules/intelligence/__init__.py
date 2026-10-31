"""Módulo intelligence: métricas, histórico, experimentos, planner y auditoría.

Expone la lectura de resultados (Meta Ads, snapshots), el baseline histórico y
las reglas de planificación. El agente de ads vive en ``agents/meta_ads_agent``.
"""

from __future__ import annotations

__all__ = [
    "MetricsSnapshot",
    "SnapshotWindow",
    "SnapshotStatus",
    "load_tenant_env",
    "run_capture_cycle",
    "get_historical_reuse_info",
    "get_performance_by_personaje",
    "load_horario_performance",
    "Observacion",
    "Hipotesis",
    "build_schedule",
    "ScheduleItem",
    "run_audit",
    "validate_publications_csv",
    "capture_ads_insights",
    "record_ad_insights",
    "load_ad_insights",
    "latest_by_ad",
    "ledger_path",
    "discover_campaigns",
    "checkpoint_schedule",
    "run_due_captures",
    "build_change_plan",
    "render_plan_markdown",
    "load_campaign_policy",
    "MetaAdsAgent",
    "audit_tenant",
]

_EXPORTS = {
    "MetricsSnapshot": ("modules.intelligence.metrics_snapshot", "MetricsSnapshot"),
    "SnapshotWindow": ("modules.intelligence.metrics_snapshot", "SnapshotWindow"),
    "SnapshotStatus": ("modules.intelligence.metrics_snapshot", "SnapshotStatus"),
    "load_tenant_env": ("modules.intelligence.metrics_snapshot", "load_tenant_env"),
    "run_capture_cycle": ("modules.intelligence.metrics_snapshot", "run_capture_cycle"),
    "get_historical_reuse_info": (
        "modules.intelligence.historical_baseline",
        "get_historical_reuse_info",
    ),
    "get_performance_by_personaje": (
        "modules.intelligence.historical_baseline",
        "get_performance_by_personaje",
    ),
    "load_horario_performance": (
        "modules.intelligence.historical_baseline",
        "load_horario_performance",
    ),
    "Observacion": ("modules.intelligence.experiment_log", "Observacion"),
    "Hipotesis": ("modules.intelligence.experiment_log", "Hipotesis"),
    "build_schedule": ("modules.intelligence.planner", "build_schedule"),
    "ScheduleItem": ("modules.intelligence.planner", "ScheduleItem"),
    "run_audit": ("modules.intelligence.audit", "run_audit"),
    "validate_publications_csv": ("modules.intelligence.audit", "validate_publications_csv"),
    "capture_ads_insights": ("modules.intelligence.ads_adapters", "capture_ads_insights"),
    "record_ad_insights": ("modules.intelligence.ads_ledger", "record_ad_insights"),
    "load_ad_insights": ("modules.intelligence.ads_ledger", "load_ad_insights"),
    "latest_by_ad": ("modules.intelligence.ads_ledger", "latest_by_ad"),
    "ledger_path": ("modules.intelligence.ads_ledger", "ledger_path"),
    "discover_campaigns": ("modules.intelligence.campaign_capture", "discover_campaigns"),
    "checkpoint_schedule": ("modules.intelligence.campaign_capture", "checkpoint_schedule"),
    "run_due_captures": ("modules.intelligence.campaign_capture", "run_due_captures"),
    "build_change_plan": (
        "modules.intelligence.campaign_optimizer",
        "build_change_plan",
    ),
    "render_plan_markdown": (
        "modules.intelligence.campaign_optimizer",
        "render_plan_markdown",
    ),
    "load_campaign_policy": ("modules.intelligence.campaign_optimizer", "load_policy"),
    "MetaAdsAgent": ("modules.intelligence.agents.meta_ads_agent", "MetaAdsAgent"),
    "audit_tenant": ("modules.intelligence.agents.tenant_auditor", "audit_tenant"),
}


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    module_name, attribute = _EXPORTS[name]
    return getattr(importlib.import_module(module_name), attribute)
