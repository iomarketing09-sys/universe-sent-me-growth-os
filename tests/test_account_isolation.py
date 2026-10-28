"""Account isolation: pieces stored for one account must not leak into another."""

import tempfile
from pathlib import Path

from growthos.storage.database import Database
from growthos.storage.repositories import PieceRepository
from growthos.core.models import Piece
from growthos.core.enums import (
    EstadoPieza,
    Plataforma,
    TipoContenido,
    Categoria,
    Prioridad,
    DificultadProduccion,
    Reutilizable,
    BloqueadoCanon,
)


def _repo(db_path: Path) -> tuple[PieceRepository, Database]:
    db = Database(db_path=db_path)
    db.init_schema()
    return PieceRepository(db), db


def test_account_isolation_using_core():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = Path(tmpdir)
        repo_fb, db_fb = _repo(data_dir / "firma_bordados.db")
        repo_usm, db_usm = _repo(data_dir / "universe_sent_me.db")

        try:
            piece_fb = Piece(
                id_pieza="CNT-0001",
                titulo="Firma Bordados Test Piece",
                tipo_contenido=TipoContenido.REEL,
                plataforma_principal=Plataforma.FACEBOOK,
                estado_operativo=EstadoPieza.IDEA,
                prioridad=Prioridad.ALTA,
                dificultad_produccion=DificultadProduccion.BAJA,
                es_reutilizable=Reutilizable.SI,
                categoria_tematica=Categoria.HUMOR,
                bloqueado_canon=BloqueadoCanon.NO,
            )
            piece_usm = Piece(
                id_pieza="CNT-0002",
                titulo="Universe Sent Me Test Piece",
                tipo_contenido=TipoContenido.CARRUSEL,
                plataforma_principal=Plataforma.INSTAGRAM,
                estado_operativo=EstadoPieza.PENDIENTE_PRODUCCION,
                prioridad=Prioridad.MEDIA,
                dificultad_produccion=DificultadProduccion.MEDIA,
                es_reutilizable=Reutilizable.NO,
                categoria_tematica=Categoria.NARRATIVA,
                bloqueado_canon=BloqueadoCanon.NO,
            )

            repo_fb.save(piece_fb)
            repo_usm.save(piece_usm)

            pieces_fb = repo_fb.get_all()
            pieces_usm = repo_usm.get_all()

            assert len(pieces_fb) == 1, f"Firma Bordados repo should have 1 piece, got {len(pieces_fb)}"
            assert len(pieces_usm) == 1, f"Universe Sent Me repo should have 1 piece, got {len(pieces_usm)}"
            assert pieces_fb[0].id_pieza == "CNT-0001"
            assert pieces_usm[0].id_pieza == "CNT-0002"

            assert pieces_fb[0].titulo == "Firma Bordados Test Piece"
            assert pieces_usm[0].titulo == "Universe Sent Me Test Piece"
        finally:
            db_fb.close()
            db_usm.close()
