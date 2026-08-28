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
)


class Piece(BaseModel):
    """Content piece (CNT-####) - core identity entity."""

    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        extra="allow",  # Allow extra fields from CSV
    )

    # Required identity
    ID_Pieza: str = Field(..., description="Unique piece ID (CNT-####)")
    Fecha_Creacion: Optional[date] = Field(default=None, description="Creation date")
    Ultima_Modificacion: Optional[datetime] = Field(default=None, description="Last modification timestamp")
    Estado: EstadoPieza = Field(default=EstadoPieza.IDEA, description="Operational state")

    # Narrative fields
    Titulo: Optional[str] = Field(default=None, description="Title/logline")
    Tipo_Contenido: Optional[TipoContenido] = Field(default=None, description="Content format")
    Personaje_Principal: Optional[str] = Field(default=None, description="Main character ID")
    Personajes_Secundarios: Optional[str] = Field(default=None, description="Secondary characters")
    Lugar: Optional[str] = Field(default=None, description="Location ID")
    Categoria: Optional[Categoria] = Field(default=None, description="Thematic category")

    # Strategic fields
    Plataforma: Optional[Plataforma] = Field(default=None, description="Primary platform")
    Hipotesis_ID: Optional[str] = Field(default=None, description="Hypothesis ID (HB-###)")
    Objetivo: Optional[str] = Field(default=None, description="Strategic objective")
    Prioridad: Optional[Prioridad] = Field(default=None, description="Priority level")
    Dificultad_Produccion: Optional[DificultadProduccion] = Field(default=None, description="Production difficulty")
    Es_Reutilizable: Optional[Reutilizable] = Field(default=None, description="Reuse flag")
    Bloqueado_Canon: Optional[BloqueadoCanon] = Field(default=None, description="Canon block flag")
    Fecha_Ultima_Publicacion: Optional[date] = Field(default=None, description="Last publication date")
    Dias_Desde_Publicacion: Optional[int] = Field(default=None, description="Days since last publication")

    # Source & asset tracking
    Fuente: Optional[str] = Field(default=None, description="Source reference (file, Drive, etc.)")
    Formato: Optional[str] = Field(default=None, description="Technical format specs")
    Bloqueado_Canon_Detalle: Optional[str] = Field(default=None, description="Canon block detail")

    # Normalized operational fields
    Estado_Operacion_Normalizado: Optional[EstadoProduccion] = Field(default=None)
    Estado_Canon_Normalizado: Optional[EstadoCanon] = Field(default=None)
    Asset_Ref_Confirmado: Optional[str] = Field(default=None)
    Asset_Ref_Candidato: Optional[str] = Field(default=None)
    Reconciliacion_Estado: Optional[ReconciliacionEstado] = Field(default=None)
    Reconciliacion_Confianza: Optional[ReconciliacionConfianza] = Field(default=None)
    Reconciliacion_Fuente: Optional[str] = Field(default=None)
    Reconciliacion_Nota: Optional[str] = Field(default=None)
    Registro_Relacionado: Optional[str] = Field(default=None)
    Drive_Reference_ID: Optional[str] = Field(default=None)
    Meta_Publication_ID: Optional[str] = Field(default=None)
    Meta_Permalink: Optional[str] = Field(default=None)
    Asset_Set: Optional[str] = Field(default=None)
    Asset_Ref: Optional[str] = Field(default=None)
    Asset_Filename: Optional[str] = Field(default=None)
    Drive_ID: Optional[str] = Field(default=None)
    Estado_Canon: Optional[EstadoCanon] = Field(default=None)
    Estado_Produccion: Optional[EstadoProduccion] = Field(default=None)
    Estado_Publicacion: Optional[EstadoPublicacion] = Field(default=None)
    Ultima_Sincronizacion: Optional[date] = Field(default=None)
    Motivo_Revision_Normalizado: Optional[MotivoRevision] = Field(default=None)
    Personaje_Principal_Normalizado: Optional[str] = Field(default=None)
    Personajes_Secundarios_Normalizados: Optional[str] = Field(default=None)
    Rol_Narrativo: Optional[str] = Field(default=None)
    Tipo_Humor_Normalizado: Optional[str] = Field(default=None)
    Potencial_Etiquetado: Optional[str] = Field(default=None)
    Confianza_Taxonomia: Optional[str] = Field(default=None)
    Fuente_Taxonomia: Optional[str] = Field(default=None)
    Nota_Taxonomia: Optional[str] = Field(default=None)

    @field_validator("ID_Pieza")
    @classmethod
    def validate_piece_id(cls, v: str) -> str:
        """Validate CNT-#### format."""
        if v and not v.startswith("CNT-"):
            raise ValueError(f"ID_Pieza must start with 'CNT-': {v}")
        return v

    @field_validator("Fecha_Ultima_Publicacion", "Fecha_Creacion", "Ultima_Sincronizacion", mode="before")
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
        if self.Fecha_Ultima_Publicacion and self.Dias_Desde_Publicacion is None:
            self.Dias_Desde_Publicacion = (date.today() - self.Fecha_Ultima_Publicacion).days
        return self


