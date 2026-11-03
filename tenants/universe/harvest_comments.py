#!/usr/bin/env python3
"""
harvest_comments.py - Recolector Unificado On-Demand para Universe Sent Me.
Monitoreo de salud instantáneo de OmniRoute y desacoplamiento seguro.
"""
import argparse
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


def sync_approval_files(local_dir: Path, drive_dest: Path) -> list[Path]:
    """Copia las colas locales a Drive; la cola local siempre es la fuente."""
    synced = []
    for local_file in sorted(local_dir.glob("aprobaciones*.json")):
        target_file = drive_dest / local_file.name
        shutil.copy2(local_file, target_file)
        synced.append(target_file)
        print(f"   🚀 Sincronizado: {target_file}")
    return synced

def main(argv=None):
    parser = argparse.ArgumentParser(description="Recolector de comentarios de Universe")
    parser.add_argument("--agent", action="store_true", help="Usar CommunicationsAgent en modo sugerencia")
    parser.add_argument("--agent-model", default=None, help="Modelo de OmniRoute para el agente")
    parser.add_argument("--hours", type=int, default=48, help="Ventana de tiempo en horas")
    parser.add_argument("--max-comments", type=int, default=100, help="Máximo de comentarios")
    args = parser.parse_args(argv)

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

    print(f"\n🔍 [2/4] Extrayendo comentarios activos (últimas {args.hours}h, modo seguro)...")
    try:
        command = [
            sys.executable,
            str(main_script),
            "--dry-run",
            "--hours",
            str(max(1, args.hours)),
            "--max-comments",
            str(max(1, args.max_comments)),
        ]
        if args.agent:
            command.append("--agent")
        if args.agent_model:
            command.extend(["--agent-model", args.agent_model])
        res = subprocess.run(command, cwd=str(COMM_DIR), capture_output=True, text=True)
        for line in res.stdout.splitlines():
            if any(k in line for k in ["Total comentarios", "Descartados", "Requieren revision", "Propuestas", "RESUMEN", "seen", "OmniRoute", "Aviso"]):
                print(f"   {line}")
        if res.returncode != 0:
            detail = res.stderr.strip() or res.stdout.strip()
            print(f"   ❌ La extracción falló (código {res.returncode}).")
            if detail:
                print(f"   {detail.splitlines()[-1]}")
            return res.returncode
    except Exception as e:
        print(f"❌ Error al ejecutar extracción: {e}")
        return 1

    # 3. Validar plantilla aprobaciones.json generada por main.py
    print("\n📝 [3/4] Validando plantilla estructurada de aprobaciones...")
    if APROBACIONES_LOCAL.exists():
        print(f"   ✅ Plantilla local disponible: {APROBACIONES_LOCAL.name}")
    else:
        print("   ⚠️ No se encontró aprobaciones.json; revisa la salida de la extracción.")

    # 4. Sincronizar a Google Drive
    print("\n☁️ [4/4] Sincronizando con Google Drive (Cloud SSOT)...")
    drive_dest = None
    for cand in DRIVE_CANDIDATES:
        if cand.exists() and cand.is_dir():
            drive_dest = cand
            break

    if drive_dest and APROBACIONES_LOCAL.exists():
        try:
            sync_approval_files(COMM_DIR, drive_dest)
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
