"""Tests del módulo creative: kit de marca y selección de imágenes."""

from __future__ import annotations

from pathlib import Path

from modules.creative.brand_kit import load_brand_kit, logo_path, palette_hex
from modules.creative.image_selector import (
    load_approved_models,
    select_campaign_assets,
)


ROOT = Path(__file__).resolve().parents[1]


def test_brand_kit_flexi_tiene_rojo_de_marca_y_logo():
    kit = load_brand_kit("flexi", base_path=str(ROOT))
    palette = palette_hex("flexi", base_path=str(ROOT))
    assert kit["season"]["macrotendencia"] == "Luz y sombra"
    assert palette["Rojo Flexi"] == "#D82232"
    assert "Arena" in palette
    assert logo_path("flexi", base_path=str(ROOT)) is not None


def test_brand_kit_es_aislado_por_tenant():
    flexi = load_brand_kit("flexi", base_path=str(ROOT))
    micas = load_brand_kit("micas-art-deco", base_path=str(ROOT))
    assert flexi["tenant_id"] != micas["tenant_id"]
    assert flexi["palette"] != micas["palette"]


def test_selector_solo_usa_modelos_aprobados():
    approved = {str(m["code"]) for m in load_approved_models("flexi", base_path=str(ROOT))}
    result = select_campaign_assets("flexi", base_path=str(ROOT), max_total=20)
    assert result["selected"], "debe seleccionar al menos una imagen"
    assert {item["model_code"] for item in result["selected"]} <= approved


def test_selector_deduplica_mayusculas_y_copias():
    result = select_campaign_assets("flexi", base_path=str(ROOT), max_total=50)
    names = [item["filename"].lower() for item in result["selected"]]
    assert len(names) == len(set(names))
    assert not any("(1)" in name for name in names)


def test_selector_respeta_limites():
    result = select_campaign_assets(
        "flexi", base_path=str(ROOT), max_per_model=2, max_total=4
    )
    assert result["total"] <= 4
    per_model = {}
    for item in result["selected"]:
        per_model[item["model_code"]] = per_model.get(item["model_code"], 0) + 1
    assert all(count <= 2 for count in per_model.values())


def test_selector_reporta_modelos_sin_assets():
    result = select_campaign_assets(
        "flexi", base_path=str(ROOT), model_codes=["999999"]
    )
    assert result["selected"] == []
    assert result["models_without_assets"] == ["999999"]
