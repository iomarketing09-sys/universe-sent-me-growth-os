"""Golden test for CSV round-trip: Import → SQLite → Export preserves semantic equivalence."""

import csv
import tempfile
from pathlib import Path

import pytest

from growthos.core.models import Piece
from growthos.storage.csv_adapter import CSVAdapter
from growthos.storage.database import Database
from growthos.storage.repositories import PieceRepository


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
    """Test round-trip with the actual Content_Inventory.csv."""
    import os

    inventory_path = Path("GrowthOS/Content_Inventory.csv")
    if not inventory_path.exists():
        pytest.skip("Content_Inventory.csv not found")

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(db_path=db_path)
        db.init_schema()

        repo = PieceRepository(db)

        # Import
        pieces = CSVAdapter.import_csv(Piece, inventory_path)
        assert len(pieces) > 0, "Should import at least one piece"

        # Save to SQLite
        for piece in pieces:
            repo.save(piece)

        # Export
        export_path = Path(tmpdir) / "exported_inventory.csv"
        all_pieces = repo.get_all()
        CSVAdapter.export_piece_csv(all_pieces, export_path)

        # Compare
        result = CSVAdapter.compare_semantic(inventory_path, export_path)

        # Debug output
        print(f"Original rows: {result['original_rows']}")
        print(f"Exported rows: {result['exported_rows']}")
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

        # Semantic match required
        assert result["match"], f"Semantic mismatch: {result}"
        db.close()


def test_csv_roundtrip_preserves_critical_fields():
    """Test that critical fields are preserved in round-trip."""
    # Create a minimal CSV with known values
    test_data = [
        {
            "ID_Pieza": "CNT-001",
            "Titulo": "Test Piece",
            "Personaje_Principal": "@char_USM_universe",
            "Personajes_Secundarios": "",
            "Tipo_Contenido": "Reel",
            "Plataforma": "Facebook",
            "Objetivo": "Test",
            "Hipotesis": "HB-001",
            "Estado": "Aprobado",
            "Prioridad": "Alta",
            "Dificultad_Produccion": "Baja",
            "Reutilizable": "Sí",
            "Fecha_Ultima_Publicacion": "2026-07-01",
            "Fuente": "test.md",
            "Formato": "9:16",
            "Categoria": "Humor",
            "Bloqueado_Canon": "No",
            "Estado_Operacion_Normalizado": "Aprobado",
            "Estado_Canon_Normalizado": "Canon_Clear_or_Unverified",
            "Asset_Ref_Confirmado": "260001",
            "Asset_Ref_Candidato": "",
            "Reconciliacion_Estado": "Resolved_Production_Set",
            "Reconciliacion_Confianza": "High",
            "Reconciliacion_Fuente": "test",
            "Reconciliacion_Nota": "",
            "Registro_Relacionado": "",
            "Drive_Reference_ID": "",
            "Meta_Publication_ID": "",
            "Meta_Permalink": "",
            "Asset_Set": "",
            "Asset_Ref": "260001",
            "Asset_Filename": "test.mp4",
            "Drive_ID": "drive123",
            "Estado_Canon": "Aprobado",
            "Estado_Produccion": "Asset_Listo",
            "Estado_Publicacion": "No_Publicada",
            "Ultima_Sincronizacion": "2026-08-15",
            "Motivo_Revision_Normalizado": "",
            "Personaje_Principal_Normalizado": "Universe",
            "Personajes_Secundarios_Normalizados": "Ninguno",
            "Rol_Narrativo": "Protagonista",
            "Tipo_Humor_Normalizado": "Fandom o referencia",
            "Potencial_Etiquetado": "Medio",
            "Confianza_Taxonomia": "Alta",
            "Fuente_Taxonomia": "Inventario + reglas taxonómicas",
            "Nota_Taxonomia": "",
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.csv"
        output_path = Path(tmpdir) / "output.csv"
        db_path = Path(tmpdir) / "test.db"

        # Write input CSV
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
        "ID_Pieza": "CNT-001",
        "Titulo": "",
        "Personaje_Principal": "",
        "Personajes_Secundarios": "",
        "Tipo_Contenido": "",
        "Plataforma": "",
        "Objetivo": "",
        "Hipotesis": "",
        "Estado": "Idea",
        "Prioridad": "",
        "Dificultad_Produccion": "",
        "Reutilizable": "",
        "Fecha_Ultima_Publicacion": "",
        "Fuente": "",
        "Formato": "",
        "Categoria": "",
        "Bloqueado_Canon": "",
        "Estado_Operacion_Normalizado": "",
        "Estado_Canon_Normalizado": "",
        "Asset_Ref_Confirmado": "",
        "Asset_Ref_Candidato": "",
        "Reconciliacion_Estado": "",
        "Reconciliacion_Confianza": "",
        "Reconciliacion_Fuente": "",
        "Reconciliacion_Nota": "",
        "Registro_Relacionado": "",
        "Drive_Reference_ID": "",
        "Meta_Publication_ID": "",
        "Meta_Permalink": "",
        "Asset_Set": "",
        "Asset_Ref": "",
        "Asset_Filename": "",
        "Drive_ID": "",
        "Estado_Canon": "",
        "Estado_Produccion": "",
        "Estado_Publicacion": "",
        "Ultima_Sincronizacion": "",
        "Motivo_Revision_Normalizado": "",
        "Personaje_Principal_Normalizado": "",
        "Personajes_Secundarios_Normalizados": "",
        "Rol_Narrativo": "",
        "Tipo_Humor_Normalizado": "",
        "Potencial_Etiquetado": "",
        "Confianza_Taxonomia": "",
        "Fuente_Taxonomia": "",
        "Nota_Taxonomia": "",
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
        assert pieces[0].Estado.name == "IDEA"  # Enum value

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
        {"ID_Pieza": "CNT-001", "Estado": "Idea", "Titulo": "Test 1"},
        {"ID_Pieza": "CNT-002", "Estado": "Idea", "Titulo": "Test 2"},
        {"ID_Pieza": "CNT-001", "Estado": "Idea", "Titulo": "Test 1 Duplicate"},
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
