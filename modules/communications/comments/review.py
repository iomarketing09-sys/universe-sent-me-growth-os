"""Lectura local de la bandeja de comentarios para revisión humana."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from modules.communications.comments.log import read_comment_log
from modules.communications.comments.paths import CommentPaths


def load_approvals(path: Path) -> Dict[str, Any] | None:
    """Lee aprobaciones; no crea ni repara archivos."""
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"aprobaciones.json inválido: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("aprobaciones.json debe contener un objeto")
    return payload


def _approval_stats(items: list[Dict[str, Any]]) -> Dict[str, Any]:
    approved = [item for item in items if item.get("approved") is True]
    published = [
        item
        for item in items
        if item.get("published") is True or str(item.get("reply_id") or "").strip()
    ]
    pending = [
        item
        for item in approved
        if str(item.get("approved_response") or "").strip()
        and item.get("published") is not True
        and not str(item.get("reply_id") or "").strip()
    ]
    approved_without_response = [
        item
        for item in approved
        if not str(item.get("approved_response") or "").strip()
        and item.get("published") is not True
        and not str(item.get("reply_id") or "").strip()
    ]
    discarded = [item for item in items if item.get("discarded") is True]
    review_pending = [
        item
        for item in items
        if item.get("approved") is not True
        and item.get("discarded") is not True
        and item.get("published") is not True
        and not str(item.get("reply_id") or "").strip()
    ]
    errors = [item for item in items if str(item.get("last_error") or "").strip()]
    return {
        "total": len(items),
        "approved": len(approved),
        "approved_pending": len(pending),
        "approved_without_response": len(approved_without_response),
        "not_approved": len(items) - len(approved),
        "discarded": len(discarded),
        "review_pending": len(review_pending),
        "published": len(published),
        "errors": len(errors),
        "pending_comment_ids": [str(item.get("comment_id") or "") for item in pending],
    }


def _log_stats(rows: list[Dict[str, str]]) -> Dict[str, Any]:
    latest: Dict[str, Dict[str, str]] = {}
    for row in rows:
        comment_id = str(row.get("comment_id") or "")
        if comment_id:
            latest[comment_id] = row
    missing_meme = [
        comment_id
        for comment_id, row in latest.items()
        if row.get("publish_status") == "sin_contexto"
    ]
    return {
        "rows": len(rows),
        "pending_approval": sum(row.get("publish_status") == "pending_approval" for row in rows),
        "published": sum(row.get("publish_status") == "published" for row in rows),
        "already_published": sum(row.get("publish_status") == "already_published" for row in rows),
        "discarded": sum(row.get("publish_status") == "discarded" for row in rows),
        "already_replied": sum(row.get("publish_status") == "already_replied" for row in rows),
        "sin_contexto": len(missing_meme),
        "sin_contexto_comment_ids": missing_meme,
    }


def inbox_snapshot(
    tenant_id: str,
    base_path: Optional[Path] = None,
    storage_dir: Optional[Path] = None,
    approvals_file: Optional[Path] = None,
) -> Dict[str, Any]:
    """Resume aprobaciones y log local sin red ni escrituras."""
    paths = CommentPaths.for_tenant(tenant_id, base_path, storage_dir)
    approval_path = Path(approvals_file) if approvals_file else paths.approvals_file
    payload = load_approvals(approval_path)
    approvals = [] if payload is None else payload.get("approvals") or []
    if not isinstance(approvals, list):
        raise ValueError("'approvals' debe ser una lista")

    stats = _approval_stats([item for item in approvals if isinstance(item, dict)])
    return {
        "tenant_id": tenant_id,
        "configured": payload is not None,
        "storage_dir": str(paths.storage_dir),
        "approvals_file": str(approval_path),
        "kind": None if payload is None else payload.get("kind"),
        "source": None if payload is None else payload.get("source"),
        "comments_log_file": str(paths.comments_log_file),
        "generated_at": None if payload is None else payload.get("generated_at"),
        "reviewed_at": None if payload is None else payload.get("reviewed_at"),
        "lookback_hours": None if payload is None else payload.get("lookback_hours"),
        "approvals": stats,
        "comments_log": _log_stats(read_comment_log(paths.comments_log_file)),
    }


def review_comments(
    tenant_id: str,
    base_path: Optional[Path] = None,
    storage_dir: Optional[Path] = None,
    approvals_file: Optional[Path] = None,
) -> Dict[str, Any]:
    """Alias de fachada para la revisión local de comentarios."""
    return inbox_snapshot(tenant_id, base_path, storage_dir, approvals_file)
