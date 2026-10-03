"""
Historical Baseline API - Read-only access to Universe's historical data.

This module provides functions to load and query the historical data stored
in /home/universe-sent-me/growth-os/tenants/universe/historical/.
All functions are pure readers; they do not modify any files.
"""
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Base path to the tenant's historical data
HISTORICAL_BASE = Path(
    "/home/universe-sent-me/growth-os/tenants/universe/historical"
)


def _read_csv(path: Path) -> List[Dict[str, str]]:
    """Read a CSV file and return a list of dictionaries."""
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def load_historical_metrics() -> Dict[str, Any]:
    """
    Load all historical metric sources.
    Returns a dict with keys:
        - cortes_diarios: list of posts from 2026-08-24 with full metrics
        - actividad_diaria: list of daily page metrics (Jun-Jul 2026)
        - rendimiento_horario: list of hourly aggregates (Jun 2026)
        - cola_reutilizacion: list of reuse-approved assets (Jun 2026)
    """
    cortes_path = HISTORICAL_BASE / "publications" / "cortes_diarios_agosto_2026.csv"
    actividad_path = (
        HISTORICAL_BASE
        / "publications"
        / "actividad_diaria_instagram_jun_jul_2026.csv"
    )
    horario_path = HISTORICAL_BASE / "metrics" / "rendimiento_horario_junio_2026.csv"
    cola_path = HISTORICAL_BASE / "metrics" / "cola_reutilizacion_junio_2026.csv"

    return {
        "cortes_diarios": _read_csv(cortes_path),
        "actividad_diaria": _read_csv(actividad_path),
        "rendimiento_horario": _read_csv(horario_path),
        "cola_reutilizacion": _read_csv(cola_path),
    }


def load_historical_experiments() -> List[Dict[str, str]]:
    """Load historical experiments from experiments/experimentos_históricos.csv."""
    path = HISTORICAL_BASE / "experiments" / "experimentos_históricos.csv"
    return _read_csv(path)


def load_historical_hypotheses() -> List[Dict[str, str]]:
    """Load historical hypotheses from hypotheses/hipótesis_históricas.csv."""
    path = HISTORICAL_BASE / "hypotheses" / "hipótesis_históricas.csv"
    return _read_csv(path)


def load_reuse_queue() -> List[Dict[str, str]]:
    """Load the reuse queue from metrics/cola_reutilizacion_junio_2026.csv."""
    path = HISTORICAL_BASE / "metrics" / "cola_reutilizacion_junio_2026.csv"
    return _read_csv(path)


def load_asset_inventory() -> List[Dict[str, str]]:
    """Load the asset inventory from assets/inventario_memes.csv."""
    path = HISTORICAL_BASE / "assets" / "inventario_memes.csv"
    return _read_csv(path)


def load_horario_performance() -> List[Dict[str, str]]:
    """Load hourly performance from metrics/rendimiento_horario_junio_2026.csv."""
    path = HISTORICAL_BASE / "metrics" / "rendimiento_horario_junio_2026.csv"
    return _read_csv(path)


def get_performance_by_personaje() -> List[Dict[str, Any]]:
    """
    Compute historical performance by personaje using available data.
    Uses cortes_diarios_agosto_2026.csv (has asset_ref with personaje names)
    and cola_reutilizacion_junio_2026.csv (has personaje_principal).
    Returns a list of dicts with aggregated metrics and evidence level.
    """
    cortes = load_historical_metrics()["cortes_diarios"]
    reuse = load_reuse_queue()

    # Aggregate from cortes_diarios (each row has asset_ref like "2607825 - Kael - ...")
    personaje_stats = {}
    for row in cortes:
        asset_ref = row.get("asset_ref", "")
        # Extract first token before " - " as personaje
        personaje = asset_ref.split(" - ")[0] if " - " in asset_ref else "Desconocido"
        stats = personaje_stats.setdefault(
            personaje,
            {
                "posts": 0,
                "interacciones": 0,
                "reactions": 0,
                "comments": 0,
                "shares": 0,
                "sources": set(),
            },
        )
        stats["posts"] += 1
        try:
            stats["interacciones"] += int(row.get("interactions", 0) or 0)
        except ValueError:
            pass
        try:
            stats["reactions"] += int(row.get("reactions", 0) or 0)
        except ValueError:
            pass
        try:
            stats["comments"] += int(row.get("comments", 0) or 0)
        except ValueError:
            pass
        try:
            stats["shares"] += int(row.get("shares", 0) or 0)
        except ValueError:
            pass
        stats["sources"].add("cortes_diarios_agosto_2026.csv")

    # Aggregate from cola_reutilizacion (has personaje_principal)
    for row in reuse:
        personaje = row.get("personaje_principal", "Desconocido")
        if not personaje:
            personaje = "Desconocido"
        stats = personaje_stats.setdefault(
            personaje,
            {
                "posts": 0,
                "interacciones": 0,
                "reactions": 0,
                "comments": 0,
                "shares": 0,
                "sources": set(),
            },
        )
        stats["posts"] += 1
        # cola queue has shares and comments but not interactions/reactions directly
        try:
            stats["shares"] += int(row.get("shares", 0) or 0)
        except ValueError:
            pass
        try:
            stats["comments"] += int(row.get("comments", 0) or 0)
        except ValueError:
            pass
        # interactions not available in cola; approximate as shares+comments? we skip.
        stats["sources"].add("cola_reutilizacion_junio_2026.csv")

    # Build result list
    result = []
    for personaje, stats in personaje_stats.items():
        sources = ", ".join(sorted(stats["sources"]))
        # Determine evidence level based on number of sources and posts
        if stats["posts"] >= 2 and len(stats["sources"]) > 1:
            evidence = "confirmed_descriptive"
        elif stats["posts"] == 1:
            evidence = "inferred"
        else:
            evidence = "uncertain"
        result.append(
            {
                "personaje": personaje,
                "posts": stats["posts"],
                "interacciones": stats["interacciones"],
                "reactions": stats["reactions"],
                "comments": stats["comments"],
                "shares": stats["shares"],
                "evidence_level": evidence,
                "sources": sources,
            }
        )
    # Sort by posts descending
    result.sort(key=lambda x: x["posts"], reverse=True)
    return result


