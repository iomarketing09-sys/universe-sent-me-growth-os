#!/usr/bin/env python3
"""Publica respuestas de comentarios ya aprobadas, fuera del chat.

El worker no captura comentarios, no genera propuestas y no cambia
``approved``. Solo procesa la cola maestra y lotes de publicación explícitos.
El candado evita que dos ejecuciones (timer + manual) publiquen a la vez. La
cola local es la única fuente de verdad: no se copia a Drive ni a otra ruta.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.cgo.orchestrator import CgoOrchestrator
from modules.cgo.result import BLOCKED, ERROR
from modules.communications.comments.paths import CommentPaths


READ_ONLY_KINDS = {"review_queue"}


def load_queue(path: Path) -> Optional[Dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("approvals"), list):
        return None
    return payload


def pending_approvals(payload: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if payload is None or payload.get("kind") in READ_ONLY_KINDS:
        return []
    return [
        item
        for item in payload.get("approvals", [])
        if isinstance(item, dict)
        and item.get("approved") is True
        and str(item.get("approved_response") or "").strip()
        and item.get("published") is not True
        and not str(item.get("reply_id") or "").strip()
    ]


def queue_candidates(paths: CommentPaths) -> List[Path]:
    """Devuelve solo la cola maestra y lotes publicables explícitos.

    Las vistas de revisión y los lotes cerrados nunca se publican. Los lotes
    publicables deben llamarse ``aprobaciones_publish_*.json`` y declarar
    ``kind: publish_batch``; así un archivo viejo no se ejecuta por accidente.
    """
    candidates: List[Path] = [paths.approvals_file]
    for path in sorted(paths.storage_dir.glob("aprobaciones_publish_*.json")):
        payload = load_queue(path)
        if payload is None or payload.get("kind") != "publish_batch":
            continue
        candidates.append(path)
    return candidates


def acquire_lock(path: Path) -> Optional[TextIO]:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+", encoding="utf-8")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return None
    handle.seek(0)
    handle.truncate()
    handle.write(f"pid={os.getpid()}\n")
    handle.flush()
    return handle


def publish_queue(
    *,
    tenant_id: str,
    base_path: Path,
    queue_path: Path,
    batch_size: int,
    batch_pause_seconds: int,
) -> int:
    result = CgoOrchestrator(
        base_path=str(base_path),
        dry_run=False,
        publish=True,
        comments_batch_size=batch_size,
        comments_batch_pause_seconds=batch_pause_seconds,
        comments_approvals_file=queue_path,
    ).run_one("comments_review", tenant_id)

    print(f"[{result.status}] {queue_path.name}")
    for item in result.actions:
        print(f"  - {item.get('kind')}: {item.get('status')} · {item.get('detail')}")
    if result.reason:
        print(f"  reason: {result.reason}")
    if result.status in (BLOCKED, ERROR):
        return 1
    return int(result.data.get("publish_returncode") or 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publica en segundo plano las respuestas ya aprobadas."
    )
    parser.add_argument("--tenant", default="universe")
    parser.add_argument("--base-path", type=Path, default=ROOT)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--batch-pause-seconds", type=int, default=900)
    parser.add_argument(
        "--lock-file",
        type=Path,
        default=None,
        help="Candado exclusivo; por defecto vive en la carpeta de comentarios.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo muestra qué colas y cuántas respuestas publicaría.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.batch_size < 1:
        print("ERROR: --batch-size debe ser mayor que cero.")
        return 2
    if args.batch_pause_seconds < 0:
        print("ERROR: --batch-pause-seconds no puede ser negativo.")
        return 2

    base_path = Path(args.base_path).resolve()
    paths = CommentPaths.for_tenant(args.tenant, base_path)
    lock_path = args.lock_file or (paths.storage_dir / ".publish.lock")
    lock = acquire_lock(lock_path)
    if lock is None:
        print(f"⏭️ Otra publicación sigue activa ({lock_path}); no se inicia otra.")
        return 0

    try:
        candidates = queue_candidates(paths)

        failures = 0
        published_queues = 0
        for queue_path in candidates:
            payload = load_queue(queue_path)
            pending = pending_approvals(payload)
            if not pending:
                continue
            print(f"🚀 {queue_path.name}: {len(pending)} respuestas aprobadas pendientes.")
            published_queues += 1
            if args.dry_run:
                continue
            failures += int(
                publish_queue(
                    tenant_id=args.tenant,
                    base_path=base_path,
                    queue_path=queue_path,
                    batch_size=args.batch_size,
                    batch_pause_seconds=args.batch_pause_seconds,
                )
                != 0
            )

        if args.dry_run:
            print(f"Dry-run: {published_queues} cola(s) con trabajo pendiente.")
        elif published_queues == 0:
            print("Sin respuestas aprobadas pendientes.")
        return 1 if failures else 0
    finally:
        lock.close()


if __name__ == "__main__":
    raise SystemExit(main())
