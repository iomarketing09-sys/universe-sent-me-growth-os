"""Golden test for CSV round-trip: Import → SQLite → Export preserves semantic equivalence."""

import csv
import tempfile
from pathlib import Path

import pytest

from growthos.core.models import Piece
from growthos.storage.csv_adapter import CSVAdapter
from growthos.storage.database import Database
from growthos.storage.repositories import PieceRepository
from growthos.core.enums import (
    EstadoPieza,
    Plataforma,
    TipoContenido,
    Categoria,
    Prioridad,
    DificultadProduccion,
    Reutilizable,
    BloqueadoCanon,
    EstadoCanon,
    EstadoProduccion,
    EstadoPublicacion,
    MotivoRevision,
    ReconciliacionEstado,
    ReconciliacionConfianza,
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(db_path=db_path)
        db.init_schema()
        yield db
        db.close()


def test_csv_roundtrip_with_real_inventory():
    """Test round-trip with the actual Content_Inventory.csv.
    
    Note: The real inventory contains 85 rows but only ~5 have fully valid enum values.
    The rest have "Category C" values requiring human decision (not auto-normalized).
    This test verifies that the pieces which CAN be imported round-trip correctly.
    """
    inventory_path = Path("GrowthOS/Content_Inventory.csv")
    if not inventory_path.exists():
        pytest.skip("Content_Inventory.csv not found")

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(db_path=db_path)
        db.init_schema()

        repo = PieceRepository(db)

        # Import - only rows with valid enum values will be imported
        pieces = CSVAdapter.import_csv(Piece, inventory_path)
        assert len(pieces) > 0, "Should import at least one piece with valid enums"
        imported_ids = [p.ID_Pieza for p in pieces]

        # Save to SQLite
        for piece in pieces:
            repo.save(piece)

        # Export
        export_path = Path(tmpdir) / "exported_inventory.csv"
        all_pieces = repo.get_all()
        CSVAdapter.export_piece_csv(all_pieces, export_path)

        # Compare - filter original CSV to only include imported IDs
        # Read original CSV
        with inventory_path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            orig_rows = [r for r in reader if r.get("id") in imported_ids]
        
        # Write filtered original to temp file for comparison
        filtered_orig_path = Path(tmpdir) / "filtered_original.csv"
        if orig_rows:
            with filtered_orig_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=orig_rows[0].keys())
                writer.writeheader()
                writer.writerows(orig_rows)

        # Apply the same normalizations that happen during import to the original rows
        # so that comparison is fair
        from growthos.storage.csv_adapter import apply_normalizations
        normalized_orig_rows = []
        for row in orig_rows:
            csv_id = row.get("id") or row.get("ID_Pieza") or ""
            norm_row = apply_normalizations(row, csv_id)
            normalized_orig_rows.append(norm_row)
        
        normalized_orig_path = Path(tmpdir) / "normalized_original.csv"
        if normalized_orig_rows:
            with normalized_orig_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=normalized_orig_rows[0].keys())
                writer.writeheader()
                writer.writerows(normalized_orig_rows)

        result = CSVAdapter.compare_semantic(normalized_orig_path, export_path)

        # Debug output
        print(f"Normalized original rows: {result['original_rows']}")
        print(f"Exported rows: {result['exported_rows']}")
        print(f"Imported IDs: {imported_ids}")
        print(f"Match: {result['match']}")

        if result["id_mismatch"]:
            print(f"ID mismatches: {result['id_mismatch']}")
        if result["field_mismatches"]:
            for field, mismatches in result["field_mismatches"].items():
                print(f"  {field}: {len(mismatches)} mismatches")
                for m in mismatches[:3]:
                    print(f"    Row {m['row']}: '{m['original']}' vs '{m['exported']}'")
        if result["errors"]:
            for err in result["errors"]:
                print(f"  Error: {err}")

        # The exported file should contain exactly the imported pieces in the same order
        assert result["exported_rows"] == len(imported_ids)
        assert result["match"], f"Semantic mismatch for imported pieces: {result}"
        db.close()


