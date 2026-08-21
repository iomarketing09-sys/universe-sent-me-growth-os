from __future__ import annotations

import csv
from pathlib import Path

CALENDAR = Path("Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv")
STAGING = Path("Operations/Research/2026-08-21_Comparable_Experiment_Publication_Staging.csv")

updates = {
    ("2026-08-24", "10:00"): {
        "old": "Universe - Existencial 260661.png",
        "brief": "FUT-MICRO-006",
        "hypothesis": "HB-007",
        "cell": "MICRO-STRICT-3P",
        "asset": "FUT-MICRO-006_HB-007_Microhistoria_Cotidiana_3P_v3.png",
        "caption": "A veces uno llega tarde y todavía quiere tener la razón. 😭",
        "caption_treatment": "caption_refuerzo",
        "caption_function": "refuerzo_semantico",
        "narrative": "dialogue_sequential_3_panel",
        "humor": "everyday_social_reframe",
        "characters": "Elara_and_Evan",
        "theme_confound": "everyday_social_context; relational_or_anxiety_risk; panel_count; caption_treatment",
        "hashtags": "#ElaraUSM #EvanUSM #UniverseSentMe",
    },
    ("2026-08-24", "13:30"): {
        "old": "2608048 - Universe - Inalcanzable para todos.jpeg",
        "brief": "FUT-MICRO-005",
        "hypothesis": "HB-006",
        "cell": "MICRO-STRICT-3P",
        "asset": "FUT-MICRO-005_HB-006_Microhistoria_Romantico_Absurd_3P_v3.png",
        "caption": "Bueno… tampoco era para tanto. 🤭",
        "caption_treatment": "caption_minimo",
        "caption_function": "reaccion",
        "narrative": "dialogue_sequential_3_panel",
        "humor": "romantic_absurd_reframe",
        "characters": "Elara_and_Evan",
        "theme_confound": "romantic_context; character_novelty; panel_count; caption_treatment",
        "hashtags": "#ElaraUSM #EvanUSM #UniverseSentMe",
    },
    ("2026-08-27", "16:00"): {
        "old": "2608064 - Universe - Quieren hacer pendejo al que nacio asi.jpeg",
        "brief": "FUT-ACID-003",
        "hypothesis": "HB-009",
        "cell": "ACID-DIALOGUE",
        "asset": "FUT-ACID-003_HB-009_Dialogo_Acido_Situacional_v3.png",
        "caption": "No era una opinión, era evidencia. 😮‍💨",
        "caption_treatment": "caption_minimo",
        "caption_function": "reaccion",
        "narrative": "interpersonal_dialogue",
        "humor": "interpersonal_contradiction",
        "characters": "Universe_and_Evan",
        "theme_confound": "acid_target; voice_clarity; relationship_context; caption_treatment; hour_16_nonpreferred",
        "hashtags": "#UniverseUSM #EvanUSM #UniverseSentMe",
    },
}

with CALENDAR.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames

assert fieldnames is not None
seen = set()
for row in rows:
    key = (row["Fecha"], row["Hora"])
    if key not in updates:
        continue
    spec = updates[key]
    assert row["Archivo"] == spec["old"], (key, row["Archivo"], spec["old"])
    row["Día"] = {"2026-08-24": "Lunes", "2026-08-27": "Jueves"}[row["Fecha"]]
    row["Archivo"] = spec["asset"]
    row["Estado"] = "Aprobado_Sustitucion_Pendiente_Meta"
    row["Contexto_Nota"] = f"Fernando aprobó la sustitución de {spec['old']} por {spec['brief']} v3; Meta aún no modificado."
    row["Experiment_ID"] = "EXP-2026-08-COMP-GAPS-01"
    row["Caption_Propuesto"] = spec["caption"]
    row["Tipo_Copy"] = spec["caption_treatment"]
    row["Instagram_Decision"] = "No — Facebook experiment first"
    row["Instagram_Motivo"] = "Separate approval required; no automatic cross-post."
    row["Drive_Destino_Propuesto"] = "Production_Repo_No_Move_Yet"
    row["Asset_Estado_Operativo"] = "Selected_v3_Approved_Calendar_Substitution_Pending_Meta"
    row["Hashtags_Propuestos"] = spec["hashtags"]
    row["Drive_ID"] = ""
    seen.add(key)

assert seen == set(updates), seen
with CALENDAR.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

staging_fields = [
    "Publication_ID", "Brief_ID", "ID_Pieza", "Asset_Ref", "Plataforma",
    "Fecha_Planeada_Local", "Hora_Planeada_Local", "Estado_Operativo",
    "Meta_Action", "Original_Slot_Asset", "Experiment_ID", "Hypothesis_ID",
    "Cell_ID", "Caption_Treatment", "Caption_Function", "Narrative_Structure",
    "Humor_Function", "Character_Presence", "Hora_Test", "Hora_Test_TZ",
    "Theme_Confound", "Reuse_Status", "Caption_Propuesto", "Caption_Status",
    "CNT_Status", "Affiliate_Attachment", "Instagram_Status", "Notes",
]

staging_rows = []
for (day, hour), spec in updates.items():
    staging_rows.append({
        "Publication_ID": f"PUB-FB-COMP-{day.replace('-', '')}-{hour.replace(':', '')}",
        "Brief_ID": spec["brief"],
        "ID_Pieza": spec["brief"],
        "Asset_Ref": f"Operations/Production/Generated_Comparable_Assets/{spec['asset']}",
        "Plataforma": "Facebook",
        "Fecha_Planeada_Local": day,
        "Hora_Planeada_Local": hour,
        "Estado_Operativo": "Aprobado_Sustitucion_Pendiente_Meta",
        "Meta_Action": "Not_Executed",
        "Original_Slot_Asset": spec["old"],
        "Experiment_ID": "EXP-2026-08-COMP-GAPS-01",
        "Hypothesis_ID": spec["hypothesis"],
        "Cell_ID": spec["cell"],
        "Caption_Treatment": spec["caption_treatment"],
        "Caption_Function": spec["caption_function"],
        "Narrative_Structure": spec["narrative"],
        "Humor_Function": spec["humor"],
        "Character_Presence": spec["characters"],
        "Hora_Test": hour,
        "Hora_Test_TZ": "America/Matamoros",
        "Theme_Confound": spec["theme_confound"],
        "Reuse_Status": "New_Asset_Proposed",
        "Caption_Propuesto": spec["caption"],
        "Caption_Status": "Pending_Final_Confirmation",
        "CNT_Status": "Not_Created",
        "Affiliate_Attachment": "No",
        "Instagram_Status": "Separate_Review",
        "Notes": "Calendar substitution approved by Fernando; final Meta scheduling/publication gate still pending.",
    })

with STAGING.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=staging_fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(staging_rows)

print("calendar_substitutions_applied=3")
print(f"staging_rows_written={len(staging_rows)}")
print("meta_action=Not_Executed")
print("publication=Not_Executed")
