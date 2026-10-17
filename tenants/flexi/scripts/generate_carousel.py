#!/usr/bin/env python3
"""
Generador de carruseles para Meta Ads / Instagram / WhatsApp.
Plantillas programáticas usando Pillow.
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ Pillow no instalado. Ejecutar: pip install pillow")

@dataclass
class CarouselSpec:
    model_code: str
    model_name: str
    brand: str  # 'flexi' o 'quirelli'
    colors: List[str]
    asset_paths: List[Path]
    output_dir: Path
    format: str = "square"  # square (1080x1080), story (1080x1920)
    slides: int = 3

# Brand guidelines (de brand_voice.json)
BRAND_CONFIG = {
    "flexi": {
        "primary_color": "#003366",  # Azul marino Flexi
        "secondary_color": "#FFFFFF",
        "accent_color": "#FFD700",   # Dorado
        "font_primary": "Montserrat-Bold",
        "font_secondary": "Montserrat-Regular",
        "logo_path": None,  # Se resolverá desde assets/brand
        "tagline": "Camina con confianza"
    },
    "quirelli": {
        "primary_color": "#1A1A2E",    # Azul oscuro casi negro
        "secondary_color": "#FFFFFF",
        "accent_color": "#C9A84C",     # Dorado Quirelli
        "font_primary": "PlayfairDisplay-Bold",
        "font_secondary": "PlayfairDisplay-Regular",
        "logo_path": None,
        "tagline": "Arte en cada paso"
    }
}

def load_brand_voice() -> Dict:
    """Carga brand_voice.json"""
    path = Path("/home/universe-sent-me/growth-os/tenants/flexi/brand_voice.json")
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_model_assets(model_code: str, brand: str) -> List[Path]:
    """Obtiene paths de assets para un modelo"""
    base = Path("/home/universe-sent-me/growth-os/tenants/flexi/assets") / brand / "campana_oi26" / model_code
    if base.exists():
        return list(base.glob("*.jpg")) + list(base.glob("*.JPG")) + list(base.glob("*.png")) + list(base.glob("*.PNG"))
    return []

def create_carousel_template(spec: CarouselSpec) -> List[Path]:
    """Crea carrusel usando plantilla programática"""
    if not PIL_AVAILABLE:
        print("Pillow requerido para generar imágenes")
        return []
    
    brand_cfg = BRAND_CONFIG.get(spec.brand, BRAND_CONFIG["flexi"])
    output_paths = []
    
    # Dimensiones
    if spec.format == "square":
        width, height = 1080, 1080
    else:
        width, height = 1080, 1920
    
    # Colores
    primary = brand_cfg["primary_color"]
    secondary = brand_cfg["secondary_color"]
    accent = brand_cfg["accent_color"]
    
    for slide_idx in range(spec.slides):
        # Crear canvas
        img = Image.new('RGB', (width, height), primary)
        draw = ImageDraw.Draw(img)
        
        # Slide 1: Hero con producto
        if slide_idx == 0:
            # Fondo con asset principal
            if spec.asset_paths:
                asset_img = Image.open(spec.asset_paths[0])
                # Redimensionar manteniendo aspect ratio
                asset_img.thumbnail((width, height), Image.Resampling.LANCZOS)
                # Centrar
                x = (width - asset_img.width) // 2
                y = (height - asset_img.height) // 2
                img.paste(asset_img, (x, y))
            
            # Overlay con nombre modelo
            draw.rectangle([0, height-200, width, height], fill=primary + "CC")
            draw.text((50, height-180), spec.model_name, fill=secondary, font_size=48)
            draw.text((50, height-120), f"Modelo {spec.model_code}", fill=accent, font_size=24)
            
        # Slide 2: Colores disponibles
        elif slide_idx == 1:
            draw.text((50, 100), "Colores Disponibles", fill=secondary, font_size=48)
            y_pos = 200
            for color in spec.colors[:5]:
                draw.text((100, y_pos), f"● {color}", fill=secondary, font_size=32)
                y_pos += 80
            
            # Tagline
            draw.text((50, height-150), brand_cfg["tagline"], fill=accent, font_size=36)
            
        # Slide 3: CTA / Tecnología
        elif slide_idx == 2:
            draw.text((50, 100), "Tecnología", fill=secondary, font_size=48)
            tech_text = "Walking Soft" if spec.brand == "flexi" else "Hexafoam"
            draw.text((50, 200), tech_text, fill=accent, font_size=36)
            draw.text((50, 300), "Confort todo el día", fill=secondary, font_size=28)
            
            # CTA
            draw.rectangle([width//2-150, height-200, width//2+150, height-120], fill=accent)
            draw.text((width//2-100, height-185), "VER MÁS", fill=primary, font_size=32)
        
        # Guardar
        output_file = spec.output_dir / f"{spec.brand}_{spec.model_code}_slide{slide_idx+1}.png"
        img.save(output_file, "PNG", quality=95)
        output_paths.append(output_file)
        print(f"  ✅ Slide {slide_idx+1}: {output_file}")
    
    return output_paths

def main():
    parser = argparse.ArgumentParser(description="Generar carruseles para Meta Ads")
    parser.add_argument("--model", help="Código de modelo (ej: 143001)")
    parser.add_argument("--brand", choices=["flexi", "quirelli"], default="flexi")
    parser.add_argument("--top5", action="store_true", help="Generar top 5 prioridad")
    parser.add_argument("--format", choices=["square", "story"], default="square")
    parser.add_argument("--slides", type=int, default=3)
    args = parser.parse_args()
    
    output_dir = Path("/home/universe-sent-me/growth-os/tenants/flexi/content/carruseles")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.top5:
        # Leer mapeo para top 5
        map_csv = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/catalogo_con_assets.csv")
        if map_csv.exists():
            import csv
            with open(map_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Filtrar completos, ordenar por asset_count
                rows = [r for r in reader if r['estado'] == 'COMPLETO']
                rows.sort(key=lambda x: -int(x['asset_count']))
                top5 = rows[:5]
                
                for row in top5:
                    model_code = row['modelo']
                    brand = row['marca'].lower()
                    colors = row['colores_catalogo'].split(';')
                    assets = get_model_assets(model_code, brand)
                    
                    spec = CarouselSpec(
                        model_code=model_code,
                        model_name=row['nombre_asset'],
                        brand=brand,
                        colors=colors,
                        asset_paths=assets,
                        output_dir=output_dir,
                        format=args.format,
                        slides=args.slides
                    )
                    print(f"\n🎨 Generando carrusel para {model_code} ({brand})...")
                    create_carousel_template(spec)
    elif args.model:
        # Cargar info del modelo desde mapeo
        map_csv = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/catalogo_con_assets.csv")
        model_info = None
        if map_csv.exists():
            import csv
            with open(map_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['modelo'] == args.model:
                        model_info = row
                        break
        
        if model_info:
            brand = model_info['marca'].lower()
            colors = model_info['colores_catalogo'].split(';')
            assets = get_model_assets(args.model, brand)
            
            spec = CarouselSpec(
                model_code=args.model,
                model_name=model_info['nombre_asset'],
                brand=brand,
                colors=colors,
                asset_paths=assets,
                output_dir=output_dir,
                format=args.format,
                slides=args.slides
            )
            print(f"\n🎨 Generando carrusel para {args.model} ({brand})...")
            create_carousel_template(spec)
        else:
            print(f"❌ Modelo {args.model} no encontrado en mapeo")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
