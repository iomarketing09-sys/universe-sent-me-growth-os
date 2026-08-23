#!/usr/bin/env python3
"""Record the latest read-only Facebook review delta and proposed actions."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
JSON_PATH = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_03.json"
SYNCED_AT = "2026-08-23T19:09:24+0000"
CUTOFF = "2026-08-23T16:56:42+0000"
FIELDS = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo",
    "Señal", "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado",
    "Respuesta_Fecha", "Respuesta_Meta_ID", "Insight_Anonimo", "Accion_Calendario",
    "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID", "Privacidad", "Fuente",
    "Ultima_Sincronizacion",
]

# id, post_id, created, message, state, signal, suggestion, insight, priority, moderation
ROOT_SPECS = [
    ("122151376365072582_1397524005805789", "122151376365072582", "2026-08-23T18:32:35+0000", "Shr", "No_Requiere_Respuesta", "Texto demasiado breve para inferir intención", "No responder", "No hay contexto suficiente para una respuesta útil.", "Baja", "No_Accion"),
    ("122154733605072582_2041839189774293", "122154733605072582", "2026-08-23T18:37:40+0000", "Joshua Fe 👉🏽", "No_Requiere_Respuesta", "Nombre o mención sin contexto", "No responder", "El comentario no contiene una idea o solicitud clara.", "Baja", "No_Accion"),
    ("122151376083072582_1870186187563324", "122151376083072582", "2026-08-23T18:12:13+0000", "yo  pero a veces hasta me da miedo quedar atorada como perros", "Pendiente_Respuesta", "Remate sexualizado sobre el meme", "Jajaja, el modo travesura también viene con advertencias de seguridad. 😅🙈", "La usuaria continúa el humor del reel; responder con complicidad breve sin repetir la formulación explícita.", "Baja", "No_Accion"),
    ("122151376083072582_1385775342983817", "122151376083072582", "2026-08-23T17:37:33+0000", "Jajaja si soy", "Pendiente_Respuesta", "Autoidentificación humorística", "Jajaja, queda oficialmente confesado. 😂🙈", "Confirmación breve del remate; conviene responder con una línea ligera.", "Baja", "No_Accion"),
    ("122151376011072582_2033022903995271", "122151376011072582", "2026-08-23T17:00:53+0000", "Las cuatro estaciones, Antonio Vivaldi.", "Pendiente_Respuesta", "Recomendación musical de Vivaldi", "Las cuatro estaciones de Vivaldi: cuatro moods y todos con violines dramáticos. 🎻✨", "La propuesta recoge la estructura de cuatro estaciones y el dramatismo instrumental, en vez de elogiar de forma genérica.", "Media", "No_Accion"),
    ("122151376011072582_2110248423207879", "122151376011072582", "2026-08-23T18:08:10+0000", "Con migo danza el que ama mí Alma", "Pendiente_Respuesta", "Título o frase musical de tono poético", "‘Conmigo danza el que ama mi alma’: ese título ya llega con poesía y movimiento. 🎶✨", "La respuesta se apoya en el lenguaje poético del comentario sin atribuir artista ni datos no confirmados.", "Media", "No_Accion"),
    ("122151376011072582_1622582352867257", "122151376011072582", "2026-08-23T17:03:01+0000", "alguien como tú - Josean log", "Pendiente_Respuesta", "Recomendación de ‘Alguien como tú’ de Josean Log", "Alguien como tú de Josean Log: una elección que suena a nostalgia suave y confesión. 🎶✨", "El artista y el título permiten una reacción específica sobre el tono emocional de la elección.", "Media", "No_Accion"),
    ("122151375549072582_2854017014972594", "122151375549072582", "2026-08-23T18:59:03+0000", "Una singular singularidad singularizada singularmente", "Pendiente_Respuesta", "Juego verbal con ‘singularidad’", "Eso fue una singularidad verbal en expansión. 🤯✨", "El comentario funciona como experimento lingüístico y admite una respuesta breve sobre su propia repetición.", "Baja", "No_Accion"),
    ("122151375549072582_1041452398791312", "122151375549072582", "2026-08-23T19:08:26+0000", "Nosotros...por si no lo sabias", "Pendiente_Respuesta", "Respuesta colectiva sobre el origen", "El plot twist más incómodo: nosotros también estamos en la lista. 🤔✨", "Mantiene abierta la paradoja de creadores y criaturas sin tomar posición teológica.", "Media", "No_Accion"),
    ("122151375549072582_1963359551036593", "122151375549072582", "2026-08-23T18:40:01+0000", "Es algo q no te incumbe mortal ingrato😇", "Pendiente_Respuesta", "Remate de humor con voz divina", "Entendido, mortal se retira… pero deja la pregunta abierta. 😇😂", "El comentario adopta una voz celestial; la respuesta puede seguir el juego sin discutir la creencia.", "Baja", "No_Accion"),
    ("122151375549072582_1723626708895458", "122151375549072582", "2026-08-23T19:02:20+0000", "Y quien es el de este dibujo??", "Pendiente_Respuesta", "Pregunta directa sobre la figura de la imagen", "Es el creador del meme… aunque parece que él también está buscando quién lo creó. 😂✨", "La respuesta evita inventar un nombre de personaje y reacciona al texto de la imagen: una figura creadora que también pregunta por su origen.", "Media", "No_Accion"),
    ("122151375549072582_1370750357963444", "122151375549072582", "2026-08-23T17:26:55+0000", "Nosotros te creamos, y tú nos creaste. Confuso pero cierto.", "Pendiente_Respuesta", "Paradoja de creador y criatura", "Ese es el plot twist cósmico: creadores y criaturas mirándose al espejo. 🤔✨", "La propuesta recoge literalmente la reciprocidad del comentario sin convertirla en una afirmación doctrinal.", "Media", "No_Accion"),
    ("122151375549072582_2126386847941459", "122151375549072582", "2026-08-23T19:06:14+0000", "El hombre", "Pendiente_Respuesta", "Respuesta breve al origen de la figura", "Respuesta breve para una pregunta cósmica enorme. 😅🤔", "La brevedad del comentario es parte del remate; no hace falta añadir una tesis.", "Baja", "No_Accion"),
    ("122151375549072582_1365567789035301", "122151375549072582", "2026-08-23T19:05:30+0000", "La gente cree que Dios no existe, y que importa quien creo a Dios lo que importa es Que lo adores y le obedezcas , para que preguntar tanto si lo que importa es estar bien", "Pendiente_Respuesta", "Reflexión sobre fe, duda y práctica religiosa", "Ahí está la tensión interesante: para algunas personas importa la fe; para otras, seguir preguntando también forma parte de la búsqueda. 🤔✨", "Responder de forma neutral, sin validar una doctrina ni debatir la creencia personal del usuario.", "Media", "No_Accion"),
    ("122151375549072582_2272618483487529", "122151375549072582", "2026-08-23T18:40:17+0000", "Una super conciencia", "Pendiente_Respuesta", "Hipótesis de una superconciencia", "Una superconciencia: eso ya suena a que el universo se está pensando a sí mismo. 🤔✨", "La propuesta trata la idea como hipótesis creativa, no como hecho.", "Media", "No_Accion"),
    ("122151375549072582_901941632636512", "122151375549072582", "2026-08-23T18:44:12+0000", "Me decía una niña de 16 años , Dios existe porqué nosotros existimos.", "Pendiente_Respuesta", "Aforismo sobre existencia y creencia", "Una respuesta sencilla para una pregunta enorme: existencia y creencia encontrándose en la misma frase. 🤔✨", "No se diagnostica ni se afirma la verdad de la frase; se reconoce su carácter reflexivo.", "Media", "No_Accion"),
    ("122151375549072582_37855550027424046", "122151375549072582", "2026-08-23T17:52:54+0000", "Sofia la madre la sabiduria el neon que probiene del pleroma ella lo creo.", "Pendiente_Respuesta", "Referencia esotérica sobre el origen", "El hilo ya se fue de la teología a la cosmogonía. 🤔✨", "Responder al giro del hilo sin confirmar nombres, conceptos o relaciones teológicas no verificadas.", "Media", "No_Accion"),
    ("122151375549072582_1036994699332009", "122151375549072582", "2026-08-23T18:28:21+0000", "Pues quien ??? Yo mero \" el hombre\"", "Pendiente_Respuesta", "Autoatribución humorística del origen", "Ese ‘yo mero’ llegó con demasiada seguridad para una pregunta que lleva siglos abierta. 😂🤔", "El usuario responde con seguridad cómica; conviene mantener la paradoja en tono ligero.", "Baja", "No_Accion"),
    ("122151375549072582_1495068889305489", "122151375549072582", "2026-08-23T17:46:05+0000", "ájaa! De la mera exótica 😏🤣🤣", "Pendiente_Respuesta", "Remate coloquial y pícaro", "La mera exótica: respuesta oficial con sello de misterio y picardía. 😏😂✨", "El tono del comentario es juguetón y permite una respuesta cómplice sin explicar la imagen.", "Baja", "No_Accion"),
    ("122151375549072582_1377242193921035", "122151375549072582", "2026-08-23T18:32:14+0000", "Quien sabe 🥱🤔", "Pendiente_Respuesta", "Reconocimiento de incertidumbre", "La respuesta más honesta de todo el hilo: quién sabe. 🥱🤔✨", "El comentario funciona como remate de incertidumbre; conviene no cerrarlo con una explicación artificial.", "Baja", "No_Accion"),
    ("122151375549072582_2032167597504773", "122151375549072582", "2026-08-23T17:27:49+0000", "Êl asî mismo se creô, llegô del multiverso y se creô asî mismo para este universo.", "Pendiente_Respuesta", "Origen autocreado con giro de multiverso", "Plot twist de multiverso: se creó a sí mismo y llegó con su propio origen incluido. 🤯✨", "La respuesta sigue el marco fantástico del comentario sin presentar la idea como canon o hecho.", "Media", "No_Accion"),
    ("122151375549072582_2502202590246984", "122151375549072582", "2026-08-23T18:59:52+0000", "El humano después de fumar un porro jajaja", "Pendiente_Respuesta", "Humor sobre una explicación alterada del universo", "El humano después de fumar un porro: intentando resolver el origen del universo con confianza absoluta. 😂🌌", "Se conserva el chiste del usuario sin promover consumo ni convertirlo en recomendación.", "Baja", "No_Accion"),
    ("122151375549072582_1595535212280412", "122151375549072582", "2026-08-23T18:21:52+0000", "El humano", "Pendiente_Respuesta", "Respuesta breve: el humano como creador", "La humanidad nominada como creadora y criatura al mismo tiempo. 🤔✨", "La respuesta amplía el remate sin imponer una lectura religiosa.", "Baja", "No_Accion"),
    ("122151375549072582_28655859584020446", "122151375549072582", "2026-08-23T18:26:45+0000", "el humano es su amigo imaginario", "Pendiente_Respuesta", "Giro humorístico sobre creador y criatura", "Ese giro convierte al humano en creador, criatura y amigo imaginario a la vez. 🤯✨", "Reacciona a la inversión del concepto de amigo imaginario con humor cósmico.", "Baja", "No_Accion"),
    ("122151375549072582_1701646280916056", "122151375549072582", "2026-08-23T18:01:13+0000", "L Roberto LJ jjaaj dios no existe,solo te hacen creér que existe", "Pendiente_Respuesta", "Postura escéptica sobre la creencia", "El hilo ya entró en territorio de preguntas incómodas: creer, dudar y seguir preguntando. 🤔✨", "Se reconoce la postura sin debatir ni afirmar una conclusión teológica.", "Media", "No_Accion"),
    ("122151375549072582_1620066063117283", "122151375549072582", "2026-08-23T18:02:19+0000", "El ser humano... Inventamos cada cosa para no hacernos cargos de nuestros errores y para justificar todo lo que no entendemos", "Pendiente_Respuesta", "Reflexión crítica sobre las explicaciones humanas", "Esa lectura toca una fibra incómoda: a veces creamos respuestas para convivir con lo que no entendemos. 🤔✨", "La respuesta acompaña la reflexión sin convertir una generalización en hecho universal.", "Media", "No_Accion"),
    ("122151375549072582_1694912638287381", "122151375549072582", "2026-08-23T18:30:07+0000", "Eres una construcción racional de nuestras dudas ascedidas por el vacío de la incomprensión humana y la soberbia de querer entender", "Pendiente_Respuesta", "Definición filosófica del concepto divino", "Eso suena a una definición filosófica del meme: dudas, vacío y ganas de entender en una sola frase. 🤔✨", "Se reacciona a la construcción conceptual del comentario, sin validar su tesis.", "Media", "No_Accion"),
    ("122151375549072582_826905977110802", "122151375549072582", "2026-08-23T18:49:13+0000", "😊🤭😂🤣", "Pendiente_Respuesta", "Reacción emocional al debate", "La pregunta dejó al hilo entre la risa y la crisis existencial. 😂🤔", "La combinación de emojis indica que el usuario recibió el meme en clave humorística y reflexiva.", "Baja", "No_Accion"),
    ("122151375549072582_1068603845556930", "122151375549072582", "2026-08-23T18:23:11+0000", "Apocalipsis 22:13 yo soy el alfa y la omega, el principio y el fin, el primero y el ultimo", "Pendiente_Respuesta", "Cita bíblica sobre principio y fin", "Alfa y Omega: una respuesta que vuelve a poner la conversación en escala cósmica. 🤔✨", "Se reconoce la referencia aportada por el usuario sin entrar a interpretar o debatir la doctrina.", "Media", "No_Accion"),
    ("122151375549072582_2076221029645579", "122151375549072582", "2026-08-23T18:54:12+0000", "Héctor Ser", "No_Requiere_Respuesta", "Nombre aislado sin contexto", "No responder", "Solo aparece un nombre; no hay intención clara.", "Baja", "No_Accion"),
    ("122151375549072582_2044378132857128", "122151375549072582", "2026-08-23T17:33:04+0000", "Gabriel Quintero", "No_Requiere_Respuesta", "Nombre aislado sin contexto", "No responder", "Solo aparece un nombre; no hay intención clara.", "Baja", "No_Accion"),
    ("122151375549072582_2089754968329324", "122151375549072582", "2026-08-23T18:41:52+0000", "Hit✨️💨", "No_Requiere_Respuesta", "Interacción ambigua sin contexto", "No responder", "No permite inferir si es una reacción, una mención o una solicitud.", "Baja", "No_Accion"),
    ("122151375549072582_1782291889888079", "122151375549072582", "2026-08-23T18:35:02+0000", "Será que no es persona será aire yo creo DIOS ES AIRE NOMAS", "Pendiente_Respuesta", "Hipótesis humorística sobre una figura de aire", "La teoría del aire acaba de entrar oficialmente al expediente cósmico. 🌬️🤔", "La propuesta sigue el humor y la imagen sin corregir ni confirmar la hipótesis.", "Media", "No_Accion"),
    ("122151375549072582_2020808335220703", "122151375549072582", "2026-08-23T18:02:40+0000", "Esa pregunta quebró absolutamente toda creencia religiosa en mi mente 🤣", "Pendiente_Respuesta", "Reacción humorística de crisis existencial", "Jajaja, entonces el meme sí venía con daños colaterales filosóficos. 🤣🤔", "El usuario expresa impacto humorístico; la respuesta reconoce el tono sin hacer afirmaciones sobre religión.", "Baja", "No_Accion"),
    ("122151375549072582_1004388505976156", "122151375549072582", "2026-08-23T18:52:18+0000", "🤔🤨🫣😎 La  élite lo creo invento y los esquizofrenicos adoctrinados e ignorantes y sumisos se la tragaron tienen muchos amigos imaginarios 🐑💩🤡💀", "No_Requiere_Respuesta", "Insultos y lenguaje estigmatizante dirigidos a otras personas", "No responder", "Contiene ataques personales y lenguaje estigmatizante; requiere revisión manual de moderación según las reglas de la Página, no una respuesta pública.", "Media", "Revisar"),
    ("122151375549072582_942638681466045", "122151375549072582", "2026-08-23T18:47:59+0000", "Dios existe por qué el pendejo ser humano lo creó. Por la puta necesidad de creer en algo superior.", "No_Requiere_Respuesta", "Postura provocadora con lenguaje vulgar", "No responder", "El contenido es sobre el tema, pero el tono vulgar y confrontativo no ofrece una apertura clara para respuesta de marca.", "Baja", "Revisar"),
    ("122151375549072582_1110818364949332", "122151375549072582", "2026-08-23T18:30:19+0000", "El es el TODO ha existido siempre pynch3$ nalgas miadas con ese meme te caerá la vrgx", "No_Requiere_Respuesta", "Insulto y amenaza vulgar en un hilo público", "No responder", "Contiene insultos y una amenaza vulgar; no responder y dejar para revisión manual de moderación.", "Media", "Revisar"),
]

# id, parent_id, post_id, created, message, state, signal, suggestion, insight, priority, moderation
REPLY_SPECS = [
    ("122151376011072582_2488170114997851", "122151376011072582_1350675507083697", "122151376011072582", "2026-08-23T18:07:54+0000", "Universe Sent Me solo dale la oportunidad y escuchala lo entenderas cuando la escuches", "Pendiente_Respuesta", "Invitación directa a escuchar la canción recomendada", "La vamos a escuchar con atención; ya quedó anotada en la lista cósmica. 🎶✨", "La usuaria retoma la conversación después de la respuesta de la Página y formula una invitación concreta.", "Media", "No_Accion"),
    ("122151375549072582_1817089682764579", "122151375549072582_1755338779425523", "122151375549072582", "2026-08-23T17:25:20+0000", "L Roberto LJ Hay que tener en cuenta que nuestro Dios es un sincretismo entre amon, zeus y el dios abrahamico Y pues amon-ra se creo a si mismo, el tmbn es la nada misma, pero cuando la nada adquirio consciencia se creo todo (Te invito a investigar por tu cuenta, pues estoy parafraseando)", "Pendiente_Respuesta", "Aporte teológico y cosmogónico dentro del hilo", "Sí, ahí ya entramos en historia de las religiones y cosmogonías. Gracias por aportar la referencia; la pregunta se puso aún más grande. 🤔✨", "Responder sin confirmar la tesis histórica o teológica; reconocer que el usuario amplió el marco de la conversación.", "Media", "No_Accion"),
    ("122151375549072582_2445223119302734", "122151375549072582_4590382837949041", "122151375549072582", "2026-08-23T18:45:36+0000", "Daniel Ricardo Mesa seas mamón, no metas la física en lo teológico.", "No_Requiere_Respuesta", "Insulto dirigido a otra persona", "No responder", "Es una disputa entre usuarios con lenguaje insultante; no entrar al intercambio.", "Media", "Revisar"),
    ("122151375549072582_1334349785149802", "122151375549072582_4590382837949041", "122151375549072582", "2026-08-23T18:55:20+0000", "Daniel Ricardo Mesa hahaha esa es la masa idiota", "No_Requiere_Respuesta", "Insulto dirigido a otra persona", "No responder", "Es una disputa entre usuarios con lenguaje insultante; no entrar al intercambio.", "Media", "Revisar"),
    ("122151375549072582_1558962762367236", "122151375549072582_901941632636512", "122151375549072582", "2026-08-23T18:51:34+0000", "Filos Zen y tiene toda la razón", "No_Requiere_Respuesta", "Acuerdo breve entre usuarios", "No responder", "La réplica expresa acuerdo con otra persona y no solicita intervención de la Página.", "Baja", "No_Accion"),
    ("122151375549072582_999401489813305", "122151375549072582_37855550027424046", "122151375549072582", "2026-08-23T17:58:18+0000", "Jose Estrella si le sabes no le llamas papá dios le llamas yaldabaoth WOW!!", "No_Requiere_Respuesta", "Provocación entre usuarios sobre una creencia", "No responder", "La réplica intensifica el debate entre usuarios y no requiere intervención de la Página.", "Baja", "Revisar"),
    ("122151375549072582_3607944949355092", "122151375549072582_1036994699332009", "122151375549072582", "2026-08-23T18:33:35+0000", "White Benny pero no ay hombres lo que abunda es puro gays", "No_Requiere_Respuesta", "Lenguaje homofóbico dirigido a terceros", "No responder", "Contiene lenguaje despectivo hacia un grupo protegido; requiere revisión manual de moderación y no respuesta pública.", "Media", "Revisar"),
    ("122151375549072582_1031688816340908", "122151375549072582_1495068889305489", "122151375549072582", "2026-08-23T19:00:48+0000", "Zeus IR de la que dejó verde al Paul", "No_Requiere_Respuesta", "Réplica ambigua sin contexto suficiente", "No responder", "No se entiende con claridad la intención ni el referente; no asumir significado.", "Baja", "No_Accion"),
]


def build_row(spec, nested=False):
    if nested:
        comment_id, parent_id, post_id, created, message, state, signal, suggestion, insight, priority, moderation = spec
        source = f"Meta Graph API v26.0 — réplica nueva posterior a {CUTOFF}"
        kind = "Réplica_Anidada"
    else:
        comment_id, post_id, created, message, state, signal, suggestion, insight, priority, moderation = spec
        parent_id = ""
        source = f"Meta Graph API v26.0 — comentario raíz posterior a {CUTOFF}"
        kind = "Contextual_Sustantivo" if state == "Pendiente_Respuesta" else "No_Accion"
    return {
        "Comentario_ID": comment_id,
        "Post_ID": post_id,
        "CNT_ID": parent_id,
        "Fecha_Comentario": created,
        "Plataforma": "Facebook",
        "Tipo": kind,
        "Señal": signal,
        "Respuesta_Estado": state,
        "Respuesta_Sugerida": suggestion,
        "Aprobacion_Estado": "Pendiente_Fernando" if state == "Pendiente_Respuesta" else "No_Aplica",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": insight,
        "Accion_Calendario": "Ninguna",
        "Prioridad": priority,
        "Moderacion_Estado": moderation,
        "Asset_Respuesta_ID": "",
        "Privacidad": "Anonimizado",
        "Fuente": source,
        "Ultima_Sincronizacion": SYNCED_AT,
    }

rows_to_add = [build_row(spec) for spec in ROOT_SPECS] + [build_row(spec, nested=True) for spec in REPLY_SPECS]
with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
    reader = csv.DictReader(source)
    existing_ids = {row["Comentario_ID"] for row in reader}
new_rows = [row for row in rows_to_add if row["Comentario_ID"] not in existing_ids]
if new_rows:
    with CSV_PATH.open("a", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS, lineterminator="\n")
        writer.writerows(new_rows)

payload = {
    "reviewed_at": SYNCED_AT,
    "cutoff": CUTOFF,
    "source": "Meta Graph API v26.0",
    "read_only_review": True,
    "root_comment_count": len(ROOT_SPECS),
    "new_user_reply_count": len(REPLY_SPECS),
    "new_record_count": len(new_rows),
    "respondable_count": sum(row["Respuesta_Estado"] == "Pendiente_Respuesta" for row in new_rows),
    "no_action_count": sum(row["Respuesta_Estado"] == "No_Requiere_Respuesta" for row in new_rows),
    "moderation_review_count": sum(row["Moderacion_Estado"] == "Revisar" for row in new_rows),
    "records": new_rows,
}
JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"NEW_RECORDS={len(new_rows)}")
print(f"RESPONDABLE={payload['respondable_count']}")
print(f"NO_ACTION={payload['no_action_count']}")
print(f"MODERATION_REVIEW={payload['moderation_review_count']}")
