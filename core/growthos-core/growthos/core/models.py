"""Pydantic models for GrowthOS domain entities."""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.config import ConfigDict

from growthos.core.enums import (
    EstadoPieza,
    Plataforma,
    TipoContenido,
    Categoria,
    Prioridad,
    DificultadProduccion,
    Reutilizable,
    BloqueadoCanon,
    EstadoCanon,
    EstadoProduccion,
    EstadoPublicacion,
    MotivoRevision,
    ReconciliacionEstado,
    ReconciliacionConfianza,
    LeadSource,
    DealStage,
    PaymentStatus,
    FunnelLine,
)


class Piece(BaseModel):
    """Content piece (CNT-####) - core identity entity."""

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        extra="allow",  # Allow extra fields from CSV
    )

    # Required identity
    id_pieza: str = Field(..., description="Unique piece ID (CNT-####)")
    fecha_creacion: Optional[date] = Field(default=None, description="Creation date")
    ultima_modificacion: Optional[datetime] = Field(default=None, description="Last modification timestamp")
    estado_operativo: EstadoPieza = Field(default=EstadoPieza.IDEA, description="Operational state")

    # Narrative fields
    titulo: Optional[str] = Field(default=None, description="Title/logline")
    tipo_contenido: Optional[TipoContenido] = Field(default=None, description="Content format")
    personaje_principal: Optional[str] = Field(default=None, description="Main character ID")
    personajes_secundarios: Optional[str] = Field(default=None, description="Secondary characters")
    lugar: Optional[str] = Field(default=None, description="Location ID")
    categoria_tematica: Optional[Categoria] = Field(default=None, description="Thematic category")

    # Strategic fields
    plataforma_principal: Optional[Plataforma] = Field(default=None, description="Primary platform")
    hipotesis_id: Optional[str] = Field(default=None, description="Hypothesis ID (HB-###)")
    objetivo: Optional[str] = Field(default=None, description="Strategic objective")
    prioridad: Optional[Prioridad] = Field(default=None, description="Priority level")
    dificultad_produccion: Optional[DificultadProduccion] = Field(default=None, description="Production difficulty")
    es_reutilizable: Optional[Reutilizable] = Field(default=None, description="Reuse flag")
    bloqueado_canon: Optional[BloqueadoCanon] = Field(default=None, description="Canon block flag")
    fecha_ultima_publicacion: Optional[date] = Field(default=None, description="Last publication date")
    dias_desde_publicacion: Optional[int] = Field(default=None, description="Days since last publication")

    # Source & asset tracking
    fuente: Optional[str] = Field(default=None, description="Source reference (file, Drive, etc.)")
    formato: Optional[str] = Field(default=None, description="Technical format specs")
    bloqueado_canon_detalle: Optional[str] = Field(default=None, description="Canon block detail")

    # Normalized operational fields
    estado_operacion_normalizado: Optional[EstadoProduccion] = Field(default=None)
    estado_canon_normalizado: Optional[EstadoCanon] = Field(default=None)
    asset_ref_confirmado: Optional[str] = Field(default=None)
    asset_ref_candidato: Optional[str] = Field(default=None)
    reconciliacion_estado: Optional[ReconciliacionEstado] = Field(default=None)
    reconciliacion_confianza: Optional[ReconciliacionConfianza] = Field(default=None)
    reconciliacion_fuente: Optional[str] = Field(default=None)
    reconciliacion_nota: Optional[str] = Field(default=None)
    registro_relacionado: Optional[str] = Field(default=None)
    drive_reference_id: Optional[str] = Field(default=None)
    meta_publication_id: Optional[str] = Field(default=None)
    meta_permalink: Optional[str] = Field(default=None)
    asset_set: Optional[str] = Field(default=None)
    asset_ref: Optional[str] = Field(default=None)
    asset_filename: Optional[str] = Field(default=None)
    drive_id: Optional[str] = Field(default=None)
    estado_canon: Optional[EstadoCanon] = Field(default=None)
    estado_produccion: Optional[EstadoProduccion] = Field(default=None)
    estado_publicacion: Optional[EstadoPublicacion] = Field(default=None)
    ultima_sincronizacion: Optional[date] = Field(default=None)
    motivo_revision_normalizado: Optional[MotivoRevision] = Field(default=None)
    personaje_principal_normalizado: Optional[str] = Field(default=None)
    personajes_secundarios_normalizados: Optional[str] = Field(default=None)
    rol_narrativo: Optional[str] = Field(default=None)
    tipo_humor_normalizado: Optional[str] = Field(default=None)
    potencial_etiquetado: Optional[str] = Field(default=None)
    confianza_taxonomia: Optional[str] = Field(default=None)
    fuente_taxonomia: Optional[str] = Field(default=None)
    nota_taxonomia: Optional[str] = Field(default=None)

    @field_validator("id_pieza")
    @classmethod
    def validate_piece_id(cls, v: str) -> str:
        """Validate CNT-#### format."""
        if v and not v.startswith("CNT-"):
            raise ValueError(f"ID_Pieza must start with 'CNT-': {v}")
        return v

    @field_validator("fecha_ultima_publicacion", "fecha_creacion", "ultima_sincronizacion", mode="before")
    @classmethod
    def parse_dates(cls, v):
        """Parse various date formats."""
        if v is None or v == "":
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, str):
            # Try multiple formats
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S%z"):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
        return v

    @model_validator(mode="after")
    def compute_days_since_publication(self) -> "Piece":
        """Calculate days since last publication."""
        if self.fecha_ultima_publicacion and self.dias_desde_publicacion is None:
            self.dias_desde_publicacion = (date.today() - self.fecha_ultima_publicacion).days
        return self


