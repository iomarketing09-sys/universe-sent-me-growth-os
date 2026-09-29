#!/usr/bin/env python3
"""
process_product_images.py — Pipeline de Optimización y Recorte de Imágenes para Catálogo
Tenant: Mica's Art & Deco (Growth OS)
"""

from __future__ import annotations
import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

def enhance_artwork(img: Image.Image) -> Image.Image:
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.08)
    sharpness = ImageEnhance.Sharpness(img)
    img = sharpness.enhance(1.15)
    color = ImageEnhance.Color(img)
    img = color.enhance(1.05)
    return img

def create_gallery_mockup(artwork: Image.Image, output_size: int = 1200) -> Image.Image:
    max_dim = int(output_size * 0.75)
    artwork_copy = artwork.copy()
    artwork_copy.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    w, h = artwork_copy.size
    
    bg_color = (248, 247, 245, 255)
    canvas = Image.new("RGBA", (output_size, output_size), bg_color)
    
    shadow_margin = 30
    shadow = Image.new("RGBA", (w + shadow_margin * 2, h + shadow_margin * 2), (0, 0, 0, 0))
    shadow_box = Image.new("RGBA", (w, h), (30, 30, 30, 50))
    shadow.paste(shadow_box, (shadow_margin, shadow_margin + 10))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    
    x = (output_size - w) // 2
    y = (output_size - h) // 2
    
    canvas.paste(shadow, (x - shadow_margin, y - shadow_margin), shadow)
    canvas.paste(artwork_copy, (x, y), artwork_copy if artwork_copy.mode == "RGBA" else None)
    return canvas.convert("RGB")

def process_image(input_path: Path, output_dir: Path, remove_bg: bool = True):
    print(f"\n[+] Procesando: {input_path.name}")
    try:
        raw_img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"    [-] Error abriendo imagen: {e}")
        return
        
    stem = input_path.stem.replace(" ", "_")
    
    if remove_bg:
        try:
            import rembg
            print("    -> Aplicando recorte neuronal con rembg...")
            cutout = rembg.remove(raw_img)
        except ImportError:
            print("    [!] rembg no instalado. Usando imagen directa (pip install rembg).")
            cutout = raw_img
    else:
        cutout = raw_img
        
    cutout_path = output_dir / f"{stem}_cutout.png"
    cutout.save(cutout_path, "PNG")
    print(f"    -> Guardado PNG transparente: {cutout_path.name}")
    
    enhanced = enhance_artwork(cutout)
    print("    -> Generando montaje e-commerce con sombra suave de galería...")
    gallery_img = create_gallery_mockup(enhanced, output_size=1200)
    gallery_path = output_dir / f"{stem}_ecommerce.jpg"
    gallery_img.save(gallery_path, "JPEG", quality=95)
    print(f"    -> Guardado montaje para Meta/Web: {gallery_path.name}")

def main():
    parser = argparse.ArgumentParser(description="Pipeline de Imágenes para Catálogo - Mica's Art & Deco")
    parser.add_argument("input", help="Ruta de una imagen o carpeta con fotos originales")
    parser.add_argument("--output", default="assets/processed", help="Carpeta de destino")
    parser.add_argument("--no-rembg", action="store_true", help="Omitir recorte de fondo")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if input_path.is_file():
        process_image(input_path, output_dir, remove_bg=not args.no_rembg)
    elif input_path.is_dir():
        valid_exts = [".jpg", ".jpeg", ".png", ".webp"]
        images = [f for f in input_path.iterdir() if f.suffix.lower() in valid_exts]
        print(f"[+] Se encontraron {len(images)} imágenes en {input_path}")
        for img in images:
            process_image(img, output_dir, remove_bg=not args.no_rembg)
    else:
        print(f"[-] No se encontró: {input_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
