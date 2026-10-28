"""Tests for GrowthOS Pydantic models and validators."""

import pytest
from datetime import date

from growthos.core.enums import (
    EstadoPieza,
    Plataforma,
    TipoContenido,
    Categoria,
    Prioridad,
    EstadoCanon,
    BloqueadoCanon,
    Reutilizable,
    EstadoProduccion,
    MotivoRevision,
)
from growthos.core.models import Piece, Publication, Experiment, MetricsSnapshot, AssetAlias
from growthos.core.validators import (
    validate_piece_id,
    validate_30_day_rule,
    validate_canon_block,
    validate_unique_ids,
    validate_state_transition,
    validate_piece_for_scheduling,
)


class TestEnums:
    """Test enum values are correct."""

    def test_estado_pieza_values(self):
        assert EstadoPieza.IDEA == "Idea"
        assert EstadoPieza.APROBADO == "Aprobado"
        assert EstadoPieza.PUBLICADO == "Publicado"

    def test_plataforma_values(self):
        assert Plataforma.FACEBOOK == "Facebook"
        assert Plataforma.INSTAGRAM == "Instagram"

    def test_tipo_contenido_values(self):
        assert TipoContenido.REEL == "Reel"
        assert TipoContenido.CARRUSEL == "Carrusel"

    def test_categoria_values(self):
        assert Categoria.HUMOR == "Humor"
        assert Categoria.NARRATIVA == "Narrativa"


class TestPieceModel:
    """Test Piece model validation."""

    def test_valid_piece(self, sample_piece_data):
        # Map PascalCase to snake_case
        piece_data = {
            "id_pieza": sample_piece_data["ID_Pieza"],
            "titulo": sample_piece_data["Titulo"],
        }
        piece = Piece(**piece_data)
        assert piece.id_pieza == "CNT-001"
        assert piece.titulo == "Test Piece"

    def test_piece_id_validation(self):
        # Valid IDs
        piece = Piece(id_pieza="CNT-001", estado_operativo=EstadoPieza.IDEA)
        assert piece.id_pieza == "CNT-001"

        # Invalid ID format
        with pytest.raises(ValueError):
            Piece(id_pieza="INVALID-001", estado_operativo=EstadoPieza.IDEA)

    def test_date_parsing(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.IDEA,
            fecha_ultima_publicacion="2026-07-29",
        )
        assert piece.fecha_ultima_publicacion == date(2026, 7, 29)

        # Different format
        piece2 = Piece(
            id_pieza="CNT-002",
            estado_operativo=EstadoPieza.IDEA,
            fecha_ultima_publicacion="07/29/2026",
        )
        assert piece2.fecha_ultima_publicacion == date(2026, 7, 29)

    def test_days_since_publication_auto_computed(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.IDEA,
            fecha_ultima_publicacion=date(2026, 7, 29),
        )
        # Days should be computed
        assert piece.dias_desde_publicacion is not None
        assert piece.dias_desde_publicacion >= 0

    def test_extra_fields_allowed(self):
        """Extra fields from CSV should be allowed."""
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.IDEA,
            unknown_field="should be ignored",
        )
        # Should not raise
        assert piece.id_pieza == "CNT-001"


class TestPublicationModel:
    """Test Publication model."""

    def test_valid_publication(self):
        pub = Publication(
            id_pieza="CNT-001",
            publicacion_id="PUB-001",
            fecha_publicacion="2026-08-15",
            plataforma=Plataforma.FACEBOOK,
            meta_post_id="123_456",
        )
        assert pub.id_pieza == "CNT-001"
        assert pub.meta_post_id == "123_456"


class TestExperimentModel:
    """Test Experiment model."""

    def test_valid_experiment(self):
        exp = Experiment(
            experiment_id="EXP-001",
            hipotesis_id="HB-001",
            id_pieza="CNT-001",
        )
        assert exp.experiment_id == "EXP-001"
        assert exp.hipotesis_id == "HB-001"


class TestMetricsSnapshotModel:
    """Test MetricsSnapshot model."""

    def test_valid_snapshot(self):
        snap = MetricsSnapshot(
            snapshot_id="SNAP-001",
            meta_post_id="123_456",
            target_at_utc="2026-08-15T10:00:00",
            window_type="E0",
        )
        assert snap.snapshot_id == "SNAP-001"
        assert snap.window_type == "E0"


