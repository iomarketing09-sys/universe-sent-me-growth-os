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

    # 1. Sincronizar desde Google Drive si existe versión aprobada en la nube
    for cand in DRIVE_CANDIDATES:
        if cand.exists() and cand.is_dir():
            drive_file = cand / "aprobaciones.json"
            if drive_file.exists():
                try:
                    shutil.copy2(drive_file, APROBACIONES_LOCAL)
                    print("📥 Sincronizada la última versión de aprobaciones.json desde Google Drive.")
                except Exception as e:
                    print(f"   ⚠️ Aviso al sincronizar desde Drive: {e}")
                break

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
    print("📡 Despachando respuestas aprobadas a Meta Graph API...\n")
    res = subprocess.run(cmd, cwd=str(COMM_DIR))
    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
