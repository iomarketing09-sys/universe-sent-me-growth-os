"""Tests del reporte de cobertura de medición."""

from __future__ import annotations

from modules.intelligence.measurement_coverage import (
    build_measurement_coverage,
    render_measurement_coverage,
)
from modules.intelligence.metrics_snapshot import MetricsSnapshot


def test_coverage_detecta_muestras_de_video_y_reach():
    snapshots = [
        MetricsSnapshot(
            publication_id="fb_video",
            platform="Facebook",
            reach=0,
            video_views=100,
            video_views_organic=100,
            video_complete_views=55,
            video_watch_time=6000,
            video_length=15000,
        ),
        MetricsSnapshot(
            publication_id="ig_post",
            platform="Instagram",
            reach=420,
            views=700,
            saved=4,
        ),
    ]

    report = build_measurement_coverage("universe", snapshots)

    assert report["hypotheses"]["HB-UNI-002"]["status"] == "samples_available"
    assert report["hypotheses"]["HB-UNI-002"]["publications"] == 1
    assert report["hypotheses"]["HB-UNI-004"]["status"] == "samples_available"
    assert report["platforms"]["Facebook"]["metrics"]["video_completion_rate"]["median"] == 0.55
    assert report["platforms"]["Instagram"]["metrics"]["reach"]["median"] == 420.0


def test_coverage_reporta_bloqueos_sin_datos():
    report = build_measurement_coverage(
        "universe",
        [MetricsSnapshot(publication_id="fb_photo", platform="Facebook")],
    )

    assert report["hypotheses"]["HB-UNI-002"]["status"] == "no_samples"
    assert report["hypotheses"]["HB-UNI-004"]["status"] == "no_samples"
    assert "instagram_manage_insights" in report["hypotheses"]["HB-UNI-004"]["blocker"]
    assert "Sin videos Facebook" in report["hypotheses"]["HB-UNI-002"]["blocker"]


def test_render_coverage_es_legible():
    report = build_measurement_coverage(
        "universe",
        [MetricsSnapshot(publication_id="ig_post", platform="Instagram", reach=420)],
    )

    text = render_measurement_coverage(report)

    assert "Cobertura de medición · universe" in text
    assert "HB-UNI-004: samples_available" in text


def test_coverage_deduplica_publicaciones_y_usa_ultimo_snapshot():
    snapshots = [
        MetricsSnapshot(
            publication_id="fb_video",
            platform="Facebook",
            captured_at_utc="2026-11-01T00:00:00+00:00",
            video_views_organic=100,
            video_complete_views=50,
        ),
        MetricsSnapshot(
            publication_id="fb_video",
            platform="Facebook",
            captured_at_utc="2026-11-02T00:00:00+00:00",
            video_views_organic=100,
            video_complete_views=60,
        ),
    ]

    report = build_measurement_coverage("universe", snapshots)

    metric = report["platforms"]["Facebook"]["metrics"]["video_completion_rate"]
    assert metric["rows"] == 2
    assert metric["publications"] == 1
    assert metric["median"] == 0.6
    assert report["hypotheses"]["HB-UNI-002"]["publications"] == 1


def test_coverage_acepta_cero_porcentaje_de_completacion_como_dato():
    report = build_measurement_coverage(
        "universe",
        [
            MetricsSnapshot(
                publication_id="fb_video",
                platform="Facebook",
                video_views_organic=100,
                video_complete_views=0,
            )
        ],
    )

    metric = report["platforms"]["Facebook"]["metrics"]["video_completion_rate"]
    assert metric["publications"] == 1
    assert metric["median"] == 0.0
