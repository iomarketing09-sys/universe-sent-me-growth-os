"""Registro de capacidades del orquestador CGO."""

from modules.cgo.capabilities import (
    canon_sync,
    cross_tenant_report,
    daily_pipeline,
    meta_publishing,
    monetization_report,
    tenant_onboarding,
    verify_setup,
    weekly_calendar,
)

CAPABILITIES = {
    "daily_pipeline": daily_pipeline.run,
    "weekly_calendar": weekly_calendar.run,
    "tenant_onboarding": tenant_onboarding.run,
    "cross_tenant_report": cross_tenant_report.run,
    "canon_sync": canon_sync.run,
    "meta_publishing": meta_publishing.run,
    "monetization_report": monetization_report.run,
    "verify_setup": verify_setup.run,
}

ALL_TENANTS = {"cross_tenant_report", "verify_setup"}

__all__ = ["CAPABILITIES", "ALL_TENANTS"]
