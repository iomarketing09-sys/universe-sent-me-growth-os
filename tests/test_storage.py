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
        ID_Pieza="CNT-001",
        Estado=EstadoPieza.IDEA,
        Titulo="Test Piece",
        Personaje_Principal="@char_USM_universe",
        Plataforma="Facebook",
    )

    repo.save(piece)
    assert repo.count() == 1

    retrieved = repo.get_by_id("CNT-001")
    assert retrieved is not None
    assert retrieved.ID_Pieza == "CNT-001"
    assert retrieved.Titulo == "Test Piece"


def test_piece_repository_get_all(temp_db):
    """Test PieceRepository get_all."""
    repo = PieceRepository(temp_db)

    for i in range(3):
        piece = Piece(
            ID_Pieza=f"CNT-{i+1:04d}",
            Estado=EstadoPieza.IDEA,
            Titulo=f"Piece {i+1}",
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
        ID_Pieza="CNT-001",
        Estado=EstadoPieza.IDEA,
        Titulo="Test Piece",
    )
    piece_repo.save(piece)

    pub = Publication(
        ID_Pieza="CNT-001",
        Publicacion_ID="PUB-001",
        Meta_Post_ID="123_456",
        Plataforma="Facebook",
    )

    repo.save(pub)
    assert repo.count() == 1

    retrieved = repo.get_by_meta_post_id("123_456")
    assert retrieved is not None
    assert retrieved.Meta_Post_ID == "123_456"


def test_csv_adapter_import_pieces():
    """Test CSVAdapter.import_csv for pieces."""
    import csv

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "test.csv"

        test_data = [
            {
                "ID_Pieza": "CNT-001",
                "Titulo": "Test 1",
                "Estado": "Aprobado",
                "Personaje_Principal": "@char_USM_universe",
            },
            {
                "ID_Pieza": "CNT-002",
                "Titulo": "Test 2",
                "Estado": "Idea",
                "Personaje_Principal": "@char_USM_wilfred",
            },
        ]

        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=test_data[0].keys())
            writer.writeheader()
            writer.writerows(test_data)

        pieces = CSVAdapter.import_csv(Piece, csv_path)
        assert len(pieces) == 2
        assert pieces[0].ID_Pieza == "CNT-001"
        assert pieces[1].ID_Pieza == "CNT-002"


def test_csv_adapter_export_pieces(temp_db):
    """Test CSVAdapter.export_piece_csv."""
    import csv

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "export.csv"

        repo = PieceRepository(temp_db)
        pieces = [
            Piece(ID_Pieza="CNT-001", Estado=EstadoPieza.IDEA, Titulo="Test 1"),
            Piece(ID_Pieza="CNT-002", Estado=EstadoPieza.APROBADO, Titulo="Test 2"),
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
        assert rows[0]["id"] == "CNT-001"
        assert rows[1]["id"] == "CNT-002"
