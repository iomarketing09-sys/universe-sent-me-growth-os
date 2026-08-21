#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"
OUT_JSON = ROOT / "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.json"
OUT_MD = ROOT / "Operations/Research/2026-08-21_Junio_57_Approved_Character_Analysis.md"

with INPUT.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

for row in rows:
    row["interactions_n"] = int(row["interactions"] or 0)
    row["shares_n"] = int(row["shares"] or 0)
    row["comments_n"] = int(row["comments"] or 0)

approved = [r for r in rows if r["approval_status"] == "Approved_Character_Analysis"]
reserve = [r for r in rows if r["approval_status"] == "Reserve_Not_Approved"]
cell_pending = [r for r in rows if r["approval_status"] == "Pending_Cell_Validation"]
controls = [r for r in rows if r["utility_class"] == "Format_Control"]
character_reserve = [r for r in rows if r["utility_class"] == "Character_Review" and r["approval_status"] != "Approved_Character_Analysis"]

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

groups = {
    "approved_character_analysis": approved,
    "character_reserve": character_reserve,
    "format_controls": controls,
    "all_reserve_not_approved": reserve,
    "pending_cell_candidate": cell_pending,
}
by_hypothesis = defaultdict(list)
for row in approved:
    by_hypothesis[row["character_hypothesis"]].append(row)

hypothesis_stats = {}
for hypothesis, group in sorted(by_hypothesis.items(), key=lambda item: (-sum(r["interactions_n"] for r in item[1]), item[0])):
    item = stats(group)
    item["meta_ids"] = [r["meta_id"] for r in group]
    item["ranks"] = [int(r["priority_rank"]) for r in group]
    hypothesis_stats[hypothesis] = item

universe_group = by_hypothesis.get("Universe visual candidate", [])
outlier = max(approved, key=lambda row: (row["interactions_n"], row["shares_n"]))
approved_without_outlier = [row for row in approved if row is not outlier]
confounder_summary = {
    "approved_interactions_share_from_universe": round(sum(r["interactions_n"] for r in universe_group) / sum(r["interactions_n"] for r in approved), 4),
    "approved_shares_share_from_universe": round(sum(r["shares_n"] for r in universe_group) / sum(r["shares_n"] for r in approved), 4),
    "approved_shares_per_interaction": round(sum(r["shares_n"] for r in approved) / sum(r["interactions_n"] for r in approved), 4),
    "format_control_shares_per_interaction": round(sum(r["shares_n"] for r in controls) / sum(r["interactions_n"] for r in controls), 4),
    "outlier_meta_id": outlier["meta_id"],
    "outlier_interactions_share": round(outlier["interactions_n"] / sum(r["interactions_n"] for r in approved), 4),
    "outlier_shares_share": round(outlier["shares_n"] / sum(r["shares_n"] for r in approved), 4),
    "selection_bias_warning": "Universe visual candidate subgroup is dominated by one high-performing transformation-like case; no character effect inferred.",
}

payload = {
    "method": "Descriptive lifetime comparison of the approved visual-character subset; no causal attribution.",
    "source": str(INPUT.relative_to(ROOT)),
    "approved_scope": "Selective character analysis only; no CNT, canon, reuse, calendar or publication.",
    "group_stats": {name: stats(group) for name, group in groups.items()},
    "approved_without_outlier": stats(approved_without_outlier),
    "hypothesis_stats": hypothesis_stats,
    "confounder_summary": confounder_summary,
    "top_approved_by_interactions": [
        {"meta_id": r["meta_id"], "rank": int(r["priority_rank"]), "hypothesis": r["character_hypothesis"], "interactions": r["interactions_n"], "shares": r["shares_n"], "comments": r["comments_n"]}
        for r in sorted(approved, key=lambda x: (-x["interactions_n"], -x["shares_n"]))
    ],
    "limits": [
        "Selection was based on visual utility, not random sampling.",
        "Character hypotheses are not canonical identity assignments.",
        "Lifetime metrics are descriptive and include low/zero values.",
        "No timing, caption or asset-match control is available for this queue.",
        "The subset is too small and selected to infer character causality or a ranking."
    ],
}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "---",
    'title: "Análisis cuantitativo — 17 casos aprobados de personajes en junio"',
    'purpose: "Describir la distribución de lifetime interactions, shares y comments del subconjunto aprobado sin atribuir causalidad al personaje."',
    "status: Active",
    "created: 2026-08-21",
    "updated: 2026-08-21",
    'version: "1.1"',
    'author: "Manus AI (CGO)"',
    "related_documents:",
    '  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Character_Utility.csv"',
    '  - "Operations/Research/2026-08-21_Junio_57_Unmatched_Visual_Findings.md"',
    '  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"',
    '  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"',
    'organization: "Operations/Research"',
    "---",
    "",
    "# Análisis cuantitativo — 17 casos aprobados de personajes en junio",
    "",
    "Este corte es descriptivo. Los 17 casos fueron seleccionados por utilidad visual y no constituyen una muestra aleatoria; por lo tanto, sus medianas no pueden interpretarse como efecto causal de Universe, Wilfred, Ganso, Fantasma, Silvio u otro personaje.",
    "",
    "## Comparación de grupos",
    "",
    "| Grupo | n | Interacciones totales | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales | Mediana comentarios |",
    "|---|---:|---:|---:|---:|---:|---:|---:|",
]
for name, label in [
    ("approved_character_analysis", "17 aprobados para personajes"),
    ("character_reserve", "2 reservas de personaje"),
    ("format_controls", "36 controles de formato"),
    ("pending_cell_candidate", "1 candidato de celda"),
]:
    s = payload["group_stats"][name]
    lines.append(f"| {label} | {s['n']} | {s['interactions_total']} | {s['interactions_median']} | {s['shares_total']} | {s['shares_median']} | {s['comments_total']} | {s['comments_median']} |")
