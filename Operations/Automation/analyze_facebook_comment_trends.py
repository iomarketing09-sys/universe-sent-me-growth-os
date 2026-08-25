"""Analyze Facebook comment interaction trends from repository evidence.

This script performs no Meta calls and no writes to Facebook. It reads the
current read-only scan, prior scan artifacts, and the anonymized ledger, then
writes a JSON and Markdown comparison report.
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
CURRENT_SCAN = RESEARCH / "2025-placeholder"


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00").replace("+0000", "+00:00"))


def pct(value: int | float, total: int | float) -> float:
    return round((value / total * 100) if total else 0.0, 2)


def safe_title(message: str) -> str:
    if "MaeveUSM" in message:
        return "Reel de Maeve"
    if "#UniverseUSM" in message:
        return "Meme ‘larga vida a esas mujeres que aprietan desde adentro’"
    if "😌" in message:
        return "Publicación de contexto breve"
    return message or "Publicación sin caption recuperable"


def load_scan(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_scan(scan: dict, label: str, candidate_key: str = "new_unanswered_not_in_ledger") -> dict:
    rows = scan.get(candidate_key, [])
    by_type = Counter(row.get("comment_type") for row in rows)
    by_post = Counter()
    post_messages: dict[str, str] = {}
    for row in rows:
        post_id = row.get("post_id") or ""
        by_post[post_id] += 1
        post_messages.setdefault(post_id, row.get("post_message") or "")
    roots = by_type.get("Comentario_Raiz", 0)
    nested = by_type.get("Replica_Anidada", 0)
    created_times = [parse_dt(row["comment_created_time"]) for row in rows if row.get("comment_created_time")]
    cohort_min = min(created_times) if created_times else None
    cohort_max = max(created_times) if created_times else None
    duration_hours = round((cohort_max - cohort_min).total_seconds() / 3600, 2) if cohort_min and cohort_max else None
    return {
        "label": label,
        "reviewed_at": scan.get("reviewed_at"),
        "cursor": scan.get("cursor"),
        "candidate_count": len(rows),
        "root_count": roots,
        "nested_count": nested,
        "root_share_pct": pct(roots, len(rows)),
        "nested_share_pct": pct(nested, len(rows)),
        "posts_with_candidates": len(by_post),
        "cohort_min_comment_time": cohort_min.isoformat() if cohort_min else None,
        "cohort_max_comment_time": cohort_max.isoformat() if cohort_max else None,
        "cohort_duration_hours": duration_hours,
        "observed_comments_per_hour": round(len(rows) / max(duration_hours, 1e-9), 2) if duration_hours else None,
        "top_posts": [
            {
                "post_id": post_id,
                "post_reference": safe_title(post_messages.get(post_id, "")),
                "count": count,
                "share_pct": pct(count, len(rows)),
            }
            for post_id, count in by_post.most_common()
        ],
    }


def window_rows(rows: list[dict], start: datetime, end: datetime) -> list[dict]:
    output = []
    for row in rows:
        value = row.get("Fecha_Comentario", "")
        if not value:
            continue
        created = parse_dt(value)
        if start <= created < end:
            output.append(row)
    return output


def summarize_window(rows: list[dict], label: str, start: datetime, end: datetime) -> dict:
    by_type = Counter(row.get("Tipo") for row in rows)
    by_status = Counter(row.get("Respuesta_Estado") for row in rows)
    by_signal = Counter(row.get("Señal") for row in rows)
    by_post = Counter(row.get("Post_ID") for row in rows)
    return {
        "label": label,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "count": len(rows),
        "comments_per_day": round(len(rows) / max((end - start).total_seconds() / 86400, 1e-9), 2),
        "root_count": by_type.get("Comentario_Raiz", 0),
        "nested_count": by_type.get("Replica_Anidada", 0),
        "root_share_pct": pct(by_type.get("Comentario_Raiz", 0), len(rows)),
        "status_counts": dict(by_status),
        "signal_counts": dict(by_signal),
        "posts_with_comments": len(by_post),
        "top_post_ids": [{"post_id": post_id, "count": count} for post_id, count in by_post.most_common(10)],
    }


def main() -> None:
    current_path = RESEARCH / "2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json"
    current_editorial_path = RESEARCH / "2026-08-25_Facebook_Editorial_Review_After_Five_Approved_Replies.json"
    prior_95_path = RESEARCH / "2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json"
    prior_83_path = RESEARCH / "2026-08-24_Facebook_Comment_Review_After_Batch14.json"
    prior_95_editorial_path = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json"
    prior_83_editorial_path = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Batch14.json"
    ledger_path = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
    out_json = RESEARCH / "2026-08-25_Facebook_Comment_Interaction_Trends_Analysis.json"
    out_md = RESEARCH / "2026-08-25_Facebook_Comment_Interaction_Trends_Analysis.md"

    current = load_scan(current_path)
    current_editorial = load_scan(current_editorial_path)
    prior_95 = load_scan(prior_95_path)
    prior_83 = load_scan(prior_83_path)
    prior_95_editorial = load_scan(prior_95_editorial_path)
    prior_83_editorial = load_scan(prior_83_editorial_path)
    current_rows = current.get("new_unanswered_not_in_ledger", [])
    editorial_records = current_editorial.get("records", [])
    if len(current_rows) != 101 or len(editorial_records) != 101:
        raise SystemExit(f"CURRENT_COHORT_EXPECTED_101: scan={len(current_rows)} editorial={len(editorial_records)}")

    with ledger_path.open("r", encoding="utf-8-sig", newline="") as handle:
        ledger_rows = list(csv.DictReader(handle))
    if len(ledger_rows) != 549 or len({row.get("Comentario_ID") for row in ledger_rows}) != 549:
        raise SystemExit("LEDGER_EXPECTED_549_UNIQUE_ROWS")

    reviewed_at = parse_dt(current["reviewed_at"])
    cursor = parse_dt(current["cursor"])
    prior_7_start = cursor - timedelta(days=7)
    prior_14_start = cursor - timedelta(days=14)
    current_duration_hours = round((reviewed_at - cursor).total_seconds() / 3600, 2)
    current_min = min(parse_dt(row["comment_created_time"]) for row in current_rows)
    current_max = max(parse_dt(row["comment_created_time"]) for row in current_rows)
    burst_duration_hours = round((current_max - current_min).total_seconds() / 3600, 2)
    current_hour_counts = Counter(parse_dt(row["comment_created_time"]).strftime("%Y-%m-%dT%H:00Z") for row in current_rows)
    current_proposals = sum(1 for row in editorial_records if row.get("editorial_decision") == "Pendiente_Respuesta")
    current_no_action = sum(1 for row in editorial_records if row.get("editorial_decision") == "No_Requiere_Respuesta")
    current_music = sum(1 for row in editorial_records if row.get("comment_id") in set(current_editorial.get("music_candidate_ids", [])))

    previous_7_rows = window_rows(ledger_rows, prior_7_start, cursor)
    previous_14_rows = window_rows(ledger_rows, prior_14_start, prior_7_start)
    current_summary = summarize_scan(current, "Corte actual posterior a cinco respuestas")
    prior_95_summary = summarize_scan(prior_95, "Corte anterior de 95 comentarios")
    prior_83_summary = summarize_scan(prior_83, "Corte anterior de 83 comentarios")
    previous_7_summary = summarize_window(previous_7_rows, "Ventana de 7 días inmediatamente anterior al cursor", prior_7_start, cursor)
    previous_14_summary = summarize_window(previous_14_rows, "Ventana de 7 días entre 14 y 7 días antes del cursor", prior_14_start, prior_7_start)
    prior_week_growth_pct = round((previous_7_summary["count"] - previous_14_summary["count"]) / previous_14_summary["count"] * 100, 2) if previous_14_summary["count"] else None

    prior_83_proposals = prior_83_editorial.get("proposal_count", 0)
    prior_83_no_action = prior_83_editorial.get("no_action_count", 0)
    prior_95_proposals = prior_95_editorial.get("proposal_count", 0)
    prior_95_no_action = prior_95_editorial.get("no_action_count", 0)
    history = [
        {"label": "Corte de 83", "comments": prior_83_summary["candidate_count"], "proposals": prior_83_proposals, "no_action": prior_83_no_action, "proposal_rate_pct": pct(prior_83_proposals, prior_83_summary["candidate_count"]), "duration_hours": prior_83_summary["cohort_duration_hours"], "comments_per_hour": prior_83_summary["observed_comments_per_hour"]},
        {"label": "Corte de 95", "comments": prior_95_summary["candidate_count"], "proposals": prior_95_proposals, "no_action": prior_95_no_action, "proposal_rate_pct": pct(prior_95_proposals, prior_95_summary["candidate_count"]), "duration_hours": prior_95_summary["cohort_duration_hours"], "comments_per_hour": prior_95_summary["observed_comments_per_hour"]},
        {"label": "Corte actual de 101", "comments": len(current_rows), "proposals": current_proposals, "no_action": current_no_action, "proposal_rate_pct": pct(current_proposals, len(current_rows)), "duration_hours": current_summary["cohort_duration_hours"], "comments_per_hour": current_summary["observed_comments_per_hour"]},
    ]
    current_top = current_summary["top_posts"][0] if current_summary["top_posts"] else {"post_reference": "N/D", "share_pct": 0}
    prior_95_top = prior_95_summary["top_posts"][0] if prior_95_summary["top_posts"] else {"post_reference": "N/D", "share_pct": 0}

    report = {
        "title": "Facebook Comment Interaction Trends Analysis",
        "purpose": "Comparar el corte actual de 101 comentarios nuevos con cortes previos y ventanas temporales del ledger, sin inferir alcance o impresiones que no estén disponibles.",
        "status": "Review",
        "created_at": current["reviewed_at"],
        "updated_at": current["reviewed_at"],
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json",
            "Operations/Research/2026-08-25_Facebook_Editorial_Review_After_Five_Approved_Replies.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
            "GrowthOS/00_01_Changelog_GrowthOS.md",
        ],
        "source_scope": "Repository evidence from Meta Graph API v26.0 read-only scans and the anonymized Community Engagement Log",
        "comparison_limits": [
            "Comment counts measure observed comments in the scanned 20 own Page posts, not reach, impressions, views, or unique commenters.",
            "The current scan reads one level of replies and up to 100 objects per collection; it is not a full historical export.",
            "The current 101-comment cohort is a burst after the previous publication cursor, while prior weekly windows cover different post mixes and durations.",
        ],
        "current_scan": {
            **current_summary,
            "reviewed_at": current["reviewed_at"],
            "cursor": current["cursor"],
            "current_unanswered_units_in_scope": current["current_unanswered_units"],
            "new_units_since_cursor": current["new_units_since_latest_cursor"],
            "api_error_count": current["api_error_count"],
            "proposal_count": current_proposals,
            "no_action_count": current_no_action,
            "proposal_rate_pct": pct(current_proposals, len(current_rows)),
            "music_candidate_count": current_music,
            "burst_min_comment_time": current_min.isoformat(),
            "burst_max_comment_time": current_max.isoformat(),
            "burst_duration_hours": burst_duration_hours,
            "cursor_to_review_hours": current_duration_hours,
            "observed_comments_per_hour_in_burst": round(len(current_rows) / max(burst_duration_hours, 1e-9), 2),
            "hourly_counts_utc": dict(sorted(current_hour_counts.items())),
        },
        "prior_scans": [prior_83_summary, prior_95_summary],
        "cut_history": history,
        "ledger_windows": [previous_7_summary, previous_14_summary],
        "derived_comparisons": {
            "current_vs_prior_95_pct_change": round((len(current_rows) - prior_95_summary["candidate_count"]) / prior_95_summary["candidate_count"] * 100, 2),
            "current_vs_prior_83_pct_change": round((len(current_rows) - prior_83_summary["candidate_count"]) / prior_83_summary["candidate_count"] * 100, 2),
            "current_vs_prior_7_day_ledger_count_pct_change": round((len(current_rows) - previous_7_summary["count"]) / previous_7_summary["count"] * 100, 2) if previous_7_summary["count"] else None,
            "current_vs_prior_7_day_ledger_hourly_rate_pct_change": round(((len(current_rows) / max(burst_duration_hours, 1e-9)) - (previous_7_summary["count"] / 168)) / (previous_7_summary["count"] / 168) * 100, 2) if previous_7_summary["count"] else None,
            "current_vs_prior_95_duration_pct_change": round((current_summary["cohort_duration_hours"] - prior_95_summary["cohort_duration_hours"]) / prior_95_summary["cohort_duration_hours"] * 100, 2),
            "current_vs_prior_95_hourly_rate_pct_change": round((current_summary["observed_comments_per_hour"] - prior_95_summary["observed_comments_per_hour"]) / prior_95_summary["observed_comments_per_hour"] * 100, 2),
            "current_top_post_share_minus_prior_95_top_post_share_percentage_points": round(current_top["share_pct"] - prior_95_top["share_pct"], 2),
            "prior_7_day_vs_prior_14_to_7_day_count_pct_change": prior_week_growth_pct,
            "current_proposal_rate_minus_prior_95_percentage_points": round(pct(current_proposals, len(current_rows)) - pct(prior_95_proposals, prior_95_summary["candidate_count"]), 2),
            "current_nested_share_minus_prior_95_percentage_points": round(current_summary["nested_share_pct"] - prior_95_summary["nested_share_pct"], 2),
        },
        "editorial_outcomes_current": {
            "proposals": [
                {
                    "comment_id": row.get("comment_id"),
                    "comment_message": row.get("comment_message"),
                    "post_reference": row.get("post_reference"),
                    "proposed_reply": row.get("proposed_reply"),
                }
                for row in editorial_records
                if row.get("editorial_decision") == "Pendiente_Respuesta"
            ],
            "no_action_count": current_no_action,
            "no_action_by_reason": dict(Counter(row.get("reason_code") for row in editorial_records if row.get("editorial_decision") == "No_Requiere_Respuesta")),
        },
    }

    def table(rows: list[list[object]]) -> str:
        return "\n".join("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in rows)

    history_rows = [["Corte", "Comentarios", "Propuestas", "No acción", "Tasa propuesta", "Duración h", "Comentarios/h"]]
    history_rows += [[item["label"], item["comments"], item["proposals"], item["no_action"], f"{item['proposal_rate_pct']}%", item["duration_hours"], item["comments_per_hour"]] for item in history]
    top_current = current_summary["top_posts"][:5]
    top_rows = [["Referencia", "Comentarios nuevos", "% del corte"]] + [[item["post_reference"], item["count"], f"{item['share_pct']}%"] for item in top_current]
    ledger_rows_md = [["Ventana", "Comentarios", "Por día"]]
    for item in (previous_7_summary, previous_14_summary):
        ledger_rows_md.append([item["label"], item["count"], item["comments_per_day"]])
    hourly_rows = [["Hora UTC", "Comentarios"]] + [[hour, count] for hour, count in sorted(current_hour_counts.items())]
    proposal_rows = [["Comentario", "Publicación", "Respuesta propuesta"]]
    for item in report["editorial_outcomes_current"]["proposals"]:
        proposal_rows.append([item["comment_message"], item["post_reference"], item["proposed_reply"]])

    markdown = f"""---
