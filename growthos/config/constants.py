"""Centralized constants and allowed values for GrowthOS."""

# Character IDs (from Canon)
CHARACTER_IDS = [
    "@char_USM_universe",
    "@char_USM_wilfred",
    "@char_USM_elara",
    "@char_USM_ganso",
    "@char_USM_payaso",
    "@char_USM_hada",
    "@char_USM_evan",
    "@char_USM_kael",
    "@char_USM_maeve",
    "@char_USM_fantasma",
]

# Location IDs (from Canon)
LOCATION_IDS = [
    "@loc_USM_bosque",
    "@loc_USM_torre",
    "@loc_USM_claridad",
    "@loc_USM_sueños",
    "@loc_USM_mercado",
    "@loc_USM_hogar",
    "N/A",
]

# Platforms
PLATAFORMAS = [
    "Instagram",
    "Facebook",
    "TikTok",
    "YouTube Shorts",
    "Multi",
]

# Content Types
TIPOS_CONTENIDO = [
    "Reel",
    "Carrusel",
    "Foto",
    "Historia",
    "Trailer",
    "Texto",
    "Reel / Meme adaptado",
    "Reel / Sección recurrente",
    "Mini-historia serializada",
]

# Categories
CATEGORIAS = [
    "Humor",
    "Filosofía",
    "Tarot",
    "Magia",
    "Narrativa",
    "Afiliación",
    "Educación",
    "Marca / Narrativa / Resonancia",
    "Humor / Meme",
    "Humor / Reseña / Comerciar",
]

# Priorities
PRIORIDADES = ["Alta", "Media", "Baja"]

# Production Difficulty
DIFICULTADES = ["Muy_Baja", "Baja", "Media", "Alta"]

# Reutilizable
REUTILIZABLE_OPTIONS = ["Sí", "No"]

# Canon Block
BLOQUEADO_CANON_OPTIONS = ["Sí", "No"]

# Estados de la pieza (maquina de estados)
ESTADOS_PIEZA = [
    "Idea",
    "Pendiente de Producción",
    "En Producción",
    "Pendiente Revisión Claude",
    "Pendiente Aprobación Fernando",
    "Aprobado",
    "Rechazado / Requiere Reescritura",
    "Programado",
    "Publicado",
    "En Análisis",
    "Archivado",
    "Reutilizado / Archivado",
    "Diferido",
    "Bloqueado",
]

# Estado Canon (normalizado)
ESTADOS_CANON = [
    "Libre",
    "Revision",
    "Aprobado",
    "Bloqueado",
    "Canon_Clear_or_Unverified",
    "Canon_Review_Required",
    "Canon_Constrained",
    "Canon_Partial",
    "Canon_Resuelto_Reconciliacion_Pendiente",
    "Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente",
    "Inventario_Reconciliacion_Pendiente",
    "Canon_Aprobacion_Administrativa",
    "Canon_Restriccion_No_Bloqueante",
    "Canon_Contradiccion_Sustantiva",
    "Deferred_Operational",
]

# Estado Producción (normalizado)
ESTADOS_PRODUCCION = [
    "Idea",
    "En_Produccion",
    "Asset_Listo",
    "Pendiente_Revision",
    "Diferido",
    "Production_Pending",
    "Resolved_Production_Set",
    "No_Confirmed_Match",
]

# Estado Publicación (normalizado)
ESTADOS_PUBLICACION = [
    "No_Publicada",
    "Programada",
    "Publicada",
    "Archivada",
    "Error",
]

# Motivos de revisión normalizados
MOTIVOS_REVISION = [
    "Canon_Contradiccion_Sustantiva",
    "Canon_Aprobacion_Administrativa",
    "Canon_Restriccion_No_Bloqueante",
    "Canon_Resuelto_Reconciliacion_Pendiente",
    "Inventario_Reconciliacion_Pendiente",
    "Identidad_Reconciliada_Sin_Conflicto_Canon_Evidente",
]

# Reconciliation states
RECONCILIACION_ESTADOS = [
    "Resolved_Production_Set",
    "No_Confirmed_Match",
    "Pending",
]

RECONCILIACION_CONFIANZA = ["High", "Medium", "Low", "None"]

# Hypothesis IDs format
HIPOTESIS_PREFIX = "HB-"

# Experiment IDs format
EXPERIMENT_PREFIX = "EXP-"

# Asset refs (260####)
ASSET_REF_PREFIX = "260"

# Piece ID format
PIECE_ID_PREFIX = "CNT-"
PIECE_ID_PATTERN = r"^CNT-\d{4}$"
