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
    if piece.Es_Reutilizable != Reutilizable.SI:
        return False

    if not piece.Fecha_Ultima_Publicacion:
        return True  # Never published, can be used

    ref = reference_date or date.today()
    days_since = (ref - piece.Fecha_Ultima_Publicacion).days
    return days_since >= 30


def validate_canon_block(piece: Piece) -> bool:
    """
    Validate canon block rule.
    Returns True if piece is NOT blocked by canon.
    """
    # Check explicit block flag
    if piece.Bloqueado_Canon == BloqueadoCanon.SI:
        return False

    # Check normalized canon state
    blocked_states = {
        EstadoCanon.BLOQUEADO,
        EstadoCanon.REVIEW_REQUIRED,
        EstadoCanon.CONTRADICCION_SUSTANTIVA,
        EstadoCanon.DEFERRED_OPERATIONAL,
    }
    if piece.Estado_Canon_Normalizado in blocked_states:
        return False

    # Check operational state for canon-related blocks
    if piece.Estado in {EstadoPieza.BLOQUEADO, EstadoPieza.DIFERIDO}:
        # Check if it's canon-related
        if piece.Motivo_Revision_Normalizado in {
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
        if piece.ID_Pieza in seen:
            duplicates.append(piece.ID_Pieza)
        else:
            seen.add(piece.ID_Pieza)
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

    if piece.Estado != EstadoPieza.APROBADO:
        errors.append(f"Piece must be Aprobado, current: {piece.Estado}")

    if not validate_canon_block(piece):
        errors.append("Piece is blocked by canon")

    if not piece.Personaje_Principal:
        errors.append("Missing Personaje_Principal")

    if not piece.Tipo_Contenido:
        errors.append("Missing Tipo_Contenido")

    if not piece.Plataforma:
        errors.append("Missing Plataforma")

    if not piece.Asset_Ref_Confirmado and not piece.Asset_Ref_Candidato:
        errors.append("Missing asset reference")

    return len(errors) == 0, errors
