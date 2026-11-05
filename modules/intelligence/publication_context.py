"""Escritor del contexto de publicaciones para comentarios y análisis.

Mantiene ``publication_contexts.json`` como fuente única por tenant. No abre
imágenes: solo usa el nombre del asset, la transcripción disponible en
``assets_meme_text.csv`` y los datos que ya trae la publicación.
"""

from __future__ import annotations

import csv
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from modules.intelligence.planner import parse_asset_filename


def contexts_path(tenant_root: Path) -> Path:
    return Path(tenant_root) / "publication_contexts.json"


def load_contexts(tenant_root: Path) -> Dict[str, Any]:
    path = contexts_path(tenant_root)
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def save_contexts(tenant_root: Path, contexts: Dict[str, Any]) -> None:
    """Escribe de forma atómica para no dejar el JSON truncado."""
    path = contexts_path(tenant_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(contexts, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def _short_id(value: Any) -> str:
    return str(value or "").strip().split("_")[-1]


def _matching_keys(contexts: Dict[str, Any], post_id: str) -> list[str]:
    post_id = str(post_id or "").strip()
    short = _short_id(post_id)
    matches: list[str] = []
    for key, value in contexts.items():
        stored = str((value or {}).get("publication_id") or key).strip()
        if stored == post_id or _short_id(stored) == short:
            matches.append(key)
    if post_id in contexts and post_id not in matches:
        matches.insert(0, post_id)
    return matches


def _merged_existing(contexts: Dict[str, Any], keys: list[str]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for key in keys:
        value = contexts.get(key) or {}
        if not isinstance(value, dict):
            continue
        for field in (
            "publication_id",
            "asset_ref",
            "character",
            "meme_text",
            "visual_context",
            "caption",
            "published_at",
        ):
            if not merged.get(field) and str(value.get(field) or "").strip():
                merged[field] = value.get(field)
    return merged


def _meme_text_index(tenant_root: Path) -> Dict[str, str]:
    path = Path(tenant_root) / "assets_meme_text.csv"
    if not path.is_file():
        return {}
    index: Dict[str, str] = {}
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                filename = str(row.get("filename") or "").strip()
                text = str(row.get("meme_text") or "").strip()
                if filename and text:
                    index[filename] = text
    except (OSError, csv.Error, UnicodeDecodeError):
        return {}
    return index


def _derived_asset_fields(
    tenant_root: Path,
    asset_filename: str,
) -> Dict[str, str]:
    filename = Path(str(asset_filename or "")).name
    parsed = parse_asset_filename(filename) if filename else {}
    characters = parsed.get("characters") or []
    meme_text = str(parsed.get("meme_text") or "").strip()
    if not meme_text and filename:
        meme_text = _meme_text_index(tenant_root).get(filename, "")
    return {
        "character": "+".join(str(name) for name in characters),
        "meme_text": meme_text,
    }


def record_publication(
    tenant_root: Path,
    *,
    post_id: str,
    asset_filename: str,
    caption: str,
    published_at: str = "",
    character: str = "",
    meme_text: str = "",
    visual_context: str = "",
) -> Dict[str, Any]:
    """Crea o completa el contexto de una publicación.

    Es idempotente y conserva los campos ricos que ya existan, por ejemplo el
    ``visual_context`` obtenido por visión. Si el post ya tiene alias corto y
    largo, actualiza ambos para no dejar copias divergentes.
    """
    post_id = str(post_id or "").strip()
    if not post_id:
        return {}

    contexts = load_contexts(tenant_root)
    keys = _matching_keys(contexts, post_id)
    existing = _merged_existing(contexts, keys)
    derived = _derived_asset_fields(tenant_root, asset_filename)

    merged = {
        "publication_id": str(existing.get("publication_id") or post_id),
        "asset_ref": str(existing.get("asset_ref") or asset_filename or ""),
        "character": str(character or existing.get("character") or derived["character"] or ""),
        "meme_text": str(meme_text or existing.get("meme_text") or derived["meme_text"] or ""),
        "visual_context": str(visual_context or existing.get("visual_context") or ""),
        "caption": str(caption or existing.get("caption") or ""),
        "published_at": str(published_at or existing.get("published_at") or ""),
    }

    targets = keys or [post_id]
    changed = False
    for key in targets:
        if contexts.get(key) != merged:
            contexts[key] = dict(merged)
            changed = True

    if changed:
        save_contexts(tenant_root, contexts)
    return merged


__all__ = [
    "contexts_path",
    "load_contexts",
    "save_contexts",
    "record_publication",
]
