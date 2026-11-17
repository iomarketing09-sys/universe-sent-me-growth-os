"""Carga contexto editorial externo de publicaciones sin modificar su fuente.

Para Universe Sent Me, el CSV de Google Drive es la referencia editorial. La
resolución se hace únicamente por ID de Facebook o permalink exacto; no se
intenta emparejar por fecha, caption ni similitud textual.
"""
from __future__ import annotations

import csv
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

DEFAULT_UNIVERSE_CSV = (
    Path.home()
    / "GoogleDrive"
    / "Universe sent me"
    / "Publicaciones Universe Sent Me — Noviembre 2026.csv"
)


def source_path(tenant_id: str = "universe") -> Path | None:
    """Devuelve la ruta configurada; admite UNIVERSE_PUBLICATION_CONTEXT_CSV.

    Si no se define, usa el CSV de noviembre en la carpeta GoogleDrive del
    usuario que ejecuta Growth OS.
    """
    if tenant_id != "universe":
        return None
    configured = os.getenv("UNIVERSE_PUBLICATION_CONTEXT_CSV", "").strip()
    return Path(configured).expanduser() if configured else DEFAULT_UNIVERSE_CSV


def _clean(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _facebook_id(value: str) -> str:
    value = _clean(value)
    if not value or "verificar" in value.casefold():
        return ""
    if value.startswith("http"):
        parsed = urlparse(value)
        path_match = re.search(r"/posts/(pfbid[\w]+)", parsed.path)
        if path_match:
            return path_match.group(1)
        return _clean(parse_qs(parsed.query).get("fbid", [""])[0])
    return value


def _published_at(row: dict[str, str]) -> str:
    date, time = _clean(row.get("Fecha")), _clean(row.get("Hora"))
    if not date:
        return ""
    try:
        return datetime.fromisoformat(f"{date}T{time or '00:00'}").isoformat()
    except ValueError:
        return date


def load_external_contexts(path: Path | None) -> list[dict[str, Any]]:
    """Lee el CSV y traduce sus columnas al contrato de contexto de Growth."""
    if path is None or not path.is_file():
        return []
    contexts: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                publication_id = _facebook_id(row.get("ID de FB", ""))
                permalink = _clean(row.get("Enlace"))
                if not publication_id and permalink and "verificar" not in permalink.casefold():
                    publication_id = _facebook_id(permalink)
                if not publication_id:
                    continue
                meme_text = _clean(row.get("Texto de la imagen"))
                if meme_text.casefold() == "por verificar":
                    meme_text = ""
                contexts.append(
                    {
                        "publication_id": publication_id,
                        "permalink_url": permalink if permalink.startswith("http") else "",
                        "asset_ref": _clean(row.get("Asset")),
                        "character": _clean(row.get("Personaje")),
                        "meme_text": meme_text,
                        "visual_context": _clean(row.get("Contexto")),
                        "caption": _clean(row.get("Caption publicado")),
                        "published_at": _published_at(row),
                        "source_notes": _clean(row.get("Notas")),
                        "context_source": "google_drive_november_2026",
                    }
                )
    except (OSError, csv.Error, UnicodeDecodeError):
        return []
    return contexts


def context_matches(context: dict[str, Any], post_id: str, permalink_url: str = "") -> bool:
    """Coincidencia estricta con ID de Graph o ID visible en permalink."""
    raw_post_id = _clean(post_id)
    candidates = {
        _facebook_id(raw_post_id),
        _facebook_id(raw_post_id.rsplit("_", 1)[-1]),
        _facebook_id(permalink_url),
    }
    candidates.discard("")
    raw_stored = _clean(context.get("publication_id"))
    stored_ids = {
        _facebook_id(raw_stored),
        _facebook_id(raw_stored.rsplit("_", 1)[-1]),
    }
    stored_ids.discard("")
    return bool(stored_ids.intersection(candidates))


__all__ = ["source_path", "load_external_contexts", "context_matches"]
