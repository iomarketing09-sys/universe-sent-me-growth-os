"""Vista de revisión de propuestas nuevas, sin publicar ni aprobar nada."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from modules.communications.comments.log import read_comment_log, write_json_atomic
from modules.communications.comments.paths import CommentPaths
from modules.communications.comments.review import load_approvals
from modules.communications.review_report import generate_review_files


def _is_review_candidate(item: Dict[str, Any]) -> bool:
    if item.get("approved") is True:
        return False
    if item.get("published") is True or str(item.get("reply_id") or "").strip():
        return False
    if item.get("discarded") is True:
        return False
    if item.get("publish_status") in {"already_replied", "published", "already_published"}:
        return False
    if item.get("decision") in {"already_replied", "already_published"}:
        return False
    return True


def _answered_comment_ids(comments_log_file: Path) -> set[str]:
    latest: Dict[str, str] = {}
    for row in read_comment_log(comments_log_file):
        comment_id = str(row.get("comment_id") or "").strip()
        if comment_id:
            latest[comment_id] = str(row.get("publish_status") or "").strip()
    return {
        comment_id
        for comment_id, status in latest.items()
        if status in {"already_replied", "published", "already_published"}
    }


def build_new_proposals_queue(
    tenant_id: str,
    base_path: Optional[Path] = None,
    *,
    output_file: Optional[Path] = None,
    markdown_path: Optional[Path] = None,
    csv_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Crea una vista de solo lectura con las propuestas aún no revisadas.

    La fuente de verdad sigue siendo ``aprobaciones.json``. Esta vista no se
    usa para publicar: sirve para revisar en chat y decidir qué aprobar.
    """
    paths = CommentPaths.for_tenant(tenant_id, base_path)
    master_path = paths.approvals_file
    payload = load_approvals(master_path)
    if payload is None:
        raise FileNotFoundError(f"No existe {master_path}")

    source_items = payload.get("approvals") or []
    if not isinstance(source_items, list):
        raise ValueError("'approvals' debe ser una lista")

    answered = _answered_comment_ids(paths.comments_log_file)
    candidates = [
        dict(item)
        for item in source_items
        if isinstance(item, dict)
        and _is_review_candidate(item)
        and str(item.get("comment_id") or "").strip() not in answered
    ]
    output_path = (
        Path(output_file)
        if output_file
        else paths.storage_dir / "aprobaciones_nuevas.json"
    )
    markdown_output = (
        Path(markdown_path)
        if markdown_path
        else paths.storage_dir / "reports" / "nuevas_pendientes.md"
    )
    csv_output = (
        Path(csv_path)
        if csv_path
        else paths.storage_dir / "reports" / "nuevas_pendientes.csv"
    )

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(master_path),
        "kind": "review_queue",
        "total_pending": len(candidates),
        "total_approved": 0,
        "instructions": (
            "Vista de propuestas nuevas sin aprobar. Revisar en chat; "
            "marcar approved: true en aprobaciones.json solo después de aprobar."
        ),
        "approvals": candidates,
    }
    write_json_atomic(output_path, snapshot)
    report = generate_review_files(
        output_path,
        markdown_path=markdown_output,
        csv_path=csv_output,
    )
    return {
        "queue_file": str(output_path),
        "markdown": report["markdown"],
        "csv": report["csv"],
        "items": len(candidates),
        "without_response": sum(
            1
            for item in candidates
            if not str(item.get("approved_response") or "").strip()
        ),
    }
