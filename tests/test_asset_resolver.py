"""
Tests para growth/asset_resolver.py
"""
from pathlib import Path
import tempfile
import json

from growth.asset_resolver import load_manifest, find_matching_assets, resolve_asset


def _create_test_manifest(tmp_path):
    """Crea un manifest de prueba temporal."""
    manifest = {
        "version": "1.0",
        "generated_from": ["test"],
        "assets": [
            {
                "asset_ref": "video_20_anos",
                "calendar_references": ["20 años bordando"],
                "source_file_key": "VID-20260821-WA0002.mp4",
                "source_filename": "VID-20260821-WA0002.mp4",
                "source_path": None,
                "description": "Video institucional",
                "evidence_source": "asset_inventory.csv",
                "confidence": "DETERMINISTIC"
            },
            {
                "asset_ref": "soul_blues_catalog",
                "calendar_references": ["Catálogo Soul & Blues"],
                "source_file_key": "SOUL&BLUES 2025.pdf",
                "source_filename": "SOUL&BLUES 2025.pdf",
                "source_path": "Catalogos/",
                "description": "Catálogo",
                "evidence_source": "Catalogos/",
                "confidence": "DETERMINISTIC"
            },
            {
                "asset_ref": "uniforme_corporativo",
                "calendar_references": ["uniforme corporativo"],
                "source_file_key": "",
                "source_filename": "",
                "source_path": None,
                "description": "Sin evidencia física",
                "evidence_source": "Manus/...",
                "confidence": "INSUFFICIENT_EVIDENCE"
            },
            {
                "asset_ref": "otro_video_distinto",
                "calendar_references": ["video extra"],
                "source_file_key": "OTRO-VIDEO.mp4",
                "source_filename": "OTRO-VIDEO.mp4",
                "source_path": None,
                "description": "Otro video con archivo distinto",
                "evidence_source": "test",
                "confidence": "DETERMINISTIC"
            }
        ]
    }
    manifest_path = tmp_path / "assets_manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f)
    return manifest_path


def _patch_manifest_path(monkeypatch, manifest_path):
    """Parchea MANIFEST_PATH en el módulo."""
    import growth.asset_resolver as ar
    monkeypatch.setattr(ar, "MANIFEST_PATH", manifest_path)


def test_resolve_match_by_source_filename(monkeypatch, tmp_path):
    """1. MATCH por source_filename exacto."""
    manifest_path = _create_test_manifest(tmp_path)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    row = {"asset_filename": "VID-20260821-WA0002.mp4", "piece": "Video 20 años"}
    result = resolve_asset(row)
    
    assert result["status"] == "MATCH"
    assert result["asset_ref"] == "video_20_anos"
    assert result["source_filename"] == "VID-20260821-WA0002.mp4"
    assert result["source_file_key"] == "VID-20260821-WA0002.mp4"
    assert result["confidence"] == "DETERMINISTIC"


def test_resolve_match_by_source_file_key(monkeypatch, tmp_path):
    """2. MATCH por source_file_key exacto si aplica."""
    manifest_path = _create_test_manifest(tmp_path)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    row = {"asset_filename": "SOUL&BLUES 2025.pdf", "piece": "Catálogo"}
    result = resolve_asset(row)
    
    assert result["status"] == "MATCH"
    assert result["asset_ref"] == "soul_blues_catalog"


def test_resolve_missing_not_in_manifest(monkeypatch, tmp_path):
    """3. MISSING cuando no existe en manifest."""
    manifest_path = _create_test_manifest(tmp_path)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    row = {"asset_filename": "archivo_inexistente.jpg", "piece": "Test"}
    result = resolve_asset(row)
    
    assert result["status"] == "MISSING"
    assert result["asset_ref"] is None
    assert "No existe relación explícita" in result["reason"]


