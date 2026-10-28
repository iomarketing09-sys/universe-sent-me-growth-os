"""Auditoría local de tenants (onboarding de CGO)."""

from modules.intelligence.agents.tenant_auditor.agent import (
    BLOCKED,
    PARTIAL,
    READY,
    audit_tenant,
)

__all__ = ["audit_tenant", "READY", "PARTIAL", "BLOCKED"]
