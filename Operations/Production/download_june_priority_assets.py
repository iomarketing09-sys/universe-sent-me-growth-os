#!/usr/bin/env python3
import csv
import subprocess
from pathlib import Path

src = Path("Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion_Enriquecido.csv")
out_dir = Path("Operations/Research/June_Priority_Assets")
out_dir.mkdir(parents=True, exist_ok=True)
seen = set()
with src.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("drive_match_status") != "Exacto_unico":
            continue
        did = row.get("drive_id_confirmed", "")
        ref = row.get("asset_ref_normalized", "")
        if not did or did in seen:
            continue
        seen.add(did)
        ext = Path(row.get("drive_filename_exact", "")).suffix or ".bin"
        target = out_dir / f"{ref}{ext}"
        if target.exists():
            continue
        params = f'{{"fileId":"{did}","alt":"media"}}'
        subprocess.run(["gws", "drive", "files", "get", "--params", params, "--output", str(target)], check=True)
        print(ref, target)
print(f"downloaded_or_present={len(seen)}")
