"""
Publicador con gate de auditoría integrado.

Este módulo implementa la publicación automática condicionada al resultado
de `run_publication_workflow()`. Solo publica si `ready_for_publication == True`.
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import csv
from datetime import datetime

from growth.publication_tracker import (
    load_publications,
    pending_publications,
    REQUIRED_COLUMNS,
)
from growth.workflow import run_publication_workflow


def _write_publications(csv_path: Path, rows: List[Dict[str, str]]) -> None:
    """Escribe todas las filas al CSV manteniendo el orden de columnas."""
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def publish_pending(csv_path: Path) -> Dict[str, Any]:
    """
    Publica las publicaciones pendientes si pasan el gate de auditoría.

    Flujo:
    1. Ejecuta run_publication_workflow() como gate
    2. Si ready_for_publication == True: actualiza status a "published"
    3. Si ready_for_publication == False: bloquea y devuelve resultado de auditoría

    Args:
        csv_path: Ruta al publication_log.csv

    Returns:
        Diccionario con:
            - success: bool — True si se publicó algo, False si se bloqueó
            - published_count: int — Número de filas publicadas (0 si bloqueado)
            - blocked: bool — True si la publicación fue bloqueada por el gate
            - audit: dict — Resultado completo de la auditoría
            - error: str | None — Error si success=False por razón distinta al gate
    """
    # 1. Gate de auditoría ANTES de cualquier publicación
    workflow_result = run_publication_workflow(csv_path)

    # Si la auditoría falló (CSV inexistente, malformado, etc.)
    if not workflow_result["success"]:
        return {
            "success": False,
            "published_count": 0,
            "blocked": True,
            "audit": workflow_result["audit"],
            "error": workflow_result["error"],
        }

    # 2. Verificar gate: ready_for_publication
    if not workflow_result["ready_for_publication"]:
        return {
            "success": False,
            "published_count": 0,
            "blocked": True,
            "audit": workflow_result["audit"],
            "error": "Gate de auditoría: hay assets MISSING o AMBIGUOUS",
        }

    # 3. GATE PASÓ: ready_for_publication == True → publicar
    # Cargar todas las filas
    all_rows = load_publications(csv_path)
    published_count = 0
    now = datetime.now().isoformat(timespec="seconds")

    for row in all_rows:
        if row.get("status", "").strip().lower() == "pending":
            row["status"] = "published"
            row["published_at"] = now
            # Generar publication_id si no existe
            if not row.get("publication_id"):
                row["publication_id"] = f"pub_{now.replace(':', '-').replace('T', '_')}_{published_count}"
            published_count += 1

    # Guardar CSV actualizado
    _write_publications(csv_path, all_rows)

    return {
        "success": True,
        "published_count": published_count,
        "blocked": False,
        "audit": workflow_result["audit"],
        "error": None,
    }


def get_pending_count(csv_path: Path) -> int:
    """Devuelve cuántas publicaciones están pendientes."""
    return len(pending_publications(csv_path))