lines += [
    "",
    "La lectura principal es que el subconjunto aprobado concentra señales visuales útiles, pero no puede competir limpiamente contra los controles porque fue seleccionado por legibilidad de personaje. El grupo se utiliza para validar identidad, rol y comparabilidad; no para declarar que un personaje rinde mejor.",
    "",
    "## Confusores y sensibilidad descriptiva",
    "",
    f"El grupo Universe suma {sum(r['interactions_n'] for r in universe_group)} de las {sum(r['interactions_n'] for r in approved)} interacciones aprobadas ({confounder_summary['approved_interactions_share_from_universe']:.1%}) y {sum(r['shares_n'] for r in universe_group)} de los {sum(r['shares_n'] for r in approved)} shares ({confounder_summary['approved_shares_share_from_universe']:.1%}). Esta concentración se debe principalmente al caso de 164 interacciones y 42 shares, por lo que cualquier lectura por personaje queda dominada por un outlier visual/estructural.",
    f"La razón shares/interacción es {confounder_summary['approved_shares_per_interaction']:.1%} en los 17 aprobados y {confounder_summary['format_control_shares_per_interaction']:.1%} en los 36 controles. La diferencia es solo descriptiva: ambos grupos tienen distinta selección visual, distinta composición y no comparten control de hora, caption o temática.",
    f"El outlier {outlier['meta_id']} representa {confounder_summary['outlier_interactions_share']:.1%} de las interacciones y {confounder_summary['outlier_shares_share']:.1%} de los shares del subconjunto aprobado. Sin ese caso, el grupo baja a {stats(approved_without_outlier)['interactions_total']} interacciones totales, mediana de {stats(approved_without_outlier)['interactions_median']} interacciones, {stats(approved_without_outlier)['shares_total']} shares y mediana de {stats(approved_without_outlier)['shares_median']} shares.",
    "",
    "## Distribución por hipótesis visual",
    "",
    "| Hipótesis visual | n | Mediana interacciones | Shares totales | Mediana shares | Comentarios totales |",
    "|---|---:|---:|---:|---:|---:|",
]
for hypothesis, s in hypothesis_stats.items():
    lines.append(f"| {hypothesis} | {s['n']} | {s['interactions_median']} | {s['shares_total']} | {s['shares_median']} | {s['comments_total']} |")
lines += [
    "",
    "## Casos de mayor valor descriptivo",
    "",
    "| Meta_ID | Hipótesis visual | Interacciones | Shares | Comentarios | Lectura |",
    "|---|---|---:|---:|---:|---|",
]
for item in payload["top_approved_by_interactions"][:8]:
    lines.append(f"| `{item['meta_id']}` | {item['hypothesis']} | {item['interactions']} | {item['shares']} | {item['comments']} | Prioridad descriptiva; no prueba causalidad |")
lines += [
    "",
    "## Conclusión operativa",
    "",
    "Los 17 casos aprobados quedan listos para análisis de identidad y taxonomía, pero no justifican un ranking de personajes ni una regla de producción. La siguiente ampliación debe preguntar si una señal visual se mantiene dentro de una celda comparable, con controles de estructura y tema; no si un personaje es intrínsecamente mejor.",
    "",
    "El candidato `1036844829507460_122127951885072582` se mantiene fuera de este corte de personajes porque su pregunta principal es estructural: cuatro paneles, turnos claros y remate. Su validación está definida por separado como `Pending_Cell_Validation`.",
    "",
    "## Limitaciones",
    "",
    "La selección no es aleatoria, los captions históricos no están disponibles de forma homogénea, el match Drive no está cerrado para estos 17 casos y no existe control equilibrado de hora. Por estas razones, este documento no modifica canon ni reglas de calendario.",
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"approved": len(approved), "character_reserve": len(character_reserve), "format_controls": len(controls), "json": str(OUT_JSON), "markdown": str(OUT_MD)}, ensure_ascii=False, indent=2))
