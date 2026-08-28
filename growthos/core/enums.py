"""Enumerations for GrowthOS domain model."""
from enum import Enum


class EstadoPieza(str, Enum):
    """Piece state machine states."""

    IDEA = "Idea"
    PENDIENTE_PRODUCCION = "Pendiente de Producción"
    EN_PRODUCCION = "En Producción"
    PENDIENTE_REVISION_CLAUDE = "Pendiente Revisión Claude"
    PENDIENTE_APROBACION_FERNANDO = "Pendiente Aprobación Fernando"
    APROBADO = "Aprobado"
    RECHAZADO = "Rechazado / Requiere Reescritura"
    PROGRAMADO = "Programado"
    PUBLICADO = "Publicado"
    EN_ANALISIS = "En Análisis"
    ARCHIVADO = "Archivado"
    REUTILIZADO_ARCHIVADO = "Reutilizado / Archivado"
    DIFERIDO = "Diferido"
    BLOQUEADO = "Bloqueado"


class Plataforma(str, Enum):
    """Target platforms."""

    INSTAGRAM = "Instagram"
    FACEBOOK = "Facebook"
    TIKTOK = "TikTok"
    YOUTUBE_SHORTS = "YouTube Shorts"
    MULTI = "Multi"


class TipoContenido(str, Enum):
    """Content format/deliverable type."""

    REEL = "Reel"
    CARRUSEL = "Carrusel"
    FOTO = "Foto"
    HISTORIA = "Historia"
    TRAILER = "Trailer"
    TEXTO = "Texto"
    REEL_MEME_ADAPTADO = "Reel / Meme adaptado"
    REEL_SECCION_RECURRENTE = "Reel / Sección recurrente"
    MINI_HISTORIA_SERIALIZADA = "Mini-historia serializada"


class Categoria(str, Enum):
    """Thematic category."""

    HUMOR = "Humor"
    FILOSOFIA = "Filosofía"
    TAROT = "Tarot"
    MAGIA = "Magia"
    NARRATIVA = "Narrativa"
    AFILIACION = "Afiliación"
    EDUCACION = "Educación"
    MARCA_NARRATIVA_RESONANCIA = "Marca / Narrativa / Resonancia"
    HUMOR_MEME = "Humor / Meme"
    HUMOR_RESEÑA_COMERCIAR = "Humor / Reseña / Comerciar"


class Prioridad(str, Enum):
    """Urgency/importance level."""

    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class DificultadProduccion(str, Enum):
    """Production effort estimate."""

    MUY_BAJA = "Muy_Baja"
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"


class Reutilizable(str, Enum):
    """Reuse flag."""

    SI = "Sí"
    NO = "No"


class BloqueadoCanon(str, Enum):
    """Canon block flag."""

    SI = "Sí"
    NO = "No"


class EstadoCanon(str, Enum):
    """Canon state (normalized)."""

    LIBRE = "Libre"
    REVISION = "Revision"
    APROBADO = "Aprobado"
    BLOQUEADO = "Bloqueado"
    CLEAR_UNVERIFIED = "Canon_Clear_or_Unverified"
    REVIEW_REQUIRED = "Canon_Review_Required"
    CONSTRAINED = "Canon_Constrained"
    PARTIAL = "Canon_Partial"
    RESUELTO_RECONCILIACION_PENDIENTE = "Canon_Resuelto_Reconciliacion_Pendiente"
    IDENTIDAD_RECONCILIADA = "Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente"
    INVENTARIO_RECONCILIACION_PENDIENTE = "Inventario_Reconciliacion_Pendiente"
    APROBACION_ADMINISTRATIVA = "Canon_Aprobacion_Administrativa"
    RESTRICCION_NO_BLOQUEANTE = "Canon_Restriccion_No_Bloqueante"
    CONTRADICCION_SUSTANTIVA = "Canon_Contradiccion_Sustantiva"
    DEFERRED_OPERATIONAL = "Deferred_Operational"


class EstadoProduccion(str, Enum):
    """Production state (normalized)."""

    IDEA = "Idea"
    EN_PRODUCCION = "En_Produccion"
    ASSET_LISTO = "Asset_Listo"
    PENDIENTE_REVISION = "Pendiente_Revision"
    DIFERIDO = "Diferido"
    PRODUCTION_PENDING = "Production_Pending"
    RESOLVED_PRODUCTION_SET = "Resolved_Production_Set"
    NO_CONFIRMED_MATCH = "No_Confirmed_Match"


class EstadoPublicacion(str, Enum):
    """Publication state (normalized)."""

    NO_PUBLICADA = "No_Publicada"
    PROGRAMADA = "Programada"
    PUBLICADA = "Publicada"
    ARCHIVADA = "Archivada"
    ERROR = "Error"


class MotivoRevision(str, Enum):
    """Normalized review reason."""

    CONTRADICCION_SUSTANTIVA = "Canon_Contradiccion_Sustantiva"
    APROBACION_ADMINISTRATIVA = "Canon_Aprobacion_Administrativa"
    RESTRICCION_NO_BLOQUEANTE = "Canon_Restriccion_No_Bloqueante"
    RESUELTO_RECONCILIACION_PENDIENTE = "Canon_Resuelto_Reconciliacion_Pendiente"
    INVENTARIO_RECONCILIACION_PENDIENTE = "Inventario_Reconciliacion_Pendiente"
    IDENTIDAD_RECONCILIADA = "Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente"


class ReconciliacionEstado(str, Enum):
    """Reconciliation state."""

    RESOLVED_PRODUCTION_SET = "Resolved_Production_Set"
    NO_CONFIRMED_MATCH = "No_Confirmed_Match"
    PENDING = "Pending"


class ReconciliacionConfianza(str, Enum):
    """Reconciliation confidence."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "None"
