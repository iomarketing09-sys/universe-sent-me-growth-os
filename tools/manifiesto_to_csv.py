#!/usr/bin/env python3
"""
Convierte manifiesto Markdown (tabla) → meta_import.csv oficial
Uso: python3 tools/manifiesto_to_csv.py tenants/firma-bordados/docs/Manifiestos_Semanales/manifiesto_aprobado_20260908.md
"""
import sys
import csv
import re
from pathlib import Path
from typing import List, Dict, Any

# Constantes oficiales
WHATSAPP = "878 788 0735"
WHATSAPP_E164 = "5218787880735"
HASHTAGS = "#FirmaBordados #BordadoPersonalizado #UniformesCorporativos #PiedrasNegras #EaglePass #Bordados #Embroidery"
LOCATION = "Piedras Negras, Coahuila, México"
LINK_URL = f"https://wa.me/{WHATSAPP_E164}"
FIRST_COMMENT = f"Cotiza por WhatsApp: {WHATSAPP}"
TIMEZONE = "America/Matamoros"

# Columnas CSV de salida
FIELDNAMES = [
    "Date (YYYY-MM-DD)", "Time (HH:MM, 24h)", "Timezone", "Post Type",
    "Media URL", "Caption", "Link URL", "Hashtags", "Location", "First Comment"
]

def parse_markdown_table(md_path: Path) -> List[Dict[str, str]]:
    """Extrae filas de la tabla Markdown del manifiesto."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    
    rows = []
    in_table = False
    
    for line in lines:
        line = line.strip()
        
        # Detectar inicio de tabla (línea con | Fecha | Hora |)
        if '| Fecha' in line and '| Hora' in line:
            in_table = True
            continue
        
        # Detectar separador de tabla (---)
        if in_table and line.startswith('|---'):
            continue
        
        # Fin de tabla
        if in_table and not line.startswith('|'):
            break
        
        # Procesar fila de datos
        if in_table and line.startswith('|') and 'Fecha' not in line:
            # Split por | y limpiar
            parts = [p.strip() for p in line.split('|')]
            # parts[0] está vacío por el | inicial, parts[-1] vacío por | final
            if len(parts) >= 6:
                fecha = parts[1].strip()
                hora = parts[2].strip()
                tipo = parts[3].strip().upper()
                archivo = parts[4].strip()
                caption = parts[5].strip()
                
                # Saltar filas vacías o de ejemplo
                if not fecha or fecha == "2026-09-08" and archivo == "archivo_lunes_manana.png":
                    continue  # Saltar fila de ejemplo del template
                
                # Normalizar tipo
                if tipo in ("VIDEO", "REEL"):
                    tipo = "VIDEO"
                elif tipo in ("TEXT", "TEXT_ONLY"):
                    tipo = "TEXT_ONLY"
                    archivo = ""
                else:
                    tipo = "PHOTO"
                
                # Si archivo es "—" o vacío, dejarlo vacío
                if archivo in ("—", "-", ""):
                    archivo = ""
                
                rows.append({
                    "fecha": fecha,
                    "hora": hora,
                    "tipo": tipo,
                    "archivo": archivo,
                    "caption": caption,
                })
    
    return rows

def validate_rows(rows: List[Dict]) -> List[str]:
    """Valida filas y retorna lista de warnings/errores."""
    errors = []
    seen = set()
    
    for i, row in enumerate(rows, 1):
        # Validar fecha
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', row["fecha"]):
            errors.append(f"Fila {i}: Fecha inválida '{row['fecha']}' (esperado YYYY-MM-DD)")
        
        # Validar hora
        if not re.match(r'^\d{2}:\d{2}$', row["hora"]):
            errors.append(f"Fila {i}: Hora inválida '{row['hora']}' (esperado HH:MM)")
        
        # Validar tipo
        if row["tipo"] not in ("PHOTO", "VIDEO", "TEXT_ONLY"):
            errors.append(f"Fila {i}: Tipo inválido '{row['tipo']}' (PHOTO|VIDEO|TEXT_ONLY)")
        
        # Validar archivo para PHOTO/VIDEO
        if row["tipo"] in ("PHOTO", "VIDEO") and not row["archivo"]:
            errors.append(f"Fila {i}: Archivo requerido para {row['tipo']}")
        
        # Validar caption no vacío
        if not row["caption"] or len(row["caption"]) < 10:
            errors.append(f"Fila {i}: Caption muy corto o vacío")
        
        # Detectar duplicados fecha+hora
        key = (row["fecha"], row["hora"])
        if key in seen:
            errors.append(f"Fila {i}: Duplicado fecha+hora {key}")
        seen.add(key)
    
    return errors

def write_meta_import_csv(rows: List[Dict], output_path: Path):
    """Escribe meta_import.csv con formato oficial."""
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        
        for row in rows:
            writer.writerow({
                "Date (YYYY-MM-DD)": row["fecha"],
                "Time (HH:MM, 24h)": row["hora"],
                "Timezone": TIMEZONE,
                "Post Type": row["tipo"],
                "Media URL": row["archivo"],
                "Caption": row["caption"],
                "Link URL": LINK_URL,
                "Hashtags": HASHTAGS,
                "Location": LOCATION,
                "First Comment": FIRST_COMMENT,
            })

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 tools/manifiesto_to_csv.py <manifiesto_aprobado.md> [output.csv]")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"❌ Archivo no encontrado: {md_path}")
        sys.exit(1)
    
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("tenants/firma-bordados/meta_import.csv")
    
    print(f"📖 Leyendo: {md_path}")
    rows = parse_markdown_table(md_path)
    
    if not rows:
        print("❌ No se encontraron filas válidas en la tabla")
        sys.exit(1)
    
    print(f"📋 {len(rows)} filas parseadas")
    
    # Validar
    errors = validate_rows(rows)
    if errors:
        print("\n⚠️  ERRORES DE VALIDACIÓN:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    
    print("✅ Validación OK")
    
    # Escribir CSV
    write_meta_import_csv(rows, output_path)
    print(f"✅ meta_import.csv generado: {output_path}")
    
    # Resumen
    print("\n--- RESUMEN ---")
    for r in rows:
        print(f"  {r['fecha']} {r['hora']} | {r['tipo']:10} | {r['archivo'] or '—':40} | {r['caption'][:60]}...")

if __name__ == "__main__":
    main()