title: \"Facebook Comment Interaction Trends Analysis\"
purpose: \"Comparación de tendencias de interacción observada en comentarios de Facebook.\"
status: Review
created: {current['reviewed_at'][:10]}
updated: {current['reviewed_at'][:10]}
version: \"1.0\"
author: \"Manus AI\"
related_documents:
  - Operations/Research/2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json
  - Operations/Research/2026-08-25_Facebook_Editorial_Review_After_Five_Approved_Replies.json
  - Operations/Research/2026-08-15_Community_Engagement_Log.csv
  - Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md
  - GrowthOS/00_01_Changelog_GrowthOS.md
organization: Operations/Research
---

# Tendencias de interacción en comentarios de Facebook

## Resumen ejecutivo

El corte actual observó **101 comentarios nuevos** entre `{current_min.isoformat()}` y `{current_max.isoformat()}` dentro de las 20 publicaciones propias más recientes. El volumen supera en **{report['derived_comparisons']['current_vs_prior_95_pct_change']}%** al corte anterior de 95 comentarios y en **{report['derived_comparisons']['current_vs_prior_83_pct_change']}%** al corte de 83. Sin embargo, el volumen no equivale a demanda directa de la Página: **71 de 101 ({current_summary['nested_share_pct']}%) son réplicas anidadas**, y solo **2 ({pct(current_proposals, len(current_rows))}%)** fueron suficientemente específicas para proponer respuesta.

