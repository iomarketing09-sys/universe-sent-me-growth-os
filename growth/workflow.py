"""
Capa de integración de Growth OS para el flujo de publicación.

Este módulo expone `run_publication_workflow()` que orquesta la auditoría
de activos y produce un resultado estructurado para consumo por capas superiores
de Growth OS.
"""
from pathlib import Path
from typing import Dict, Any

from growth.audit import run_audit, validate_publications_csv


def run_publication_workflow(csv_path: Path) -> Dict[str, Any]:
    """
    Ejecuta el flujo completo de validación de publicaciones para Growth OS.

    Args:
        csv_path: Ruta al CSV de publicaciones (formato publication_log.csv
                  o asset_inventory.csv).

    Returns:
        Diccionario estructurado con:
            - success: bool — True si la auditoría se ejecutó sin errores de I/O/parseo
            - audit: dict — Resultado completo de run_audit() o validate_publications_csv()
                          (total, missing, ambiguous, problematic_rows)
            - ready_for_publication: bool — True solo si missing=0 Y ambiguous=0
            - error: str | None — Mensaje de error si success=False
    """
    # Usar validate_publications_csv que ya maneja errores de forma estructurada
    audit_result = validate_publications_csv(csv_path)

    # ready_for_publication: solo MATCH (sin MISSING ni AMBIGUOUS)
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
