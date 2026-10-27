"""Tests for GrowthOS enums."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "growthos"))

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
    LeadSource,
    DealStage,
    FunnelLine,
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
        assert Plataforma.TIKTOK == "TikTok"

    def test_tipo_contenido_values(self):
        assert TipoContenido.REEL == "Reel"
        assert TipoContenido.CARRUSEL == "Carrusel"

    def test_categoria_values(self):
        assert Categoria.HUMOR == "Humor"
        assert Categoria.NARRATIVA == "Narrativa"

    def test_lead_source_values(self):
        assert LeadSource.ORGANIC == "Organic"
        assert LeadSource.META_ADS == "Meta_Ads"

    def test_deal_stage_values(self):
        assert DealStage.NEW == "New"
        assert DealStage.CLOSED_WON == "Closed_Won"

    def test_funnel_line_values(self):
        assert FunnelLine.TOFU == "TOFU"
        assert FunnelLine.BOFU == "BOFU"