class Publication(BaseModel):
    """Publication log entry - one row per platform+date."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    id_pieza: str = Field(..., description="Reference to Piece (CNT-####)")
    publicacion_id: Optional[str] = Field(default=None, description="Unique publication ID")
    fecha_publicacion: Optional[date] = Field(default=None, description="Publication date")
    hora_publicacion: Optional[str] = Field(default=None, description="Publication time (HH:MM)")
    plataforma: Optional[Plataforma] = Field(default=None, description="Platform")
    meta_post_id: Optional[str] = Field(default=None, description="Meta Graph API post ID")
    meta_permalink: Optional[str] = Field(default=None, description="Post permalink")
    estado: Optional[EstadoPublicacion] = Field(default=None, description="Publication state")
    asset_filename: Optional[str] = Field(default=None, description="Asset filename used")
    caption: Optional[str] = Field(default=None, description="Posted caption")
    hashtags: Optional[str] = Field(default=None, description="Hashtags used")
    error_message: Optional[str] = Field(default=None, description="Error if failed")
    creado_en: Optional[datetime] = Field(default_factory=datetime.now, description="Log creation timestamp")
    actualizado_en: Optional[datetime] = Field(default_factory=datetime.now, description="Last update timestamp")

    @field_validator("fecha_publicacion", mode="before")
    @classmethod
    def parse_date(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
        return v


class Experiment(BaseModel):
    """Experiment log entry - quantitative learning."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    experiment_id: str = Field(..., description="Experiment ID (EXP-...)")
    hipotesis_id: Optional[str] = Field(default=None, description="Hypothesis ID (HB-###)")
    id_pieza: Optional[str] = Field(default=None, description="Related piece")
    publicacion_id: Optional[str] = Field(default=None, description="Related publication")
    fecha_publicacion: Optional[date] = Field(default=None)
    plataforma: Optional[Plataforma] = Field(default=None)
    formato: Optional[str] = Field(default=None)
    personaje: Optional[str] = Field(default=None)
    slot_horario: Optional[str] = Field(default=None)
    vistas: Optional[int] = Field(default=None)
    retencion_pct: Optional[float] = Field(default=None)
    interacciones: Optional[int] = Field(default=None)
    interacciones_24h: Optional[int] = Field(default=None)
    interacciones_72h: Optional[int] = Field(default=None)
    shares: Optional[int] = Field(default=None)
    comentarios: Optional[int] = Field(default=None)
    reactions: Optional[int] = Field(default=None)
    estado_canon: Optional[str] = Field(default=None)
    veredicto: Optional[str] = Field(default=None)
    conclusion: Optional[str] = Field(default=None)
    observaciones: Optional[str] = Field(default=None)


class CommunityEngagement(BaseModel):
    """Community engagement log - qualitative signals."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    comentario_id: str = Field(..., description="Unique comment ID")
    post_id: Optional[str] = Field(default=None, description="Post ID")
    cnt_id: Optional[str] = Field(default=None, description="Related content piece ID")
    tipo: Optional[str] = Field(default=None, description="Comment type")
    autor: Optional[str] = Field(default=None, description="Comment author")
    texto: Optional[str] = Field(default=None, description="Comment text")
    fecha_comentario: Optional[date] = Field(default=None)
    respuesta_estado: Optional[str] = Field(default=None)
    respuesta_texto: Optional[str] = Field(default=None)
    fecha_respuesta: Optional[date] = Field(default=None)
    accion_calendario: Optional[str] = Field(default=None)
    prioridad: Optional[Prioridad] = Field(default=None)
    ventana_revision: Optional[str] = Field(default=None)


class MetricsSnapshot(BaseModel):
    """Metrics Snapshot model."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    snapshot_id: str
    meta_post_id: str
    publication_id: Optional[str] = None
    target_at_utc: str
    window_type: str
    reactions: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    views: Optional[int] = None
    reach: Optional[int] = None
    retention_pct: Optional[float] = None
    validation_status: str = ""
    raw_response: str = ""
    error_message: str = ""
    created_at: Optional[date] = None


class AssetAlias(BaseModel):
    """Asset Alias model."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    alias_id: str
    asset_ref: str
    asset_filename: str = ""
    drive_id: str = ""
    meta_post_id: str = ""
    meta_permalink: str = ""
    fecha_publicacion: Optional[date] = None
    hora_publicacion: str = ""
    sha256: str = ""
    cnt_creation_allowed: bool = False
    confidence: Optional[ReconciliacionConfianza] = Field(default=None)
    proposed_record_type: str = ""
    canon_impact: str = ""
    status: str = ""
    evidence_path: str = ""
    notes: str = ""
    created_at: Optional[date] = None
    updated_at: Optional[date] = None


class Deal(BaseModel):
    """Deal model for CRM pipeline."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    deal_id: str
    tenant_id: str
    lead_source: Optional[LeadSource] = Field(default=None)
    deal_stage: DealStage = Field(default=DealStage.NEW)
    funnel_line: Optional[FunnelLine] = Field(default=None)
    amount: Optional[float] = None
    amount_collected: float = 0.0
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDIENTE)
    payment_method: str = ""
    payment_date: Optional[date] = None
    appointment_at: Optional[date] = None
    product_ref: str = ""
    source_publication_id: str = ""
    source_campaign_id: str = ""
    source_conversation_id: str = ""
    currency: str = "MXN"
    contact_name: str = ""
    contact_phone: str = ""
    contact_email: str = ""
    notes: str = ""
    lost_reason: str = ""
    created_at: Optional[date] = None
    updated_at: Optional[date] = None
    closed_at: Optional[date] = None

    @field_validator("amount", "amount_collected")
    @classmethod
    def _non_negative_money(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value < 0:
            raise ValueError("Los montos del deal no pueden ser negativos.")
        return value
