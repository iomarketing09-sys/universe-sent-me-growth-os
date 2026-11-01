"""Rutas del módulo de comentarios sin efectos secundarios."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


def repository_root(start: Optional[Path] = None) -> Path:
    """Encuentra la raíz que contiene ``modules`` y ``tenants``."""
    current = Path(start or __file__).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "modules").is_dir() and (candidate / "tenants").is_dir():
            return candidate
    return Path.cwd().resolve()


def load_tenant_config(tenant_id: str, base_path: Optional[Path] = None) -> Dict[str, Any]:
    path = (Path(base_path) if base_path else repository_root()) / "tenants" / tenant_id / "config.json"
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


@dataclass(frozen=True)
class CommentPaths:
    """Ubicación de los datos de comentarios de un tenant."""

    tenant_id: str
    base_path: Path
    storage_dir: Path

    @classmethod
    def for_tenant(
        cls,
        tenant_id: str,
        base_path: Optional[Path] = None,
        storage_dir: Optional[Path] = None,
    ) -> "CommentPaths":
        if not tenant_id or Path(tenant_id).name != tenant_id:
            raise ValueError("tenant_id inválido")

        root = Path(base_path).resolve() if base_path else repository_root()
        storage = (
            Path(storage_dir)
            if storage_dir is not None
            else root / "tenants" / tenant_id / "comment_responses" / "facebook_comments"
        )
        if not storage.is_absolute():
            storage = root / storage
        return cls(tenant_id=tenant_id, base_path=root, storage_dir=storage.resolve())

    @property
    def tenant_dir(self) -> Path:
        return self.base_path / "tenants" / self.tenant_id

    @property
    def approvals_file(self) -> Path:
        return self.storage_dir / "aprobaciones.json"

    @property
    def comments_log_file(self) -> Path:
        return self.storage_dir / "data" / "comments_log.csv"

    @property
    def publication_contexts_file(self) -> Path:
        return self.tenant_dir / "publication_contexts.json"

    @property
    def env_files(self) -> tuple[Path, ...]:
        return (self.base_path / ".env", self.tenant_dir / ".env")
