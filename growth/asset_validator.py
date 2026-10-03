"""
Compatibilidad hacia atrás: asset_validator mantiene implementación original para tests.

Este módulo mantiene la interfaz original para no romper tests existentes.
Los tests parchean ASSET_ROOT y EXCLUDED_DIR, por lo que usamos la implementación original aquí.
La nueva validación unificada está en growth.asset_validation.
"""
from pathlib import Path
from typing import Dict, List, Tuple
import csv

# Configuración global para tests (parcheada por tests)
ASSET_ROOT = (
    Path(__file__).resolve().parents[1]
    / "tenants"
    / "firma-bordados"
    / "assets"
    / "Firma Bordados "
)

CSV_PATH = Path(__file__).resolve().parents[1] / "publication_log.csv"

EXCLUDED_DIR = ASSET_ROOT / "Publicaciones Agosto"


def _canonical_path(path: Path) -> Path:
    """Return a canonical absolute path."""
    return path.resolve()


def _find_in_root(name: str) -> List[Path]:
    """Search recursively for an exact filename under ASSET_ROOT."""
    return [p for p in ASSET_ROOT.rglob(name) if p.is_file()]


def _exclude_folder(paths: List[Path]) -> List[Path]:
    """Exclude assets located inside the already-published folder."""
    excluded = EXCLUDED_DIR.resolve()

    result = []
    for path in paths:
        resolved = path.resolve()
        try:
            resolved.relative_to(excluded)
        except ValueError:
            result.append(path)

    return result


def find_asset(name: str) -> Tuple[str, List[Path]]:
    """
    Find an exact filename under ASSET_ROOT.

    Empty filenames are MISSING.
    Files inside Publicaciones Agosto are ignored.
    """
    if not name or not name.strip() or name.strip() in {"–", "-"}:
        return "MISSING", []

    matches = _find_in_root(name.strip())
    matches = _exclude_folder(matches)

    if not matches:
        return "MISSING", []

    if len(matches) > 1:
        return "AMBIGUOUS", matches

    return "MATCH", matches


def validate_row(row: Dict[str, str]) -> Dict[str, str]:
    """Validate one publication row without modifying its original fields."""
    asset_name = (row.get("asset_filename") or "").strip()
    status, matches = find_asset(asset_name)

    row["status"] = status
    row["asset_path"] = ""
    row["ambiguous_paths"] = ""

    if status == "MATCH":
        row["asset_path"] = str(_canonical_path(matches[0]))

    elif status == "AMBIGUOUS":
        row["ambiguous_paths"] = " | ".join(
            str(_canonical_path(path)) for path in matches
        )

    return row


def validate_csv(csv_path: Path = CSV_PATH) -> List[Dict[str, str]]:
    """Read and validate every row in the publication CSV."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    for row in rows:
        validate_row(row)

    return rows
