"""Enums for GrowthOS."""

from enum import Enum


class BaseEnum(Enum):
    """Base enum with string comparison and hashing."""
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return hash((self.__class__, self.value))


class EstadoPieza(BaseEnum):
    IDEA = "Idea"
    PENDIENTE_PRODUCCION = "Pendiente de Producción"
    APROBADO = "Aprobado"
    PUBLICADO = "Publicado"
    ARCHIVADO = "Archivado"
    DIFERIDO = "Diferido"
    BLOQUEADO = "Bloqueado"
    PROGRAMADO = "Programado"


class Plataforma(BaseEnum):
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    YOUTUBE_SHORTS = "YouTube Shorts"
    MULTI = "Multi"


class TipoContenido(BaseEnum):
    REEL = "Reel"
    CARRUSEL = "Carrusel"
    REEL_MEME_ADAPTADO = "Reel / Meme adaptado"
    REEL_SECCION_RECURRENTE = "Reel / Sección recurrente"
    TRAILER_TEASER = "Trailer / Teaser"
    MINI_HISTORIA_SERIALIZADA = "Mini-historia serializada"


class Categoria(BaseEnum):
    HUMOR = "Humor"
    NARRATIVA = "Narrativa"
    HUMOR_MEME = "Humor / Meme"
    HUMOR_RESEÑA_COMERCIAR = "Humor / Reseña / Comerciar"
    MARCA_NARRATIVA_RESONANCIA = "Marca / Narrativa / Resonancia"


class Prioridad(BaseEnum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class DificultadProduccion(BaseEnum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"


class Reutilizable(BaseEnum):
    SÍ = "Sí"
    NO = "No"


class BloqueadoCanon(BaseEnum):
    NO = "No"
    SÍ = "Sí"


class EstadoCanon(BaseEnum):
    CANON_CLEAR_OR_UNVERIFIED = "Canon_Clear_or_Unverified"
    CANON_CONSTRAINED = "Canon_Constrained"
    CANON_REVIEW_REQUIRED = "Canon_Review_Required"
    CANON_PARTIAL = "Canon_Partial"


class EstadoProduccion(BaseEnum):
    ASSET_LISTO = "Asset_Listo"
    IDEA = "Idea"
    PENDIENTE_REVISION = "Pendiente_Revision"
    EN_PRODUCCION = "En_Produccion"
    DIFERIDO = "Diferido"


class EstadoPublicacion(BaseEnum):
    NO_PUBLICADA = "No_Publicada"
    PUBLICADA = "Publicada"


class MotivoRevision(BaseEnum):
    CANON_CONTRADICCION_SUSTANTIVA = "Canon_Contradiccion_Sustantiva"
    CANON_ABSOLUCION_ADMINISTRATIVA = "Canon_Absolucion_Administrativa"
    CANON_RESTRICCION_NO_BLOQUEANTE = "Canon_Restriccion_No_Bloqueante"
    CANON_RESUELTO_RECONCILIACION_PENDIENTE = "Canon_Resuelto_Reconciliacion_Pendiente"
    INVENTARIO_RECONCILIACION_PENDIENTE = "Inventario_Reconciliacion_Pendiente"
    IDENTIDAD_RECONCILIADA_SIN_CONFLICTO_CANON_EVIDENTE = "Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente"


class ReconciliacionEstado(BaseEnum):
    NO_CONFIRMED_MATCH = "No_Confirmed_Match"
    RESOLVED_PRODUCTION_SET = "Resolved_Production_Set"


class ReconciliacionConfianza(BaseEnum):
    ALTA = "High"
    MEDIA = "Medium"
    BAJA = "Low"
    NINGUNA = "None"
