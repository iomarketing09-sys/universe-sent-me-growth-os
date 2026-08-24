"""Sync verified batch 06 replies into the community ledger."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_06.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Publication_Record_Batch_06.json"

batch = json.loads(BATCH.read_text(encoding="utf-8"))
if batch.get("verified_count") != batch.get("requested_count"):
    raise SystemExit("BATCH_NOT_FULLY_VERIFIED")
with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
records = []
for result in batch.get("results", []):
    if not result.get("verified"):
        raise SystemExit(f"UNVERIFIED_RESULT: {result}")
    parent_id = result["parent_comment_id"]
    row = by_id.get(parent_id)
    if row is None:
        raise SystemExit(f"PARENT_NOT_IN_LEDGER: {parent_id}")
    row.update({
        "Respuesta_Estado": "Respondido",
        "Respuesta_Sugerida": result.get("message", ""),
        "Aprobacion_Estado": "Aprobada",
        "Respuesta_Fecha": batch.get("published_at", ""),
        "Respuesta_Meta_ID": result.get("reply_id", ""),
        "Insight_Anonimo": "Respuesta aprobada por Fernando y verificada en Meta.",
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — publicación verificada",
        "Ultima_Sincronizacion": batch.get("published_at", ""),
    })
    records.append({"comment_id": parent_id, "reply_id": result.get("reply_id"), "status": "Respondido", "verified": True})
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
payload = {
    "recorded_at": batch.get("published_at"),
    "source": "Meta Graph API v26.0",
    "batch_file": str(BATCH.relative_to(ROOT)),
    "updated_rows": len(records),
    "verified_rows": len(records),
    "records": records,
    "new_proposals_published": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False))
