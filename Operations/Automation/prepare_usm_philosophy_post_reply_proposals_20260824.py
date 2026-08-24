"""Classify all unanswered roots on the correct ☁️✨🤔 post and prepare USM replies."""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Comment_Review_Post_Batch10.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
JSON_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.json"
MD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.md"
RECORD_OUT = ROOT / "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Review_Record.json"

PROPOSALS = {
    "122151375549072582_1442803861236285": ("El universo recibe esa teoría con una ceja levantada: el hombre creando a su propio creador. 🤔✨", "Retoma directamente la tesis del comentario y el giro del meme."),
    "122151375549072582_872181139160064": ("Jajaja, el diosito también se puede confundir; la pregunta venía con trampa. 😅🤔", "Devuelve la reacción emocional al meme sin entrar a corregir una creencia."),
    "122151375549072582_1780347913099754": ("El creador sí se puso creativo con las luciérnagas. 😂✨", "Responde al ejemplo de las luciérnagas sin repetir el lenguaje corporal explícito."),
    "122151375549072582_972981675802863": ("El humano quiere descifrar el cosmos mientras todavía negocia con su propia mente. 🤔😂", "Retoma el contraste entre la curiosidad cósmica y el dominio de uno mismo."),
    "122151375549072582_1586390436263285": ("Ese es el espejo incómodo del meme: crear al creador a nuestra imagen. 🤔✨", "Responde a la formulación exacta de imagen y semejanza."),
    "122151375549072582_1039895839038595": ("La humanidad ya se nominó sola. 😂🤔", "Remate breve para la respuesta de una sola frase."),
    "122151375549072582_1644442960710725": ("El imaginario colectivo también pidió crédito de autoría. 🤔✨", "Retoma el concepto central sin sonar a plantilla."),
    "122151375549072582_1403487698543780": ("La imaginación humana siempre llega con presupuesto ilimitado. 😎✨", "Convierte la interpretación del comentario en un remate visual y específico."),
    "122151375549072582_1617891193262090": ("El cerebro creativo se fue demasiado lejos con esta pregunta. 😂🌌", "Mantiene el tono ligero sin reforzar el insulto o la etiqueta del comentario."),
    "122151375549072582_1642353581234558": ("Ahí está la paradoja: si siempre existió, la pregunta cambia de dueño. 🤔✨", "Responde a la idea de existencia eterna con la misma paradoja del post."),
    "122151375549072582_2682838392118151": ("Los griegos ya tenían una mitología lista para cubrir ese puesto. 😂🏛️", "Retoma la referencia griega en lugar de elogiarla de forma genérica."),
    "122151375549072582_1783035276182829": ("Con razón el universo salió con tantas preguntas pendientes. 😂🌌", "Devuelve el chiste sobre fumar sin añadir detalles ni escalarlo."),
    "122151375549072582_2553794695093209": ("Ese “usted mismo” viene con demasiada seguridad para una pregunta eterna. 😉🤔", "Responde al tono confiado y coloquial del comentario."),
    "122151375549072582_2242124606609181": ("Dios siendo Dios y el hilo intentando tomar apuntes. 😂🤔", "Retoma exactamente la lectura humorística de Dios actuando como Dios."),
    "122151375549072582_27540592708951388": ("El ave fénix al menos tiene experiencia con empezar desde cero. 🔥🤔", "Usa la imagen del ave fénix para conectar con el origen y la creación."),
    "122151375549072582_2139938020237319": ("Esa es la trampa: si tiene creador, ya no sería el primero. 🤔", "Responde directamente a la pregunta sin repetir el insulto del comentario."),
    "122151375549072582_1859721888531923": ("Loca, pero de esas que se quedan dando vueltas todo el día. 😂🤔", "Valida el efecto del meme con un remate de personalidad propia."),
    "122151375549072582_1271513331667499": ("Exacto: ahí es donde el meme deja de ser chiste y se vuelve paradoja. 🤔✨", "Retoma la contradicción central de crear algo que siempre estuvo."),
    "122151375549072582_1345438560907663": ("Llegó el gran Yo con respuesta incluida. 😌🤔", "Juega con la fórmula exacta del comentario sin añadir una referencia innecesaria."),
    "122151375549072582_1284524650312354": ("La hormiga no necesita conocer al panadero para seguir preguntando por la miga; quizá ahí está el punto. 🤔✨", "Retoma la metáfora de la hormiga y la miga, que es el núcleo distintivo del comentario."),
    "122151375549072582_2159556928109209": ("La misma trampa, pero con plumas: una pregunta que se persigue a sí misma. 😂🐔", "Responde a la comparación huevo-gallina con un giro breve y específico."),
    "122151375549072582_1933875761350410": ("El “nosotros” vuelve a aparecer: la humanidad no piensa soltar el crédito. 😂🤔", "Retoma la palabra clave y la conecta con el tema de autoría."),
    "122151375549072582_1046880914865088": ("El sospechoso habitual del hilo: el hombre. 😂🤔", "Remate corto para una respuesta breve y recurrente del hilo."),
    "122151375549072582_1074916168231993": ("Nosotros otra vez… esto ya parece una junta de accionistas de la creación. 😂", "Diferencia la segunda aparición de “Nosotros” con una imagen nueva."),
    "122151375549072582_2089754968329324": ("El universo registró ese “hit” y se quedó pensando. 😂✨", "Responde al “hit” sin inventar una interpretación musical no expresada."),
    "122151375549072582_1004388505976156": ("El hilo se puso más intenso que la pregunta original. Mejor volvamos al misterio central: ¿quién creó al creador? 🤔", "Desescala el lenguaje despectivo y devuelve la conversación al tema del post sin tono de moderación."),
    "122151375549072582_942638681466045": ("La pregunta encontró una respuesta bastante contundente… y bastante incendiaria. 🤔😂", "Mantiene el remate juguetón sin repetir las expresiones vulgares."),
    "122151375549072582_1110818364949332": ("El hilo ya pasó de la filosofía a los gritos del multiverso. 😂🌌", "No compite con el insulto; reconoce la escalada y conserva el tono USM."),
}
NO_ACTION = {
    "122151375549072582_1046418834638831": "Texto aislado de una sola palabra sin señal suficiente.",
    "122151375549072582_1837178844383978": "Respuesta de una sola palabra; no hay contexto adicional que retomar.",
    "122151375549072582_2263197197773933": "Referencia aislada a una persona/familiar; no responde de forma clara al contenido del post.",
    "122151375549072582_1775198897248896": "Puntuación aislada.",
    "122151375549072582_1383611429837958": "Solo emojis; no se fuerza una respuesta genérica.",
    "122151375549072582_2076221029645579": "Nombre aislado; parece etiqueta o identificación, no una reacción desarrollada al post.",
    "122151375549072582_2044378132857128": "Nombre aislado; no hay señal textual suficiente para responder.",
    "122151375549072582_1640754384339219": "Solo emojis; no se fuerza una respuesta genérica.",
    "122151375549072582_1450732226864481": "Comentario vacío.",
}


