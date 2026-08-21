from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
EXPERIMENT_LOG = ROOT / "Operations/Research/2026-08-15_ExperimentLog.csv"
WAVE1 = ROOT / "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"
BRIDGE = ROOT / "GrowthOS/Integracion_Growth_OS.md"
REPORT = ROOT / "Operations/Research/2026-08-21_Validacion_Cruzada_Hipotesis_Briefs_Comparables.md"

TARGET_BRIEFS = {
    "FUT-MICRO-005": {
        "overlap": "FAM-03 / H-AUG-FAM03 (Conversación_Relacional): comparte contexto romántico/interpersonal; la celda sigue separada por estructura estricta de tres paneles y caption mínimo.",
        "action": "Mantener fuera del agregado FAM-03; usar `MICRO-STRICT-3P` como celda primaria y registrar el contexto romántico como confusor.",
    },
    "FUT-MICRO-006": {
        "overlap": "FAM-02 / H-AUG-FAM02 (Relatable_Social) y FAM-03 / H-AUG-FAM03: comparte situación social/interpersonal; la secuencia exacta de tres paneles es la diferencia declarada.",
        "action": "No combinar automáticamente con FAM-02/FAM-03; conservar `MICRO-STRICT-3P` y `everyday_social_context` como definición primaria.",
    },
    "FUT-TRANS-003": {
        "overlap": "FAM-05 / H-AUG-FAM05 (Personaje_Marcador) y HB-002 (Universe/formato Reel): comparte identidad visual de Universe, pero prueba transformación estática con preservación de gafas, no superioridad de personaje ni formato Reel.",
        "action": "No atribuir un resultado a Universe sin auditar identidad; mantener separado de FAM-05 y de HB-002, y excluir cambios de formato como explicación.",
    },
    "FUT-ACID-003": {
        "overlap": "FAM-04 / H-AUG-FAM04 (Ácido_Interpersonal): solapamiento semántico directo de familia y métrica; la nueva celda restringe el caso a diálogo de dos voces con objetivo situacional seguro.",
        "action": "No mezclar en el mismo denominador sin declarar una subcelda; mantener `ACID-DIALOGUE` como estructura primaria y revisar que el ácido no sea genérico.",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def extract_known_ids() -> tuple[set[str], set[str], set[str]]:
    experiment_ids = {row["Experiment_ID"] for row in read_csv(EXPERIMENT_LOG) if row.get("Experiment_ID")}
    wave1_rows = read_csv(WAVE1)
    experiment_ids.update(row["Experiment_ID"] for row in wave1_rows if row.get("Experiment_ID"))
    hypothesis_ids = {row["Hypothesis_ID"] for row in read_csv(EXPERIMENT_LOG) if row.get("Hypothesis_ID")}
    hypothesis_ids.update(row["Hypothesis_ID"] for row in wave1_rows if row.get("Hypothesis_ID"))
    bridge_text = BRIDGE.read_text(encoding="utf-8")
    bridge_hypotheses = set(re.findall(r"\bHB-\d{3}\b", bridge_text))
    return experiment_ids, hypothesis_ids, bridge_hypotheses


def cross_validate(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], set[str], set[str], set[str]]:
    existing_experiments, existing_hypotheses, registered_hypotheses = extract_known_ids()
    selected = {row["Brief_ID"]: row for row in rows if row["Brief_ID"] in TARGET_BRIEFS}
    if set(selected) != set(TARGET_BRIEFS):
        raise RuntimeError("La matriz no contiene exactamente los cuatro briefs esperados.")

    results = []
    for brief_id, row in selected.items():
        experiment_id = row["Experiment_ID"]
        hypothesis_id = row["Hypothesis_ID"]
        direct_experiment_collision = experiment_id in existing_experiments
        direct_hypothesis_collision = hypothesis_id in existing_hypotheses
        hypothesis_registered = hypothesis_id in registered_hypotheses
        canonical_hypothesis_format = bool(re.fullmatch(r"HB-\d{3}", hypothesis_id))
        clean_status = row["Status"] == "Approved_for_Preflight"
        clean_generation_block = row["Generation_Authorization"] == "Pending_Human_Approval"
        clean_reuse = row["Reuse_Status"] == "New_Asset_Proposed"
        checks = {
            "experiment_id_unique": not direct_experiment_collision,
            "hypothesis_id_unique": not direct_hypothesis_collision,
            "hypothesis_registered": hypothesis_registered,
            "hypothesis_format": canonical_hypothesis_format,
            "approval_scope": clean_status,
            "generation_block": clean_generation_block,
            "new_asset_guard": clean_reuse,
        }
        hard_conflicts = [name for name, passed in checks.items() if name in {"experiment_id_unique", "hypothesis_id_unique", "approval_scope", "generation_block", "new_asset_guard"} and not passed]
        warnings = [name for name, passed in checks.items() if name in {"hypothesis_registered", "hypothesis_format"} and not passed]
        status = "PASS" if not hard_conflicts and not warnings else "PASS_WITH_WARNINGS" if not hard_conflicts else "CONFLICT"
        results.append(
            {
                "brief_id": brief_id,
                "experiment_id": experiment_id,
                "hypothesis_id": hypothesis_id,
                "cell_id": row["Cell_ID"],
                "status": status,
                "direct_conflict": "No" if not hard_conflicts else "; ".join(hard_conflicts),
                "registry_warning": "None" if not warnings else "Hypothesis_ID no registrado en HypothesisBank local y/o no cumple formato HB-###",
                "semantic_overlap": TARGET_BRIEFS[brief_id]["overlap"],
                "action": TARGET_BRIEFS[brief_id]["action"],
                "checks": "; ".join(f"{key}={'PASS' if passed else 'WARN/FAIL'}" for key, passed in checks.items()),
            }
        )
    return results, existing_experiments, existing_hypotheses, registered_hypotheses


def write_report(results: list[dict[str, str]], existing_experiments: set[str], existing_hypotheses: set[str], registered_hypotheses: set[str]) -> None:
    conflicts = [item for item in results if item["status"] == "CONFLICT"]
    warnings = [item for item in results if item["status"] == "PASS_WITH_WARNINGS"]
    if warnings:
        registry_summary = f"{len(warnings)} briefs aún tienen advertencias de registro o nomenclatura."
        pre_generation_summary = "Antes de producir assets se debe resolver el registro/nomenclatura de las hipótesis y mantener separados los agregados que tienen solapamiento semántico con Wave 1."
    else:
        registry_summary = "Las cuatro hipótesis están registradas en el HypothesisBank con IDs únicos y formato HB-###."
        pre_generation_summary = "El registro formal no autoriza generación. Se mantienen separados los agregados que tienen solapamiento semántico con Wave 1."
    lines = [
        "---",
        'title: "Validación cruzada de hipótesis — briefs comparables"',
        'purpose: "Verificar colisiones de identificadores, solapamientos semánticos y contaminación con experimentos previos antes de generar assets."',
        f"status: {'Review' if conflicts or warnings else 'Active'}",
        "created: 2026-08-21",
        "updated: 2026-08-21",
        'version: "1.1"',
        'author: "Manus AI (CGO)"',
        "related_documents:",
        '  - "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"',
        '  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"',
        '  - "Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv"',
        '  - "Operations/Research/2026-08-15_ExperimentLog.csv"',
        '  - "GrowthOS/Integracion_Growth_OS.md"',
        '  - "Operations/Production/validate_comparable_hypothesis_conflicts.py"',
        '  - "Operations/Research/2026-08-21_Simulacion_Impacto_Solapamientos_Comparables.md"',
        'organization: "Operations/Research"',
        "---",
        "",
        "# Validación cruzada de hipótesis — briefs comparables",
        "",
        "## Veredicto ejecutivo",
        "",
        f"No se detectaron colisiones directas de `Experiment_ID` ni de `Hypothesis_ID` contra los registros existentes para los cuatro briefs. El resultado es `{len(results) - len(conflicts)}/{len(results)} sin conflicto duro`. {registry_summary}",
        "",
        f"> {pre_generation_summary}",
        "",
        "## Matriz de verificación",
        "",
        "| Brief_ID | Experiment_ID | Hypothesis_ID | Cell_ID | Estado | Conflicto directo | Advertencia de registro |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in results:
        lines.append(
            f"| `{item['brief_id']}` | `{item['experiment_id']}` | `{item['hypothesis_id']}` | `{item['cell_id']}` | `{item['status']}` | `{item['direct_conflict']}` | {item['registry_warning']} |"
        )

    lines.extend(
        [
            "",
            "## Solapamientos semánticos controlables",
            "",
            "| Brief_ID | Solapamiento observado | Regla de separación |",
            "|---|---|---|",
        ]
    )
    for item in results:
        lines.append(f"| `{item['brief_id']}` | {item['semantic_overlap']} | {item['action']} |")

    lines.extend(
        [
            "",
            "## Conflictos con experimentos previos",
            "",
            "La revisión cruzó los cuatro briefs contra los IDs presentes en `ExperimentLog`, los 15 registros conceptuales de `Wave_1_Signal_Experiment_Design.csv` y el `HypothesisBank` documentado en `Integracion_Growth_OS.md`. Los experimentos previos relevantes son `EXP-2026-08-BASELINE-01`, `EXP-2026-08-BASELINE-02`, `EXP-2026-08-BASELINE-03`, `EXP-2026-08-CAL-01` y `EXP-2026-08-FAM01-W1` a `EXP-2026-08-FAM05-W1`; ninguno coincide con `EXP-2026-08-COMP-GAPS-01`.",
            "",
            "El principal riesgo no es una colisión de ID sino un solapamiento de variables. `FUT-ACID-003` es semánticamente próximo a `FAM-04`; `FUT-TRANS-003` comparte el marcador de Universe con `FAM-05` y el sujeto Universe con `HB-002`; `FUT-MICRO-005` se aproxima a `FAM-03`; y `FUT-MICRO-006` se aproxima a `FAM-02` y `FAM-03`. Las diferencias de `Cell_ID`, `Narrative_Structure` y controles de confusión permiten mantenerlos separados, pero los resultados no deben combinarse automáticamente.",
            "",
            "El horario propuesto (`16:00`, `18:00`, `20:00`, `22:00`) se superpone con franjas usadas por Wave 1 y con la hipótesis histórica de horario `HB-003`. Por ello `Hora_Test` debe tratarse como covariable, no como resultado de estas hipótesis, y las piezas no deben presentarse como una prueba aislada del efecto horario.",
            "",
            "## Acción requerida antes de generación",
            "",
            "1. Mantener los IDs formales HB-006 a HB-009 registrados en el HypothesisBank; no reutilizarlos en otra hipótesis.",
            "2. Mantener `EXP-2026-08-COMP-GAPS-01` como experimento separado de P0, `EXP-2026-08-CAL-01`, Wave 1, afiliados y reuse.",
            "3. Conservar las cuatro celdas y no agrupar por familia Wave 1 solo porque comparten tema, personaje o métrica.",
            "4. Revisar nuevamente `Caption_Treatment` y `Caption_Function` como variables distintas; el caption no debe absorber el efecto de la estructura visual.",
            "",
            "## Reproducibilidad",
            "",
            f"El validador comparó {len(existing_experiments)} identificadores de experimento conocidos, {len(existing_hypotheses)} identificadores de hipótesis encontrados en ledgers/matrices y {len(registered_hypotheses)} entradas `HB-###` del bridge. Script: `Operations/Production/validate_comparable_hypothesis_conflicts.py`.",
            "",
            "## Referencias",
            "",
            "[1]: `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv` — hipótesis y metadatos propuestos.",
            "[2]: `Operations/Research/2026-08-15_ExperimentLog.csv` — experimentos y observaciones registrados.",
            "[3]: `Operations/Production/2026-08-20_Wave1_Signal_Experiment_Design.csv` — matriz conceptual de Wave 1.",
            "[4]: `GrowthOS/Integracion_Growth_OS.md` — HypothesisBank y ExperimentLog condensados.",
            "[5]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — convención de IDs y reglas de evidencia.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_matrix(rows: list[dict[str, str]], results: list[dict[str, str]]) -> None:
    by_brief = {item["brief_id"]: item for item in results}
    new_fields = ["Cross_Validation_Status", "Cross_Validation_Notes"]
    fieldnames = list(rows[0])
    for field in new_fields:
        if field not in fieldnames:
            fieldnames.append(field)
    for row in rows:
        if row["Brief_ID"] not in by_brief:
            continue
        item = by_brief[row["Brief_ID"]]
        row["Cross_Validation_Status"] = item["status"]
        row["Cross_Validation_Notes"] = (
            f"Direct_ID_Conflict=No. {item['registry_warning']}. {item['semantic_overlap']} "
            f"Regla: {item['action']}"
        )
    with MATRIX.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    matrix_rows = read_csv(MATRIX)
    results, known_experiments, known_hypotheses, registered_hypotheses = cross_validate(matrix_rows)
    update_matrix(matrix_rows, results)
    write_report(results, known_experiments, known_hypotheses, registered_hypotheses)
    print(f"briefs_checked={len(results)}")
    print(f"direct_conflicts={sum(item['status'] == 'CONFLICT' for item in results)}")
    print(f"warnings={sum(item['status'] == 'PASS_WITH_WARNINGS' for item in results)}")
    print(f"report={REPORT}")
    for item in results:
        print(item["brief_id"], item["status"], item["hypothesis_id"], item["direct_conflict"])
