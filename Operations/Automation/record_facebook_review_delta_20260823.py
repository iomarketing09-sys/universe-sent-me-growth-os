#!/usr/bin/env python3
"""Record the latest read-only Facebook comment review delta."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
JSON_PATH = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_02.json"
SYNCED_AT = "2026-08-23T16:56:42+0000"
CUTOFF = "2026-08-23T02:36:53+0000"

FIELDS = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo",
    "Señal", "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado",
    "Respuesta_Fecha", "Respuesta_Meta_ID", "Insight_Anonimo", "Accion_Calendario",
    "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID", "Privacidad", "Fuente",
    "Ultima_Sincronizacion",
]

POST_ID = "122151376011072582"
POST_ID_HUMOR = "122151376083072582"
records = [
    {
        "Comentario_ID": "122151376083072582_1078572578055585",
        "Post_ID": POST_ID_HUMOR,
        "Fecha_Comentario": "2026-08-23T16:36:02+0000",
        "Tipo": "Contextual_Sustantivo",
        "Señal": "Continuación breve del remate con ‘Amén hermanas’",
        "Respuesta_Estado": "Pendiente_Respuesta",
        "Respuesta_Sugerida": "Amén, hermanas: el acta del modo travesura ya quedó aprobada. 🤓😂",
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Insight_Anonimo": "La comunidad prolonga el remate del hilo; conviene responder con complicidad sin volver explícito el contenido íntimo.",
        "Prioridad": "Baja",
        "Fuente": f"Meta Graph API v26 — corte posterior a {CUTOFF}",
    },
    {
        "Comentario_ID": "122151376011072582_1374323618238603",
        "Post_ID": POST_ID,
        "Fecha_Comentario": "2026-08-23T15:45:50+0000",
        "Tipo": "Contextual_Sustantivo",
        "Señal": "Recomendación de ‘Mis manos en tu cintura’ de Nino Bravo",
        "Respuesta_Estado": "Pendiente_Respuesta",
        "Respuesta_Sugerida": "Mis manos en tu cintura: Nino Bravo poniendo el romance en modo clásico. 🎶✨",
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Insight_Anonimo": "La canción y el artista están identificados; la respuesta puede jugar con el tono romántico clásico sin elogio intercambiable.",
        "Prioridad": "Media",
        "Fuente": f"Meta Graph API v26 — corte posterior a {CUTOFF}",
    },
    {
        "Comentario_ID": "122151376011072582_1474344638049134",
        "Post_ID": POST_ID,
        "Fecha_Comentario": "2026-08-23T16:45:27+0000",
        "Tipo": "Contextual_Sustantivo",
        "Señal": "Recomendación de ‘Tonight’ de The Smashing Pumpkins",
        "Respuesta_Estado": "Pendiente_Respuesta",
        "Respuesta_Sugerida": "Tonight de The Smashing Pumpkins: nostalgia alternativa activada en tres palabras. 🧡💛🖤🎶",
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Insight_Anonimo": "El comentario identifica canción y artista; la propuesta recoge la energía nostálgica y alternativa de la elección.",
        "Prioridad": "Media",
        "Fuente": f"Meta Graph API v26 — corte posterior a {CUTOFF}",
    },
    {
        "Comentario_ID": "122151376011072582_1807143836955837",
        "Post_ID": POST_ID,
        "Fecha_Comentario": "2026-08-23T16:44:44+0000",
        "Tipo": "Contextual_Sustantivo",
        "Señal": "Cita religiosa extensa con enlace externo y sin solicitud clara",
        "Respuesta_Estado": "No_Requiere_Respuesta",
        "Respuesta_Sugerida": "No responder",
        "Aprobacion_Estado": "No_Aplica",
        "Insight_Anonimo": "Texto religioso extenso con enlace externo, sin pregunta ni vínculo claro con la publicación; no responder sin asumir intención. No se marca como spam ni se modera automáticamente.",
        "Prioridad": "Baja",
        "Fuente": f"Meta Graph API v26 — corte posterior a {CUTOFF}",
    },
    {
        "Comentario_ID": "122151376011072582_2991082287899276",
        "Post_ID": POST_ID,
        "Fecha_Comentario": "2026-08-23T16:28:17+0000",
        "Tipo": "Contextual_Sustantivo",
        "Señal": "Recomendación de ‘Stirb nicht vor mir’ de Rammstein",
        "Respuesta_Estado": "Pendiente_Respuesta",
        "Respuesta_Sugerida": "Stirb nicht vor mir: Rammstein llevando el drama romántico hasta el borde del abismo. 🖤🎶",
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Insight_Anonimo": "El título y el artista permiten una respuesta específica sobre el dramatismo de la canción, sin traducir ni sobreexplicar.",
        "Prioridad": "Media",
        "Fuente": f"Meta Graph API v26 — corte posterior a {CUTOFF}",
    },
    {
        "Comentario_ID": "122151376011072582_2308975296571861",
        "Post_ID": POST_ID,
        "Fecha_Comentario": "2026-08-23T15:57:09+0000",
        "Tipo": "Contextual_Sustantivo",
        "Señal": "Recomendación de ‘Birdie’ de León Larregui",
        "Respuesta_Estado": "Pendiente_Respuesta",
        "Respuesta_Sugerida": "Birdie de León Larregui: ternura y viaje cósmico en la misma canción. ✨🎶",
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Insight_Anonimo": "La canción y el artista están identificados; la respuesta conecta con una sensación de ternura y viaje sin usar una fórmula genérica.",
        "Prioridad": "Media",
        "Fuente": f"Meta Graph API v26 — corte posterior a {CUTOFF}",
    },
    {
        "Comentario_ID": "122151375549072582_1089305796872950",
        "Post_ID": "122151375549072582",
        "Fecha_Comentario": "2026-08-23T16:30:08+0000",
        "Tipo": "Contextual_Sustantivo",
        "Señal": "Réplica humorística que transforma BigBang en ‘bigbong’",
        "Respuesta_Estado": "Pendiente_Respuesta",
        "Respuesta_Sugerida": "Jajaja, el universo también tiene problemas de dicción. 🤣💥",
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Insight_Anonimo": "La réplica continúa el juego verbal del hilo; debe tratarse como una unidad nueva aunque el comentario raíz ya tenga respuesta de la Página.",
        "Prioridad": "Baja",
        "Fuente": f"Meta Graph API v26 — réplica de usuario posterior a {CUTOFF}",
    },
]

with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as source:
    reader = csv.DictReader(source)
    existing_ids = {row["Comentario_ID"] for row in reader}

new_records = []
for record in records:
    row = {field: "" for field in FIELDS}
    row.update(record)
    row["Plataforma"] = "Facebook"
    row["CNT_ID"] = ""
    row["Respuesta_Fecha"] = ""
    row["Respuesta_Meta_ID"] = ""
    row["Accion_Calendario"] = "Ninguna"
    row["Moderacion_Estado"] = "No_Accion"
    row["Asset_Respuesta_ID"] = ""
    row["Privacidad"] = "Anonimizado"
    row["Ultima_Sincronizacion"] = SYNCED_AT
    if row["Comentario_ID"] not in existing_ids:
        new_records.append(row)

if new_records:
    with CSV_PATH.open("a", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS, lineterminator="\n")
        writer.writerows(new_records)

payload = {
    "reviewed_at": SYNCED_AT,
    "cutoff": CUTOFF,
    "source": "Meta Graph API v26.0",
    "read_only": True,
    "new_records": new_records,
    "new_record_count": len(new_records),
    "respondable_count": sum(r["Respuesta_Estado"] == "Pendiente_Respuesta" for r in new_records),
    "no_action_count": sum(r["Respuesta_Estado"] == "No_Requiere_Respuesta" for r in new_records),
}
JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"NEW_RECORDS={len(new_records)}")
print(f"RESPONDABLE={payload['respondable_count']}")
print(f"NO_ACTION={payload['no_action_count']}")
