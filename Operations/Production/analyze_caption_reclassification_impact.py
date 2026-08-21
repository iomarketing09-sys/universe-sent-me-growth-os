#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"
OUT_JSON = ROOT / "Operations/Research/2026-08-21_Junio_Caption_Reclassification_Impact.json"
OUT_MD = ROOT / "Operations/Research/2026-08-21_Junio_Caption_Reclassification_Impact.md"

with INPUT.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))
for row in rows:
    row["interactions_n"] = int(row["interactions"] or 0)
    row["shares_n"] = int(row["shares"] or 0)
    row["comments_n"] = int(row["comments"] or 0)

# Preserve the original rule-based label in the audit so the pre-review
# distribution remains reproducible even after manual overrides.
PRE_OVERRIDE = {r["meta_id"]: r["rule_based_treatment"] for r in rows}


def group_stats(group):
    if not group:
        return {"n": 0, "interactions_total": 0, "interactions_median": None, "shares_total": 0, "shares_median": None, "comments_total": 0, "comments_median": None, "share_rate": None}
    interactions = sum(r["interactions_n"] for r in group)
    shares = sum(r["shares_n"] for r in group)
    comments = sum(r["comments_n"] for r in group)
    return {
        "n": len(group),
        "interactions_total": interactions,
        "interactions_median": statistics.median(r["interactions_n"] for r in group),
        "shares_total": shares,
        "shares_median": statistics.median(r["shares_n"] for r in group),
        "comments_total": comments,
        "comments_median": statistics.median(r["comments_n"] for r in group),
        "share_rate": round(shares / interactions, 4) if interactions else None,
    }


def stats_by(field_map):
    groups = defaultdict(list)
    for row in rows:
        groups[field_map[row["meta_id"]]].append(row)
    return {key: group_stats(value) for key, value in sorted(groups.items())}

pre = stats_by(PRE_OVERRIDE)
post = stats_by({r["meta_id"]: r["proposed_caption_treatment"] for r in rows})
all_stats = group_stats(rows)
changed = []
for row in rows:
    before = PRE_OVERRIDE[row["meta_id"]]
    after = row["proposed_caption_treatment"]
    if before != after:
        changed.append({
            "meta_id": row["meta_id"],
            "character_hypothesis": row["character_hypothesis"],
            "before": before,
            "after": after,
            "interactions": row["interactions_n"],
            "shares": row["shares_n"],
            "comments": row["comments_n"],
        })
confirmed_unchanged = [
    {"meta_id": row["meta_id"], "character_hypothesis": row["character_hypothesis"], "treatment": row["proposed_caption_treatment"], "interactions": row["interactions_n"], "shares": row["shares_n"], "comments": row["comments_n"]}
    for row in rows if row["meta_id"] == "1036844829507460_122130196011072582"
]
ganso = next(row for row in changed if row["meta_id"] == "1036844829507460_122134608507072582")
universe = confirmed_unchanged[0]

