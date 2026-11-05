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


def get_experiment_log_path(tenant_id: str, base_path: Optional[Path] = None) -> Path:
    """Ruta del experiment log para un tenant"""
    root = Path(base_path) if base_path else Path('.')
    return root / 'tenants' / tenant_id / 'experiment_log.csv'


def load_experiment_log(tenant_id: str, base_path: Optional[Path] = None) -> List[Observacion]:
    """Carga todo el experiment log"""
    log_path = get_experiment_log_path(tenant_id, base_path)
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


def save_experiment_log(
    tenant_id: str,
    observations: List[Observacion],
    base_path: Optional[Path] = None,
) -> None:
    """Guarda todo el experiment log (append-only safe)"""
    log_path = get_experiment_log_path(tenant_id, base_path)
    
    # Ensure directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with log_path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=EXPERIMENT_LOG_FIELDS)
        writer.writeheader()
        for obs in observations:
            writer.writerow(obs.to_dict())


def append_observation(
    tenant_id: str,
    obs: Observacion,
    base_path: Optional[Path] = None,
) -> Observacion:
    """Agrega una observación nueva (append-only)"""
    observations = load_experiment_log(tenant_id, base_path)
    observations.append(obs)
    save_experiment_log(tenant_id, observations, base_path)
    return obs


def sync_observation(
    tenant_id: str,
    *,
    meta_id: str,
    plataforma: str = "",
    contenido_referencia: str = "",
    fecha: str = "",
    slot: str = "",
    hypothesis_id: str = "",
    experiment_id: str = "",
    formato: str = "",
    tipo_contenido: str = "",
    window: str = "",
    interacciones: int = 0,
    base_path: Optional[Path] = None,
) -> Optional[Observacion]:
    """Crea o actualiza la observación de una pieza a partir de sus métricas.

    Es idempotente por ``meta_id``: cada publicación tiene una sola fila que se
    va completando con las ventanas E24/E72. No cierra la observación: el
    veredicto sigue siendo una decisión humana.
    """
    if not meta_id:
        return None
    hypothesis_id = str(hypothesis_id or "").strip()
    experiment_id = str(experiment_id or "").strip()
    observations = load_experiment_log(tenant_id, base_path)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    target = next((obs for obs in observations if obs.meta_id == meta_id), None)
    if target is None:
        month = (fecha or datetime.now().strftime("%Y-%m-%d"))[:7]
        target = Observacion(
            experiment_id=experiment_id or f"EXP-{month}-AUTO",
            hypothesis_id=hypothesis_id,
            nivel=NivelExperimento.PIEZA.value,
            fecha_inicio=fecha,
            contenido_referencia=contenido_referencia,
            plataforma=plataforma,
            formato=formato,
            tipo_contenido=tipo_contenido,
            slot_planeado=slot,
            meta_id=meta_id,
            estado_publicacion=EstadoPublicacion.PUBLICADA.value,
            fuente="metrics_snapshot",
            created_at=now,
            updated_at=now,
        )
        observations.append(target)
    else:
        if contenido_referencia and not target.contenido_referencia:
            target.contenido_referencia = contenido_referencia
        if slot and not target.slot_planeado:
            target.slot_planeado = slot
        if fecha and not target.fecha_inicio:
            target.fecha_inicio = fecha
        if hypothesis_id and not target.hypothesis_id:
            target.hypothesis_id = hypothesis_id
        if experiment_id and (
            not target.experiment_id or target.experiment_id.endswith("-AUTO")
        ):
            target.experiment_id = experiment_id
        if formato and not target.formato:
            target.formato = formato
        if tipo_contenido and not target.tipo_contenido:
            target.tipo_contenido = tipo_contenido
        target.estado_publicacion = EstadoPublicacion.PUBLICADA.value

    value = int(interacciones or 0)
    if window == "E24":
        target.interacciones_24h = max(int(target.interacciones_24h or 0), value)
    elif window == "E72":
        target.interacciones_72h = max(int(target.interacciones_72h or 0), value)
    target.interacciones_totales = max(int(target.interacciones_totales or 0), value)
    target.updated_at = now
    save_experiment_log(tenant_id, observations, base_path)
    if target.hypothesis_id:
        link_observation_to_hypothesis(
            tenant_id,
            target.hypothesis_id,
            target.observacion_id,
            base_path=base_path,
        )
    return target


def get_observations_for_piece(
    tenant_id: str,
    contenido_ref: str,
    base_path: Optional[Path] = None,
) -> List[Observacion]:
    """Obtiene todas las observaciones para una pieza/contenido específico"""
    all_obs = load_experiment_log(tenant_id, base_path)
    return [obs for obs in all_obs if obs.contenido_referencia == contenido_ref]


