"""Record and propose responses for the latest Facebook comment delta.

This script appends only new comment IDs. It never publishes to Facebook.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_06.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Record_Delta_06.json"
FIELDS = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo",
    "Señal", "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado",
    "Respuesta_Fecha", "Respuesta_Meta_ID", "Insight_Anonimo", "Accion_Calendario",
    "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID", "Privacidad", "Fuente",
    "Ultima_Sincronizacion",
]

SUGGESTIONS = {
    "122151376539072582_1033595316219697": "Maeve no miente… solo deja que cada quien saque sus conclusiones 😹",
    "122151376083072582_3309129972605548": "Jajaja, aquí cada quien interpreta a su manera 😹🙈",
}

NO_ACTION = {
    "122155182621072582_1634878035019592": "Comentario vacío; no requiere respuesta.",
}

review = json.loads(INPUT.read_text(encoding="utf-8"))
reviewed_at = review.get("reviewed_at", "")
cutoff = review.get("cutoff", "")
source = f"Meta Graph API v26.0 — revisión posterior a {cutoff}"

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    existing_ids = {row.get("Comentario_ID", "") for row in reader}
    fieldnames = reader.fieldnames or FIELDS

new_records = []
for comment in review.get("comments", []):
    comment_id = comment.get("comment_id")
    if not comment_id or comment_id in existing_ids:
        continue
    record = {field: "" for field in fieldnames}
    record.update({
        "Comentario_ID": comment_id,
        "Post_ID": comment.get("post_id", ""),
        "Fecha_Comentario": comment.get("comment_created_time", ""),
        "Plataforma": "Facebook",
        "Tipo": comment.get("comment_type", ""),
        "Señal": "Propuesta_Respuesta" if comment_id in SUGGESTIONS else "Sin_Contenido",
        "Respuesta_Estado": "Pendiente_Respuesta" if comment_id in SUGGESTIONS else "No_Requiere_Respuesta",
        "Respuesta_Sugerida": SUGGESTIONS.get(comment_id, ""),
        "Aprobacion_Estado": "Pendiente_Fernando" if comment_id in SUGGESTIONS else "No_Aplica",
        "Insight_Anonimo": NO_ACTION.get(comment_id, "Respuesta breve contextual propuesta; validar antes de publicar."),
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media" if comment_id in SUGGESTIONS else "Baja",
        "Moderacion_Estado": "No_Accion",
        "Privacidad": "Anonimizado",
        "Fuente": source,
        "Ultima_Sincronizacion": reviewed_at,
    })
    new_records.append(record)

if new_records:
    with LEDGER.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n").writerows(new_records)

payload = {
    "recorded_at": reviewed_at,
    "cutoff": cutoff,
    "source": "Meta Graph API v26.0",
    "read_only_review": True,
    "input_count": len(review.get("comments", [])),
    "new_records_appended": len(new_records),
    "respondable_proposals": len([r for r in new_records if r["Respuesta_Estado"] == "Pendiente_Respuesta"]),
    "no_action_records": len([r for r in new_records if r["Respuesta_Estado"] == "No_Requiere_Respuesta"]),
    "proposals": [{"comment_id": r["Comentario_ID"], "post_id": r["Post_ID"], "suggested_reply": r["Respuesta_Sugerida"]} for r in new_records if r["Respuesta_Sugerida"]],
    "no_publication_performed": True,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("input_count", "new_records_appended", "respondable_proposals", "no_action_records")}, ensure_ascii=False))
