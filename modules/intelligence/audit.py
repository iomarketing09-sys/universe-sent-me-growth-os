"""
Auditoría de activos de Growth OS.

Este módulo proporciona la función run_audit() que valida un CSV de publicaciones
contra los archivos reales en el directorio de activos, usando
asset_validator para compatibilidad con tests existentes.

La nueva validación unificada está en growth.asset_validation para el nuevo código.
"""
from pathlib import Path
from typing import Dict, List, Any
import csv

from growth.asset_validator import validate_csv, find_asset


def run_audit(csv_path: Path) -> Dict[str, Any]:
    """
    Ejecuta una auditoría completa del CSV de publicaciones.

    Args:
        csv_path: Ruta al archivo CSV con columnas:
            date, time, platform, piece, asset_filename, status, ...

    Returns:
        Diccionario con:
            - total: total de filas procesadas
            - missing: cantidad de filas con status MISSING
            - ambiguous: cantidad de filas con status AMBIGUOUS
            - problematic_rows: lista de dicts con filas MISSING/AMBIGUOUS
                (incluye row_number, asset_filename, status, detalles)

    Raises:
        FileNotFoundError: Si el CSV no existe.
        ValueError: Si el CSV está malformado o tiene columnas inválidas.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")

    # Usar asset_validator para compatibilidad con tests
    validated_rows = validate_csv(csv_path)

    # Contar resultados
    total = len(validated_rows)
    missing = 0
    ambiguous = 0
    problematic_rows = []

    for idx, row in enumerate(validated_rows, start=1):
        status = row.get("status", "")
        asset_filename = row.get("asset_filename", "")

        if status == "MISSING":
            missing += 1
            problematic_rows.append({
                "row_number": idx,
                "asset_filename": asset_filename,
                "status": "MISSING",
                "detail": "Archivo no encontrado en el directorio de activos"
            })
        elif status == "AMBIGUOUS":
            ambiguous += 1
            paths = row.get("ambiguous_paths", "")
            problematic_rows.append({
                "row_number": idx,
                "asset_filename": asset_filename,
                "status": "AMBIGUOUS",
                "detail": f"Múltiples coincidencias: {paths}"
            })

    return {
        "total": total,
        "missing": missing,
        "ambiguous": ambiguous,
        "problematic_rows": problematic_rows,
        "ready_for_publication": missing == 0 and ambiguous == 0
    }


def validate_publications_csv(csv_path: Path) -> Dict[str, Any]:
    """
    Función de conveniencia para validate_publications.py.
    Wrapper que maneja errores y devuelve resultado estructurado.
    """
    try:
        result = run_audit(csv_path)
        result["success"] = True
        result["error"] = None
        return result
    except FileNotFoundError as e:
        return {
            "success": False,
            "error": str(e),
            "total": 0,
            "missing": 0,
            "ambiguous": 0,
            "problematic_rows": [],
            "ready_for_publication": False
        }
    except (ValueError, csv.Error) as e:
        return {
            "success": False,
            "error": f"CSV malformado: {e}",
            "total": 0,
            "missing": 0,
            "ambiguous": 0,
            "problematic_rows": [],
            "ready_for_publication": False
        }
