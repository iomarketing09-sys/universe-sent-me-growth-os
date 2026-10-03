"""Core models for the new GrowthOS."""

from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator, computed_field
from .enums import (
    EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad,
    DificultadProduccion, Reutilizable, BloqueadoCanon, EstadoCanon,
    EstadoProduccion, EstadoPublicacion, MotivoRevision,
    ReconciliacionEstado, ReconciliacionConfianza,
)


class Piece(BaseModel):
    """Piece model representing a content inventory item."""
    
    ID_Pieza: str
    Titulo: str = ""
    Personaje_Principal: str = ""
    Personajes_Secundarios: str = ""
    Tipo_Contenido: Optional[str] = None  # Store as string
    Plataforma: Optional[str] = None      # Store as string
    Objetivo: str = ""
    Hipotesis_ID: str = ""
    Estado: Optional[str] = None          # Store as string
    Prioridad: Optional[str] = None       # Store as string
    Dificultad_Produccion: Optional[str] = None  # Store as string
    Es_Reutilizable: Optional[str] = None  # Store as string
    Fecha_Ultima_Publicacion: Optional[date] = None
    Fuente: str = ""
    Formato: str = ""
    Categoria: Optional[str] = None       # Store as string
    Bloqueado_Canon: Optional[str] = None  # Store as string
    Estado_Operacion_Normalizado: str = ""
    Estado_Canon_Normalizado: str = ""
    Asset_Ref_Confirmado: str = ""
    Asset_Ref_Candidato: str = ""
    Reconciliacion_Estado: Optional[str] = None  # Store as string
    Reconciliacion_Confianza: Optional[str] = None  # Store as string
    Reconciliacion_Fuente: str = ""
    Reconciliacion_Nota: str = ""
    Registro_Relacionado: str = ""
    Drive_Reference_ID: str = ""
    Meta_Publication_ID: str = ""
    Meta_Permalink: str = ""
    Asset_Set: str = ""
    Asset_Ref: str = ""
    Asset_Filename: str = ""
    Drive_ID: str = ""
    Estado_Canon: Optional[str] = None    # Store as string
    Estado_Produccion: Optional[str] = None  # Store as string
    Estado_Publicacion: Optional[str] = None  # Store as string
    Ultima_Sincronizacion: str = ""
    Motivo_Revision_Normalizado: Optional[str] = None  # Store as string
    Personaje_Principal_Normalizado: str = ""
    Personajes_Secundarios_Normalizados: str = ""
    Rol_Narrativo: str = ""
    Tipo_Humor_Normalizado: str = ""
    Potencial_Etiquetado: str = ""
    Confianza_Taxonomia: str = ""
    Fuente_Taxonomia: str = ""
    Nota_Taxonomia: str = ""
    
    @field_validator('ID_Pieza')
    @classmethod
    def validate_id_pieza(cls, v):
        import re
        # Allow formats like CNT-0001, FB-0001, HB-001, etc.
        # Pattern: uppercase letters, hyphen, 1-4 digits
        pattern = r'^[A-Z]{2,4}-\d{1,4}$'
        if not isinstance(v, str) or not re.match(pattern, v):
            raise ValueError('Invalid piece ID format. Expected format like CNT-0001 or FB-0001')
        num_part = v.split('-')[1]
        if not (1 <= int(num_part) <= 9999):
            raise ValueError('Piece ID number out of range')
        return v
    
    @field_validator('Fecha_Ultima_Publicacion', mode='before')
    @classmethod
    def parse_fecha(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            if value.strip() == "":
                return None
        if isinstance(value, date):
            return value
        for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
            try:
                return date.strptime(value, fmt)
            except ValueError:
                pass
        return value
    
    @field_validator('Tipo_Contenido')
    @classmethod
    def validate_tipo_contenido(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in TipoContenido]
        if v not in valid_values:
            raise ValueError(f'Invalid Tipo_Contenido: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Plataforma')
    @classmethod
    def validate_plataforma(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in Plataforma]
        if v not in valid_values:
            raise ValueError(f'Invalid Plataforma: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Estado')
    @classmethod
    def validate_estado(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in EstadoPieza]
        if v not in valid_values:
            raise ValueError(f'Invalid Estado: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Prioridad')
    @classmethod
    def validate_prioridad(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in Prioridad]
        if v not in valid_values:
            raise ValueError(f'Invalid Prioridad: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Dificultad_Produccion')
    @classmethod
    def validate_dificultad_produccion(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in DificultadProduccion]
        if v not in valid_values:
            raise ValueError(f'Invalid Dificultad_Produccion: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Es_Reutilizable')
    @classmethod
    def validate_es_reutilizable(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in Reutilizable]
        if v not in valid_values:
            raise ValueError(f'Invalid Es_Reutilizable: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Categoria')
    @classmethod
    def validate_categoria(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in Categoria]
        if v not in valid_values:
            raise ValueError(f'Invalid Categoria: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Bloqueado_Canon')
    @classmethod
    def validate_bloqueado_canon(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in BloqueadoCanon]
        if v not in valid_values:
            raise ValueError(f'Invalid Bloqueado_Canon: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Estado_Canon')
    @classmethod
    def validate_estado_canon(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in EstadoCanon]
        if v not in valid_values:
            raise ValueError(f'Invalid Estado_Canon: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Estado_Produccion')
    @classmethod
    def validate_estado_produccion(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in EstadoProduccion]
        if v not in valid_values:
            raise ValueError(f'Invalid Estado_Produccion: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Estado_Publicacion')
    @classmethod
    def validate_estado_publicacion(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in EstadoPublicacion]
        if v not in valid_values:
            raise ValueError(f'Invalid Estado_Publicacion: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Motivo_Revision_Normalizado')
    @classmethod
    def validate_motivo_Revision_normalizado(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in MotivoRevision]
        if v not in valid_values:
            raise ValueError(f'Invalid Motivo_Revision_Normalizado: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Reconciliacion_Estado')
    @classmethod
    def validate_reconciliacion_estado(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in ReconciliacionEstado]
        if v not in valid_values:
            raise ValueError(f'Invalid Reconciliacion_Estado: {v}. Valid values: {valid_values}')
        return v
    
    @field_validator('Reconciliacion_Confianza')
    @classmethod
    def validate_reconciliacion_confianza(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in ReconciliacionConfianza]
        if v not in valid_values:
            raise ValueError(f'Invalid Reconciliacion_Confianza: {v}. Valid values: {valid_values}')
        return v
    
    @computed_field
    @property
    def Dias_Desde_Publicacion(self) -> Optional[int]:
        if self.Fecha_Ultima_Publicacion is None:
            return None
        today = date.today()
        delta = today - self.Fecha_Ultima_Publicacion
        return delta.days
    
    model_config = {
        'arbitrary_types_allowed': True,
        'validate_assignment': True,
        'extra': 'allow',
    }


class Publication(BaseModel):
    """Publication model."""
    ID_Pieza: str
    Publicacion_ID: str
    Fecha_Publicacion: Optional[date] = None
    Plataforma: Optional[str] = None
    Meta_Post_ID: str = ""

    @field_validator('Fecha_Publicacion', mode='before')
    @classmethod
    def parse_fecha(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            if value.strip() == "":
                return None
        if isinstance(value, date):
            return value
        for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
            try:
                return date.strptime(value, fmt)
            except ValueError:
                pass
        return value

    @field_validator('Plataforma')
    @classmethod
    def validate_plataforma(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in Plataforma]
        if v not in valid_values:
            raise ValueError(f'Invalid Plataforma: {v}. Valid values: {valid_values}')
        return v


class Experiment(BaseModel):
    """Experiment model."""
    Experiment_ID: str
    Hipotesis_ID: str
    ID_Pieza: str


class CommunityEngagement(BaseModel):
    """Community Engagement model."""
    ID: str
    Comentario_ID: str
    Post_ID: str
    CNT_ID: str
    Tipo: str
    Autor: str
    Texto: str
    Fecha_Comentario: Optional[date] = None
    Respuesta_Estado: str = ""
    Respuesta_Texto: str = ""
    Fecha_Respuesta: Optional[date] = None
    Accion_Calendario: str = ""
    Prioridad: Optional[str] = None
    Ventana_Revision: Optional[date] = None
    Created_At: Optional[date] = None

    @field_validator('Prioridad')
    @classmethod
    def validate_prioridad(cls, v):
        if v is None:
            return v
        valid_values = [e.value for e in Prioridad]
        if v not in valid_values:
            raise ValueError(f'Invalid Prioridad: {v}. Valid values: {valid_values}')
        return v


class MetricsSnapshot(BaseModel):
    """Metrics Snapshot model."""
    Snapshot_ID: str
    Meta_Post_ID: str
    Publication_ID: Optional[str] = None
    Target_At_UTC: str
    Window_Type: str
    Reactions: Optional[int] = None
    Comments: Optional[int] = None
    Shares: Optional[int] = None
    Views: Optional[int] = None
    Reach: Optional[int] = None
    Retention_Pct: Optional[float] = None
    Validation_Status: str = ""
    Raw_Response: str = ""
    Error_Message: str = ""
    Created_At: Optional[date] = None


class AssetAlias(BaseModel):
    """Asset Alias model."""
    Alias_ID: str
    Asset_Ref: str
    Asset_Filename: str = ""
    Drive_ID: str = ""
    Meta_Post_ID: str = ""
    Meta_Permalink: str = ""
    Fecha_Publicacion: Optional[date] = None
    Hora_Publicacion: str = ""
    SHA256: str = ""
    CNT_Creation_Allowed: bool = False
    Confidence: str = ""
    Proposed_Record_Type: str = ""
    Canon_Impact: str = ""
    Status: str = ""
    Evidence_Path: str = ""
    Notes: str = ""
    Created_At: Optional[date] = None
    Updated_At: Optional[date] = None
