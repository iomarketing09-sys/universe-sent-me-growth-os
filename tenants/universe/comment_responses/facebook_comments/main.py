#!/usr/bin/env python3
"""Compatibilidad del comando histórico de comentarios de Universe."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.communications.comments.facebook import (  # noqa: E402
    CommentProcessor,
    load_environment,
    main,
    publish_approved,
    resolve_page_token,
)

__all__ = [
    "CommentProcessor",
    "load_environment",
    "main",
    "publish_approved",
    "resolve_page_token",
]


if __name__ == "__main__":
    raise SystemExit(main())
