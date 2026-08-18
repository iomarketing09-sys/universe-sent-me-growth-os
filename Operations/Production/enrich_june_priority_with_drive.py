#!/usr/bin/env python3
import re
from pathlib import Path
import pandas as pd

priority_path = Path("Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion.csv")
drive_path = Path("Operations/Research/2026-08-18_Drive_Assets_Junio_Listing.json")
out_path = Path("Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion_Enriquecido.csv")

priority = pd.read_csv(priority_path, dtype=str).fillna("")
drive = pd.read_json(drive_path)
files = drive.get("files", pd.Series(dtype=object)).tolist()
by_ref = {}
for f in files:
    m = re.search(r"(?:^|\s)(\d{3,7})(?:\D|$)", f.get("name", ""))
    if m:
        by_ref.setdefault(m.group(1), []).append(f)

rows = []
for _, r in priority.iterrows():
    raw_ref = r["asset_ref"]
    ref_match = re.search(r"(?<!\d)(\d{3,7})(?!\d)", raw_ref)
    ref = ref_match.group(1) if ref_match else raw_ref
    r["asset_ref_normalized"] = ref
    matches = by_ref.get(ref, [])
    r["drive_match_count"] = str(len(matches))
    r["drive_match_status"] = "Exacto_unico" if len(matches) == 1 else ("Multiples" if len(matches) > 1 else "No_encontrado")
    r["drive_filename_exact"] = matches[0].get("name", "") if len(matches) == 1 else ""
    r["drive_id_confirmed"] = matches[0].get("id", "") if len(matches) == 1 else ""
    rows.append(r)
pd.DataFrame(rows).to_csv(out_path, index=False)
print(f"wrote {len(rows)} rows to {out_path}")
print(pd.DataFrame(rows)[["asset_ref","shares","comments","drive_match_status","drive_filename_exact"]].to_string(index=False))
