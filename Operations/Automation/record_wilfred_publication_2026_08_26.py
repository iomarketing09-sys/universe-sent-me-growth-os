#!/usr/bin/env python3
"""Record the verified publication for Wilfred's approved Facebook reply."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
PUBLICATION = RESEARCH / "2026-08-26_18-24-00_Facebook_Wilfred_Publication.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
QUEUE_IN = RESEARCH / "2026-08-26_18-15-41_Facebook_Pending_Queue_GET_Only.json"
QUEUE_OUT = RESEARCH / "2026-08-26_18-26-39_Facebook_Pending_Queue_After_Wilfred_Publication.json"
EDITORIAL = RESEARCH / "2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json"
RECORD_JSON = RESEARCH / "2026-08-26_18-26-39_Facebook_Wilfred_Publication_Record.json"
RECORD_MD = RESEARCH / "2026-08-26_18-26-39_Facebook_Wilfred_Publication_Record.md"
TARGET_ID = "122151377553072582_1857148135657699"
REVIEWED_AT = "2026-08-26T18:26:39+00:00"


def main() -> None:
    publication = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    result = publication.get("result") or {}
    if not (
        publication.get("published_count") == 1
        and publication.get("verified_count") == 1
        and result.get("verified") is True
        and result.get("parent_comment_id") == TARGET_ID
        and result.get("message") == "Wilfred ya tomó nota: un guiño y un toque de canela. 🌲😂"
        and result.get("is_hidden") is False
    ):
        raise SystemExit("PUBLICATION_EVIDENCE_MISMATCH")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    matches = [row for row in rows if row.get("Comentario_ID") == TARGET_ID]
    if len(matches) != 1:
        raise SystemExit(f"LEDGER_TARGET_COUNT:{len(matches)}")
    row = matches[0]
    if row.get("Respuesta_Estado") not in ("Pendiente_Respuesta", "Respondido"):
        raise SystemExit(f"LEDGER_TARGET_STATE:{row.get('Respuesta_Estado')}")
    row.update({
        "Respuesta_Estado": "Respondido",
        "Aprobacion_Estado": "Aprobada",
        "Respuesta_Sugerida": result.get("message") or row.get("Respuesta_Sugerida", ""),
        "Respuesta_Fecha": result.get("created_time") or "",
        "Respuesta_Meta_ID": result.get("reply_id") or "",
        "Moderacion_Estado": "Respondido",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — publicación y verificación explícitas 2026-08-26T18:26:39Z",
        "Ultima_Sincronizacion": REVIEWED_AT,
        "Accion_Calendario": "Publicada y verificada",
        "Prioridad": "Media",
    })
    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    queue = json.loads(QUEUE_IN.read_text(encoding="utf-8"))
    pending = queue.get("pending_comments", [])
    target_items = [item for item in pending if item.get("comment_id") == TARGET_ID]
    if len(target_items) != 1:
        raise SystemExit(f"QUEUE_TARGET_COUNT:{len(target_items)}")
    remaining = [item for item in pending if item.get("comment_id") != TARGET_ID]
    queue_out = dict(queue)
    queue_out.update({
        "title": "Facebook Pending Queue — after verified Wilfred publication",
        "updated_at": REVIEWED_AT,
        "related_documents": list(dict.fromkeys((queue.get("related_documents") or []) + [
            "Operations/Research/2026-08-26_18-24-00_Facebook_Wilfred_Publication.json",
            "Operations/Research/2026-08-26_18-26-39_Facebook_Wilfred_Publication_Record.json",
        ])),
        "pending_response_count": len(remaining),
        "pending_approval_count": len(remaining),
        "published_from_this_review": 1,
        "pending_comments": remaining,
    })
    QUEUE_OUT.write_text(json.dumps(queue_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    editorial = json.loads(EDITORIAL.read_text(encoding="utf-8"))
    updated = False
    for decision in editorial.get("decisions", []):
        if decision.get("comment_id") == TARGET_ID:
            decision.update({
                "decision": "Respondido",
                "response_state": "Respondido",
                "approval_state": "Aprobada",
                "proposed_reply": result.get("message"),
                "response_meta_id": result.get("reply_id"),
                "response_created_time": result.get("created_time"),
                "publication_status": "Publicado_y_verificado",
            })
            updated = True
    if not updated:
        raise SystemExit("EDITORIAL_TARGET_NOT_FOUND")
    editorial["updated_at"] = REVIEWED_AT
    editorial["publication_update"] = {
        "published_count": 1,
        "verified_count": 1,
        "target_comment_id": TARGET_ID,
        "reply_id": result.get("reply_id"),
        "publication_status": "Publicado_y_verificado",
    }
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    record = {
        "title": "Facebook Wilfred Reply — publication and ledger update",
        "purpose": "Record the explicit approval, verified publication, queue closure and ledger update for exactly one Facebook reply.",
        "status": "Active",
        "created_at": publication.get("created_at"),
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-26_18-24-00_Facebook_Wilfred_Publication.json",
            "Operations/Research/2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-26_18-26-39_Facebook_Pending_Queue_After_Wilfred_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": publication.get("page_id"),
        "explicit_user_approval": True,
        "target_comment_id": TARGET_ID,
        "reply_id": result.get("reply_id"),
        "published_count": 1,
        "verified_count": 1,
        "is_hidden": result.get("is_hidden"),
        "parent_id_returned": result.get("parent_id_returned"),
        "ledger_state": "Respondido",
        "queue_pending_response_count_after": len(remaining),
        "additional_cases_published": 0,
    }
    RECORD_JSON.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "---",
        'title: "Facebook Wilfred Reply — publication and ledger update"',
        'purpose: "Record the explicit approval, verified publication, queue closure and ledger update for exactly one Facebook reply."',
        "status: Active",
        "created: 2026-08-26",
        "updated: 2026-08-26",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-26_18-24-00_Facebook_Wilfred_Publication.json",
        "  - Operations/Research/2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json",
        "  - Operations/Research/2026-08-26_18-26-39_Facebook_Pending_Queue_After_Wilfred_Publication.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Publicación verificada: respuesta de Wilfred",
        "",
        "> Respuesta publicada: “Wilfred ya tomó nota: un guiño y un toque de canela. 🌲😂”",
        "",
        "Meta Graph API v26.0 confirmó la publicación de una única respuesta autorizada. El texto coincidió exactamente, la autoría fue la Página, `is_hidden=false` y el parent devuelto correspondió al comentario objetivo.",
        "",
        "| Control | Resultado |",
        "|---|---:|",
        "| Publicadas | 1 |",
        "| Verificadas | 1 |",
        "| Duplicados/conflictos en preflight | 0 |",
        "| Comentarios adicionales publicados | 0 |",
        f"| Ledger | {len(rows)} filas / validación posterior requerida |",
        f"| Cola pendiente después del cierre | {len(remaining)} propuestas |",
        "",
        "Los cuatro casos de baja señal y los dos comentarios con lenguaje íntimo permanecen sin respuesta y no fueron incluidos en esta operación.",
        "",
    ]
    RECORD_MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"published": 1, "verified": 1, "ledger_rows": len(rows), "pending_after": len(remaining)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
