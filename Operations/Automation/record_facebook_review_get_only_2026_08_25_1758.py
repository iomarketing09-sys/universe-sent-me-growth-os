#!/usr/bin/env python3
"""Append one classified GET-only Facebook review to the anonymized ledger."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
EDITORIAL = RESEARCH / "2026-08-25_17-58-20_Facebook_Editorial_Review_GET_Only.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"

FIELDNAMES = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo", "Señal",
    "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado", "Respuesta_Fecha", "Respuesta_Meta_ID",
    "Insight_Anonimo", "Accion_Calendario", "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID",
    "Privacidad", "Fuente", "Ultima_Sincronizacion",
]


def ledger_row(item: dict, reviewed_at: str) -> dict:
    proposal = item["response_state"] == "Pendiente_Respuesta"
    return {
        "Comentario_ID": item["comment_id"],
        "Post_ID": item["post_id"],
        "CNT_ID": item.get("parent_comment_id") or "",
        "Fecha_Comentario": item["comment_created_time"],
        "Plataforma": "Facebook",
        "Tipo": item["comment_type"],
        "Señal": item["signal"],
        "Respuesta_Estado": "Pendiente_Respuesta" if proposal else "No_Requiere_Respuesta",
        "Respuesta_Sugerida": item["proposed_reply"] if proposal else "No responder",
        "Aprobacion_Estado": "Pendiente_Fernando" if proposal else "No_Aplica",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": item["reason"],
        "Accion_Calendario": "Ninguna",
        "Prioridad": item["priority"],
        "Moderacion_Estado": "Revisar" if proposal else "No_Accion",
        "Asset_Respuesta_ID": "",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — revisión GET-only 2026-08-25 17:58 UTC",
        "Ultima_Sincronizacion": reviewed_at,
    }


def main() -> None:
    editorial = json.loads(EDITORIAL.read_text(encoding="utf-8"))
    items = editorial["items"]
    expected = editorial["new_comment_count"]
    if len(items) != expected:
        raise SystemExit(f"EDITORIAL_COUNT_MISMATCH:{len(items)}:{expected}")
    ids = [item["comment_id"] for item in items]
    if len(ids) != len(set(ids)):
        raise SystemExit("DUPLICATE_EDITORIAL_IDS")
    if any(item["source"] != "Meta Graph API v26.0 — revisión GET-only" for item in items):
        raise SystemExit("SOURCE_MISMATCH")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDNAMES:
            raise SystemExit("LEDGER_SCHEMA_MISMATCH")
        existing_ids = {row.get("Comentario_ID", "") for row in reader}

    new_items = [item for item in items if item["comment_id"] not in existing_ids]
    rows = [ledger_row(item, editorial["updated_at"]) for item in new_items]
    if len({row["Comentario_ID"] for row in rows}) != len(rows):
        raise SystemExit("DUPLICATE_APPEND_IDS")
    if any(row["Privacidad"] != "Anonimizado" for row in rows):
        raise SystemExit("PRIVACY_CONTRACT_FAILURE")

    with LEDGER.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n").writerows(rows)

    editorial["ledger_rows_from_review"] = len(items)
    editorial["ledger_rows_appended_this_execution"] = len(rows)
    editorial["skipped_existing_ids"] = sorted(set(ids) & existing_ids)
    editorial["ledger_sync_status"] = "PASS"
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "reviewed_at": editorial["updated_at"],
        "candidate_count": len(items),
        "ledger_rows_appended": len(rows),
        "skipped_existing": len(items) - len(rows),
        "ledger_sync_status": "PASS",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
