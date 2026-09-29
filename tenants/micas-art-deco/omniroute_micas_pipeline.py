#!/usr/bin/env python3
"""
omniroute_micas_pipeline.py — Mica's Art & Deco
Pipeline con Universe_Combo (Nvidia Llama 3.2 Vision).
"""
import os
import io
import re
import sys
import json
import base64
import requests
from pathlib import Path
from PIL import Image, ImageFilter

OMNIROUTE_URL = "http://localhost:20128/v1/chat/completions"
BASE_PRODUCTS_DIR = Path("/home/universe-sent-me/GoogleDrive/MICAS/002 PRODUCTOS/02 - Pinturas Mica")

def process_painting(image_path):
    input_path = Path(image_path)
    if not input_path.exists():
        print(f"[-] Archivo no encontrado: {input_path}")
        return

    out_folder = input_path.parent / "procesadas"
    out_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("MICA'S ART & DECO — PIPELINE VISUAL CON UNIVERSE_COMBO")
    print(f"Lienzo: {input_path.name} ({input_path.stat().st_size / (1024*1024):.2f} MB)")
    print("=" * 65)

    # 1. Pre-escalado ligero en memoria (0% CPU)
    print("[1/3] Pre-escalando foto a 1024px para envío ultraligero...")
    with Image.open(input_path) as full_img:
        full_img = full_img.convert("RGB")
        orig_w, orig_h = full_img.size

        max_dim = 1024
        if max(orig_w, orig_h) > max_dim:
            scale = max_dim / max(orig_w, orig_h)
            new_size = (int(orig_w * scale), int(orig_h * scale))
            preview_img = full_img.resize(new_size, Image.Resampling.LANCZOS)
        else:
            preview_img = full_img

        buffer = io.BytesIO()
        preview_img.save(buffer, format="JPEG", quality=85)
        b64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # 2. Análisis multimodal con Universe_Combo
    print("[2/3] Consultando a Universe_Combo (Llama 3.2 Vision) en OmniRoute...")
    prompt = (
        "Eres el curador de arte de Mica's Art & Deco. Analiza esta fotografía de una pintura al óleo.\n"
        "Responde ÚNICAMENTE un objeto JSON válido con las siguientes claves:\n"
        "- 'box_2d': [ymin, xmin, ymax, xmax] coordenadas normalizadas de 0.0 a 1.0 que encierren exactamente el bastidor o lienzo de la pintura (sin incluir mesa, atril ni pared).\n"
        "- 'titulo': título comercial y poético para e-commerce.\n"
        "- 'descripcion': descripción en la voz cercana y paciente de Mica, resaltando la pincelada al óleo y la serenidad que aporta al hogar.\n"
        "- 'paleta_colores': lista de 3 a 5 colores principales de la pintura.\n"
        "No agregues texto fuera del JSON."
    )

    payload = {
        "model": "Universe_Combo",
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 600
    }

    analysis = None
    try:
        resp = requests.post(OMNIROUTE_URL, json=payload, timeout=60)
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            raw_content = data["choices"][0]["message"]["content"]
            match = re.search(r'\{.*\}', raw_content, re.DOTALL)
            if match:
                analysis = json.loads(match.group(0))
            else:
                analysis = json.loads(raw_content.strip())
        else:
            print(f"[!] Respuesta de OmniRoute sin 'choices': {data}")
    except Exception as e:
        print(f"[!] Error al consultar/parsear: {e}")

    if not analysis or "box_2d" not in analysis or len(analysis["box_2d"]) < 4:
        analysis = {
            "box_2d": [0.08, 0.08, 0.92, 0.92],
            "titulo": f"Óleo Colección Mica - {input_path.stem}",
            "descripcion": "Pintura al óleo sobre lienzo de autor con rica textura y estudio de luz natural.",
            "paleta_colores": ["Tonos cálidos", "Tierra", "Óleo natural"]
        }

    print(f"[+] Título: {analysis.get('titulo')}")
    print(f"[+] Coordenadas: {analysis.get('box_2d')}")

    # 3. Montaje y recorte protegido
    print("[3/3] Generando montaje de galería sobre lienzo lino (#F8F7F5)...")
    box = analysis.get("box_2d", [0.08, 0.08, 0.92, 0.92])

    # Desempaquetado nativo sin índices numéricos
    coords = [float(v) for v in box[:4]]
    ymin, xmin, ymax, xmax = coords

    if max(ymin, xmin, ymax, xmax) > 1.0:
        ymin = ymin / 1000.0
        xmin = xmin / 1000.0
        ymax = ymax / 1000.0
        xmax = xmax / 1000.0

    left = max(0, int(xmin * orig_w))
    top = max(0, int(ymin * orig_h))
    right = min(orig_w, int(xmax * orig_w))
    bottom = min(orig_h, int(ymax * orig_h))

    if right <= left or bottom <= top:
        left, top, right, bottom = 0, 0, orig_w, orig_h

    cropped_painting = full_img.crop((left, top, right, bottom))

    canvas_w, canvas_h = 1200, 1200
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (248, 247, 245, 255))

    cw, ch = cropped_painting.size
    aspect = cw / ch
    if aspect >= 1.0:
        target_w = 880
        target_h = int(target_w / aspect)
    else:
        target_h = 880
        target_w = int(target_h * aspect)

    p_final = cropped_painting.resize((target_w, target_h), Image.Resampling.LANCZOS).convert("RGBA")

    # Sombra difusa suave de galería
    shadow_pad = 50
    shadow = Image.new("RGBA", (target_w + shadow_pad, target_h + shadow_pad), (0, 0, 0, 0))
    shadow_box = Image.new("RGBA", (target_w, target_h), (35, 30, 25, 75))
    shadow.paste(shadow_box, (shadow_pad // 2, shadow_pad // 2))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))

    pos_x = (canvas_w - target_w) // 2
    pos_y = (canvas_h - target_h) // 2

    canvas.paste(shadow, (pos_x - 10, pos_y - 4), shadow)
    canvas.paste(p_final, (pos_x, pos_y), p_final)

    out_img = out_folder / f"{input_path.stem}_ecommerce.jpg"
    canvas.convert("RGB").save(out_img, "JPEG", quality=95)

    out_json = out_folder / f"{input_path.stem}_ficha.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    print("=" * 65)
    print("¡PROCESO COMPLETADO EXITOSAMENTE!")
    print(f"Foto de Galería: {out_img}")
    print(f"Ficha Comercial: {out_json}")
    print("=" * 65)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[-1]
    else:
        target = str(BASE_PRODUCTS_DIR / "Manzana.jpg")
    process_painting(target)
