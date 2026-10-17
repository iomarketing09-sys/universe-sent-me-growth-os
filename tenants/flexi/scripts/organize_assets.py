#!/usr/bin/env python3
"""
Script para extraer y organizar assets de marketing de Flexi y Quirelli.
Fuente: /home/universe-sent-me/GoogleDrive/Informes FLEXI/marketing/
Destino: tenants/flexi/assets/
"""

import os
import re
import json
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configuración de rutas
SOURCE_BASE = Path("/home/universe-sent-me/GoogleDrive/Informes FLEXI/marketing")
DEST_BASE = Path("/home/universe-sent-me/growth-os/tenants/flexi/assets")

# Patrones de nomenclatura detectados
FLEXI_PATTERN = re.compile(r'^([A-Z_]+)_(\d{5,6})_([A-ZÁÉÍÓÚÑ]+)_OI26', re.IGNORECASE)
QUIRELLI_PATTERN = re.compile(r'^([A-Z_]+)_(\d{5,6})_([A-ZÁÉÍÓÚÑ]+)_QUIRELLI_OI26', re.IGNORECASE)

# Modelos oficiales del catálogo (cargados desde CSV)
CATALOG_MODELS = set()

@dataclass
class AssetInfo:
    """Información de un asset individual"""
    source_path: str
    dest_path: str
    filename: str
    brand: str  # 'flexi' o 'quirelli'
    model_name: str  # ej: GINNY, ADRIENNA
    model_code: str  # ej: 143001, 307201
    color: str
    is_catalog: bool = False
    is_technology: bool = False
    is_brand: bool = False
    is_derechos: bool = False
    size_bytes: int = 0
    extracted_at: str = ""
    error: str = ""

def load_catalog_models():
    """Carga los códigos de modelo del catálogo oficial"""
    global CATALOG_MODELS
    csv_path = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/catalogo_modelos_oficiales.csv")
    if csv_path.exists():
        import csv
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                CATALOG_MODELS.add(row['Modelo'].strip())
    print(f"Modelos en catálogo oficial: {len(CATALOG_MODELS)}")

def parse_filename(filename: str, brand_hint: str = None) -> Optional[Tuple[str, str, str]]:
    """
    Parsea el nombre de archivo y retorna (model_name, model_code, color)
    Retorna None si no coincide con patrón conocido
    """
    # Probar patrón Flexi
    match = FLEXI_PATTERN.match(filename)
    if match:
        return match.group(1), match.group(2), match.group(3)
    
    # Probar patrón Quirelli
    match = QUIRELLI_PATTERN.match(filename)
    if match:
        return match.group(1), match.group(2), match.group(3)
    
    # Si hay hint de marca, intentar patrones más flexibles
    if brand_hint == 'flexi':
        # Buscar código de 5-6 dígitos
        code_match = re.search(r'(\d{5,6})', filename)
        if code_match:
            code = code_match.group(1)
            # Intentar extraer nombre y color alrededor del código
            parts = filename.replace('.jpg', '').replace('.JPG', '').replace('.png', '').replace('.PNG', '').split('_')
            if len(parts) >= 3:
                return parts[0], code, parts[2]
    
    return None

def determine_brand_from_path(path: Path) -> str:
    """Determina la marca basándose en la ruta"""
    path_str = str(path).lower()
    if 'quirelli' in path_str:
        return 'quirelli'
    return 'flexi'

def should_process_file(filename: str) -> bool:
    """Filtra archivos a procesar (imágenes, PDFs relevantes)"""
    ext = filename.lower().split('.')[-1]
    return ext in ['jpg', 'jpeg', 'png', 'pdf', 'zip']

def extract_zip(zip_path: Path, extract_to: Path) -> List[Path]:
    """Extrae un ZIP y retorna lista de archivos extraídos"""
    extracted = []
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_to)
            for member in zf.namelist():
                extracted.append(extract_to / member)
    except Exception as e:
        print(f"Error extrayendo {zip_path}: {e}")
    return extracted

def safe_copy(src: Path, dst: Path) -> bool:
    """Copia archivo manejando errores de I/O"""
    try:
        # Usar copy en lugar de copy2 para evitar errores de xattr
        shutil.copy(src, dst)
        return True
    except OSError as e:
        print(f"  ⚠️ Error copiando {src.name}: {e}")
        return False
    except Exception as e:
        print(f"  ⚠️ Error inesperado copiando {src.name}: {e}")
        return False

