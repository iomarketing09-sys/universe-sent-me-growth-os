#!/usr/bin/env python3
"""Run a read-only daily Meta metrics cut for Universe Sent Me.

The runner captures lifetime-observable counters for the local calendar day,
keeps Reels separate from image/post denominators, joins only by explicit
Meta_Post_ID in Publication_Log, and writes dated evidence files. It never
writes Metrics_Snapshot_Log.csv, Publication_Log.csv, ExperimentLog.csv, or
content on Meta.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

REPO = Path(os.environ.get("USM_GROWTH_OS_REPO", "/home/ubuntu/universe-sent-me-growth-os"))
PAGE_ID = "1036844829507460"
GRAPH_BASE = "https://graph.facebook.com/v26.0"
LOCAL_TZ = ZoneInfo("America/Matamoros")
PUBLICATION_LOG = REPO / "Operations/Research/2026-08-15_Publication_Log.csv"


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


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def local_iso(dt: datetime) -> str:
    return dt.astimezone(LOCAL_TZ).isoformat()


def counter(value: Any) -> int | None:
    if not isinstance(value, dict):
        return None
    summary = value.get("summary")
    if not isinstance(summary, dict):
        return None
    raw = summary.get("total_count")
    if isinstance(raw, bool):
        return None
    if isinstance(raw, (int, float)):
        return int(raw)
    if isinstance(raw, str) and raw.strip().isdigit():
        return int(raw.strip())
    return None


def shares_counter(value: Any) -> int | None:
    if isinstance(value, dict):
        raw = value.get("count")
    else:
        raw = value
    if isinstance(raw, bool):
        return None
    if isinstance(raw, (int, float)):
        return int(raw)
    if isinstance(raw, str) and raw.strip().isdigit():
        return int(raw.strip())
    return None


def interactions_known(record: dict[str, Any]) -> int:
    return sum(value for value in (record.get("reactions"), record.get("comments"), record.get("shares")) if isinstance(value, int))


def derive_page_token(user_token: str) -> str:
    response = requests.get(
        f"{GRAPH_BASE}/me/accounts",
        headers={"Authorization": f"Bearer {user_token}"},
        params={"fields": "id,access_token", "limit": 100},
        timeout=30,
    )
    response.raise_for_status()
    for account in response.json().get("data", []):
        if account.get("id") == PAGE_ID and account.get("access_token"):
            return str(account["access_token"])
    raise RuntimeError(f"Page token not found for page {PAGE_ID}")


def fetch_feed(page_token: str, start_utc: datetime, end_utc: datetime) -> dict[str, Any]:
    response = requests.get(
        f"{GRAPH_BASE}/{PAGE_ID}/feed",
        headers={"Authorization": f"Bearer {page_token}"},
        params={
            "fields": "id,message,created_time,updated_time,is_published,permalink_url,reactions.limit(0).summary(true),comments.limit(0).summary(true),shares",
            "since": iso(start_utc),
            "until": iso(end_utc),
            "limit": 100,
        },
        timeout=30,
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw_text": response.text}
    if response.status_code != 200:
        raise RuntimeError(f"Meta feed request failed with HTTP {response.status_code}: {payload}")
    return payload


def load_publications() -> dict[str, dict[str, str]]:
    with PUBLICATION_LOG.open(encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        return {row.get("Meta_Post_ID", ""): row for row in rows if row.get("Meta_Post_ID")}


def normalize_record(record: dict[str, Any], publications: dict[str, dict[str, str]], capture_utc: datetime) -> dict[str, Any]:
    meta_id = str(record.get("id", ""))
    created = parse_dt(str(record.get("created_time", "")))
    if created is None:
        raise RuntimeError(f"Meta record {meta_id} has no created_time")
    permalink = str(record.get("permalink_url", ""))
    fmt = "Reel" if "/reel/" in permalink else "Image_or_post"
    row = publications.get(meta_id, {})
    reactions = counter(record.get("reactions"))
    comments = counter(record.get("comments"))
    shares = shares_counter(record.get("shares"))
    normalized = {
        "date_local": created.astimezone(LOCAL_TZ).date().isoformat(),
        "time_local": created.astimezone(LOCAL_TZ).strftime("%H:%M:%S"),
        "content_type": fmt,
        "interactions": interactions_known({"reactions": reactions, "comments": comments, "shares": shares}),
        "reactions": reactions,
        "comments": comments,
        "shares": shares,
        "piece_id": row.get("ID_Pieza", ""),
        "asset_ref": row.get("Asset_Ref", ""),
        "meta_post_id": meta_id,
        "permalink_url": permalink,
        "join_status": "Publication_Log_Meta_Post_ID_match" if row else "Unmapped_Meta_Post_ID",
        "is_published": bool(record.get("is_published") is True),
        "observation_quality": "fresh/incomplete" if (capture_utc - created).total_seconds() < 900 else "observable_lifetime_at_capture",
        "family_character_note": row.get("Notas", "") if row else "No explicit Publication_Log mapping; no identity inferred",
        "publicacion_id": row.get("Publicacion_ID", ""),
        "experiment_id": row.get("Experiment_ID", ""),
        "hypothesis_id": row.get("Hypothesis_ID", ""),
        "planned_time_local": row.get("Hora_Planeada_Local", ""),
    }
    return normalized


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "date_local", "time_local", "content_type", "interactions", "reactions", "comments", "shares",
        "piece_id", "asset_ref", "meta_post_id", "permalink_url", "join_status", "is_published",
        "observation_quality", "family_character_note", "publicacion_id", "experiment_id", "hypothesis_id",
        "planned_time_local",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_format: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_format.setdefault(row["content_type"], []).append(row)
    summary: dict[str, Any] = {}
    for fmt, members in by_format.items():
        values = [int(row["interactions"]) for row in members]
        counter_totals = {
            field: sum(int(row[field]) for row in members if isinstance(row[field], int))
            for field in ("reactions", "comments", "shares")
        }
        summary[fmt] = {
            "publications": len(members),
            "interactions_known": sum(values),
            "mean_interactions_known": round(sum(values) / len(values), 2) if values else None,
            "median_interactions_known": (sum(sorted(values)[len(values) // 2 - 1:len(values) // 2 + 1]) / 2) if values and len(values) % 2 == 0 else (sorted(values)[len(values) // 2] if values else None),
            "reactions_known": counter_totals["reactions"],
            "comments_known": counter_totals["comments"],
            "shares_known": counter_totals["shares"],
            "fresh_or_incomplete": sum(row["observation_quality"] == "fresh/incomplete" for row in members),
        }
    return summary


def write_analysis(path: Path, *, capture_local: datetime, capture_utc: datetime, start_local: datetime, end_local: datetime, rows: list[dict[str, Any]], raw_path: str) -> dict[str, Any]:
    formats = aggregate(rows)
    top = sorted(rows, key=lambda row: int(row["interactions"]), reverse=True)
    analysis = {
        "title": "Corte diario de métricas de Meta — 22:00 local",
        "purpose": "Registrar acumulados observables del feed real, separar formatos y alimentar una actualización descriptiva del Growth OS sin sustituir snapshots E24/E72.",
        "status": "Active",
        "created": capture_local.date().isoformat(),
        "updated": capture_local.date().isoformat(),
        "version": "1.0",
        "author": "Manus AI (CGO)",
        "organization": "Operations/Research",
        "captured_at_local": local_iso(capture_local),
        "captured_at_utc": iso(capture_utc),
        "window_start_local": local_iso(start_local),
        "window_end_local": local_iso(end_local),
        "window_start_utc": iso(start_local),
        "window_end_utc": iso(end_local),
        "source": "Meta Graph API v26 / Page feed",
        "raw_evidence_path": raw_path,
        "records_returned": len(rows),
        "published_records": sum(row["is_published"] is True for row in rows),
        "unmapped_records": sum(row["join_status"] != "Publication_Log_Meta_Post_ID_match" for row in rows),
        "formats": formats,
        "top_by_interactions_known": top[:10],
        "interpretation_rules": [
            "All counters are lifetime-observable totals at capture time, not exact 24-hour increments.",
            "Reels remain a separate denominator and are not combined with image/post conclusions.",
            "Unmapped Meta_Post_ID values are reported without inferring CNT, character, family, or experiment.",
            "This cut does not write Metrics_Snapshot_Log.csv, Publication_Log.csv, or ExperimentLog.csv.",
        ],
        "growth_update": {
            "performed_in_same_run": True,
            "mode": "descriptive_draft",
            "can_close_hypotheses": False,
            "can_write_e24_e72": False,
            "recommendation": "Use the observed ranking and format-separated signals as a draft input for Growth OS review; require valid E0/E24/E72 for contractual experiment learning.",
        },
    }
    path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return analysis


def write_markdown(path: Path, analysis: dict[str, Any], rows: list[dict[str, Any]], related: list[str]) -> None:
    lines = [
        "---",
        f'title: "{analysis["title"]}"',
        f'purpose: "{analysis["purpose"]}"',
        f'status: {analysis["status"]}',
        f'created: {analysis["created"]}',
        f'updated: {analysis["updated"]}',
        f'version: "{analysis["version"]}"',
        f'author: "{analysis["author"]}"',
        "related_documents:",
    ]
    lines.extend(f'  - "{item}"' for item in related)
    lines.extend(["organization: \"Operations/Research\"", "---", "", "# Alcance del corte", ""])
    lines.append(f'El corte se realizó el **{analysis["captured_at_local"]}** en `America/Matamoros`, con una ventana desde **{analysis["window_start_local"]}** hasta **{analysis["window_end_local"]}**. Meta devolvió **{analysis["records_returned"]} publicaciones**, de las cuales **{analysis["published_records"]}** están confirmadas como publicadas.')
    lines.append("Las cifras son acumulados lifetime observables al momento de la consulta; no representan incrementos exactos de 24 horas ni sustituyen los snapshots contractuales E0/E24/E72.")
    lines.extend(["", "## Resumen por formato", "", "| Formato | Publicaciones | Interacciones conocidas | Media | Mediana | Reacciones | Comentarios | Shares |", "|---|---:|---:|---:|---:|---:|---:|---:|"])
    for fmt, values in sorted(analysis["formats"].items()):
        lines.append(f'| {fmt} | {values["publications"]} | {values["interactions_known"]} | {values["mean_interactions_known"]} | {values["median_interactions_known"]} | {values["reactions_known"]} | {values["comments_known"]} | {values["shares_known"]} |')
    lines.extend(["", "## Detalle de publicaciones", "", "| Hora local | Formato | CNT / pieza | Interacciones conocidas | Reacciones | Comentarios | Shares | Calidad | Cruce |", "|---|---|---|---:|---:|---:|---:|---|---|"])
    for row in sorted(rows, key=lambda item: item["time_local"]):
        piece = row["piece_id"] or row["asset_ref"] or "No asignado"
        lines.append(f'| {row["time_local"]} | {row["content_type"]} | {piece} | {row["interactions"]} | {row["reactions"] if row["reactions"] is not None else "No expuesto"} | {row["comments"] if row["comments"] is not None else "No expuesto"} | {row["shares"] if row["shares"] is not None else "No expuesto"} | {row["observation_quality"]} | {row["join_status"]} |')
    lines.extend(["", "## Lectura para Growth OS", "", "El corte actualiza el Growth OS dentro de la misma ejecución en modo **descriptivo y Draft**: registra el ranking observable y separa formatos, pero no cierra hipótesis, no proyecta métricas a `ExperimentLog` y no escribe valores E24/E72. Las decisiones editoriales deben esperar validación humana y, cuando se trate de experimentos, snapshots temporales válidos.", "", "## Salvaguardas", "", "- No se publicó, editó, reprogramó, canceló ni eliminó contenido.", "- No se escribió `Metrics_Snapshot_Log.csv`; el E0 del caso productivo conserva su control independiente.", "- No se asignaron CNT, personaje, familia o experimento a IDs que no tuvieran coincidencia explícita en `Publication_Log.csv`.", "- Reels permanecen fuera de los promedios de imagen/post.", "", "## Fuentes", "", f'- `{analysis["raw_evidence_path"]}` — respuesta raw sanitizada del feed Meta.', "- `Operations/Research/2026-08-15_Publication_Log.csv` — cruce explícito de Meta Post ID.", "- `Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md` — definición del corte y sus limitaciones.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date-local", help="Local calendar date YYYY-MM-DD; defaults to today in America/Matamoros")
    parser.add_argument("--captured-at-utc", help="Capture timestamp; defaults to now")
    args = parser.parse_args()
    capture_utc = parse_dt(args.captured_at_utc) if args.captured_at_utc else datetime.now(timezone.utc)
    assert capture_utc is not None
    capture_local = capture_utc.astimezone(LOCAL_TZ)
    date_local = datetime.fromisoformat(args.date_local).date() if args.date_local else capture_local.date()
    start_local = datetime.combine(date_local, time.min, tzinfo=LOCAL_TZ)
    end_local = capture_local if capture_local.date() == date_local else datetime.combine(date_local, time(22, 0), tzinfo=LOCAL_TZ)
    start_utc = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)
    token = os.environ.get("META_PAGE_ACCESS_TOKEN")
    if not token:
        raise SystemExit("META_PAGE_ACCESS_TOKEN is required")
    page_token = derive_page_token(token)
    feed = fetch_feed(page_token, start_utc, end_utc)
    publications = load_publications()
    rows = [normalize_record(record, publications, capture_utc) for record in feed.get("data", []) if record.get("is_published") is True]
    research = REPO / "Operations/Research"
    raw_path = research / f"{date_local.isoformat()}_Meta_Daily_Metrics_Raw.json"
    csv_path = research / f"{date_local.isoformat()}_Corte_Diario_Metricas_2200.csv"
    analysis_path = research / f"{date_local.isoformat()}_Analisis_Corte_Diario_Metricas_2200.json"
    md_path = research / f"{date_local.isoformat()}_Corte_Diario_Metricas_2200.md"
    raw_record = {
        "captured_at_local": local_iso(capture_local),
        "captured_at_utc": iso(capture_utc),
        "timezone": "America/Matamoros",
        "page_id": PAGE_ID,
        "page_name": "Universe Sent Me",
        "window_start_local": local_iso(start_local),
        "window_end_local": local_iso(end_local),
        "window_start_utc": iso(start_utc),
        "window_end_utc": iso(end_utc),
        "source_endpoint": f"{GRAPH_BASE}/{PAGE_ID}/feed",
        "feed_http_status": 200,
        "feed_error": None,
        "records_returned": len(feed.get("data", [])),
        "data": feed.get("data", []),
        "pagination": feed.get("paging"),
        "limitations": [
            "Interactions are lifetime observable totals at capture time, not exact 24-hour increments.",
            "Views, reach, retention and watch time were not requested or available in this basic feed extraction.",
            "Reels remain a separate format denominator and are not combined with image conclusions.",
        ],
    }
    raw_path.write_text(json.dumps(raw_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_path, rows)
    analysis = write_analysis(analysis_path, capture_local=capture_local, capture_utc=capture_utc, start_local=start_local, end_local=end_local, rows=rows, raw_path=str(raw_path.relative_to(REPO)))
    write_markdown(md_path, analysis, rows, [
        "Operations/Research/2026-08-21_Corte_Diario_Metricas_2200.md",
        "Operations/Research/2026-08-15_Publication_Log.csv",
        "Operations/Research/Metrics_Snapshot_Log.csv",
        "Operations/Automation/run_daily_metrics_cut.py",
    ])
    print(json.dumps({"status": "cut_recorded", "capture_local": local_iso(capture_local), "records": len(rows), "raw": str(raw_path), "csv": str(csv_path), "analysis": str(analysis_path), "markdown": str(md_path), "formats": analysis["formats"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

