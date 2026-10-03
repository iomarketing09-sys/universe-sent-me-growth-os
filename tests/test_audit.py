"""
Test end-to-end para el módulo audit.py
"""
from pathlib import Path
import tempfile
import csv

from growth.audit import run_audit, validate_publications_csv


def test_run_audit_with_valid_csv(tmp_path):
    """Test run_audit with a CSV that has known assets."""
    # Crear estructura de archivos de prueba
    asset_root = tmp_path / "Firma_Bordados - Drive" / "Firma Bordados "
    asset_root.mkdir(parents=True)

    # Crear algunos archivos de prueba
    (asset_root / "test_video.mp4").write_text("dummy")
    (asset_root / "test_image.jpg").write_text("dummy")
    (asset_root / "dup.jpg").write_text("a")
    (asset_root / "sub").mkdir(parents=True, exist_ok=True)
    (asset_root / "sub" / "dup.jpg").write_text("b")

    # Crear CSV de prueba
    csv_path = tmp_path / "test_inventory.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "time", "platform", "piece", "calendar_reference", "asset_filename", "status", "notes"])
        writer.writerow(["2026-08-31", "08:30", "Facebook", "Video test", "ref1", "test_video.mp4", "pending", ""])
        writer.writerow(["2026-08-31", "09:00", "Instagram", "Foto test", "ref2", "test_image.jpg", "pending", ""])
        writer.writerow(["2026-08-31", "10:00", "Facebook", "Missing", "ref3", "nonexistent.png", "pending", ""])
        writer.writerow(["2026-08-31", "11:00", "Instagram", "Ambiguous", "ref4", "dup.jpg", "pending", ""])
        writer.writerow(["2026-08-31", "12:00", "Facebook", "Empty", "ref5", "", "pending", ""])
        writer.writerow(["2026-08-31", "13:00", "Instagram", "Dash", "ref6", "–", "pending", ""])

    # Parchear ASSET_ROOT y EXCLUDED_DIR en asset_validator
    import growth.asset_validator as av
    original_asset_root = av.ASSET_ROOT
    original_excluded_dir = av.EXCLUDED_DIR
    av.ASSET_ROOT = asset_root
    av.EXCLUDED_DIR = asset_root / "Publicaciones Agosto"

    try:
        result = run_audit(csv_path)

        assert result["total"] == 6
        assert result["missing"] == 3  # nonexistent.png, empty, dash
        assert result["ambiguous"] == 1  # dup.jpg
        assert len(result["problematic_rows"]) == 4

        # Verificar detalles de filas problemáticas
        statuses = {r["asset_filename"]: r["status"] for r in result["problematic_rows"]}
        assert statuses["nonexistent.png"] == "MISSING"
        assert statuses[""] == "MISSING"
        assert statuses["–"] == "MISSING"
        assert statuses["dup.jpg"] == "AMBIGUOUS"
    finally:
        av.ASSET_ROOT = original_asset_root
        av.EXCLUDED_DIR = original_excluded_dir


def test_run_audit_nonexistent_csv(tmp_path):
    """Test run_audit raises FileNotFoundError for missing CSV."""
    csv_path = tmp_path / "no_existe.csv"
    try:
        run_audit(csv_path)
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        assert "no_existe.csv" in str(e)


def test_validate_publications_csv_success(tmp_path):
    """Test validate_publications_csv returns success dict."""
    asset_root = tmp_path / "Firma_Bordados - Drive" / "Firma Bordados "
    asset_root.mkdir(parents=True)
    (asset_root / "ok.jpg").write_text("dummy")

    csv_path = tmp_path / "test.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "time", "platform", "piece", "calendar_reference", "asset_filename", "status", "notes"])
        writer.writerow(["2026-08-31", "08:30", "Facebook", "Test", "ref1", "ok.jpg", "pending", ""])

    import growth.asset_validator as av
    original_asset_root = av.ASSET_ROOT
    original_excluded_dir = av.EXCLUDED_DIR
    av.ASSET_ROOT = asset_root
    av.EXCLUDED_DIR = asset_root / "Publicaciones Agosto"

    try:
        result = validate_publications_csv(csv_path)
        assert result["success"] is True
        assert result["error"] is None
        assert result["total"] == 1
        assert result["missing"] == 0
        assert result["ambiguous"] == 0
    finally:
        av.ASSET_ROOT = original_asset_root
        av.EXCLUDED_DIR = original_excluded_dir


def test_validate_publications_csv_not_found(tmp_path):
    """Test validate_publications_csv handles missing file gracefully."""
    csv_path = tmp_path / "missing.csv"
    result = validate_publications_csv(csv_path)
    assert result["success"] is False
    assert "CSV no encontrado" in result["error"]
    assert result["total"] == 0
