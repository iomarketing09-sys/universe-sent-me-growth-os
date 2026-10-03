#!/usr/bin/env python3
"""
Auto-despacho nocturno de planes desde Google Drive montado.
Ejecución diaria a las 8:00 PM (20:00 hora frontera).
100% Librería estándar de Python (soporta .xlsx y .csv en montajes FUSE/rclone).
"""
import sys
import os
import io
import csv
import glob
import argparse
import logging
import zipfile
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

# Rutas del sistema
GROWTH_OS_ROOT = Path("/home/universe-sent-me/growth-os")
TENANT_DIR = GROWTH_OS_ROOT / "tenants/universe"
GDRIVE_GROWTH_OS = Path("/home/universe-sent-me/GoogleDrive/Growth OS")
IMPORTS_DIR = TENANT_DIR / "imports"
LOGS_DIR = TENANT_DIR / "logs"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
IMPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "nightly_deploy.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def get_target_date(args_date: str = None) -> tuple[str, str]:
    """Retorna (YYYYMMDD, YYYY-MM-DD). Por defecto calcula el día siguiente."""
    if args_date:
        dt = datetime.strptime(args_date, "%Y-%m-%d")
    else:
        dt = datetime.now() + timedelta(days=1)
    return dt.strftime("%Y%m%d"), dt.strftime("%Y-%m-%d")

def find_plan_file(date_compact: str) -> Path | None:
    """Busca el archivo de plan en la carpeta de Drive montada."""
    patterns = [
        f"*Plan_Universe_Sent_Me_{date_compact}*.xlsx",
        f"*Plan_Universe_Sent_Me_{date_compact}*.csv",
        f"*Plan_Universe_Sent_Me_{date_compact}*"
    ]
    for pattern in patterns:
        matches = [p for p in GDRIVE_GROWTH_OS.glob(pattern) if p.is_file()]
        if matches:
            return matches[0]
    return None

def format_excel_time(val: str) -> str:
    """Convierte fracciones decimales de tiempo de Excel (ej: 0.41666) a HH:MM."""
    val = str(val).strip()
    if ":" in val:
        return val
    try:
        f = float(val)
        total_minutes = int(round(f * 24 * 60))
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
    except ValueError:
        return val

def parse_xlsx(path: Path) -> list[dict]:
    """Lee un archivo .xlsx cargando los bytes en memoria (compatible con FUSE/rclone)."""
    with open(path, "rb") as f:
        file_bytes = f.read()

    with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
        shared_strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            tree = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in tree.findall(".//{*}si"):
                text = "".join([t.text for t in si.findall(".//{*}t") if t.text])
                shared_strings.append(text)

        sheet_xml = z.read("xl/worksheets/sheet1.xml")
        tree = ET.fromstring(sheet_xml)

        rows_data = []
        for r_elem in tree.findall(".//{*}row"):
            row_dict = {}
            for c_elem in r_elem.findall("{*}c"):
                ref = c_elem.attrib.get("r", "")
                col_match = re.match(r"([A-Z]+)", ref)
                col_letter = col_match.group(1) if col_match else ""

                t_attr = c_elem.attrib.get("t")
                v_el = c_elem.find("{*}v")
                val = v_el.text if v_el is not None else ""

                if t_attr == "s" and val.isdigit():
                    idx = int(val)
                    val = shared_strings[idx] if idx < len(shared_strings) else val
                elif t_attr == "inlineStr":
                    is_el = c_elem.find("{*}is")
                    if is_el is not None:
                        val = "".join([t.text for t in is_el.findall(".//{*}t") if t.text])
                row_dict[col_letter] = val
            if row_dict:
                rows_data.append(row_dict)

        if not rows_data:
            return []

        header_row = rows_data[0]
        def col_key(c): return (len(c), c)
        sorted_cols = sorted(header_row.keys(), key=col_key)
        headers = [header_row[c].strip() for c in sorted_cols]

        result_dicts = []
        for r in rows_data[1:]:
            item = {}
            for c, h in zip(sorted_cols, headers):
                item[h] = r.get(c, "")
            result_dicts.append(item)
        return result_dicts