def get_signals_by_formato() -> List[Dict[str, Any]]:
    """
    Compute historical signals by formato (e.g., micro-historias 3 paneles).
    Uses cortes_diarios_agosto_2026.csv where asset_ref contains format hints.
    """
    cortes = load_historical_metrics()["cortes_diarios"]
    formato_stats = {}
    for row in cortes:
        asset_ref = row.get("asset_ref", "")
        # Detect format hints in asset_ref
        formato = "Desconocido"
        if "FUT-MICRO" in asset_ref or "Microhistoria" in asset_ref:
            formato = "Micro-historia 3 paneles"
        elif "Kael" in asset_ref:
            formato = "Kael (Lore/Identidad)"
        elif "Universe" in asset_ref:
            formato = "Universe (Humor absurdo)"
        elif "Wilfred" in asset_ref:
            formato = "Wilfred (Sabiduría/Observacional)"
        else:
            formato = "Otro"
        stats = formato_stats.setdefault(
            formato,
            {
                "posts": 0,
                "interacciones": 0,
                "reactions": 0,
                "comments": 0,
                "shares": 0,
                "sources": set(),
            },
        )
        stats["posts"] += 1
        try:
            stats["interacciones"] += int(row.get("interactions", 0) or 0)
        except ValueError:
            pass
        try:
            stats["reactions"] += int(row.get("reactions", 0) or 0)
        except ValueError:
            pass
        try:
            stats["comments"] += int(row.get("comments", 0) or 0)
        except ValueError:
            pass
        try:
            stats["shares"] += int(row.get("shares", 0) or 0)
        except ValueError:
            pass
        stats["sources"].add("cortes_diarios_agosto_2026.csv")

    result = []
    for formato, stats in formato_stats.items():
        sources = ", ".join(sorted(stats["sources"]))
        if stats["posts"] >= 2:
            evidence = "confirmed_descriptive"
        elif stats["posts"] == 1:
            evidence = "inferred"
        else:
            evidence = "uncertain"
        result.append(
            {
                "formato": formato,
                "posts": stats["posts"],
                "interacciones": stats["interacciones"],
                "reactions": stats["reactions"],
                "comments": stats["comments"],
                "shares": stats["shares"],
                "evidence_level": evidence,
                "sources": sources,
            }
        )
    result.sort(key=lambda x: x["posts"], reverse=True)
    return result


def get_evidence_levels() -> Dict[str, List[Dict[str, Any]]]:
    """
    Return historical hypotheses and experiments with their evidence levels.
    """
    experiments = load_historical_experiments()
    hypotheses = load_historical_hypotheses()

    # Experiments: we know they are inferred, no formal verdict
    exp_result = []
    for exp in experiments:
        exp_result.append(
            {
                "experiment_id": exp.get("experiment_id", ""),
                "descripcion": exp.get("descripcion", ""),
                "fecha_asociada": exp.get("fecha_asociada", ""),
                "fuente": exp.get("fuente", ""),
                "estado": exp.get("estado", ""),
                "evidence_level": "inferred",  # as per document
            }
        )

    # Hypotheses: from file, they are labeled as Histórico but we treat as inferred
    hyp_result = []
    for hyp in hypotheses:
        hyp_result.append(
            {
                "hypothesis_id": hyp.get("hypothesis_id", ""),
                "descripcion": hyp.get("descripcion", ""),
                "criterio_exito": hyp.get("criterio_exito", ""),
                "estado": hyp.get("estado", ""),
                "fuente": hyp.get("fuente", ""),
                "evidence_level": "inferred",  # per doc: inferida
            }
        )

    return {"experiments": exp_result, "hypotheses": hyp_result}


