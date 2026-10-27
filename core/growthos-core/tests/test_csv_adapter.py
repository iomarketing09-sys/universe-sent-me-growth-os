"""Tests for CSV adapter."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "growthos"))

import pytest
from growthos.core.models import Piece
from growthos.storage.csv_adapter import CSVAdapter


class TestCSVAdapter:
    """Test CSVAdapter functionality."""

    def test_read_write_roundtrip(self, tmp_path):
        """Test reading and writing CSV preserves data."""
        csv_file = tmp_path / "test_pieces.csv"
        
        # Create test pieces with required fields
        pieces = [
            Piece(
                id_pieza="CNT-001", 
                titulo="Piece 1", 
                estado_operativo="Idea",
                tipo_contenido="Reel",
                plataforma_principal="Instagram",
                categoria_tematica="Humor"
            ),
            Piece(
                id_pieza="CNT-002", 
                titulo="Piece 2", 
                estado_operativo="Aprobado",
                tipo_contenido="Carrusel",
                plataforma_principal="Facebook",
                categoria_tematica="Narrativa"
            ),
        ]
        
        # Write
        CSVAdapter.export_csv(pieces, csv_file)
        
        # Read back
        read_pieces = CSVAdapter.import_csv(Piece, csv_file)
        
        assert len(read_pieces) == 2
        assert read_pieces[0].id_pieza == "CNT-001"
        assert read_pieces[1].id_pieza == "CNT-002"

    def test_csv_adapter_update(self, tmp_path):
        """Test updating a piece in CSV."""
        csv_file = tmp_path / "test_pieces.csv"
        
        piece = Piece(
            id_pieza="CNT-001", 
            titulo="Original", 
            estado_operativo="Idea",
            tipo_contenido="Reel",
            plataforma_principal="Instagram",
            categoria_tematica="Humor"
        )
        CSVAdapter.export_csv([piece], csv_file)
        
        # Update - re-export all
        piece.titulo = "Updated"
        CSVAdapter.export_csv([piece], csv_file)
        
        # Read back
        read_pieces = CSVAdapter.import_csv(Piece, csv_file)
        assert len(read_pieces) == 1
        assert read_pieces[0].titulo == "Updated"

    def test_csv_adapter_delete(self, tmp_path):
        """Test deleting by removing file and re-importing."""
        csv_file = tmp_path / "test_pieces.csv"
        
        piece = Piece(
            id_pieza="CNT-001", 
            titulo="To Delete", 
            estado_operativo="Idea",
            tipo_contenido="Reel",
            plataforma_principal="Instagram",
            categoria_tematica="Humor"
        )
        CSVAdapter.export_csv([piece], csv_file)
        
        # Verify it's there
        read_pieces = CSVAdapter.import_csv(Piece, csv_file)
        assert len(read_pieces) == 1
        
        # Delete the file completely
        csv_file.unlink()
        
        # Verify gone
        read_pieces = CSVAdapter.import_csv(Piece, csv_file)
        assert len(read_pieces) == 0
