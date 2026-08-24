"""Register the post-Batch-14 Facebook review without publishing.

The script is idempotent: it appends each newly scanned comment once and uses
explicit editorial decisions to keep actionable proposals separate from
user-to-user conversations, low-signal comments, and escalation risks.
"""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
INPUT = RESEARCH / "2026-08-24_Facebook_Comment_Context_After_Batch14.json"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
OUT = RESEARCH / "2026-08-24_Facebook_Editorial_Review_After_Batch14.json"
PAGE_SOURCE = "Meta Graph API v26 — After Batch 14 review"

PROPOSALS = {
    "122151376083072582_1064431163230561": ("El doctor Kegel estaría orgulloso de este comentario. 😂", "Media", "Referencia directa al origen del ejercicio; permite un remate inteligente sin añadir contenido explícito."),
    "122151376539072582_1069501129107761": ("El comité de amigas ya emitió su veredicto. 😂", "Media", "Aporta validación social en tono de humor y responde a la experiencia que menciona el comentario."),
    "122151376083072582_1482819530395036": ("Ese comentario llegó con la experiencia certificada incluida. 😂🙈", "Media", "Dobles sentidos del meme; la respuesta acompaña el tono sin describir ni escalar contenido sexual."),
    "122151376011072582_1418262703532657": ("Scorpions siempre entra con nostalgia elegante; “You & I” queda muy bien en este mood. 🖤🌹", "Alta", "Referencia musical concreta y conectada con el mood de la publicación."),
    "122151376083072582_1042114515343799": ("El universo ya confirmó que los perritos vienen con efectos secundarios. 😂🙈", "Media", "Retoma el juego de palabras del comentario y mantiene el doble sentido en un nivel no gráfico."),
    "122151376083072582_4578713942406487": ("El universo no garantiza efectos secundarios; solo dejó el chiste servido. 😂🙈", "Media", "Responde al remate sexual del comentario sin competir con su intensidad ni añadir detalles."),
    "122151376083072582_1375056147466831": ("Ese es el espíritu: humor, salud y cero excusas. 😂✨", "Media", "El comentario combina el chiste con una referencia explícita a salud del suelo pélvico; la respuesta conserva ambos elementos con criterio."),
    "122151376083072582_1597619722155027": ("Jajaja, el debate se fue a otro universo; aquí solo veníamos por el ejercicio. 😂🙈", "Media", "Desescala una comparación sexual y devuelve la conversación al tema del meme."),
    "122151376083072582_1054911050596272": ("El algoritmo también quiso participar en la clase de anatomía. 😂🙈", "Alta", "Comentario autoconsciente sobre la distribución del meme; oportunidad de respuesta específica y compartible."),
    "122151376539072582_1723720622176837": ("El universo advierte: agarrarle gusto no sustituye la técnica. 😂", "Media", "Contesta el juego verbal sin añadir una descripción sexual explícita."),
    "122151376083072582_2128221185244977": ("El algoritmo dejó el doble sentido servido y ustedes hicieron el resto. 😂🙈", "Media", "Reacción a una segunda variante del chiste del perrito; mantiene continuidad sin repetir una plantilla."),
    "122151376539072582_1967578493929235": ("El universo deja la invitación en modo misterioso. 😌", "Media", "Comentario de coqueteo en una raíz, con una respuesta breve y cómplice que no escala."),
    "122151376083072582_1754742345836101": ("El universo recomienda empezar por la constancia, no por la urgencia. 😂", "Alta", "Expresa intención clara de experimentar el tema del meme; permite una respuesta editorial con criterio."),
    "122151376011072582_1511346237415004": ("Jajaja, esa canción llegó con la indirecta incluida. 😌", "Alta", "Mención directa a Universe Sent Me dentro de un hilo musical; la respuesta conecta el comentario con “Frío frío” de Juan Luis Guerra."),
    "122151376011072582_1076789614927276": ("“Mujer amante” entra justo en ese mood de canción que no pide permiso. 🖤", "Alta", "Título musical concreto que amplía la conversación del post sin respuesta genérica."),
    "122151376539072582_757157010825943": ("El comité científico del universo queda oficialmente convocado. 🧐😂", "Media", "El comentario presenta una afirmación irónica como evidencia científica; oportunidad de remate temático."),
    "122151376083072582_1508436187637419": ("El universo repite tema, pero ustedes nunca repiten el comentario. 😂", "Media", "Alude a la continuidad del contenido y reconoce el nuevo giro del hilo."),
    "122151376539072582_2105653843654560": ("La leche también quiso entrar al debate nutricional. 😂", "Media", "Juega con la explicación literal del comentario y el doble sentido del post sin añadir explicitud."),
    "122151376365072582_1038307515745573": ("A veces el aire dice más que cualquier promesa. 💔", "Alta", "Comentario reflexivo sobre una publicación de ruptura; respuesta emocional y específica."),
    "122151376083072582_1037049892299180": ("Amarre, sí, pero con rutina incluida. 😂", "Media", "Retoma la idea de amarre del comentario y la conecta con el ejercicio del meme."),
    "122151376629072582_1041344015455456": ("Hay tronos que parecen lejanos, pero el universo siempre encuentra la forma de acercar la señal. ✨", "Alta", "Comentario filosófico en una publicación sobre el cambio; oportunidad de respuesta con voz de marca."),
    "122151376011072582_1780015050089465": ("“Sueños del alma” le queda perfecto a ese mood: suave por fuera, intenso por dentro. ✨", "Media", "Referencia musical o poética específica que encaja con la publicación y permite una respuesta con criterio."),
    "122151376083072582_1852477149460266": ("La llave podrá ser de alta presión, pero el universo también exige buena técnica. 😂", "Media", "Riff específico sobre la metáfora de la llave; responde al comentario sin escalar el contenido sexual."),
    "122151376083072582_1658593382547991": ("El universo no entrega experiencias por catálogo, pero recomienda ir sin prisa. 😅", "Media", "Expresa falta de experiencia; la respuesta mantiene empatía y prudencia sin prometer ni describir."),
}

