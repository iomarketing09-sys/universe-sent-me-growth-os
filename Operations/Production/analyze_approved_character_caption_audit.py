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

ambiguous = [r for r in rows if r["treatment_confidence"] == "Low" or r["proposed_caption_treatment"] == "historical_unavailable"]
payload = {
    "method": "Descriptive analysis of rule-based caption-treatment proposals on the approved character subset; no causal attribution.",
    "source": str(INPUT.relative_to(ROOT)),
    "treatment_stats": treatment_stats,
    "source_stats": source_stats,
    "ambiguous_or_unavailable_count": len(ambiguous),
    "ambiguous_or_unavailable_meta_ids": [r["meta_id"] for r in ambiguous],
    "manual_review_status": "Pending_Manual_Caption_Review",
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
    "La propuesta automática distribuye los casos en siete `caption_minimo`, seis `caption_conversacional`, tres `caption_refuerzo` y uno `historical_unavailable`. Sin embargo, la confianza final permanece sin confirmar: varias etiquetas dependen de si el caption ilumina la imagen, repite el texto visual o solo añade hashtags.",
    "",
    "## Casos que requieren revisión manual prioritaria",
    "",
    "Los tres casos propuestos como `caption_refuerzo` tienen confianza baja porque una frase breve puede estar reforzando la lectura o simplemente acompañando una imagen ya autosuficiente. Los seis casos propuestos como `caption_conversacional` requieren comprobar que existe una invitación real y no solo una pregunta retórica o una palabra interrogativa. El caso `historical_unavailable` no debe ser rellenado por inferencia.",
    "",
    "| Meta_ID | Propuesta | Confianza | Interacciones | Shares | Motivo de revisión |",
    "|---|---|---|---:|---:|---|",
]
for row in ambiguous:
    lines.append(f"| `{row['meta_id']}` | `{row['proposed_caption_treatment']}` | {row['treatment_confidence']} | {row['interactions']} | {row['shares']} | {row['rationale']} |")
lines += [
    "",
    "## Lectura analítica",
    "",
    "El grupo `caption_minimo` puede mostrar una mediana distinta de `caption_conversacional`, pero esa comparación está contaminada por la selección visual de personajes, fechas, temas y posibles diferencias de formato. No se debe concluir que un tratamiento funciona mejor. Para comparar tratamientos dentro de una celda se requieren al menos dos casos por tratamiento y una estructura comparable; estos 17 casos no cumplen ese balance.",
    "",
    "La única decisión válida en este momento es de priorización: revisar primero los casos de confianza baja y conservar el texto Meta exacto. Una vez confirmadas manualmente las etiquetas, podrán usarse como covariable descriptiva en el análisis de personajes, pero no como resultado causal.",
    "",
    "## Estado de los datos",
    "",
    "Todos los registros permanecen en `Pending_Manual_Caption_Review` y `caption_confidence_final=Unconfirmed`. El tratamiento no se copia al ledger experimental principal hasta que exista una revisión humana o una regla documental aprobada para el histórico.",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"n": len(rows), "treatment_stats": treatment_stats, "ambiguous": len(ambiguous), "json": str(OUT_JSON), "markdown": str(OUT_MD)}, ensure_ascii=False, indent=2))
