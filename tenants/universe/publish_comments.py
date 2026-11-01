#!/usr/bin/env python3
"""
publish_comments.py - Publicador Unificado de Respuestas en Vivo para Universe Sent Me.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

TENANT_DIR = Path(__file__).resolve().parent
COMM_DIR = TENANT_DIR / "comment_responses" / "facebook_comments"
APROBACIONES_LOCAL = COMM_DIR / "aprobaciones.json"

DRIVE_CANDIDATES = [
    Path(os.path.expanduser("~/GoogleDrive/Growth OS")),
    Path("/home/universe-sent-me/GoogleDrive/Growth OS"),
]

def main():
    print("=" * 70)
    print("🚀 INICIANDO PUBLICACIÓN EN VIVO DE RESPUESTAS APROBADAS")
    print("=" * 70)

    drive_file = None
    for cand in dict.fromkeys(DRIVE_CANDIDATES):
        if cand.exists() and cand.is_dir():
            candidate_file = cand / "aprobaciones.json"
            if candidate_file.exists():
                drive_file = candidate_file
                break

    if drive_file and (
        not APROBACIONES_LOCAL.exists()
        or drive_file.stat().st_mtime > APROBACIONES_LOCAL.stat().st_mtime
    ):
        try:
            shutil.copy2(drive_file, APROBACIONES_LOCAL)
            print("📥 aprobaciones.json de Drive es más reciente; se usará esa versión.")
        except Exception as e:
            print(f"   ⚠️ Aviso al sincronizar desde Drive: {e}")
    elif drive_file:
        print("📌 Se usará la versión local de aprobaciones.json, que es más reciente que Drive.")

    if not APROBACIONES_LOCAL.exists():
        print(f"❌ Error: No se encontró {APROBACIONES_LOCAL}")
        return 1

    main_script = COMM_DIR / "main.py"
    if not main_script.exists():
        print(f"❌ Error: No se encontró main.py en {COMM_DIR}")
        return 1

    # 2. Cargar .env del tenant
    env_file = TENANT_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'").strip('"')

    # 3. Publicar respuestas aprobadas
    cmd = [
        sys.executable,
        str(main_script),
        "--live",
        "--publish-approved",
        str(APROBACIONES_LOCAL)
    ]
    cmd.extend(sys.argv[1:])
    print("📡 Despachando respuestas aprobadas a Meta Graph API...\n")
    res = subprocess.run(cmd, cwd=str(COMM_DIR))
    if res.returncode == 0 and drive_file:
        try:
            shutil.copy2(APROBACIONES_LOCAL, drive_file)
            print("☁️ Estado de publicación sincronizado de vuelta a Google Drive.")
        except Exception as e:
            print(f"   ⚠️ No se pudo sincronizar el estado a Drive: {e}")
    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
