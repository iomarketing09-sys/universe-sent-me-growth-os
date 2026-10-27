"""Copywriter Agent - copy por tenant usando la voz de marca y skills de anuncios."""

__all__ = ["CopywriterAgent", "create_copywriter_agent"]
__version__ = "1.0.0"


def __getattr__(name):
    """Import perezoso para evitar el warning de runpy con `python -m`."""
    if name in __all__:
        from .agent import CopywriterAgent, create_copywriter_agent

        return {
            "CopywriterAgent": CopywriterAgent,
            "create_copywriter_agent": create_copywriter_agent,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
