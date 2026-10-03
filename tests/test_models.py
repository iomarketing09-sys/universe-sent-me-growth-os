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
        piece = Piece(**sample_piece_data)
        assert piece.ID_Pieza == "CNT-001"
        assert piece.Titulo == "Test Piece"
        assert piece.Personaje_Principal == "@char_USM_universe"

    def test_piece_id_validation(self):
        # Valid IDs
        piece = Piece(ID_Pieza="CNT-001", Estado=EstadoPieza.IDEA)
        assert piece.ID_Pieza == "CNT-001"

        # Invalid ID format
        with pytest.raises(ValueError):
            Piece(ID_Pieza="INVALID-001", Estado=EstadoPieza.IDEA)

    def test_date_parsing(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.IDEA,
            Fecha_Ultima_Publicacion="2026-07-29",
        )
        assert piece.Fecha_Ultima_Publicacion == date(2026, 7, 29)

        # Different format
        piece2 = Piece(
            ID_Pieza="CNT-002",
            Estado=EstadoPieza.IDEA,
            Fecha_Ultima_Publicacion="07/29/2026",
        )
        assert piece2.Fecha_Ultima_Publicacion == date(2026, 7, 29)

    def test_days_since_publication_auto_computed(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.IDEA,
            Fecha_Ultima_Publicacion=date(2026, 7, 29),
        )
        # Days should be computed
        assert piece.Dias_Desde_Publicacion is not None
        assert piece.Dias_Desde_Publicacion >= 0

    def test_extra_fields_allowed(self):
        """Extra fields from CSV should be allowed."""
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.IDEA,
            unknown_field="should be ignored",
        )
        # Should not raise
        assert piece.ID_Pieza == "CNT-001"


class TestPublicationModel:
    """Test Publication model."""

    def test_valid_publication(self):
        pub = Publication(
            ID_Pieza="CNT-001",
            Publicacion_ID="PUB-001",
            Fecha_Publicacion="2026-08-15",
            Plataforma=Plataforma.FACEBOOK,
            Meta_Post_ID="123_456",
        )
        assert pub.ID_Pieza == "CNT-001"
        assert pub.Meta_Post_ID == "123_456"


class TestExperimentModel:
    """Test Experiment model."""

    def test_valid_experiment(self):
        exp = Experiment(
            Experiment_ID="EXP-001",
            Hipotesis_ID="HB-001",
            ID_Pieza="CNT-001",
        )
        assert exp.Experiment_ID == "EXP-001"
        assert exp.Hipotesis_ID == "HB-001"


class TestMetricsSnapshotModel:
    """Test MetricsSnapshot model."""

    def test_valid_snapshot(self):
        snap = MetricsSnapshot(
            Snapshot_ID="SNAP-001",
            Meta_Post_ID="123_456",
            Target_At_UTC="2026-08-15T10:00:00",
            Window_Type="E0",
        )
        assert snap.Snapshot_ID == "SNAP-001"
        assert snap.Window_Type == "E0"


class TestAssetAliasModel:
    """Test AssetAlias model."""

    def test_valid_alias(self):
        alias = AssetAlias(
            Alias_ID="ALIAS-001",
            Asset_Ref="260001",
        )
        assert alias.Alias_ID == "ALIAS-001"
        assert alias.Asset_Ref == "260001"


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
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Es_Reutilizable=Reutilizable.SI,
            Fecha_Ultima_Publicacion=date(2026, 7, 1),  # ~60 days ago
        )
        assert validate_30_day_rule(piece, date(2026, 8, 30)) is True

    def test_validate_30_day_rule_not_reusable(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Es_Reutilizable=Reutilizable.NO,
        )
        assert validate_30_day_rule(piece) is False

    def test_validate_30_day_rule_recent_publication(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Es_Reutilizable=Reutilizable.SI,
            Fecha_Ultima_Publicacion=date(2026, 8, 20),  # 10 days ago
        )
        assert validate_30_day_rule(piece, date(2026, 8, 30)) is False

    def test_validate_30_day_rule_never_published(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Es_Reutilizable=Reutilizable.SI,
            Fecha_Ultima_Publicacion=None,
        )
        assert validate_30_day_rule(piece) is True

    def test_validate_canon_block_explicit(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Bloqueado_Canon=BloqueadoCanon.SI,
        )
        assert validate_canon_block(piece) is False

    def test_validate_canon_block_normalized_state(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Bloqueado_Canon=BloqueadoCanon.NO,
            Estado_Canon_Normalizado=EstadoCanon.BLOQUEADO,
        )
        assert validate_canon_block(piece) is False

    def test_validate_canon_block_deferred(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.DIFERIDO,
            Bloqueado_Canon=BloqueadoCanon.NO,
            Estado_Canon_Normalizado=EstadoCanon.DEFERRED_OPERATIONAL,
            Motivo_Revision_Normalizado=MotivoRevision.INVENTARIO_RECONCILIACION_PENDIENTE,
        )
        assert validate_canon_block(piece) is False

    def test_validate_canon_block_clear(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Bloqueado_Canon=BloqueadoCanon.NO,
            Estado_Canon_Normalizado=EstadoCanon.CLEAR_UNVERIFIED,
        )
        assert validate_canon_block(piece) is True

    def test_validate_unique_ids(self):
        pieces = [
            Piece(ID_Pieza="CNT-001", Estado=EstadoPieza.IDEA),
            Piece(ID_Pieza="CNT-002", Estado=EstadoPieza.IDEA),
            Piece(ID_Pieza="CNT-001", Estado=EstadoPieza.IDEA),  # Duplicate
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
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.APROBADO,
            Bloqueado_Canon=BloqueadoCanon.NO,
            Personaje_Principal="@char_USM_universe",
            Tipo_Contenido=TipoContenido.REEL,
            Plataforma=Plataforma.FACEBOOK,
            Asset_Ref_Confirmado="260001",
        )
        valid, errors = validate_piece_for_scheduling(piece)
        assert valid is True
        assert errors == []

    def test_validate_piece_for_scheduling_invalid(self):
        piece = Piece(
            ID_Pieza="CNT-001",
            Estado=EstadoPieza.IDEA,  # Not approved
            Bloqueado_Canon=BloqueadoCanon.NO,
        )
        valid, errors = validate_piece_for_scheduling(piece)
        assert valid is False
        assert any("Aprobado" in e for e in errors)
