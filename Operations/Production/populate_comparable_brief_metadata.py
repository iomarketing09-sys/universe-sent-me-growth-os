from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-21_Briefs_Comparables_Revision_Humana.csv"

COMMON_EXPERIMENT_ID = "EXP-2026-08-COMP-GAPS-01"

METADATA = {
    "FUT-MICRO-005": {
        "Hypothesis_ID": "H-COMP-MICRO3P-005",
        "Caption_Function": "reaccion",
        "Humor_Function": "romantic_absurd_reframe",
        "Hora_Test": "18:00",
        "Hora_Test_TZ": "America/Matamoros",
        "Theme_Confound": "romantic_context; character_novelty; panel_count; caption_treatment",
        "Reuse_Status": "New_Asset_Proposed",
        "Metadata_Notes": "Hora propuesta, no programada. Caption mínimo: reacción/remate breve, sin pregunta abierta. Personajes genéricos; exactamente tres paneles.",
    },
    "FUT-MICRO-006": {
        "Hypothesis_ID": "H-COMP-MICRO3P-006",
        "Caption_Function": "refuerzo_semantico",
        "Humor_Function": "everyday_social_reframe",
        "Hora_Test": "20:00",
        "Hora_Test_TZ": "America/Matamoros",
        "Theme_Confound": "everyday_social_context; relational_or_anxiety_risk; panel_count; caption_treatment",
        "Reuse_Status": "New_Asset_Proposed",
        "Metadata_Notes": "Hora propuesta, no programada. Caption de refuerzo: ilumina la lectura sin repetir globos ni abrir una conversación artificial. Conflicto no romántico.",
    },
    "FUT-TRANS-003": {
        "Hypothesis_ID": "H-COMP-TRANS-003",
        "Caption_Function": "pregunta_abierta",
        "Humor_Function": "visual_identity_contrast",
        "Hora_Test": "16:00",
        "Hora_Test_TZ": "America/Matamoros",
        "Theme_Confound": "transformation_type; identity_legibility; background_dominance; caption_treatment",
        "Reuse_Status": "New_Asset_Proposed",
        "Metadata_Notes": "Hora propuesta, no programada. Caption conversacional: invitación breve/pregunta abierta sin describir literalmente el antes/después. Verificar gafas en ambos estados.",
    },
    "FUT-ACID-003": {
        "Hypothesis_ID": "H-COMP-ACID-003",
        "Caption_Function": "reaccion",
        "Humor_Function": "interpersonal_contradiction",
        "Hora_Test": "22:00",
        "Hora_Test_TZ": "America/Matamoros",
        "Theme_Confound": "acid_target; voice_clarity; relationship_context; caption_treatment",
        "Reuse_Status": "New_Asset_Proposed",
        "Metadata_Notes": "Hora propuesta, no programada. Caption mínimo, sin explicar el remate. Objetivo ácido limitado a situación, hábito o contradicción; sin coerción ni ataque a rasgos protegidos.",
    },
}

NEW_FIELDS = [
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

with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

if not rows:
    raise RuntimeError("La matriz está vacía.")

missing_briefs = set(METADATA) - {row["Brief_ID"] for row in rows}
if missing_briefs:
    raise RuntimeError(f"Faltan briefs en la matriz: {sorted(missing_briefs)}")

fieldnames = list(rows[0])
for field in NEW_FIELDS:
    if field not in fieldnames:
        fieldnames.append(field)

for row in rows:
    for key, value in row.items():
        if isinstance(value, str):
            row[key] = " ".join(value.splitlines())
    brief_id = row["Brief_ID"]
    if brief_id not in METADATA:
        continue
    row["Experiment_ID"] = COMMON_EXPERIMENT_ID
    row.update(METADATA[brief_id])
    row["Metadata_Status"] = "Complete_Proposed_Not_Authorized"
    row["Generation_Authorization"] = "Pending_Human_Approval"

with MATRIX.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(f"metadata_rows_completed={len(METADATA)}")
print(f"experiment_id={COMMON_EXPERIMENT_ID}")
print(f"path={MATRIX}")
for brief_id, values in METADATA.items():
    print(brief_id, values["Hypothesis_ID"], values["Caption_Function"], values["Humor_Function"], values["Hora_Test"], values["Reuse_Status"])
