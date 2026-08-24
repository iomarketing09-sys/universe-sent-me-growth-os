"""Record Batch 14 editorial review without publishing anything to Facebook."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json"
INVENTORY = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Current_Unanswered_Inventory.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Batch14_Engagement_Proposals.json"

# Editorial decisions are based on visible comment text and thread context. No names are stored here.
DECISIONS = {
    "122151376011072582_1844719709832925": {"action": "proposal", "signal": "Recomendación musical", "reference": "Saturno — Rafa Espino", "reply": "Saturno de Rafa Espino… esa sí deja el corazón orbitando un rato. 🪐🎶", "priority": "Media", "insight": "La persona aportó una canción concreta; responder al título y artista evita un agradecimiento musical genérico."},
    "122151376011072582_1060227956395275": {"action": "proposal", "signal": "Playlist musical", "reference": "Warcry, Kaleus, Mago de Oz y Macaco", "reply": "Eso ya es una playlist con cuatro formas de decir lo mismo: aquí hay sentimientos y no pocos. 🎶✨", "priority": "Media", "insight": "La lista reúne cuatro canciones y merece una respuesta que reconozca su hilo emocional, no un elogio genérico."},
    "122151376011072582_4502922900025556": {"action": "proposal", "signal": "Recomendación musical", "reference": "Canción de cuna — Los Piojos", "reply": "‘Canción de cuna’ de Los Piojos… elección para cuando el recuerdo no quiere dormir. 🎶🌙", "priority": "Media", "insight": "La respuesta juega con el título y conserva el tono nocturno sin inventar una interpretación extensa."},
    "122151376011072582_1418254450159338": {"action": "proposal", "signal": "Historia personal y música de duelo", "reference": "Amor eterno y una ausencia que no era de pareja", "reply": "Hay ausencias que no necesitan haber sido pareja para doler así. ‘Amor eterno’ lo entiende demasiado bien. 🥺🎶", "priority": "Alta", "insight": "Reconoce la pérdida sin diagnosticar ni hacer humor; conecta la experiencia con la canción concreta."},
    "122151376011072582_1568269204678844": {"action": "proposal", "signal": "Referencia musical de despedida", "reference": "Mi historia entre tus dedos", "reply": "‘Mi historia entre tus dedos’… de esas canciones que convierten una despedida en escena completa. 🎶🥀", "priority": "Media", "insight": "Responde a la imagen emocional del título sin afirmar artista o contexto que la persona no indicó."},
    "122151376539072582_1448883027065510": {"action": "proposal", "signal": "Doble sentido con petición de resultado", "reference": "Pregunta sobre hacer crecer los 🍑 en el meme de Maeve", "reply": "Jajaja, el universo no promete resultados, pero sí recomienda constancia. 😂🙈", "priority": "Media", "insight": "Devuelve el juego sobre la petición sin añadir instrucciones ni escalar el contenido sexual."},
    "122151376083072582_932843502558471": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Réplica breve de aprobación en el hilo del meme", "reason": "Réplica dirigida a otra persona; no interrumpir una conversación usuario-a-usuario.", "priority": "Baja", "insight": "Mención o reacción breve sin solicitud dirigida a la Página."},
    "122151376083072582_28802659646003528": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Réplica breve de aprobación en el hilo del meme", "reason": "Réplica dirigida a otra persona; no interrumpir una conversación usuario-a-usuario.", "priority": "Baja", "insight": "Mención o reacción breve sin solicitud dirigida a la Página."},
    "122151376083072582_1367795585545947": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Réplica breve dentro del hilo del meme", "reason": "Réplica de usuario sin apertura clara para la Página.", "priority": "Baja", "insight": "La señal es demasiado breve y está dirigida a otra persona."},
    "122151376083072582_1875655376797902": {"action": "proposal", "signal": "Lenguaje sexualizado de doble sentido", "reference": "Comparación explícita de dos prácticas en el meme", "reply": "Jajaja, el comentario llegó con manual técnico incluido. 😂🙈", "priority": "Media", "insight": "Respuesta cómplice y no gráfica; reconoce la intensidad sin competir con ella ni añadir detalles."},
    "122151376539072582_1468084575158511": {"action": "no_action", "signal": "Texto de baja señal", "reference": "Frase breve y ambigua sobre el meme de Maeve", "reason": "No hay una lectura suficientemente clara para responder sin inventar contexto.", "priority": "Baja", "insight": "Texto ambiguo; mantener fuera de publicación."},
    "122151376083072582_1216558461547643": {"action": "proposal", "signal": "Juego de palabras del meme", "reference": "El famoso perrito 🥰", "reply": "El universo ya tiene demasiadas especies involucradas en esto. 😂", "priority": "Media", "insight": "Continúa el juego de especies que la persona ya introdujo, sin agregar una referencia ajena."},
    "122151376011072582_2122543521717318": {"action": "proposal", "signal": "Corrección dirigida a la Página", "reference": "Réplica que corrige el remate de ‘Frío frío’ de Juan Luis Guerra", "reply": "Jajaja, tienes razón: el frío era solo en el título; la confusión fue nuestra. 😂🎶", "priority": "Alta", "insight": "La réplica menciona a la Página y responde directamente a su intervención; merece continuidad específica."},
    "122151376083072582_1766545104476907": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Réplica de broma entre comentaristas del meme", "reason": "Intercambio dirigido a otra persona; no interrumpir por defecto.", "priority": "Baja", "insight": "Conversación social sin solicitud de intervención de la Página."},
    "122151376083072582_1539874414078742": {"action": "proposal", "signal": "Complicidad breve con el meme", "reference": "El chiquito siempre 🤭", "reply": "Jajaja, ese detalle no pasó desapercibido. 😂🙈", "priority": "Media", "insight": "La respuesta reconoce exactamente el detalle que el comentario subraya, sin volverlo más explícito."},
    "122151376083072582_28148795568072687": {"action": "no_action", "signal": "Aprobación breve", "reference": "Jajaja se pasan…", "reason": "Risa o aprobación de baja señal sin una apertura concreta para conversación.", "priority": "Baja", "insight": "Confirmación de comprensión, pero sin contexto adicional."},
    "122151376539072582_1049776371233063": {"action": "proposal", "signal": "Doble sentido y precisión humorística", "reference": "Aclaración humorística sobre la forma de la situación del meme", "reply": "Jajaja, el universo agradece la precisión técnica. 😂🙈", "priority": "Media", "insight": "Devuelve el remate como falsa precisión técnica y no agrega contenido explícito."},
    "122151376083072582_1959476711400866": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Réplica nueva sobre la versión de otro familiar", "reason": "Réplica dirigida a otra persona dentro de un intercambio usuario-a-usuario; no intervenir.", "priority": "Baja", "insight": "Es el único comentario posterior al cursor Batch 13, pero no está dirigido a la Página."},
    "122151375465072582_4699112460337022": {"action": "no_action", "signal": "Reacción de emoji", "reference": "💞🫶✨ en una publicación de Maeve y Kael", "reason": "Reacción afectiva sin texto; no permite construir una respuesta específica.", "priority": "Baja", "insight": "Señal positiva de baja fricción, sin contexto textual."},
    "122151376083072582_1363924695858655": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Corrección de otra persona sobre el ejercicio del meme", "reason": "Réplica técnica dirigida a otra persona; no interrumpir el hilo.", "priority": "Baja", "insight": "No es una pregunta dirigida a la Página."},
    "122151376083072582_3701844673318079": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Réplica breve dentro del hilo del meme", "reason": "Réplica dirigida a otra persona; no interrumpir por defecto.", "priority": "Baja", "insight": "Mención breve sin solicitud de intervención."},
    "122151376083072582_27750034838001055": {"action": "no_action", "signal": "Etiqueta o nombre aislado", "reference": "Nombre aislado dentro del hilo del meme", "reason": "Nombre o etiqueta sin contexto suficiente para una respuesta de la Página.", "priority": "Baja", "insight": "Posible identificación entre usuarios, no oportunidad autónoma."},
    "122151376539072582_27935583276097528": {"action": "no_action", "signal": "Respuesta de baja señal", "reference": "Si tú en el meme de Maeve", "reason": "Identificación demasiado breve y sin contexto adicional.", "priority": "Baja", "insight": "Puede expresar identificación, pero no abre una conversación útil."},
    "122151376083072582_2217697402410708": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Réplica que nombra el ejercicio del meme", "reason": "Réplica dirigida a otra persona; no interrumpir el hilo.", "priority": "Baja", "insight": "Aporta contexto al intercambio entre usuarios, no una petición a la Página."},
    "122151376083072582_2294338478000981": {"action": "proposal", "signal": "Aprobación explícita del meme", "reference": "Amén 🤣🤣", "reply": "Ese amén viene con toda la convicción. 😂✨", "priority": "Media", "insight": "Retoma la palabra exacta del comentario y la convierte en un remate de marca."},
    "122151375843072582_842359288869319": {"action": "no_action", "signal": "Risa breve", "reference": "Jajajaj en una publicación de autoobservación", "reason": "Risa aislada sin contenido adicional al que responder.", "priority": "Baja", "insight": "Señal de agrado, pero no oportunidad conversacional independiente."},
    "122151376083072582_1053899660748200": {"action": "no_action", "signal": "Conversación entre usuarios", "reference": "Elogio dirigido a otra persona dentro del hilo", "reason": "Réplica social sin solicitud a la Página; no interrumpir.", "priority": "Baja", "insight": "La persona está conversando con otro usuario."},
    "122151376083072582_910971145400039": {"action": "proposal", "signal": "Consejo humorístico sobre el meme", "reference": "Recomendación de apretar y soltar al hacer pipí", "reply": "Jajaja, el tutorial llegó con instrucciones incluidas. 😂🙈", "priority": "Media", "insight": "Reconoce el formato de tutorial sin validar ni ampliar la recomendación; mantiene el tono no gráfico."},
    "122151375549072582_1356485370871041": {"action": "no_action", "signal": "Conversación filosófica entre usuarios", "reference": "Réplica teológica extensa sobre el Tao y Giordano Bruno", "reason": "Aporte dirigido a otros participantes en un debate ya abierto; no interrumpir sin una petición a la Página.", "priority": "Baja", "insight": "Debate entre usuarios; intervenir requeriría asumir una postura doctrinal."},
    "122151375549072582_1759740911890964": {"action": "no_action", "signal": "Conversación filosófica entre usuarios", "reference": "Réplica teológica extensa sobre el nombre de Dios", "reason": "Debate entre usuarios sin solicitud dirigida a la Página; no interrumpir.", "priority": "Baja", "insight": "No responder para evitar entrar institucionalmente en una disputa doctrinal."},
    "122151375549072582_1009066035494694": {"action": "no_action", "signal": "Conversación filosófica entre usuarios", "reference": "Réplica sobre existencia, dualidad y Dios", "reason": "Réplica dirigida a otros usuarios; no interrumpir la conversación.", "priority": "Baja", "insight": "Intercambio doctrinal entre seguidores."},
    "122151375549072582_1068685309201303": {"action": "no_action", "signal": "Conversación filosófica entre usuarios", "reference": "Réplica sobre metáfora, astrología y Nietzsche", "reason": "Debate entre usuarios sin pregunta dirigida a la Página.", "priority": "Baja", "insight": "Responder exigiría asumir o corregir una interpretación filosófica."},
    "122151375549072582_1800401234474137": {"action": "no_action", "signal": "Conversación filosófica entre usuarios", "reference": "Réplica sobre ciencia, religión e historia", "reason": "Aporte dirigido a otro usuario y no a la Página; no interrumpir.", "priority": "Baja", "insight": "Debate sensible que conviene dejar como conversación comunitaria."},
    "122151375549072582_1296590669083805": {"action": "no_action", "signal": "Conversación filosófica entre usuarios", "reference": "Réplica crítica sobre símbolos y sentido", "reason": "Discusión entre usuarios; no entrar con una respuesta institucional.", "priority": "Baja", "insight": "La respuesta de la Página no es necesaria para sostener el hilo."},
    "122151375549072582_1540949493877836": {"action": "no_action", "signal": "Conversación filosófica entre usuarios", "reference": "Réplica breve dentro del debate del post filosófico", "reason": "Réplica dirigida a otros participantes; no interrumpir.", "priority": "Baja", "insight": "Comentario de continuidad interna del hilo."},
    "122151375549072582_1702306021068700": {"action": "no_action", "signal": "Crítica entre usuarios", "reference": "Réplica que cuestiona la respuesta de otro usuario", "reason": "Disputa entre usuarios sin solicitud dirigida a la Página; no intervenir.", "priority": "Baja", "insight": "No convertir a la Página en árbitro del debate."},
    "122151375549072582_1307689874582977": {"action": "no_action", "signal": "Historia personal dentro de conversación", "reference": "Réplica sobre una relación pasada y una persona importante", "reason": "Historia compartida dentro de un hilo entre usuarios, sin pedir intervención de la Página.", "priority": "Baja", "insight": "La historia merece respeto, pero la Página no debe irrumpir en el intercambio."},
}

review = json.loads(REVIEW.read_text(encoding="utf-8"))
inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
all_inventory_rows = {row["comment_id"]: row for row in inventory["current_unanswered"]}
all_rows = {
    cid: row for cid, row in all_inventory_rows.items()
    if row.get("ledger_status") in {"Not_In_Ledger", "Sin_Revisar"}
}
missing = sorted(set(all_rows) - set(DECISIONS))
if missing:
    raise SystemExit("MISSING_EDITORIAL_DECISIONS: " + ",".join(missing))
extra_decisions = sorted(set(DECISIONS) - set(all_rows))
if extra_decisions:
    raise SystemExit("DECISION_NOT_IN_REVIEW_SCOPE: " + ",".join(extra_decisions))

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    ledger_rows = list(reader)
    fields = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in ledger_rows}

for cid, decision in DECISIONS.items():
    item = all_rows[cid]
    status = "Pendiente_Respuesta" if decision["action"] == "proposal" else "No_Requiere_Respuesta"
    approval = "Pendiente_Fernando" if decision["action"] == "proposal" else "No_Aplica"
    suggested = decision.get("reply", "No responder")
    row = by_id.get(cid)
    if row is None:
        row = {field: "" for field in fields}
        row.update({
            "Comentario_ID": cid,
            "Post_ID": item.get("post_id", ""),
            "CNT_ID": "",
            "Fecha_Comentario": item.get("comment_created_time", ""),
            "Plataforma": "Facebook",
            "Tipo": item.get("comment_type", "Comentario_Raiz"),
        })
        ledger_rows.append(row)
        by_id[cid] = row
    row.update({
        "Señal": decision["signal"],
        "Respuesta_Estado": status,
        "Respuesta_Sugerida": suggested,
        "Aprobacion_Estado": approval,
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": decision.get("insight", decision.get("reason", "")),
        "Accion_Calendario": "Ninguna",
        "Prioridad": decision["priority"],
        "Moderacion_Estado": "No_Accion",
        "Asset_Respuesta_ID": "",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — Batch 14 review",
        "Ultima_Sincronizacion": review["reviewed_at"],
    })

with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(ledger_rows)

proposals = []
no_action = []
for cid, decision in DECISIONS.items():
    item = all_rows[cid]
    record = {
        "comment_id": cid,
        "post_id": item.get("post_id"),
        "comment_type": item.get("comment_type"),
        "comment_created_time": item.get("comment_created_time"),
        "comment_message": item.get("comment_message", ""),
        "post_message": item.get("post_message", ""),
        "parent_comment_id": item.get("parent_comment_id"),
        "reference": decision["reference"],
        "signal": decision["signal"],
        "priority": decision["priority"],
        "already_logged_before_batch14": item.get("already_logged", False),
        "created_after_batch13_cursor": item.get("created_after_batch13_cursor", False),
    }
    if decision["action"] == "proposal":
        record.update({"status": "Pendiente_Respuesta", "approval_status": "Pendiente_Fernando", "suggested_reply": decision["reply"], "insight": decision["insight"]})
        proposals.append(record)
    else:
        record.update({"status": "No_Requiere_Respuesta", "approval_status": "No_Aplica", "reason": decision["reason"], "insight": decision["insight"]})
        no_action.append(record)

result = {
    "title": "Facebook Batch 14 Engagement Proposals",
    "purpose": "Reconciliar oportunidades nuevas y antiguas detectadas en el escaneo Batch 14 y preparar respuestas específicas para aprobación humana, sin publicar.",
    "status": "Review",
    "created_at": review["reviewed_at"],
    "updated_at": review["reviewed_at"],
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-24_Facebook_Comment_Review_Batch_14.json",
        "Operations/Research/2026-08-24_Facebook_Batch14_Current_Unanswered_Inventory.json",
        "Operations/Research/2026-08-24_Facebook_Batch14_Candidate_Context.json",
        "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch13.json",
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
    ],
    "organization": "Operations/Research",
    "source": "Meta Graph API v26.0, revisión de solo lectura",
    "read_only": True,
    "reviewed_at": review["reviewed_at"],
    "cursor": review["cursor"],
    "scan_counts": {
        "current_unanswered_units": review["current_unanswered_units"],
        "new_since_batch13_cursor": review["new_units_since_batch13_cursor"],
        "new_unanswered_not_in_ledger_since_batch13_cursor": review["new_unanswered_not_in_ledger_since_batch13_cursor"],
        "unanswered_reviewed_for_editorial_classification": len(DECISIONS),
        "already_classified_unanswered_not_reopened": len(all_inventory_rows) - len(all_rows),
        "proposals_pending_approval": len(proposals),
        "no_action_classifications": len(no_action),
        "api_error_count": review["api_error_count"],
    },
    "proposals": proposals,
    "no_action": no_action,
    "published": False,
    "authorization_required": True,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"reviewed": len(DECISIONS), "proposals": len(proposals), "no_action": len(no_action), "published": False}, ensure_ascii=False))
