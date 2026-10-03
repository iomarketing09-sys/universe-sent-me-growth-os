import sys
import tempfile
from pathlib import Path

# Add the core to sys.path
CORE_PATH = Path('/home/universe-sent-me/growth-os/core/growthos-core')
sys.path.insert(0, str(CORE_PATH))

from storage.repositories import PieceRepository
from core.models import Piece
from core.enums import (
    EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad,
    DificultadProduccion, Reutilizable, BloqueadoCanon
)

def test_account_isolation_using_core():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        base_path = data_dir / "pieces.csv"
        
        # Create repos for the two accounts
        repo_fb = PieceRepository(base_path, account_id="firma_bordados")
        repo_usm = PieceRepository(base_path, account_id="universe_sent_me")
        
        # Create a piece for each account
        piece_fb = Piece(
            ID_Pieza="FB-0001",
            Titulo="Firma Bordados Test Piece",
            Tipo_Contenido=TipoContenido.REEL,
            Plataforma=Plataforma.FACEBOOK,
            Estado=EstadoPieza.IDEA,
            Prioridad=Prioridad.ALTA,
            Dificultad_Produccion=DificultadProduccion.BAJA,
            Es_Reutilizable=Reutilizable.SÍ,
            Categoria=Categoria.HUMOR,
            Bloqueado_Canon=BloqueadoCanon.NO,
        )
        piece_usm = Piece(
            ID_Pieza="USM-0001",
            Titulo="Universe Sent Me Test Piece",
            Tipo_Contenido=TipoContenido.CARRUSEL,
            Plataforma=Plataforma.INSTAGRAM,
            Estado=EstadoPieza.PENDIENTE_PRODUCCION,
            Prioridad=Prioridad.MEDIA,
            Dificultad_Produccion=DificultadProduccion.MEDIA,
            Es_Reutilizable=Reutilizable.NO,
            Categoria=Categoria.NARRATIVA,
            Bloqueado_Canon=BloqueadoCanon.NO,
        )
        
        # Save each piece to its respective repository
        repo_fb.save(piece_fb)
        repo_usm.save(piece_usm)
        
        # Load all pieces from each repository
        pieces_fb = repo_fb.get_all()
        pieces_usm = repo_usm.get_all()
        
        # Each repository should only see its own piece
        assert len(pieces_fb) == 1, f"Firma Bordados repo should have 1 piece, got {len(pieces_fb)}"
        assert len(pieces_usm) == 1, f"Universe Sent Me repo should have 1 piece, got {len(pieces_usm)}"
        assert pieces_fb[0].ID_Pieza == "FB-0001"
        assert pieces_usm[0].ID_Pieza == "USM-0001"
        
        # Verify that the underlying files are different and contain correct data
        file_fb = data_dir / "pieces_firma_bordados.csv"
        file_usm = data_dir / "pieces_universe_sent_me.csv"
        assert file_fb.exists(), f"Expected file {file_fb} not found"
        assert file_usm.exists(), f"Expected file {file_usm} not found"
        
        # Check that file_fb contains piece_fb and not piece_usm
        with open(file_fb, 'r', encoding='utf-8') as f:
            content_fb = f.read()
            assert "Firma Bordados Test Piece" in content_fb
            assert "Universe Sent Me Test Piece" not in content_fb
        # Check that file_usm contains piece_usm and not piece_fb
        with open(file_usm, 'r', encoding='utf-8') as f:
            content_usm = f.read()
            assert "Universe Sent Me Test Piece" in content_usm
            assert "Firma Bordados Test Piece" not in content_usm
        
        # Also verify that the base file (pieces.csv) may exist but should be empty or only headers if never used directly
        base_file = data_dir / "pieces.csv"
        if base_file.exists():
            with open(base_file, 'r', encoding='utf-8') as f:
                base_content = f.read()
                # It should not contain our piece data because we used account_id suffixed files
                assert "Firma Bordados Test Piece" not in base_content
                assert "Universe Sent Me Test Piece" not in base_content
        
        print("Account isolation test using core PASSED.")

if __name__ == "__main__":
    test_account_isolation_using_core()
