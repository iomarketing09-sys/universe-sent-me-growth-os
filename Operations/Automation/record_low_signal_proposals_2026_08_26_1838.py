#!/usr/bin/env python3
"""Record four Fernando-selected low-signal Facebook engagement proposals."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
QUEUE_IN = RESEARCH / "2026-08-26_18-26-39_Facebook_Pending_Queue_After_Wilfred_Publication.json"
QUEUE_OUT = RESEARCH / "2026-08-26_18-38-17_Facebook_Pending_Queue_Low_Signal_Proposals.json"
EDITORIAL_OUT = RESEARCH / "2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json"
REPORT = RESEARCH / "2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.md"
REVIEWED_AT = "2026-08-26T18:38:17+00:00"

PROPOSALS = {
    "122151377649072582_2511249876017099": {
        "post_id": "1036844829507460_122151377649072582",
        "comment_message": "Pues claro que nooooooo, ni pierdo .., , ni voy 😏",
        "post_reference": "🪦🧟‍♀️😅 #MaeveUSM #MemesUSM #UniverseSentMe",
        "reply": "Ese “ni voy” ya viene con cláusula de permanencia. 😂",
        "reason": "Fernando identificó una cuenta activa de la Página; el comentario ofrece una apertura breve para responder al remate de permanencia sin escalar el doble sentido.",
    },
    "122151377649072582_2227921178135227": {
        "post_id": "1036844829507460_122151377649072582",
        "comment_message": "pues no te mueres...👁️👁️🔥🌀",
        "post_reference": "🪦🧟‍♀️😅 #MaeveUSM #MemesUSM #UniverseSentMe",
        "reply": "El universo confirmó que aquí nadie se escapa tan fácil. 👁️🔥",
        "reason": "Fernando identificó una cuenta activa de la Página; se propone un remate específico al tono de inmortalidad/escape del comentario.",
    },
    "122151377109072582_1103053779073759": {
        "post_id": "1036844829507460_122151377109072582",
        "comment_message": "Seeeee",
        "post_reference": "😈🚲🫣 #KaelUSM #MemesUSM #UniverseSentMe",
        "reply": "Ese “seeeee” sonó a confirmación oficial. 😂",
        "reason": "Fernando identificó una cuenta activa de la Página; la respuesta convierte la reacción breve en un remate participativo sin inventar contexto.",
    },
    "122151377109072582_28380292711566338": {
        "post_id": "1036844829507460_122151377109072582",
        "comment_message": "Ni me lo recuerdes!!",
        "post_reference": "😈🚲🫣 #KaelUSM #MemesUSM #UniverseSentMe",
        "reply": "Jajaja, el recuerdo llegó sin tocar la puerta. 😅",
        "reason": "Fernando identificó una cuenta activa de la Página; la respuesta sigue la reacción de memoria con un giro breve y natural.",
    },
}


def main() -> None:
    queue = json.loads(QUEUE_IN.read_text(encoding="utf-8"))
    no_action = list(queue.get("no_action", []))
    pending = list(queue.get("pending_comments", []))
    if any(item.get("comment_id") in {p for p in PROPOSALS} for item in pending):
        raise SystemExit("TARGET_ALREADY_PENDING")
    found = {item.get("comment_id"): item for item in no_action}
    if set(found) & set(PROPOSALS) != set(PROPOSALS):
        raise SystemExit("TARGETS_NOT_IN_NO_ACTION")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    by_id = {row.get("Comentario_ID"): row for row in rows}
    if len(by_id) != len(rows):
        raise SystemExit("DUPLICATE_LEDGER_IDS_BEFORE_RECLASSIFICATION")

    decisions = []
    for cid, proposal in PROPOSALS.items():
        row = by_id.get(cid)
        if row is None:
            raise SystemExit(f"LEDGER_TARGET_NOT_FOUND:{cid}")
        if row.get("Respuesta_Estado") not in ("No_Requiere_Respuesta", "Pendiente_Respuesta"):
            raise SystemExit(f"LEDGER_TARGET_STATE_UNEXPECTED:{cid}:{row.get('Respuesta_Estado')}")
        row.update({
            "Respuesta_Estado": "Pendiente_Respuesta",
            "Respuesta_Sugerida": proposal["reply"],
            "Aprobacion_Estado": "Pendiente_Fernando",
            "Respuesta_Fecha": "",
            "Respuesta_Meta_ID": "",
            "Insight_Anonimo": proposal["reason"],
            "Accion_Calendario": "Revisar con Fernando",
            "Prioridad": "Media",
            "Moderacion_Estado": "Pendiente_Revision",
            "Privacidad": "Anonimizado",
            "Fuente": "Revisión editorial USM — baja señal priorizada por Fernando 2026-08-26",
            "Ultima_Sincronizacion": REVIEWED_AT,
        })
        decisions.append({
            "comment_id": cid,
            "post_id": proposal["post_id"],
            "comment_message": proposal["comment_message"],
            "post_reference": proposal["post_reference"],
            "decision": "Propuesta",
            "response_state": "Pendiente_Respuesta",
            "approval_state": "Pendiente_Fernando",
            "category": "low_signal_reengagement",
            "reason": proposal["reason"],
            "proposed_reply": proposal["reply"],
            "publication_status": "No_Publicar_Sin_Autorizacion_Posterior",
        })

    with LEDGER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    remaining_no_action = [item for item in no_action if item.get("comment_id") not in PROPOSALS]
    for cid, proposal in PROPOSALS.items():
        pending.append({
            "comment_id": cid,
            "post_id": proposal["post_id"],
            "comment_message": proposal["comment_message"],
            "post_reference": proposal["post_reference"],
            "candidate_reply": proposal["reply"],
            "decision": "Propuesta",
            "approval_status": "Pendiente_Fernando",
            "publication_status": "No_Publicar_Sin_Autorizacion_Posterior",
            "reason": proposal["reason"],
        })
    queue_out = dict(queue)
    queue_out.update({
        "title": "Facebook Pending Queue — low-signal re-engagement proposals",
        "updated_at": REVIEWED_AT,
        "related_documents": list(dict.fromkeys((queue.get("related_documents") or []) + [
            "Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json",
            "Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.md",
        ])),
        "pending_response_count": len(pending),
        "pending_approval_count": len(pending),
        "no_action_count": len(remaining_no_action),
        "published_from_this_review": 0,
        "pending_comments": pending,
        "no_action": remaining_no_action,
    })
    QUEUE_OUT.write_text(json.dumps(queue_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    editorial = {
        "title": "Facebook Low-Signal Proposal Review — 2026-08-26 18:38 UTC",
        "purpose": "Registrar la selección editorial de cuatro comentarios de baja señal para re-engagement, con propuestas específicas pendientes de aprobación humana.",
        "status": "Review",
        "created_at": REVIEWED_AT,
        "updated_at": REVIEWED_AT,
        "version": "1.0",
        "author": "Manus AI",
        "related_documents": [
            "Operations/Research/2026-08-26_18-26-39_Facebook_Pending_Queue_After_Wilfred_Publication.json",
            "Operations/Research/2026-08-26_18-15-41_Facebook_Editorial_Review_GET_Only.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-26_18-38-17_Facebook_Pending_Queue_Low_Signal_Proposals.json",
            "Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.md",
        ],
        "organization": "Operations/Research",
        "source": "Fernando editorial selection from the latest Facebook GET-only review",
        "read_only_meta_state": True,
        "new_proposal_count": 4,
        "no_action_reclassified_count": 4,
        "context_review_count_preserved": queue.get("context_review_count"),
        "publication_count": 0,
        "decisions": decisions,
    }
    EDITORIAL_OUT.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = [
        "---",
        'title: "Facebook Low-Signal Proposal Review — 2026-08-26 18:38 UTC"',
        'purpose: "Propuestas de re-engagement para cuatro comentarios de baja señal identificados por Fernando."',
        "status: Review",
        "created: 2026-08-26",
        "updated: 2026-08-26",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-26_18-38-17_Facebook_Low_Signal_Proposal_Review.json",
        "  - Operations/Research/2026-08-26_18-38-17_Facebook_Pending_Queue_Low_Signal_Proposals.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "organization: Operations/Research",
        "---",
        "",
        "# Propuestas para comentarios de baja señal",
        "",
        "Fernando identificó que cuatro comentarios de baja señal provienen de usuarios activos de la Página. Se propone probar respuestas breves y específicas, manteniendo fuera los dos comentarios con lenguaje íntimo, las conversaciones laterales y cualquier otro caso No_Requiere_Respuesta.",
        "",
        "| Comentario | Publicación | Propuesta | Estado |",
        "|---|---|---|---|",
    ]
    for proposal in PROPOSALS.values():
        report.append(f"| {proposal['comment_message']} | {proposal['post_reference']} | {proposal['reply']} | `Pendiente_Fernando` |")
    report += [
        "",
        "## Decisión operativa",
        "",
        "Los cuatro comentarios fueron movidos de `No_Requiere_Respuesta` a `Pendiente_Respuesta` en el ledger y añadidos a una nueva cola de propuestas. No se publicó ninguna respuesta. Los dos comentarios con lenguaje íntimo permanecen sin acción y no fueron reclassificados.",
        "",
        "## Controles",
        "",
        "| Control | Resultado |",
        "|---|---:|",
        "| Propuestas nuevas | 4 |",
        "| Publicaciones | 0 |",
        "| Casos íntimos reclassificados | 0 |",
        "| Casos de contexto modificados | 0 |",
        f"| Ledger después de la reclasificación | {len(rows)} filas |",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"proposals": 4, "no_action_reclassified": 4, "publication_count": 0, "ledger_rows": len(rows), "pending_after": len(pending)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
