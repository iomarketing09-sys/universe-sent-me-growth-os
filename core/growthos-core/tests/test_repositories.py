"""Tests for repositories."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "growthos"))

import pytest
from growthos.core.models import Piece, Publication
from growthos.storage.repositories import PieceRepository, PublicationRepository
from growthos.storage.database import Database


class TestRepositories:
    """Test repository functionality."""

    def test_piece_repository_crud(self, tmp_path):
        """Test PieceRepository CRUD operations."""
        db_path = tmp_path / "test.db"
        db = Database(db_path)
        db.init_schema()
        
        repo = PieceRepository(db)
        
        # Create
        piece = Piece(id_pieza="CNT-001", titulo="Test Piece", estado_operativo="Idea")
        repo.save(piece)
        
        # Read
        read_piece = repo.get_by_id("CNT-001")
        assert read_piece is not None
        assert read_piece.id_pieza == "CNT-001"
        assert read_piece.titulo == "Test Piece"
        
        # Update
        piece.titulo = "Updated"
        repo.save(piece)
        read_piece = repo.get_by_id("CNT-001")
        assert read_piece.titulo == "Updated"
        
        # Count
        assert repo.count() == 1

    def test_publication_repository(self, tmp_path):
        """Test PublicationRepository."""
        db_path = tmp_path / "test.db"
        db = Database(db_path)
        db.init_schema()
        
        # First create the piece (FK requirement)
        piece_repo = PieceRepository(db)
        piece = Piece(id_pieza="CNT-001", titulo="Test Piece", estado_operativo="Idea")
        piece_repo.save(piece)
        
        # Now test publication
        repo = PublicationRepository(db)
        
        pub = Publication(id_pieza="CNT-001", publicacion_id="PUB-001", fecha_publicacion="2026-10-15")
        repo.save(pub)
        
        read_pub = repo.get_by_id("PUB-001")
        assert read_pub is not None
        assert read_pub.publicacion_id == "PUB-001"
