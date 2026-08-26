#!/usr/bin/env python3
"""Record and verify the four approved low-signal Facebook publications."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
PUBLICATION = RESEARCH / "2026-08-26_18-44-00_Facebook_Low_Signal_Publication.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
QUEUE_IN = RESEARCH / "2026-08-26_18-38-17_Facebook_Pending_Queue_Low_Signal_Proposals.json"
QUEUE_OUT = RESEARCH / "2026-08-26_18-49-09_Facebook_Pending_Queue_After_Low_Signal_Publication.json"
EDITORIAL = RESEARCH / "2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json"
RECORD_JSON = RESEARCH / "2026-08-26_18-49-09_Facebook_Low_Signal_Publication_Record.json"
RECORD_MD = RESEARCH / "2026-08-26_18-49-09_Facebook_Low_Signal_Publication_Record.md"
REVIEWED_AT = "2026-08-26T18:49:07+00:00"
TARGETS = {
    "122151377649072582_2511249876017099",
    "122151377649072582_2227921178135227",
    "122151377109072582_1103053779073759",
    "122151377109072582_28380292711566338",
}


def main() -> None:
    publication = json.loads(PUBLICATION.read_text(encoding="utf-8"))
    results = publication.get("results") or []
    result_ids = {item.get("parent_comment_id") for item in results}
    if not (
        publication.get("requested_count") == 4
        and publication.get("published_count") == 4
        and publication.get("verified_count") == 4
        and result_ids == TARGETS
        and all(item.get("verified") is True and item.get("is_hidden") is False for item in results)
    ):
        raise SystemExit("PUBLICATION_EVIDENCE_MISMATCH")
    if any(item.get("parent_id_returned") != item.get("parent_comment_id") for item in results):
        raise SystemExit("PARENT_VERIFICATION_MISMATCH")

    by_target = {item["parent_comment_id"]: item for item in results}
    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    ledger_map = {row.get("Comentario_ID"): row for row in rows}
    if len(ledger_map) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS")
    for target_id in TARGETS:
        row = ledger_map.get(target_id)
        if row is None:
            raise SystemExit(f"LEDGER_TARGET_NOT_FOUND:{target_id}")
        result = by_target[target_id]
        row.update({
            "Respuesta_Estado": "Respondido",
            "Aprobacion_Estado": "Aprobada",
            "Respuesta_Sugerida": result.get("message") or row.get("Respuesta_Sugerida", ""),
            "Respuesta_Fecha": result.get("created_time") or "",
            "Respuesta_Meta_ID": result.get("reply_id") or "",
            "Moderacion_Estado": "Respondido",
            "Privacidad": "Anonimizado",
            "Fuente": "Meta Graph API v26.0 — publicación y verificación explícitas 2026-08-26",
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
    if {item.get("comment_id") for item in pending} != TARGETS:
        raise SystemExit("QUEUE_TARGET_SET_MISMATCH")
    queue_out = dict(queue)
    queue_out.update({
        "title": "Facebook Pending Queue — after verified low-signal publication",
        "updated_at": REVIEWED_AT,
        "related_documents": list(dict.fromkeys((queue.get("related_documents") or []) + [
            "Operations/Research/2026-08-26_18-44-00_Facebook_Low_Signal_Publication.json",
            "Operations/Research/2026-08-26_18-49-09_Facebook_Low_Signal_Publication_Record.json",
        ])),
        "pending_response_count": 0,
        "pending_approval_count": 0,
        "published_from_this_review": 4,
        "pending_comments": [],
    })
    QUEUE_OUT.write_text(json.dumps(queue_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    editorial = json.loads(EDITORIAL.read_text(encoding="utf-8"))
    for decision in editorial.get("decisions", []):
        target_id = decision.get("comment_id")
        if target_id in TARGETS:
            result = by_target[target_id]
            decision.update({
                "decision": "Respondido",
                "response_state": "Respondido",
                "approval_state": "Aprobada",
                "proposed_reply": result.get("message"),
                "response_meta_id": result.get("reply_id"),
                "response_created_time": result.get("created_time"),
                "publication_status": "Publicado_y_verificado",
            })
    editorial["updated_at"] = REVIEWED_AT
    editorial["publication_update"] = {
        "published_count": 4,
        "verified_count": 4,
        "publication_status": "Publicado_y_verificado",
        "additional_cases_published": 0,
    }
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    record = {
        "title": "Facebook Low-Signal Replies — publication and ledger update",
        "purpose": "Record the explicit approval, verified publication, queue closure and ledger update for exactly four low-signal Facebook replies.",
        "status": "Active",
        "created_at": publication.get("created_at"),
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-26_18-44-00_Facebook_Low_Signal_Publication.json",
            "Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json",
            "Operations/Research/2026-08-26_18-49-09_Facebook_Pending_Queue_After_Low_Signal_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "organization": "Operations/Research",
        "source": "Meta Graph API v26.0",
        "page_id": publication.get("page_id"),
        "explicit_user_approval": True,
        "requested_count": 4,
        "published_count": 4,
        "verified_count": 4,
        "strict_direct_parent_count": publication.get("strict_direct_parent_count"),
        "queue_pending_response_count_after": 0,
        "additional_cases_published": 0,
        "results": results,
    }
    RECORD_JSON.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "---",
        'title: "Facebook Low-Signal Replies — publication and ledger update"',
        'purpose: "Record the explicit approval, verified publication, queue closure and ledger update for exactly four low-signal Facebook replies."',
        "status: Active",
        "created: 2026-08-26",
        "updated: 2026-08-26",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-26_18-44-00_Facebook_Low_Signal_Publication.json",
        "  - Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json",
        "  - Operations/Research/2026-08-26_18-49-09_Facebook_Pending_Queue_After_Low_Signal_Publication.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Publicación verificada: cuatro respuestas de baja señal",
        "",
        "Fernando autorizó explícitamente las cuatro respuestas. El preflight no encontró duplicados ni conflictos. Meta Graph API v26.0 confirmó 4/4 publicaciones, todas con texto exacto, autoría de la Página, `is_hidden=false` y parent directo correcto.",
        "",
        "| Control | Resultado |",
        "|---|---:|",
        "| Publicadas | 4 |",
        "| Verificadas | 4 |",
        "| Parent directo | 4/4 |",
        "| Duplicados/conflictos | 0 |",
        "| Casos íntimos publicados | 0 |",
        "| Cola de propuestas después del cierre | 0 |",
        "| Ledger | 644 filas / validación posterior requerida |",
        "",
        "Los dos casos de lenguaje íntimo, los dos casos de contexto y las cinco no acciones restantes no fueron incluidos en la operación.",
        "",
    ]
    RECORD_MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"published": 4, "verified": 4, "ledger_rows": len(rows), "pending_after": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
