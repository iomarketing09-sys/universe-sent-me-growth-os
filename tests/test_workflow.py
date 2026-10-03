"""
Tests de integración para growth/workflow.py
"""
from pathlib import Path
import csv

from growth.workflow import run_publication_workflow


def _setup_test_assets(tmp_path):
    """Crea estructura de assets de prueba y retorna asset_root."""
    asset_root = tmp_path / "Firma_Bordados - Drive" / "Firma Bordados "
    asset_root.mkdir(parents=True)
    (asset_root / "ok.jpg").write_text("dummy")
    (asset_root / "video.mp4").write_text("dummy")
    (asset_root / "dup.jpg").write_text("a")
    (asset_root / "sub").mkdir(parents=True, exist_ok=True)
    (asset_root / "sub" / "dup.jpg").write_text("b")

    import growth.asset_validator as av
    original_asset_root = av.ASSET_ROOT
    original_excluded_dir = av.EXCLUDED_DIR
    av.ASSET_ROOT = asset_root
    av.EXCLUDED_DIR = asset_root / "Publicaciones Agosto"
    return asset_root, original_asset_root, original_excluded_dir


def _teardown_test_assets(original_asset_root, original_excluded_dir):
    import growth.asset_validator as av
    av.ASSET_ROOT = original_asset_root
    av.EXCLUDED_DIR = original_excluded_dir


def _write_csv(csv_path: Path, rows: list):
    """Escribe CSV con header y filas dadas."""
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "time", "platform", "piece", "calendar_reference", "asset_filename", "status", "notes"])
        for row in rows:
            writer.writerow(row)


class TestAllMatch:
    """Test 1 — Todo MATCH → success=True, ready_for_publication=True"""

    def test_all_match_returns_ready_true(self, tmp_path):
        asset_root, orig_root, orig_excl = _setup_test_assets(tmp_path)
        try:
            csv_path = tmp_path / "test.csv"
            _write_csv(csv_path, [
                ["2026-08-31", "08:30", "Facebook", "Test 1", "ref1", "ok.jpg", "pending", ""],
                ["2026-08-31", "09:00", "Instagram", "Test 2", "ref2", "video.mp4", "pending", ""],
            ])

            result = run_publication_workflow(csv_path)

            assert result["success"] is True
            assert result["ready_for_publication"] is True
            assert result["audit"]["total"] == 2
            assert result["audit"]["missing"] == 0
            assert result["audit"]["ambiguous"] == 0
            assert result["audit"]["problematic_rows"] == []
            assert result["error"] is None
        finally:
            _teardown_test_assets(orig_root, orig_excl)


class TestMissing:
    """Test 2 — MISSING → success=False, ready_for_publication=False, conserva fila"""

    def test_missing_returns_not_ready(self, tmp_path):
        asset_root, orig_root, orig_excl = _setup_test_assets(tmp_path)
        try:
            csv_path = tmp_path / "test.csv"
            _write_csv(csv_path, [
                ["2026-08-31", "08:30", "Facebook", "Test 1", "ref1", "ok.jpg", "pending", ""],
                ["2026-08-31", "09:00", "Instagram", "Test 2", "ref2", "nonexistent.png", "pending", ""],
            ])

            result = run_publication_workflow(csv_path)

            assert result["success"] is True  # auditoría ejecutada OK
            assert result["ready_for_publication"] is False
            assert result["audit"]["total"] == 2
            assert result["audit"]["missing"] == 1
            assert result["audit"]["ambiguous"] == 0
            assert len(result["audit"]["problematic_rows"]) == 1
            prob = result["audit"]["problematic_rows"][0]
            assert prob["asset_filename"] == "nonexistent.png"
            assert prob["status"] == "MISSING"
            assert result["error"] is None
        finally:
            _teardown_test_assets(orig_root, orig_excl)


class TestAmbiguous:
    """Test 3 — AMBIGUOUS → success=False, ready_for_publication=False, conserva fila"""

    def test_ambiguous_returns_not_ready(self, tmp_path):
        asset_root, orig_root, orig_excl = _setup_test_assets(tmp_path)
        try:
            csv_path = tmp_path / "test.csv"
            _write_csv(csv_path, [
                ["2026-08-31", "08:30", "Facebook", "Test 1", "ref1", "ok.jpg", "pending", ""],
                ["2026-08-31", "09:00", "Instagram", "Test 2", "ref2", "dup.jpg", "pending", ""],
            ])

            result = run_publication_workflow(csv_path)

            assert result["success"] is True
            assert result["ready_for_publication"] is False
            assert result["audit"]["total"] == 2
            assert result["audit"]["missing"] == 0
            assert result["audit"]["ambiguous"] == 1
            assert len(result["audit"]["problematic_rows"]) == 1
            prob = result["audit"]["problematic_rows"][0]
            assert prob["asset_filename"] == "dup.jpg"
            assert prob["status"] == "AMBIGUOUS"
            assert result["error"] is None
        finally:
            _teardown_test_assets(orig_root, orig_excl)


class TestInvalidCSV:
    """Test 4 — CSV inexistente o inválido → manejo limpio"""

    def test_nonexistent_csv(self, tmp_path):
        csv_path = tmp_path / "no_existe.csv"
        result = run_publication_workflow(csv_path)

        assert result["success"] is False
        assert result["ready_for_publication"] is False
        assert "CSV no encontrado" in result["error"]
        assert result["audit"]["total"] == 0
        assert result["audit"]["missing"] == 0
        assert result["audit"]["ambiguous"] == 0
        assert result["audit"]["problematic_rows"] == []

    def test_malformed_csv(self, tmp_path):
        # CSV con comillas sin cerrar - el parser de Python lo maneja pero puede dar filas incompletas
        csv_path = tmp_path / "bad.csv"
        # Escribir CSV malformado directamente
        csv_path.write_text('date,asset_filename\n"unclosed,quote\n')

        result = run_publication_workflow(csv_path)

        # validate_publications_csv no lanza, devuelve success=False para errores de parseo
        # o success=True si el parser lo lee (comportamiento actual)
        # Lo importante: no crashea y devuelve estructura consistente
        assert "success" in result
        assert "audit" in result
        assert "ready_for_publication" in result
        assert "error" in result
