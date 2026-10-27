"""Compatibilidad: el código vive en ``modules.identity.tenant_registry``.

Este archivo se conserva para no romper imports existentes.
"""

from modules.identity.tenant_registry import *  # noqa: F401,F403
