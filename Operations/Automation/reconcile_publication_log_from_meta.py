#!/usr/bin/env python3
"""Safely reconcile local publication rows against a read-only Meta feed export."""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(os.environ.get("USM_GROWTH_OS_REPO", "/home/ubuntu/universe-sent-me-growth-os"))
DEFAULT_LOG = REPO / "Operations/Research/2026-08-15_Publication_Log.csv"
LOCAL_TZ = ZoneInfo("America/Matamoros")
ACTIVE_SCHEDULED = {"Programada", "Programada_Meta_Verificado"}


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    if len(text) >= 5 and text[-5] in "+-" and text[-3] != ":":
        text = text[:-2] + ":" + text[-2:]
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def append_note(value: str, marker: str) -> str:
    return value if marker in value else f"{value.rstrip()} {marker}".strip()


def load_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def atomic_write(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False, dir=path.parent, prefix=f".{path.name}.") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def build_plan(rows: list[dict[str, str]], feed: dict, now: datetime) -> dict:
    feed_by_id = {item.get("id"): item for item in feed.get("data", []) if item.get("id") and item.get("is_published") is True}
    rows_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("Plataforma") == "Facebook" and row.get("Meta_Post_ID", "").strip():
            rows_by_id[row["Meta_Post_ID"].strip()].append(row)
    cancelled_ids = {
        meta_id
        for meta_id, entries in rows_by_id.items()
        if any(entry.get("Estado_Publicacion", "").startswith("Cancelada") for entry in entries)
    }
    updates = []
    skipped = []
    for meta_id, entries in rows_by_id.items():
        if meta_id in cancelled_ids:
            continue
        meta = feed_by_id.get(meta_id)
        if not meta:
            continue
        for row in entries:
            if row.get("Estado_Publicacion") not in ACTIVE_SCHEDULED:
                continue
            created = parse_dt(meta.get("created_time"))
            if not created:
                skipped.append({"meta_post_id": meta_id, "reason": "feed_created_time_missing"})
                continue
            if created > now:
                skipped.append({"meta_post_id": meta_id, "reason": "feed_created_time_in_future"})
                continue
            local = created.astimezone(LOCAL_TZ)
            marker = f"[RECONCILIACION-META-FEED:{now.strftime('%Y%m%dT%H%M%SZ')}] is_published=true; created_time={created.isoformat()}"
            updates.append({
                "publicacion_id": row.get("Publicacion_ID", ""),
                "meta_post_id": meta_id,
                "from_state": row.get("Estado_Publicacion", ""),
                "to_state": "Publicado",
                "fecha_publicacion_local": local.date().isoformat(),
                "hora_publicacion_local": local.strftime("%H:%M:%S"),
                "marker": marker,
                "row": row,
            })
    return {"updates": updates, "skipped": skipped, "feed_published_ids": len(feed_by_id)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feed", type=Path, required=True)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--now", help="UTC timestamp used for deterministic markers")
    parser.add_argument("--apply", action="store_true", help="Apply only the safe planned updates")
    args = parser.parse_args()
    now = parse_dt(args.now) if args.now else datetime.now(timezone.utc)
    assert now is not None
    rows, fields = load_rows(args.log)
    feed = json.loads(args.feed.read_text(encoding="utf-8"))
    plan = build_plan(rows, feed, now)
    applied = []
    if args.apply:
        for item in plan["updates"]:
            row = item["row"]
            row["Estado_Publicacion"] = "Publicado"
            row["Eliminada"] = "No"
            row["Fecha_Publicacion_Local"] = item["fecha_publicacion_local"]
            row["Hora_Publicacion_Local"] = item["hora_publicacion_local"]
            row["Notas"] = append_note(row.get("Notas", ""), item["marker"])
            row["Fuente"] = append_note(row.get("Fuente", ""), "Meta Graph API feed read-only")
            applied.append({k: v for k, v in item.items() if k != "row"})
        if applied:
            atomic_write(args.log, rows, fields)
    report = {
        "status": "APPLIED" if args.apply else "DRY_RUN",
        "log": str(args.log),
        "feed": str(args.feed),
        "feed_published_ids": plan["feed_published_ids"],
        "planned_updates": [{k: v for k, v in item.items() if k != "row"} for item in plan["updates"]],
        "applied_updates": applied,
        "skipped": plan["skipped"],
        "safe_scope": "Only Facebook rows in Programada/Programada_Meta_Verificado with matching is_published=true feed record; cancelled Meta_Post_ID groups excluded.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
