"""Runner sintético puro para G-SEC-2.11.

Diseño recordatorio: este archivo solo evalúa los cinco casos abstractos ya
definidos. No abre archivos, no consulta procesos, servicios, red o entorno, no
persiste resultados y no contiene una interfaz de línea de comandos.
"""

from __future__ import annotations

from dataclasses import dataclass

from policy_core_gsec211 import (
    AggregateOutcome,
    ComponentKind,
    DirectedObservation,
    DirectedState,
    RegistryEntry,
    ReviewContext,
    WindowAuthorization,
    evaluate_policy,
)


@dataclass(frozen=True)
class SyntheticCaseResult:
    """Resultado efímero y agregado de un caso sintético abstracto."""

    case_id: str
    passed: bool


_REVIEWED = ReviewContext(True, True, True)
_AUTHORIZED = WindowAuthorization(True, True, True)
_SYNTHETIC_REGISTRY = (
    RegistryEntry("synthetic_alpha", ComponentKind.SERVICE, "public_alpha"),
)


def run_synthetic_cases() -> tuple[SyntheticCaseResult, ...]:
    """Evaluar los cinco casos sintéticos sin E/S, procesos, red ni persistencia."""

    absent = (DirectedObservation("synthetic_alpha", DirectedState.NOT_PRESENT),)
    present = (DirectedObservation("synthetic_alpha", DirectedState.PRESENT),)
    invalid_registry = (
        RegistryEntry("synthetic_alpha", ComponentKind.SERVICE, "not/allowed"),
    )

    cases = (
        (
            "empty_registry_blocks",
            evaluate_policy(_REVIEWED, _AUTHORIZED, (), ()),
            AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED,
        ),
        (
            "out_of_scope_identifier_stops",
            evaluate_policy(_REVIEWED, _AUTHORIZED, invalid_registry, ()),
            AggregateOutcome.SCOPE_MISMATCH,
        ),
        (
            "missing_authorization_blocks",
            evaluate_policy(
                _REVIEWED,
                WindowAuthorization(False, True, True),
                _SYNTHETIC_REGISTRY,
                absent,
            ),
            AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED,
        ),
        (
            "abstract_presence_is_candidate",
            evaluate_policy(_REVIEWED, _AUTHORIZED, _SYNTHETIC_REGISTRY, present),
            AggregateOutcome.REGISTERED_EXECUTION_CANDIDATE_OBSERVED,
        ),
        (
            "complete_abstract_absence_is_limited",
            evaluate_policy(_REVIEWED, _AUTHORIZED, _SYNTHETIC_REGISTRY, absent),
            AggregateOutcome.REGISTERED_NON_EXECUTION_OBSERVED,
        ),
    )

    return tuple(
        SyntheticCaseResult(case_id=case_id, passed=actual is expected)
        for case_id, actual, expected in cases
    )


def all_synthetic_cases_pass(
    results: tuple[SyntheticCaseResult, ...],
) -> bool:
    """Reducir el reporte efímero a una sola respuesta lógica."""

    return len(results) == 5 and all(result.passed for result in results)
