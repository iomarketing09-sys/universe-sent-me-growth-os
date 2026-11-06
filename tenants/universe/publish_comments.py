#!/usr/bin/env python3
"""
publish_comments.py - Publicador Unificado de Respuestas en Vivo para Universe Sent Me.
"""
import os
import sys
import subprocess
from pathlib import Path

TENANT_DIR = Path(__file__).resolve().parent
COMM_DIR = TENANT_DIR / "comment_responses" / "facebook_comments"
APROBACIONES_LOCAL = COMM_DIR / "aprobaciones.json"

def main():
    print("=" * 70)
    print("🚀 INICIANDO PUBLICACIÓN EN VIVO DE RESPUESTAS APROBADAS")
    print("=" * 70)

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
    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
