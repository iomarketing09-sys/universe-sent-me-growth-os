#!/usr/bin/env python3
"""
add_voice_and_subtitles.py — Bam in a Can
Genera la locución institucional en inglés (ChristopherNeural) con edge-tts,
construye los subtítulos formateados para 9:16 vertical (.ass) y mezcla
el audio de efectos de sonido con la voz en FFmpeg.
"""

from __future__ import annotations
import os
import sys
import subprocess
from pathlib import Path

DRIVE_DIR = Path("/home/universe-sent-me/GoogleDrive/Bam in a can/can 008")

VOICE_TEXT = (
    "Collection Unit 008. In 1925, certified radium water was sold as an elixir. "
    "One bottle per day... until your bones dissolved. Sealed for your protection. "
    "Do not drink the water."
)

ASS_SUBTITLES = """[Script Info]
Title: Bam in a Can - CAN-008 Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,52,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,3,3,0,2,60,60,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.60,0:00:02.80,Default,,0,0,0,,COLLECTION UNIT: CAN-008
Dialogue: 0,0:00:03.00,0:00:06.80,Default,,0,0,0,,In 1925, certified radium water was sold as an elixir.
Dialogue: 0,0:00:07.00,0:00:10.50,Default,,0,0,0,,One bottle per day... until your bones dissolved.
Dialogue: 0,0:00:10.80,0:00:13.80,Default,,0,0,0,,Sealed for your protection. Do not drink the water.
"""

def generate_voice(voice_file: Path) -> bool:
    print(f"[*] Generando locución institucional en inglés con edge-tts...")
    cmd = [
        "edge-tts",
        "--voice", "en-US-ChristopherNeural",
        "--rate", "+8%",
        "--text", VOICE_TEXT,
        "--write-media", str(voice_file)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[+] Locución generada con éxito: {voice_file.name}")
        return True
    except FileNotFoundError:
        print("[-] Aviso: 'edge-tts' no está instalado. Instalándolo con pip...")
        res = subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"])
        if res.returncode == 0:
            return generate_voice(voice_file)
        else:
            print("[-] No se pudo instalar edge-tts automáticamente.")
            return False
    except Exception as e:
        print(f"[-] Error generando voz: {e}")
        return False

def main():
    candidates = [
        Path("CAN008_Radium_Water_13s.mp4"),
        DRIVE_DIR / "CAN008_Radium_Water_13s.mp4",
        Path("CAN008_Radium_Water_14s.mp4"),
        DRIVE_DIR / "CAN008_Radium_Water_14s.mp4"
    ]
    input_video = None
    for c in candidates:
        if c.exists():
            input_video = c
            break

    if not input_video and DRIVE_DIR.exists():
        found = list(DRIVE_DIR.glob("*008*.mp4"))
        if found:
            input_video = found[0]

    if not input_video or not input_video.exists():
        print("[-] Error: No se encontró el video editado de entrada.")
        print(f"    Rutas buscadas: {candidates}")
        sys.exit(1)

    print("=" * 65)
    print(" BAM IN A CAN — POST-PRODUCCIÓN: VOZ INSTITUCIONAL + SUBTÍTULOS")
    print("=" * 65)
    print(f" Video Base       : {input_video.name}")
    print(f" Voz Seleccionada : en-US-ChristopherNeural (Narrador de archivo)")
    print(f" Duración Meta    : 14.0 segundos")
    print("=" * 65)

    voice_file = Path("can008_voice.mp3")
    ass_file = Path("can008.ass")
    output_local = Path("CAN008_Final_14s.mp4")
    output_drive = DRIVE_DIR / "CAN008_Final_14s.mp4"

    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ASS_SUBTITLES)
    print(f"[+] Archivo de subtítulos preparado: {ass_file.name}")

    if not generate_voice(voice_file):
        print("[-] Abortando por falta de audio de voz.")
        sys.exit(1)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_video),
        "-i", str(voice_file),
        "-filter_complex",
        "[0:a]volume=0.75[asfx];[1:a]volume=1.05[avoice];[asfx][avoice]amix=inputs=2:duration=first[aout];"
        "[0:v]ass=can008.ass[vout]",
        "-map", "[vout]", "-map", "[aout]",
        "-t", "14.0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        str(output_local)
    ]

    print("[*] Renderizando mezcla de audio y quemado de subtítulos con FFmpeg...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if res.returncode == 0 and output_local.exists():
        size_mb = output_local.stat().st_size / (1024 * 1024)
        print(f"\n[+] ¡ÉXITO! Video final terminado:")
        print(f"    Archivo: {output_local.name} ({size_mb:.2f} MB)")
        print(f"    Duración: 14.0 segundos")

        if DRIVE_DIR.exists():
            try:
                import shutil
                shutil.copy2(output_local, output_drive)
                print(f"    [Drive] Sincronizado en: {output_drive}")
            except Exception as e:
                print(f"    [-] Aviso: No se pudo copiar a Drive: {e}")
    else:
        print(f"[-] Error en FFmpeg: {res.stderr}")

if __name__ == "__main__":
    main()
