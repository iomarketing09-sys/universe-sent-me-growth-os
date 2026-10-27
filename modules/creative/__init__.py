"""Módulo creative: copy, kit de marca y selección de imágenes.

Los agentes creativos viven aquí (``agents/copywriter_agent``) y el módulo
expone utilidades compartidas para armar piezas: paleta de marca por tenant y
selección de imágenes reales de producto.
"""

from __future__ import annotations

__all__ = [
    "CopywriterAgent",
    "create_copywriter_agent",
    "load_voice_profile",
    "validate_variant",
    "validate_batch",
    "load_brand_kit",
    "palette_hex",
    "logo_path",
    "load_approved_models",
    "list_model_assets",
    "select_campaign_assets",
]

_EXPORTS = {
    "CopywriterAgent": (
        "modules.creative.agents.copywriter_agent.agent",
        "CopywriterAgent",
    ),
    "create_copywriter_agent": (
        "modules.creative.agents.copywriter_agent.agent",
        "create_copywriter_agent",
    ),
    "load_voice_profile": (
        "modules.creative.agents.copywriter_agent.skills.voice_loader",
        "load_voice_profile",
    ),
    "validate_variant": (
        "modules.creative.agents.copywriter_agent.skills.copy_validator",
        "validate_variant",
    ),
    "validate_batch": (
        "modules.creative.agents.copywriter_agent.skills.copy_validator",
        "validate_batch",
    ),
    "load_brand_kit": ("modules.creative.brand_kit", "load_brand_kit"),
    "palette_hex": ("modules.creative.brand_kit", "palette_hex"),
    "logo_path": ("modules.creative.brand_kit", "logo_path"),
    "load_approved_models": ("modules.creative.image_selector", "load_approved_models"),
    "list_model_assets": ("modules.creative.image_selector", "list_model_assets"),
    "select_campaign_assets": ("modules.creative.image_selector", "select_campaign_assets"),
}


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    module_name, attribute = _EXPORTS[name]
    return getattr(importlib.import_module(module_name), attribute)