payload = {
    "period": "June approved character subset",
    "n": len(rows),
    "metrics_total": all_stats,
    "pre_override": pre,
    "post_manual_review": post,
    "changed_assignments": changed,
    "confirmed_unchanged": confirmed_unchanged,
    "requested_focus": {
        "ganso": ganso,
        "universe": universe,
        "direct_effect": "Ganso moves between descriptive groups; Universe remains in caption_refuerzo. Neither post-level metrics nor total-period metrics change."
    },
    "interpretation": [
        "Reclassification does not change any post-level interaction, share or comment value; it only moves a row between descriptive treatment groups.",
        "Ganso is the only treatment assignment that changed from caption_refuerzo to caption_minimo; four additional conversational cases moved to caption_refuerzo during full manual review.",
        "Universe was manually confirmed as caption_refuerzo, so its metrics remain in that group.",
        "The final caption_refuerzo median is compositional: four conversational rows enter while Ganso exits, and the Universe outlier remains; this is not causal evidence.",
        "The total subset remains 300 interactions, 53 shares and 13 comments."
    ],
    "limits": [
        "The pre-override distribution reconstructs the documented rule-based state; it is not a new Meta measurement.",
        "The subset is selected for character utility and is not a balanced caption experiment.",
        "No ExperimentLog or editorial metric ledger was changed."
    ],
}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "---",
    'title: "Impacto de reclasificaciones de captions — Ganso y Universe"',
    'purpose: "Medir cuánto cambia la lectura agregada de engagement al mover Ganso a caption_minimo y confirmar Universe como caption_refuerzo, sin alterar métricas post-level."',
    "status: Active",
    "created: 2026-08-21",
    "updated: 2026-08-21",
    'version: "1.0"',
    'author: "Manus AI (CGO)"',
    "related_documents:",
    '  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Audit.csv"',
    '  - "Operations/Research/2026-08-21_Junio_Approved_Character_Caption_Manual_Findings.md"',
    '  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"',
    'organization: "Operations/Research"',
    "---",
    "",
    "# Impacto de las reclasificaciones",
    "",
    "La reclasificación modifica únicamente la pertenencia descriptiva a un grupo de caption. No modifica interacciones, shares, comentarios, fecha, post, contenido ni el ExperimentLog.",
    "",
    "## Cambio de asignaciones",
    "",
    "| Caso | Antes de revisión | Después de revisión | Interacciones | Shares | Comentarios |",
    "|---|---|---|---:|---:|---:|",
]
for item in changed:
    lines.append(f"| `{item['meta_id']}` ({item['character_hypothesis']}) | `{item['before']}` | `{item['after']}` | {item['interactions']} | {item['shares']} | {item['comments']} |")
lines += [
    "| `1036844829507460_122130196011072582` (Universe) | `caption_refuerzo` | `caption_refuerzo` confirmado | 164 | 42 | 2 |",
    "",
    "## Comparación agregada antes/después",
    "",
    "| Tratamiento | n antes | Interacciones antes | Shares antes | Comentarios antes | n después | Interacciones después | Shares después | Comentarios después |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
]
for treatment in sorted(set(pre) | set(post)):
    a = pre.get(treatment, group_stats([]))
    b = post.get(treatment, group_stats([]))
    lines.append(f"| `{treatment}` | {a['n']} | {a['interactions_total']} | {a['shares_total']} | {a['comments_total']} | {b['n']} | {b['interactions_total']} | {b['shares_total']} | {b['comments_total']} |")
lines += [
    "",
    "El total del subconjunto permanece en **300 interacciones, 53 shares y 13 comentarios**. El efecto directo solicitado es la transferencia de Ganso: 14 interacciones, 2 shares y 3 comentarios salen de `caption_refuerzo` y entran a `caption_minimo`. Universe no se mueve y sigue aportando 164 interacciones y 42 shares al grupo de refuerzo. La revisión completa también movió cuatro captions conversacionales a refuerzo; esos cambios deben analizarse por separado del efecto Ganso/Universe.",
    "",
    "La mediana de `caption_refuerzo` cambia de 7 a 6.5 interacciones después de la revisión completa porque cuatro casos conversacionales entran al grupo y Ganso sale; el grupo final conserva el outlier de Universe. La diferencia es composicional y no significa que `caption_refuerzo` haya mejorado ni que `caption_minimo` haya empeorado.",
    "",
    "## Decisión de uso",
    "",
    "La reclasificación de Ganso debe conservarse como corrección taxonómica descriptiva. La confirmación de Universe debe conservarse como revisión manual del tratamiento, pero ninguno de los dos cambios autoriza una conclusión causal ni una actualización del ExperimentLog. La comparación de tratamientos permanece descriptiva porque el subconjunto no está balanceado por celda; la revisión manual completa no crea evidencia causal.",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"json": str(OUT_JSON), "markdown": str(OUT_MD), "changed": changed, "pre": pre, "post": post}, ensure_ascii=False, indent=2))
