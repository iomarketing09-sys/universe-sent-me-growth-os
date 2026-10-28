"""Módulo CGO: orquestador del Growth OS.

Es el único módulo que importa a los demás. No duplica reglas de negocio: cada
capacidad delega en el módulo dueño (social, identity, creative,
communications, intelligence) y devuelve un ``CgoResult`` uniforme.
"""

from modules.cgo.orchestrator import CgoOrchestrator
from modules.cgo.result import (
    BLOCKED,
    ERROR,
    NOT_CONFIGURED,
    OK,
    PARTIAL,
    CgoContext,
    CgoResult,
    GateResult,
)
from modules.cgo.tracks import (
    NATIVE_DIGITAL,
    PHYSICAL_CRO,
    capability_allowed,
    tenant_track,
)

__all__ = [
    "CgoOrchestrator",
    "CgoContext",
    "CgoResult",
    "GateResult",
    "OK",
    "PARTIAL",
    "BLOCKED",
    "NOT_CONFIGURED",
    "ERROR",
    "NATIVE_DIGITAL",
    "PHYSICAL_CRO",
    "capability_allowed",
    "tenant_track",
]
