import sys
import tempfile
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from storage.csv_adapter import CSVAdapter, PieceCSVAdapter
from core.models import Piece
from core.enums import (
    EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad,
    DificultadProduccion, Reutilizable, BloqueadoCanon, EstadoCanon,
    EstadoProduccion, EstadoPublicacion, MotivoRevision,
    ReconciliacionEstado, ReconciliacionConfianza
)

def test_csv_adapter_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "test.csv"
        adapter = PieceCSVAdapter(csv_path)
        # Create a sample piece
        piece = Piece(
            ID_Pieza="CNT-0001",
            Titulo="Test Piece",
            Tipo_Contenido=TipoContenido.REEL,
            Plataforma=Plataforma.INSTAGRAM,
            Estado=EstadoPieza.IDEA,
            Prioridad=Prioridad.ALTA,
            Dificultad_Produccion=DificultadProduccion.BAJA,
            Es_Reutilizable=Reutilizable.SÍ,
            Categoria=Categoria.HUMOR,
            Bloqueado_Canon=BloqueadoCanon.NO,
            # Leave other fields as default (empty strings or None)
        )
        # Write
        adapter.write_all(Piece, [piece])
        # Read back
        records = adapter.read_all(Piece)
        assert len(records) == 1
        read_piece = records[0]
        # Check that essential fields match
        assert read_piece.ID_Pieza == piece.ID_Pieza
        assert read_piece.Titulo == piece.Titulo
        assert read_piece.Tipo_Contenido == piece.Tipo_Contenido
        assert read_piece.Plataforma == piece.Plataforma
        assert read_piece.Estado == piece.Estado
        assert read_piece.Prioridad == piece.Prioridad
        assert read_piece.Dificultad_Produccion == piece.Dificultad_Produccion
        assert read_piece.Es_Reutilizable == piece.Es_Reutilizable
        assert read_piece.Categoria == piece.Categoria
        assert read_piece.Bloqueado_Canon == piece.Bloqueado_Canon
        # Note: other fields that were defaulted may be empty strings vs None; we accept either.
        # For simplicity, we just check that the piece is valid.
        assert read_piece.ID_Pieza.startswith("CNT-")

def test_csv_adapter_with_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "empty.csv"
        adapter = PieceCSVAdapter(csv_path)
        # Write nothing
        adapter.write_all(Piece, [])
        # Read back
        records = adapter.read_all(Piece)
        assert len(records) == 0
        # File should exist with only header
        assert csv_path.exists()
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 1  # header only
            # Check that header contains expected fields (just a few)
            header = lines[0].strip()
            assert 'ID_Pieza' in header
            assert 'Titulo' in header

if __name__ == "__main__":
    test_csv_adapter_roundtrip()
    test_csv_adapter_with_empty()
    print("All CSV adapter tests passed.")
