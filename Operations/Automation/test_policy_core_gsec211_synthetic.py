"""Pruebas sintéticas no ejecutadas para el núcleo puro G-SEC-2.11.

Diseño recordatorio: los casos usan únicamente etiquetas abstractas. No hay
procesos, rutas, red, archivos, datos reales ni llamadas al sistema.
"""

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


REVIEWED = ReviewContext(True, True, True)
AUTHORIZED = WindowAuthorization(True, True, True)
SYNTHETIC_REGISTRY = (
    RegistryEntry("synthetic_alpha", ComponentKind.SERVICE, "public_alpha"),
)


def test_empty_registry_blocks_without_a_positive_result() -> None:
    assert (
        evaluate_policy(REVIEWED, AUTHORIZED, (), ())
        is AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED
    )


def test_out_of_scope_identifier_stops_before_observation() -> None:
    invalid_registry = (
        RegistryEntry("synthetic_alpha", ComponentKind.SERVICE, "not/allowed"),
    )
    assert (
        evaluate_policy(REVIEWED, AUTHORIZED, invalid_registry, ())
        is AggregateOutcome.SCOPE_MISMATCH
    )


def test_missing_authorization_blocks_even_with_abstract_absence() -> None:
    absent = (DirectedObservation("synthetic_alpha", DirectedState.NOT_PRESENT),)
    assert (
        evaluate_policy(
            REVIEWED,
            WindowAuthorization(False, True, True),
            SYNTHETIC_REGISTRY,
            absent,
        )
        is AggregateOutcome.OBSERVATION_INCOMPLETE_OR_BLOCKED
    )


def test_abstract_presence_stops_as_a_candidate() -> None:
    present = (DirectedObservation("synthetic_alpha", DirectedState.PRESENT),)
    assert (
        evaluate_policy(REVIEWED, AUTHORIZED, SYNTHETIC_REGISTRY, present)
        is AggregateOutcome.REGISTERED_EXECUTION_CANDIDATE_OBSERVED
    )


def test_complete_abstract_absence_is_limited_to_the_registry() -> None:
    absent = (DirectedObservation("synthetic_alpha", DirectedState.NOT_PRESENT),)
    assert (
        evaluate_policy(REVIEWED, AUTHORIZED, SYNTHETIC_REGISTRY, absent)
        is AggregateOutcome.REGISTERED_NON_EXECUTION_OBSERVED
    )
