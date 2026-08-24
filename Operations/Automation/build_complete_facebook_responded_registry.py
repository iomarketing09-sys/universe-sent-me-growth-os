"""Build a consolidated registry of every Respondido Facebook ledger row."""

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Operations/Research"
LEDGER = RESEARCH / "2026-08-15_Community_Engagement_Log.csv"
VERIFICATION = RESEARCH / "2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json"
REPAIR = RESEARCH / "2026-08-24_Facebook_Complete_Responded_Registration_Repair.json"
OUT_JSON = RESEARCH / "2026-08-24_Facebook_Complete_Responded_Registry.json"
OUT_MD = RESEARCH / "2026-08-24_Facebook_Complete_Responded_Registry.md"


def raw_items(payload):
    return payload.get("records") or payload.get("results") or []


def normalize_evidence(item, path):
    verification = item.get("verification") or {}
    payload = verification.get("payload") or {}
    checks = verification.get("checks") or {}
    reply_id = item.get("reply_id") or (item.get("post_response") or {}).get("id")
    comment_id = item.get("comment_id") or item.get("target_comment_id") or item.get("parent_comment_id")
    historical_verified = bool(item.get("verified") is True or item.get("status") in {"Respondido", "published_verified"} or (checks and all(checks.values())))
    return {
        "source_file": path.name,
        "comment_id": comment_id,
        "reply_id": reply_id,
        "historical_status": item.get("status"),
        "historical_verified": historical_verified,
        "historical_message": item.get("message") or item.get("response_message") or payload.get("message"),
        "historical_created_time": item.get("reply_created_time") or item.get("created_time") or payload.get("created_time") or item.get("run_at_utc"),
    }


# Include both the normalized record files and the initial raw publication
# evidence. Deduplication is by reply ID; differing target IDs are retained as
# aliases in the source list rather than silently discarded.
evidence = defaultdict(list)
paths = sorted(RESEARCH.glob("2026-08-24_Facebook_Comment_Publication_Record_Batch_*.json"))
paths += sorted(RESEARCH.glob("2026-08-23_Facebook_Comment_Publication_Batch*.json"))
for path in paths:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for item in raw_items(payload):
        normalized = normalize_evidence(item, path)
        if normalized["reply_id"]:
            evidence[normalized["reply_id"]].append(normalized)

with LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
    ledger_rows = list(csv.DictReader(handle))
responded_rows = [row for row in ledger_rows if row.get("Respuesta_Estado") == "Respondido"]
ledger_by_id = {row.get("Comentario_ID"): row for row in ledger_rows}

verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
verification_by_reply = {row.get("reply_id"): row for row in verification.get("results", []) if row.get("reply_id")}
repair = json.loads(REPAIR.read_text(encoding="utf-8"))
correction_by_reply = {}
for item in repair.get("correction_details", []):
    if item.get("reply_id"):
        correction_by_reply.setdefault(item["reply_id"], []).append(item)