def display_text(text):
    text = (text or "").strip().replace("\n", " ")
    return text or "[comentario vacío]"


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
roots = [item for item in audit.get("unanswered", []) if item.get("comment_type") == "Comentario_Raiz"]
if len(roots) != 37:
    raise SystemExit(f"EXPECTED_37_UNANSWERED_ROOTS: {len(roots)}")
if set(item["comment_id"] for item in roots) != set(PROPOSALS) | set(NO_ACTION):
    raise SystemExit("ROOT_IDS_DO_NOT_MATCH_CLASSIFICATION")

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}

proposal_items = []
no_action_items = []
new_ids = []
for raw in roots:
    cid = raw["comment_id"]
    if cid in PROPOSALS:
        reply, reason = PROPOSALS[cid]
        item = {"comment_id": cid, "comment_message": display_text(raw.get("comment_message")), "comment_created_time": raw.get("comment_created_time"), "suggested_reply": reply, "reason": reason, "status": "Pendiente_Respuesta", "approval_status": "Pendiente_Fernando"}
        proposal_items.append(item)
    else:
        item = {"comment_id": cid, "comment_message": "[nombre, emoji, vacío o señal insuficiente]", "comment_created_time": raw.get("comment_created_time"), "suggested_reply": "", "reason": NO_ACTION[cid], "status": "No_Requiere_Respuesta", "approval_status": "No_Aplica"}
        no_action_items.append(item)
    row = by_id.get(cid)
    if row is None:
        row = {key: "" for key in fieldnames}
        row["Comentario_ID"] = cid
        row["Post_ID"] = audit.get("post_id", "")
        row["CNT_ID"] = ""
        row["Fecha_Comentario"] = raw.get("comment_created_time", "")
        row["Plataforma"] = "Facebook"
        row["Tipo"] = "Comentario_Raiz"
        rows.append(row)
        by_id[cid] = row
        new_ids.append(cid)
    row.update({
        "Señal": "Post_☁️✨🤔_Batch10_Review",
        "Respuesta_Estado": item["status"],
        "Respuesta_Sugerida": item["suggested_reply"],
        "Aprobacion_Estado": item["approval_status"],
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": item["reason"],
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media" if item["suggested_reply"] else "Baja",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — auditoría completa del post ☁️✨🤔 después de Batch 10",
        "Ultima_Sincronizacion": audit.get("reviewed_at", ""),
    })

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

