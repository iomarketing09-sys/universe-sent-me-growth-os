"""
Tests unitarios para growth/meta_publisher.py
"""
import os
import json
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

# Importar el módulo - las env vars ya están seteadas en conftest o se setean aquí
from growth.meta_publisher import (
    MetaPublisher,
    MetaResponse,
    load_dryrun_schedule,
    resolve_asset_path,
    publish_schedule_from_dryrun,
)


class TestMetaPublisherInit:
    """Tests de inicialización."""
    
    def test_init_dry_run_default(self):
        """Dry-run es True por defecto via env var."""
        publisher = MetaPublisher()
        assert publisher.dry_run is True
    
    def test_init_with_params(self):
        """Inicialización con parámetros explícitos."""
        publisher = MetaPublisher(
            page_id="page_123",
            access_token="token_456",
            dry_run=True,
        )
        assert publisher.page_id == "page_123"
        assert publisher.access_token == "token_456"
        assert publisher.dry_run is True
    
    def test_init_real_mode_requires_credentials(self):
        """Modo real requiere credenciales - test con env vars limpias."""
        # Guardar env vars actuales
        old_meta_page_id = os.environ.get("META_PAGE_ID")
        old_fb_page_id = os.environ.get("FB_PAGE_ID")
        old_meta_access_token = os.environ.get("META_ACCESS_TOKEN")
        old_meta_page_token = os.environ.get("META_PAGE_ACCESS_TOKEN")
        
        try:
            # Limpiar TODAS las env vars de credenciales
            for key in ["META_PAGE_ID", "FB_PAGE_ID", "META_ACCESS_TOKEN", "META_PAGE_ACCESS_TOKEN"]:
                if key in os.environ:
                    del os.environ[key]
            
            # Instanciar pasando explícitamente valores vacíos para evitar auto-loader
            with pytest.raises(ValueError, match="Modo real requiere credenciales"):
                MetaPublisher(page_id="", access_token="", dry_run=False)
        finally:
            # Restaurar
            if old_meta_page_id:
                os.environ["META_PAGE_ID"] = old_meta_page_id
            if old_fb_page_id:
                os.environ["FB_PAGE_ID"] = old_fb_page_id
            if old_meta_access_token:
                os.environ["META_ACCESS_TOKEN"] = old_meta_access_token
            if old_meta_page_token:
                os.environ["META_PAGE_ACCESS_TOKEN"] = old_meta_page_token
    
    def test_init_real_mode_with_credentials(self):
        """Modo real funciona con credenciales."""
        publisher = MetaPublisher(
            page_id="page_123",
            access_token="token_456",
            dry_run=False,
        )
        assert publisher.dry_run is False


class TestBuildScheduledTime:
    """Tests de conversión de tiempo."""
    
    def test_iso_to_unix_timestamp(self):
        """Convierte ISO datetime a UNIX timestamp."""
        publisher = MetaPublisher(dry_run=True)
        ts = publisher._build_scheduled_time("2026-08-31T13:30:00+00:00")
        expected = int(datetime(2026, 8, 31, 13, 30, 0, tzinfo=timezone.utc).timestamp())
        assert ts == expected
    
    def test_z_suffix_handling(self):
        """Maneja sufijo Z correctamente."""
        publisher = MetaPublisher(dry_run=True)
        ts = publisher._build_scheduled_time("2026-08-31T13:30:00Z")
        expected = int(datetime(2026, 8, 31, 13, 30, 0, tzinfo=timezone.utc).timestamp())
        assert ts == expected


class TestMockResponse:
    """Tests de respuestas mock."""
    
    def test_mock_response_structure(self):
        """Estructura de respuesta mock correcta."""
        publisher = MetaPublisher(dry_run=True)
        response = publisher._mock_response("text")
        
        assert isinstance(response, MetaResponse)
        assert response.success is True
        assert response.status == "scheduled"
        assert response.post_id is not None
        assert response.post_id.startswith("mock_text_")
        assert response.raw_response == {"id": response.post_id, "status": "scheduled"}
        assert response.error is None
    
    def test_mock_response_types(self):
        """Diferentes tipos generan IDs distintos."""
        publisher = MetaPublisher(dry_run=True)
        text_resp = publisher._mock_response("text")
        photo_resp = publisher._mock_response("photo")
        video_resp = publisher._mock_response("video")
        
        assert text_resp.post_id.startswith("mock_text_")
        assert photo_resp.post_id.startswith("mock_photo_")
        assert video_resp.post_id.startswith("mock_video_")


class TestPublishText:
    """Tests de publicación de texto."""
    
    def test_publish_text_basic(self):
        """Publicación de texto básica."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_text(
            message="Test message",
            scheduled_publish_time="2026-08-31T13:30:00+00:00",
        )
        
        assert isinstance(result, MetaResponse)
        assert result.success is True
        assert result.status == "scheduled"
    
    def test_publish_text_with_link(self):
        """Publicación de texto con link."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_text(
            message="Test with link",
            scheduled_publish_time="2026-08-31T13:30:00+00:00",
            link="https://wa.me/5218787880735",
        )
        
        assert result.success is True
    
    def test_publish_text_unix_timestamp(self):
        """Acepta UNIX timestamp directo."""
        publisher = MetaPublisher(dry_run=True)
        ts = int(datetime(2026, 8, 31, 13, 30, 0, tzinfo=timezone.utc).timestamp())
        result = publisher.publish_text(
            message="Test",
            scheduled_publish_time=ts,
        )
        assert result.success is True


