"""Tests del analizador de copys publicados del Brand Voice Agent."""

from __future__ import annotations

import json
from pathlib import Path

from modules.identity.agents.brand_voice_agent.skills.post_voice_analyzer import analyze_posts, load_posts


def _write_posts(path: Path, posts):
    path.mkdir(parents=True, exist_ok=True)
    (path / "meta_posts_20261011.json").write_text(
        json.dumps(posts, ensure_ascii=False), encoding="utf-8"
    )


def test_load_posts_deduplicates_and_prefers_latest(tmp_path):
    tenant = tmp_path / "tenants" / "demo"
    _write_posts(
        tenant / "data",
        [
            {"post_id": "1", "message": "Versión vieja", "created_time": "2026-10-01"},
            {"post_id": "1", "message": "Versión nueva", "created_time": "2026-10-02"},
            {"post_id": "2", "message": "Otro post", "created_time": "2026-10-03"},
        ],
    )

    posts, sources = load_posts(tenant)

    assert sources == ["meta_posts_20261011.json"]
    assert [post["message"] for post in posts] == ["Otro post", "Versión nueva"]


def test_analyze_posts_extracts_real_patterns(tmp_path):
    tenant = tmp_path / "tenants" / "demo"
    _write_posts(
        tenant / "data",
        [
            {
                "post_id": "1",
                "message": (
                    "Tus pies necesitan un descanso 👣 Elige calzado cómodo.\n\n"
                    "Te esperamos en Zapatería Demo #PiedrasNegras"
                ),
                "created_time": "2026-10-01",
            },
            {
                "post_id": "2",
                "message": (
                    "Tu día comienza mejor con confort 😌\n\n"
                    "Visítanos en Zapatería Demo #PiedrasNegras"
                ),
                "created_time": "2026-10-02",
            },
        ],
    )

    posts, sources = load_posts(tenant)
    evidence = analyze_posts(posts, sources=sources, max_examples=2)

    assert evidence["posts_analyzed"] == 2
    assert evidence["emoji"]["posts_with_emoji"] == 2
    assert evidence["second_person_openings_ratio"] == 1.0
    assert evidence["local_markers"]
    assert evidence["signature_examples"]
    assert all("text" in example for example in evidence["signature_examples"])


def test_analyze_posts_without_posts_is_safe():
    evidence = analyze_posts([], sources=[])

    assert evidence["posts_analyzed"] == 0
    assert evidence["signature_examples"] == []
    assert evidence["ad_translation"] == []
