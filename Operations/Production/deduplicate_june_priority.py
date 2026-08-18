#!/usr/bin/env python3
import re
from pathlib import Path
import pandas as pd

src = Path("Operations/Research/Historical_Performance_Individuals.csv")
out = Path("Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion.csv")
df = pd.read_csv(src, dtype=str).fillna("")
j = df[df["period"].eq("Junio_2026")].copy()
for c in ["shares", "comments", "reactions", "metric_value"]:
    j[c] = pd.to_numeric(j[c], errors="coerce").fillna(0)
j["interactions"] = j["metric_value"]
j["asset_ref_normalized"] = j["asset_ref"].str.extract(r"(?<!\d)(\d{3,7})(?!\d)", expand=False).fillna("")
j["priority_score"] = j["shares"] + 5 * j["comments"] + 0.1 * j["interactions"]
j = j.sort_values(["shares", "interactions", "comments"], ascending=False)
# Keep one row per Meta publication; this removes role/record duplicates.
j = j.drop_duplicates(subset=["meta_id"], keep="first")
cols = [c for c in ["period", "role", "asset_ref", "filename_or_concept", "meta_id", "date", "local_time", "format", "metric_value", "reactions", "comments", "shares", "interactions", "priority_score", "asset_ref_normalized", "personaje_principal_normalizado", "tipo_humor_normalizado", "potencial_etiquetado"] if c in j]
j.head(25)[cols].to_csv(out, index=False)
print(f"unique June posts: {len(j)}; priority rows: {min(25, len(j))}; output: {out}")
print(j.head(25)[cols].to_string(index=False))