SPECIAL_NO_ACTION = {
    "122151376083072582_1345634194224651": "Agradecimiento breve sin señal adicional; conservar el tono del ledger sin forzar una respuesta genérica.",
    "122151376083072582_1814552109914822": "Agradecimiento breve sin señal adicional; no requiere intervención de la Página en este corte.",
    "122151376539072582_1719781712610755": "Comentario demasiado breve y ambiguo para construir una respuesta específica.",
    "122151376539072582_1809525246881121": "Reacción ambigua de baja señal; no hay una idea concreta que desarrollar.",
    "122151376539072582_2104411286852333": "Emoji aislado; no requiere respuesta de la Página.",
    "122151376083072582_2189838228609288": "Solicitud sexual explícita y de baja señal; no sumar escalada ni normalizar una respuesta gráfica.",
    "122151376539072582_1038391735671409": "Oferta de servicio con tono promocional/sexual; no es una oportunidad de engagement de la Página.",
    "122151376539072582_1097649419495817": "Remate sexual breve y ambiguo; no construir una respuesta sin contexto suficiente.",
    "122151376539072582_2185999025299395": "Reacción breve y ambigua; no requiere una respuesta específica.",
    "122151376083072582_1424399456418240": "Elogio aislado de baja señal; responder sería una fórmula genérica.",
    "122151376539072582_2801993696836141": "Invitación sexual abierta; no responder para evitar escalada y mantener el tono no gráfico de USM.",
}


def default_no_action(record):
    if record["comment_type"] == "Replica_Anidada":
        return "Réplica dentro de una conversación usuario-a-usuario; intervenir rompería el intercambio y no hay solicitud clara a la Página."
    message = (record.get("comment_message") or "").lower()
    if any(term in message for term in ("20cm", "domicilio", "el oyo", "semen", "penes grandes", "pompitas")):
        return "Contenido sexual explícito, solicitación o promoción; no añadir una respuesta que escale el hilo."
    if len(message.strip()) <= 12:
        return "Señal baja o ambigua; no hay suficiente material para una respuesta específica de USM."
    return "No intervenir: comentario de baja señal, conversación lateral o contenido que no requiere una respuesta de la Página."


review = json.loads(INPUT.read_text(encoding="utf-8"))
candidates = review["records"]
ids = {record["comment_id"] for record in candidates}
if set(PROPOSALS) & set(SPECIAL_NO_ACTION):
    raise SystemExit("OVERLAPPING_EDITORIAL_DECISIONS")
if set(PROPOSALS) | set(SPECIAL_NO_ACTION) - ids:
    # This branch is intentionally not used; exact coverage is checked below.
    pass

