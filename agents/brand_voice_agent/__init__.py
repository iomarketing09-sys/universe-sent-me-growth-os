"""Brand Voice Agent - agente de voz de marca por tenant."""

__all__ = [
    "BrandVoiceAgent",
    "ModelRouter",
    "get_model_alias",
    "get_generation_params",
    "BrandVoiceMemory",
]


def __getattr__(name):
    """Import perezoso para que `python -m agents.brand_voice_agent.agent` no avise."""
    if name == "BrandVoiceAgent":
        from .agent import BrandVoiceAgent

        return BrandVoiceAgent
    if name in {"ModelRouter", "get_model_alias", "get_generation_params"}:
        from . import models

        return getattr(models, name)
    if name == "BrandVoiceMemory":
        from .memory import BrandVoiceMemory

        return BrandVoiceMemory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
