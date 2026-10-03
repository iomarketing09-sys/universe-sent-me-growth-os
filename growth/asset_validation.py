"""
Validación unificada de assets.

Consolida la lógica de:
- asset_resolver.py (resolver contra manifest)
- asset_validator.py (validar existencia en disco)
- audit.py (auditoría completa)

Proporciona una única función clara:
    validate_asset(asset_filename, tenant_id) -> (status, path, asset_ref, reason)
"""
import os
import json
import csv
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


def load_manifest(tenant_id: str = "firma-bordados") -> Dict[str, Any]:
    """Carga el manifest del tenant."""
    manifest_path = Path(__file__).resolve().parents[1] / "tenants" / tenant_id / "assets_manifest.json"
    with manifest_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_asset_in_manifest(
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


def get_tenant_assets_root(tenant_id: str = "firma-bordados") -> Path:
    """Obtiene la ruta raíz de assets del tenant."""
    # For firma-bordados, assets are in Google Drive mount
    if tenant_id == "firma-bordados":
        return Path("/home/universe-sent-me/GoogleDrive/01 - Firma Assets")
    
    # Fallback to local tenant assets folder
    return (
        Path(__file__).resolve().parents[1]
        / "tenants"
        / tenant_id
        / "assets"
        / tenant_id.replace("-", " ").title()
    )


def find_asset_on_disk(asset_filename: str, tenant_id: str = "firma-bordados") -> List[Path]:
    """
    Busca un archivo recursivamente en el directorio de assets del tenant.
    
    Excluye la carpeta 'Publicaciones Agosto' (ya programadas).
    """
    if not asset_filename or not asset_filename.strip():
        return []
    
    assets_root = get_tenant_assets_root(tenant_id)
    excluded_dir = assets_root / "Publicaciones Agosto"
    
    matches = []
    for root, dirs, files in os.walk(assets_root):
        # Skip excluded directory
        if excluded_dir in Path(root).resolve().parents:
            continue
        if asset_filename in files:
            matches.append(Path(root) / asset_filename)
    
    return matches


def validate_asset(
    asset_filename: str,
    tenant_id: str = "firma-bordados"
) -> Dict[str, Any]:
    """
    Valida un asset completo: manifest + disco.
    
    Returns:
        Dict con:
            - status: "MATCH" | "MISSING" | "AMBIGUOUS"
            - asset_ref: str o None
            - source_filename: str o None
            - source_file_key: str o None
            - path: Path o None (ruta absoluta si MATCH)
            - confidence: str o None
            - reason: str explicando el resultado
    """
    # 1. Buscar en manifest
    manifest = load_manifest(tenant_id)
    manifest_matches = find_asset_in_manifest(asset_filename, manifest)
    
    if not manifest_matches:
        return {
            "status": "MISSING",
            "asset_ref": None,
            "source_filename": None,
            "source_file_key": None,
            "path": None,
            "confidence": None,
            "reason": f"No existe en assets_manifest.json: {asset_filename}"
        }
    
    if len(manifest_matches) > 1:
        refs = [m.get("asset_ref") for m in manifest_matches]
        return {
            "status": "AMBIGUOUS",
            "asset_ref": None,
            "source_filename": None,
            "source_file_key": None,
            "path": None,
            "confidence": None,
            "reason": f"Múltiples coincidencias en manifest: {refs}"
        }
    
    # Exactly one match in manifest
    asset = manifest_matches[0]
    canonical_filename = asset.get("source_filename") or asset.get("source_file_key")
    
    # 2. Validar existencia en disco
    disk_matches = find_asset_on_disk(canonical_filename, tenant_id)
    
    if not disk_matches:
        return {
            "status": "MISSING",
            "asset_ref": asset.get("asset_ref"),
            "source_filename": asset.get("source_filename"),
            "source_file_key": asset.get("source_file_key"),
            "path": None,
            "confidence": asset.get("confidence"),
            "reason": f"Asset en manifest pero no encontrado en disco: {canonical_filename}"
        }
    
    if len(disk_matches) > 1:
        paths = [str(p) for p in disk_matches]
        return {
            "status": "AMBIGUOUS",
            "asset_ref": asset.get("asset_ref"),
            "source_filename": asset.get("source_filename"),
            "source_file_key": asset.get("source_file_key"),
            "path": None,
            "confidence": asset.get("confidence"),
            "reason": f"Múltiples archivos en disco: {paths}"
        }
    
    # MATCH: one in manifest, one on disk
    return {
        "status": "MATCH",
        "asset_ref": asset.get("asset_ref"),
        "source_filename": asset.get("source_filename"),
        "source_file_key": asset.get("source_file_key"),
        "path": disk_matches[0].resolve(),
        "confidence": asset.get("confidence"),
        "reason": f"Coincidencia completa: {canonical_filename}"
    }


def audit_publications(
    csv_path: Path,
    tenant_id: str = "firma-bordados"
) -> Dict[str, Any]:
    """
    Ejecuta auditoría completa de un CSV de publicaciones.
    
    Compatible con el formato de publication_log.csv y meta_import.csv.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")
    
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    
    total = len(rows)
    missing = 0
    ambiguous = 0
    problematic_rows = []
    
    for idx, row in enumerate(rows, start=1):
        asset_filename = (row.get("asset_filename") or row.get("Media URL") or "").strip()
        
        if not asset_filename:
            # TEXT_ONLY posts are valid without asset
            continue
        
        result = validate_asset(asset_filename, tenant_id)
        status = result["status"]
        
        if status == "MISSING":
            missing += 1
            problematic_rows.append({
                "row_number": idx,
                "asset_filename": asset_filename,
                "status": "MISSING",
                "detail": result["reason"]
            })
        elif status == "AMBIGUOUS":
            ambiguous += 1
            problematic_rows.append({
                "row_number": idx,
                "asset_filename": asset_filename,
                "status": "AMBIGUOUS",
                "detail": result["reason"]
            })
    
    return {
        "success": True,
        "total": total,
        "missing": missing,
        "ambiguous": ambiguous,
        "problematic_rows": problematic_rows,
        "ready_for_publication": missing == 0 and ambiguous == 0
    }


# Backwards compatibility functions
def validate_csv(csv_path: Path) -> List[Dict[str, str]]:
    """Compatibilidad con asset_validator.validate_csv()."""
    if not csv_path.exists():
        return []
    
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    
    for row in rows:
        asset_filename = (row.get("asset_filename") or "").strip()
        result = validate_asset(asset_filename, "firma-bordados")
        
        row["status"] = result["status"]
        row["asset_path"] = str(result["path"]) if result["path"] else ""
        row["ambiguous_paths"] = ""
        if result["status"] == "AMBIGUOUS":
            row["ambiguous_paths"] = result["reason"]
    
    return rows


def find_asset(name: str) -> Tuple[str, List[Path]]:
    """Compatibilidad con asset_validator.find_asset()."""
    result = validate_asset(name, "firma-bordados")
    return result["status"], [result["path"]] if result["path"] else []


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3 asset_validation.py <asset_filename> [tenant_id]")
        sys.exit(1)
    
    asset_filename = sys.argv[1]
    tenant_id = sys.argv[2] if len(sys.argv) > 2 else "firma-bordados"
    
    result = validate_asset(asset_filename, tenant_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