La conversación está fuertemente concentrada en los mismos dos formatos de doble sentido que dominaron el corte previo. La señal nueva más útil es musical: aparecieron dos referencias identificables por título y artista —`CONTIGO` de Karol G y `Aventurera` de Alberto Plaza—, ambas conservadas como propuestas pendientes. El resto se clasificó sin acción por conversación usuario-a-usuario, baja señal, contexto ambiguo o lenguaje sensible.

> Esta comparación mide **comentarios observados**, no alcance, impresiones, reproducciones, sentimiento poblacional ni usuarios únicos. Por ello, describe la presión conversacional visible en los hilos y no el rendimiento total de las publicaciones.

## Comparación de cortes editoriales

{table(history_rows[:1] + [["---", "---", "---", "---", "---", "---", "---"]] + history_rows[1:])}

La tasa de propuesta descendió de **{pct(prior_95_proposals, prior_95_summary['candidate_count'])}%** en el corte anterior de 95 a **{pct(current_proposals, len(current_rows))}%** ahora, una diferencia de **{report['derived_comparisons']['current_proposal_rate_minus_prior_95_percentage_points']} puntos porcentuales**. No debe interpretarse como caída de interés: refleja que el volumen adicional está compuesto sobre todo por réplicas laterales y reacciones que no requieren intervención de la Página.

