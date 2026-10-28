"""Meta Ads Agent: resultados de campañas de Meta para un tenant."""

__all__ = ["MetaAdsAgent"]
__version__ = "1.0.0"


def __getattr__(name):
    """Import perezoso para no ejecutar el módulo dos veces con ``python -m``."""
    if name in __all__:
        from modules.intelligence.agents.meta_ads_agent.agent import MetaAdsAgent

        return MetaAdsAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