def get_observations_for_hypothesis(
    tenant_id: str,
    hypothesis_id: str,
    base_path: Optional[Path] = None,
) -> List[Observacion]:
    """Obtiene observaciones para una hipótesis"""
    all_obs = load_experiment_log(tenant_id, base_path)
    return [obs for obs in all_obs if obs.hypothesis_id == hypothesis_id]


def get_observation_by_meta_id(
    tenant_id: str,
    meta_id: str,
    base_path: Optional[Path] = None,
) -> Optional[Observacion]:
    """Busca una observación por el ID nativo de Meta."""
    if not meta_id:
        return None
    return next(
        (obs for obs in load_experiment_log(tenant_id, base_path) if obs.meta_id == meta_id),
        None,
    )


def update_observation(
    tenant_id: str,
    observacion_id: str,
    base_path: Optional[Path] = None,
    **updates,
) -> Optional[Observacion]:
    """Actualiza una observación existente"""
    observations = load_experiment_log(tenant_id, base_path)
    for obs in observations:
        if obs.observacion_id == observacion_id:
            for key, value in updates.items():
                if hasattr(obs, key):
                    setattr(obs, key, value)
            obs.updated_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
            save_experiment_log(tenant_id, observations, base_path)
            return obs
    return None


def close_observation(tenant_id: str, observacion_id: str, 
                      veredicto: str, conclusion: str, proxima_accion: str,
                      interacciones_totales: int = 0, mediana_interacciones: float = 0.0,
                      interacciones_24h: int = 0, interacciones_72h: int = 0,
                      base_path: Optional[Path] = None) -> Optional[Observacion]:
    """Cierra una observación con veredicto final y métricas"""
    return update_observation(tenant_id, observacion_id,
        base_path=base_path,
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


def close_observation_by_meta_id(
    tenant_id: str,
    meta_id: str,
    veredicto: str,
    conclusion: str,
    proxima_accion: str,
    base_path: Optional[Path] = None,
) -> Optional[Observacion]:
    """Cierra una observación usando el ID nativo de Meta."""
    observation = get_observation_by_meta_id(tenant_id, meta_id, base_path)
    if observation is None:
        return None
    return close_observation(
        tenant_id,
        observation.observacion_id,
        veredicto=veredicto,
        conclusion=conclusion,
        proxima_accion=proxima_accion,
        base_path=base_path,
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


def get_hypothesis_bank_path(
    tenant_id: str,
    base_path: Optional[Path] = None,
) -> Path:
    """Ruta canónica del banco, con compatibilidad para ledgers legados.

    El lugar canónico es ``tenants/<tenant>/experiments/hypothesis_bank.csv``.
    Algunos tenants antiguos lo tienen en la raíz del tenant; se respeta si el
    archivo canónico todavía no existe.
    """
    root = Path(base_path) if base_path else Path('.')
    tenant_dir = root / 'tenants' / tenant_id
    preferred = tenant_dir / 'experiments' / 'hypothesis_bank.csv'
    legacy = tenant_dir / 'hypothesis_bank.csv'
    if preferred.exists():
        return preferred
    if legacy.exists():
        return legacy
    return preferred


HYPOTHESIS_FIELDS = [
    'hypothesis_id', 'descripcion', 'metrica_principal', 'criterio_exito',
    'estado', 'fecha_creacion', 'fecha_cierre', 'observaciones_ids', 'veredicto_final'
]


def load_hypothesis_bank(
    tenant_id: str,
    base_path: Optional[Path] = None,
) -> List[Hipotesis]:
    path = get_hypothesis_bank_path(tenant_id, base_path)
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


def save_hypothesis_bank(
    tenant_id: str,
    hypotheses: List[Hipotesis],
    base_path: Optional[Path] = None,
) -> None:
    path = get_hypothesis_bank_path(tenant_id, base_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HYPOTHESIS_FIELDS)
        writer.writeheader()
        for h in hypotheses:
            d = h.to_dict()
            d['observaciones_ids'] = '|'.join(d['observaciones_ids'])
            writer.writerow(d)


def add_hypothesis(
    tenant_id: str,
    hypothesis: Hipotesis,
    base_path: Optional[Path] = None,
) -> Hipotesis:
    hypotheses = load_hypothesis_bank(tenant_id, base_path)
    hypotheses.append(hypothesis)
    save_hypothesis_bank(tenant_id, hypotheses, base_path)
    return hypothesis


def get_hypothesis(
    tenant_id: str,
    hypothesis_id: str,
    base_path: Optional[Path] = None,
) -> Optional[Hipotesis]:
    for h in load_hypothesis_bank(tenant_id, base_path):
        if h.hypothesis_id == hypothesis_id:
            return h
    return None


def link_observation_to_hypothesis(
    tenant_id: str,
    hypothesis_id: str,
    observacion_id: str,
    base_path: Optional[Path] = None,
) -> bool:
    """Vincula una observación a una hipótesis en ambos sentidos.

    Devuelve ``False`` si la observación o la hipótesis no existen; no crea un
    banco vacío para una hipótesis desconocida.
    """
    observations = load_experiment_log(tenant_id, base_path)
    observation = next(
        (obs for obs in observations if obs.observacion_id == observacion_id),
        None,
    )
    if observation is None:
        return False

    hypotheses = load_hypothesis_bank(tenant_id, base_path)
    hypothesis = next(
        (h for h in hypotheses if h.hypothesis_id == hypothesis_id),
        None,
    )
    if hypothesis is None:
        return False

    changed = False
    if observation.hypothesis_id != hypothesis_id:
        observation.hypothesis_id = hypothesis_id
        observation.updated_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
        changed = True
    if observacion_id not in hypothesis.observaciones_ids:
        hypothesis.observaciones_ids.append(observacion_id)
        changed = True

    if changed:
        save_experiment_log(tenant_id, observations, base_path)
        save_hypothesis_bank(tenant_id, hypotheses, base_path)
    return True


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
    hypothesis_id = hypothesis_id or str(publication_row.get('hypothesis_id') or '')
    experiment_id = experiment_id or str(publication_row.get('experiment_id') or '')
    
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
# CLI
# ==============================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Experiment log y hypothesis bank")
    parser.add_argument("tenant")
    parser.add_argument("--base-path", type=Path, default=Path("."))
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list")

    show_parser = subparsers.add_parser("show-hypothesis")
    show_parser.add_argument("hypothesis_id")

    link_parser = subparsers.add_parser("link")
    link_parser.add_argument("meta_id")
    link_parser.add_argument("hypothesis_id")

    close_parser = subparsers.add_parser("close")
    close_parser.add_argument("meta_id")
    close_parser.add_argument("--veredicto", required=True)
    close_parser.add_argument("--conclusion", required=True)
    close_parser.add_argument("--proxima-accion", default="")

    add_parser = subparsers.add_parser("add-hypothesis")
    add_parser.add_argument("--descripcion", default="")
    add_parser.add_argument("--metrica", default="")
    add_parser.add_argument("--criterio", default="")

    args = parser.parse_args()
    tenant = args.tenant
    base_path = args.base_path

    if args.command in (None, "list"):
        observations = load_experiment_log(tenant, base_path)
        print(f"Experiment Log ({tenant}): {len(observations)} observaciones")
        for observation in observations[-10:]:
            print(
                f"  {observation.observacion_id} | {observation.meta_id} | "
                f"{observation.hypothesis_id or '-'} | {observation.veredicto or 'en curso'}"
            )

    elif args.command == "show-hypothesis":
        hypothesis = get_hypothesis(tenant, args.hypothesis_id, base_path)
        if hypothesis:
            print(f"{hypothesis.hypothesis_id}: {hypothesis.descripcion}")
            print(f"  Estado: {hypothesis.estado}")
            print(f"  Observaciones: {hypothesis.observaciones_ids}")
        else:
            print("No encontrada")

    elif args.command == "link":
        observation = get_observation_by_meta_id(tenant, args.meta_id, base_path)
        if observation is None:
            print("Observación no encontrada")
            raise SystemExit(1)
        linked = link_observation_to_hypothesis(
            tenant,
            args.hypothesis_id,
            observation.observacion_id,
            base_path,
        )
        if not linked:
            print("Hipótesis no encontrada")
            raise SystemExit(1)
        print(f"Vinculada {observation.observacion_id} -> {args.hypothesis_id}")

    elif args.command == "close":
        observation = close_observation_by_meta_id(
            tenant,
            args.meta_id,
            veredicto=args.veredicto,
            conclusion=args.conclusion,
            proxima_accion=args.proxima_accion,
            base_path=base_path,
        )
        if observation is None:
            print("Observación no encontrada")
            raise SystemExit(1)
        print(f"Cerrada {observation.observacion_id}: {observation.veredicto}")

    elif args.command == "add-hypothesis":
        hypothesis = Hipotesis(
            hypothesis_id=f"HB-{len(load_hypothesis_bank(tenant, base_path)) + 1:03d}",
            descripcion=args.descripcion or input("Descripción: "),
            metrica_principal=args.metrica or input("Métrica principal: "),
            criterio_exito=args.criterio or input("Criterio de éxito: "),
        )
        add_hypothesis(tenant, hypothesis, base_path)
        print(f"Hipótesis agregada: {hypothesis.hypothesis_id}")
