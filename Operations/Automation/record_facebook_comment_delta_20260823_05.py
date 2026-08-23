"""Record a read-only Facebook comment review delta in the community ledger."""

import csv
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_05.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Record_Delta_05.json"
FIELDS = [
    "Comentario_ID", "Post_ID", "CNT_ID", "Fecha_Comentario", "Plataforma", "Tipo",
    "Señal", "Respuesta_Estado", "Respuesta_Sugerida", "Aprobacion_Estado",
    "Respuesta_Fecha", "Respuesta_Meta_ID", "Insight_Anonimo", "Accion_Calendario",
    "Prioridad", "Moderacion_Estado", "Asset_Respuesta_ID", "Privacidad", "Fuente",
    "Ultima_Sincronizacion",
]
WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+")
MODERATION_TERMS = (
    "pene", "verga", "chup", "chupada", "fundillo", "coger", "cogiendo",
    "ching", "sexo", "sexual", "desnudo", "desnuda", "idiota", "puto", "puta",
)


def is_emoji_or_symbol_only(text):
    for char in text:
        if char.isspace():
            continue
        category = unicodedata.category(char)
        if category[0] in {"L", "N"}:
            return False
        if category.startswith("M"):
            continue
        if category in {"Pc", "Pd", "Pe", "Pf", "Pi", "Po", "Ps", "Sc", "Sk", "Sm", "So", "Cf"}:
            continue
        return False
    return bool(text.strip())


def classify(row):
    text = (row.get("comment_message") or "").strip()
    lowered = text.lower()
    words = WORD_RE.findall(text)
    if not text:
        return "Sin_contenido", "No requiere respuesta; comentario vacío.", "Baja", "No_Accion"
    if any(term in lowered for term in MODERATION_TERMS):
        return "Revisión_moderación", "No responder automáticamente; revisar contexto humano.", "Media", "Revisar"
    if is_emoji_or_symbol_only(text):
        return "Emoji_o_símbolo", "Reacción breve; no requiere respuesta.", "Baja", "No_Accion"
    if row.get("comment_type") == "Replica_Anidada" and len(words) <= 5:
        return "Réplica_baja_señal", "Conversación de usuarios o remate breve; no interrumpir por defecto.", "Baja", "No_Accion"
    if len(words) <= 3 and "?" not in text and "¿" not in text:
        return "Respuesta_breve", "Señal de baja fricción; no requiere respuesta por defecto.", "Baja", "No_Accion"
    return "Contextual_sustantivo", "Comentario contextual nuevo; requiere revisión humana antes de responder.", "Media", "No_Accion"


data = json.loads(INPUT.read_text(encoding="utf-8"))
rows = data.get("comments", [])
with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    existing_ids = {row.get("Comentario_ID", "") for row in reader}

synced_at = data.get("reviewed_at") or datetime.now(timezone.utc).isoformat(timespec="seconds")
cutoff = data.get("cutoff", "")
source = f"Meta Graph API v26.0 — revisión posterior a {cutoff}"
new_records = []
category_counts = Counter()
for row in rows:
    comment_id = row.get("comment_id")
    if not comment_id or comment_id in existing_ids:
        continue
    category, insight, priority, moderation_status = classify(row)
    category_counts[category] += 1
    response_status = "Sin_Revisar" if category in {"Contextual_sustantivo", "Revisión_moderación"} else "No_Requiere_Respuesta"
    approval_status = "No_Aplica"
    record = {field: "" for field in FIELDS}
    record.update({
        "Comentario_ID": comment_id,
        "Post_ID": row.get("post_id", ""),
        "Fecha_Comentario": row.get("comment_created_time", ""),
        "Plataforma": "Facebook",
        "Tipo": row.get("comment_type", ""),
        "Señal": category,
        "Respuesta_Estado": response_status,
        "Aprobacion_Estado": approval_status,
        "Insight_Anonimo": insight,
        "Accion_Calendario": "Ninguna",
        "Prioridad": priority,
        "Moderacion_Estado": moderation_status,
        "Privacidad": "Anonimizado",
        "Fuente": source,
        "Ultima_Sincronizacion": synced_at,
    })
    new_records.append(record)

if new_records:
    with LEDGER.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writerows(new_records)

payload = {
    "recorded_at": synced_at,
    "cutoff": cutoff,
    "source": "Meta Graph API v26.0",
    "read_only_review": True,
    "input_count": len(rows),
    "new_records_appended": len(new_records),
    "already_present": len(rows) - len(new_records),
    "category_counts": dict(category_counts),
    "human_review_count": sum(1 for record in new_records if record["Respuesta_Estado"] == "Sin_Revisar"),
    "moderation_review_count": sum(1 for record in new_records if record["Moderacion_Estado"] == "Revisar"),
    "appended_comment_ids": [record["Comentario_ID"] for record in new_records],
    "no_publication_performed": True,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: payload[key] for key in ("input_count", "new_records_appended", "already_present", "category_counts", "respondable_review_count", "moderation_review_count")}, ensure_ascii=False))