proposal_items.sort(key=lambda item: item.get("comment_created_time") or "", reverse=True)
no_action_items.sort(key=lambda item: item.get("comment_created_time") or "", reverse=True)
payload = {
    "title": "Facebook ☁️✨🤔 Post Batch 10 Reply Proposals",
    "purpose": "Revisar las 37 raíces que seguían sin respuesta en el post ☁️✨🤔 después de la publicación del Batch 10 y proponer respuestas con personalidad de Universe Sent Me.",
    "status": "Review",
    "created_at": audit.get("reviewed_at"),
    "updated_at": audit.get("reviewed_at"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Comment_Review_Post_Batch10.json",
        "Operations/Research/2026-08-24_Facebook_Comment_Publication_Batch_10.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Review_Record.json",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0 / direct post comments + one-level nested replies",
    "reviewed_at": audit.get("reviewed_at"),
    "post_id": audit.get("post_id"),
    "root_comments_without_direct_page_reply": len(roots),
    "proposal_count": len(proposal_items),
    "no_action_count": len(no_action_items),
    "new_ledger_rows": len(new_ids),
    "publication_performed": False,
    "proposals": proposal_items,
    "no_action": no_action_items,
    "next_step": "Fernando puede aprobar un subconjunto por IDs; no publicar estas propuestas sin autorización explícita.",
}
JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = [
    "# Propuestas de respuesta — post ☁️✨🤔 después de Batch 10",
    "",
    "**Propósito:** revisar todas las raíces sin respuesta del post correcto y preparar remates con personalidad de Universe Sent Me.",
    "**Estado:** Review",
    "**Fecha de creación:** 2026-08-24",
    "**Última actualización:** 2026-08-24",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_USM_Philosophy_Post_Comment_Review_Post_Batch10.json`; `2026-08-24_Facebook_Comment_Publication_Batch_10.json`; `2026-08-15_Community_Engagement_Log.csv`",
    "**Organización:** Operations/Research",
    "",
    f"La auditoría correcta del post `1036844829507460_122151375549072582` encontró **{len(roots)} raíces sin respuesta directa** después del Batch 10. Se prepararon **{len(proposal_items)} propuestas específicas** y **{len(no_action_items)} casos sin acción**. No se publicó ninguna respuesta de este corte.",
    "",
    "## Propuestas con personalidad USM",
    "",
    "| Comentario | Respuesta propuesta |",
    "|---|---|",
]
for item in proposal_items:
    md.append(f"| {item['comment_message']} | **{item['suggested_reply']}** |")
md.extend([
    "",
    "## Casos sin acción",
    "",
    "| Caso | Motivo |",
    "|---|---|",
])
for item in no_action_items:
    md.append(f"| {item['comment_message']} | {item['reason']} |")
md.extend([
    "",
    "## Regla de publicación",
    "",
    "Las 28 propuestas quedan pendientes de aprobación explícita de Fernando. Los casos sin acción no deben recibir respuestas genéricas, y cualquier futura publicación deberá pasar por preconsulta anti-duplicado y verificación en Meta Graph API v26.0.",
])
MD_OUT.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

record = {
    "title": "Facebook ☁️✨🤔 Post Batch 10 Review Record",
    "purpose": "Registrar las 37 raíces revisadas del post ☁️✨🤔: 28 propuestas y 9 casos sin acción.",
    "status": "Active",
    "created_at": audit.get("reviewed_at"),
    "updated_at": audit.get("reviewed_at"),
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Comment_Review_Post_Batch10.json",
        "Operations/Research/2026-08-24_Facebook_USM_Philosophy_Post_Batch10_Reply_Proposals.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0",
    "reviewed_at": audit.get("reviewed_at"),
    "roots_reviewed": len(roots),
    "proposal_count": len(proposal_items),
    "no_action_count": len(no_action_items),
    "new_rows_added": len(new_ids),
    "publication_performed": False,
    "new_comment_ids": new_ids,
}
RECORD_OUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"roots_reviewed": len(roots), "proposals": len(proposal_items), "no_action": len(no_action_items), "new_ledger_rows": len(new_ids)}, ensure_ascii=False))
