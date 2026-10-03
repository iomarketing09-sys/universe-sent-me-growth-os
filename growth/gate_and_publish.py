"""
Gate de auditoría + publicación simplificado con idempotencia básica y enriquecimiento de datos.

Consolida la lógica de:
- audit.py (auditoría de assets)
- workflow.py (orquestación)
- publisher.py (publicación condicionada)

En una única operación clara:
    validate_and_publish(csv_path, meta_import_path, tenant_id, publisher) -> result

Idempotencia: si row["publication_id"] existe (post_id de Meta), NO se vuelve a publicar.
Enriquecimiento: si se proporciona meta_import_path, se usan sus captions y hashtags.
"""
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import csv
from datetime import datetime

from growth.asset_validation import audit_publications
from growth.publication_tracker import (
    load_publications,
    pending_publications,
    REQUIRED_COLUMNS,
)


def _write_publications(csv_path: Path, rows: List[Dict[str, str]]) -> None:
    """Escribe todas las filas al CSV manteniendo el orden de columnas."""
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _load_meta_import(meta_import_path: Path) -> Dict[str, Dict[str, str]]:
    """
    Carga meta_import.csv y crea un diccionario de búsqueda por (date, time, media_filename).
    
    Returns:
        Diccionario con clave (date_str, time_24, media_filename) -> fila completa
    """
    if not meta_import_path.exists():
        return {}
    
    lookup = {}
    with meta_import_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalizar date y time para matching
            date_str = row.get('Date (YYYY-MM-DD)', '').strip()
            time_str = row.get('Time (HH:MM, 24h)', '').strip()
            
            # Convertir a formato 24h si es necesario (aunque ya debería estar en 24h)
            try:
                if time_str and ('AM' in time_str.upper() or 'PM' in time_str.upper()):
                    dt = datetime.strptime(time_str, '%I:%M %p')
                    time_24 = dt.strftime('%H:%M')
                else:
                    time_24 = time_str
            except:
                time_24 = time_str
            
            media_filename = row.get('Media URL', '').strip()
            
            # Crear clave de búsqueda
            key = (date_str, time_24, media_filename)
            lookup[key] = row
    
    return lookup