## Velocidad y concentración

El burst actual contiene {len(current_rows)} comentarios en {burst_duration_hours} horas de timestamps efectivos, equivalente a **{round(len(current_rows) / max(burst_duration_hours, 1e-9), 2)} comentarios observados por hora**. El corte anterior de 95 tuvo {prior_95_summary['cohort_duration_hours']} horas y {prior_95_summary['observed_comments_per_hour']} comentarios por hora: el volumen actual creció principalmente porque la ventana duró **{report['derived_comparisons']['current_vs_prior_95_duration_pct_change']}%** más, no porque la velocidad por hora aumentara —la tasa cambió **{report['derived_comparisons']['current_vs_prior_95_hourly_rate_pct_change']}%**. La ventana cursor–revisión fue de {current_duration_hours} horas.

### Distribución horaria UTC

{table(hourly_rows[:1] + [["---", "---"]] + hourly_rows[1:])}

La ventana semanal inmediata anterior del ledger contiene {previous_7_summary['count']} comentarios frente a {previous_14_summary['count']} en la semana previa; es un cambio de **{prior_week_growth_pct}%**. Esta comparación es histórica y no equivale a un ritmo de alcance, porque el ledger mezcla publicaciones y estados distintos.

### Publicaciones que concentran el corte actual

{table(top_rows[:1] + [["---", "---", "---"]] + top_rows[1:])}

