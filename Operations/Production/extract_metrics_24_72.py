#!/usr/bin/env python3
"""Extract and record 24/72-hour metric-window evidence for USM.

The script processes all due Facebook publications in one run. It never
publishes content and never touches Instagram. Lifetime interaction totals
returned by Graph API are evidence only; they are not written into 24h/72h
fields unless an exact time-bounded payload is available.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

REPO = Path(os.environ.get("USM_GROWTH_OS_REPO", "/home/ubuntu/universe-sent-me-growth-os"))
PUBLICATION_LOG = REPO / "Operations/Research/2026-08-15_Publication_Log.csv"
EXPERIMENT_LOG = REPO / "Operations/Research/2026-08-15_ExperimentLog.csv"
DEFAULT_EVIDENCE = REPO / "Operations/Research/2026-08-16_Metricas_24_72_Extraccion.json"
GRAPH_BASE = "https://graph.facebook.com/v26.0"
PAGE_ID = "1036844829507460"
EXPERIMENT_ID = "EXP-2026-08-CAL-01"
LOCAL_TZ = ZoneInfo("America/Matamoros")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Evaluate due rows and write evidence without API calls or ledger updates.")
    parser.add_argument("--now", help="Override current time with an ISO-8601 timestamp for deterministic testing.")
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE, help="Evidence JSON output path.")
    parser.add_argument("--run-id", help="Stable idempotency marker; defaults to the current UTC timestamp.")
    return parser.parse_args()


def parse_now(value: str | None) -> datetime:
    if value:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def parse_publication_time(row: dict[str, str]) -> datetime | None:
    date_value = (row.get("Fecha_Publicacion_Local") or "").strip()
    time_value = (row.get("Hora_Publicacion_Local") or "").strip()
    if not date_value or not time_value:
        return None
    try:
        parsed = datetime.fromisoformat(f"{date_value}T{time_value}")
    except ValueError:
        return None
    return parsed.replace(tzinfo=LOCAL_TZ).astimezone(timezone.utc)


def due_windows(row: dict[str, str], now: datetime) -> tuple[datetime | None, list[str], float | None]:
    published = parse_publication_time(row)
    if published is None:
        return None, [], None
    age_seconds = (now - published).total_seconds()
    due: list[str] = []
    notes = row.get("Notas", "") or ""
    if age_seconds >= 24 * 3600 and not (row.get("Interacciones_24h") or "").strip() and "24h_snapshot_unavailable" not in notes:
        due.append("24h")
    if age_seconds >= 72 * 3600 and not (row.get("Interacciones_72h") or "").strip() and "72h_snapshot_unavailable" not in notes:
        due.append("72h")
    return published, due, age_seconds / 3600


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if not reader.fieldnames:
            raise RuntimeError(f"Missing CSV header: {path}")
        return rows, list(reader.fieldnames)


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def count_from_summary(obj: Any) -> int | None:
    if not isinstance(obj, dict):
        return None
    summary = obj.get("summary")
    if isinstance(summary, dict) and isinstance(summary.get("total_count"), (int, float)):
        return int(summary["total_count"])
    return None


def derive_page_headers(user_token: str) -> tuple[dict[str, str], dict[str, Any]]:
    user_headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(
        f"{GRAPH_BASE}/me/accounts",
        headers=user_headers,
        params={"fields": "id,name,access_token", "limit": 100},
        timeout=30,
    )
    response.raise_for_status()
    page = next((item for item in response.json().get("data", []) if item.get("id") == PAGE_ID), None)
    if not page or not page.get("access_token"):
        raise RuntimeError("Page Access Token for Universe Sent Me was not derivable")
    return {"Authorization": f"Bearer {page['access_token']}"}, {
        "page_id": page.get("id"),
        "page_name": page.get("name"),
        "status_code": response.status_code,
    }


def query_lifetime_totals(meta_id: str, page_headers: dict[str, str]) -> dict[str, Any]:
    fields = "created_time,reactions.limit(0).summary(true),comments.limit(0).summary(true),shares"
    response = requests.get(
        f"{GRAPH_BASE}/{meta_id}",
        headers=page_headers,
        params={"fields": fields},
        timeout=30,
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw_text": response.text}
    reactions = count_from_summary(payload.get("reactions")) if isinstance(payload, dict) else None
    comments = count_from_summary(payload.get("comments")) if isinstance(payload, dict) else None
    shares = payload.get("shares", {}).get("count") if isinstance(payload, dict) and isinstance(payload.get("shares"), dict) else None
    values = [value for value in (reactions, comments, shares) if isinstance(value, int)]
    return {
        "http_status": response.status_code,
        "payload": payload,
        "lifetime_totals": {
            "reactions": reactions,
            "comments": comments,
            "shares": shares,
            "interactions": sum(values) if values else None,
        },
        "exact_window_available": False,
        "window_note": "Meta response contains current lifetime totals only; no exact 24h/72h snapshot written.",
    }


def append_marker(existing: str, marker: str) -> str:
    if marker in existing:
        return existing
    return f"{existing.rstrip()} {marker}".strip()


def update_ledgers(
    publication_rows: list[dict[str, str]],
    experiment_rows: list[dict[str, str]],
    due_by_publication: dict[str, list[str]],
    evidence_by_publication: dict[str, dict[str, Any]],
    run_id: str,
    extracted_at: str,
) -> None:
    marker = f"[METRICS-RUN:{run_id}]"
    publication_by_id = {row.get("Publicacion_ID"): row for row in publication_rows}
    for publicacion_id, windows in due_by_publication.items():
        evidence = evidence_by_publication.get(publicacion_id, {})
        row = publication_by_id[publicacion_id]
        unavailable_markers = " ".join(f"{window}_snapshot_unavailable" for window in windows if not evidence.get("exact_window_available", False))
        note = f"{marker} {extracted_at}: {','.join(windows)} due; {unavailable_markers}; {evidence.get('window_note', 'no exact window')}"
        row["Notas"] = append_marker(row.get("Notas", ""), note)

    for row in experiment_rows:
        publicacion_id = row.get("Observacion_ID", "")
        if not publicacion_id.startswith("OBS-FB-15_16-"):
            continue
        windows = due_by_publication.get(publicacion_id.replace("OBS-FB-", "PUB-FB-"), [])
        if not windows:
            continue
        evidence = evidence_by_publication.get(publicacion_id.replace("OBS-FB-", "PUB-FB-"), {})
        unavailable_markers = " ".join(f"{window}_snapshot_unavailable" for window in windows if not evidence.get("exact_window_available", False))
        note = f"{marker} {extracted_at}: {','.join(windows)} due; {unavailable_markers}; {evidence.get('window_note', 'no exact window')}"
        row["Conclusion"] = append_marker(row.get("Conclusion", ""), note)


def main() -> int:
    args = parse_args()
    now = parse_now(args.now)
    extracted_at = now.isoformat()
    run_id = args.run_id or now.strftime("%Y%m%dT%H%M%SZ")

    publication_rows, publication_fields = read_csv(PUBLICATION_LOG)
    experiment_rows, experiment_fields = read_csv(EXPERIMENT_LOG)
    candidates: list[dict[str, Any]] = []
    due_by_publication: dict[str, list[str]] = {}

    for row in publication_rows:
        if row.get("Plataforma") != "Facebook" or row.get("Experiment_ID") != EXPERIMENT_ID or not row.get("Meta_Post_ID"):
            continue
        published, due, age_hours = due_windows(row, now)
        if published is None:
            continue
        candidate = {
            "publicacion_id": row.get("Publicacion_ID"),
            "id_pieza": row.get("ID_Pieza"),
            "meta_post_id": row.get("Meta_Post_ID"),
            "published_at_utc": published.isoformat(),
            "due_windows": due,
            "age_hours": round(age_hours or 0, 3),
        }
        candidates.append(candidate)
        if due:
            due_by_publication[row["Publicacion_ID"]] = due

    evidence_by_publication: dict[str, dict[str, Any]] = {}
    responses: list[dict[str, Any]] = []
    page_context: dict[str, Any] | None = None
    if due_by_publication and not args.dry_run:
        token = os.environ.get("META_PAGE_ACCESS_TOKEN")
        if not token:
            raise SystemExit("META_PAGE_ACCESS_TOKEN is required when due windows exist")
        page_headers, page_context = derive_page_headers(token)
        for candidate in candidates:
            if not candidate["due_windows"]:
                continue
            result = query_lifetime_totals(candidate["meta_post_id"], page_headers)
            candidate["evidence"] = result
            evidence_by_publication[candidate["publicacion_id"]] = result
            responses.append({
                "publicacion_id": candidate["publicacion_id"],
                "id_pieza": candidate["id_pieza"],
                "meta_post_id": candidate["meta_post_id"],
                **result,
            })
    elif due_by_publication:
        for candidate in candidates:
            if candidate["due_windows"]:
                candidate["evidence"] = {
                    "exact_window_available": False,
                    "window_note": "Dry run: no API request and no ledger update.",
                }

    exact_window_writes = 0
    if due_by_publication and not args.dry_run:
        update_ledgers(publication_rows, experiment_rows, due_by_publication, evidence_by_publication, run_id, extracted_at)
        write_csv(PUBLICATION_LOG, publication_rows, publication_fields)
        write_csv(EXPERIMENT_LOG, experiment_rows, experiment_fields)

    result = {
        "extracted_at_utc": extracted_at,
        "extracted_at_local": now.astimezone(LOCAL_TZ).isoformat(),
        "timezone": str(LOCAL_TZ),
        "experiment_id": EXPERIMENT_ID,
        "definition": "Only exact time-bounded 24h/72h snapshots may populate metric fields. Current lifetime totals are retained as evidence and never substituted into window fields.",
        "single_wakeup_batch": True,
        "instagram_touched": False,
        "content_published": False,
        "candidate_count": len(candidates),
        "eligible_count": len(due_by_publication),
        "exact_window_writes": exact_window_writes,
        "ledger_updates": bool(due_by_publication and not args.dry_run),
        "page_context": page_context,
        "candidates": candidates,
        "responses": responses,
        "status": "dry_run" if args.dry_run else ("extracted_lifetime_only" if due_by_publication else "no_eligible_windows"),
        "run_id": run_id,
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("extracted_at_utc", "candidate_count", "eligible_count", "exact_window_writes", "status")}, ensure_ascii=False))
    for candidate in candidates:
        print(candidate["publicacion_id"], candidate["id_pieza"], "due=" + (",".join(candidate["due_windows"]) or "none"), "age_hours=" + str(candidate["age_hours"]))
    print("evidence_file=" + str(args.evidence))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