class TestAssetAliasModel:
    """Test AssetAlias model."""

    def test_valid_alias(self):
        alias = AssetAlias(
            alias_id="ALIAS-001",
            asset_ref="260001",
        )
        assert alias.alias_id == "ALIAS-001"
        assert alias.asset_ref == "260001"


class TestValidators:
    """Test cross-field validators."""

    def test_validate_piece_id(self):
        assert validate_piece_id("CNT-001") is True
        assert validate_piece_id("CNT-9999") is True
        assert validate_piece_id("CNT-0000") is False
        assert validate_piece_id("CNT-10000") is False
        assert validate_piece_id("INVALID-001") is False
        assert validate_piece_id("") is False
        assert validate_piece_id(None) is False

    def test_validate_30_day_rule_reusable(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            es_reutilizable=Reutilizable.SI,
            fecha_ultima_publicacion=date(2026, 7, 1),  # ~60 days ago
        )
        assert validate_30_day_rule(piece, date(2026, 8, 30)) is True

    def test_validate_30_day_rule_not_reusable(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            es_reutilizable=Reutilizable.NO,
        )
        assert validate_30_day_rule(piece) is False

    def test_validate_30_day_rule_recent_publication(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            es_reutilizable=Reutilizable.SI,
            fecha_ultima_publicacion=date(2026, 8, 20),  # 10 days ago
        )
        assert validate_30_day_rule(piece, date(2026, 8, 30)) is False

    def test_validate_30_day_rule_never_published(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            es_reutilizable=Reutilizable.SI,
            fecha_ultima_publicacion=None,
        )
        assert validate_30_day_rule(piece) is True

    def test_validate_canon_block_explicit(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            bloqueado_canon=BloqueadoCanon.SI,
        )
        assert validate_canon_block(piece) is False

    def test_validate_canon_block_normalized_state(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            bloqueado_canon=BloqueadoCanon.NO,
            estado_canon_normalizado=EstadoCanon.BLOQUEADO,
        )
        assert validate_canon_block(piece) is False

    def test_validate_canon_block_deferred(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.DIFERIDO,
            bloqueado_canon=BloqueadoCanon.NO,
            estado_canon_normalizado=EstadoCanon.DEFERRED_OPERATIONAL,
            motivo_revision_normalizado=MotivoRevision.INVENTARIO_RECONCILIACION_PENDIENTE,
        )
        assert validate_canon_block(piece) is False

    def test_validate_canon_block_clear(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            bloqueado_canon=BloqueadoCanon.NO,
            estado_canon_normalizado=EstadoCanon.CLEAR_UNVERIFIED,
        )
        assert validate_canon_block(piece) is True

    def test_validate_unique_ids(self):
        pieces = [
            Piece(id_pieza="CNT-001", estado_operativo=EstadoPieza.IDEA),
            Piece(id_pieza="CNT-002", estado_operativo=EstadoPieza.IDEA),
            Piece(id_pieza="CNT-001", estado_operativo=EstadoPieza.IDEA),  # Duplicate
        ]
        dupes = validate_unique_ids(pieces)
        assert dupes == ["CNT-001"]

    def test_validate_state_transition(self):
        # Valid transitions
        assert validate_state_transition(EstadoPieza.IDEA, EstadoPieza.PENDIENTE_PRODUCCION) is True
        assert validate_state_transition(EstadoPieza.APROBADO, EstadoPieza.PROGRAMADO) is True
        assert validate_state_transition(EstadoPieza.PROGRAMADO, EstadoPieza.PUBLICADO) is True

        # Invalid transitions
        assert validate_state_transition(EstadoPieza.IDEA, EstadoPieza.PUBLICADO) is False
        assert validate_state_transition(EstadoPieza.ARCHIVADO, EstadoPieza.APROBADO) is False

    def test_validate_piece_for_scheduling_valid(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.APROBADO,
            bloqueado_canon=BloqueadoCanon.NO,
            personaje_principal="@char_USM_universe",
            tipo_contenido=TipoContenido.REEL,
            plataforma_principal=Plataforma.FACEBOOK,
            asset_ref_confirmado="260001",
        )
        valid, errors = validate_piece_for_scheduling(piece)
        assert valid is True
        assert errors == []

    def test_validate_piece_for_scheduling_invalid(self):
        piece = Piece(
            id_pieza="CNT-001",
            estado_operativo=EstadoPieza.IDEA,  # Not approved
            bloqueado_canon=BloqueadoCanon.NO,
        )
        valid, errors = validate_piece_for_scheduling(piece)
        assert valid is False
        assert any("Aprobado" in e for e in errors)
