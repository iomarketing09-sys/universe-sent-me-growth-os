#!/usr/bin/env python3
"""
Experiment Log + Hypothesis Bank para Growth OS

Registra observaciones de experimentos por pieza/publicación.
Permite aprendizaje sistemático y decisiones basadas en evidencia.

Basado en: universe-sent-me-growth-os/Operations/Research/ExperimentLog.csv
"""

import csv
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class NivelExperimento(str, Enum):
    """Nivel de agregación del experimento"""
    PIEZA = "Pieza"           # Una sola pieza
    COHORTE = "Cohorte"       # Grupo de piezas (ej. semana)
    CAMPANA = "Campaña"       # Campaña completa


class EstadoPublicacion(str, Enum):
    """Estado de la publicación al momento de la observación"""
    PROGRAMADA = "Programada"
    PUBLICADA = "Publicada"
    CANCELADA = "Cancelada"
    FALLIDA = "Fallida"


@dataclass
class Observacion:
    """Una observación en el Experiment Log"""
    # Identidad
    observacion_id: str = field(default_factory=lambda: f"OBS-{uuid.uuid4().hex[:8].upper()}")
    experiment_id: str = ""           # EXP-YYYY-MM-DESC
    hypothesis_id: str = ""           # HB-###
    nivel: str = NivelExperimento.PIEZA.value
    
    # Temporal
    fecha_inicio: str = ""            # YYYY-MM-DD
    fecha_fin: str = ""               # YYYY-MM-DD (vacío si en curso)
    
    # Contenido
    contenido_referencia: str = ""    # Descripción o ID_Pieza (CNT-####)
    plataforma: str = ""              # Facebook, Instagram, TikTok, etc.
    formato: str = ""                 # Foto, Reel, Carrusel, Video, Texto
    tipo_contenido: str = ""          # Humor, Educativo, Promocional, Narrativo, etc.
    posts_n: int = 1                  # Número de posts en esta observación
    
    # Métricas (se llenan cuando hay datos)
    interacciones_totales: int = 0
    interacciones_dia: float = 0.0
    mediana_interacciones: float = 0.0
    shares_interacciones: float = 0.0
    
    # Timing
    slot_planeado: str = ""           # HH:MM (24h)
    hora_real: str = ""               # HH:MM (24h) real
    meta_id: str = ""                 # Meta Post ID / Photo ID / Reel ID
    
    # Ventanas de medición (se llenan por worker E24/E72)
    interacciones_24h: int = 0
    interacciones_72h: int = 0
    
    # Canon y estado
    estado_canon: str = ""            # Aprobado, Canon_Clear, Canon_Review, No_aplica
    estado_publicacion: str = EstadoPublicacion.PROGRAMADA.value
    
    # Aprendizaje (se llena al cerrar)
    veredicto: str = ""               # Baseline, Resultado, Aprendizaje, etc.
    conclusion: str = ""              # Qué aprendimos
    proxima_accion: str = ""          # Qué hacer a continuación
    fuente: str = ""                  # Documento origen (ej. archivo markdown)
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec='seconds'))
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec='seconds'))
    
    # Campos internos
    _is_new: bool = field(default=True, repr=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a dict para CSV (excluye campos internos)"""
        d = asdict(self)
        d.pop('_is_new', None)
        return d
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Observacion':
        """Crea desde dict (CSV row)"""
        # Filtrar solo campos válidos
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in d.items() if k in valid_fields}
        return cls(**filtered)


# ==============================================================================
# EXPERIMENT LOG MANAGER
# ==============================================================================

EXPERIMENT_LOG_FIELDS = [
    'observacion_id', 'experiment_id', 'hypothesis_id', 'nivel',
    'fecha_inicio', 'fecha_fin',
    'contenido_referencia', 'plataforma', 'formato', 'tipo_contenido', 'posts_n',
    'interacciones_totales', 'interacciones_dia', 'mediana_interacciones', 'shares_interacciones',
    'slot_planeado', 'hora_real', 'meta_id',
    'interacciones_24h', 'interacciones_72h',
    'estado_canon', 'estado_publicacion',
    'veredicto', 'conclusion', 'proxima_accion', 'fuente',
    'created_at', 'updated_at'
]


def get_experiment_log_path(tenant_id: str) -> Path:
    """Ruta del experiment log para un tenant"""
    return Path(f'tenants/{tenant_id}/experiment_log.csv')


def load_experiment_log(tenant_id: str) -> List[Observacion]:
    """Carga todo el experiment log"""
    log_path = get_experiment_log_path(tenant_id)
    if not log_path.exists():
        return []
    
    observations = []
    with log_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                obs = Observacion.from_dict(row)
                obs._is_new = False
                observations.append(obs)
            except Exception as e:
                print(f"Warning: Error loading row: {e}")
    return observations


def save_experiment_log(tenant_id: str, observations: List[Observacion]) -> None:
    """Guarda todo el experiment log (append-only safe)"""
    log_path = get_experiment_log_path(tenant_id)
    
    # Ensure directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with log_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EXPERIMENT_LOG_FIELDS)
        writer.writeheader()
        for obs in observations:
            writer.writerow(obs.to_dict())


def append_observation(tenant_id: str, obs: Observacion) -> Observacion:
    """Agrega una observación nueva (append-only)"""
    observations = load_experiment_log(tenant_id)
    observations.append(obs)
    save_experiment_log(tenant_id, observations)
    return obs


def get_observations_for_piece(tenant_id: str, contenido_ref: str) -> List[Observacion]:
    """Obtiene todas las observaciones para una pieza/contenido específico"""
    all_obs = load_experiment_log(tenant_id)
    return [obs for obs in all_obs if obs.contenido_referencia == contenido_ref]


def get_observations_for_hypothesis(tenant_id: str, hypothesis_id: str) -> List[Observacion]:
    """Obtiene observaciones para una hipótesis"""
    all_obs = load_experiment_log(tenant_id)
    return [obs for obs in all_obs if obs.hypothesis_id == hypothesis_id]


def update_observation(tenant_id: str, observacion_id: str, **updates) -> Optional[Observacion]:
    """Actualiza una observación existente"""
    observations = load_experiment_log(tenant_id)
    for obs in observations:
        if obs.observacion_id == observacion_id:
            for key, value in updates.items():
                if hasattr(obs, key):
                    setattr(obs, key, value)
            obs.updated_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
            save_experiment_log(tenant_id, observations)
            return obs
    return None


def close_observation(tenant_id: str, observacion_id: str, 
                      veredicto: str, conclusion: str, proxima_accion: str,
                      interacciones_totales: int = 0, mediana_interacciones: float = 0.0,
                      interacciones_24h: int = 0, interacciones_72h: int = 0) -> Optional[Observacion]:
    """Cierra una observación con veredicto final y métricas"""
    return update_observation(tenant_id, observacion_id,
        veredicto=veredicto,
        conclusion=conclusion,
        proxima_accion=proxima_accion,
        fecha_fin=datetime.now().strftime('%Y-%m-%d'),
        estado_publicacion=EstadoPublicacion.PUBLICADA.value,
        interacciones_totales=interacciones_totales,
        mediana_interacciones=mediana_interacciones,
        interacciones_24h=interacciones_24h,
        interacciones_72h=interacciones_72h
    )


# ==============================================================================
# HYPOTHESIS BANK
# ==============================================================================

@dataclass
class Hipotesis:
    """Entrada en el Hypothesis Bank"""
    hypothesis_id: str = ""           # HB-###
    descripcion: str = ""             # Qué se quiere validar
    metrica_principal: str = ""       # Mediana_interacciones, Shares, etc.
    criterio_exito: str = ""          # "Mediana > 30 en 7 días"
    estado: str = "Activa"            # Activa, Validada, Rechazada, En_prueba
    fecha_creacion: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    fecha_cierre: str = ""
    observaciones_ids: List[str] = field(default_factory=list)
    veredicto_final: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def get_hypothesis_bank_path(tenant_id: str) -> Path:
    return Path(f'tenants/{tenant_id}/hypothesis_bank.csv')


HYPOTHESIS_FIELDS = [
    'hypothesis_id', 'descripcion', 'metrica_principal', 'criterio_exito',
    'estado', 'fecha_creacion', 'fecha_cierre', 'observaciones_ids', 'veredicto_final'
]


def load_hypothesis_bank(tenant_id: str) -> List[Hipotesis]:
    path = get_hypothesis_bank_path(tenant_id)
    if not path.exists():
        return []
    hypotheses = []
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse observaciones_ids
            if row.get('observaciones_ids'):
                row['observaciones_ids'] = row['observaciones_ids'].split('|')
            else:
                row['observaciones_ids'] = []
            hypotheses.append(Hipotesis(**row))
    return hypotheses


def save_hypothesis_bank(tenant_id: str, hypotheses: List[Hipotesis]) -> None:
    path = get_hypothesis_bank_path(tenant_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HYPOTHESIS_FIELDS)
        writer.writeheader()
        for h in hypotheses:
            d = h.to_dict()
            d['observaciones_ids'] = '|'.join(d['observaciones_ids'])
            writer.writerow(d)


def add_hypothesis(tenant_id: str, hypothesis: Hipotesis) -> Hipotesis:
    hypotheses = load_hypothesis_bank(tenant_id)
    hypotheses.append(hypothesis)
    save_hypothesis_bank(tenant_id, hypotheses)
    return hypothesis


def get_hypothesis(tenant_id: str, hypothesis_id: str) -> Optional[Hipotesis]:
    for h in load_hypothesis_bank(tenant_id):
        if h.hypothesis_id == hypothesis_id:
            return h
    return None


def link_observation_to_hypothesis(tenant_id: str, hypothesis_id: str, observacion_id: str) -> None:
    """Vincula una observación a una hipótesis"""
    hypotheses = load_hypothesis_bank(tenant_id)
    for h in hypotheses:
        if h.hypothesis_id == hypothesis_id:
            if observacion_id not in h.observaciones_ids:
                h.observaciones_ids.append(observacion_id)
    save_hypothesis_bank(tenant_id, hypotheses)


# ==============================================================================
# HELPERS PARA INTEGRACIÓN CON PUBLICACIÓN
# ==============================================================================

def create_observation_from_publication(
    tenant_id: str,
    publication_row: Dict[str, str],
    hypothesis_id: str = "",
    experiment_id: str = ""
) -> Observacion:
    """
    Crea una observación inicial a partir de una fila de publication_log.
    Se llama después de publicar exitosamente.
    """
    now = datetime.now()
    fecha_hoy = now.strftime('%Y-%m-%d')
    hora_ahora = now.strftime('%H:%M')
    
    obs = Observacion(
        experiment_id=experiment_id or f"EXP-{fecha_hoy}-{publication_row.get('tenant_id', 'FB')[:2].upper()}",
        hypothesis_id=hypothesis_id,
        nivel=NivelExperimento.PIEZA.value,
        fecha_inicio=fecha_hoy,
        contenido_referencia=publication_row.get('piece', '') or publication_row.get('asset_filename', ''),
        plataforma=publication_row.get('platform', '').split('/')[0],  # "Facebook/Instagram" -> "Facebook"
        formato=publication_row.get('piece', '').split()[-1] if publication_row.get('piece') else 'Foto',
        tipo_contenido='',  # Se infiere o se deja para completar
        posts_n=1,
        slot_planeado=publication_row.get('time', ''),
        hora_real=hora_ahora,
        meta_id=publication_row.get('publication_id', ''),
        estado_canon='Aprobado',  # Asumimos que si se publicó, pasó canon
        estado_publicacion=EstadoPublicacion.PUBLICADA.value,
        fuente=f"Publicación {publication_row.get('date', '')} {publication_row.get('time', '')}"
    )
    return obs


# ==============================================================================
# CLI PARA TESTING
# ==============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python -m growth.experiment_log <tenant_id> [comando]")
        print("Comandos: list, add-hypothesis, show-hypothesis")
        sys.exit(1)
    
    tenant = sys.argv[1]
    
    if len(sys.argv) == 2 or sys.argv[2] == 'list':
        obs = load_experiment_log(tenant)
        print(f"Experiment Log ({tenant}): {len(obs)} observaciones")
        for o in obs[-5:]:
            print(f"  {o.observacion_id} | {o.contenido_referencia} | {o.veredicto or 'en curso'}")
    
    elif sys.argv[2] == 'add-hypothesis':
        h = Hipotesis(
            hypothesis_id=f"HB-{len(load_hypothesis_bank(tenant))+1:03d}",
            descripcion=input("Descripción: "),
            metrica_principal=input("Métrica principal: "),
            criterio_exito=input("Criterio de éxito: ")
        )
        add_hypothesis(tenant, h)
        print(f"Hipótesis agregada: {h.hypothesis_id}")
    
    elif sys.argv[2] == 'show-hypothesis':
        h = get_hypothesis(tenant, sys.argv[3])
        if h:
            print(f"{h.hypothesis_id}: {h.descripcion}")
            print(f"  Estado: {h.estado}")
            print(f"  Observaciones: {h.observaciones_ids}")
        else:
            print("No encontrada")
