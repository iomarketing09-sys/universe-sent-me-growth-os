import sys
import tempfile
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from storage.repositories import PieceRepository
from core.models import Piece
from core.enums import EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad, DificultadProduccion, Reutilizable, BloqueadoCanon

def test_repository_multi_account_isolation():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        base_path = data_dir / "pieces.csv"
        # Create repos for two accounts
        repo_a = PieceRepository(base_path, account_id="account_a")
        repo_b = PieceRepository(base_path, account_id="account_b")
        # Create a piece for each account
        piece_a = Piece(
            ID_Pieza="CNT-0001",
            Titulo="Piece A",
            Tipo_Contenido=TipoContenido.REEL,
            Plataforma=Plataforma.FACEBOOK,
            Estado=EstadoPieza.IDEA,
            Prioridad=Prioridad.ALTA,
            Dificultad_Produccion=DificultadProduccion.BAJA,
            Es_Reutilizable=Reutilizable.SÍ,
            Categoria=Categoria.HUMOR,
            Bloqueado_Canon=BloqueadoCanon.NO,
        )
        piece_b = Piece(
            ID_Pieza="CNT-0002",
            Titulo="Piece B",
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
        repo_a.save(piece_a)
        repo_b.save(piece_b)
        # Load all pieces from each repository
        pieces_a = repo_a.get_all()
        pieces_b = repo_b.get_all()
        # Each repository should only see its own piece
        assert len(pieces_a) == 1
        assert len(pieces_b) == 1
        assert pieces_a[0].ID_Pieza == "CNT-0001"
        assert pieces_a[0].Titulo == "Piece A"
        assert pieces_b[0].ID_Pieza == "CNT-0002"
        assert pieces_b[0].Titulo == "Piece B"
        # Verify that the underlying files are different and contain correct data
        file_a = data_dir / "pieces_account_a.csv"
        file_b = data_dir / "pieces_account_b.csv"
        assert file_a.exists()
        assert file_b.exists()
        # Check that file_a contains piece_a and not piece_b
        with open(file_a, 'r', encoding='utf-8') as f:
            content_a = f.read()
            assert "Piece A" in content_a
            assert "Piece B" not in content_a
            assert "account_a" in str(file_a)
        with open(file_b, 'r', encoding='utf-8') as f:
            content_b = f.read()
            assert "Piece B" in content_b
            assert "Piece A" not in content_b
            assert "account_b" in str(file_b)
        # Also verify that the base file (pieces.csv) may exist but should be empty or only headers if never used directly
        # Since we always used account_id, the base file should be untouched (maybe only header if adapter wrote header on init?)
        # We'll just ensure it doesn't contain our data.
        base_file = data_dir / "pieces.csv"
        if base_file.exists():
            with open(base_file, 'r', encoding='utf-8') as f:
                base_content = f.read()
                # It should not contain our piece data because we used account_id suffixed files
                assert "Piece A" not in base_content
                assert "Piece B" not in base_content

def test_repository_no_account_id():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir) / "data"
        data_dir.mkdir()
        base_path = data_dir / "pieces.csv"
        repo = PieceRepository(base_path)  # no account_id
        piece = Piece(
            ID_Pieza="CNT-0003",
            Titulo="Piece No Account",
            Tipo_Contenido=TipoContenido.REEL,
            Plataforma=Plataforma.FACEBOOK,
            Estado=EstadoPieza.IDEA,
            Prioridad=Prioridad.ALTA,
            Dificultad_Produccion=DificultadProduccion.BAJA,
            Es_Reutilizable=Reutilizable.SÍ,
            Categoria=Categoria.HUMOR,
            Bloqueado_Canon=BloqueadoCanon.NO,
        )
        repo.save(piece)
        pieces = repo.get_all()
        assert len(pieces) == 1
        assert pieces[0].ID_Pieza == "CNT-0003"
        # The file should be exactly the base path
        assert base_path.exists()
        with open(base_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Piece No Account" in content

if __name__ == "__main__":
    test_repository_multi_account_isolation()
    test_repository_no_account_id()
    print("All repository tests passed.")
