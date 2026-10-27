"""Tests for storage layer: database, repositories, CSV adapter."""

import tempfile
from pathlib import Path

import pytest

from growthos.core.models import Piece, Publication
from growthos.storage.database import Database
from growthos.storage.repositories import PieceRepository, PublicationRepository
from growthos.storage.csv_adapter import CSVAdapter
from growthos.core.enums import EstadoPieza


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(db_path=db_path)
        db.init_schema()
        yield db
        db.close()


def test_database_init_schema(temp_db):
    """Test database schema initialization."""
    # Check tables exist
    tables = temp_db.fetchall(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    table_names = [t["name"] for t in tables]

    expected_tables = [
        "pieces", "publications", "experiments",
        "community_engagement", "metrics_snapshots",
        "asset_aliases", "schema_version"
    ]
    for table in expected_tables:
        assert table in table_names, f"Missing table: {table}"

    # Check schema_version has entry
    version = temp_db.fetchone("SELECT version FROM schema_version")
    assert version is not None
    assert version["version"] == 1


def test_piece_repository_save_and_get(temp_db):
    """Test PieceRepository save and get."""
    repo = PieceRepository(temp_db)

    piece = Piece(
        id_pieza="CNT-001",
        estado_operativo=EstadoPieza.IDEA,
        titulo="Test Piece",
        personaje_principal="@char_USM_universe",
        plataforma_principal="Facebook",
    )

    repo.save(piece)
    assert repo.count() == 1

    retrieved = repo.get_by_id("CNT-001")
    assert retrieved is not None
    assert retrieved.id_pieza == "CNT-001"
    assert retrieved.titulo == "Test Piece"


def test_piece_repository_get_all(temp_db):
    """Test PieceRepository get_all."""
    repo = PieceRepository(temp_db)

    for i in range(3):
        piece = Piece(
            id_pieza=f"CNT-{i+1:04d}",
            estado_operativo=EstadoPieza.IDEA,
            titulo=f"Piece {i+1}",
        )
        repo.save(piece)

    all_pieces = repo.get_all()
    assert len(all_pieces) == 3


def test_publication_repository(temp_db):
    """Test PublicationRepository."""
    repo = PublicationRepository(temp_db)
    piece_repo = PieceRepository(temp_db)

    # First create a piece (FK requirement)
    piece = Piece(
        id_pieza="CNT-001",
        estado_operativo=EstadoPieza.IDEA,
        titulo="Test Piece",
    )
    piece_repo.save(piece)

    pub = Publication(
        id_pieza="CNT-001",
        publicacion_id="PUB-001",
        meta_post_id="123_456",
        plataforma="Facebook",
    )

    repo.save(pub)
    assert repo.count() == 1

    retrieved = repo.get_by_meta_post_id("123_456")
    assert retrieved is not None
    assert retrieved.meta_post_id == "123_456"


def test_csv_adapter_import_pieces():
    """Test CSVAdapter.import_csv for pieces."""
    import csv

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "test.csv"

        test_data = [
            {
                "id": "CNT-001",
                "titulo": "Test 1",
                "estado_operacion_normalizado": "Aprobado",
                "personaje_principal": "@char_USM_universe",
            },
            {
                "id": "CNT-002",
                "titulo": "Test 2",
                "estado_operacion_normalizado": "Idea",
                "personaje_principal": "@char_USM_wilfred",
            },
        ]

        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=test_data[0].keys())
            writer.writeheader()
            writer.writerows(test_data)

        pieces = CSVAdapter.import_csv(Piece, csv_path)
        assert len(pieces) == 2
        assert pieces[0].id_pieza == "CNT-001"
        assert pieces[1].id_pieza == "CNT-002"


def test_csv_adapter_export_pieces(temp_db):
    """Test CSVAdapter.export_piece_csv."""
    import csv

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "export.csv"

        repo = PieceRepository(temp_db)
        pieces = [
            Piece(id_pieza="CNT-001", estado_operativo=EstadoPieza.IDEA, titulo="Test 1"),
            Piece(id_pieza="CNT-002", estado_operativo=EstadoPieza.APROBADO, titulo="Test 2"),
        ]

        for p in pieces:
            repo.save(p)

        all_pieces = repo.get_all()
        CSVAdapter.export_piece_csv(all_pieces, csv_path)

        # Verify export
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0]["id_pieza"] == "CNT-001"
        assert rows[1]["id_pieza"] == "CNT-002"