records = []
for row in responded_rows:
    reply_id = row.get("Respuesta_Meta_ID")
    current = verification_by_reply.get(reply_id, {})
    historical = evidence.get(reply_id, [])
    required_fields_complete = all(row.get(field) for field in ("Comentario_ID", "Post_ID", "Respuesta_Sugerida", "Aprobacion_Estado", "Respuesta_Fecha", "Respuesta_Meta_ID", "Fuente", "Privacidad"))
    if current.get("verified") is True:
        basis = "current_meta_verified"
    elif historical and any(item.get("historical_verified") for item in historical):
        basis = "historical_evidence_verified_current_object_inaccessible"
    elif current.get("api_ok") is False:
        basis = "ledger_historical_trace_current_object_inaccessible"
    else:
        basis = "ledger_trace_review"
    records.append({
        "comment_id": row.get("Comentario_ID"),
        "post_id": row.get("Post_ID"),
        "comment_date": row.get("Fecha_Comentario"),
        "comment_type": row.get("Tipo"),
        "reply_id": reply_id,
        "reply_message": row.get("Respuesta_Sugerida"),
        "reply_date": row.get("Respuesta_Fecha"),
        "response_status": row.get("Respuesta_Estado"),
        "approval_status": row.get("Aprobacion_Estado"),
        "privacy": row.get("Privacidad"),
        "source": row.get("Fuente"),
        "registration_complete": required_fields_complete,
        "current_meta_api_ok": current.get("api_ok"),
        "current_meta_verified": current.get("verified"),
        "current_meta_status_code": current.get("status_code"),
        "current_meta_error": current.get("error"),
        "current_parent_semantics": current.get("parent_semantics"),
        "current_api_created_time": current.get("api_created_time"),
        "historical_evidence_present": bool(historical),
        "historical_evidence_verified": any(item.get("historical_verified") for item in historical),
        "historical_evidence_files": sorted({item["source_file"] for item in historical}),
        "historical_evidence_count": len(historical),
        "recording_basis": basis,
        "corrections_applied": correction_by_reply.get(reply_id, []),
    })

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
summary = {
    "ledger_rows_total": len(ledger_rows),
    "respondido_rows": len(records),
    "registration_complete_rows": sum(1 for item in records if item["registration_complete"]),
    "current_meta_api_ok_rows": sum(1 for item in records if item["current_meta_api_ok"]),
    "current_meta_verified_rows": sum(1 for item in records if item["current_meta_verified"]),
    "currently_inaccessible_rows": sum(1 for item in records if item["current_meta_api_ok"] is False),
    "historical_evidence_present_rows": sum(1 for item in records if item["historical_evidence_present"]),
    "historical_evidence_verified_rows": sum(1 for item in records if item["historical_evidence_verified"]),
    "rows_without_historical_evidence_artifact": sum(1 for item in records if not item["historical_evidence_present"]),
    "corrections_applied_rows": sum(1 for item in records if item["corrections_applied"]),
    "current_parent_semantics_counts": dict(Counter(item.get("current_parent_semantics") or "not_available" for item in records)),
    "recording_basis_counts": dict(Counter(item["recording_basis"] for item in records)),
}

