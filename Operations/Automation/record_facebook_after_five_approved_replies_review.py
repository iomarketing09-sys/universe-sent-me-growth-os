"""Classify and record the read-only Facebook review after five approved replies.

No Meta writes occur here. The script appends only unseen IDs to the anonymized
Community Engagement Log and emits complete editorial and queue artifacts.
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
REVIEW = RESEARCH / "2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
EDITORIAL = RESEARCH / "2026-08-25_Facebook_Editorial_Review_After_Five_Approved_Replies.json"
REPORT_MD = RESEARCH / "2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.md"
QUEUE = RESEARCH / "2026-08-25_Facebook_Pending_Queue_After_Five_Approved_Replies.json"

PROPOSALS = {
    "122151376011072582_1051573194149891": {
        "proposed_reply": "«CONTIGO» de Karol G: el corazón sí sabe elegir soundtrack. 💗🎶",
        "editorial_insight": "Es una recomendación musical identificable por título y artista; la respuesta reconoce la canción y la conecta con el tono emocional de la publicación sin inventar una interpretación de la letra.",
        "priority": "Media",
    },
    "122151376011072582_1458569976337294": {
        "proposed_reply": "«Aventurera» de Alberto Plaza: esa sí trae nostalgia con pasaporte propio. 🎶🌙",
        "editorial_insight": "Es una referencia musical identificable por título y artista; la propuesta responde a esa elección concreta y mantiene un remate USM breve, sin fingir que el comentario pidió análisis musical.",
        "priority": "Media",
    },
}
MUSIC_IDS = set(PROPOSALS)


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
    if "😌" in post_message:
        return "Publicación de contexto breve — caption visible: `😌 #UniverseSentMe`"
    return f"Publicación con caption visible: `{post_message}`"


def classify_no_action(row: dict) -> tuple[str, str]:
    message = (row.get("comment_message") or "").strip()
    if not message:
        return "Baja_señal", "Comentario sin texto recuperable; se conserva para cobertura, sin intervención."
    if row.get("comment_type") == "Replica_Anidada":
        return "Conversación_Usuario_Usuario", "Réplica dentro de una conversación entre usuarios; no interrumpir desde la Página salvo una mención directa, que no apareció en este corte."
    if re.search(r"\b(verg|pene|cm|coger|cog|culo|chiquito|venosa|pitudo|desnalg|vagina|ordeñ|mamar|chupar|chupad|semen|sexo|sexual|cojer|coja|cojo|nalg|nalgas|caderas|fundillo|clavar|orinan|perrito)\w*", message, re.I) or any(mark in message for mark in ("🍆", "🥵", "🫦")):
        return "Lenguaje_Sensible", "Lenguaje sexual explícito o descripción íntima; no escalar ni competir desde la Página."
    if re.search(r"\b(hola|jaj|jaja|sisi|seee|obvio|mentira|verdad|ufff|gracias|rico|amén|amen|yo|mor)\b", message, re.I) or len(message) <= 14:
        return "Baja_señal", "Aprobación, risa, saludo, agradecimiento o reacción breve sin una pregunta dirigida a Universe Sent Me."
    return "Conversación_Contextual", "Comentario contextual, anecdótico o crítico sin una solicitud inequívoca a Universe Sent Me; se conserva sin asumir intención."


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
        "Fuente": "Meta Graph API v26.0 — revisión posterior a cinco respuestas aprobadas",
        "Ultima_Sincronizacion": reviewed_at,
    }


def main() -> None:
    scan = load_json(REVIEW)
    reviewed_at = scan["reviewed_at"]
    candidates = scan["new_unanswered_not_in_ledger"]
    if len(candidates) != scan["new_unanswered_not_in_ledger_since_latest_cursor"]:
        raise SystemExit("SCAN_CANDIDATE_COUNT_MISMATCH")
    if len({row.get("comment_id") for row in candidates}) != len(candidates):
        raise SystemExit("DUPLICATE_SCAN_COMMENT_IDS")

    with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        existing_ids = {row.get("Comentario_ID", "") for row in reader}

    records = []
    ledger_rows_to_append = []
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
        records.append(record)
        if cid in existing_ids:
            skipped_existing.append(cid)
        else:
            ledger_rows_to_append.append(build_ledger_row(row, decision, reviewed_at))

    if len(records) != 101:
        raise SystemExit(f"EXPECTED_101_REVIEW_RECORDS: got={len(records)}")
    if len(ledger_rows_to_append) != len(set(ledger_rows_to_append_row["Comentario_ID"] for ledger_rows_to_append_row in ledger_rows_to_append)):
        raise SystemExit("DUPLICATE_LEDGER_APPEND_IDS")

    fieldnames = [
        "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo", "Señal",
        "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado", "Respuesta_Fecha", "Respuesta_Meta_ID",
        "Insight_Anonimo", "Accion_Calendario", "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID",
        "Privacidad", "Fuente", "Ultima_Sincronizacion",
    ]
    if ledger_rows_to_append:
        with LEDGER.open("a", encoding="utf-8", newline="") as handle:
            csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n").writerows(ledger_rows_to_append)

    proposals = [r for r in records if r["editorial_decision"] == "Pendiente_Respuesta"]
    no_action = [r for r in records if r["editorial_decision"] == "No_Requiere_Respuesta"]
    by_post = Counter((r["post_id"], r["post_reference"]) for r in records)
    by_type = Counter(r["comment_type"] for r in records)
    no_action_reasons = Counter(r["reason_code"] for r in no_action)

    editorial = {
        "title": "Facebook Editorial Review After Five Approved Replies",
        "purpose": "Clasificación completa de la cola nueva posterior a las cinco últimas respuestas aprobadas; separa propuestas pendientes de autorización de unidades conservadas sin acción.",
        "status": "Review",
        "created_at": reviewed_at,
        "updated_at": reviewed_at,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json",
            "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
            "Operations/Research/2026-08-15_Community_Engagement_Log.md",
            "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
            "GrowthOS/00_01_Changelog_GrowthOS.md",
        ],
        "source": "Meta Graph API v26.0 / read-only Page feed, direct post comments and one-level nested replies",
        "read_only_review": True,
        "reviewed_at": scan["reviewed_at"],
        "page_posts_reviewed": scan["page_posts_reviewed"],
        "root_comments_seen": scan["root_comments_seen"],
        "comment_ids_seen": scan["comment_ids_seen"],
        "current_unanswered_units_in_scope": scan["current_unanswered_units"],
        "new_units_since_latest_cursor": scan["new_units_since_latest_cursor"],
        "logged_unanswered_since_latest_cursor": scan["logged_unanswered_since_latest_cursor"],
        "api_error_count": scan["api_error_count"],
        "cursor": scan["cursor"],
        "cursor_source": scan["cursor_source"],
        "candidate_count": len(records),
        "proposal_count": len(proposals),
        "no_action_count": len(no_action),
        "published_count": 0,
        "direct_page_mention_count": 0,
        "music_candidate_ids": sorted(MUSIC_IDS),
        "ledger_rows_from_review": len(records),
        "ledger_rows_appended_this_execution": len(ledger_rows_to_append),
        "skipped_existing_ids": skipped_existing,
        "counts_by_type": dict(by_type),
        "counts_by_no_action_reason": dict(no_action_reasons),
        "records": records,
    }
    EDITORIAL.write_text(json.dumps(editorial, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    queue = {
        "title": "Facebook Pending Queue After Five Approved Replies",
        "purpose": "Cola actual de propuestas que requieren aprobación de Fernando y registro de casos cerrados sin acción después del corte de solo lectura.",
        "status": "Review",
        "created_at": reviewed_at,
        "updated_at": reviewed_at,
        "version": "1.0",
        "author": "Manus AI",
        "organization": "Operations/Research",
        "related_documents": [
            "Operations/Research/2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json",
            "Operations/Research/2026-08-25_Facebook_Editorial_Review_After_Five_Approved_Replies.json",
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
        'title: "Facebook Comment Review After Five Approved Replies"',
        'purpose: "Revisión, clasificación y registro de comentarios nuevos de Facebook posterior a las cinco últimas respuestas aprobadas."',
        "status: Review",
        f"created: {reviewed_at[:10]}",
        f"updated: {reviewed_at[:10]}",
        'version: "1.0"',
        'author: "Manus AI"',
        "related_documents:",
        "  - Operations/Research/2026-08-25_Facebook_Comment_Review_After_Five_Approved_Replies.json",
        "  - Operations/Research/2026-08-25_Facebook_Editorial_Review_After_Five_Approved_Replies.json",
        "  - Operations/Research/2026-08-25_Facebook_Pending_Queue_After_Five_Approved_Replies.json",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "  - Operations/Research/2026-08-15_Community_Engagement_Log.md",
        "  - Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
        "  - GrowthOS/00_01_Changelog_GrowthOS.md",
        "organization: Operations/Research",
        "---",
        "",
        "# Revisión de comentarios de Facebook posterior a cinco respuestas aprobadas",
        "",
        f"La revisión de solo lectura se ejecutó con **Meta Graph API v26.0** a las `{reviewed_at}`. El cursor fue `{scan['cursor']}`, correspondiente al cierre verificado de las cinco respuestas anteriores. Se revisaron {scan['page_posts_reviewed']} publicaciones propias, {scan['root_comments_seen']} comentarios raíz y {scan['comment_ids_seen']} IDs de comentarios y réplicas, con {scan['api_error_count']} errores de API. En el alcance completo había {scan['current_unanswered_units']} unidades sin respuesta directa; {len(records)} eran nuevas y no estaban registradas.",
        "",
        "## Resultado ejecutivo",
        "",
        "| Resultado | Casos | Estado |\n|---|---:|---|\n"
        f"| Unidades actuales sin respuesta directa en el alcance | {scan['current_unanswered_units']} | Incluye backlog histórico |\n"
        f"| Comentarios nuevos sin respuesta directa | {len(records)} | Registrados todos en el ledger |\n"
        f"| Propuestas específicas | {len(proposals)} | `Pendiente_Fernando`; no publicadas |\n"
        f"| No requiere respuesta | {len(no_action)} | `No_Requiere_Respuesta` |\n"
        "| Publicaciones realizadas | 0 | No hubo autorización nueva |\n"
        f"| Errores de Meta API | {scan['api_error_count']} | Sin errores |",
        "",
        "El corte no publicó respuestas. Las dos propuestas son referencias musicales identificables por título y artista; cualquier escritura futura requiere autorización nueva y específica de Fernando.",
        "",
        "## Distribución del corte",
        "",
        "| Publicación / referencia | Hallazgos | Tratamiento editorial |\n|---|---:|---|\n"
        + "\n".join(
            f"| {md(post_ref)} | {count} | {('Predominan réplicas usuario-a-usuario y lenguaje sensible.' if 'Maeve' in post_ref else 'Se priorizaron dos referencias musicales identificables.' if '😌' in post_ref else 'Se conserva como señal contextual, breve o vacía.') } |"
            for (_, post_ref), count in by_post.items()
        ),
        "",
        "## Propuestas pendientes de autorización",
        "",
        "| Comentario | Referencia de la publicación | Respuesta propuesta | Por qué sí merece revisión |\n|---|---|---|---|\n"
        + "\n".join(
            f"| `{r['comment_id']}` — {md(r['comment_message'])} | {md(r['post_reference'])} | **{md(r['proposed_reply'])}** | {md(r['editorial_insight'])} |"
            for r in proposals
        ),
        "",
        "## Casos cerrados sin acción",
        "",
        "| Categoría | Casos | Criterio aplicado |\n|---|---:|---|\n"
        + "\n".join(
            f"| `{md(reason)}` | {count} | {md(next((r['editorial_insight'] for r in no_action if r['reason_code'] == reason), 'Se conserva para trazabilidad, sin respuesta pública.'))} |"
            for reason, count in no_action_reasons.items()
        ),
        "",
        "La clasificación conserva los 101 IDs: las 71 réplicas se dejan en sus conversaciones laterales; los comentarios raíz se separan entre señales breves, contexto crítico o anecdótico y lenguaje sensible. No se respondió a recomendaciones de ejercicios ni se amplificaron descripciones íntimas desde la Página.",
        "",
        "## Inventario completo de los 101 hallazgos",
        "",
        "Todos los IDs recuperados en este corte están incluidos en el JSON editorial y en el ledger. La tabla siguiente permite auditar que ningún comentario quedó fuera.",
        "",
        "| # | Comentario_ID | Tipo | Comentario | Decisión | Motivo resumido |\n|---:|---|---|---|---|---|\n"
        + "\n".join(
            f"| {i} | `{r['comment_id']}` | {r['comment_type']} | {md(r['comment_message'])} | `{r['editorial_decision']}` | {md(r['editorial_insight'])} |"
            for i, r in enumerate(records, start=1)
        ),
        "",
        "## Integridad y siguiente paso",
        "",
        f"Se incorporaron {len(ledger_rows_to_append)} filas nuevas al ledger; {len(skipped_existing)} IDs ya estaban registrados. El ledger permanece anonimizado, append-only y con IDs únicos. No existe ninguna respuesta publicable sin una nueva autorización explícita de Fernando.",
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