def process_directory(source_dir: Path, brand: str, asset_list: List[AssetInfo], 
                      is_catalog: bool = False, is_technology: bool = False, 
                      is_brand: bool = False, is_derechos: bool = False):
    """Procesa un directorio recursivamente"""
    for file_path in source_dir.rglob('*'):
        if file_path.is_file() and should_process_file(file_path.name):
            parsed = parse_filename(file_path.name, brand)
            if parsed:
                model_name, model_code, color = parsed
                # Normalizar color
                color = color.upper().replace('_', ' ')
                
                # Determinar subcarpeta destino
                if is_catalog:
                    subdir = 'catalogo'
                elif is_technology:
                    subdir = 'tecnologias'
                elif is_brand:
                    subdir = 'brand'
                elif is_derechos:
                    subdir = 'derechos'
                else:
                    subdir = 'campana_oi26'
                
                # Estructura: brand/subdir/model_code/
                dest_dir = DEST_BASE / brand / subdir / model_code
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / file_path.name
                
                # Copiar archivo
                if not dest_file.exists():
                    success = safe_copy(file_path, dest_file)
                    if not success:
                        asset_list.append(AssetInfo(
                            source_path=str(file_path),
                            dest_path=str(dest_file),
                            filename=file_path.name,
                            brand=brand,
                            model_name=model_name,
                            model_code=model_code,
                            color=color,
                            is_catalog=is_catalog,
                            is_technology=is_technology,
                            is_brand=is_brand,
                            is_derechos=is_derechos,
                            size_bytes=0,
                            extracted_at=datetime.now().isoformat(),
                            error=f"Copy failed: {file_path.name}"
                        ))
                        continue
                
                asset_list.append(AssetInfo(
                    source_path=str(file_path),
                    dest_path=str(dest_file),
                    filename=file_path.name,
                    brand=brand,
                    model_name=model_name,
                    model_code=model_code,
                    color=color,
                    is_catalog=is_catalog,
                    is_technology=is_technology,
                    is_brand=is_brand,
                    is_derechos=is_derechos,
                    size_bytes=file_path.stat().st_size if file_path.exists() else 0,
                    extracted_at=datetime.now().isoformat(),
                    error=""
                ))
            else:
                # Archivo sin patrón reconocido - copiar a folder genérico
                if is_catalog or is_technology or is_brand or is_derechos:
                    subdir = 'catalogo' if is_catalog else ('tecnologias' if is_technology else ('brand' if is_brand else 'derechos'))
                    dest_dir = DEST_BASE / brand / subdir / 'otros'
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    dest_file = dest_dir / file_path.name
                    if not dest_file.exists():
                        success = safe_copy(file_path, dest_file)
                        if not success:
                            continue
                    
                    asset_list.append(AssetInfo(
                        source_path=str(file_path),
                        dest_path=str(dest_file),
                        filename=file_path.name,
                        brand=brand,
                        model_name='DESCONOCIDO',
                        model_code='000000',
                        color='DESCONOCIDO',
                        is_catalog=is_catalog,
                        is_technology=is_technology,
                        is_brand=is_brand,
                        is_derechos=is_derechos,
                        size_bytes=file_path.stat().st_size if file_path.exists() else 0,
                        extracted_at=datetime.now().isoformat(),
                        error=""
                    ))