payload = {
    "title": "Facebook — registro consolidado de todos los comentarios respondidos",
    "purpose": "Dejar en un solo artefacto la trazabilidad completa de las 166 filas Respondido del Community Engagement Log: comentario, publicación, respuesta, Meta ID, timestamp, aprobación, evidencia histórica y verificación actual.",
    "status": "Active",
    "created_at": now,
    "updated_at": now,
    "version": "1.0",
    "author": "Manus AI",
    "related_documents": [
        "Operations/Research/2026-08-15_Community_Engagement_Log.csv",
        "Operations/Research/2026-08-15_Community_Engagement_Log.md",
        "Operations/Research/2026-08-24_Facebook_All_Replies_Reconciliation.json",
        "Operations/Research/2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json",
        "Operations/Research/2026-08-24_Facebook_Complete_Responded_Registration_Repair.json",
        "Operations/Research/2026-08-15_Auditoria_Comentarios_Facebook.md",
        "GrowthOS/00_01_Changelog_GrowthOS.md",
    ],
    "organization": "Operations/Research",
    "source": "Community Engagement Log plus historical publication evidence and Meta Graph API v26.0 GET-only verification",
    "summary": summary,
    "records": records,
}
OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# Facebook — registro consolidado de todos los comentarios respondidos",
    "",
    "**Propósito:** consolidar las 166 filas `Respondido` del ledger con todos los campos de registro, evidencia histórica y verificación actual de Meta.",
    "**Estado:** Active",
    "**Fecha de creación:** 2026-08-24",
    f"**Última actualización:** {now}",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-15_Community_Engagement_Log.csv`; `2026-08-24_Facebook_All_Replies_Reconciliation.json`; `2026-08-24_Facebook_All_Responded_Comments_Meta_Verification.json`; `2026-08-24_Facebook_Complete_Responded_Registration_Repair.json`; `2026-08-15_Auditoria_Comentarios_Facebook.md`; `GrowthOS/00_01_Changelog_GrowthOS.md`",
    "**Organización:** Operations/Research",
    "",
    "## Resultado de la conciliación",
    "",
    "El registro contiene todas las filas que el ledger marca como `Respondido`. La integridad administrativa está completa: cada fila conserva comentario, publicación, respuesta, aprobación, Meta reply ID, timestamp, fuente y privacidad anonimizada. La verificación actual de Meta confirma la mayoría de los objetos; tres reply IDs históricos devuelven actualmente HTTP 400 y se conservan como respondidos porque existe trazabilidad histórica en el ledger y, cuando está disponible, evidencia de publicación previa. No se reintentó ninguna respuesta.",
    "",
    "| Indicador | Resultado |",
    "|---|---:|",
    f"| Filas totales del ledger | {summary['ledger_rows_total']} |",
    f"| Comentarios con estado `Respondido` | {summary['respondido_rows']} |",
    f"| Registro administrativo completo | {summary['registration_complete_rows']} |",
    f"| Verificados actualmente por Meta | {summary['current_meta_verified_rows']} |",
    f"| API accesible actualmente | {summary['current_meta_api_ok_rows']} |",
    f"| Objetos actualmente inaccesibles | {summary['currently_inaccessible_rows']} |",
    f"| Con evidencia histórica de lote | {summary['historical_evidence_present_rows']} |",
    f"| Con evidencia histórica marcada verificada | {summary['historical_evidence_verified_rows']} |",
    f"| Filas corregidas en esta conciliación | {summary['corrections_applied_rows']} |",
    "",
    "## Correcciones aplicadas",
    "",
    "Se corrigieron dos textos que contenían notas editoriales en lugar del texto realmente publicado por la Página. También se corrigió un `Comentario_ID` histórico cuyo reply confirmó mediante Meta un parent ID distinto. Las correcciones no generaron publicaciones nuevas.",
    "",
    "| Reply ID | Tipo de corrección | Resultado |",
    "|---|---|---|",
]
for item in repair.get("correction_details", []):
    if item.get("type") == "response_text":
        lines.append(f"| `{item['reply_id']}` | Texto de respuesta | `{item['after']}` |")
    elif item.get("type") == "comment_id":
        lines.append(f"| `{item['reply_id']}` | Comment_ID | `{item['old_comment_id']}` → `{item['new_comment_id']}` |")
lines.extend([
    "",
    "## Excepciones actuales de Meta",
    "",
    "Los siguientes tres replies no pudieron abrirse con el GET directo durante este corte. El ledger los conserva como `Respondido`; no se consideran pendientes de publicación y no se reintentaron para evitar duplicados.",
    "",
    "| Comentario_ID | Respuesta_Meta_ID | Estado actual | Base de conservación |",
    "|---|---|---|---|",
])
for item in records:
    if item["current_meta_api_ok"] is False:
        base = "Evidencia histórica disponible" if item["historical_evidence_present"] else "Trazabilidad histórica del ledger"
        lines.append(f"| `{item['comment_id']}` | `{item['reply_id']}` | HTTP {item.get('current_meta_status_code') or 'n/a'} | {base} |")
lines.extend([
    "",
    "## Distribución de verificación",
    "",
    "| Base de registro | Filas |",
    "|---|---:|",
])
for key, value in sorted(summary["recording_basis_counts"].items()):
    lines.append(f"| `{key}` | {value} |")
lines.extend([
    "",
    "## Fuente de verdad",
    "",
    "El CSV `Operations/Research/2026-08-15_Community_Engagement_Log.csv` permanece como ledger operativo único. Este registro consolidado es la vista auditable de todas sus filas `Respondido`; no sustituye el CSV ni autoriza publicaciones futuras.",
    "",
    "## Referencias",
    "",
    "[1]: https://developers.facebook.com/docs/graph-api/reference/comment/ \"Meta for Developers — Comment reference\"",
    "[2]: https://developers.facebook.com/documentation/pages-api/comments-mentions \"Meta for Developers — Comments and @mentions\"",
])
OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"ledger_rows_total": summary["ledger_rows_total"], "respondido_rows": summary["respondido_rows"], "registration_complete_rows": summary["registration_complete_rows"], "current_meta_verified_rows": summary["current_meta_verified_rows"], "currently_inaccessible_rows": summary["currently_inaccessible_rows"], "historical_evidence_present_rows": summary["historical_evidence_present_rows"], "corrections_applied_rows": summary["corrections_applied_rows"]}, ensure_ascii=False))
