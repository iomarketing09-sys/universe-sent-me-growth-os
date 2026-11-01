"""Módulo communications: WhatsApp y comentarios.

WhatsApp es solo lectura. Los comentarios de Facebook permiten captura y
publicación únicamente de respuestas aprobadas explícitamente.
"""

from __future__ import annotations

__all__ = [
    "CommunicationsAgent",
    "OmniRouteClient",
    "check_response",
    "WhatsAppAgent",
    "collect_whatsapp_live",
    "collect_remote_contacts",
    "diagnose_echoes",
    "conversation_summary",
    "depth_distribution",
    "campaign_conversations",
]

_EXPORTS = {
    "CommunicationsAgent": ("modules.communications.agent", "CommunicationsAgent"),
    "OmniRouteClient": ("modules.communications.llm", "OmniRouteClient"),
    "check_response": ("modules.communications.policy", "check_response"),
    "WhatsAppAgent": ("modules.communications.whatsapp.agent", "WhatsAppAgent"),
    "collect_whatsapp_live": (
        "modules.communications.whatsapp.adapters",
        "collect_whatsapp_live",
    ),
    "collect_remote_contacts": (
        "modules.communications.whatsapp.adapters",
        "collect_remote_contacts",
    ),
    "diagnose_echoes": (
        "modules.communications.whatsapp.echo_diagnostics",
        "diagnose_echoes",
    ),
    "conversation_summary": (
        "modules.communications.whatsapp.conversations",
        "conversation_summary",
    ),
    "depth_distribution": (
        "modules.communications.whatsapp.conversations",
        "depth_distribution",
    ),
    "campaign_conversations": (
        "modules.communications.whatsapp.conversations",
        "campaign_conversations",
    ),
}


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    module_name, attribute = _EXPORTS[name]
    return getattr(importlib.import_module(module_name), attribute)
