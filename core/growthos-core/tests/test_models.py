"""Tests for GrowthOS Pydantic models and validators."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "growthos"))

from datetime import date
import pytest

from growthos.core.enums import (
    EstadoPieza,
    Plataforma,
    TipoContenido,
    Categoria,
    Prioridad,
    DificultadProduccion,
    Reutilizable,
    BloqueadoCanon,
    EstadoCanon,
    EstadoProduccion,
    EstadoPublicacion,
    MotivoRevision,
    ReconciliacionEstado,
    ReconciliacionConfianza,
)
from growthos.core.models import Piece, Publication, Experiment, MetricsSnapshot, AssetAlias, Deal


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

    def test_valid_piece(self):
        piece = Piece(
            id_pieza="CNT-001",
            titulo="Test Piece",
            personaje_principal="@char_USM_universe",
            estado_operativo=EstadoPieza.IDEA,
        )
        assert piece.id_pieza == "CNT-001"
        assert piece.titulo == "Test Piece"
        assert piece.personaje_principal == "@char_USM_universe"

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


class TestPublicationModel:
    """Test Publication model."""

    def test_valid_publication(self):
        pub = Publication(
            id_pieza="CNT-001",
            publicacion_id="PUB-001",
            fecha_publicacion="2026-10-15",
            plataforma=Plataforma.INSTAGRAM,
        )
        assert pub.id_pieza == "CNT-001"
        assert pub.plataforma == Plataforma.INSTAGRAM


class TestExperimentModel:
    """Test Experiment model."""

    def test_valid_experiment(self):
        exp = Experiment(
            experiment_id="EXP-001",
            hipotesis_id="HB-001",
            id_pieza="CNT-001",
            vistas=1000,
        )
        assert exp.experiment_id == "EXP-001"
        assert exp.vistas == 1000


class TestMetricsSnapshotModel:
    """Test MetricsSnapshot model."""

    def test_valid_snapshot(self):
        snap = MetricsSnapshot(
            snapshot_id="SNAP-001",
            meta_post_id="POST-001",
            target_at_utc="2026-10-15T12:00:00Z",
            window_type="E24",
            reactions=100,
        )
        assert snap.snapshot_id == "SNAP-001"
        assert snap.reactions == 100


class TestAssetAliasModel:
    """Test AssetAlias model."""

    def test_valid_alias(self):
        alias = AssetAlias(
            alias_id="ALIAS-001",
            asset_ref="CNT-001",
        )
        assert alias.alias_id == "ALIAS-001"
        assert alias.asset_ref == "CNT-001"


class TestDealModel:
    """Test Deal model."""

    def test_valid_deal(self):
        deal = Deal(
            deal_id="DEAL-001",
            tenant_id="flexi",
            lead_source="Meta_Ads",
            amount=500.0,
        )
        assert deal.deal_id == "DEAL-001"
        assert deal.tenant_id == "flexi"
        assert deal.amount == 500.0
