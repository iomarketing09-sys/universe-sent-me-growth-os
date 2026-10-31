#!/usr/bin/env python3
"""Backfill de métricas lifetime actuales para posts históricos de Universe.

No reconstruye E0/E24/E72: Meta solo entrega el acumulado actual de estas
métricas. Las filas se guardan con ``window=LIFETIME_BACKFILL`` para que no se
confundan con una captura hecha en la ventana original.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional

import requests

METRICS_DIR = Path(__file__).resolve().parent
TENANT_DIR = METRICS_DIR.parent
REPO_ROOT = Path(__file__).resolve().parents[3]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.intelligence.metrics_snapshot import (  # noqa: E402
    MetricsSnapshot,
    SnapshotStatus,
    api_get,
    capture_post_insights,
    load_snapshot_log,
    save_snapshot_log,
)

TENANT_ID = TENANT_DIR.name
ROOT_ENV_PATH = REPO_ROOT / ".env"
TENANT_ENV_PATH = TENANT_DIR / ".env"


def load_env() -> Dict[str, str]:
    env: Dict[str, str] = {}
    for path in (ROOT_ENV_PATH, TENANT_ENV_PATH):
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.replace("export ", "").strip()] = value.strip().strip("'\"")
    return env


def get_page_token(user_token: str, page_id: str) -> Optional[str]:
    if not user_token or not page_id:
        return None
    try:
        response = requests.get(
            f"https://graph.facebook.com/v26.0/{page_id}",
            params={"fields": "access_token", "access_token": user_token},
            timeout=20,
        )
        if response.status_code == 200:
            return response.json().get("access_token") or user_token
    except requests.RequestException:
        pass
    return user_token


def as_int(value) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, dict):
        for key in ("value", "total_count", "count"):
            if key in value:
                return as_int(value[key])
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return 0


def facebook_post_ids(snapshots: Iterable[MetricsSnapshot]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for snapshot in snapshots:
        post_id = (snapshot.publication_id or "").strip()
        if snapshot.platform != "Facebook" or not post_id or post_id in seen:
            continue
        seen.add(post_id)
        result.append(post_id)
    return result


def reaction_fields(value) -> Dict[str, int]:
    fields = {
        "like": "reaction_like",
        "love": "reaction_love",
        "wow": "reaction_wow",
        "haha": "reaction_haha",
        "sorry": "reaction_sorry",
        "sad": "reaction_sorry",
        "anger": "reaction_anger",
        "angry": "reaction_anger",
        "care": "reaction_care",
    }
    if not isinstance(value, dict):
        return {}
    result: Dict[str, int] = {}
    for key, raw in value.items():
        target = fields.get(str(key).lower())
        if target:
            result[target] = as_int(raw)
    return result


def build_backfill_snapshot(page_token: str, post_id: str, now_iso: str) -> MetricsSnapshot:
    counts = api_get(page_token, post_id, {
        "fields": "reactions.limit(0).summary(true),comments.limit(0).summary(true),shares"
    })
    insights = capture_post_insights(page_token, post_id)
    insights_available = any(not key.startswith("_") for key in insights)

    reactions = as_int((counts.get("reactions") or {}).get("summary", {}).get("total_count", 0))
    comments = as_int((counts.get("comments") or {}).get("summary", {}).get("total_count", 0))
    shares = as_int((counts.get("shares") or {}).get("count", 0))
    unavailable = insights.get("_unavailable_metrics", "")
    reasons = insights.get("_unavailable_reasons", {}) or {}
    unavailable_text = ",".join(
        part for part in (
            unavailable,
            ", ".join(f"{metric}:{why}" for metric, why in reasons.items()),
        ) if part
    )

    snapshot = MetricsSnapshot(
        snapshot_id="SNAP-BF-" + hashlib.sha1(post_id.encode("utf-8")).hexdigest()[:12].upper(),
        publication_id=post_id,
        tenant_id=TENANT_ID,
        platform="Facebook",
        window="LIFETIME_BACKFILL",
        target_at_utc=now_iso,
        captured_at_utc=now_iso,
        reactions=reactions,
        comments=comments,
        shares=shares,
        total_interactions=reactions + comments + shares,
        clicks=as_int(insights.get("post_clicks", 0)),
        video_views=as_int(insights.get("post_video_views", 0)),
        video_watch_time=as_int(insights.get("post_video_avg_time_watched", 0)),
        status=SnapshotStatus.CAPTURED.value,
        unavailable_metrics=unavailable_text,
        insights_available=insights_available,
        created_at=now_iso,
    )
    for field, value in reaction_fields(insights.get("post_reactions_by_type_total")).items():
        setattr(snapshot, field, value)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None, help="Máximo de posts a procesar")
    parser.add_argument("--dry-run", action="store_true", help="Consultar Meta sin escribir el ledger")
    args = parser.parse_args()

    env = load_env()
    page_id = env.get("FB_PAGE_ID") or env.get("META_PAGE_ID")
    user_token = env.get("META_ACCESS_TOKEN") or env.get("PAGE_ACCESS_TOKEN")
    if not page_id or not user_token:
        print("Faltan FB_PAGE_ID/META_ACCESS_TOKEN en .env", file=sys.stderr)
        return 1

    page_token = get_page_token(user_token, page_id)
    if not page_token:
        print("No se pudo obtener token de página", file=sys.stderr)
        return 1

    existing = {snap.snapshot_id: snap for snap in load_snapshot_log(TENANT_ID)}
    post_ids = facebook_post_ids(existing.values())
    if args.limit is not None:
        post_ids = post_ids[:args.limit]

    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    created = 0
    for index, post_id in enumerate(post_ids, start=1):
        snapshot = build_backfill_snapshot(page_token, post_id, now_iso)
        existing[snapshot.snapshot_id] = snapshot
        created += 1
        if index % 10 == 0 or index == len(post_ids):
            print(f"backfill: {index}/{len(post_ids)}")

    if args.dry_run:
        print(f"dry-run: {created} snapshots LIFETIME_BACKFILL listos, sin escribir")
        return 0

    save_snapshot_log(
        TENANT_ID,
        sorted(existing.values(), key=lambda snap: (snap.captured_at_utc, snap.snapshot_id)),
    )
    print(f"backfill: {created} snapshots LIFETIME_BACKFILL escritos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
