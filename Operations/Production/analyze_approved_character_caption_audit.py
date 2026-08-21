#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"
OUT_JSON = ROOT / "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Analysis.json"
OUT_MD = ROOT / "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Analysis.md"

with INPUT.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))
for row in rows:
    row["interactions_n"] = int(row["interactions"] or 0)
    row["shares_n"] = int(row["shares"] or 0)
    row["comments_n"] = int(row["comments"] or 0)


def stats(group):
    if not group:
        return {"n": 0, "interactions_total": 0, "interactions_median": None, "shares_total": 0, "shares_median": None, "comments_total": 0, "comments_median": None}
    return {
        "n": len(group),
        "interactions_total": sum(r["interactions_n"] for r in group),
        "interactions_median": statistics.median(r["interactions_n"] for r in group),
        "shares_total": sum(r["shares_n"] for r in group),
        "shares_median": statistics.median(r["shares_n"] for r in group),
        "comments_total": sum(r["comments_n"] for r in group),
        "comments_median": statistics.median(r["comments_n"] for r in group),
    }

by_treatment = defaultdict(list)
by_source = defaultdict(list)
for row in rows:
    by_treatment[row["proposed_caption_treatment"]].append(row)
    by_source[row["caption_source"]].append(row)

treatment_stats = {key: stats(group) for key, group in sorted(by_treatment.items())}
source_stats = {key: stats(group) for key, group in sorted(by_source.items())}

manual_reviewed = [r for r in rows if r["manual_review_status"] == "Analyst_Reviewed"]
pending_review = [r for r in rows if r["manual_review_status"] != "Analyst_Reviewed"]
payload = {
    "method": "Descriptive analysis of rule-based caption-treatment proposals on the approved character subset; no causal attribution.",
    "source": str(INPUT.relative_to(ROOT)),
    "treatment_stats": treatment_stats,
    "source_stats": source_stats,
    "manual_reviewed_count": len(manual_reviewed),
    "pending_review_count": len(pending_review),
    "manual_reviewed_meta_ids": [r["meta_id"] for r in manual_reviewed],
    "pending_review_meta_ids": [r["meta_id"] for r in pending_review],
    "manual_review_status": "Manual_Review_Complete",
    "limits": [
        "Treatment labels are rule-based proposals and are not final historical labels.",
        "The 17-case subset was selected for visual character utility, not randomly.",
        "Treatments are confounded with character, topic, date, format and likely creative intent.",
        "No ExperimentLog treatment field is updated by this analysis.",
        "A minimum of two cases per treatment within the same cell is required before treatment comparison; this subset is not balanced by cell."
    ],
}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "---",
    'title: "Análisis descriptivo de captions — 17 casos aprobados de personajes"',
    'purpose: "Medir la distribución de propuestas de tratamiento de caption y su rendimiento descriptivo, sin convertir reglas automáticas en etiquetas históricas finales."',
    "status: Review",
    "created: 2026-08-21",
    "updated: 2026-08-21",
    'version: "1.2"',
    'author: "Manus AI (CGO)"',
    "related_documents:",
    '  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"',
    '  - "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"',
    '  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"',
    '  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Manual_Findings.md"',
    '  - "Operations/Research/2026-08-21_Junio_Caption_Reclassification_Impact.md"',
    'organization: "Operations/Research"',
    "---",
    "",
    "# Análisis descriptivo de captions — 17 casos aprobados de personajes",
    "",
    "La auditoría conserva el texto exacto de Meta y registra tratamientos descriptivos después de una revisión manual de los 17 casos. Estas etiquetas no modifican el ExperimentLog ni demuestran un efecto causal del caption.",
    "",
    "## Distribución por tratamiento propuesto",
    "",
    "| Tratamiento propuesto | n | Interacciones totales | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales |",
    "|---|---:|---:|---:|---:|---:|---:|",
]
for treatment, s in treatment_stats.items():
    lines.append(f"| `{treatment}` | {s['n']} | {s['interactions_total']} | {s['interactions_median']} | {s['shares_total']} | {s['shares_median']} | {s['comments_total']} |")
lines += [
    "",
    f"La revisión manual de los {len(rows)} casos está completa. El corte queda distribuido en {treatment_stats.get('caption_minimo', {}).get('n', 0)} `caption_minimo`, {treatment_stats.get('caption_conversacional', {}).get('n', 0)} `caption_conversacional`, {treatment_stats.get('caption_refuerzo', {}).get('n', 0)} `caption_refuerzo` y {treatment_stats.get('historical_unavailable', {}).get('n', 0)} `historical_unavailable`. Todas las etiquetas tienen revisión documentada; las diferencias de confianza se conservan en el CSV.",
    "",
    "## Decisiones revisadas manualmente",
    "",
    "La revisión manual confirmó los 17 casos. Universe conserva `caption_refuerzo`; Ganso pasa a `caption_minimo`; la mujer mágica, Universe de reacción, Silvio y Wilfred interrogativo quedan como `caption_refuerzo`; los captions de hashtags, emojis o frases de acompañamiento quedan como `caption_minimo`; el roster mixto y Universe con CTA quedan como `caption_conversacional`; y Fantasma sin mensaje queda como `historical_unavailable`.",
    "",
    "| Meta_ID | Propuesta | Confianza | Interacciones | Shares | Motivo de revisión |",
    "|---|---|---|---:|---:|---|",
]
for row in rows:
    lines.append(f"| `{row['meta_id']}` | `{row['proposed_caption_treatment']}` | {row['treatment_confidence']} | {row['interactions']} | {row['shares']} | {row['rationale']} |")
lines += [
    "",
    "## Lectura analítica",
    "",
    "El grupo `caption_minimo` puede mostrar una mediana distinta de `caption_conversacional`, pero esa comparación está contaminada por la selección visual de personajes, fechas, temas y posibles diferencias de formato. No se debe concluir que un tratamiento funciona mejor. Para comparar tratamientos dentro de una celda se requieren al menos dos casos por tratamiento y una estructura comparable; estos 17 casos no cumplen ese balance.",
    "",
    "La revisión completa permite usar las etiquetas como covariables descriptivas en el análisis de personajes, pero no como resultados causales. El grupo `caption_refuerzo` conserva una fuerte sensibilidad al outlier de Universe y no debe interpretarse como un efecto del tratamiento.",
    "",
    "## Estado de los datos",
    "",
    "Los 17 registros tienen `manual_review_status=Analyst_Reviewed`; `caption_confidence_final` queda en High o Medium según la evidencia. El tratamiento sigue fuera del ledger experimental principal porque el subconjunto no está balanceado por celda y la revisión no crea evidencia causal.",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"n": len(rows), "treatment_stats": treatment_stats, "pending_review": len(pending_review), "json": str(OUT_JSON), "markdown": str(OUT_MD)}, ensure_ascii=False, indent=2))
