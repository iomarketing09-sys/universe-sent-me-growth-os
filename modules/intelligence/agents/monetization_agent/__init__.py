"""Monetization Agent: reporte y conciliación read-only por tenant."""

__all__ = ["MonetizationAgent"]
__version__ = "1.0.0"


def __getattr__(name):
    """Import perezoso para no ejecutar el módulo dos veces con ``python -m``."""
    if name in __all__:
        from modules.intelligence.agents.monetization_agent.agent import MonetizationAgent

        return MonetizationAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
