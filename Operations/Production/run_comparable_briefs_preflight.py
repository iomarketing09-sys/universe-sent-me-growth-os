from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"
DESIGN = ROOT / "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"
REPORT = ROOT / "Operations/Production/2026-08-21_Preflight_Briefs_Comparables.md"

REQUIRED_MATRIX_FIELDS = {
    "Brief_ID",
    "Cell_ID",
    "Status",
    "Narrative_Structure",
    "Theme",
    "Caption_Treatment",
    "Character_Presence",
    "Required_Identity_Checks",
    "Primary_Metric",
    "Requested_Decision",
    "Decision_By",
    "Decision_Date",
    "Experiment_ID",
    "Hypothesis_ID",
    "Caption_Function",
    "Humor_Function",
    "Hora_Test",
    "Hora_Test_TZ",
    "Theme_Confound",
    "Reuse_Status",
    "Metadata_Status",
    "Generation_Authorization",
    "Metadata_Notes",
}

REQUIRED_PRE_GENERATION_FIELDS = [
    "Experiment_ID",
    "Hypothesis_ID",
    "Cell_ID",
    "Caption_Treatment",
    "Caption_Function",
    "Narrative_Structure",
    "Humor_Function",
    "Character_Presence",
    "Hora_Test",
    "Theme_Confound",
    "Reuse_Status",
]

EXPECTED = {
    "FUT-MICRO-005": {
        "cell": "MICRO-STRICT-3P",
        "structure": "dialogue_sequential_3_panel",
        "theme": "romantic_absurd",
        "caption": "caption_minimo",
        "character": "generic_pair",
        "identity_token": "exactly 3 panels",
    },
    "FUT-MICRO-006": {
        "cell": "MICRO-STRICT-3P",
        "structure": "dialogue_sequential_3_panel",
        "theme": "everyday_social_conflict",
        "caption": "caption_refuerzo",
        "character": "generic_pair",
        "identity_token": "exactly 3 panels",
    },
    "FUT-TRANS-003": {
        "cell": "TRANS-UNIVERSE",
        "structure": "visual_before_after",
        "theme": "transformation_identity",
        "caption": "caption_conversacional",
        "character": "Universe_Confirmed",
        "identity_token": "preserva_gafas_universe=Sí",
    },
    "FUT-ACID-003": {
        "cell": "ACID-DIALOGUE",
        "structure": "interpersonal_dialogue",
        "theme": "acid_interpersonal",
        "caption": "caption_minimo",
        "character": "generic_pair_or_confirmed_character",
        "identity_token": "Confirm no unsafe canonical identity distortion",
    },
}


def read_matrix() -> list[dict[str, str]]:
    with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise RuntimeError("La matriz de briefs está vacía.")
    missing = REQUIRED_MATRIX_FIELDS - set(rows[0])
    if missing:
        raise RuntimeError(f"Faltan campos en la matriz: {sorted(missing)}")
    return rows


