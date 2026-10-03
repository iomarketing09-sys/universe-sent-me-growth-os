import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))
from core.enums import (
    EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad,
    DificultadProduccion, Reutilizable, BloqueadoCanon, EstadoCanon,
    EstadoProduccion, EstadoPublicacion, MotivoRevision,
    ReconciliacionEstado, ReconciliacionConfianza, BaseEnum
)

def test_enum_values():
    # Test that enums have expected values
    assert EstadoPieza.IDEA.value == "Idea"
    assert EstadoPieza.PENDIENTE_PRODUCCION.value == "Pendiente de Producción"
    assert EstadoPieza.APROBADO.value == "Aprobado"
    assert EstadoPieza.PUBLICADO.value == "Publicado"
    assert EstadoPieza.ARCHIVADO.value == "Archivado"
    assert EstadoPieza.DIFERIDO.value == "Diferido"
    assert EstadoPieza.BLOQUEADO.value == "Bloqueado"
    assert EstadoPieza.PROGRAMADO.value == "Programado"

    assert Plataforma.FACEBOOK.value == "Facebook"
    assert Plataforma.INSTAGRAM.value == "Instagram"
    assert Plataforma.TIKTOK.value == "TikTok"
    assert Plataforma.YOUTUBE_SHORTS.value == "YouTube Shorts"
    assert Plataforma.MULTI.value == "Multi"

    assert TipoContenido.REEL.value == "Reel"
    assert TipoContenido.CARRUSEL.value == "Carrusel"
    assert TipoContenido.REEL_MEME_ADAPTADO.value == "Reel / Meme adaptado"
    assert TipoContenido.REEL_SECCION_RECURRENTE.value == "Reel / Sección recurrente"
    assert TipoContenido.TRAILER_TEASER.value == "Trailer / Teaser"
    assert TipoContenido.MINI_HISTORIA_SERIALIZADA.value == "Mini-historia serializada"

    assert Categoria.HUMOR.value == "Humor"
    assert Categoria.NARRATIVA.value == "Narrativa"
    assert Categoria.HUMOR_MEME.value == "Humor / Meme"
    assert Categoria.HUMOR_RESEÑA_COMERCIAR.value == "Humor / Reseña / Comerciar"
    assert Categoria.MARCA_NARRATIVA_RESONANCIA.value == "Marca / Narrativa / Resonancia"

    assert Prioridad.ALTA.value == "Alta"
    assert Prioridad.MEDIA.value == "Media"
    assert Prioridad.BAJA.value == "Baja"

    assert DificultadProduccion.BAJA.value == "Baja"
    assert DificultadProduccion.MEDIA.value == "Media"
    assert DificultadProduccion.ALTA.value == "Alta"

    assert Reutilizable.SÍ.value == "Sí"
    assert Reutilizable.NO.value == "No"

    assert BloqueadoCanon.SÍ.value == "Sí"
    assert BloqueadoCanon.NO.value == "No"

    assert EstadoCanon.CANON_CLEAR_OR_UNVERIFIED.value == "Canon_Clear_or_Unverified"
    assert EstadoCanon.CANON_CONSTRAINED.value == "Canon_Constrained"
    assert EstadoCanon.CANON_REVIEW_REQUIRED.value == "Canon_Review_Required"
    assert EstadoCanon.CANON_PARTIAL.value == "Canon_Partial"

    assert EstadoProduccion.ASSET_LISTO.value == "Asset_Listo"
    assert EstadoProduccion.IDEA.value == "Idea"
    assert EstadoProduccion.PENDIENTE_REVISION.value == "Pendiente_Revision"
    assert EstadoProduccion.EN_PRODUCCION.value == "En_Produccion"
    assert EstadoProduccion.DIFERIDO.value == "Diferido"

    assert EstadoPublicacion.NO_PUBLICADA.value == "No_Publicada"
    assert EstadoPublicacion.PUBLICADA.value == "Publicada"

    assert MotivoRevision.CANON_CONTRADICCION_SUSTANTIVA.value == "Canon_Contradiccion_Sustantiva"
    assert MotivoRevision.CANON_ABSOLUCION_ADMINISTRATIVA.value == "Canon_Absolucion_Administrativa"
    assert MotivoRevision.CANON_RESTRICCION_NO_BLOQUEANTE.value == "Canon_Restriccion_No_Bloqueante"
    assert MotivoRevision.CANON_RESUELTO_RECONCILIACION_PENDIENTE.value == "Canon_Resuelto_Reconciliacion_Pendiente"
    assert MotivoRevision.INVENTARIO_RECONCILIACION_PENDIENTE.value == "Inventario_Reconciliacion_Pendiente"
    assert MotivoRevision.IDENTIDAD_RECONCILIADA_SIN_CONFLICTO_CANON_EVIDENTE.value == "Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente"

    assert ReconciliacionEstado.NO_CONFIRMED_MATCH.value == "No_Confirmed_Match"
    assert ReconciliacionEstado.RESOLVED_PRODUCTION_SET.value == "Resolved_Production_Set"

    assert ReconciliacionConfianza.ALTA.value == "High"
    assert ReconciliacionConfianza.MEDIA.value == "Medium"
    assert ReconciliacionConfianza.BAJA.value == "Low"
    assert ReconciliacionConfianza.NINGUNA.value == "None"

def test_base_enum_string_comparison():
    # Test BaseEnum allows comparison with string
    assert EstadoPieza.IDEA == "Idea"
    assert EstadoPieza.IDEA != "Publicado"
    assert EstadoPieza.IDEA is not "Idea"  # identity different
    assert hash(EstadoPieza.IDEA) == hash((EstadoPieza, "Idea"))

if __name__ == "__main__":
    test_enum_values()
    test_base_enum_string_comparison()
    print("All enum tests passed.")