def validate_and_publish(
    csv_path: Path,
    tenant_id: str = "firma-bordados",
    publisher: Optional[Any] = None,
    publish_fn: Optional[Callable] = None,
    meta_import_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Ejecuta gate de auditoría y publica si pasa.

    Idempotencia: filas con publication_id (post_id de Meta) se saltan.
    Enriquecimiento: si se proporciona meta_import_path, se usan sus captions y hashtags.

    Args:
        csv_path: Ruta al publication_log.csv
        tenant_id: ID del tenant (para validación de assets)
        publisher: Instancia de MetaPublisher (opcional, para publicación real)
        publish_fn: Función personalizada de publicación (row, publisher) -> MetaResponse
                   La fila será enriquecida con datos de meta_import si se proporciona
        meta_import_path: Ruta opcional al meta_import.csv para enriquecer datos
    
    Returns:
        Diccionario con:
            - success: bool
            - published_count: int
            - blocked: bool
            - audit: dict (total, missing, ambiguous, problematic_rows, ready_for_publication)
            - error: str | None
            - results: List[MetaResponse] si se publicó
    """
    # 1. Gate de auditoría
    if not csv_path.exists():
        return {
            "success": False,
            "published_count": 0,
            "blocked": True,
            "audit": {"total": 0, "missing": 0, "ambiguous": 0, "problematic_rows": [], "ready_for_publication": False},
            "error": f"CSV no encontrado: {csv_path}",
            "results": []
        }

    audit_result = audit_publications(csv_path, tenant_id)

    if not audit_result["ready_for_publication"]:
        return {
            "success": False,
            "published_count": 0,
            "blocked": True,
            "audit": audit_result,
            "error": "Gate de auditoría: hay assets MISSING o AMBIGUOUS",
            "results": []
        }

    # 2. GATE PASÓ: ready_for_publication == True
    all_rows = load_publications(csv_path)
    
    # Cargar meta_import para enriquecimiento si se proporciona
    meta_lookup = {}
    if meta_import_path and meta_import_path.exists():
        meta_lookup = _load_meta_import(meta_import_path)
    
    now = datetime.now().isoformat(timespec="seconds")
    results = []
    published_count = 0
    skipped_count = 0

    # 3. Publicar cada fila pendiente (solo si NO tiene publication_id)
    for row in all_rows:
        slot_id = row.get("publication_id") or row.get("piece") or f"row_{published_count}"
        
        # IDEMPOTENCIA: si ya tiene post_id de Meta, saltar
        if row.get("publication_id", "").strip():
            skipped_count += 1
            continue
        
        # Enriquecer fila con datos de meta_import si está disponible
        enriched_row = row.copy()
        if meta_lookup:
            # Crear clave de búsqueda a partir de la fila de publication_log
            date_str = row.get('date', '').strip()
            time_str = row.get('time', '').strip()
            
            # Normalizar time a 24h para matching
            try:
                if time_str and ('AM' in time_str.upper() or 'PM' in time_str.upper()):
                    dt = datetime.strptime(time_str, '%I:%M %p')
                    time_24 = dt.strftime('%H:%M')
                else:
                    time_24 = time_str
            except:
                time_24 = time_str
            
            media_filename = row.get('asset_filename', '').strip()
            
            # Buscar en meta_import
            lookup_key = (date_str, time_24, media_filename)
            if lookup_key in meta_lookup:
                meta_row = meta_lookup[lookup_key]
                # Enriquecer con caption y hashtags de meta_import
                if 'Caption' in meta_row:
                    enriched_row['Caption'] = meta_row['Caption']
                if 'Hashtags' in meta_row:
                    enriched_row['Hashtags'] = meta_row['Hashtags']
                # También asegurar que el asset_filename coincida (por si acaso)
                if 'Media URL' in meta_row:
                    enriched_row['asset_filename'] = meta_row['Media URL']
        
        if publisher and publish_fn:
            # Publicación real usando la fila enriquecida
            try:
                result = publish_fn(enriched_row, publisher)
                results.append(result)
                if result.success:
                    published_count += 1
            except Exception as e:
                result = type('MetaResponse', (), {
                    'success': False,
                    'error': str(e),
                    'post_id': None,
                    'status': 'error',
                    'raw_response': {}
                })()
                results.append(result)
        else:
            # Simulación: solo marcar como publicado localmente
            results.append(type('MetaResponse', (), {
                'success': True,
                'post_id': f"mock_{slot_id}_{now.replace(':', '-').replace('T', '_')}",
                'status': 'scheduled',
                'error': None,
                'raw_response': {'id': f"mock_{slot_id}", 'status': 'scheduled'}
            })())
            published_count += 1

        # Actualizar fila con el resultado
        # Prioridad: post_id de Meta > publication_id existente > fallback
        meta_post_id = None
        if results and results[-1].post_id:
            meta_post_id = results[-1].post_id
        
        enriched_row["status"] = "published"
        enriched_row["published_at"] = now
        if meta_post_id:
            enriched_row["publication_id"] = meta_post_id
        elif not enriched_row.get("publication_id"):
            # Fallback solo si NO hay post_id de Meta
            enriched_row["publication_id"] = f"pub_{now.replace(':', '-').replace('T', '_')}_{published_count}"
        
        # Actualizar la fila original en all_rows para el guardado final
        for key in ["status", "published_at", "publication_id"]:
            if key in enriched_row:
                row[key] = enriched_row[key]

    # 4. Guardar CSV actualizado
    _write_publications(csv_path, all_rows)

    return {
        "success": True,
        "published_count": published_count,
        "blocked": False,
        "audit": audit_result,
        "error": None,
        "results": results,
        "skipped_count": skipped_count
    }


# Backwards compatibility: keep old function signatures
def run_publication_workflow(csv_path: Path) -> Dict[str, Any]:
    """Compatibilidad con growth.workflow.run_publication_workflow()."""
    from growth.audit import validate_publications_csv
    audit_result = validate_publications_csv(csv_path)

    ready = (
        audit_result.get("success", False)
        and audit_result.get("missing", 0) == 0
        and audit_result.get("ambiguous", 0) == 0
    )

    return {
        "success": audit_result.get("success", False),
        "audit": {
            "total": audit_result.get("total", 0),
            "missing": audit_result.get("missing", 0),
            "ambiguous": audit_result.get("ambiguous", 0),
            "problematic_rows": audit_result.get("problematic_rows", []),
        },
        "ready_for_publication": ready,
        "error": audit_result.get("error"),
    }


def publish_pending(csv_path: Path) -> Dict[str, Any]:
    """Compatibilidad con growth.publisher.publish_pending()."""
    return validate_and_publish(csv_path)


def get_pending_count(csv_path: Path) -> int:
    """Compatibilidad con growth.publisher.get_pending_count()."""
    return len(pending_publications(csv_path))
