"""Núcleo de política puro para G-SEC-2.11.

Diseño recordatorio: solo validar entradas abstractas y reducirlas a una
categoría agregada. Este módulo no consulta procesos, archivos, red, servicios,
variables de entorno ni mecanismos externos; tampoco persiste resultados.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Sequence


class AggregateOutcome(str, Enum):
    """Las únicas salidas públicas permitidas por G-SEC-2.11."""

    SCOPE_MISMATCH = "scope_mismatch"
    OBSERVATION_INCOMPLETE_OR_BLOCKED = "observation_incomplete_or_blocked"
    REGISTERED_EXECUTION_CANDIDATE_OBSERVED = (
        "registered_execution_candidate_observed"
    )
    REGISTERED_NON_EXECUTION_OBSERVED = "registered_non_execution_observed"


class ComponentKind(str, Enum):
    """Categorías cerradas admisibles para una entrada ya autorizada."""

    SERVICE = "service"
    AUTOMATION = "automation"
    DEDICATED_WRAPPER = "dedicated_wrapper"
    DEDICATED_PROCESS = "dedicated_process"


class DirectedState(str, Enum):
    """Estado abstracto, sin detalles técnicos de una consulta dirigida."""

    PRESENT = "present"
    NOT_PRESENT = "not_present"


@dataclass(frozen=True)
class ReviewContext:
    """Confirma en memoria que los tres documentos aplicables están en Review."""

    gate_reviewed: bool
    specification_reviewed: bool
    code_contract_reviewed: bool


@dataclass(frozen=True)
class WindowAuthorization:
    """Contexto lógico de una autorización puntual; no contiene identidad ni fecha."""

    is_one_time: bool
    is_current: bool
    scope_matches_registry: bool


@dataclass(frozen=True)
class RegistryEntry:
    """Entrada abstracta y no sensible de un registro temporal autorizado."""

    label: str
    kind: ComponentKind
    exact_public_name: str


@dataclass(frozen=True)
class DirectedObservation:
    """Respuesta abstracta por etiqueta, sin PID, ruta, usuario ni texto fuente."""

    label: str
    state: DirectedState


_SAFE_LABEL = re.compile(r"^[a-z][a-z0-9_-]{2,63}$")


def evaluate_policy(
    review: ReviewContext,
    authorization: WindowAuthorization,
    registry: Sequence[RegistryEntry],
    observations: Sequence[DirectedObservation],
) -> AggregateOutcome:
    """Aplicar la precedencia fail-closed a valores ya abstractos y en memoria.

    Esta función no realiza observaciones. Recibe estados que otro componente no
    definido tendría que haber reducido previamente a ``present`` o
    ``not_present``. Su única salida es una categoría agregada.
    """

    registry_scope = _registry_scope_outcome(registry)
    if registry_scope is not None:
        return registry_scope

    observation_scope = _observation_scope_outcome(registry, observations)
    if observation_scope is not None:
        return observation_scope

    if not _review_is_complete(review):
        return AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED

    if not _authorization_is_valid(authorization):
        return AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED

    if len(registry) == 0 or len(observations) != len(registry):
        return AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED

    if any(item.state is DirectedState.PRESENT for item in observations):
        return AggregateOutcome.REGISTERED_EXECUTION_CANDIDATE_OBSERVED

    return AggregateOutcome.REGISTERED_NON_EXECUTION_OBSERVED


def _registry_scope_outcome(
    registry: Sequence[RegistryEntry],
) -> AggregateOutcome | None:
    """Rechazar el exceso de alcance antes de considerar bloqueos operativos."""

    labels: set[str] = set()
    for entry in registry:
        if not isinstance(entry, RegistryEntry):
            return AggregateOutcome.SCOPE_MISMATCH
        if not isinstance(entry.kind, ComponentKind):
            return AggregateOutcome.SCOPE_MISMATCH
        if not _is_safe_identifier(entry.label):
            return AggregateOutcome.SCOPE_MISMATCH
        if not _is_safe_identifier(entry.exact_public_name):
            return AggregateOutcome.SCOPE_MISMATCH
        if entry.label in labels:
            return AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED
        labels.add(entry.label)
    return None


def _observation_scope_outcome(
    registry: Sequence[RegistryEntry],
    observations: Sequence[DirectedObservation],
) -> AggregateOutcome | None:
    """Aceptar exclusivamente respuestas abstractas de etiquetas registradas."""

    allowed_labels = {entry.label for entry in registry}
    observed_labels: set[str] = set()
    for observation in observations:
        if not isinstance(observation, DirectedObservation):
            return AggregateOutcome.SCOPE_MISMATCH
        if observation.label not in allowed_labels:
            return AggregateOutcome.SCOPE_MISMATCH
        if observation.label in observed_labels:
            return AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED
        if not isinstance(observation.state, DirectedState):
            return AggregateOutcome.SCOPE_MISMATCH
        observed_labels.add(observation.label)
    return None


def _review_is_complete(review: ReviewContext) -> bool:
    return (
        isinstance(review, ReviewContext)
        and review.gate_reviewed
        and review.specification_reviewed
        and review.code_contract_reviewed
    )


def _authorization_is_valid(authorization: WindowAuthorization) -> bool:
    return (
        isinstance(authorization, WindowAuthorization)
        and authorization.is_one_time
        and authorization.is_current
        and authorization.scope_matches_registry
    )


def _is_safe_identifier(value: object) -> bool:
    """Aceptar solo identificadores cerrados, no rutas ni valores libres."""

    return isinstance(value, str) and bool(_SAFE_LABEL.fullmatch(value))
