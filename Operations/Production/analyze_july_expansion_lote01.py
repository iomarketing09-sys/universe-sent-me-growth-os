#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "Operations/Research/Historical_Performance_Individuals.csv"
REVIEWED = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv"
OUT_JSON = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Analysis.json"
OUT_MD = ROOT / "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Analysis.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def n(row: dict[str, str], field: str) -> int:
    return int(float(row.get(field) or 0))


def median(values: list[int]) -> float:
    return statistics.median(values) if values else 0


def summarize(rows: list[dict[str, str]]) -> dict:
    interactions = [n(row, "metric_value") for row in rows]
    shares = [n(row, "shares") for row in rows]
    comments = [n(row, "comments") for row in rows]
    return {
        "n": len(rows),
        "interactions_total": sum(interactions),
        "interactions_median": median(interactions),
        "interactions_mean": round(sum(interactions) / len(interactions), 2) if rows else 0,
        "shares_total": sum(shares),
        "shares_median": median(shares),
        "comments_total": sum(comments),
        "comments_median": median(comments),
        "share_rate_median": median([round(s / i, 4) if i else 0 for s, i in zip(shares, interactions)]),
    }


def group_by(rows: list[dict[str, str]], field: str) -> dict[str, dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[row.get(field) or "No determinado"].append(row)
    return {key: summarize(value) for key, value in sorted(groups.items())}


def explode_group(rows: list[dict[str, str]], field: str) -> dict[str, dict]:
    groups = defaultdict(list)
    for row in rows:
        values = [value.strip() for value in (row.get(field) or "No determinado").split(";") if value.strip()]
        for value in values:
            groups[value].append(row)
    return {key: summarize(value) for key, value in sorted(groups.items())}


def markdown(payload: dict) -> str:
    def table(data: dict[str, dict], label: str) -> str:
        lines = [f"### {label}", "", "| Grupo | n | Mediana interacciones | Mediana shares | Mediana comentarios |", "|---|---:|---:|---:|---:|"]
        for key, value in data.items():
            lines.append(f"| {key} | {value['n']} | {value['interactions_median']} | {value['shares_median']} | {value['comments_median']} |")
        return "\n".join(lines)

    s = payload["expanded_lot"]
    b = payload["coverage"]
    return f'''---
title: "Análisis de ampliación individual de julio — lote 01"
purpose: "Medir el valor descriptivo de 16 publicaciones de julio reconciliadas visualmente, aplicar taxonomía conservadora y preparar la siguiente fase de celdas comparables."
status: Review
created: 2026-08-21
updated: 2026-08-21
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-21_Julio_Expansion_Individual_Lote01.csv"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Findings.md"
  - "Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv"
  - "Operations/Research/2026-08-17_Analisis_Julio_Taxonomia_y_Pendientes_Growth_OS.md"
  - "Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md"
organization: "Operations/Research"
---

# Análisis de ampliación individual de julio — lote 01

## Alcance

El lote fue construido como la unión de las 12 publicaciones de julio con más shares y las 12 con más comentarios, excluyendo los seis top posts ya reconciliados individualmente. De los 17 candidatos iniciales, 16 obtuvieron un match visual Meta→Drive de alta confianza; un caso permanece en `Candidate_Review`. Los 16 casos confirmados se integraron al ledger histórico sin crear CNT.

| Capa | Antes del lote | Después del lote | Lectura |
|---|---:|---:|---|
| Publicaciones de julio con métricas comparables | 207 | 207 | La base mensual ya estaba completa |
| Publicaciones de julio reconciliadas individualmente | 6 | 22 | La cobertura individual pasa de 2.9% a 10.6% |
| Casos con evidencia visual Meta→Drive | 6 | 22 | Incluye seis top previos y 16 nuevos |
| Casos con taxonomía visual revisada | 6 | 22 | Los 16 nuevos tienen revisión conservadora asistida |
| CNT nuevos creados | 0 | 0 | Se mantiene la regla de no creación masiva |

## Resultado de rendimiento del lote ampliado

El lote ampliado no es una muestra aleatoria de julio: fue seleccionado por shares y comentarios. Por eso sus medianas describen una cola de alto interés, no el rendimiento típico de todo el mes. Su utilidad es ampliar la evidencia individual y localizar casos comparables, no estimar uplift causal.

| Muestra | n | Interacciones totales | Mediana interacciones | Mediana shares | Mediana comentarios |
|---|---:|---:|---:|---:|---:|
| Seis top posts originales | {payload['original_six']['n']} | {payload['original_six']['interactions_total']} | {payload['original_six']['interactions_median']} | {payload['original_six']['shares_median']} | {payload['original_six']['comments_median']} |
| 16 nuevos matches | {s['n']} | {s['interactions_total']} | {s['interactions_median']} | {s['shares_median']} | {s['comments_median']} |
| 22 casos individuales de julio | {payload['all_individual_july']['n']} | {payload['all_individual_july']['interactions_total']} | {payload['all_individual_july']['interactions_median']} | {payload['all_individual_july']['shares_median']} | {payload['all_individual_july']['comments_median']} |
| Julio completo, base comparable | {payload['july_comparable']['n']} | {payload['july_comparable']['interactions_total']} | {payload['july_comparable']['interactions_median']} | {payload['july_comparable']['shares_median']} | {payload['july_comparable']['comments_median']} |

{table(payload['by_character'], 'Personaje principal observado')}

{table(payload['by_role'], 'Rol narrativo')}

{table(payload['by_humor'], 'Tipo de humor; una publicación puede aparecer en más de una categoría')}

{table(payload['by_tagging'], 'Potencial de etiquetado')}

## Lectura CGO

La ampliación mejora sustancialmente la cobertura individual de julio, pero mantiene un sesgo deliberado hacia publicaciones con shares o comentarios altos. La señal descriptiva más sólida sigue siendo la combinación de situación legible, difusión social y potencial de etiquetado; no se puede atribuir el resultado a Universe como personaje porque una parte importante de la muestra contiene recursos visuales no canónicos o personajes genéricos.

La taxonomía también confirma que el filename `Universe - Existencial` continúa siendo insuficiente. Los 16 casos nuevos incluyen Universe visualmente identificable, gatos no canónicos, objetos conceptuales, personajes genéricos, una referencia a Kiri y escenas de pareja. Esta mezcla es precisamente la razón por la que la clasificación debe conservar evidencia visual y nivel de confianza por fila.

El lote queda listo para la siguiente fase: revisar qué casos completan celdas comparables. No se deben declarar nuevas señales operativas todavía. Los tratamientos de caption se mantienen como `historical_unavailable` y no se estima su efecto.

## Limitaciones

Las métricas son lifetime históricas y no son ventanas de 24/72 horas. El lote no representa el promedio de julio, porque fue seleccionado por rendimiento social. La clasificación asistida fue revisada de forma conservadora; cualquier modificación canónica requiere revisión separada con Claude. El caso borderline `1036844829507460_122142624879072582` no está incluido en las 16 filas confirmadas.

## Referencias

[1]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Visual_Findings.md` — evidencia visual y estado de los 17 candidatos.
[2]: `Operations/Research/2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv` — taxonomía revisada de los 16 matches.
[3]: `Operations/Research/Historical_Performance_Individuals.csv` — ledger individual histórico actualizado.
[4]: `Operations/Research/2026-08-20_Comparativo_Crecimiento_Junio_Julio.json` — referencia comparable completa de julio.
[5]: `Operations/Research/2026-08-20_Propuesta_Expansion_Celdas_Comparables.md` — umbrales para completar las celdas narrativas.
'''


def main() -> None:
    historical = read_csv(HISTORICAL)
    july = [row for row in historical if row.get("period") == "Julio_2026"]
    original = [row for row in july if row.get("role") == "July top post"]
    expanded = [row for row in july if row.get("role") == "July expansion lot 01"]
    reviewed = read_csv(REVIEWED)
    july_comparable = []
    comparable_path = ROOT / "Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv"
    with comparable_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if row.get("month") == "2026-07":
                july_comparable.append({"metric_value": row.get("interactions", "0"), "shares": row.get("shares", "0"), "comments": row.get("comments", "0")})

    payload = {
        "created": "2026-08-21",
        "coverage": {"july_comparable": len(july_comparable), "july_individual_before": 6, "july_individual_after": len(july), "confirmed_new_matches": len(expanded), "borderline_excluded": 1},
        "original_six": summarize(original),
        "expanded_lot": summarize(expanded),
        "all_individual_july": summarize(july),
        "july_comparable": summarize(july_comparable),
        "by_character": group_by(expanded, "personaje_principal_normalizado"),
        "by_role": group_by(expanded, "rol_narrativo"),
        "by_humor": explode_group(expanded, "tipo_humor_normalizado"),
        "by_tagging": group_by(expanded, "potencial_etiquetado"),
        "reviewed_taxonomy_rows": len(reviewed),
        "guardrails": ["Lifetime only", "Selected by shares/comments", "No CNT created", "No canon change", "Caption treatment historical_unavailable"],
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(payload), encoding="utf-8")
    print(json.dumps({"output_json": str(OUT_JSON), "output_md": str(OUT_MD), "coverage": payload["coverage"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
