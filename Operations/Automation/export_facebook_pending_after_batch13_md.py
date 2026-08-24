"""Export the two explicitly excluded pending Facebook items after Batch 13."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch13.json"
OUT = ROOT / "Operations/Research/2026-08-24_Facebook_Pending_Queue_After_Batch13.md"

queue = json.loads(QUEUE.read_text(encoding="utf-8"))
rows = queue.get("pending", [])
if len(rows) != 2:
    raise SystemExit(f"EXPECTED_2_EXCLUDED_PENDING: {len(rows)}")

lines = [
    "# Cola pendiente de Facebook después del Batch 13",
    "",
    "**Propósito:** registrar los dos comentarios que permanecen sin respuesta por decisión editorial de Fernando.",
    "**Estado:** Active",
    "**Fecha de creación:** 2026-08-24",
    "**Última actualización:** 2026-08-24",
    "**Versión:** 1.0",
    "**Autor:** Manus AI",
    "**Documentos relacionados:** `2026-08-24_Facebook_Comment_Publication_Batch_13.json`; `2026-08-24_Facebook_Comment_Publication_Record_Batch_13.json`; `2026-08-24_Facebook_Pending_Queue_After_Batch13.json`; `2026-08-15_Community_Engagement_Log.csv`",
    "**Organización:** Operations/Research",
    "",
    "Después del Batch 13 quedan **2 registros pendientes**, ambos excluidos explícitamente de publicación:",
    "",
    "| Caso | Motivo | Estado |",
    "|---|---|---|",
    "| Réplica de L Roberto en el hilo filosófico | Fernando indicó no contestarla por ser una réplica de usuario a usuario. | Excluida — no responder |",
    "| Comentario musical inaccesible sin texto recuperable | Meta no carga el objeto; no se fuerza una publicación sobre un comentario que no puede verificarse. | Bloqueada por API — no responder |",
    "",
    "Las otras diez respuestas autorizadas del Batch 13 fueron publicadas y verificadas. No queda ninguna otra respuesta aprobada pendiente en esta cola.",
]
OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
print(json.dumps({"remaining_pending": len(rows), "excluded": 2}, ensure_ascii=False))
