#!/usr/bin/env python3
"""
Reubicación de assets según la regla de custodia hacia adelante:
- Si se reutilizó en Julio/Agosto/Septiembre -> se mueve a ese mes.
- El resto se queda en la raíz de '06 Junio/' (nunca hacia atrás).
- Se elimina 'New folder/'.
"""

from __future__ import annotations
import argparse
import csv
import json
import re
import shutil
from pathlib import Path

def normalize_name(name: str) -> str:
    base = Path(name).stem.strip().lower()
    match = re.search(r'\b(260\d{3,4}|humor[\d\.]+)\b', base)
    return match.group(1) if match else base

def scan_full_repo(growth_root: Path) -> dict[str, str]:
    history: dict[str, str] = {}

    def register(filename_raw: str, date_str: str):
        if not filename_raw or not date_str:
            return
        clean_date = date_str.strip()[:10]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", clean_date):
            return
            
        raw_name = Path(filename_raw).name.strip()
        norm_key = normalize_name(raw_name)
        
        if raw_name not in history or clean_date > history[raw_name]:
            history[raw_name] = clean_date
        if norm_key not in history or clean_date > history[norm_key]:
            history[norm_key] = clean_date

    for csv_file in growth_root.rglob("*.csv"):
        if ".git" in str(csv_file) or ".venv" in str(csv_file):
            continue
        try:
            with csv_file.open(encoding="utf-8", errors="ignore") as f:
                for row in csv.reader(f):
                    dates = [col.strip()[:10] for col in row if re.match(r"^\d{4}-\d{2}-\d{2}", col.strip())]
                    if dates:
                        latest_date = max(dates)
                        for col in row:
                            clean_col = col.strip()
                            if any(ext in clean_col.lower() for ext in [".png", ".jpeg", ".jpg"]) or re.search(r'\b(260\d{3,4}|humor[\d\.]+)\b', clean_col.lower()):
                                register(clean_col, latest_date)
        except Exception:
            pass

    for json_file in growth_root.rglob("*contexts*.json"):
        if ".git" in str(json_file):
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        dt = v.get("date") or v.get("scheduled_date") or v.get("published_date") or ""
                        asset = v.get("asset") or v.get("file") or v.get("filename") or v.get("media_url") or ""
                        if dt and asset:
                            register(asset, dt)
        except Exception:
            pass

    drive_growth = Path("/home/universe-sent-me/GoogleDrive/Growth OS")
    if drive_growth.exists():
        for csv_file in drive_growth.glob("*.csv"):
            try:
                with csv_file.open(encoding="utf-8", errors="ignore") as f:
                    for row in csv.reader(f):
                        if len(row) >= 5 and re.match(r"^\d{4}-\d{2}-\d{2}$", row[0].strip()):
                            register(row[4], row[0])
            except Exception:
                pass

    return history

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Ejecuta los movimientos físicamente.")
    args = parser.parse_args()

    growth_root = Path("/home/universe-sent-me/growth-os")
    assets_root = Path("/home/universe-sent-me/GoogleDrive/Universe sent me/USM/Humor existencial")
    if not assets_root.exists():
        assets_root = Path.home() / "GoogleDrive" / "Universe sent me" / "USM" / "Humor existencial"

    source_dir = assets_root / "06 Junio" / "New folder"

    if not source_dir.exists():
        print(f"❌ No se encontró el directorio de origen: {source_dir}")
        return 1

    files = [f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() in [".png", ".jpeg", ".jpg"]]
    print(f"📦 Total assets en '06 Junio/New folder/': {len(files)}")

    history = scan_full_repo(growth_root)

    moves = []
    for f in sorted(files, key=lambda x: x.name):
        norm_k = normalize_name(f.name)
        last_date = history.get(f.name) or history.get(norm_k) or ""

        # Regla hacia adelante: solo avanzar a meses posteriores a junio
        if last_date.startswith("2026-09"):
            dest = assets_root / "09 Septiembre"
            tag = f"Reutilizado en Septiembre ({last_date})"
        elif last_date.startswith("2026-08"):
            dest = assets_root / "08 Agosto"
            tag = f"Reutilizado en Agosto ({last_date})"
        elif last_date.startswith("2026-07"):
            dest = assets_root / "07 Julio"
            tag = f"Reutilizado en Julio ({last_date})"
        else:
            dest = assets_root / "06 Junio"
            tag = "Base Junio (activo para reuso)"

        moves.append((f, dest, tag))

    print("\n--- Plan de Movimientos (Regla hacia adelante) ---")
    for src, dst, tag in moves:
        print(f"• {src.name} -> {dst.name}/ [{tag}]")

    counts = {}
    for _, dst, _ in moves:
        counts[dst.name] = counts.get(dst.name, 0) + 1
    
    print("\n📊 Resumen de reubicación:")
    for dest_name, c in sorted(counts.items()):
        print(f"• A '{dest_name}/': {c} assets")

    if not args.live:
        print("\n⚠️ MODO DRY-RUN: Ejecuta con --live para aplicar:")
        print("python3 depurate_new_folder.py --live")
    else:
        print("\n🚀 EJECUTANDO MOVIMIENTOS FÍSICOS EN GOOGLE DRIVE...")
        for src, dst, _ in moves:
            dst.mkdir(parents=True, exist_ok=True)
            target = dst / src.name
            shutil.move(str(src), str(target))
            print(f"✅ Movido: {src.name} -> {dst.name}/")

        remaining = list(source_dir.iterdir())
        if not remaining:
            source_dir.rmdir()
            print("\n🧹 Carpeta '06 Junio/New folder/' eliminada con éxito.")
        else:
            print(f"\n⚠️ Quedan {len(remaining)} elementos no reconocidos en 'New folder/'.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
