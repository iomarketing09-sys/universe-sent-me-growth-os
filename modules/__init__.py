"""Growth OS modules.

Cada módulo encapsula un dominio del negocio y expone una API pública estable.
Los módulos dependen de ``core`` (dominio y almacenamiento) y no entre sí, salvo
por el orquestador ``cgo``.
"""

__all__ = ["communications", "creative", "identity", "social"]