def test_resolve_missing_insufficient_evidence(monkeypatch, tmp_path):
    """4. MISSING cuando el manifest tiene INSUFFICIENT_EVIDENCE."""
    manifest_path = _create_test_manifest(tmp_path)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    # uniforme_corporativo es INSUFFICIENT_EVIDENCE con source_filename vacío
    row = {"asset_filename": "", "piece": "Uniforme corporativo"}
    result = resolve_asset(row)
    
    assert result["status"] == "MISSING"
    assert result["asset_ref"] is None


def test_resolve_ambiguous_multiple_deterministic(monkeypatch, tmp_path):
    """5. AMBIGUOUS cuando existen múltiples matches válidos."""
    # Crear manifest con duplicados
    manifest = {
        "version": "1.0",
        "generated_from": ["test"],
        "assets": [
            {
                "asset_ref": "video_a",
                "calendar_references": ["video a"],
                "source_file_key": "DUPLICADO.mp4",
                "source_filename": "DUPLICADO.mp4",
                "source_path": None,
                "description": "Video A",
                "evidence_source": "test",
                "confidence": "DETERMINISTIC"
            },
            {
                "asset_ref": "video_b",
                "calendar_references": ["video b"],
                "source_file_key": "DUPLICADO.mp4",
                "source_filename": "DUPLICADO.mp4",
                "source_path": None,
                "description": "Video B",
                "evidence_source": "test",
                "confidence": "DETERMINISTIC"
            }
        ]
    }
    manifest_path = tmp_path / "ambiguous_manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    row = {"asset_filename": "DUPLICADO.mp4", "piece": "Video"}
    result = resolve_asset(row)
    
    assert result["status"] == "AMBIGUOUS"
    assert result["asset_ref"] is None
    assert "Múltiples coincidencias" in result["reason"]


def test_resolve_empty_manifest(monkeypatch, tmp_path):
    """6. Manifest vacío."""
    manifest = {"version": "1.0", "generated_from": [], "assets": []}
    manifest_path = tmp_path / "empty_manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    row = {"asset_filename": "cualquier_cosa.jpg", "piece": "Test"}
    result = resolve_asset(row)
    
    assert result["status"] == "MISSING"


def test_resolve_invalid_manifest(monkeypatch, tmp_path):
    """7. Manifest inválido (malformed JSON)."""
    manifest_path = tmp_path / "bad_manifest.json"
    manifest_path.write_text("{ invalid json }")
    _patch_manifest_path(monkeypatch, manifest_path)
    
    row = {"asset_filename": "test.jpg", "piece": "Test"}
    try:
        resolve_asset(row)
        assert False, "Debería haber lanzado excepción"
    except json.JSONDecodeError:
        pass  # Esperado


def test_resolve_row_without_asset_filename(monkeypatch, tmp_path):
    """8. Publication row sin asset_filename."""
    manifest_path = _create_test_manifest(tmp_path)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    row = {"asset_filename": "", "piece": "Solo piece"}
    result = resolve_asset(row)
    
    assert result["status"] == "MISSING"


def test_no_fuzzy_matching(monkeypatch, tmp_path):
    """9. No fuzzy matching - solo coincidencia exacta."""
    manifest_path = _create_test_manifest(tmp_path)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    # "VID-20260821-WA0002.mp4" vs "VID-20260821-WA0002" (sin .mp4)
    row = {"asset_filename": "VID-20260821-WA0002", "piece": "Test"}
    result = resolve_asset(row)
    
    assert result["status"] == "MISSING", "No debe hacer fuzzy matching"


def test_original_data_not_modified(monkeypatch, tmp_path):
    """10. No modificar datos originales."""
    manifest_path = _create_test_manifest(tmp_path)
    _patch_manifest_path(monkeypatch, manifest_path)
    
    original_row = {"asset_filename": "VID-20260821-WA0002.mp4", "piece": "Video 20 años"}
    row_copy = dict(original_row)
    
    resolve_asset(original_row)
    
    # Verificar que la fila original no fue modificada
    assert original_row == row_copy


def test_load_manifest_success():
    """Test que load_manifest carga el manifest real."""
    manifest = load_manifest()
    assert "version" in manifest
    assert "assets" in manifest
    assert isinstance(manifest["assets"], list)