def get_publicaciones_con_metricas() -> List[Dict[str, Any]]:
    """
    Return list of historical posts that have actual metrics (interactions, etc.).
    Only cortes_diarios_agosto_2026.csv has full post-level metrics.
    """
    cortes = load_historical_metrics()["cortes_diarios"]
    result = []
    for row in cortes:
        result.append(
            {
                "date_local": row.get("date_local", ""),
                "time_local": row.get("time_local", ""),
                "content_type": row.get("content_type", ""),
                "piece_id": row.get("piece_id", ""),
                "asset_ref": row.get("asset_ref", ""),
                "meta_post_id": row.get("meta_post_id", ""),
                "permalink_url": row.get("permalink_url", ""),
                "interactions": int(row.get("interactions", 0) or 0),
                "reactions": int(row.get("reactions", 0) or 0),
                "comments": int(row.get("comments", 0) or 0),
                "shares": int(row.get("shares", 0) or 0),
                "experiment_id": row.get("experiment_id", ""),
                "hypothesis_id": row.get("hypothesis_id", ""),
                "join_status": row.get("join_status", ""),
                "is_published": row.get("is_published", ""),
                "observation_quality": row.get("observation_quality", ""),
                "family_character_note": row.get("family_character_note", ""),
                "publicacion_id": row.get("publicacion_id", ""),
                "experiment_id_col": row.get("experiment_id", ""),
                "hypothesis_id_col": row.get("hypothesis_id", ""),
                "planned_time_local": row.get("planned_time_local", ""),
            }
        )
    return result


# Example usage for dry-run (commented out to avoid execution on import)
if __name__ == "__main__":
    # Simple test prints
    print("=== Historical Baseline API Test ===")
    metrics = load_historical_metrics()
    print(f"Cortes diarios posts: {len(metrics['cortes_diarios'])}")
    print(f"Actividad diaria días: {len(metrics['actividad_diaria'])}")
    print(f"Rendimiento horario filas: {len(metrics['rendimiento_horario'])}")
    print(f"Cola reuse assets: {len(metrics['cola_reutilizacion'])}")
    print("\nExperiments:")
    for exp in load_historical_experiments():
        print(f"  {exp.get('experiment_id')}: {exp.get('descripcion')}")
    print("\nHypotheses:")
    for hyp in load_historical_hypotheses():
        print(f"  {hyp.get('hypothesis_id')}: {hyp.get('descripcion')}")
    print("\nPerformance by personaje:")
    for p in get_performance_by_personaje():
        print(
            f"  {p['personaje']}: posts={p['posts']}, "
            f"interacciones={p['interacciones']}, shares={p['shares']}, "
            f"evidence={p['evidence_level']}"
        )
    print("\nSignals by formato:")
    for f in get_signals_by_formato():
        print(
            f"  {f['formato']}: posts={f['posts']}, interacciones={f['interacciones']}, "
            f"evidence={f['evidence_level']}"
        )
    print("\nPublicaciones con métricas (post-level):")
    for pub in get_publicaciones_con_metricas()[:3]:  # show first 3
        print(
            f"  {pub['date_local']} {pub['time_local']} | "
            f"asset={pub['asset_ref'][:30]}... | "
            f"int={pub['interactions']} shares={pub['shares']}"
        )

def get_historical_reuse_info(asset_filename: str) -> Optional[Dict[str, Any]]:
    """
    Return historical reuse information for an asset filename.
    Looks up the asset in the reuse queue (cola_reutilizacion_junio_2026.csv)
    by matching the numeric part of asset_filename with asset_ref.
    Returns a dict with the row data if found, else None.
    """
    try:
        # Extract numeric part from asset_filename (e.g., "123456 - Kael - Test.png" -> "123456")
        import re
        match = re.search(r'\d+', asset_filename)
        if not match:
            return None
        asset_num = match.group(0)
        reuse_queue = load_reuse_queue()
        for row in reuse_queue:
            if row.get('asset_ref') == asset_num:
                return row
        return None
    except Exception:
        return None


def get_historical_hypothesis_by_id(hyp_id: str) -> Optional[Dict[str, Any]]:
    """
    Return a historical hypothesis by its hypothesis_id.
    Returns the hypothesis dict if found, else None.
    """
    try:
        hypotheses = load_historical_hypotheses()
        for hyp in hypotheses:
            if hyp.get('hypothesis_id') == hyp_id:
                return hyp
        return None
    except Exception:
        return None
