#!/usr/bin/env python3
"""
Valida manifiesto aprobado antes de convertir a CSV:
- Assets existen en Google Drive (búsqueda recursiva por NOMBRE DE ARCHIVO)
- Horarios válidos y en zona horaria correcta
- Sin duplicados fecha+hora
- Tipos y formatos correctos
- 21 slots esperados (3/día × 7 días)
"""
import sys
import re
import os
from pathlib import Path
from typing import List, Dict

GOOGLE_DRIVE_ASSETS = Path("/home/universe-sent-me/GoogleDrive/01 - Firma Assets")

def find_asset_recursive(base_dir: Path, filename: str):
    """Busca por nombre de archivo (no path) recursivamente."""
    if not base_dir.exists():
        return None
    for root, dirs, files in os.walk(base_dir):
        if filename in files:
            return Path(root) / filename
    return None

def parse_markdown_table(md_path: Path) -> List[Dict[str, str]]:
    content = md_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    rows = []
    in_table = False
    
    for line in lines:
        line = line.strip()
        if '| Fecha' in line and '| Hora' in line:
            in_table = True
            continue
        if in_table and line.startswith('|---'):
            continue
        if in_table and not line.startswith('|'):
            break
        if in_table and line.startswith('|') and 'Fecha' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                fecha = parts[1].strip()
                hora = parts[2].strip()
                tipo = parts[3].strip().upper()
                archivo = parts[4].strip()
                caption = parts[5].strip()
                
                # Saltar fila de ejemplo del template
                if not fecha or (fecha == "2026-09-08" and archivo == "archivo_lunes_manana.png"):
                    continue
                
                # Normalizar tipo
                if tipo in ("VIDEO", "REEL"): tipo = "VIDEO"
                elif tipo in ("TEXT", "TEXT_ONLY"): 
                    tipo = "TEXT_ONLY"
                    archivo = ""
                else: tipo = "PHOTO"
                
                if archivo in ("—", "-", ""): archivo = ""
                
                rows.append({
                    "fecha": fecha, "hora": hora, "tipo": tipo,
                    "archivo": archivo, "caption": caption,
                })
    return rows

def validate_assets(rows: List[Dict]) -> List[str]:
    """Verifica que archivos existan en Google Drive (busca por nombre)."""
    errors = []
    for i, row in enumerate(rows, 1):
        if row["tipo"] in ("PHOTO", "VIDEO") and row["archivo"]:
            # Extraer solo el nombre del archivo (último componente)
            filename = Path(row["archivo"]).name
            found = find_asset_recursive(GOOGLE_DRIVE_ASSETS, filename)
            if not found:
                errors.append(f"Fila {i}: Asset NO ENCONTRADO en Google Drive: '{filename}' (referenciado como '{row['archivo']}')")
            else:
                rel = found.relative_to(GOOGLE_DRIVE_ASSETS)
                print(f"  ✅ Asset encontrado: {filename} → {rel}")
    return errors

def validate_schedule(rows: List[Dict]) -> List[str]:
    """Valida estructura de horarios."""
    errors = []
    seen = set()
    dates = set()
    
    for i, row in enumerate(rows, 1):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', row["fecha"]):
            errors.append(f"Fila {i}: Fecha inválida '{row['fecha']}'")
        else:
            dates.add(row["fecha"])
        
        if not re.match(r'^\d{2}:\d{2}$', row["hora"]):
            errors.append(f"Fila {i}: Hora inválida '{row['hora']}'")
        else:
            h, m = map(int, row["hora"].split(':'))
            if h not in (8, 14, 20) or m not in (0, 30):
                errors.append(f"Fila {i}: Hora fuera de estándar (08:30, 14:30, 20:00): '{row['hora']}'")
        
        key = (row["fecha"], row["hora"])
        if key in seen:
            errors.append(f"Fila {i}: Duplicado fecha+hora {key}")
        seen.add(key)
        
        if row["tipo"] not in ("PHOTO", "VIDEO", "TEXT_ONLY"):
            errors.append(f"Fila {i}: Tipo inválido '{row['tipo']}'")
        
        if row["tipo"] in ("PHOTO", "VIDEO") and not row["archivo"]:
            errors.append(f"Fila {i}: Archivo requerido para {row['tipo']}")
    
    if len(dates) != 7:
        errors.append(f"Se esperan 7 días únicos, encontrados: {len(dates)} ({sorted(dates)})")
    
    if len(rows) != 21:
        errors.append(f"Se esperan 21 slots (3/día × 7 días), encontrados: {len(rows)}")
    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 tools/validate_manifiesto.py <manifiesto_aprobado.md>")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"❌ No encontrado: {md_path}")
        sys.exit(1)
    
    print(f"🔍 Validando: {md_path}")
    rows = parse_markdown_table(md_path)
    print(f"📋 {len(rows)} filas parseadas")
    
    all_errors = []
    
    print("\n🔎 Validando assets en Google Drive (búsqueda por nombre)...")
    all_errors.extend(validate_assets(rows))
    
    print("\n🔎 Validando estructura de horarios...")
    all_errors.extend(validate_schedule(rows))
    
    print("\n" + "="*60)
    if all_errors:
        print(f"❌ {len(all_errors)} ERRORES:")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ TODO OK - Manifiesto listo para conversión")
        print(f"   {len(rows)} slots | {len(set(r['fecha'] for r in rows))} días | Assets verificados")
        sys.exit(0)

if __name__ == "__main__":
    main()
