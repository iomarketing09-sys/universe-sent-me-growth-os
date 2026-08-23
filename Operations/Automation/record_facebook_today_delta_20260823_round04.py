#!/usr/bin/env python3
"""Record new same-day Facebook comments found after the latest review."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
JSON_PATH = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_04.json"
SYNCED_AT = "2026-08-23T19:33:07+0000"
CUTOFF = "2026-08-23T19:09:24+0000"
FIELDS = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo",
    "Señal", "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado",
    "Respuesta_Fecha", "Respuesta_Meta_ID", "Insight_Anonimo", "Accion_Calendario",
    "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID", "Privacidad", "Fuente",
    "Ultima_Sincronizacion",
]

SPECS = [
    ("122151375549072582_2130811011171538", "2026-08-23T19:22:01+0000", "Nosotros", "Respuesta breve sobre el origen", "El ‘nosotros’ acaba de entrar como candidato oficial. 🤔✨", "La respuesta de una palabra continúa directamente la pregunta de la imagen y deja abierta la paradoja creador-criatura.", "Baja"),
    ("122151375549072582_2053549225533216", "2026-08-23T19:19:50+0000", "😂🤣🤣🤣🤣🤣🤣🤣", "Reacción humorística al debate", "La pregunta provocó una risa nerviosa colectiva. 😂🤔", "Es una reacción clara al hilo filosófico; se puede responder sin agregar una tesis.", "Baja"),
    ("122151375549072582_1394530616118799", "2026-08-23T19:32:34+0000", "Esa es una muy buena pregunta 🤔", "Reconocimiento de la pregunta central", "Y todavía no aparece el departamento de respuestas cósmicas. 🤔😂", "El usuario valida el planteamiento del meme; la propuesta mantiene el tono cósmico y abierto.", "Baja"),
    ("122151375549072582_1220311087840453", "2026-08-23T19:32:40+0000", "A ti “la histeria colectiva”", "Remate sobre el origen de las creencias", "La histeria colectiva: creadora oficial de varias teorías y unos cuantos dolores de cabeza. 😂🤔", "La respuesta retoma literalmente el giro del comentario y evita discutir una postura religiosa como hecho.", "Baja"),
]

rows=[]
for comment_id, created, message, signal, suggestion, insight, priority in SPECS:
    rows.append({
        "Comentario_ID": comment_id,
        "Post_ID": "122151375549072582",
        "CNT_ID": "",
        "Fecha_Comentario": created,
        "Plataforma": "Facebook",
        "Tipo": "Contextual_Sustantivo",
        "Señal": signal,
        "Respuesta_Estado": "Pendiente_Respuesta",
        "Respuesta_Sugerida": suggestion,
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": insight,
        "Accion_Calendario": "Ninguna",
        "Prioridad": priority,
        "Moderacion_Estado": "No_Accion",
        "Asset_Respuesta_ID": "",
        "Privacidad": "Anonimizado",
        "Fuente": f"Meta Graph API v26.0 — comentario de hoy posterior a {CUTOFF}",
        "Ultima_Sincronizacion": SYNCED_AT,
    })

with CSV_PATH.open("r",encoding="utf-8-sig",newline="") as source:
    reader=csv.DictReader(source)
    existing={row["Comentario_ID"] for row in reader}
new_rows=[row for row in rows if row["Comentario_ID"] not in existing]
if new_rows:
    with CSV_PATH.open("a",encoding="utf-8",newline="") as target:
        csv.DictWriter(target,fieldnames=FIELDS,lineterminator="\n").writerows(new_rows)

payload={
    "reviewed_at":SYNCED_AT,
    "cutoff":CUTOFF,
    "source":"Meta Graph API v26.0",
    "read_only_review":True,
    "new_today_count":len(new_rows),
    "respondable_count":len(new_rows),
    "records":new_rows,
}
JSON_PATH.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"NEW_TODAY_RECORDS={len(new_rows)}")
print(f"RESPONDABLE={len(new_rows)}")
