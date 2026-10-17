#!/usr/bin/env python3
"""
Script para mapear catálogo oficial con assets disponibles.
Genera reportes de cobertura y priorización.
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass

CATALOG_CSV = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/catalogo_modelos_oficiales.csv")
ASSET_MANIFEST = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/asset_manifest.json")
OUTPUT_CSV = Path("/home/universe-sent-me/growth-os/tenants/flexi/data/catalogo_con_assets.csv")
OUTPUT_REPORT = Path("/home/universe-sent-me/growth-os/tenants/flexi/docs/MAPEO_CATALOGO_ASSETS_20261014.md")

@dataclass
class CatalogEntry:
    numero: str
    modelo: str
    color: str

def load_catalog() -> List[CatalogEntry]:
    """Carga el catálogo oficial"""
    entries = []
    with open(CATALOG_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(CatalogEntry(
                numero=row.get('N.º', ''),
                modelo=row.get('Modelo', '').strip(),
                color=row.get('Color', '').strip()
            ))
    return entries

def load_manifest() -> Dict:
    """Carga el manifest de assets"""
    with open(ASSET_MANIFEST, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_color(color: str) -> str:
    """Normaliza nombres de colores para comparación"""
    return color.upper().strip().replace(' ', '_').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('Ñ', 'N')

def main():
    print("=" * 60)
    print("MAPEO CATÁLOGO ↔ ASSETS")
    print("=" * 60)
    
    # Cargar datos
    catalog = load_catalog()
    manifest = load_manifest()
    
    # Construir índice de assets por modelo
    assets_by_model = manifest.get("by_model", {})
    
    # Estadísticas
    total_catalog = len(catalog)
    matched = 0
    unmatched = 0
    partial_matches = 0
    
    # Preparar salida CSV
    rows = []
    
    # Modelos únicos en catálogo
    catalog_models = {}
    for entry in catalog:
        code = entry.modelo
        if code not in catalog_models:
            catalog_models[code] = {"colors": set(), "entries": []}
        catalog_models[code]["colors"].add(normalize_color(entry.color))
        catalog_models[code]["entries"].append(entry)
    
    print(f"\nModelos únicos en catálogo: {len(catalog_models)}")
    print(f"Modelos con assets en manifest: {len(assets_by_model)}")
    
    # Procesar cada modelo del catálogo
    for model_code, model_info in sorted(catalog_models.items()):
        catalog_colors = model_info["colors"]
        
        # Buscar en assets (por código)
        asset_key = None
        for key, info in assets_by_model.items():
            if info["model_code"] == model_code:
                asset_key = key
                break
        
        if asset_key:
            asset_info = assets_by_model[asset_key]
            asset_colors = set(normalize_color(c) for c in asset_info["colors"])
            asset_count = asset_info["asset_count"]
            brand = asset_info["brand"]
            
            # Coincidencia de colores
            matched_colors = catalog_colors & asset_colors
            missing_colors = catalog_colors - asset_colors
            extra_colors = asset_colors - catalog_colors
            
            if matched_colors:
                matched += 1
                if missing_colors:
                    partial_matches += 1
            else:
                unmatched += 1
            
            rows.append({
                "modelo": model_code,
                "nombre_asset": asset_info["model_name"],
                "marca": brand,
                "colores_catalogo": ";".join(sorted(catalog_colors)),
                "colores_assets": ";".join(sorted(asset_colors)),
                "colores_match": ";".join(sorted(matched_colors)),
                "colores_faltantes": ";".join(sorted(missing_colors)),
                "colores_extra": ";".join(sorted(extra_colors)),
                "asset_count": asset_count,
                "estado": "COMPLETO" if not missing_colors else ("PARCIAL" if matched_colors else "SOLO_ASSETS")
            })
        else:
            # Modelo en catálogo SIN assets
            unmatched += 1
            rows.append({
                "modelo": model_code,
                "nombre_asset": "SIN_ASSETS",
                "marca": "DESCONOCIDA",
                "colores_catalogo": ";".join(sorted(catalog_colors)),
                "colores_assets": "",
                "colores_match": "",
                "colores_faltantes": ";".join(sorted(catalog_colors)),
                "colores_extra": "",
                "asset_count": 0,
                "estado": "SIN_ASSETS"
            })
    
    # Modelos con assets NO en catálogo
    catalog_codes = set(catalog_models.keys())
    for key, info in assets_by_model.items():
        if info["model_code"] not in catalog_codes and info["model_code"] != "000000":
            rows.append({
                "modelo": info["model_code"],
                "nombre_asset": info["model_name"],
                "marca": info["brand"],
                "colores_catalogo": "NO_EN_CATALOGO",
                "colores_assets": ";".join(sorted(info["colors"])),
                "colores_match": "",
                "colores_faltantes": "",
                "colores_extra": ";".join(sorted(info["colors"])),
                "asset_count": info["asset_count"],
                "estado": "ASSETS_SIN_CATALOGO"
            })
    
    # Escribir CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ["modelo", "nombre_asset", "marca", "colores_catalogo", "colores_assets", 
                      "colores_match", "colores_faltantes", "colores_extra", "asset_count", "estado"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n✅ CSV generado: {OUTPUT_CSV}")
    
    # Generar reporte Markdown
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("# Reporte de Mapeo Catálogo ↔ Assets\n\n")
        f.write(f"**Fecha:** 2026-10-14\n\n")
        f.write(f"## Resumen Ejecutivo\n\n")
        f.write(f"- **Modelos en catálogo oficial:** {total_catalog} variantes ({len(catalog_models)} modelos únicos)\n")
        f.write(f"- **Modelos con assets completos:** {matched - partial_matches}\n")
        f.write(f"- **Modelos con assets parciales:** {partial_matches}\n")
        f.write(f"- **Modelos SIN assets:** {unmatched}\n")
        f.write(f"- **Modelos con assets pero NO en catálogo:** {len([r for r in rows if r['estado'] == 'ASSETS_SIN_CATALOGO'])}\n\n")
        
        f.write(f"## Modelos Listos para Producción (Completos)\n\n")
        ready = [r for r in rows if r['estado'] == 'COMPLETO']
        for r in ready:
            f.write(f"- **{r['modelo']}** ({r['nombre_asset']}) - {r['marca']} - {r['asset_count']} assets - Colores: {r['colores_catalogo']}\n")
        
        f.write(f"\n## Modelos Parciales (Faltan Colores)\n\n")
        partial = [r for r in rows if r['estado'] == 'PARCIAL']
        for r in partial:
            f.write(f"- **{r['modelo']}** ({r['nombre_asset']}) - {r['marca']} - Faltan: {r['colores_faltantes']} | Tenemos: {r['colores_match']}\n")
        
        f.write(f"\n## Modelos SIN Assets (Prioridad de Fotografía)\n\n")
        sin_assets = [r for r in rows if r['estado'] == 'SIN_ASSETS']
        for r in sin_assets:
            f.write(f"- **{r['modelo']}** - Colores necesarios: {r['colores_catalogo']}\n")
        
        f.write(f"\n## Assets de Modelos NO en Catálogo (Revisar)\n\n")
        extra = [r for r in rows if r['estado'] == 'ASSETS_SIN_CATALOGO']
        for r in extra:
            f.write(f"- **{r['modelo']}** ({r['nombre_asset']}) - {r['marca']} - {r['asset_count']} assets - Colores: {r['colores_assets']}\n")
        
        # Top 5 prioridad para producción
        f.write(f"\n## Top 5 Prioridad para Producción Inmediata\n\n")
        # Priorizar: completos, con más assets, marcas alternadas
        priority = sorted(ready, key=lambda x: -x['asset_count'])[:5]
        for i, r in enumerate(priority, 1):
            f.write(f"{i}. **{r['modelo']}** ({r['nombre_asset']}) - {r['marca'].capitalize()} - {r['asset_count']} assets - {r['colores_catalogo']}\n")
    
    print(f"✅ Reporte generado: {OUTPUT_REPORT}")
    print(f"\n📊 Resumen:")
    print(f"   Completos: {matched - partial_matches}")
    print(f"   Parciales: {partial_matches}")
    print(f"   Sin assets: {unmatched}")
    print(f"   Assets sin catálogo: {len(extra)}")

if __name__ == "__main__":
    main()
