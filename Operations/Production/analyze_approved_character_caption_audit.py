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
    "manual_review_status": "Partial_Manual_Review_Complete",
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
    'version: "1.0"',
    'author: "Manus AI (CGO)"',
    "related_documents:",
    '  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"',
    '  - "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"',
    '  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"',
    'organization: "Operations/Research"',
    "---",
    "",
    "# Análisis descriptivo de captions — 17 casos aprobados de personajes",
    "",
    "La auditoría conserva el texto exacto de Meta y genera una propuesta de tratamiento mediante reglas explícitas. Esta clasificación sirve para detectar qué casos merecen revisión manual; no modifica el ExperimentLog ni demuestra un efecto causal del caption.",
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
    "Tras la revisión manual de cuatro casos, el corte queda distribuido en ocho `caption_minimo`, seis `caption_conversacional`, dos `caption_refuerzo` y uno `historical_unavailable`. Los otros 13 casos siguen pendientes porque varias etiquetas dependen de si el caption ilumina la imagen, repite el texto visual o solo añade hashtags.",
    "",
    "## Casos que requieren revisión manual prioritaria",
    "",
    "La revisión manual confirmó cuatro casos: el outlier de Universe queda como `caption_refuerzo`, el caso de Ganso pasa a `caption_minimo`, el Wilfred corto conserva `caption_refuerzo` con ambigüedad y el Fantasma sin mensaje queda como `historical_unavailable`. Los 13 restantes siguen pendientes; en particular, las propuestas `caption_conversacional` requieren comprobar que existe una invitación real y no solo una pregunta retórica o una palabra interrogativa.",
    "",
    "| Meta_ID | Propuesta | Confianza | Interacciones | Shares | Motivo de revisión |",
    "|---|---|---|---:|---:|---|",
]
for row in manual_reviewed:
    lines.append(f"| `{row['meta_id']}` | `{row['proposed_caption_treatment']}` | {row['treatment_confidence']} | {row['interactions']} | {row['shares']} | {row['rationale']} |")
lines += [
    "",
    "## Lectura analítica",
    "",
    "El grupo `caption_minimo` puede mostrar una mediana distinta de `caption_conversacional`, pero esa comparación está contaminada por la selección visual de personajes, fechas, temas y posibles diferencias de formato. No se debe concluir que un tratamiento funciona mejor. Para comparar tratamientos dentro de una celda se requieren al menos dos casos por tratamiento y una estructura comparable; estos 17 casos no cumplen ese balance.",
    "",
    "La única decisión válida en este momento es descriptiva: cuatro casos ya tienen revisión manual documentada y 13 permanecen pendientes. Las etiquetas confirmadas podrán usarse como covariable descriptiva en el análisis de personajes, pero no como resultado causal.",
    "",
    "## Estado de los datos",
    "",
    "Cuatro registros tienen `manual_review_status=Analyst_Reviewed`; los otros 13 permanecen en `Pending_Manual_Caption_Review`. El tratamiento no se copia al ledger experimental principal hasta que exista una revisión humana completa o una regla documental aprobada para el histórico.",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"n": len(rows), "treatment_stats": treatment_stats, "pending_review": len(pending_review), "json": str(OUT_JSON), "markdown": str(OUT_MD)}, ensure_ascii=False, indent=2))