def read_plan_rows(plan_path: Path) -> list[dict]:
    """Carga las filas del plan ya sea desde .xlsx o .csv."""
    if plan_path.suffix.lower() == ".xlsx":
        return parse_xlsx(plan_path)
    else:
        with open(plan_path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

def main():
    parser = argparse.ArgumentParser(description="Despachador automático nocturno desde Drive")
    parser.add_argument("--date", help="Fecha objetivo YYYY-MM-DD (por defecto mañana)", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Ejecuta en modo de prueba sin publicar")
    args = parser.parse_args()

    compact_date, iso_date = get_target_date(args.date)
    logging.info(f"=== Iniciando revisión de plan para fecha: {iso_date} ({compact_date}) ===")

    # Candado 1: Idempotencia (evitar reprogramar si ya se procesó)
    lock_marker = IMPORTS_DIR / f".dispatched_{compact_date}.lock"
    if lock_marker.exists() and not args.dry_run:
        logging.info(f"[SKIP] El plan para {iso_date} ya fue despachado previamente (lock file presente).")
        return

    # Buscar archivo en Drive montado
    plan_path = find_plan_file(compact_date)
    if not plan_path:
        logging.warning(f"[AVISO] No se encontró ningún archivo de plan para {iso_date} en {GDRIVE_GROWTH_OS}.")
        return

    logging.info(f"Plan encontrado en Drive: {plan_path.name}")

    try:
        rows = read_plan_rows(plan_path)
    except Exception as e:
        logging.error(f"Error al leer {plan_path}: {e}")
        return

    if not rows or "Estado" not in rows[0]:
        logging.error("El archivo está vacío o no contiene la columna 'Estado'. Abortando por seguridad.")
        return

    # Candado 2: Filtro de Aprobación Humana
    approved_rows = [r for r in rows if r.get("Estado", "").strip().upper() == "APROBADO"]
    if not approved_rows:
        logging.warning(f"[PAUSA] El plan {plan_path.name} existe pero no tiene filas con Estado 'APROBADO'.")
        return

    logging.info(f"Filas aprobadas para programar: {len(approved_rows)} de {len(rows)}")

    # Convertir al schema canonical del Meta Bulk Uploader
    canonical_fieldnames = [
        "Date (YYYY-MM-DD)",
        "Time (HH:MM, 24h)",
        "Timezone",
        "Post Type",
        "Media URL",
        "Caption",
        "Link URL",
        "Hashtags",
        "Location",
        "First Comment"
    ]

    local_csv_path = IMPORTS_DIR / f"meta_import_{iso_date}.csv"
    try:
        with open(local_csv_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=canonical_fieldnames)
            writer.writeheader()
            for r in approved_rows:
                writer.writerow({
                    "Date (YYYY-MM-DD)": iso_date,
                    "Time (HH:MM, 24h)": format_excel_time(r.get("Hora", "")),
                    "Timezone": "America/Matamoros",
                    "Post Type": "PHOTO",
                    "Media URL": Path(r.get("Archivo", "").strip()).name,
                    "Caption": r.get("Caption", "").strip(),
                    "Link URL": "",
                    "Hashtags": "",
                    "Location": "",
                    "First Comment": ""
                })
        logging.info(f"CSV canonical generado localmente: {local_csv_path}")
    except Exception as e:
        logging.error(f"Error al escribir CSV local: {e}")
        return

    # Invocar deploy_universe.py
    deploy_cmd = [
        sys.executable,
        str(GROWTH_OS_ROOT / "deploy_universe.py"),
        str(local_csv_path)
    ]
    if not args.dry_run:
        deploy_cmd.append("--live")

    logging.info(f"Ejecutando comando: {' '.join(deploy_cmd)}")
    result = subprocess.run(deploy_cmd, cwd=GROWTH_OS_ROOT)

    if result.returncode == 0:
        logging.info(f"✅ Despacho exitoso para {iso_date}.")
        # Alerta de Monetización para posts programados
        for r in approved_rows:
            cat = str(r.get("Categoria", "")).lower()
            if "monetiz" in cat:
                archivo = r.get("Archivo", "").strip()
                hora = r.get("Hora", "")
                logging.info("")
                logging.info("=" * 65)
                logging.info("💰 ALERTA DE MONETIZACIÓN DETECTADA (Meta Business Suite)")
                logging.info("=" * 65)
                logging.info(f"📌 Pieza programada: {archivo}")
                logging.info(f"⏰ Hora programada: {hora}")
                logging.info("🎯 Acción: Meta Business Suite > Programadas > Agregar producto de afiliación")
                
                archivo_low = archivo.lower()
                if "silvio" in archivo_low:
                    logging.info("🛒 Producto Sugerido: Diario Journaling / Afirmaciones (Silvio)")
                    logging.info("🔗 Enlace Afiliado: https://meli.la/1PsJGQa")
                    logging.info("🌐 URL Canónica: https://articulo.mercadolibre.com.mx/MLM-3721321142")
                elif "ganso" in archivo_low:
                    logging.info("🛒 Producto Sugerido: Cafetera Prensa Francesa (Ganso) | Tag: wilfred210926prensatop1")
                    logging.info("🌐 URL Canónica: https://articulo.mercadolibre.com.mx/MLM-1927515901")
                elif "wilfred" in archivo_low:
                    logging.info("🛒 Producto Sugerido: Tetera Hierro / Vela Cedro / Marco Aurelio (Wilfred)")
                elif "evan" in archivo_low:
                    logging.info("🛒 Producto Sugerido: Antifaz 3D / Sunset Lamp (Evan)")
                elif "universe" in archivo_low:
                    logging.info("🛒 Producto Sugerido: Difusor de Aromas Nebulosa (Universe)")
                logging.info("=" * 65)
                logging.info("")

        if not args.dry_run:
            lock_marker.touch()
    else:
        logging.error(f"❌ Error durante el despacho de deploy_universe.py (código {result.returncode}).")

if __name__ == "__main__":
    main()