La concentración confirma que el volumen está impulsado por formatos concretos, no distribuido uniformemente por todo el perfil. El Reel de Maeve representa **{current_top['share_pct']}%** del corte, frente a **{prior_95_top['share_pct']}%** en el corte anterior (+{report['derived_comparisons']['current_top_post_share_minus_prior_95_top_post_share_percentage_points']} puntos porcentuales). Esta observación recomienda comparar próximos cortes por publicación y no usar el total de comentarios como único KPI de engagement.

## Profundidad y calidad de la interacción

La proporción de réplicas anidadas en el corte actual es **{current_summary['nested_share_pct']}%**, frente a **{prior_95_summary['nested_share_pct']}%** en el corte anterior de 95; la diferencia es de **{report['derived_comparisons']['current_nested_share_minus_prior_95_percentage_points']} puntos porcentuales**. El hilo está activo, pero la mayoría de esa actividad ocurre entre usuarios. En el ledger, la ventana inmediata anterior de siete días contiene {previous_7_summary['count']} comentarios ({previous_7_summary['comments_per_day']} por día), mientras la ventana de siete días anterior contiene {previous_14_summary['count']} ({previous_14_summary['comments_per_day']} por día).

{table(ledger_rows_md[:1] + [["---", "---", "---"]] + ledger_rows_md[1:])}

