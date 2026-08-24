"""Classify and record the read-only Facebook review after the latest approved publication.

This script performs no writes to Meta. It appends only unseen comment IDs to the
anonymized Community Engagement Log and emits editorial, report, and queue artifacts.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
REVIEW = RESEARCH / "2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json"
CONTEXT = RESEARCH / "2026-08-24_Facebook_Direct_Page_Mention_Context_After_Batch14.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
EDITORIAL = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json"
REPORT_MD = RESEARCH / "2026-08-24_Facebook_Comment_Review_After_Approved_Publication.md"
QUEUE = RESEARCH / "2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json"

PROPOSALS = {
    "122151376539072582_1063233976446841": {
        "proposed_reply": "El asterisco siempre aparece para salvar la credibilidad del meme. 😂✳️",
        "editorial_insight": "El comentario convierte el asterisco en el remate del meme; la respuesta lo reconoce sin repetir ni ampliar el doble sentido.",
        "priority": "Media",
    },
    "122151376539072582_2056563468318334": {
        "proposed_reply": "El universo no entrega certificados; aquí solo venimos a observar las teorías. 😂🙈",
        "editorial_insight": "Es una pregunta directa sobre la afirmación del meme; la propuesta responde con humor sin presentar la broma como un hecho médico.",
        "priority": "Media",
    },
    "122151376539072582_1406586844746099": {
        "proposed_reply": "Jajaja, no saques conclusiones tan literales; el meme no prometía transformaciones de ese tipo. 😂🙈",
        "editorial_insight": "El comentario lleva la premisa a una consecuencia corporal absurda; la respuesta devuelve el remate y evita escalar el contenido íntimo.",
        "priority": "Media",
    },
    "122151376083072582_1620854262795787": {
        "proposed_reply": "La trampa del cangrejo ya quedó oficialmente registrada. 😂🦀",
        "editorial_insight": "El comentario aporta un nombre juguetón al mecanismo sugerido por el meme; la propuesta es específica y no añade contenido gráfico.",
        "priority": "Media",
    },
    "122151376083072582_1036099909244517": {
        "proposed_reply": "Jajaja, de meme a campaña de salud pública en dos comentarios. 😂🙈",
        "editorial_insight": "Es el único reply nuevo que menciona directamente a Universe Sent Me. El parent explica el chiste como reducción de costillas y marcación abdominal; la propuesta continúa el giro hacia salud pública sin dar consejo médico.",
        "priority": "Alta",
    },
}

MUSIC_ID = "122151376011072582_2607700726348753"
DIRECT_MENTION_ID = "122151376083072582_1036099909244517"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def md(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\r", "").replace("\n", "<br>")


def post_reference(post_message: str) -> str:
    if "MaeveUSM" in post_message:
        return "Reel de Maeve — caption visible: `😳🛏️🔥 #MaeveUSM #MemesUSM #UniverseSentMe`"
    if "#UniverseUSM" in post_message:
        return "Meme de la frase confirmada `larga vida a esas mujeres que aprietan desde adentro`; caption visible: `😏🙈😂 #UniverseUSM #MemesUSM #UniverseSentMe`"
    if "💔" in post_message:
        return "Publicación de tono emocional — caption visible: `💔 #UniverseSentMe`"
    if "Bueno" in post_message:
        return "Publicación con caption visible: `Bueno… tampoco era para tanto. 🤭`"
    if "😌" in post_message:
        return "Publicación de contexto breve — caption visible: `😌 #UniverseSentMe`"
    return f"Publicación con caption visible: `{post_message}`"


def classify_no_action(row: dict) -> tuple[str, str]:
    message = (row.get("comment_message") or "").strip()
    if not message:
        return "Baja_señal", "Comentario sin texto recuperable; se conserva para cobertura, sin intervención."
    if row.get("comment_id") == MUSIC_ID:
        return "Baja_señal", "Referencia aislada posiblemente musical (‘Coco valiente’), pero sin artista ni contexto suficiente para una respuesta musical específica. Se conserva y no se omite."
    if row.get("comment_type") == "Replica_Anidada":
        return "Conversación_Usuario_Usuario", "Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo mención directa, que en este corte se trató como propuesta separada."
    if re.search(r"\b(verg|pene|cm|coger|cog|culo|chiquito|venosa|pitudo|desnalg|vagina|ordeñ|mamar|chupar|chupad|semen|sexo|sexual|cojer|coja|cojo|nalg|caderas)\w*", message, re.I) or "🍆" in message or "🥵" in message or "🫦" in message:
        return "Lenguaje_Sensible", "Lenguaje sexual explícito o descripción íntima; no escalar ni competir desde la Página."
    if re.search(r"\b(hola|jaj|jaja|sisi|seee|obvio|mentira|confirmo|verdad|ufff|así sea|asi sea|amén|amen)\b", message, re.I) or len(message) <= 14:
        return "Baja_señal", "Aprobación, risa, saludo o reacción breve sin una pregunta o contexto que exija respuesta."
    return "Conversación_Contextual", "Mención a terceros, etiqueta o señal ambigua sin una solicitud dirigida a Universe Sent Me; no asumir intención."


def build_ledger_row(row: dict, decision: dict, reviewed_at: str) -> dict:
    proposal = decision["editorial_decision"] == "Pendiente_Respuesta"
    return {
        "Comentario_ID": row["comment_id"],
        "Post_ID": row["post_id"],
        "CNT_ID": "",
        "Fecha_Comentario": row["comment_created_time"],
        "Plataforma": "Facebook",
        "Tipo": row["comment_type"],
        "Señal": decision["signal"],
        "Respuesta_Estado": "Pendiente_Respuesta" if proposal else "No_Requiere_Respuesta",
        "Respuesta_Sugerida": decision["proposed_reply"] if proposal else "No responder",
        "Aprobacion_Estado": "Pendiente_Fernando" if proposal else "No_Aplica",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": decision["editorial_insight"],
        "Accion_Calendario": "Ninguna",
        "Prioridad": decision["priority"],
        "Moderacion_Estado": "Revisar" if proposal else "No_Accion",
        "Asset_Respuesta_ID": "",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — revisión posterior a publicación aprobada",
        "Ultima_Sincronizacion": reviewed_at,
    }


def main() -> None:
    scan = load_json(REVIEW)
    reviewed_at = scan["reviewed_at"]
    candidates = scan["new_unanswered_not_in_ledger"]
    context = load_json(CONTEXT)
    context_parent = context.get("context", {}).get("parent", {})
    context_note = {
        "target_id": DIRECT_MENTION_ID,
        "parent_id": context.get("parent_id"),
        "parent_message": context_parent.get("message", ""),
        "parent_of_target_id": (context.get("context", {}).get("target", {}).get("parent") or {}).get("id"),
    }

    records = []
    ledger_rows_to_append = []
    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        existing_ids = {row.get("Comentario_ID", "") for row in reader}

    skipped_existing = []
    for row in candidates:
        cid = row["comment_id"]
        proposal = PROPOSALS.get(cid)
        if proposal:
            decision = {
                "editorial_decision": "Pendiente_Respuesta",
                "signal": "Oportunidad de engagement específica",
                "proposed_reply": proposal["proposed_reply"],
                "editorial_insight": proposal["editorial_insight"],
                "priority": proposal["priority"],
                "reason_code": "Propuesta específica pendiente de autorización humana",
            }
        else:
            signal, insight = classify_no_action(row)
            decision = {
                "editorial_decision": "No_Requiere_Respuesta",
                "signal": signal,
                "proposed_reply": "No responder",
                "editorial_insight": insight,
                "priority": "Baja",
                "reason_code": signal,
            }
        record = {
            "comment_id": cid,
            "post_id": row["post_id"],
            "post_reference": post_reference(row.get("post_message", "")),
            "comment_created_time": row["comment_created_time"],
            "comment_type": row["comment_type"],
            "comment_message": row.get("comment_message", ""),
            "parent_comment_id": row.get("parent_comment_id"),
            "editorial_decision": decision["editorial_decision"],
            "approval_state": "Pendiente_Fernando" if decision["editorial_decision"] == "Pendiente_Respuesta" else "No_Aplica",
            "moderation_state": "Revisar" if decision["editorial_decision"] == "Pendiente_Respuesta" else "No_Accion",
            "signal": decision["signal"],
            "priority": decision["priority"],
            "proposed_reply": decision["proposed_reply"],
            "editorial_insight": decision["editorial_insight"],
            "reason_code": decision["reason_code"],
        }
        if cid == DIRECT_MENTION_ID:
            record["context_note"] = "Mención directa a la Página; el parent explica el chiste como una supuesta rutina para reducir costillas y marcar abdomen."
        if cid == MUSIC_ID:
            record["context_note"] = "Referencia aislada: `Coco valiente`; no contiene artista, letra ni una petición musical verificable."
        records.append(record)
        if cid in existing_ids:
            skipped_existing.append(cid)
        else:
            ledger_rows_to_append.append(build_ledger_row(row, decision, reviewed_at))

    fieldnames = [
        "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo", "Señal",
        "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado", "Respuesta_Fecha", "Respuesta_Meta_ID",
        "Insight_Anonimo", "Accion_Calendario", "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID",
        "Privacidad", "Fuente", "Ultima_Sincronizacion",
    ]
    if ledger_rows_to_append:
        with LEDGER.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writerows(ledger_rows_to_append)

    proposals = [r for r in records if r["editorial_decision"] == "Pendiente_Respuesta"]
    no_action = [r for r in records if r["editorial_decision"] == "No_Requiere_Respuesta"]
    no_action_reasons = Counter(r["reason_code"] for r in no_action)
    by_post = Counter((r["post_id"], r["post_reference"]) for r in records)
    by_type = Counter(r["comment_type"] for r in records)

    editorial = {
        "title": "Facebook Editorial Review After Approved Publication",
        "purpose": "Clasificación completa del corte de comentarios nuevos posterior a la última publicación aprobada; separa propuestas pendientes de autorización de unidades conservadas sin acción.",
        "status": "Review",
        "created_at": reviewed_at,
        "updated_at": reviewed_at,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json",
            "Operations/Research/2026-08-24_Facebook_Direct_Page_Mention_Context_After_Batch14.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-15_Community_Engagement_Log.md",
            "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
            "GrowthOS/00_01_Changelog_GrowthOS.md",
        ],
        "source": "Meta Graph API v26.0 / read-only Page feed, direct post comments and one-level nested replies",
        "read_only_review": True,
        "cursor": scan["cursor"],
        "cursor_source": scan["cursor_source"],
        "api_error_count": scan["api_error_count"],
        "candidate_count": len(records),
        "proposal_count": len(proposals),
        "no_action_count": len(no_action),
        "published_count": 0,
        "current_unanswered_units_in_scope": scan["current_unanswered_units"],
        "ledger_rows_from_review": len(records),
        "ledger_rows_appended_this_execution": len(ledger_rows_to_append),
        "skipped_existing_ids": skipped_existing,
        "direct_page_mention": context_note,
        "music_like_candidate_id": MUSIC_ID,
        "counts_by_type": dict(by_type),
        "counts_by_no_action_reason": dict(no_action_reasons),
        "records": records,
    }
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    queue = {
        "title": "Facebook Pending Queue After Approved Publication Review",
        "purpose": "Cola actual de propuestas que requieren aprobación de Fernando y registro de casos cerrados sin acción después del corte de solo lectura.",
        "status": "Review",
        "created_at": reviewed_at,
        "updated_at": reviewed_at,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-24_Facebook_Editorial_Review_After_Approved_Publication.json",
            "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        ],
        "source": "Meta Graph API v26.0 / read-only review",
        "read_only_review": True,
        "approval_required_for_publication": True,
        "review_cursor": scan["cursor"],
        "current_unanswered_units_in_scope": scan["current_unanswered_units"],
        "review_candidate_count": len(records),
        "pending_response_count": len(proposals),
        "pending_response_with_proposal_count": len(proposals),
        "no_action_count_in_review": len(no_action),
        "publishable_without_new_approval": 0,
        "published_from_this_review": 0,
        "pending_comments": [
            {
                "comment_id": r["comment_id"],
                "post_id": r["post_id"],
                "comment_created_time": r["comment_created_time"],
                "comment_message": r["comment_message"],
                "post_reference": r["post_reference"],
                "proposed_reply": r["proposed_reply"],
                "priority": r["priority"],
                "insight": r["editorial_insight"],
                "approval_state": r["approval_state"],
            }
            for r in proposals
        ],
        "closed_without_action": [
            {
                "comment_id": r["comment_id"],
                "post_id": r["post_id"],
                "comment_created_time": r["comment_created_time"],
                "comment_message": r["comment_message"],
                "post_reference": r["post_reference"],
                "reason": r["editorial_insight"],
            }
            for r in no_action
        ],
    }
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "---",
        'title: "Facebook Comment Review After Approved Publication"',
        'purpose: "Revisión, clasificación y registro de comentarios nuevos de Facebook posterior a la última publicación aprobada."',
        "status: Review",
        f"created: {reviewed_at[:10]}",
        f"updated: {reviewed_at[:10]}",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-24_Facebook_Comment_Review_After_Approved_Publication.json",
        "  - Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Approved_Publication_Review.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.md",
        "  - Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
        "  - GrowthOS/00_01_Changelog_GrowthOS.md",
        "organization: Operations/Research",
        "---",
        "",
        "# Revisión de comentarios de Facebook posterior a publicación aprobada",
        "",
        f"La revisión de solo lectura se ejecutó con **Meta Graph API v26.0** a las `{reviewed_at}`. El cursor correcto fue `{scan['cursor']}`, correspondiente al cierre de la última tanda aprobada. Se revisaron {scan['page_posts_reviewed']} publicaciones propias, {scan['root_comments_seen']} comentarios raíz y {scan['comment_ids_seen']} IDs de comentarios y réplicas, con {scan['api_error_count']} errores de API. En el alcance completo había {scan['current_unanswered_units']} unidades sin respuesta directa; {len(records)} eran nuevas y no estaban registradas.",
        "",
        "## Resultado ejecutivo",
        "",
        "| Resultado | Casos | Estado |\n|---|---:|---|\n"
        f"| Unidades actuales sin respuesta directa en el alcance | {scan['current_unanswered_units']} | Incluye backlog previamente registrado |\n"
        f"| Comentarios nuevos sin respuesta directa | {len(records)} | Registrados todos en el ledger |\n"
        f"| Propuestas específicas | {len(proposals)} | `Pendiente_Fernando`; no publicadas |\n"
        f"| No requiere respuesta | {len(no_action)} | `No_Requiere_Respuesta` |\n"
        "| Publicaciones realizadas | 0 | No hubo autorización nueva |\n"
        f"| Errores de Meta API | {scan['api_error_count']} | Sin errores |",
        "",
        "El corte no publicó respuestas. La autorización de la tanda anterior **no se extiende** a estos candidatos; cualquier publicación futura requiere una aprobación nueva y específica de Fernando.",
        "",
        "## Distribución del corte",
        "",
        "| Publicación / referencia | Hallazgos | Tratamiento editorial |\n|---|---:|---|\n"
        + "\n".join(
            f"| {md(post_ref)} | {count} | {('Se revisaron raíces y réplicas; predominan conversaciones usuario-a-usuario y lenguaje sensible.' if 'Maeve' in post_ref else 'Se revisaron raíces y réplicas; se separó una mención directa a la Página y una referencia musical aislada.' if '#UniverseUSM' in post_ref else 'Se conserva como señal contextual o vacía, sin asumir intención.') } |"
            for (post_id, post_ref), count in by_post.items()
        ),
        "",
        "## Propuestas pendientes de autorización",
        "",
        "Las cinco propuestas fueron seleccionadas por ser raíces o una mención directa a la Página con un remate concreto. Mantienen el tono USM, no compiten con la escalada sexual del hilo y no presentan el meme como información médica.",
        "",
        "| Comentario | Referencia de la publicación | Respuesta propuesta | Por qué sí merece revisión |\n|---|---|---|---|\n"
        + "\n".join(
            f"| `{r['comment_id']}` — {md(r['comment_message'])} | {md(r['post_reference'])} | **{md(r['proposed_reply'])}** | {md(r['editorial_insight'])} |"
            for r in proposals
        ),
        "",
        "### Mención directa a Universe Sent Me",
        "",
        f"El comentario `{DIRECT_MENTION_ID}` dice: **{md(next(r['comment_message'] for r in records if r['comment_id'] == DIRECT_MENTION_ID))}**. El parent inmediato explica el chiste como una supuesta rutina para reducir costillas y marcar abdomen, y la Página ya había respondido a la raíz con el remate sobre una “clase de anatomía”. La propuesta pendiente es: **{md(PROPOSALS[DIRECT_MENTION_ID]['proposed_reply'])}**.",
        "",
        "### Referencia musical aislada",
        "",
        f"El comentario `{MUSIC_ID}` contiene **Coco valiente**. Se conservó en el inventario completo, pero quedó sin acción porque no incluye artista, letra ni contexto que permita responder de manera específica. No se descartó silenciosamente; puede reconsiderarse si Fernando identifica la referencia.",
        "",
        "## Casos cerrados sin acción",
        "",
        "| Categoría | Casos | Criterio aplicado |\n|---|---:|---|\n"
        + "\n".join(
            f"| `{md(reason)}` | {count} | {md(next((r['editorial_insight'] for r in no_action if r['reason_code'] == reason), 'Se conserva para trazabilidad, sin respuesta pública.'))} |"
            for reason, count in no_action_reasons.items()
        ),
        "",
        "La mayor concentración corresponde al reel de Maeve: sus raíces y réplicas contienen conversaciones entre usuarios, saludos, etiquetas, reacciones breves y lenguaje sexual explícito. La regla aplicada fue no interrumpir conversaciones usuario-a-usuario ni amplificar descripciones íntimas desde la Página.",
        "",
        "## Inventario completo de los 95 hallazgos",
        "",
        "Todos los IDs recuperados en este corte están incluidos en el JSON editorial y en el ledger. La tabla siguiente permite auditar que ningún comentario quedó fuera de la clasificación.",
        "",
        "| # | Comentario_ID | Tipo | Comentario | Decisión | Motivo resumido |\n|---:|---|---|---|---|---|\n"
        + "\n".join(
            f"| {i} | `{r['comment_id']}` | {r['comment_type']} | {md(r['comment_message'])} | `{r['editorial_decision']}` | {md(r['editorial_insight'])} |"
            for i, r in enumerate(records, start=1)
        ),
        "",
        "## Integridad y siguiente paso",
        "",
        f"El corte incorporó {len(records)} filas al ledger; en esta ejecución idempotente se anexaron {len(ledger_rows_to_append)} filas nuevas y se omitieron {len(skipped_existing)} IDs ya registrados. El ledger permanece anonimizado y append-only. No existe ninguna respuesta publicable sin una nueva autorización explícita de Fernando.",
        "",
        "Documentos relacionados que deben mantenerse alineados: el ledger descriptivo, la auditoría histórica de comentarios de Facebook y el changelog de GrowthOS. La corrección del cursor queda documentada en el nuevo auditor `Operations/Automation/audit_facebook_comments_after_approved_publication.py`.",
        "",
        "## Referencias",
        "",
        "Fuentes: [Meta Graph API Comments and Mentions][1] y [Meta Graph API Comment reference][2].",
        "",
        "[1]: https://developers.facebook.com/documentation/pages-api/comments-mentions",
        "[2]: https://developers.facebook.com/docs/graph-api/reference/comment/",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "reviewed_at": reviewed_at,
        "cursor": scan["cursor"],
        "candidate_count": len(records),
        "proposal_count": len(proposals),
        "no_action_count": len(no_action),
        "ledger_rows_appended": len(ledger_rows_to_append),
        "api_error_count": scan["api_error_count"],
        "published_count": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
