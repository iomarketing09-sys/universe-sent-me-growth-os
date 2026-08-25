#!/usr/bin/env python3
"""Reconcile ExperimentLog publication states from the canonical publication ledger."""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(os.environ.get("USM_GROWTH_OS_REPO", "/home/ubuntu/universe-sent-me-growth-os"))
DEFAULT_PUBLICATION_LOG = REPO / "Operations/Research/2026-08-15_Publication_Log.csv"
DEFAULT_EXPERIMENT_LOG = REPO / "Operations/Research/2026-08-15_ExperimentLog.csv"


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


def build_plan(publication_rows: list[dict[str, str]], experiment_rows: list[dict[str, str]], now: datetime) -> list[dict[str, object]]:
    published_by_meta: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in publication_rows:
        meta_id = row.get("Meta_Post_ID", "").strip()
        if (
            row.get("Plataforma") == "Facebook"
            and meta_id
            and row.get("Estado_Publicacion") == "Publicado"
            and row.get("Eliminada", "No") != "Sí"
        ):
            published_by_meta[meta_id].append(row)
    marker = f"[RECONCILIACION-PUBLICATION-LOG:{now.strftime('%Y%m%dT%H%M%SZ')}] Estado_Publicacion confirmado como Publicado desde Publication_Log; no se modificaron métricas ni veredicto."
    plan = []
    for row in experiment_rows:
        meta_id = row.get("Meta_ID", "").strip()
        if row.get("Plataforma") != "Facebook" or not meta_id:
            continue
        if row.get("Estado_Publicacion") not in {"Programada", "Programada_Meta_Verificado"}:
            continue
        if meta_id not in published_by_meta:
            continue
        plan.append({
            "observacion_id": row.get("Observacion_ID", ""),
            "experiment_id": row.get("Experiment_ID", ""),
            "meta_id": meta_id,
            "from_state": row.get("Estado_Publicacion", ""),
            "to_state": "Publicado",
            "metrics_24h_before": row.get("Interacciones_24h", ""),
            "metrics_72h_before": row.get("Interacciones_72h", ""),
            "verdict_before": row.get("Veredicto", ""),
            "marker": marker,
            "row": row,
        })
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publication-log", type=Path, default=DEFAULT_PUBLICATION_LOG)
    parser.add_argument("--experiment-log", type=Path, default=DEFAULT_EXPERIMENT_LOG)
    parser.add_argument("--now", help="UTC timestamp used for deterministic markers")
    parser.add_argument("--apply", action="store_true", help="Apply safe state-only updates")
    args = parser.parse_args()
    now = parse_dt(args.now) if args.now else datetime.now(timezone.utc)
    assert now is not None
    publication_rows, _ = load_rows(args.publication_log)
    experiment_rows, experiment_fields = load_rows(args.experiment_log)
    plan = build_plan(publication_rows, experiment_rows, now)
    applied = []
    if args.apply:
        for item in plan:
            row = item["row"]
            row["Estado_Publicacion"] = "Publicado"
            row["Fuente"] = append_note(row.get("Fuente", ""), item["marker"])
            applied.append({k: v for k, v in item.items() if k != "row"})
        if applied:
            atomic_write(args.experiment_log, experiment_rows, experiment_fields)
    report = {
        "status": "APPLIED" if args.apply else "DRY_RUN",
        "publication_log": str(args.publication_log),
        "experiment_log": str(args.experiment_log),
        "planned_updates": [{k: v for k, v in item.items() if k != "row"} for item in plan],
        "applied_updates": applied,
        "safe_scope": "Only Facebook ExperimentLog rows in Programada/Programada_Meta_Verificado whose Meta_ID has a non-deleted Publicado row in Publication_Log; metrics and verdicts are unchanged.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
