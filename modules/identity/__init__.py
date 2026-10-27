"""Módulo de identidad del tenant.

Agrupa el contexto que define quién es cada cliente:

- registro y configuración de tenants
- sincronización de evidencia por tenant
- voz de marca (brand voice)

El agente de voz vive en ``modules.identity.agents.brand_voice_agent``.
"""

from modules.identity.tenant_registry import TenantRegistry, get_registry
from modules.identity.sync import (
    REDACTED_VALUE,
    SYNC_SCHEMA_VERSION,
    list_tenants,
    redact_sensitive_data,
    sanitize_saved_snapshots,
    sync_tenant,
    write_snapshot,
)

__all__ = [
    "REDACTED_VALUE",
    "SYNC_SCHEMA_VERSION",
    "TenantRegistry",
    "get_registry",
    "list_tenants",
    "redact_sensitive_data",
    "sanitize_saved_snapshots",
    "sync_tenant",
    "write_snapshot",
]
