"""Register new read-only Facebook audit findings without drafting or publishing replies."""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DELTA = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Delta_08.json"
LEDGER = ROOT / "Operations/Research/2026-08-15_Community_Engagement_Log.csv"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Comment_Review_Delta_08_Record.json"


def signal_for(row):
    text = (row.get("comment_message") or "").strip()
    if not text:
        return "Vacio"
    if row.get("comment_type") == "Replica_Anidada":
        return "Conversación_Usuario_Usuario"
    if len(text) <= 12:
        return "Baja_señal"
    if any(token in text.lower() for token in ("pendej", "bollo", "ordeñ", "papucho", "frenillo", "pipi", "aprieta", "sexo", "coger", "joder")):
        return "Lenguaje_Sensible"
    return "Conversación_Contextual"


delta = json.loads(DELTA.read_text(encoding="utf-8"))
reviewed_at = delta["reviewed_at"]
with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
by_id = {row.get("Comentario_ID"): row for row in rows}
new_rows = []
skipped_existing = []
for item in delta.get("unanswered", []):
    comment_id = item.get("comment_id")
    if not comment_id:
        continue
    if comment_id in by_id:
        skipped_existing.append(comment_id)
        continue
    comment_type = item.get("comment_type") or "Comentario_Raiz"
    new_row = {
        "Comentario_ID": comment_id,
        "Post_ID": item.get("post_id", ""),
        "CNT_ID": "",
        "Fecha_Comentario": item.get("comment_created_time", ""),
        "Plataforma": "Facebook",
        "Tipo": comment_type,
        "Señal": signal_for(item),
        "Respuesta_Estado": "Sin_Revisar",
        "Respuesta_Sugerida": "",
        "Aprobacion_Estado": "Pendiente_Fernando",
        "Respuesta_Fecha": "",
        "Respuesta_Meta_ID": "",
        "Insight_Anonimo": "Hallazgo nuevo del Delta 08; requiere clasificación editorial antes de proponer respuesta.",
        "Accion_Calendario": "Ninguna",
        "Prioridad": "Media" if comment_type == "Comentario_Raiz" else "Baja",
        "Moderacion_Estado": "Revisar" if signal_for(item) == "Lenguaje_Sensible" else "No_Accion",
        "Asset_Respuesta_ID": "",
        "Privacidad": "Anonimizado",
        "Fuente": "Meta Graph API v26.0 — auditoría Delta 08",
        "Ultima_Sincronizacion": reviewed_at,
    }
    rows.append(new_row)
    by_id[comment_id] = new_row
    new_rows.append(new_row)
with LEDGER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
payload = {
    "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "reviewed_at": reviewed_at,
    "source": "Meta Graph API v26.0",
    "delta_file": str(DELTA.relative_to(ROOT)),
    "new_rows_added": len(new_rows),
    "skipped_existing": len(skipped_existing),
    "comment_ids_added": [row["Comentario_ID"] for row in new_rows],
    "comment_ids_skipped_existing": skipped_existing,
    "publication_performed": False,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False))