class Publication(BaseModel):
    """Publication log entry - one row per platform+date."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    ID_Pieza: str = Field(..., description="Reference to Piece (CNT-####)")
    Publicacion_ID: Optional[str] = Field(default=None, description="Unique publication ID")
    Fecha_Publicacion: Optional[date] = Field(default=None, description="Publication date")
    Hora_Publicacion: Optional[str] = Field(default=None, description="Publication time (HH:MM)")
    Plataforma: Optional[Plataforma] = Field(default=None, description="Platform")
    Meta_Post_ID: Optional[str] = Field(default=None, description="Meta Graph API post ID")
    Meta_Permalink: Optional[str] = Field(default=None, description="Post permalink")
    Estado: Optional[EstadoPublicacion] = Field(default=None, description="Publication state")
    Asset_Filename: Optional[str] = Field(default=None, description="Asset filename used")
    Caption: Optional[str] = Field(default=None, description="Posted caption")
    Hashtags: Optional[str] = Field(default=None, description="Hashtags used")
    Error_Message: Optional[str] = Field(default=None, description="Error if failed")
    Creado_En: Optional[datetime] = Field(default_factory=datetime.now, description="Log creation timestamp")
    Actualizado_En: Optional[datetime] = Field(default_factory=datetime.now, description="Last update timestamp")

    @field_validator("Fecha_Publicacion", mode="before")
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

    Experiment_ID: str = Field(..., description="Experiment ID (EXP-...)")
    Hipotesis_ID: Optional[str] = Field(default=None, description="Hypothesis ID (HB-###)")
    ID_Pieza: Optional[str] = Field(default=None, description="Related piece")
    Publicacion_ID: Optional[str] = Field(default=None, description="Related publication")
    Fecha_Publicacion: Optional[date] = Field(default=None)
    Plataforma: Optional[Plataforma] = Field(default=None)
    Formato: Optional[str] = Field(default=None)
    Personaje: Optional[str] = Field(default=None)
    Slot_Horario: Optional[str] = Field(default=None)
    Vistas: Optional[int] = Field(default=None)
    Retencion_Pct: Optional[float] = Field(default=None)
    Interacciones: Optional[int] = Field(default=None)
    Interacciones_24h: Optional[int] = Field(default=None)
    Interacciones_72h: Optional[int] = Field(default=None)
    Shares: Optional[int] = Field(default=None)
    Comentarios: Optional[int] = Field(default=None)
    Reactions: Optional[int] = Field(default=None)
    Estado_Canon: Optional[str] = Field(default=None)
    Veredicto: Optional[str] = Field(default=None)
    Conclusion: Optional[str] = Field(default=None)
    Observaciones: Optional[str] = Field(default=None)


class CommunityEngagement(BaseModel):
    """Community engagement log - qualitative signals."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    Comentario_ID: str = Field(..., description="Unique comment ID")
    Post_ID: Optional[str] = Field(default=None, description="Meta Post ID")
    CNT_ID: Optional[str] = Field(default=None, description="Related piece")
    Tipo: Optional[str] = Field(default=None, description="Comment type")
    Autor: Optional[str] = Field(default=None, description="Comment author (anonymized)")
    Texto: Optional[str] = Field(default=None, description="Comment text")
    Fecha_Comentario: Optional[datetime] = Field(default=None)
    Respuesta_Estado: Optional[str] = Field(default=None, description="Response status")
    Respuesta_Texto: Optional[str] = Field(default=None, description="Response text")
    Fecha_Respuesta: Optional[datetime] = Field(default=None)
    Accion_Calendario: Optional[str] = Field(default=None, description="Calendar action triggered")
    Prioridad: Optional[str] = Field(default=None)
    Ventana_Revision: Optional[str] = Field(default=None)


class MetricsSnapshot(BaseModel):
    """Metrics snapshot for E0/E24/E72 windows."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    Snapshot_ID: str = Field(..., description="Unique snapshot ID")
    Meta_Post_ID: str = Field(..., description="Meta post ID")
    Publication_ID: Optional[str] = Field(default=None)
    Target_At_UTC: datetime = Field(..., description="Target timestamp for this snapshot")
    Captured_At_UTC: datetime = Field(default_factory=datetime.utcnow, description="Actual capture time")
    Window_Type: str = Field(..., description="E0, E24, or E72")
    Reactions: int = Field(default=0)
    Comments: int = Field(default=0)
    Shares: int = Field(default=0)
    Views: Optional[int] = Field(default=None)
    Reach: Optional[int] = Field(default=None)
    Retention_Pct: Optional[float] = Field(default=None)
    Validation_Status: str = Field(default="Pending", description="Valid_E0, Invalid, Pending")
    Raw_Response: Optional[str] = Field(default=None, description="Raw API response JSON")
    Error_Message: Optional[str] = Field(default=None)


class AssetAlias(BaseModel):
    """Asset alias (260####) mapping to pieces."""

    model_config = ConfigDict(use_enum_values=True, validate_assignment=True, extra="allow")

    Alias_ID: str = Field(..., description="Alias ID (ALIAS-####)")
    Asset_Ref: str = Field(..., description="Asset reference (260####)")
    Asset_Filename: Optional[str] = Field(default=None)
    Drive_ID: Optional[str] = Field(default=None)
    Meta_Post_ID: Optional[str] = Field(default=None)
    Meta_Permalink: Optional[str] = Field(default=None)
    Fecha_Publicacion: Optional[date] = Field(default=None)
    Hora_Publicacion: Optional[str] = Field(default=None)
    SHA256: Optional[str] = Field(default=None)
    CNT_Creation_Allowed: bool = Field(default=False)
    Confidence: Optional[ReconciliacionConfianza] = Field(default=None)
    Proposed_Record_Type: Optional[str] = Field(default=None)
    Canon_Impact: Optional[str] = Field(default=None)
    Status: str = Field(default="Pending_Admin_Approval")
    Evidence_Path: Optional[str] = Field(default=None)
    Notes: Optional[str] = Field(default=None)
