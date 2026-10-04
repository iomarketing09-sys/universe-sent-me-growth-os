#!/usr/bin/env python3
"""
harvest_comments.py - Recolector Unificado On-Demand para Universe Sent Me.
Monitoreo de salud instantáneo de OmniRoute y desacoplamiento seguro.
"""
import os
import sys
import shutil
import socket
import subprocess
from pathlib import Path

TENANT_DIR = Path(__file__).resolve().parent
COMM_DIR = TENANT_DIR / "comment_responses" / "facebook_comments"
APROBACIONES_LOCAL = COMM_DIR / "aprobaciones.json"

DRIVE_CANDIDATES = [
    Path(os.path.expanduser("~/GoogleDrive/Growth OS")),
    Path("/home/universe-sent-me/GoogleDrive/Growth OS"),
]

def check_omniroute(host: str = "127.0.0.1", port: int = 20128, timeout: float = 1.0) -> bool:
    """Verifica si el puerto local de OmniRoute está activo vía handshake TCP."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def main():
    print("=" * 70)
    print("📥 INICIANDO RECOLECCIÓN UNIFICADA DE COMENTARIOS (ON-DEMAND)")
    print("=" * 70)

    # 0. Monitoreo de salud de OmniRoute
    print("🤖 [0/4] Verificando estado del gateway OmniRoute (:20128)...")
    if check_omniroute():
        print("   ✅ OmniRoute ACTIVO en 127.0.0.1:20128")
        print("   ➔ Las propuestas en voz de personaje se generarán automáticamente.")
    else:
        print("   ⚠️  [ALERTA] OmniRoute APAGADO en 127.0.0.1:20128")
        print("   ℹ️  La recolección de Meta continuará sin interrupciones.")
        print("   ➔ Las propuestas saldrán en 'null' para redactarse en Gemini chat.")
        print("   💡 Tip: Para activar el generador local, ejecuta 'omniroute' en otra terminal.\n")

    # 1. Reconciliar contextos
    reconcile_script = TENANT_DIR / "reconcile_contexts.py"
    if reconcile_script.exists():
        print("🔗 [1/4] Reconciliando contextos de publicaciones recientes...")
        try:
            res = subprocess.run([sys.executable, str(reconcile_script)], cwd=str(TENANT_DIR), capture_output=True, text=True)
            if res.returncode == 0:
                print("   ✅ Contextos reconciliados correctamente.")
            else:
                print(f"   ⚠️ Aviso: {res.stderr.strip() or res.stdout.strip()}")
        except Exception as e:
            print(f"   ⚠️ Error en reconcile_contexts: {e}")
    else:
        print("ℹ️ [1/4] reconcile_contexts.py no encontrado, usando mapeo existente.")

    # 2. Extraer comentarios con main.py
    main_script = COMM_DIR / "main.py"
    if not main_script.exists():
        print(f"❌ Error: No se encontró main.py en {COMM_DIR}")
        return 1

    print("\n🔍 [2/4] Extrayendo comentarios activos (últimas 48h, modo seguro)...")
    try:
        res = subprocess.run([sys.executable, str(main_script), "--dry-run", "--max-comments", "100"], cwd=str(COMM_DIR), capture_output=True, text=True)
        for line in res.stdout.splitlines():
            if any(k in line for k in ["Total comentarios", "Descartados", "Requieren revision", "Propuestas", "RESUMEN", "seen", "OmniRoute", "Aviso"]):
                print(f"   {line}")
    except Exception as e:
        print(f"❌ Error al ejecutar extracción: {e}")
        return 1

    # 3. Generar plantilla aprobaciones.json
    print("\n📝 [3/4] Generando plantilla estructurada de aprobaciones...")
    try:
        subprocess.run([sys.executable, str(main_script), "--create-template", str(APROBACIONES_LOCAL)], cwd=str(COMM_DIR), capture_output=True, text=True)
        if APROBACIONES_LOCAL.exists():
            print(f"   ✅ Plantilla local generada: {APROBACIONES_LOCAL.name}")
        else:
            print("   ⚠️ No se encontró el archivo aprobaciones.json generado.")
    except Exception as e:
        print(f"   ⚠️ Error al generar plantilla: {e}")

    # 4. Sincronizar a Google Drive
    print("\n☁️ [4/4] Sincronizando con Google Drive (Cloud SSOT)...")
    drive_dest = None
    for cand in DRIVE_CANDIDATES:
        if cand.exists() and cand.is_dir():
            drive_dest = cand
            break

    if drive_dest and APROBACIONES_LOCAL.exists():
        target_file = drive_dest / "aprobaciones.json"
        try:
            shutil.copy2(APROBACIONES_LOCAL, target_file)
            print(f"   🚀 Sincronizado con éxito en: {target_file}")
        except Exception as e:
            print(f"   ⚠️ Error al copiar a Drive: {e}")
    else:
        if not drive_dest:
            print("   ℹ️ Nota: Carpeta de Google Drive no detectada en rutas estándar. Archivo local guardado.")
        else:
            print("   ⚠️ No se pudo copiar el archivo a Google Drive.")

    print("\n" + "=" * 70)
    print("✨ RECOLECCIÓN COMPLETADA")
    print("👉 Dile a Gemini en el chat: 'Listo, revisa comentarios'")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