editorial_records = []
for record in candidates:
    comment_id = record["comment_id"]
    if comment_id in PROPOSALS:
        proposed, priority, insight = PROPOSALS[comment_id]
        decision = "Pendiente_Respuesta"
        approval = "Pendiente_Fernando"
        moderation = "Revisar"
        action = "Revisar con Fernando"
        signal = "Oportunidad de engagement específica"
    else:
        proposed = "No responder"
        priority = "Baja"
        insight = SPECIAL_NO_ACTION.get(comment_id, default_no_action(record))
        decision = "No_Requiere_Respuesta"
        approval = "No_Aplica"
        moderation = "No_Accion"
        action = "Ninguna"
        signal = "No accionable en este corte"
    editorial_records.append({
        **record,
        "editorial_decision": decision,
        "approval_state": approval,
        "priority": priority,
        "signal_class": signal,
        "proposed_reply": proposed,
        "editorial_insight": insight,
        "registered_at": None,
        "publication_count": 0,
        "read_only_review": True,
        "requires_explicit_approval": decision == "Pendiente_Respuesta",
        "moderation_state": moderation,
        "calendar_action": action,
    })

proposal_count = sum(item["editorial_decision"] == "Pendiente_Respuesta" for item in editorial_records)
no_action_count = sum(item["editorial_decision"] == "No_Requiere_Respuesta" for item in editorial_records)
if len(editorial_records) != 83 or proposal_count != 24 or no_action_count != 59:
    raise SystemExit(f"UNEXPECTED_DECISION_COUNTS records={len(editorial_records)} proposals={proposal_count} no_action={no_action_count}")
if set(item["comment_id"] for item in editorial_records) != ids:
    raise SystemExit("DECISION_COVERAGE_MISMATCH")

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
for item in editorial_records:
    item["registered_at"] = now

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    fieldnames = reader.fieldnames
    rows = list(reader)
if fieldnames is None:
    raise SystemExit("LEDGER_HEADER_MISSING")
existing = {row["Comentario_ID"]: row for row in rows}
new_count = 0
updated_count = 0
for item in editorial_records:
    cid = item["comment_id"]
    ledger_row = {
        "Comentario_ID": cid,
        "Post_ID": item.get("post_id") or "",
        "CNT_ID": "",
        "Fecha_Comentario": item.get("comment_created_time") or "",
        "Plataforma": "Facebook",
        "Tipo": item.get("comment_type") or "",
        "Señal": item["signal_class"],
        "Respuesta_Estado": item["editorial_decision"],
        "Respuesta_Sugerida": item["proposed_reply"],
        "Aprobacion_Estado": item["approval_state"],
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": item["editorial_insight"],
        "Accion_Calendario": item["calendar_action"],
        "Prioridad": item["priority"],
        "Moderacion_Estado": item["moderation_state"],
        "Asset_Respuesta_ID": "",
        "Privacidad": "Anonimizado",
        "Fuente": PAGE_SOURCE,
        "Ultima_Sincronizacion": now,
    }
    if cid in existing:
        if existing[cid].get("Fuente") != PAGE_SOURCE:
            raise SystemExit(f"COMMENT_ID_ALREADY_EXISTS_WITH_OTHER_SOURCE:{cid}")
        existing[cid] = ledger_row
        updated_count += 1
    else:
        rows.append(ledger_row)
        existing[cid] = ledger_row
        new_count += 1

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

result = {
    "title": "Facebook Editorial Review After Batch 14",
    "purpose": "Registro editorial de comentarios nuevos sin respuesta encontrados después del Batch 14; conserva todos los hallazgos y separa propuestas de no acción.",
    "status": "Review",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Context_After_Batch14.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch14.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Community_Engagement_Log.md",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 / post-Batch-14 read-only review",
    "read_only_review": True,
    "approval_required_for_publication": True,
    "cursor_source": "2026-08-24_Facebook_Comment_Publication_Batch_14.json",
    "cursor": "2026-08-24T04:14:14+00:00",
    "candidate_count": len(editorial_records),
    "proposal_count": proposal_count,
    "no_action_count": no_action_count,
    "newly_registered_count": new_count,
    "idempotent_updated_count": updated_count,
    "publication_count": 0,
    "ledger_rows_after_registration": len(rows),
    "records": editorial_records,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("candidate_count", "proposal_count", "no_action_count", "newly_registered_count", "idempotent_updated_count", "publication_count", "ledger_rows_after_registration")}, ensure_ascii=False))
