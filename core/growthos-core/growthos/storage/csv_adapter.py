"""CSV import/export adapter for GrowthOS.

Ensures semantic compatibility with existing CSV files:
- Import reads CSV and creates model instances
- Export writes CSV with same column structure
- Round-trip preserves critical fields (IDs, states, canon, dates)
"""

import csv
import io
import re
from pathlib import Path
from typing import List, Type, TypeVar, Dict, Any, Optional
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel

from growthos.core.models import (
    Piece,
    Publication,
    Experiment,
    CommunityEngagement,
    MetricsSnapshot,
    AssetAlias,
)

T = TypeVar("T", bound=BaseModel)


class CSVAdapter:
    """Adapter for reading/writing CSV files with Pydantic models."""

    # CSV column name to model field name mapping for Piece
    # Uses normalized state columns (not free-text "estado")
    PIECE_FIELD_MAP = {
        "id": "id_pieza",
        "titulo": "titulo",
        "personaje_principal": "personaje_principal",
        "personajes_secundarios": "personajes_secundarios",
        "tipo_contenido": "tipo_contenido",
        "plataforma": "plataforma_principal",
        "objetivo": "objetivo",
        "hipotesis": "hipotesis_id",
        # Don't map free-text "estado" - use normalized columns instead
        "estado_operacion_normalizado": "estado_operacion_normalizado",
        "prioridad": "prioridad",
        "dificultad_produccion": "dificultad_produccion",
        "reutilizable": "es_reutilizable",
        "fecha_ultima_publicacion": "fecha_ultima_publicacion",
        "fuente": "fuente",
        "formato": "formato",
        "categoria": "categoria_tematica",
        "bloqueado_canon": "bloqueado_canon",
        "estado_canon_normalizado": "estado_canon_normalizado",
        "asset_ref_confirmado": "asset_ref_confirmado",
        "asset_ref_candidato": "asset_ref_candidato",
        "reconciliacion_estado": "reconciliacion_estado",
        "reconciliacion_confianza": "reconciliacion_confianza",
        "reconciliacion_fuente": "reconciliacion_fuente",
        "reconciliacion_nota": "reconciliacion_nota",
        "registro_relacionado": "registro_relacionado",
        "drive_reference_id": "drive_reference_id",
        "meta_publication_id": "meta_publication_id",
        "meta_permalink": "meta_permalink",
        "asset_set": "asset_set",
        "Asset_Ref": "asset_ref",
        "Asset_Filename": "asset_filename",
        "Drive_ID": "drive_id",
        "Estado_Canon": "estado_canon",
        "Estado_Produccion": "estado_produccion",
        "Estado_Publicacion": "estado_publicacion",
        "Ultima_Sincronizacion": "ultima_sincronizacion",
        "Motivo_Revision_Normalizado": "motivo_revision_normalizado",
        "personaje_principal_normalizado": "personaje_principal_normalizado",
        "personajes_secundarios_normalizados": "personajes_secundarios_normalizados",
        "rol_narrativo": "rol_narrativo",
        "tipo_humor_normalizado": "tipo_humor_normalizado",
        "potencial_etiquetado": "potencial_etiquetado",
        "confianza_taxonomia": "confianza_taxonomia",
        "fuente_taxonomia": "fuente_taxonomia",
        "nota_taxonomia": "nota_taxonomia",
    }

    # Reverse mapping for export
    PIECE_FIELD_MAP_REVERSE = {v: k for k, v in PIECE_FIELD_MAP.items()}

    # Column order for CANONICAL CSV (46 columns expected by tests)
    # Matches PIECE_FIELD_MAP keys but with lowercase for consistency with CANONICAL
    COLUMN_ORDER = {
        Piece: list(PIECE_FIELD_MAP.keys()),
    }

    # CSV column to model field mapping for Piece (alias for tests)
    CSV_TO_PIECE = PIECE_FIELD_MAP_REVERSE.copy()

    # Publication field mapping
    PUBLICATION_FIELD_MAP = {
        "id_pieza": "id_pieza",
        "publicacion_id": "publicacion_id",
        "fecha_publicacion": "fecha_publicacion",
        "hora_publicacion": "hora_publicacion",
        "plataforma": "plataforma",
        "meta_post_id": "meta_post_id",
        "meta_permalink": "meta_permalink",
        "estado": "estado",
        "asset_filename": "asset_filename",
        "caption": "caption",
        "hashtags": "hashtags",
        "error_message": "error_message",
        "creado_en": "creado_en",
        "actualizado_en": "actualizado_en",
    }

    # Experiment field mapping
    EXPERIMENT_FIELD_MAP = {
        "experiment_id": "experiment_id",
        "hipotesis_id": "hipotesis_id",
        "id_pieza": "id_pieza",
        "publicacion_id": "publicacion_id",
        "fecha_publicacion": "fecha_publicacion",
        "plataforma": "plataforma",
        "formato": "formato",
        "personaje": "personaje",
        "slot_horario": "slot_horario",
        "vistas": "vistas",
        "retencion_pct": "retencion_pct",
        "interacciones": "interacciones",
        "interacciones_24h": "interacciones_24h",
        "interacciones_72h": "interacciones_72h",
        "shares": "shares",
        "comentarios": "comentarios",
        "reactions": "reactions",
        "estado_canon": "estado_canon",
        "veredicto": "veredicto",
        "conclusion": "conclusion",
        "observaciones": "observaciones",
    }

    @classmethod
    def _map_csv_to_model(cls, row: Dict[str, str], field_map: Dict[str, str]) -> Dict[str, Any]:
        """Map CSV column names to model field names."""
        mapped = {}
        for csv_key, value in row.items():
            model_key = field_map.get(csv_key)
            if model_key:
                mapped[model_key] = value
            else:
                # Keep unmapped fields as-is (they might be extra fields)
                mapped[csv_key] = value
        return mapped

    @classmethod
    def _parse_date(cls, value: str) -> Optional[date]:
        """Parse date from various string formats."""
        if not value or value.strip() == "":
            return None
        
        value = value.strip()
        
        # Skip non-date strings
        if value.lower() in ("no publicado", "sin fecha", "pendiente", "n/a", "na"):
            return None
        if "histórico" in value.lower() or "viral" in value.lower():
            return None
        
        # Try standard date formats
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        
        # Try to extract date from strings like "2026-07-29 (generado, no publicado)"
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', value)
        if date_match:
            try:
                return datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
            except ValueError:
                pass
        
        # Try datetime formats (with timezone)
        for fmt in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        
        return None

    @classmethod
    def _parse_datetime(cls, value: str) -> Optional[datetime]:
        """Parse datetime from various string formats."""
        if not value or value.strip() == "":
            return None
        
        value = value.strip()
        
        # Try datetime formats (with timezone)
        for fmt in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        
        # Try date only
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        
        return None

    @classmethod
    def _clean_row(cls, row: Dict[str, str], model: Type[T]) -> Dict[str, Any]:
        """Clean row data: convert empty strings to None, parse dates, handle enums."""
        cleaned = {}
        
        # Get model field info
        model_fields = model.model_fields
        
        for key, value in row.items():
            # Skip empty strings for optional fields
            if value == "" or value is None:
                cleaned[key] = None
                continue
            
            # Try to get field info for type hints
            field_info = model_fields.get(key)
            if field_info is not None:
                annotation = field_info.annotation

                # Unwrap Optional[T] and Union[T, None] so dates and enums are
                # handled even when the field is nullable.
                args = getattr(annotation, "__args__", ())
                candidates = tuple(arg for arg in args if arg is not type(None))
                if not candidates:
                    candidates = (annotation,)

                enum_type = next(
                    (
                        arg for arg in candidates
                        if isinstance(arg, type) and issubclass(arg, Enum)
                    ),
                    None,
                )
                if enum_type is not None:
                    try:
                        cleaned[key] = enum_type(value)
                    except ValueError:
                        cleaned[key] = None
                    continue

                if date in candidates and isinstance(value, str):
                    cleaned[key] = cls._parse_date(value)
                    continue

                if datetime in candidates and isinstance(value, str):
                    cleaned[key] = cls._parse_datetime(value)
                    continue
            
            cleaned[key] = value
        
        return cleaned

    @classmethod
    def import_csv(cls, model: Type[T], path: Path) -> List[T]:
        """Import CSV file into list of model instances."""
        path = Path(path)
        if not path.exists():
            return []

        # Determine field mapping based on model
        field_map = {}
        if model == Piece:
            field_map = cls.PIECE_FIELD_MAP
        elif model == Publication:
            field_map = cls.PUBLICATION_FIELD_MAP
        elif model == Experiment:
            field_map = cls.EXPERIMENT_FIELD_MAP

        rows: List[T] = []
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []

            for row in reader:
                # Skip empty rows
                if not any(v and v.strip() for v in row.values()):
                    continue

                try:
                    # Map CSV column names to model field names
                    mapped_row = cls._map_csv_to_model(row, field_map)
                    
                    # Clean the row before passing to model
                    cleaned_row = cls._clean_row(mapped_row, model)
                    instance = model(**cleaned_row)
                    rows.append(instance)
                except Exception as e:
                    # Log but continue - some rows may have data issues
                    print(f"Warning: skipped row in {path.name}: {e}")
                    continue

        return rows

    @classmethod
    def export_csv(cls, models: List[T], path: Path, model_type: Type[T] = None) -> None:
        """Export list of model instances to CSV.

        Preserves column order from CSV standard.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not models:
            # Write header only
            if model_type == Piece:
                with path.open("w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(list(cls.PIECE_FIELD_MAP.keys()))
            return

        # Use model's field order from first instance
        first = models[0]
        fieldnames = list(first.model_dump().keys())

        # Map model field names back to CSV column names
        if model_type == Piece:
            csv_fieldnames = [cls.PIECE_FIELD_MAP_REVERSE.get(f, f) for f in fieldnames]
        else:
            csv_fieldnames = fieldnames

        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=csv_fieldnames, extrasaction="ignore")
            writer.writeheader()
            for model in models:
                row = model.model_dump()
                # Map model field names to CSV column names
                if model_type == Piece:
                    csv_row = {cls.PIECE_FIELD_MAP_REVERSE.get(k, k): v for k, v in row.items()}
                else:
                    csv_row = row
                for key, value in csv_row.items():
                    if hasattr(value, "isoformat"):
                        csv_row[key] = value.isoformat()
                    elif value is None:
                        csv_row[key] = ""
                writer.writerow(csv_row)

    @classmethod
    def export_piece_csv(cls, pieces: List[Piece], path: Path) -> None:
        """Export pieces preserving the Content_Inventory.csv column order."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not pieces:
            return

        # Use the field names from the first piece, but preserve order
        fieldnames = list(pieces[0].model_dump().keys())

        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for piece in pieces:
                row = piece.model_dump()
                for key, value in row.items():
                    if hasattr(value, "isoformat"):
                        row[key] = value.isoformat()
                    elif value is None:
                        row[key] = ""
                writer.writerow(row)

    @classmethod
    def compare_semantic(
        cls, original_path: Path, exported_path: Path
    ) -> Dict[str, Any]:
        """
        Compare two CSV files for semantic equivalence.

        Checks:
        - Same number of rows
        - Same ID_Pieza values in same order
        - Critical fields match: ID_Pieza, estado, canon, plataforma, fechas

        Returns dict with 'match' boolean and details.
        """
        original = Path(original_path)
        exported = Path(exported_path)

        def clean_value(value: Any) -> Any:
            if value is None:
                return ""
            if isinstance(value, Enum):
                return value.value
            if hasattr(value, "isoformat"):
                return value.isoformat()
            return value

        def load_rows(path: Path) -> List[Dict[str, Any]]:
            if not path.exists():
                return []

            with path.open(encoding="utf-8-sig", newline="") as f:
                raw_rows = list(csv.DictReader(f))

            normalized = []
            for raw in raw_rows:
                if not any(
                    isinstance(value, str) and value.strip()
                    for value in raw.values()
                ):
                    continue
                mapped = cls._map_csv_to_model(raw, cls.PIECE_FIELD_MAP)
                cleaned = cls._clean_row(mapped, Piece)
                normalized.append({
                    key: clean_value(value)
                    for key, value in cleaned.items()
                })
            return normalized

        original_rows = load_rows(original)
        exported_rows = load_rows(exported)

        result = {
            "match": True,
            "original_rows": len(original_rows),
            "exported_rows": len(exported_rows),
            "id_mismatch": [],
            "field_mismatches": {},
            "errors": [],
        }

        if result["original_rows"] != result["exported_rows"]:
            result["match"] = False
            result["errors"].append(
                "Row count mismatch: "
                f"{result['original_rows']} original vs "
                f"{result['exported_rows']} exported"
            )

        for row_number, (original_row, exported_row) in enumerate(
            zip(original_rows, exported_rows), start=1
        ):
            original_id = original_row.get("id_pieza", "")
            exported_id = exported_row.get("id_pieza", "")
            if original_id != exported_id:
                result["id_mismatch"].append({
                    "row": row_number,
                    "original": original_id,
                    "exported": exported_id,
                })
                continue

            common_fields = set(original_row) & set(exported_row)
            for field in sorted(common_fields):
                if field == "id_pieza":
                    continue
                original_value = original_row.get(field, "")
                exported_value = exported_row.get(field, "")
                if original_value != exported_value:
                    result["field_mismatches"].setdefault(field, []).append({
                        "row": row_number,
                        "original": original_value,
                        "exported": exported_value,
                    })

        if result["id_mismatch"] or result["field_mismatches"]:
            result["match"] = False

        return result


def apply_normalizations(row: Dict[str, str], csv_id: str = "") -> Dict[str, Any]:
    """Return a normalized Piece row without mutating the source CSV.

    The function uses the same column mapping and value cleaning as
    :meth:`CSVAdapter.import_csv`, so round-trip comparisons can normalize
    both sides consistently.
    """
    mapped = CSVAdapter._map_csv_to_model(row, CSVAdapter.PIECE_FIELD_MAP)
    cleaned = CSVAdapter._clean_row(mapped, Piece)
    if csv_id:
        cleaned["id_pieza"] = csv_id
    return cleaned


__all__ = ["CSVAdapter", "apply_normalizations"]
