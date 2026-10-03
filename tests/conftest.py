"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest

from growthos.config import Settings
from growthos.storage.database import Database
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


@pytest.fixture(scope="session")
def test_settings():
    """Test settings with temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_growthos.db"
        settings = Settings(
            USE_SQLITE=True,
            DATABASE_URL=f"sqlite:///{db_path}",
            MOCK_META_API=True,
            CSV_ROUNDTRIP_STRICT=True,
        )
        yield settings


@pytest.fixture(scope="function")
def test_db(test_settings):
    """Function-scoped test database."""
    db = Database(db_path=test_settings.sqlite_path)
    db.init_schema()
    yield db
    db.close()


@pytest.fixture
def sample_piece_data():
    """Sample piece data matching Content_Inventory.csv structure (already normalized)."""
    return {
        "ID_Pieza": "CNT-001",
        "Titulo": "Test Piece",
        "Personaje_Principal": "@char_USM_universe",
        "Personajes_Secundarios": "",
        "Tipo_Contenido": TipoContenido.REEL_MEME_ADAPTADO,
        "Plataforma": Plataforma.MULTI,
        "Objetivo": "Test objective",
        "Hipotesis_ID": "",
        "Estado": EstadoPieza.APROBADO,
        "Prioridad": Prioridad.ALTA,
        "Dificultad_Produccion": DificultadProduccion.BAJA,
        "Es_Reutilizable": Reutilizable.SI,
        "Fecha_Ultima_Publicacion": "2026-07-29",
        "Fuente": "08_Production/Reels/Reel_001.md",
        "Formato": "9:16, ~9s, 3 shots",
        "Categoria": Categoria.HUMOR_MEME,
        "Bloqueado_Canon": BloqueadoCanon.SI,
        "Estado_Operacion_Normalizado": EstadoProduccion.NO_CONFIRMED_MATCH,
        "Estado_Canon_Normalizado": EstadoCanon.CLEAR_UNVERIFIED,
        "Asset_Ref_Confirmado": "",
        "Asset_Ref_Candidato": "",
        "Reconciliacion_Estado": ReconciliacionEstado.NO_CONFIRMED_MATCH,
        "Reconciliacion_Confianza": ReconciliacionConfianza.NONE,
        "Reconciliacion_Fuente": "",
        "Reconciliacion_Nota": "Test note",
        "Registro_Relacionado": "",
        "Drive_Reference_ID": "",
        "Meta_Publication_ID": "",
        "Meta_Permalink": "",
        "Asset_Set": "",
        "Asset_Ref": "",
        "Asset_Filename": "",
        "Drive_ID": "",
        "Estado_Canon": EstadoCanon.REVISION,
        "Estado_Produccion": EstadoProduccion.ASSET_LISTO,
        "Estado_Publicacion": EstadoPublicacion.NO_PUBLICADA,
        "Ultima_Sincronizacion": "2026-08-15",
        "Motivo_Revision_Normalizado": MotivoRevision.INVENTARIO_RECONCILIACION_PENDIENTE,
        "Personaje_Principal_Normalizado": "Universe",
        "Personajes_Secundarios_Normalizados": "Ninguno",
        "Rol_Narrativo": "Protagonista",
        "Tipo_Humor_Normalizado": "Fandom o referencia",
        "Potencial_Etiquetado": "Medio",
        "Confianza_Taxonomia": "Alta",
        "Fuente_Taxonomia": "Inventario + reglas taxonómicas",
        "Nota_Taxonomia": "Test note",
    }


@pytest.fixture
def sample_pieces_csv(sample_piece_data):
    """Create a temporary CSV file with sample data."""
    import csv

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sample_piece_data.keys())
        writer.writeheader()
        writer.writerow(sample_piece_data)
        # Add a second row
        row2 = sample_piece_data.copy()
        row2["ID_Pieza"] = "CNT-002"
        row2["Titulo"] = "Test Piece 2"
        row2["Personaje_Principal"] = "@char_USM_wilfred"
        row2["Estado"] = EstadoPieza.PENDIENTE_PRODUCCION
        row2["Bloqueado_Canon"] = BloqueadoCanon.NO
        row2["Estado_Canon_Normalizado"] = EstadoCanon.CLEAR_UNVERIFIED
        row2["Motivo_Revision_Normalizado"] = ""
        writer.writerow(row2)
        yield Path(f.name)

    # Cleanup
    Path(f.name).unlink(missing_ok=True)
