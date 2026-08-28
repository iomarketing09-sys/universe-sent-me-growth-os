"""CSV import/export adapter for GrowthOS.

Ensures semantic compatibility with existing CSV files:
- Import reads CSV and creates model instances
- Export writes CSV with same column structure
- Round-trip preserves critical fields (IDs, states, canon, dates)
"""

import csv
import io
from pathlib import Path
from typing import List, Type, TypeVar, Dict, Any

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

    # Mapping of model type to CSV column order
    COLUMN_ORDER = {
        Piece: [
            "id", "titulo", "personaje_principal", "personajes_secundarios",
            "tipo_contenido", "plataforma", "objetivo", "hipotesis",
            "estado", "prioridad", "dificultad_produccion", "reutilizable",
            "fecha_ultima_publicacion", "fuente", "formato", "categoria",
            "bloqueado_canon", "estado_operacion_normalizado",
            "estado_canon_normalizado", "asset_ref_confirmado",
            "asset_ref_candidato", "reconciliacion_estado",
            "reconciliacion_confianza", "reconciliacion_fuente",
            "reconciliacion_nota", "registro_relacionado",
            "drive_reference_id", "meta_publication_id", "meta_permalink",
            "asset_set", "asset_ref", "asset_filename", "drive_id",
            "estado_canon", "estado_produccion", "estado_publicacion",
            "ultima_sincronizacion", "motivo_revision_normalizado",
            "personaje_principal_normalizado",
            "personajes_secundarios_normalizados", "rol_narrativo",
            "tipo_humor_normalizado", "potencial_etiquetado",
            "confianza_taxonomia", "fuente_taxonomia", "nota_taxonomia",
        ],
        Publication: [
            "id_pieza", "publicacion_id", "fecha_publicacion",
            "hora_publicacion", "plataforma", "meta_post_id",
            "meta_permalink", "estado", "asset_filename", "caption",
            "hashtags", "error_message", "creado_en", "actualizado_en",
        ],
        Experiment: [
            "experiment_id", "hipotesis_id", "id_pieza", "publicacion_id",
            "fecha_publicacion", "plataforma", "formato", "personaje",
            "slot_horario", "vistas", "retencion_pct", "interacciones",
            "interacciones_24h", "interacciones_72h", "shares",
            "comentarios", "reactions", "estado_canon", "veredicto",
            "conclusion", "observaciones",
        ],
        CommunityEngagement: [
            "comentario_id", "post_id", "cnt_id", "tipo", "autor",
            "texto", "fecha_comentario", "respuesta_estado",
            "respuesta_texto", "fecha_respuesta", "accion_calendario",
            "prioridad", "ventana_revision",
        ],
        MetricsSnapshot: [
            "snapshot_id", "meta_post_id", "publication_id",
            "target_at_utc", "captured_at_utc", "window_type",
            "reactions", "comments", "shares", "views", "reach",
            "retention_pct", "validation_status", "raw_response",
            "error_message",
        ],
        AssetAlias: [
            "alias_id", "asset_ref", "asset_filename", "drive_id",
            "meta_post_id", "meta_permalink", "fecha_publicacion",
            "hora_publicacion", "sha256", "cnt_creation_allowed",
            "confidence", "proposed_record_type", "canon_impact",
            "status", "evidence_path", "notes",
        ],
    }

    @classmethod
    def import_csv(cls, model: Type[T], path: Path) -> List[T]:
        """Import CSV file into list of model instances.

        Handles the actual CSV format with 'ID_Pieza' as first column.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")

        rows: List[T] = []
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []

            for row in reader:
                # Skip empty rows
                if not any(v and v.strip() for v in row.values()):
                    continue

                # Convert CSV column names to field names
                # CSV has 'ID_Pieza' but model has 'ID_Pieza' (same)
                # Just pass through; Pydantic handles extra fields
                try:
                    instance = model(**row)
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
            if model_type and model_type in cls.COLUMN_ORDER:
                with path.open("w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(cls.COLUMN_ORDER[model_type])
            return

        # Use model's field order from first instance
        first = models[0]
        fieldnames = list(first.model_dump().keys())

        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for model in models:
                row = model.model_dump()
                # Convert dates to ISO strings
                for key, value in row.items():
                    if hasattr(value, "isoformat"):
                        row[key] = value.isoformat()
                    elif value is None:
                        row[key] = ""
                writer.writerow(row)

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

        result = {
            "match": True,
            "original_rows": 0,
            "exported_rows": 0,
            "id_mismatch": [],
            "field_mismatches": {},
            "errors": [],
        }

        def read(path: Path) -> List[Dict[str, str]]:
            with path.open(encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                return [dict(r) for r in reader]

        try:
            orig_rows = read(original)
            exp_rows = read(exported)
        except Exception as e:
            result["match"] = False
            result["errors"].append(str(e))
            return result

        result["original_rows"] = len(orig_rows)
        result["exported_rows"] = len(exp_rows)

        if len(orig_rows) != len(exp_rows):
            result["match"] = False
            result["errors"].append(
                f"Row count mismatch: {len(orig_rows)} vs {len(exp_rows)}"
            )
            return result

        # Critical fields to compare
        critical_fields = [
            "ID_Pieza",
            "Titulo",
            "Tipo_Contenido",
            "Personaje_Principal",
            "Plataforma",
            "Estado",
            "Bloqueado_Canon",
            "Fecha_Ultima_Publicacion",
            "Estado_Canon",
            "Estado_Produccion",
            "Estado_Publicacion",
        ]

        for i, (orig, exp) in enumerate(zip(orig_rows, exp_rows)):
            # Check ID
            if orig.get("ID_Pieza") != exp.get("ID_Pieza"):
                result["match"] = False
                result["id_mismatch"].append(
                    (orig.get("ID_Pieza"), exp.get("ID_Pieza"))
                )

            # Check critical fields
            for field in critical_fields:
                ov = (orig.get(field) or "").strip()
                ev = (exp.get(field) or "").strip()
                if ov != ev:
                    result["match"] = False
                    if field not in result["field_mismatches"]:
                        result["field_mismatches"][field] = []
                    result["field_mismatches"][field].append(
                        {"row": i, "original": ov, "exported": ev}
                    )

        return result
