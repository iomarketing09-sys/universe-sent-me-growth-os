#!/usr/bin/env python3
"""Sincroniza el publication log de Universe con Meta.

El scheduler de ventanas necesita un registro de publicaciones reales para
programar E0/E24/E72. Este script no captura métricas: solo descubre posts de
Facebook e Instagram y los fusiona en ``publication_log_week2.csv``.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from zoneinfo import ZoneInfo

import requests

METRICS_DIR = Path(__file__).resolve().parent
TENANT_DIR = METRICS_DIR.parent
REPO_ROOT = Path(__file__).resolve().parents[3]

TENANT_ID = TENANT_DIR.name
ROOT_ENV_PATH = REPO_ROOT / ".env"
TENANT_ENV_PATH = TENANT_DIR / ".env"
LOG_PATH = TENANT_DIR / "publication_log_week2.csv"
IMPORT_LOG_PATH = TENANT_DIR / "imports" / "publication_log_week2.csv"

LOG_FIELDS = [
    "date", "time", "platform", "piece", "asset_filename",
    "status", "publication_id", "published_at", "reach",
    "interactions", "DMs", "leads",
]


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
            params={"fields": "access_token,instagram_business_account", "access_token": user_token},
            timeout=20,
        )
        if response.status_code == 200:
            payload = response.json()
            return payload.get("access_token") or user_token
    except requests.RequestException:
        pass
    return user_token


def parse_meta_datetime(value: str) -> Optional[datetime]:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def local_slot(value: str) -> tuple[str, str, str]:
    parsed = parse_meta_datetime(value)
    if parsed is None:
        return "", "", ""
    local = parsed.astimezone(ZoneInfo("America/Matamoros"))
    return local.strftime("%Y-%m-%d"), local.strftime("%H:%M"), parsed.isoformat(timespec="seconds")


def read_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def fetch_facebook_posts(page_token: str, page_id: str) -> List[Dict[str, str]]:
    response = requests.get(
        f"https://graph.facebook.com/v26.0/{page_id}/posts",
        params={
            "fields": "id,created_time,message,permalink_url",
            "limit": 100,
            "access_token": page_token,
        },
        timeout=30,
    )
    if response.status_code >= 400:
        print(f"Facebook: {response.status_code} {response.text[:300]}", file=sys.stderr)
        return []

    rows = []
    for post in response.json().get("data", []):
        date, time, published_at = local_slot(post.get("created_time", ""))
        if not date or not time:
            continue
        rows.append({
            "date": date,
            "time": time,
            "platform": "Facebook",
            "piece": (post.get("message") or "").replace("\n", " ")[:80],
            "asset_filename": "",
            "status": "published",
            "publication_id": post.get("id", ""),
            "published_at": published_at,
            "reach": "",
            "interactions": "",
            "DMs": "",
            "leads": "",
        })
    return rows


def fetch_instagram_media(page_token: str, user_token: str, page_id: str) -> List[Dict[str, str]]:
    response = requests.get(
        f"https://graph.facebook.com/v26.0/{page_id}",
        params={"fields": "instagram_business_account", "access_token": user_token},
        timeout=30,
    )
    if response.status_code >= 400:
        print(f"Instagram account: {response.status_code} {response.text[:300]}", file=sys.stderr)
        return []
    ig_id = (response.json().get("instagram_business_account") or {}).get("id")
    if not ig_id:
        return []

    response = requests.get(
        f"https://graph.facebook.com/v26.0/{ig_id}/media",
        params={
            "fields": "id,caption,timestamp,media_type,permalink",
            "limit": 50,
            "access_token": page_token,
        },
        timeout=30,
    )
    if response.status_code >= 400:
        print(f"Instagram media: {response.status_code} {response.text[:300]}", file=sys.stderr)
        return []

    rows = []
    for media in response.json().get("data", []):
        date, time, published_at = local_slot(media.get("timestamp", ""))
        if not date or not time:
            continue
        rows.append({
            "date": date,
            "time": time,
            "platform": "Instagram",
            "piece": (media.get("caption") or "").replace("\n", " ")[:80],
            "asset_filename": "",
            "status": "published",
            "publication_id": media.get("id", ""),
            "published_at": published_at,
            "reach": "",
            "interactions": "",
            "DMs": "",
            "leads": "",
        })
    return rows


def merge_rows(existing: Iterable[Dict[str, str]], incoming: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    merged: Dict[str, Dict[str, str]] = {}
    order: List[str] = []
    for row in [*existing, *incoming]:
        publication_id = (row.get("publication_id") or "").strip()
        key = publication_id or f"{row.get('date')}|{row.get('time')}|{row.get('asset_filename')}"
        if key not in merged:
            order.append(key)
            merged[key] = {field: row.get(field, "") or "" for field in LOG_FIELDS}
            continue
        for field in LOG_FIELDS:
            current = merged[key].get(field, "")
            incoming = row.get(field, "") or ""
            if not current and incoming:
                merged[key][field] = incoming
            elif (
                field == "status"
                and current.strip().lower() != "published"
                and incoming.strip().lower() == "published"
            ):
                merged[key][field] = incoming
    rows = [merged[key] for key in order]
    return sorted(rows, key=lambda row: (row.get("date", ""), row.get("time", ""), row.get("platform", "")))


def write_rows(rows: List[Dict[str, str]]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sync_publication_log(dry_run: bool = False) -> int:
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

    existing = read_rows(LOG_PATH) or read_rows(IMPORT_LOG_PATH)
    incoming = fetch_facebook_posts(page_token, page_id) + fetch_instagram_media(page_token, user_token, page_id)
    merged = merge_rows(existing, incoming)

    if dry_run:
        print(f"dry-run: {len(merged)} publicaciones en el log ({len(existing)} existentes, {len(incoming)} desde Meta)")
        return 0

    write_rows(merged)
    print(f"publication log: {len(merged)} publicaciones ({len(existing)} existentes, {len(incoming)} desde Meta)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Consultar Meta sin escribir el log")
    args = parser.parse_args()
    return sync_publication_log(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
