"""
Resolver de assets: conecta filas de publication_log con assets_manifest.json

Este módulo NO modifica el comportamiento de auditoría existente.
Solo responde: "¿Qué asset pretende representar esta fila según el manifest?"
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import json


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "growth" / "assets_manifest.json"


def load_manifest() -> Dict[str, Any]:
    """Carga el manifest desde disco."""
    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_matching_assets(
    asset_filename: str,
    manifest: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Busca assets en el manifest que coincidan exactamente con asset_filename.
    
    Coincidencia exacta contra:
    - source_filename
    - source_file_key
    
    Solo considera assets con confidence = DETERMINISTIC.
    """
    if not asset_filename or not asset_filename.strip():
        return []
    
    target = asset_filename.strip()
    matches = []
    
    for asset in manifest.get("assets", []):
        if asset.get("confidence") != "DETERMINISTIC":
            continue
        
        # Coincidencia exacta contra source_filename
        if asset.get("source_filename", "").strip() == target:
            matches.append(asset)
            continue
        
        # Coincidencia exacta contra source_file_key
        if asset.get("source_file_key", "").strip() == target:
            matches.append(asset)
            continue
    
    return matches


def resolve_asset(
    publication_row: Dict[str, str],
    manifest: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Resuelve una fila de publication_log contra el manifest.
    
    Args:
        publication_row: Dict con al menos 'asset_filename' y opcionalmente 'piece'
        manifest: Manifest ya cargado (opcional, se carga si no se proporciona)
    
    Returns:
        Dict con:
            - status: "MATCH" | "MISSING" | "AMBIGUOUS"
            - asset_ref: str o None
            - source_filename: str o None
            - source_file_key: str o None
            - confidence: str o None
            - reason: str explicando el resultado
    """
    if manifest is None:
        manifest = load_manifest()
    
    asset_filename = publication_row.get("asset_filename", "")
    piece = publication_row.get("piece", "")
    
    # Buscar coincidencias exactas
    matches = find_matching_assets(asset_filename, manifest)
    
    if len(matches) == 1:
        asset = matches[0]
        return {
            "status": "MATCH",
            "asset_ref": asset.get("asset_ref"),
            "source_filename": asset.get("source_filename"),
            "source_file_key": asset.get("source_file_key"),
            "confidence": asset.get("confidence"),
            "reason": f"Coincidencia exacta: {asset.get('source_filename')} (source_file_key: {asset.get('source_file_key')})"
        }
    
    if len(matches) > 1:
        refs = [m.get("asset_ref") for m in matches]
        return {
            "status": "AMBIGUOUS",
            "asset_ref": None,
            "source_filename": None,
            "source_file_key": None,
            "confidence": None,
            "reason": f"Múltiples coincidencias DETERMINISTIC: {refs}"
        }
    
    # Sin coincidencias
    return {
        "status": "MISSING",
        "asset_ref": None,
        "source_filename": None,
        "source_file_key": None,
        "confidence": None,
        "reason": "No existe relación explícita en assets_manifest para este asset_filename"
    }
