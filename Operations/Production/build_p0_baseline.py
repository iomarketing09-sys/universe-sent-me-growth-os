#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd

calendar_path = Path("Operations/Research/2026-08-16_Calendario_Operativo_17_30_Agosto.csv")
meta_path = Path("Operations/Research/2026-08-17_Verificacion_Meta_Ola_Activa.json")
out_path = Path("Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv")

calendar = pd.read_csv(calendar_path, dtype=str).fillna("")
calendar = calendar[calendar["Fecha"] == "2026-08-17"].copy()
meta = json.loads(meta_path.read_text(encoding="utf-8"))
posts = meta["posts"]
by_local_slot = {}
for p in posts:
    created = datetime.strptime(p["created_time"], "%Y-%m-%dT%H:%M:%S%z")
    local = created.astimezone(ZoneInfo("America/Matamoros"))
    by_local_slot[(local.strftime("%Y-%m-%d"), local.strftime("%H:%M"))] = p
rows = []
for _, row in calendar.iterrows():
    post = by_local_slot.get((row["Fecha"], row["Hora"]))
    if not post:
        continue
    created = datetime.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S%z")
    rows.append({
        "experiment_id": row["Experiment_ID"],
        "hypothesis_ids": "H1;H2;H3;H4",
        "publication_id": f"PUB-FB-2026-08-17-{row['Hora'].replace(':','')}",
        "CNT": "",
        "Asset_Ref": row["Archivo"].split(" - ")[0].strip(),
        "asset_filename": row["Archivo"],
        "platform": "Facebook",
        "format": "Image",
        "content_type": row["Tipo_Contenido"],
        "is_new_or_reuse": "Nuevo" if row["Tipo_Contenido"] == "Nueva" else "Reuse",
        "slot_local": row["Hora"],
        "scheduled_date_local": row["Fecha"],
        "published_at_utc": created.astimezone(timezone.utc).isoformat(),
        "published_at_local": created.astimezone(ZoneInfo("America/Matamoros")).isoformat(),
        "meta_post_id": post["id"],
        "publication_status": "Publicado_confirmado_Meta",
        "baseline_captured_at": "",
        "snapshot_24h_at": "",
        "snapshot_72h_at": "",
        "window_status": "Pendiente_ventana",
        "reactions_24h": "",
        "comments_root_24h": "",
        "shares_24h": "",
        "interactions_24h": "",
        "reactions_72h": "",
        "comments_root_72h": "",
        "shares_72h": "",
        "interactions_72h": "",
        "source": "2026-08-17_Verificacion_Meta_Ola_Activa.json",
        "extraction_timestamp_utc": meta["extracted_at_utc"],
        "comparability": "Elegible_para_snapshot; sin métricas aún",
        "notes": "Cruce por fecha y slot local; los emojis/captions pueden normalizarse distinto entre calendario y Meta. No usar lifetime como 24h/72h."
    })
pd.DataFrame(rows).to_csv(out_path, index=False)
print(f"wrote {len(rows)} rows to {out_path}")