## Señal musical y oportunidad editorial

Las dos propuestas actuales son:

{table(proposal_rows[:1] + [["---", "---", "---"]] + proposal_rows[1:])}

Estas dos señales son cualitativamente diferentes de un emoji o una mención aislada: contienen una combinación interpretable de título y artista. La recomendación es mantener una respuesta breve y específica, sin convertir cada sugerencia musical en análisis de letra ni responder automáticamente las réplicas relacionadas.

## Decisiones para Growth OS

1. **Separar volumen de profundidad.** Reportar siempre raíces y réplicas por separado; en este corte, 70.3% de las unidades nuevas fueron réplicas.
2. **Medir oportunidad directa.** Usar la tasa de propuestas —2.0% en este corte— como indicador editorial complementario, no como sustituto de alcance o reproducciones.
3. **Conservar el análisis por publicación.** El total actual está concentrado en los reels/memes de doble sentido; comparar perfiles completos sin desglosar publicación ocultaría el motor real del volumen.
4. **Crear una categoría musical identificable.** Título + artista es suficiente para una propuesta breve; una referencia incompleta debe permanecer en revisión o no acción.
5. **No escalar el tono por volumen.** La actividad de usuarios no autoriza a la Página a intervenir en cada réplica ni a amplificar contenido íntimo.

## Límites y trazabilidad

La fuente es el escaneo GET-only de Meta Graph API v26.0 y el ledger anonimizado. El escaneo revisó las 20 publicaciones propias más recientes, una capa de réplicas y hasta 100 objetos por colección. No se consultaron otras redes, grupos ni herramientas externas. El inventario completo de 101 unidades permanece en el reporte editorial de este corte.

## Referencias

[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions
[2]: https://developers.facebook.com/docs/graph-api/reference/comment/
"""
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(markdown, encoding="utf-8")
    print(json.dumps({
        "current_comments": len(current_rows),
        "current_proposals": current_proposals,
        "current_no_action": current_no_action,
        "prior_95_comments": prior_95_summary["candidate_count"],
        "prior_83_comments": prior_83_summary["candidate_count"],
        "prior_7_day_ledger_comments": previous_7_summary["count"],
        "prior_14_to_7_day_ledger_comments": previous_14_summary["count"],
        "output_json": str(out_json),
        "output_md": str(out_md),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
