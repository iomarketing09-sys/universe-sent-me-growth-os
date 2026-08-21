from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "Operations/Research/2026-08-21_Autorizacion_Generacion_Briefs_Comparables.csv"
EXPECTED_BRIEFS = {
    "FUT-MICRO-005": "HB-006",
    "FUT-MICRO-006": "HB-007",
    "FUT-TRANS-003": "HB-008",
    "FUT-ACID-003": "HB-009",
}
REQUIRED_FIELDS = {
    "Brief_ID",
    "Experiment_ID",
    "Hypothesis_ID",
    "Cell_ID",
    "Generation_Request",
    "Proposed_Asset_Count",
    "Generation_Scope",
    "Caption_Treatment",
    "Caption_Function",
    "Hora_Test",
    "Hora_Test_TZ",
    "Theme_Confound",
    "Reuse_Status",
    "Mandatory_Checks",
    "Generation_Authorization",
    "Calendar_Change",
    "CNT_Creation",
    "Publication",
    "Affiliate_Attachment",
    "Decision",
    "Decision_By",
    "Decision_Date",
    "Decision_Notes",
}

with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

if set(row["Brief_ID"] for row in rows) != set(EXPECTED_BRIEFS):
    raise RuntimeError("La matriz no contiene exactamente los cuatro briefs esperados.")
if set(rows[0]) != REQUIRED_FIELDS:
    missing = REQUIRED_FIELDS - set(rows[0])
    extra = set(rows[0]) - REQUIRED_FIELDS
    raise RuntimeError(f"Estructura inesperada. missing={sorted(missing)} extra={sorted(extra)}")

for row in rows:
    brief_id = row["Brief_ID"]
    checks = {
        "hypothesis_id": row["Hypothesis_ID"] == EXPECTED_BRIEFS[brief_id],
        "generation_request": row["Generation_Request"] == "Approve_Generation_Only",
        "asset_count": row["Proposed_Asset_Count"] == "1",
        "generation_approved": row["Generation_Authorization"] == "Approved_Generation_Only",
        "calendar_block": row["Calendar_Change"] == "No",
        "cnt_block": row["CNT_Creation"] == "No",
        "publication_block": row["Publication"] == "No",
        "affiliate_block": row["Affiliate_Attachment"] == "No",
        "decision_approved": row["Decision"] == "Approved",
        "decision_by": row["Decision_By"] == "Fernando",
        "decision_date": row["Decision_Date"] == "2026-08-21",
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"{brief_id}: fallos de autorización: {failed}")

print(f"authorization_matrix_pass={len(rows)}/{len(EXPECTED_BRIEFS)}")
print("scope=Approve_Generation_Only")
print("calendar_change=No cnt_creation=No publication=No affiliate_attachment=No")
print("human_decision=Approved by Fernando on 2026-08-21")
