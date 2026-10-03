"""
Tests de integración para growth/publisher.py

Demuestran que el gate de auditoría bloquea o permite la publicación
según ready_for_publication.
"""
from pathlib import Path
import csv
import shutil

from growth.publisher import publish_pending, get_pending_count
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


def _write_test_csv(csv_path: Path, rows: list):
    """Escribe CSV con header y filas dadas (formato publication_log.csv)."""
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "date", "time", "platform", "piece", "asset_filename",
            "status", "publication_id", "published_at", "reach",
            "interactions", "DMs", "leads"
        ])
        for row in rows:
            writer.writerow(row)


def _copy_original_csv(tmp_path):
    """Copia el publication_log.csv original para tests que lo necesiten."""
    src = Path(__file__).parent.parent / "publication_log.csv"
    dst = tmp_path / "publication_log.csv"
    shutil.copy2(src, dst)
    return dst


class TestReadyForPublication:
    """Caso 1 — MATCH / READY → debe permitir publicación"""

    def test_all_match_allows_publication(self, tmp_path):
        asset_root, orig_root, orig_excl = _setup_test_assets(tmp_path)
        try:
            csv_path = tmp_path / "pub_log.csv"
            _write_test_csv(csv_path, [
                ["2026-08-31", "08:30", "Facebook", "Test 1", "ok.jpg",
                 "pending", "", "", "", "", "", ""],
                ["2026-08-31", "09:00", "Instagram", "Test 2", "video.mp4",
                 "pending", "", "", "", "", "", ""],
            ])

            # Verificar que workflow dice READY
            workflow_result = run_publication_workflow(csv_path)
            assert workflow_result["ready_for_publication"] is True

            # Publicar
            result = publish_pending(csv_path)

            assert result["success"] is True
            assert result["blocked"] is False
            assert result["published_count"] == 2
            assert result["error"] is None

            # Verificar que el CSV se actualizó
            from growth.publication_tracker import load_publications
            rows = load_publications(csv_path)
            for row in rows:
                assert row["status"] == "published"
                assert row["published_at"] != ""
                assert row["publication_id"] != ""
        finally:
            _teardown_test_assets(orig_root, orig_excl)


class TestMissingBlocksPublication:
    """Caso 2 — MISSING → debe bloquear publicación"""

    def test_missing_blocks_publication(self, tmp_path):
        asset_root, orig_root, orig_excl = _setup_test_assets(tmp_path)
        try:
            csv_path = tmp_path / "pub_log.csv"
            _write_test_csv(csv_path, [
                ["2026-08-31", "08:30", "Facebook", "Test 1", "ok.jpg",
                 "pending", "", "", "", "", "", ""],
                ["2026-08-31", "09:00", "Instagram", "Test 2", "nonexistent.png",
                 "pending", "", "", "", "", "", ""],
            ])

            # Verificar que workflow dice NOT READY
            workflow_result = run_publication_workflow(csv_path)
            assert workflow_result["ready_for_publication"] is False
            assert workflow_result["audit"]["missing"] == 1

            # Intentar publicar → debe bloquearse
            result = publish_pending(csv_path)

            assert result["success"] is False
            assert result["blocked"] is True
            assert result["published_count"] == 0
            assert "MISSING" in result["error"] or "missing" in result["error"].lower()
            assert result["audit"]["missing"] == 1

            # Verificar que el CSV NO se modificó (sigue pendiente)
            from growth.publication_tracker import load_publications
            rows = load_publications(csv_path)
            for row in rows:
                assert row["status"] == "pending"
        finally:
            _teardown_test_assets(orig_root, orig_excl)


class TestAmbiguousBlocksPublication:
    """Caso 3 — AMBIGUOUS → debe bloquear publicación"""

    def test_ambiguous_blocks_publication(self, tmp_path):
        asset_root, orig_root, orig_excl = _setup_test_assets(tmp_path)
        try:
            csv_path = tmp_path / "pub_log.csv"
            _write_test_csv(csv_path, [
                ["2026-08-31", "08:30", "Facebook", "Test 1", "ok.jpg",
                 "pending", "", "", "", "", "", ""],
                ["2026-08-31", "09:00", "Instagram", "Test 2", "dup.jpg",
                 "pending", "", "", "", "", "", ""],
            ])

            # Verificar que workflow dice NOT READY
            workflow_result = run_publication_workflow(csv_path)
            assert workflow_result["ready_for_publication"] is False
            assert workflow_result["audit"]["ambiguous"] == 1

            # Intentar publicar → debe bloquearse
            result = publish_pending(csv_path)

            assert result["success"] is False
            assert result["blocked"] is True
            assert result["published_count"] == 0
            assert "AMBIGUOUS" in result["error"] or "ambiguous" in result["error"].lower()
            assert result["audit"]["ambiguous"] == 1

            # Verificar que el CSV NO se modificó
            from growth.publication_tracker import load_publications
            rows = load_publications(csv_path)
            for row in rows:
                assert row["status"] == "pending"
        finally:
            _teardown_test_assets(orig_root, orig_excl)


class TestNonexistentCSVBlocksPublication:
    """Caso 4 — CSV inexistente → debe bloquear publicación"""

    def test_nonexistent_csv_blocks(self, tmp_path):
        csv_path = tmp_path / "no_existe.csv"

        result = publish_pending(csv_path)

        assert result["success"] is False
        assert result["blocked"] is True
        assert result["published_count"] == 0
        assert "CSV no encontrado" in result["error"]
        assert result["audit"]["total"] == 0


class TestMalformedCSVBlocksPublication:
    """Caso 5 — CSV malformado → debe bloquear publicación de forma segura"""

    def test_malformed_csv_blocks(self, tmp_path):
        # CSV con estructura incorrecta
        csv_path = tmp_path / "bad.csv"
        csv_path.write_text('col1,col2\n"unclosed quote\n')

        result = publish_pending(csv_path)

        # Debe manejar el error sin crashear
        assert "success" in result
        assert "blocked" in result
        assert "published_count" in result
        assert "audit" in result
        assert "error" in result
        # El comportamiento exacto depende de cómo validate_publications_csv maneje el CSV
        # Lo importante: no crashea y devuelve estructura consistente
        assert result["blocked"] is True or result["success"] is False


class TestOnlyPublishesPending:
    """Verifica que solo publica las filas con status 'pending'"""

    def test_only_pending_are_published(self, tmp_path):
        asset_root, orig_root, orig_excl = _setup_test_assets(tmp_path)
        try:
            csv_path = tmp_path / "pub_log.csv"
            _write_test_csv(csv_path, [
                ["2026-08-31", "08:30", "Facebook", "Test 1", "ok.jpg",
                 "pending", "", "", "", "", "", ""],
                ["2026-08-31", "09:00", "Instagram", "Test 2", "video.mp4",
                 "published", "pub_123", "2026-08-31T08:00:00", "", "", "", ""],
                ["2026-08-31", "10:00", "Facebook", "Test 3", "ok.jpg",
                 "pending", "", "", "", "", "", ""],
            ])

            result = publish_pending(csv_path)

            assert result["success"] is True
            assert result["published_count"] == 2  # Solo las 2 pendientes

            from growth.publication_tracker import load_publications
            rows = load_publications(csv_path)
            pending_count = sum(1 for r in rows if r["status"] == "pending")
            published_count = sum(1 for r in rows if r["status"] == "published")
            assert pending_count == 0
            assert published_count == 3  # 1 ya publicada + 2 nuevas
        finally:
            _teardown_test_assets(orig_root, orig_excl)
