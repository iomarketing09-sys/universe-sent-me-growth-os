#!/usr/bin/env python3
"""
build_can_video.py — Pipeline Automatizado de Renderizado y Efectos para Bam in a Can
Ensambla video base (Flow AI), genera locución institucional y subtítulos de teletipo con edge-tts,
mezcla audio, quema gancho de clasificación y exporta a 9:16 vertical (12-14s).
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

ANALOG_FILTERS = {
    "clean": "null",  # Textura nativa de Flow sin alteración destructiva
    "16mm": (
        "eq=contrast=1.15:brightness=-0.03:saturation=0.85,"
        "noise=c1s=18:c1f=t+u:allf=t+u,"
        "curves=preset=vintage"
    ),
    "vhs": (
        "eq=contrast=1.2:brightness=0.02:saturation=1.3,"
        "noise=alls=22:allf=t,"
        "boxblur=0.8:0.8"
    ),
    "crt": (
        "eq=contrast=1.3:brightness=-0.05:saturation=0.7,"
        "curves=r='0/0 0.5/0.4 1/0.9':g='0/0 0.5/0.6 1/1':b='0/0 0.5/0.4 1/0.9'"
    )
}

def generate_voiceover_and_subs(
    text: str, 
    audio_path: Path, 
    subs_path: Path, 
    voice: str = "en-US-ChristopherNeural"
) -> bool:
    print(f"[*] Generando locución institucional y subtítulos ({voice})...")
    try:
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", str(audio_path),
            "--write-subtitles", str(subs_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[+] Audio generado: {audio_path.name}")
        print(f"[+] Subtítulos sincronizados: {subs_path.name}")
        return True
    except FileNotFoundError:
        print("[-] Aviso: 'edge-tts' no está instalado. Instálalo con: pip install --break-system-packages edge-tts")
        return False
    except Exception as e:
        print(f"[-] Error generando TTS y subtítulos: {e}")
        return False

def render_can_video(
    video_input: Path,
    output_path: Path,
    voice_audio: Path = None,
    subs_file: Path = None,
    sfx_audio: Path = None,
    filter_type: str = "clean",
    target_duration: float = 13.0,
    hook_text: str = ""
):
    print("=" * 65)
    print("BAM IN A CAN — MOTOR DE RENDERIZADO Y POST-PRODUCCIÓN")
    print("=" * 65)
    print(f" Video Entrada : {video_input.name}")
    print(f" Estilo Filtro : {filter_type.upper()}")
    print(f" Duración Meta : {target_duration}s (Regla de Oro: 12-15s)")
    print(f" Subtítulos    : {'Activados (Teletipo de Archivo)' if subs_file and subs_file.exists() else 'Ninguno'}")
    print(f" Destino Final : {output_path}")

    filter_chain = ANALOG_FILTERS.get(filter_type, "null")
    
    if filter_chain != "null":
        vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{filter_chain}"
    else:
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"

    if hook_text:
        safe_hook = hook_text.replace(':', r'\:').replace("'", r"\'")
        vf += (
            f",drawtext=text='{safe_hook}':fontcolor=white:fontsize=46:"
            f"box=1:boxcolor=black@0.75:boxborderw=10:x=(w-text_w)/2:y=h*0.14:enable='between(t,0,2.5)'"
        )

    if subs_file and subs_file.exists():
        subs_path_str = str(subs_file).replace(":", r"\:")
        vf += (
            f",subtitles={subs_path_str}:force_style='FontName=Courier New,FontSize=20,"
            f"PrimaryColour=&H00FFFFFF&,BackColour=&H80000000&,BorderStyle=3,Outline=0,"
            f"Shadow=0,MarginV=140,Alignment=2'"
        )

    cmd = ["ffmpeg", "-y", "-i", str(video_input)]
    inputs_count = 1

    if voice_audio and voice_audio.exists():
        cmd.extend(["-i", str(voice_audio)])
        inputs_count += 1
    if sfx_audio and sfx_audio.exists():
        cmd.extend(["-i", str(sfx_audio)])
        inputs_count += 1

    if inputs_count == 3:
        cmd.extend([
            "-filter_complex",
            f"[0:v]{vf}[v];[1:a]volume=1.0[a1];[2:a]volume=0.7[a2];[a1][a2]amix=inputs=2:duration=first[a]",
            "-map", "[v]", "-map", "[a]"
        ])
    elif inputs_count == 2:
        cmd.extend([
            "-filter_complex",
            f"[0:v]{vf}[v];[1:a]volume=1.0[a]",
            "-map", "[v]", "-map", "[a]"
        ])
    else:
        cmd.extend(["-vf", vf])

    cmd.extend([
        "-t", str(target_duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path)
    ])

    print("\n[*] Ejecutando ensamblado con FFmpeg...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"\n[+] ¡Éxito! Video renderizado: {output_path}")
        print(f" Tamaño: {output_path.stat().st_size / (1024 * 1024):.2f} MB")
        return True
    else:
        print(f"[-] Error en FFmpeg: {res.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Ensamblador automático de videos para Bam in a Can")
    parser.add_argument("--input", required=True, help="Ruta al video base (MP4)")
    parser.add_argument("--output", default="can_output.mp4", help="Nombre o ruta del MP4 final")
    parser.add_argument("--filter", choices=["clean", "16mm", "vhs", "crt"], default="clean", help="Filtro de imagen (default: clean)")
    parser.add_argument("--voice-text", default="", help="Texto para locución y subtítulos automáticos con edge-tts")
    parser.add_argument("--no-subtitles", action="store_true", help="Desactiva los subtítulos quemados")
    parser.add_argument("--sfx", default="", help="Ruta al archivo de sonido/música de fondo")
    parser.add_argument("--hook", default="", help="Texto de clasificación superior")
    parser.add_argument("--duration", type=float, default=13.0, help="Duración en segundos (default: 13s)")
    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"[-] Archivo no encontrado: {input_file}")
        sys.exit(1)

    output_file = Path(args.output)
    voice_file = None
    subs_file = None

    if args.voice_text:
        voice_file = Path("temp_voice.mp3")
        subs_file = Path("temp_subs.vtt") if not args.no_subtitles else None
        
        if subs_file:
            ok = generate_voiceover_and_subs(args.voice_text, voice_file, subs_file)
        else:
            try:
                cmd = ["edge-tts", "--voice", "en-US-ChristopherNeural", "--text", args.voice_text, "--write-media", str(voice_file)]
                subprocess.run(cmd, check=True)
                ok = True
            except Exception:
                ok = False
        
        if not ok:
            voice_file = None
            subs_file = None

    sfx_file = Path(args.sfx) if args.sfx else None

    render_can_video(
        video_input=input_file,
        output_path=output_file,
        voice_audio=voice_file,
        subs_file=subs_file,
        sfx_audio=sfx_file,
        filter_type=args.filter,
        target_duration=args.duration,
        hook_text=args.hook
    )

    if voice_file and voice_file.exists():
        voice_file.unlink()
    if subs_file and subs_file.exists():
        subs_file.unlink()

if __name__ == "__main__":
    main()
