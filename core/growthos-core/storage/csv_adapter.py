"""CSV adapter for GrowthOS data persistence."""

import csv
import sys
from pathlib import Path
from typing import List, Type, TypeVar, Optional, Dict, Any
from enum import Enum

# Add the project root to sys.path to allow absolute imports
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT))

T = TypeVar('T')


class CSVAdapter:
    """Handles CSV operations for GrowthOS models."""
    
    def __init__(self, csv_path: Path, enum_fields: Optional[Dict[str, Type[Enum]]] = None):
        self.csv_path = csv_path
        self.enum_fields = enum_fields or {}
    
    def read_all(self, model_type: Type[T]) -> List[T]:
        """Read all records from CSV and return as model instances."""
        if not self.csv_path.exists():
            return []
        
        records = []
        with self.csv_path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                processed_row = {}
                for key, value in row.items():
                    processed_row[key] = value  # keep empty string as empty string
                
                # Convert enum fields
                for field, enum_class in self.enum_fields.items():
                    if field in processed_row and processed_row[field] is not None:
                        value = processed_row[field]
                        if value == "":
                            processed_row[field] = None
                        else:
                            try:
                                # Try to find enum by value
                                for enum_item in enum_class:
                                    if enum_item.value == value:
                                        processed_row[field] = enum_item
                                        break
                                else:
                                    # If not found, leave as string (will cause validation error if required)
                                    pass
                            except Exception:
                                # If any error, leave as string
                                pass
                
                try:
                    record = model_type(**processed_row)
                    records.append(record)
                except Exception as e:
                    # Log error but continue processing
                    print(f"Warning: Skipping row due to error: {e}")
                    continue
        
        return records
    
    def write_all(self, model_type: Type[T], records: List[T]) -> None:
        """Write all records to CSV."""
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self.csv_path.open('w', encoding='utf-8', newline='') as f:
            if records:
                # Get fieldnames from the first record's model_dump
                fieldnames = list(records[0].model_dump().keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for record in records:
                    # Convert enum values to their string representations
                    row = record.model_dump()
                    processed_row = {}
                    for key, value in row.items():
                        if isinstance(value, Enum):
                            processed_row[key] = value.value
                        else:
                            processed_row[key] = value
                    writer.writerow(processed_row)
            else:
                # Write header only
                fieldnames = model_type.model_fields.keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()


class PieceCSVAdapter(CSVAdapter):
    """CSV adapter specifically for Piece model with predefined enum fields."""
    
    def __init__(self, csv_path: Path):
        from core.enums import (
            EstadoPieza, Plataforma, TipoContenido, Categoria, Prioridad,
            DificultadProduccion, Reutilizable, BloqueadoCanon, EstadoCanon,
            EstadoProduccion, EstadoPublicacion, MotivoRevision,
            ReconciliacionEstado, ReconciliacionConfianza,
        )
        enum_fields = {
            'Tipo_Contenido': TipoContenido,
            'Plataforma': Plataforma,
            'Estado': EstadoPieza,
            'Prioridad': Prioridad,
            'Dificultad_Produccion': DificultadProduccion,
            'Es_Reutilizable': Reutilizable,
            'Categoria': Categoria,
            'Bloqueado_Canon': BloqueadoCanon,
            'Estado_Canon': EstadoCanon,
            'Estado_Produccion': EstadoProduccion,
            'Estado_Publicacion': EstadoPublicacion,
            'Motivo_Revision_Normalizado': MotivoRevision,
            'Reconciliacion_Estado': ReconciliacionEstado,
            'Reconciliacion_Confianza': ReconciliacionConfianza,
        }
        super().__init__(csv_path, enum_fields)
