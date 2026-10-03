"""
Tests de idempotencia básica: filas con publication_id se saltan.
"""
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from growth.gate_and_publish import validate_and_publish
from growth.publication_tracker import REQUIRED_COLUMNS


def _write_csv(csv_path: Path, rows: list):
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(REQUIRED_COLUMNS)
        writer.writerows(rows)


# Nombres de archivos REALES del manifest de firma-bordados
ASSET_PHOTO = "01_lunes_detalle_uniforme.png"
ASSET_VIDEO = "VID-20260821-WA0002.mp4"


def test_idempotent_skip_published(tmp_path):
    """Test A: Slot con publication_id existente → se salta, 0 llamadas a Meta."""
    csv_path = tmp_path / "pub_log.csv"
    
    # Una fila YA publicada (tiene publication_id), una pendiente
    _write_csv(csv_path, [
        ["2026-08-31", "08:30", "Facebook", "Test 1", ASSET_PHOTO,
         "published", "POST_ID_REAL_123", "2026-08-31T08:00:00", "", "", "", ""],
        ["2026-08-31", "09:00", "Instagram", "Test 2", ASSET_VIDEO,
         "pending", "", "", "", "", "", ""],
    ])
    
    class MockPublisher:
        pass
    
    call_count = {"count": 0, "called_for": []}
    def mock_publish_fn(row, publisher):
        call_count["count"] += 1
        call_count["called_for"].append(row["piece"])
        return type('MetaResponse', (), {
            'success': True,
            'post_id': f'META_POST_{call_count["count"]}',
            'status': 'scheduled',
            'error': None,
            'raw_response': {}
        })()
    
    result = validate_and_publish(
        csv_path=csv_path,
        tenant_id="firma-bordados",
        publisher=MockPublisher(),
        publish_fn=mock_publish_fn,
    )
    
    # Solo la fila pendiente se procesó
    assert result["success"] is True, f"Expected success, got: {result}"
    assert result["published_count"] == 1, f"Expected 1 published, got {result['published_count']}"
    assert result["skipped_count"] == 1, f"Expected 1 skipped, got {result['skipped_count']}"
    assert call_count["count"] == 1, f"Expected 1 call to publish_fn, got {call_count['count']}"
    assert call_count["called_for"] == ["Test 2"], f"Expected call for Test 2 only, got {call_count['called_for']}"
    
    # Verificar CSV actualizado
    from growth.publication_tracker import load_publications
    rows = load_publications(csv_path)
    assert rows[0]["status"] == "published"
    assert rows[0]["publication_id"] == "POST_ID_REAL_123"
    assert rows[1]["status"] == "published"
    assert rows[1]["publication_id"] != ""


def test_idempotent_rerun_same_csv_no_duplicates(tmp_path):
    """Test H: Ejecutar 2 veces el mismo CSV → segunda vez 0 publicaciones nuevas."""
    csv_path = tmp_path / "pub_log.csv"
    
    # Ambas pendientes
    _write_csv(csv_path, [
        ["2026-08-31", "08:30", "Facebook", "Test 1", ASSET_PHOTO,
         "pending", "", "", "", "", "", ""],
        ["2026-08-31", "09:00", "Instagram", "Test 2", ASSET_VIDEO,
         "pending", "", "", "", "", "", ""],
    ])
    
    class MockPublisher:
        pass
    
    # Primera ejecución
    call_count = {"count": 0}
    def mock_publish_fn(row, publisher):
        call_count["count"] += 1
        return type('MetaResponse', (), {
            'success': True,
            'post_id': f'META_POST_{call_count["count"]}',
            'status': 'scheduled',
            'error': None,
            'raw_response': {}
        })()
    
    result1 = validate_and_publish(
        csv_path=csv_path,
        tenant_id="firma-bordados",
        publisher=MockPublisher(),
        publish_fn=mock_publish_fn,
    )
    assert result1["published_count"] == 2
    assert result1["skipped_count"] == 0
    assert call_count["count"] == 2
    
    # Segunda ejecución (mismo CSV, ahora con publication_ids)
    call_count["count"] = 0
    result2 = validate_and_publish(
        csv_path=csv_path,
        tenant_id="firma-bordados",
        publisher=MockPublisher(),
        publish_fn=mock_publish_fn,
    )
    
    # Segunda vez: 0 nuevos, 2 saltados
    assert result2["published_count"] == 0
    assert result2["skipped_count"] == 2
    assert call_count["count"] == 0  # ¡Cero llamadas a Meta!
    
    # Verificar que los post_ids originales se conservan
    from growth.publication_tracker import load_publications
    rows = load_publications(csv_path)
    assert rows[0]["publication_id"] == "META_POST_1"
    assert rows[1]["publication_id"] == "META_POST_2"


def test_idempotent_mixed_already_and_pending(tmp_path):
    """Test G: CSV con varios ya publicados + varios pendientes → solo procesa pendientes."""
    csv_path = tmp_path / "pub_log.csv"
    
    _write_csv(csv_path, [
        ["2026-08-31", "08:30", "Facebook", "Test 1", ASSET_PHOTO,
         "published", "POST_111", "2026-08-31T08:00:00", "", "", "", ""],
        ["2026-08-31", "09:00", "Instagram", "Test 2", ASSET_VIDEO,
         "pending", "", "", "", "", "", ""],
        ["2026-08-31", "10:00", "Facebook", "Test 3", ASSET_PHOTO,
         "published", "POST_222", "2026-08-31T09:00:00", "", "", "", ""],
        ["2026-08-31", "11:00", "Instagram", "Test 4", ASSET_VIDEO,
         "pending", "", "", "", "", "", ""],
    ])
    
    class MockPublisher:
        pass
    
    call_count = {"count": 0}
    def mock_publish_fn(row, publisher):
        call_count["count"] += 1
        return type('MetaResponse', (), {
            'success': True,
            'post_id': f'NEW_POST_{call_count["count"]}',
            'status': 'scheduled',
            'error': None,
            'raw_response': {}
        })()
    
    result = validate_and_publish(
        csv_path=csv_path,
        tenant_id="firma-bordados",
        publisher=MockPublisher(),
        publish_fn=mock_publish_fn,
    )
    
    # 2 saltados (ya publicados), 2 nuevos publicados
    assert result["published_count"] == 2
    assert result["skipped_count"] == 2
    assert call_count["count"] == 2  # Solo 2 llamadas (los pendientes)
    
    from growth.publication_tracker import load_publications
    rows = load_publications(csv_path)
    assert rows[0]["publication_id"] == "POST_111"
    assert rows[2]["publication_id"] == "POST_222"
    assert rows[1]["publication_id"].startswith("NEW_POST_")
    assert rows[3]["publication_id"].startswith("NEW_POST_")


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_idempotent_skip_published(tmp_path)
        print("✅ test_idempotent_skip_published PASSED")
        test_idempotent_rerun_same_csv_no_duplicates(tmp_path)
        print("✅ test_idempotent_rerun_same_csv_no_duplicates PASSED")
        test_idempotent_mixed_already_and_pending(tmp_path)
        print("✅ test_idempotent_mixed_already_and_pending PASSED")
    print("\n🎉 TODOS LOS TESTS DE IDEMPOTENCIA PASARON")
