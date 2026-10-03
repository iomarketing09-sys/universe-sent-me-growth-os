import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from datetime import date
from core.models import Piece, Publication, Experiment, CommunityEngagement, MetricsSnapshot, AssetAlias
from core.enums import (
    EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad,
    DificultadProduccion, Reutilizable, BloqueadoCanon, EstadoCanon,
    EstadoProduccion, EstadoPublicacion, MotivoRevision,
    ReconciliacionEstado, ReconciliacionConfianza
)

def test_piece_creation():
    p = Piece(
        ID_Pieza="CNT-0001",
        Titulo="Test Piece",
        Personaje_Principal="Hero",
        Personajes_Secundarios="Sidekick",
        Tipo_Contenido=TipoContenido.REEL,
        Plataforma=Plataforma.INSTAGRAM,
        Objetivo="Test",
        Hipotesis_ID="HB-001",
        Estado=EstadoPieza.IDEA,
        Prioridad=Prioridad.ALTA,
        Dificultad_Produccion=DificultadProduccion.BAJA,
        Es_Reutilizable=Reutilizable.SÍ,
        Fecha_Ultima_Publicacion=None,
        Fuente="Test",
        Formato="MP4",
        Categoria=Categoria.HUMOR,
        Bloqueado_Canon=BloqueadoCanon.NO,
        Estado_Operacion_Normalizado="",
        Estado_Canon_Normalizado="",
        Asset_Ref_Confirmado="",
        Asset_Ref_Candidato="",
        Reconciliacion_Estado=None,
        Reconciliacion_Confianza=None,
        Reconciliacion_Fuente="",
        Reconciliacion_Nota="",
        Registro_Relacionado="",
        Drive_Reference_ID="",
        Meta_Publication_ID="",
        Meta_Permalink="",
        Asset_Set="",
        Asset_Ref="",
        Asset_Filename="",
        Drive_ID="",
        Estado_Canon=None,
        Estado_Produccion=None,
        Estado_Publicacion=None,
        Ultima_Sincronizacion="",
        Motivo_Revision_Normalizado=None,
        Personaje_Principal_Normalizado="",
        Personajes_Secundarios_Normalizados="",
        Rol_Narrativo="",
        Tipo_Humor_Normalizado="",
        Potencial_Etiquetado="",
        Confianza_Taxonomia="",
        Fuente_Taxonomia="",
        Nota_Taxonomia=""
    )
    assert p.ID_Pieza == "CNT-0001"
    assert p.Titulo == "Test Piece"
    assert p.Estado == EstadoPieza.IDEA
    assert p.Plataforma == Plataforma.INSTAGRAM
    assert p.Tipo_Contenido == TipoContenido.REEL
    assert p.Categoria == Categoria.HUMOR
    assert p.Bloqueado_Canon == BloqueadoCanon.NO
    assert p.Estado_Canon is None

def test_piece_validators():
    # Test that invalid enum raises ValueError
    try:
        Piece(
            ID_Pieza="CNT-0002",
            Titulo="Invalid",
            Estado="InvalidState",  # not in Enum
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid Estado" in str(e)
    # Test ID_Pieza format
    try:
        Piece(ID_Pieza="invalid-format", Titulo="Test")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid piece ID format" in str(e)
    try:
        Piece(ID_Pieza="CNT-00000", Titulo="Test")  # number out of range
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid piece ID format" in str(e)
    # Test valid ID
    p = Piece(ID_Pieza="CNT-0001", Titulo="Test")
    assert p.ID_Pieza == "CNT-0001"
    # Test that empty string for required string fields is allowed (they default to empty)
    p2 = Piece(ID_Pieza="CNT-0003", Titulo="")
    assert p2.Titulo == ""
    # Test that optional enum fields accept None
    p3 = Piece(ID_Pieza="CNT-0004", Titulo="Test", Tipo_Contenido=None, Plataforma=None)
    assert p3.Tipo_Contenido is None
    assert p3.Plataforma is None

def test_other_models():
    pub = Publication(ID_Pieza="CNT-0001", Publicacion_ID="pub123", Fecha_Publicacion=date(2026,8,30), Plataforma=Plataforma.FACEBOOK)
    assert pub.Publicacion_ID == "pub123"
    exp = Experiment(Experiment_ID="exp1", Hipotesis_ID="HB-001", ID_Pieza="CNT-0001")
    assert exp.Experiment_ID == "exp1"
    ce = CommunityEngagement(ID="ce1", Comentario_ID="comment1", Post_ID="post1", CNT_ID="CNT-0001", Tipo="Like", Autor="user", Texto="Test comment")
    assert ce.ID == "ce1"
    ms = MetricsSnapshot(Snapshot_ID="snap1", Meta_Post_ID="meta123", Target_At_UTC="2026-08-30T10:00:00Z", Window_Type="24h")
    assert ms.Snapshot_ID == "snap1"
    aa = AssetAlias(Alias_ID="alias1", Asset_Ref="ref123", Asset_Filename="file.jpg", Drive_ID="drive123")
    assert aa.Alias_ID == "alias1"

if __name__ == "__main__":
    test_piece_creation()
    test_piece_validators()
    test_other_models()
    print("All model tests passed.")