def test_csv_roundtrip_preserves_critical_fields():
    """Test that critical fields are preserved in round-trip."""
    # Create a minimal CSV with known values (using CSV column names, not model field names)
    test_data = [
        {
            "id": "CNT-001",
            "titulo": "Test Piece",
            "personaje_principal": "@char_USM_universe",
            "personajes_secundarios": "",
            "tipo_contenido": "Reel",
            "plataforma": "Facebook",
            "objetivo": "Test",
            "hipotesis": "HB-001",  # CSV column name
            "estado": "Aprobado",
            "prioridad": "Alta",
            "dificultad_produccion": "Baja",
            "reutilizable": "Sí",
            "fecha_ultima_publicacion": "2026-07-01",
            "fuente": "test.md",
            "formato": "9:16",
            "categoria": "Humor",
            "bloqueado_canon": "No",
            "estado_operacion_normalizado": "Asset_Listo",
            "estado_canon_normalizado": "Canon_Clear_or_Unverified",
            "asset_ref_confirmado": "260001",
            "asset_ref_candidato": "",
            "reconciliacion_estado": "Resolved_Production_Set",
            "reconciliacion_confianza": "High",
            "reconciliacion_fuente": "test",
            "reconciliacion_nota": "",
            "registro_relacionado": "",
            "drive_reference_id": "",
            "meta_publication_id": "",
            "meta_permalink": "",
            "asset_set": "",
            "Asset_Ref": "260001",
            "Asset_Filename": "test.mp4",
            "Drive_ID": "drive123",
            "Estado_Canon": "Aprobado",
            "Estado_Produccion": "Asset_Listo",
            "Estado_Publicacion": "No_Publicada",
            "Ultima_Sincronizacion": "2026-08-15",
            "Motivo_Revision_Normalizado": "",
            "personaje_principal_normalizado": "Universe",
            "personajes_secundarios_normalizados": "Ninguno",
            "rol_narrativo": "Protagonista",
            "tipo_humor_normalizado": "Fandom o referencia",
            "potencial_etiquetado": "Medio",
            "confianza_taxonomia": "Alta",
            "fuente_taxonomia": "Inventario + reglas taxonómicas",
            "nota_taxonomia": "",
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.csv"
        output_path = Path(tmpdir) / "output.csv"
        db_path = Path(tmpdir) / "test.db"

        # Write input CSV using CSV column names
        with input_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=test_data[0].keys())
            writer.writeheader()
            writer.writerows(test_data)

        # Round-trip through SQLite
        db = Database(db_path=db_path)
        db.init_schema()
        repo = PieceRepository(db)

        pieces = CSVAdapter.import_csv(Piece, input_path)
        for piece in pieces:
            repo.save(piece)

        all_pieces = repo.get_all()
        CSVAdapter.export_piece_csv(all_pieces, output_path)

        # Compare
        result = CSVAdapter.compare_semantic(input_path, output_path)

        assert result["match"], f"Critical fields not preserved: {result}"
        db.close()


def test_csv_import_handles_empty_values():
    """Test that empty values in CSV are handled correctly."""
    test_data = {
        "id": "CNT-001",
        "titulo": "",
        "personaje_principal": "",
        "personajes_secundarios": "",
        "tipo_contenido": "",
        "plataforma": "",
        "objetivo": "",
        "hipotesis": "",
        "estado": "Idea",
        "prioridad": "",
        "dificultad_produccion": "",
        "reutilizable": "",
        "fecha_ultima_publicacion": "",
        "fuente": "",
        "formato": "",
        "categoria": "",
        "bloqueado_canon": "",
        "estado_operacion_normalizado": "",
        "estado_canon_normalizado": "",
        "asset_ref_confirmado": "",
        "asset_ref_candidato": "",
        "reconciliacion_estado": "",
        "reconciliacion_confianza": "",
        "reconciliacion_fuente": "",
        "reconciliacion_nota": "",
        "registro_relacionado": "",
        "drive_reference_id": "",
        "meta_publication_id": "",
        "meta_permalink": "",
        "asset_set": "",
        "Asset_Ref": "",
        "Asset_Filename": "",
        "Drive_ID": "",
        "Estado_Canon": "",
        "Estado_Produccion": "",
        "Estado_Publicacion": "",
        "Ultima_Sincronizacion": "",
        "Motivo_Revision_Normalizado": "",
        "personaje_principal_normalizado": "",
        "personajes_secundarios_normalizados": "",
        "rol_narrativo": "",
        "tipo_humor_normalizado": "",
        "potencial_etiquetado": "",
        "confianza_taxonomia": "",
        "fuente_taxonomia": "",
        "nota_taxonomia": "",
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.csv"
        output_path = Path(tmpdir) / "output.csv"
        db_path = Path(tmpdir) / "test.db"

        with input_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=test_data.keys())
            writer.writeheader()
            writer.writerow(test_data)

        db = Database(db_path=db_path)
        db.init_schema()
        repo = PieceRepository(db)

        pieces = CSVAdapter.import_csv(Piece, input_path)
        assert len(pieces) == 1
        assert pieces[0].ID_Pieza == "CNT-001"
        assert pieces[0].Estado == EstadoPieza.IDEA  # Enum value

        for piece in pieces:
            repo.save(piece)

        all_pieces = repo.get_all()
        CSVAdapter.export_piece_csv(all_pieces, output_path)

        # Compare - should match semantically (empty strings)
        result = CSVAdapter.compare_semantic(input_path, output_path)
        assert result["match"], f"Empty values not preserved: {result}"
        db.close()


def test_csv_duplicate_ids_detected():
    """Test that duplicate CNT IDs are detected."""
    test_data = [
        {"id": "CNT-001", "estado": "Idea", "titulo": "Test 1"},
        {"id": "CNT-002", "estado": "Idea", "titulo": "Test 2"},
        {"id": "CNT-001", "estado": "Idea", "titulo": "Test 1 Duplicate"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.csv"
        db_path = Path(tmpdir) / "test.db"

        with input_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=test_data[0].keys())
            writer.writeheader()
            writer.writerows(test_data)

        pieces = CSVAdapter.import_csv(Piece, input_path)
        dupes = [p.ID_Pieza for p in pieces]
        assert dupes.count("CNT-001") == 2  # Both imported (validation happens later)

        # Validator should detect
        from growthos.core.validators import validate_unique_ids
        dupes_found = validate_unique_ids(pieces)
        assert "CNT-001" in dupes_found
