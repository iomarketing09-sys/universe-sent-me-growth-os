"""Cobertura de medición por tenant, sin emitir veredictos.

Resume qué métricas tienen muestras reales en el ledger de snapshots y qué
hipótesis todavía no pueden evaluarse. La ausencia de una métrica se reporta
como ausencia, nunca como cero.
"""

from __future__ import annotations

import argparse
import json
from statistics import median
from typing import Any, Callable, Dict, Iterable, List, Optional

from modules.intelligence.metrics_snapshot import MetricsSnapshot, load_snapshot_log


TARGET_METRICS = (
    "reach",
    "views",
    "saved",
    "video_completion_rate",
    "video_average_watch_share",
)

METRIC_UNITS = {
    "reach": "count",
    "views": "count",
    "saved": "count",
    "video_completion_rate": "ratio",
    "video_average_watch_share": "ratio",
}

DERIVED_METRICS: Dict[str, Callable[[MetricsSnapshot], Optional[float]]] = {
    "video_completion_rate": lambda snapshot: snapshot.video_completion_rate,
    "video_average_watch_share": lambda snapshot: snapshot.video_average_watch_share,
}


def _metric_value(snapshot: MetricsSnapshot, field: str) -> Optional[float]:
    if field in DERIVED_METRICS:
        return DERIVED_METRICS[field](snapshot)
    value = getattr(snapshot, field, None)
    # En el ledger un contador en 0 significa ausencia de captura, no un cero
    # observado. Las proporciones derivadas sí distinguen 0.0 de ``None``.
    if value in (None, "", 0, "0"):
        return None
    return float(value)


def _metric_summary(
    snapshots: Iterable[MetricsSnapshot],
    field: str,
) -> Dict[str, Any]:
    # Una publicación con varios snapshots cuenta una sola vez. Se toma su
    # último valor con dato para no sobrerrepresentarla frente a las demás.
    rows = 0
    latest: Dict[str, tuple[str, float]] = {}
    for snapshot in snapshots:
        value = _metric_value(snapshot, field)
        if value is None:
            continue
        rows += 1
        publication = snapshot.publication_id or snapshot.snapshot_id
        captured_at = snapshot.captured_at_utc or snapshot.created_at
        previous = latest.get(publication)
        if previous is None or captured_at >= previous[0]:
            latest[publication] = (captured_at, value)
    values: List[float] = [value for _, value in latest.values()]
    summary: Dict[str, Any] = {
        "rows": rows,
        "publications": len(latest),
        "unit": METRIC_UNITS.get(field, ""),
    }
    if values:
        summary["median"] = round(median(values), 4)
        summary["min"] = round(min(values), 4)
        summary["max"] = round(max(values), 4)
    return summary


def _hypothesis_status(
    snapshots: Iterable[MetricsSnapshot],
    *,
    field: str,
    blocker: str,
) -> Dict[str, Any]:
    summary = _metric_summary(snapshots, field)
    return {
        "status": "samples_available" if summary["publications"] else "no_samples",
        "metric": field,
        "publications": summary["publications"],
        "blocker": "" if summary["publications"] else blocker,
    }


def build_measurement_coverage(
    tenant_id: str,
    snapshots: Optional[Iterable[MetricsSnapshot]] = None,
) -> Dict[str, Any]:
    """Construye el reporte de cobertura a partir del snapshot ledger local."""
    snapshots = list(snapshots if snapshots is not None else load_snapshot_log(tenant_id))
    by_platform: Dict[str, List[MetricsSnapshot]] = {}
    for snapshot in snapshots:
        platform = snapshot.platform or "Unknown"
        by_platform.setdefault(platform, []).append(snapshot)

    platforms: Dict[str, Any] = {}
    for platform, platform_snapshots in sorted(by_platform.items()):
        platforms[platform] = {
            "snapshots": len(platform_snapshots),
            "publications": len({snap.publication_id for snap in platform_snapshots}),
            "metrics": {
                field: _metric_summary(platform_snapshots, field)
                for field in TARGET_METRICS
            },
        }

    video_blocker = (
        "Sin videos Facebook con reproducciones y completaciones orgánicas. "
        "Instagram requiere instagram_manage_insights."
    )
    reach_blocker = (
        "Facebook retiró reach/impresiones por post en Graph v26; Instagram "
        "requiere instagram_manage_insights (App Review)."
    )
    return {
        "tenant_id": tenant_id,
        "snapshots": len(snapshots),
        "publications": len({snap.publication_id for snap in snapshots if snap.publication_id}),
        "platforms": platforms,
        "hypotheses": {
            "HB-UNI-002": _hypothesis_status(
                snapshots,
                field="video_completion_rate",
                blocker=video_blocker,
            ),
            "HB-UNI-004": _hypothesis_status(
                snapshots,
                field="reach",
                blocker=reach_blocker,
            ),
        },
    }


def render_measurement_coverage(report: Dict[str, Any]) -> str:
    lines = [
        f"Cobertura de medición · {report['tenant_id']}",
        f"Snapshots: {report['snapshots']} · publicaciones: {report['publications']}",
    ]
    for platform, summary in report["platforms"].items():
        lines.append(
            f"\n{platform}: {summary['publications']} publicaciones, "
            f"{summary['snapshots']} snapshots"
        )
        for field, metric in summary["metrics"].items():
            med = f", mediana={metric['median']}" if "median" in metric else ""
            unit = f", unidad={metric['unit']}" if metric.get("unit") else ""
            lines.append(
                f"  {field}: {metric['publications']} publicaciones con dato{med}{unit}"
            )
    lines.append("\nHipótesis:")
    for hypothesis_id, status in report["hypotheses"].items():
        lines.append(
            f"  {hypothesis_id}: {status['status']} "
            f"({status['publications']} publicaciones)"
        )
        if status["blocker"]:
            lines.append(f"    bloqueo: {status['blocker']}")
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tenant_id")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    report = build_measurement_coverage(args.tenant_id)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_measurement_coverage(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "build_measurement_coverage",
    "render_measurement_coverage",
]