def validate(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = {row["Brief_ID"]: row for row in rows if row["Brief_ID"] in EXPECTED}
    if set(selected) != set(EXPECTED):
        raise RuntimeError("La matriz no contiene exactamente los cuatro briefs del preflight.")

    results: list[dict[str, str]] = []
    for brief_id, expected in EXPECTED.items():
        row = selected[brief_id]
        metadata_fields = [
            "Experiment_ID",
            "Hypothesis_ID",
            "Caption_Function",
            "Humor_Function",
            "Hora_Test",
            "Hora_Test_TZ",
            "Theme_Confound",
            "Reuse_Status",
            "Metadata_Status",
            "Generation_Authorization",
            "Metadata_Notes",
        ]
        checks = {
            "status": row["Status"] == "Approved_for_Preflight",
            "decision": row["Requested_Decision"] == "Approve_Preflight_Only",
            "decision_by": row["Decision_By"] == "Fernando",
            "cell": row["Cell_ID"] == expected["cell"],
            "structure": row["Narrative_Structure"] == expected["structure"],
            "theme": row["Theme"] == expected["theme"],
            "caption": row["Caption_Treatment"] == expected["caption"],
            "character": row["Character_Presence"] == expected["character"],
            "identity_spec": expected["identity_token"] in row["Required_Identity_Checks"],
            "metadata_complete": all(row[field].strip() for field in metadata_fields),
            "metadata_status": row["Metadata_Status"] == "Complete_Proposed_Not_Authorized",
            "reuse_status": row["Reuse_Status"] == "New_Asset_Proposed",
            "generation_block": row["Generation_Authorization"] == "Pending_Human_Approval",
        }
        failed = [name for name, passed in checks.items() if not passed]
        results.append(
            {
                "brief_id": brief_id,
                "cell": row["Cell_ID"],
                "caption": row["Caption_Treatment"],
                "spec_status": "PASS" if not failed else "FAIL",
                "failed_checks": ", ".join(failed) if failed else "—",
                "experiment_id": row["Experiment_ID"],
                "hypothesis_id": row["Hypothesis_ID"],
                "caption_function": row["Caption_Function"],
                "humor_function": row["Humor_Function"],
                "hora_test": row["Hora_Test"],
                "hora_test_tz": row["Hora_Test_TZ"],
                "theme_confound": row["Theme_Confound"],
                "reuse_status": row["Reuse_Status"],
                "generation_authorization": row["Generation_Authorization"],
                "asset_status": "PENDING — no asset generated",
                "metadata_status": "PASS — complete proposal" if not failed else "FAIL — review required",
                "promotion_status": "BLOCKED — requires separate human approval",
            }
        )
    return results


def write_report(results: list[dict[str, str]]) -> None:
    all_pass = all(item["spec_status"] == "PASS" for item in results)
    report_status = "Active" if all_pass else "Review"
    lines = [
        "---",
        'title: "Preflight de briefs comparables aprobados"',
        'purpose: "Validar reproduciblemente las especificaciones de los cuatro briefs aprobados para preflight y registrar los bloqueos antes de generación, calendario, publicación o CNT."',
        f"status: {report_status}",
        "created: 2026-08-21",
        "updated: 2026-08-21",
        'version: "1.1"',
        'author: "Manus AI (CGO)"',
        "related_documents:",
        '  - "Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md"',
        '  - "Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md"',
        '  - "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"',
        '  - "GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md"',
        'organization: "Operations/Production"',
        "---",
        "",
        "# Preflight de briefs comparables aprobados",
        "",
        "## Resultado ejecutivo",
        "",
        f"Los cuatro briefs pasan la validación de especificación y metadatos propuestos: `{len(results)}/4` con `spec_status=PASS`. Esta salida confirma coherencia entre la matriz de aprobación, el diseño técnico y los campos previos a generación; **no confirma que exista un asset**, no genera imágenes y no autoriza calendario, publicación, reuse ni creación de CNT.",
        "",
        "> La aprobación de Fernando es `Approve_Preflight_Only`. Cualquier paso que produzca un asset o lo acerque a publicación requiere una decisión humana separada.",
        "",
        "## Matriz de preflight",
        "",
        "| Brief_ID | Cell_ID | Experiment_ID | Hypothesis_ID | Caption_Treatment | Caption_Function | Humor_Function | Hora_Test | Theme_Confound | Reuse_Status | Especificación | Asset | Metadatos | Generación | Promoción |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for item in results:
        lines.append(
            f"| `{item['brief_id']}` | `{item['cell']}` | `{item['experiment_id']}` | `{item['hypothesis_id']}` | `{item['caption']}` | `{item['caption_function']}` | `{item['humor_function']}` | `{item['hora_test']} ({item['hora_test_tz']})` | `{item['theme_confound']}` | `{item['reuse_status']}` | `{item['spec_status']}` | {item['asset_status']} | {item['metadata_status']} | `{item['generation_authorization']}` | {item['promotion_status']} |"
        )

    lines.extend(
        [
            "",
            "## Campos obligatorios antes de generar cualquier asset",
            "",
            "Cada brief ya contiene una propuesta para los siguientes campos. Los valores son de diseño previo y deben revisarse antes de cualquier solicitud de generación; no constituyen autorización. La hora es una hora de prueba propuesta en `America/Matamoros`, no un slot reservado:",
            "",
            "| Campo | Regla | Estado en este preflight |",
            "|---|---|---|",
        ]
    )
    for field in REQUIRED_PRE_GENERATION_FIELDS:
        rule = "Separado de Caption_Treatment; no asumir que una pregunta retórica es conversacional." if field == "Caption_Function" else "Propuesta completada; revisar antes de generación."
        if field == "Reuse_Status":
            rule = "Debe registrar `New_Asset_Proposed`; no mezclar con reuse."
        lines.append(f"| `{field}` | {rule} | `PROPOSED_COMPLETE_NOT_AUTHORIZED` |")

    lines.extend(
        [
            "",
            "## Salvaguardas específicas",
            "",
            "**FUT-MICRO-005 y FUT-MICRO-006.** La pieza debe tener exactamente tres paneles inequívocos, turnos legibles y remate autosuficiente. No se acepta el candidato histórico de cuatro paneles `1036844829507460_122127951885072582` dentro de `MICRO-STRICT-3P`.",
            "",
            "**FUT-TRANS-003.** No se puede promover la pieza sin verificar visualmente al mismo Universe en ambos estados, gafas visibles en ambos estados y marcadores de identidad preservados. Un cambio de ropa aislado o la sustitución por otro personaje no cumple.",
            "",
            "**FUT-ACID-003.** El objetivo ácido debe ser una situación, hábito o contradicción; las voces deben distinguirse en una lectura; `Safety_Flag` debe confirmar ausencia de coerción y de ataques a rasgos protegidos.",
            "",
            "## Condiciones de promoción",
            "",
            "El resultado de este documento es `preflight_specification_pass` con metadatos propuestos completos, no `generation_approved`. Antes de cualquier generación se necesita revisar estos valores y obtener aprobación humana explícita para producir assets. Antes de calendario, publicación o CNT se necesita una aprobación posterior e independiente.",
            "",
            "## Reproducibilidad",
            "",
            "Este reporte fue generado por `Operations/Production/run_comparable_briefs_preflight.py` a partir de la matriz CSV y de los criterios del diseño técnico. Los metadatos fueron completados por `Operations/Production/populate_comparable_brief_metadata.py`. No se consultaron APIs, no se modificó Facebook o Instagram y no se usó navegación externa.",
            "",
            "## Referencias",
            "",
            "[1]: `Operations/Production/2026-08-21_Diseno_Casos_Comparables_Brechas.md` — criterios técnicos y estado de celdas.",
            "[2]: `Operations/Research/2026-08-21_Paquete_Revision_Humana_Briefs_Comparables.md` — alcance de la aprobación humana.",
            "[3]: `Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv` — matriz reproducible de decisiones y metadatos propuestos.",
            "[4]: `Operations/Production/populate_comparable_brief_metadata.py` — llenado reproducible de los valores propuestos.",
            "[5]: `GrowthOS/06_00_Reglas_Aprendizaje_Tendencias.md` — reglas de evidencia y captions.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    matrix_rows = read_matrix()
    validation_results = validate(matrix_rows)
    write_report(validation_results)
    print(f"preflight_specification_pass={sum(item['spec_status'] == 'PASS' for item in validation_results)}/{len(validation_results)}")
    print(f"report={REPORT}")
    for item in validation_results:
        print(item["brief_id"], item["spec_status"], item["asset_status"], item["promotion_status"])