class TestPublishPhoto:
    """Tests de publicación de foto."""
    
    def test_publish_photo_dry_run(self):
        """Publicación de foto en dry-run."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_photo(
            image_path="/fake/path/test.jpg",
            caption="Test caption",
            scheduled_publish_time="2026-08-31T19:00:00+00:00",
        )
        
        assert isinstance(result, MetaResponse)
        assert result.success is True
        assert result.status == "scheduled"
    
    def test_publish_photo_missing_file_real_mode(self):
        """Falla si archivo no existe en modo real."""
        publisher = MetaPublisher(
            page_id="page_123",
            access_token="token_456",
            dry_run=False,
        )
        result = publisher.publish_photo(
            image_path="/nonexistent/test.jpg",
            caption="Test",
            scheduled_publish_time="2026-08-31T19:00:00+00:00",
        )
        
        assert result.success is False
        assert "no encontrado" in result.error.lower()


class TestPublishVideo:
    """Tests de publicación de video."""
    
    def test_publish_video_dry_run(self):
        """Publicación de video en dry-run."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_video(
            video_path="/fake/path/test.mp4",
            description="Test video",
            scheduled_publish_time="2026-09-01T00:30:00+00:00",
        )
        
        assert isinstance(result, MetaResponse)
        assert result.success is True
        assert result.status == "scheduled"
    
    def test_publish_video_with_title(self):
        """Video con título opcional."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_video(
            video_path="/fake/path/test.mp4",
            description="Test",
            scheduled_publish_time="2026-09-01T00:30:00+00:00",
            title="Test Title",
        )
        assert result.success is True


class TestLoadDryrunSchedule:
    """Tests de carga de schedule."""
    
    def test_load_dryrun_schedule(self):
        """Carga schedule desde dryrun_output.json."""
        dryrun_path = Path(__file__).parent.parent / "dryrun_output.json"
        schedule = load_dryrun_schedule(dryrun_path)
        
        assert isinstance(schedule, list)
        assert len(schedule) == 20
        for slot in schedule:
            assert "slot_id" in slot
            assert "slot_type" in slot
            assert "datetime_utc" in slot
            assert "day" in slot
    
    def test_schedule_counts(self):
        """Verifica conteo media vs text."""
        dryrun_path = Path(__file__).parent.parent / "dryrun_output.json"
        schedule = load_dryrun_schedule(dryrun_path)
        
        media = sum(1 for s in schedule if s["slot_type"] == "media")
        text = sum(1 for s in schedule if s["slot_type"] == "text")
        
        assert media == 17
        assert text == 3
        assert len(schedule) == 20


class TestResolveAssetPath:
    """Tests de resolución de rutas de assets."""
    
    def test_resolve_asset_root_path(self):
        """Resuelve asset en root del tenant."""
        tenant_root = Path("/fake/tenant")
        slot = {
            "source_filename": "test.jpg",
            "source_path": None,
        }
        path = resolve_asset_path(slot, tenant_root)
        assert path == tenant_root / "test.jpg"
    
    def test_resolve_asset_with_subpath(self):
        """Resuelve asset con subpath."""
        tenant_root = Path("/fake/tenant")
        slot = {
            "source_filename": "test.jpg",
            "source_path": "subfolder/",
        }
        path = resolve_asset_path(slot, tenant_root)
        assert path == tenant_root / "subfolder" / "test.jpg"
    
    def test_resolve_asset_none_filename(self):
        """Retorna None si no hay filename."""
        tenant_root = Path("/fake/tenant")
        slot = {"source_filename": None}
        path = resolve_asset_path(slot, tenant_root)
        assert path is None


class TestPublishScheduleFromDryrun:
    """Tests de publicación completa desde dryrun."""
    
    def test_publish_schedule_dry_run(self):
        """Publica schedule completo en dry-run."""
        dryrun_path = Path(__file__).parent.parent / "dryrun_output.json"
        tenant_root = Path(__file__).parent.parent / "tenants" / "firma-bordados"
        
        results = publish_schedule_from_dryrun(
            dryrun_path=dryrun_path,
            tenant_root=tenant_root,
            dry_run=True,
        )
        
        assert len(results) == 20
        for result in results:
            assert isinstance(result, MetaResponse)
            assert result.success is True
            assert result.status == "scheduled"
    
    def test_publish_schedule_counts(self):
        """Verifica que se procesen todos los slots."""
        dryrun_path = Path(__file__).parent.parent / "dryrun_output.json"
        tenant_root = Path(__file__).parent.parent / "tenants" / "firma-bordados"
        
        results = publish_schedule_from_dryrun(
            dryrun_path=dryrun_path,
            tenant_root=tenant_root,
            dry_run=True,
        )
        
        assert len(results) == 20
        assert all(r.success for r in results)


class TestMetaResponse:
    """Tests del dataclass MetaResponse."""
    
    def test_meta_response_creation(self):
        """Creación básica."""
        resp = MetaResponse(success=True, post_id="test_123", status="scheduled")
        assert resp.success is True
        assert resp.post_id == "test_123"
    
    def test_meta_response_error(self):
        """Respuesta con error."""
        resp = MetaResponse(success=False, error="Test error")
        assert resp.success is False
        assert resp.error == "Test error"
        assert resp.post_id is None


class TestPayloadStructure:
    """Valida estructura de payloads para Meta API."""
    
    def test_text_payload_fields(self):
        """Campos requeridos para feed post."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_text(
            message="Test",
            scheduled_publish_time=1234567890,
        )
        assert result.success
    
    def test_photo_payload_fields(self):
        """Campos para photo post."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_photo(
            image_path="test.jpg",
            caption="Caption",
            scheduled_publish_time=1234567890,
        )
        assert result.success
    
    def test_video_payload_fields(self):
        """Campos para video post."""
        publisher = MetaPublisher(dry_run=True)
        result = publisher.publish_video(
            video_path="test.mp4",
            description="Desc",
            scheduled_publish_time=1234567890,
        )
        assert result.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