def process_zip_files():
    """Procesa archivos ZIP de catálogos, tecnología, brand"""
    asset_list = []
    
    # === FLEXI ===
    flexi_base = SOURCE_BASE / "Flexi"
    
    # Catálogos Flexi
    catalogo_dir = flexi_base / "Catalogo"
    for zip_file in catalogo_dir.glob("*.zip"):
        print(f"Procesando catálogo: {zip_file.name}")
        extract_dir = DEST_BASE / "flexi" / "catalogo" / "_temp_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        extracted = extract_zip(zip_file, extract_dir)
        for f in extracted:
            if f.is_file():
                process_directory(f.parent, 'flexi', asset_list, is_catalog=True)
        # Limpiar temp
        shutil.rmtree(extract_dir, ignore_errors=True)
    
    # Tecnologías y atributos
    tech_dir = flexi_base / "Tenologias y atributos"
    for zip_file in tech_dir.glob("*.zip"):
        print(f"Procesando tecnología: {zip_file.name}")
        extract_dir = DEST_BASE / "flexi" / "tecnologias" / "_temp_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        extracted = extract_zip(zip_file, extract_dir)
        for f in extracted:
            if f.is_file():
                process_directory(f.parent, 'flexi', asset_list, is_technology=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
    
    # Brand Flexi
    brand_dir = flexi_base / "logotipo oficial"
    for zip_file in brand_dir.glob("*.zip"):
        print(f"Procesando brand: {zip_file.name}")
        extract_dir = DEST_BASE / "flexi" / "brand" / "_temp_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        extracted = extract_zip(zip_file, extract_dir)
        for f in extracted:
            if f.is_file():
                process_directory(f.parent, 'flexi', asset_list, is_brand=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
    
    # Flexi Country Brand
    fc_brand_dir = flexi_base / "Logo Flexi Country"
    for zip_file in fc_brand_dir.glob("*.zip"):
        print(f"Procesando Flexi Country brand: {zip_file.name}")
        extract_dir = DEST_BASE / "flexi" / "brand" / "_temp_extract_fc"
        extract_dir.mkdir(parents=True, exist_ok=True)
        extracted = extract_zip(zip_file, extract_dir)
        for f in extracted:
            if f.is_file():
                process_directory(f.parent, 'flexi', asset_list, is_brand=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
    
    # Campaña OI26 - Fotos finales (ya descomprimidas)
    campaign_dir = flexi_base / "Campaña OI26" / "FOTOS OI26 FINALES"
    if campaign_dir.exists():
        print(f"Procesando campaña Flexi OI26...")
        process_directory(campaign_dir, 'flexi', asset_list)
    
    # Portadillas Flexi
    portadillas_dir = flexi_base / "Campaña OI26" / "PORTADILLAS FLEXI OI26"
    if portadillas_dir.exists():
        print(f"Procesando portadillas Flexi...")
        process_directory(portadillas_dir, 'flexi', asset_list)
    
    # Campaña Country OI26
    country_dir = flexi_base / "Campaña Country OI26"
    if country_dir.exists():
        # PDFs de derechos
        for pdf in country_dir.glob("*.pdf"):
            dest_dir = DEST_BASE / "shared" / "derechos"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / pdf.name
            if not dest_file.exists():
                safe_copy(pdf, dest_file)
            asset_list.append(AssetInfo(
                source_path=str(pdf),
                dest_path=str(dest_file),
                filename=pdf.name,
                brand='shared',
                model_name='DERECHOS',
                model_code='000000',
                color='N/A',
                is_derechos=True,
                size_bytes=pdf.stat().st_size if pdf.exists() else 0,
                extracted_at=datetime.now().isoformat(),
                error=""
            ))
        
        # Portadillas Quirelli (ZIP grande)
        for zip_file in country_dir.glob("*.zip"):
            print(f"Procesando portadillas Quirelli: {zip_file.name}")
            extract_dir = DEST_BASE / "quirelli" / "portadillas" / "_temp_extract"
            extract_dir.mkdir(parents=True, exist_ok=True)
            extracted = extract_zip(zip_file, extract_dir)
            for f in extracted:
                if f.is_file():
                    process_directory(f.parent, 'quirelli', asset_list)
            shutil.rmtree(extract_dir, ignore_errors=True)
    
    # === QUIRELLI ===
    quirelli_base = SOURCE_BASE / "Quirelli"
    
    # Catálogo Quirelli
    for zip_file in quirelli_base.glob("*.zip"):
        print(f"Procesando catálogo Quirelli: {zip_file.name}")
        extract_dir = DEST_BASE / "quirelli" / "catalogo" / "_temp_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        extracted = extract_zip(zip_file, extract_dir)
        for f in extracted:
            if f.is_file():
                process_directory(f.parent, 'quirelli', asset_list, is_catalog=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
    
    # Campaña Quirelli OI26
    campaign_q_dir = quirelli_base / "Campaña OI26" / "Campaña"
    if campaign_q_dir.exists():
        print(f"Procesando campaña Quirelli OI26...")
        process_directory(campaign_q_dir, 'quirelli', asset_list)
    
    # Essencial Quirelli
    essencial_dir = quirelli_base / "Campaña OI26" / "Essencial"
    if essencial_dir.exists():
        print(f"Procesando Essencial Quirelli...")
        process_directory(essencial_dir, 'quirelli', asset_list)
    
    # Brand Quirelli
    brand_q_dir = quirelli_base / "Logo oficial"
    for zip_file in brand_q_dir.glob("*.zip"):
        print(f"Procesando brand Quirelli: {zip_file.name}")
        extract_dir = DEST_BASE / "quirelli" / "brand" / "_temp_extract"
        extract_dir.mkdir(parents=True, exist_ok=True)
        extracted = extract_zip(zip_file, extract_dir)
        for f in extracted:
            if f.is_file():
                process_directory(f.parent, 'quirelli', asset_list, is_brand=True)
        shutil.rmtree(extract_dir, ignore_errors=True)
    
    # PDFs de derechos Quirelli
    for pdf in quirelli_base.glob("*.pdf"):
        dest_dir = DEST_BASE / "shared" / "derechos"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / pdf.name
        if not dest_file.exists():
            safe_copy(pdf, dest_file)
        asset_list.append(AssetInfo(
            source_path=str(pdf),
            dest_path=str(dest_file),
            filename=pdf.name,
            brand='shared',
            model_name='DERECHOS',
            model_code='000000',
            color='N/A',
            is_derechos=True,
            size_bytes=pdf.stat().st_size if pdf.exists() else 0,
            extracted_at=datetime.now().isoformat(),
            error=""
        ))
    
    return asset_list

def generate_manifest(asset_list: List[AssetInfo]):
    """Genera manifest JSON y CSV de mapeo"""
    # JSON manifest
    manifest_path = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/asset_manifest.json")
    manifest_data = {
        "generated_at": datetime.now().isoformat(),
        "total_assets": len(asset_list),
        "successful": len([a for a in asset_list if not a.error]),
        "failed": len([a for a in asset_list if a.error]),
        "by_brand": {},
        "by_model": {},
        "assets": [asdict(a) for a in asset_list]
    }
    
    # Agrupar por marca
    for asset in asset_list:
        brand = asset.brand
        if brand not in manifest_data["by_brand"]:
            manifest_data["by_brand"][brand] = 0
        manifest_data["by_brand"][brand] += 1
        
        model_key = f"{asset.model_code}_{asset.model_name}"
        if model_key not in manifest_data["by_model"]:
            manifest_data["by_model"][model_key] = {
                "model_code": asset.model_code,
                "model_name": asset.model_name,
                "brand": asset.brand,
                "colors": set(),
                "asset_count": 0
            }
        manifest_data["by_model"][model_key]["colors"].add(asset.color)
        manifest_data["by_model"][model_key]["asset_count"] += 1
    
    # Convertir sets a lists para JSON
    for model in manifest_data["by_model"].values():
        model["colors"] = sorted(list(model["colors"]))
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"Manifest JSON guardado en: {manifest_path}")
    
    # CSV para cruce con catálogo
    csv_path = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/catalogo_con_assets.csv")
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("modelo,codigo,color,marca,asset_count,tiene_assets\n")
        for model_key, model_info in manifest_data["by_model"].items():
            if model_info["model_code"] != "000000":
                en_catalogo = "SI" if model_info["model_code"] in CATALOG_MODELS else "NO"
                f.write(f'{model_info["model_name"]},{model_info["model_code"]},'
                       f'{";".join(model_info["colors"])},{model_info["brand"]},'
                       f'{model_info["asset_count"]},{en_catalogo}\n')
    print(f"CSV mapeo guardado en: {csv_path}")
    
    # Reporte de cobertura
    models_with_assets = set(m["model_code"] for m in manifest_data["by_model"].values() if m["model_code"] != "000000")
    models_in_catalog = CATALOG_MODELS
    coverage = len(models_with_assets & models_in_catalog) / len(models_in_catalog) * 100 if models_in_catalog else 0
    
    print(f"\n=== REPORTE DE COBERTURA ===")
    print(f"Modelos en catálogo oficial: {len(models_in_catalog)}")
    print(f"Modelos con assets: {len(models_with_assets)}")
    print(f"Modelos con assets Y en catálogo: {len(models_with_assets & models_in_catalog)}")
    print(f"Cobertura: {coverage:.1f}%")
    print(f"Modelos en catálogo SIN assets: {sorted(models_in_catalog - models_with_assets)}")
    print(f"Assets de modelos NO en catálogo: {sorted(models_with_assets - models_in_catalog)}")

def main():
    print("=" * 60)
    print("ORGANIZADOR DE ASSETS FLEXI / QUIRELLI")
    print("=" * 60)
    
    # Cargar catálogo
    load_catalog_models()
    
    # Limpiar destino anterior (opcional - comentar si no se quiere borrar)
    # shutil.rmtree(DEST_BASE, ignore_errors=True)
    DEST_BASE.mkdir(parents=True, exist_ok=True)
    
    # Procesar todo
    asset_list = process_zip_files()
    
    # Generar manifestos
    generate_manifest(asset_list)
    
    print(f"\n✅ Proceso completado. Total assets procesados: {len(asset_list)}")
    print(f"   Exitosos: {len([a for a in asset_list if not a.error])}")
    print(f"   Con errores: {len([a for a in asset_list if a.error])}")
    print(f"📁 Assets organizados en: {DEST_BASE}")

if __name__ == "__main__":
    main()
