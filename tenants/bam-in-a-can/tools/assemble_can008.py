#!/usr/bin/env python3
"""
assemble_can008.py — Ensamblador específico para CAN-008 (Radithor 1925)
Concatena Intro (2.5s), Apertura/Unboxing (4.5s) y Payoff Geiger (6.0s) = 13.0s total.
Conserva el audio nativo con efectos de sonido y estampa el rótulo canónico.
"""

from __future__ import annotations
import os
import sys
import subprocess
from pathlib import Path

DRIVE_DIR = Path("/home/universe-sent-me/GoogleDrive/Bam in a can/can 008")
FALLBACK_LOCAL_DIR = Path("assets/can008")

def find_clips() -> tuple[Path, Path, Path]:
    search_dirs = [DRIVE_DIR, FALLBACK_LOCAL_DIR, Path(".")]
    for d in search_dirs:
        if not d.exists():
            continue
        c1 = list(d.glob("*INTRO*"))
        c2 = list(d.glob("*ESCENA 1*")) or list(d.glob("*Hands_opening*"))
        c3 = list(d.glob("*ESCENA 2*")) or list(d.glob("*Geiger*"))
        if c1 and c2 and c3:
            return c1[0], c2[0], c3[0]
    
    print("[-] Error: No se encontraron los 3 clips en:")
    print(f"    {DRIVE_DIR}")
    sys.exit(1)

def assemble():
    clip1, clip2, clip3 = find_clips()
    output_local = Path("CAN008_Radium_Water_13s.mp4")
    output_drive = DRIVE_DIR / "CAN008_Radium_Water_13s.mp4"

    print("=" * 65)
    print(" BAM IN A CAN — ENSAMBLADO AUTOMATIZADO CAN-008 (13s)")
    print("=" * 65)
    print(f" Clip 1 (Intro)    : {clip1.name} (0.0s - 2.5s)")
    print(f" Clip 2 (Unboxing) : {clip2.name} (2.5s - 7.0s)")
    print(f" Clip 3 (Geiger)   : {clip3.name} (7.0s - 13.0s)")
    print(f" Destino local     : {output_local}")
    print("=" * 65)

    cmd = [
        "ffmpeg", "-y",
        "-ss", "0", "-t", "2.5", "-i", str(clip1),
        "-ss", "0", "-t", "4.5", "-i", str(clip2),
        "-ss", "0", "-t", "6.0", "-i", str(clip3),
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v0];"
        "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v1];"
        "[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v2];"
        "[v0][0:a][v1][1:a][v2][2:a]concat=n=3:v=1:a=1[vraw][araw];"
        "[vraw]eq=contrast=1.12:brightness=-0.02:saturation=0.9,"
        "drawtext=text='COLLECTION UNIT\\: CAN-008':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.7:boxborderw=10:x=(w-text_w)/2:y=h*0.15:enable='between(t,0,2.5)'[vout]",
        "-map", "[vout]", "-map", "[araw]",
        "-t", "13.0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        str(output_local)
    ]

    print("[*] Ejecutando renderizado y montaje con FFmpeg...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if res.returncode == 0 and output_local.exists():
        size_mb = output_local.stat().st_size / (1024 * 1024)
        print(f"\n[+] ¡ÉXITO! Video ensamblado correctamente:")
        print(f"    Archivo: {output_local.name} ({size_mb:.2f} MB)")
        print(f"    Duración: 13.0 segundos (Cumple regla de oro 12-15s)")

        if DRIVE_DIR.exists():
            try:
                import shutil
                shutil.copy2(output_local, output_drive)
                print(f"    [Drive] Sincronizado en: {output_drive}")
            except Exception as e:
                print(f"    [-] Aviso: No se pudo copiar a Drive: {e}")
        return True
    else:
        print(f"[-] Error en FFmpeg: {res.stderr}")
        return False

if __name__ == "__main__":
    assemble()
