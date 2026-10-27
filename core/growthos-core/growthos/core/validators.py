"""Cross-field validators and business rules for GrowthOS."""

from datetime import date
from typing import Optional

from growthos.core.enums import EstadoPieza, BloqueadoCanon, EstadoCanon, Reutilizable
from growthos.core.models import Piece


def validate_piece_id(piece_id: str) -> bool:
    """Validate CNT-#### format."""
    if not piece_id:
        return False
    if not piece_id.startswith("CNT-"):
        return False
    try:
        num = int(piece_id[4:])
        return 1 <= num <= 9999
    except ValueError:
        return False


def validate_30_day_rule(piece: Piece, reference_date: Optional[date] = None) -> bool:
    """
    Validate 30-day reuse rule.
    Returns True if piece can be reused (30+ days since last publication).
    """
    if piece.es_reutilizable != Reutilizable.SI:
        return False

    if not piece.fecha_ultima_publicacion:
        return True  # Never published, can be used

    ref = reference_date or date.today()
    days_since = (ref - piece.fecha_ultima_publicacion).days
    return days_since >= 30


def validate_canon_block(piece: Piece) -> bool:
    """
    Validate canon block rule.
    Returns True if piece is NOT blocked by canon.
    """
    # Check explicit block flag
    if piece.bloqueado_canon == BloqueadoCanon.SI:
        return False

    # Check normalized canon state
    blocked_states = {
        EstadoCanon.BLOQUEADO,
        EstadoCanon.REVIEW_REQUIRED,
        EstadoCanon.CONTRADICCION_SUSTANTIVA,
        EstadoCanon.DEFERRED_OPERATIONAL,
    }
    if piece.estado_canon_normalizado in blocked_states:
        return False

    # Check operational state for canon-related blocks
    if piece.estado_operativo in {EstadoPieza.BLOQUEADO, EstadoPieza.DIFERIDO}:
        # Check if it's canon-related
        if piece.motivo_revision_normalizado in {
            "Canon_Contradiccion_Sustantiva",
            "Canon_Review_Required",
            "Deferred_Operational",
        }:
            return False

    return True


def validate_unique_ids(pieces: list[Piece]) -> list[str]:
    """Check for duplicate CNT IDs. Returns list of duplicate IDs."""
    seen = set()
    duplicates = []
    for piece in pieces:
        if piece.id_pieza in seen:
            duplicates.append(piece.id_pieza)
        else:
            seen.add(piece.id_pieza)
    return duplicates


def validate_state_transition(current: EstadoPieza, target: EstadoPieza) -> bool:
    """Validate allowed state transitions per state machine."""
    allowed = {
        EstadoPieza.IDEA: {EstadoPieza.PENDIENTE_PRODUCCION},
        EstadoPieza.PENDIENTE_PRODUCCION: {
            EstadoPieza.EN_PRODUCCION,
            EstadoPieza.RECHAZADO,
        },
        EstadoPieza.EN_PRODUCCION: {
            EstadoPieza.PENDIENTE_REVISION_CLAUDE,
            EstadoPieza.RECHAZADO,
        },
        EstadoPieza.PENDIENTE_REVISION_CLAUDE: {
            EstadoPieza.PENDIENTE_APROBACION_FERNANDO,
            EstadoPieza.RECHAZADO,
        },
        EstadoPieza.PENDIENTE_APROBACION_FERNANDO: {
            EstadoPieza.APROBADO,
            EstadoPieza.RECHAZADO,
        },
        EstadoPieza.APROBADO: {EstadoPieza.PROGRAMADO},
        EstadoPieza.PROGRAMADO: {EstadoPieza.PUBLICADO, EstadoPieza.RECHAZADO},
        EstadoPieza.PUBLICADO: {EstadoPieza.EN_ANALISIS, EstadoPieza.ARCHIVADO},
        EstadoPieza.EN_ANALISIS: {
            EstadoPieza.ARCHIVADO,
            EstadoPieza.REUTILIZADO_ARCHIVADO,
        },
        EstadoPieza.RECHAZADO: {EstadoPieza.EN_PRODUCCION, EstadoPieza.ARCHIVADO},
        EstadoPieza.DIFERIDO: {EstadoPieza.PENDIENTE_PRODUCCION, EstadoPieza.ARCHIVADO},
        EstadoPieza.BLOQUEADO: {EstadoPieza.PENDIENTE_PRODUCCION, EstadoPieza.ARCHIVADO},
        EstadoPieza.ARCHIVADO: set(),
        EstadoPieza.REUTILIZADO_ARCHIVADO: set(),
    }
    return target in allowed.get(current, set())


def validate_piece_for_scheduling(piece: Piece) -> tuple[bool, list[str]]:
    """
    Validate piece is ready for scheduling.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    if piece.estado_operativo != EstadoPieza.APROBADO:
        errors.append(f"Piece must be Aprobado, current: {piece.estado_operativo}")

    if not validate_canon_block(piece):
        errors.append("Piece is blocked by canon")

    if not piece.personaje_principal:
        errors.append("Missing Personaje_Principal")

    if not piece.tipo_contenido:
        errors.append("Missing Tipo_Contenido")

    if not piece.plataforma_principal:
        errors.append("Missing Plataforma")

    if not piece.asset_ref_confirmado and not piece.asset_ref_candidato:
        errors.append("Missing asset reference")

    return len(errors) == 0, errors
