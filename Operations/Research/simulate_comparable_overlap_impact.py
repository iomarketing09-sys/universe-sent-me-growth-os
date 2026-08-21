from __future__ import annotations

import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = ROOT / "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"
BRIEFS = ROOT / "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
WAVE1 = ROOT / "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"
OUTPUT_CSV = ROOT / "Operations/Research/2026-08-21_Simulacion_Impacto_Solapamientos_Comparables.csv"
OUTPUT_MD = ROOT / "Operations/Research/2026-08-21_Simulacion_Impacto_Solapamientos_Comparables.md"

CELL_MAP = {
    "MICRO-STRICT-3P": ["MICRO-001"],
    "TRANS-UNIVERSE": ["TRANS-001", "TRANS-002"],
    "ACID-DIALOGUE": ["DIA-001", "DIA-002"],
}

FAMILY_OVERLAPS = {
    "FUT-MICRO-005": ["FAM-03"],
    "FUT-MICRO-006": ["FAM-02", "FAM-03"],
    "FUT-TRANS-003": ["FAM-05"],
    "FUT-ACID-003": ["FAM-04"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def number(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value in ("", "null", "None"):
        raise ValueError(f"Valor vacío para {key}: {row}")
    return float(value)


def summary(values: list[float]) -> tuple[float, float]:
    return statistics.mean(values), statistics.median(values)


def pct_change(new: float, old: float) -> float | None:
    return None if old == 0 else (new - old) / old * 100


def build_metric_scenarios(candidate_rows: list[dict[str, str]], brief_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_candidate_id = {row["Cell_ID"]: row for row in candidate_rows}
    results: list[dict[str, str]] = []
    for brief in brief_rows:
        brief_id = brief["Brief_ID"]
        cell_id = brief["Cell_ID"]
        candidate_ids = CELL_MAP[cell_id]
        cell_rows = [by_candidate_id[candidate_id] for candidate_id in candidate_ids]
        for metric_key in ("Interacciones", "Shares"):
            base_values = [number(row, metric_key) for row in cell_rows]
            base_mean, base_median = summary(base_values)
            base_max = max(base_values)
            for scenario, new_value in (
                ("cell_median", base_median),
                ("cell_mean", base_mean),
                ("cell_max", base_max),
            ):
                clean_values = base_values + [new_value]
                contaminated_values = base_values + [new_value, new_value]
                clean_mean, clean_median = summary(clean_values)
                contaminated_mean, contaminated_median = summary(contaminated_values)
                results.append(
                    {
                        "Record_Type": "Metric_Sensitivity",
                        "Brief_ID": brief_id,
                        "Cell_ID": cell_id,
                        "Metric": metric_key,
                        "Scenario": scenario,
                        "Historical_n": str(len(base_values)),
                        "Clean_n": str(len(clean_values)),
                        "Contaminated_n": str(len(contaminated_values)),
                        "New_Case_Value": f"{new_value:.2f}",
                        "Clean_Mean": f"{clean_mean:.2f}",
                        "Contaminated_Mean": f"{contaminated_mean:.2f}",
                        "Mean_Bias_Pct": "" if pct_change(contaminated_mean, clean_mean) is None else f"{pct_change(contaminated_mean, clean_mean):.2f}",
                        "Clean_Median": f"{clean_median:.2f}",
                        "Contaminated_Median": f"{contaminated_median:.2f}",
                        "Median_Bias_Pct": "" if pct_change(contaminated_median, clean_median) is None else f"{pct_change(contaminated_median, clean_median):.2f}",
                        "Denominator_Overstatement_Pct": f"{(len(contaminated_values) - len(clean_values)) / len(clean_values) * 100:.2f}",
                        "Overlap_Family": "",
                        "Wave1_Planned_n": "",
                        "Wave1_Contaminated_n": "",
                        "Wave1_Denominator_Overstatement_Pct": "",
                        "Wave1_Duplicate_Share_Pct": "",
                        "Schedule_Overlap": "",
                        "Caption_Treatment_Overlap": "",
                        "Interpretation": "La misma pieza se cuenta dos veces dentro de la celda: el escenario contaminado añade una copia del caso nuevo; no representa rendimiento adicional real.",
                    }
                )
    return results


def build_family_scenarios(brief_rows: list[dict[str, str]], wave1_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    planned_hours = {row["Planned_Hour"] for row in wave1_rows if row.get("Planned_Hour")}
    planned_captions = {row["Caption_Treatment"] for row in wave1_rows if row.get("Caption_Treatment")}
    results: list[dict[str, str]] = []
    for brief in brief_rows:
        brief_id = brief["Brief_ID"]
        for family in FAMILY_OVERLAPS[brief_id]:
            family_clean_n = 3
            family_contaminated_n = family_clean_n + 1
            results.append(
                {
                    "Record_Type": "Family_Overlap",
                    "Brief_ID": brief_id,
                    "Cell_ID": brief["Cell_ID"],
                    "Metric": "Denominator",
                    "Scenario": "one_brief_misclassified_into_Wave1_family",
                    "Historical_n": "",
                    "Clean_n": str(family_clean_n),
                    "Contaminated_n": str(family_contaminated_n),
                    "New_Case_Value": "",
                    "Clean_Mean": "",
                    "Contaminated_Mean": "",
                    "Mean_Bias_Pct": "",
                    "Clean_Median": "",
                    "Contaminated_Median": "",
                    "Median_Bias_Pct": "",
                    "Denominator_Overstatement_Pct": f"{(family_contaminated_n - family_clean_n) / family_clean_n * 100:.2f}",
                    "Overlap_Family": family,
                    "Wave1_Planned_n": str(family_clean_n),
                    "Wave1_Contaminated_n": str(family_contaminated_n),
                    "Wave1_Denominator_Overstatement_Pct": f"{(family_contaminated_n - family_clean_n) / family_clean_n * 100:.2f}",
                    "Wave1_Duplicate_Share_Pct": f"{1 / family_contaminated_n * 100:.2f}",
                    "Schedule_Overlap": "Yes" if brief["Hora_Test"] in planned_hours else "No",
                    "Caption_Treatment_Overlap": "Yes" if brief["Caption_Treatment"] in planned_captions else "No",
                    "Interpretation": "No hay outcomes de Wave 1 todavía; se cuantifica solo la inflación del denominador. No estimar sesgo de media/mediana sin resultados observados de la familia.",
                }
            )
    return results


def write_outputs(rows: list[dict[str, str]], brief_rows: list[dict[str, str]], wave1_rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metric_rows = [row for row in rows if row["Record_Type"] == "Metric_Sensitivity"]
    family_rows = [row for row in rows if row["Record_Type"] == "Family_Overlap"]
    planned_hours = sorted({row["Planned_Hour"] for row in wave1_rows if row.get("Planned_Hour")})
    validation_statuses = {row.get("Cross_Validation_Status", "UNREGISTERED") for row in brief_rows}
    validation_status = "PASS" if validation_statuses == {"PASS"} else ", ".join(sorted(validation_statuses))
    lines = [
        "---",
        'title: "Simulación de impacto de solapamientos semánticos — briefs comparables"',
        'purpose: "Cuantificar sensibilidad de métricas y denominadores cuando los briefs comparables se mezclan indebidamente con celdas o familias de experimentos previos."',
        "status: Active",
        "created: 2026-08-21",
        "updated: 2026-08-21",
        'version: "1.1"',
        'author: "Manus AI (CGO)"',
        "related_documents:",
        '  - "Operations/Research/2026-08-21_Validacion_Cruzada_Hipotesis_Briefs_Comparables.md"',
        '  - "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"',
        '  - "Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv"',
        '  - "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"',
        '  - "Operations/Research/simulate_comparable_overlap_impact.py"',
        'organization: "Operations/Research"',
        "---",
        "",
        "# Simulación de impacto de solapamientos semánticos",
        "",
        "## Alcance y método",
        "",
        "Esta simulación no inventa resultados futuros ni intenta estimar causalidad. Usa los valores históricos observados en las celdas comparables como escenarios de sensibilidad para un caso nuevo: `cell_median`, `cell_mean` y `cell_max`. El escenario limpio agrega una sola pieza nueva; el escenario contaminado agrega la misma pieza dos veces, simulando una doble asignación al mismo denominador. Para Wave 1 se cuantifica únicamente la inflación de `n`, porque sus outcomes todavía están pendientes.",
        "",
        "## Veredicto ejecutivo",
        "",
        f"Los cuatro briefs muestran `0` conflictos directos de IDs, pero la simulación confirma que los solapamientos sí pueden producir contaminación operativa. Cada asignación indebida de un brief a una familia Wave 1 de tres casos eleva artificialmente su denominador de `n=3` a `n=4`, un **+33.33%**, y hace que el caso duplicado represente `25.00%` del denominador contaminado. La simulación métrica de las celdas muestra que el sesgo de media depende de la distancia entre el caso nuevo y la distribución histórica; la mediana suele ser más estable, pero no debe considerarse inmune con muestras tan pequeñas.",
        "",
        "> La decisión operativa es mantener cada brief en su `Cell_ID` primaria, no sumarlo a FAM-02/FAM-03/FAM-04/FAM-05 y no interpretar el cambio de media/mediana como efecto de contenido si existe doble pertenencia.",
        "",
        "## Impacto de denominador por familia Wave 1",
        "",
        "| Brief_ID | Familia solapada | n limpio | n contaminado | Inflación del denominador | Peso del duplicado | Hora compartida | Caption compartido |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in family_rows:
        lines.append(
            f"| `{row['Brief_ID']}` | `{row['Overlap_Family']}` | {row['Wave1_Planned_n']} | {row['Wave1_Contaminated_n']} | {row['Wave1_Denominator_Overstatement_Pct']}% | {row['Wave1_Duplicate_Share_Pct']}% | {row['Schedule_Overlap']} | {row['Caption_Treatment_Overlap']} |"
        )

    lines.extend(
        [
            "",
            "La asignación de `FUT-MICRO-006` tiene dos proximidades semánticas (`FAM-02` y `FAM-03`), por lo que una clasificación indiscriminada podría contaminar dos denominadores en lugar de uno. La simulación no suma esos denominadores entre sí: los reporta como dos riesgos separados.",
            "",
            "## Sensibilidad métrica por celda",
            "",
            "| Brief_ID | Celda | Métrica | Escenario | n limpio | n contaminado | Media limpia | Media contaminada | Sesgo de media | Mediana limpia | Mediana contaminada | Sesgo de mediana |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in metric_rows:
        lines.append(
            f"| `{row['Brief_ID']}` | `{row['Cell_ID']}` | `{row['Metric']}` | `{row['Scenario']}` | {row['Clean_n']} | {row['Contaminated_n']} | {row['Clean_Mean']} | {row['Contaminated_Mean']} | {row['Mean_Bias_Pct'] or 'n/a'}% | {row['Clean_Median']} | {row['Contaminated_Median']} | {row['Median_Bias_Pct'] or 'n/a'}% |"
        )

    lines.extend(
        [
            "",
            "## Confusores adicionales",
            "",
            f"Las horas propuestas de los cuatro briefs (`16:00`, `18:00`, `20:00` y `22:00`) aparecen dentro de las franjas planificadas por Wave 1: `{', '.join(planned_hours)}`. Asimismo, los cuatro tratamientos (`caption_minimo`, `caption_refuerzo` o `caption_conversacional`) ya aparecen en la matriz Wave 1. Por ello, si una pieza se incorpora al calendario activo, `Hora_Test` y `Caption_Treatment` deben registrarse como covariables compartidas; no deben usarse como evidencia de que el solapamiento semántico causó el resultado.",
            "",
            "El archivo de candidatos contiene muestras pequeñas y heterogéneas: la celda de transformación mezcla `164` y `7` interacciones; diálogo ácido mezcla `521` y `394`; microhistoria estricta tiene `n=1`. Los escenarios altos no son expectativas: solo muestran cuánto puede moverse la media cuando se duplica un caso extremo.",
            "",
            "## Decisión operativa",
            "",
            f"1. Mantener `Cross_Validation_Status={validation_status}`. El registro formal de HB-006 a HB-009 no autoriza generación; cualquier cambio a `PASS_WITH_WARNINGS` vuelve a bloquear la promoción.",
            "2. Mantener `MICRO-STRICT-3P`, `TRANS-UNIVERSE` y `ACID-DIALOGUE` fuera de los agregados Wave 1 aunque compartan tema, personaje, caption u horario.",
            "3. No combinar `FUT-MICRO-006` con FAM-02 y FAM-03 simultáneamente; si se estudia la proximidad, elegir una sola celda primaria y registrar la otra como riesgo semántico.",
            "4. Reportar siempre métricas con y sin outlier, además de `n` limpio y `n` contaminado; no cerrar ninguna hipótesis con esta simulación.",
            "",
            "## Limitaciones",
            "",
            "La simulación no produce outcomes de Wave 1, no estima conversiones, no corrige diferencias de calidad visual y no sustituye una prueba balanceada. Su función es demostrar el costo de una doble pertenencia y señalar qué variables deben mantenerse separadas en el análisis futuro.",
            "",
            "## Referencias",
            "",
            "[1]: `Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv` — outcomes históricos por celda.",
            "[2]: `Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv` — familias, horarios y tratamientos planificados.",
            "[3]: `Operations/Research/2026-08-21_Validacion_Cruzada_Hipotesis_Briefs_Comparables.md` — conflictos y solapamientos identificados.",
        ]
    )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    candidate_rows = read_csv(CANDIDATES)
    brief_rows = read_csv(BRIEFS)
    wave1_rows = read_csv(WAVE1)
    results = build_metric_scenarios(candidate_rows, brief_rows) + build_family_scenarios(brief_rows, wave1_rows)
    write_outputs(results, brief_rows, wave1_rows)
    print(f"metric_scenarios={sum(row['Record_Type'] == 'Metric_Sensitivity' for row in results)}")
    print(f"family_overlap_rows={sum(row['Record_Type'] == 'Family_Overlap' for row in results)}")
    print(f"output_csv={OUTPUT_CSV}")
    print(f"output_report={OUTPUT_MD}")
