"""
Generador de CSV de importación para Meta Business Suite.
LOCAL/OFFLINE - sin llamadas a API.
"""
from pathlib import Path
import json
import csv
from datetime import datetime, timezone


TENANT_DIR = Path(__file__).resolve().parent
DRYRUN_PATH = Path(__file__).resolve().parents[2] / "dryrun_output.json"
OUTPUT_PATH = TENANT_DIR / "meta_import.csv"

# Hashtags base para Firma Bordados
HASHTAGS = [
    "#FirmaBordados",
    "#BordadoPersonalizado",
    "#UniformesCorporativos",
    "#PiedrasNegras",
    "#EaglePass",
    "#Bordados",
    "#Embroidery"
]

# Copies base por tipo de contenido
COPY_TEMPLATES = {
    "lunes_detalle_uniforme": "Detalle de uniforme personalizado. Calidad en cada puntada. 🧵\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "img_wa_0003": "Trabajo real de nuestro taller. Cada prenda cuenta una historia. 🧵\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "video_20_anos": "¡20 años bordando en Piedras Negras! 🎉 Dos décadas de calidad, confianza y dedicación.\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "calidad_logo_bordado": "La calidad del logo bordado habla por sí sola. Detalle, precisión y durabilidad. 🧵\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "miercoles_nombres_bordados": "Nombres bordados para identificar y cuidar cada prenda. Práctico y profesional. 🎒\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "fb_img_1787256185059": "Uniformes corporativos que proyectan profesionalismo. Tu marca bien representada. 👔\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "fb_img_1787256197738": "Equipos identificados, imagen unificada. Bordado corporativo de calidad. 👔\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "iniciales_monogramas": "Iniciales y monogramas: personalización discreta y elegante para regalos o uso personal. ✨\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "jueves_que_personalizarias": "¿Qué personalizarías hoy? Logo, nombre, monograma... tú eliges, nosotros bordamos. 🧵\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "file_catalog_myo": "Catálogo MyO disponible. Descubre opciones para tu negocio. 📋\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "fb_img_1787256161650": "Trabajo real: detalle de bordado en prenda terminada. Calidad que se ve y se siente. 🧵\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "sabado_etiqueta_negocio_local": "¡Etiqueta a un negocio local que merece uniformes personalizados! 👇\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "guia_pedido": "Guía rápida para hacer tu pedido: 1) Elige prenda 2) Define diseño 3) Cotiza por WhatsApp. 📋\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "firma_bordados_reel": "Una semana de bordados, una semana de detalles que representan a cada cliente. 🧵\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "domingo_agenda_pedido_v2": "Agenda tu pedido para la próxima semana. Cupos limitados. 📅\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    # Text-only slots
    "text_motivacional": "La calidad se cose puntada a puntada. ✨\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "text_interaccion": "¿Qué prenda te gustaría ver bordada la próxima semana? Comenta abajo 👇\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "text_cierre_semana": "Gracias por confiar en Firma Bordados esta semana. ¡Nos vemos la próxima! 🧵\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
    "text_agenda": "Agenda abierta para la próxima semana. Escríbenos y aparta tu espacio. 📅\n\n📍 Piedras Negras, Coahuila\n📱 Cotiza por WhatsApp: 878 788 0735",
}


def get_copy_for_asset(asset_ref: str, slot_type: str, day: str, slot_name: str) -> str:
    """Obtiene el copy apropiado para el asset/slot."""
    if slot_type == "text":
        # Text-only slots según día y horario
        if day == "saturday" and slot_name == "afternoon":
            return COPY_TEMPLATES["text_motivacional"]
        elif day == "sunday" and slot_name == "morning":
            return COPY_TEMPLATES["text_interaccion"]
        elif day == "sunday" and slot_name == "afternoon":
            return COPY_TEMPLATES["text_cierre_semana"]
        elif day == "sunday" and slot_name == "evening":
            return COPY_TEMPLATES["text_agenda"]
        return COPY_TEMPLATES["text_motivacional"]
    
    return COPY_TEMPLATES.get(asset_ref, COPY_TEMPLATES["text_motivacional"])


def generate_meta_csv() -> int:
    """Genera el CSV para Meta Business Suite."""
    with DRYRUN_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    schedule = data["schedule"]
    
    # Columnas compatibles con Meta Business Suite CSV import
    fieldnames = [
        "Date (YYYY-MM-DD)",
        "Time (HH:MM, 24h)",
        "Timezone",
        "Post Type",
        "Media URL",  # ruta local al archivo
        "Caption",
        "Link URL",
        "Hashtags",
        "Location",
        "First Comment",
    ]
    
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for slot in schedule:
            date_local = slot["date_local"]
            time_local = slot["time_local"]
            slot_type = slot["slot_type"]
            asset_ref = slot.get("asset_ref")
            day = slot["day"]
            
            # Determinar slot_name para copy
            hour = int(time_local.split(":")[0])
            if hour < 12:
                slot_name = "morning"
            elif hour < 18:
                slot_name = "afternoon"
            else:
                slot_name = "evening"
            
            # Copy con WhatsApp y hashtags
            copy = get_copy_for_asset(asset_ref or "", slot_type, day, slot_name)
            full_copy = f"{copy}\n\n{' '.join(HASHTAGS)}"
            
            # Media URL (ruta relativa al root del drive)
            if slot_type == "media" and asset_ref:
                source_path = slot.get("source_path") or ""
                source_filename = slot.get("source_filename") or ""
                if source_path:
                    media_url = f"{source_path}{source_filename}"
                else:
                    media_url = source_filename
            else:
                media_url = ""
            
            # Post type para Meta
            post_type = "VIDEO" if slot_type == "media" and (asset_ref and "video" in asset_ref.lower() or (slot.get("source_filename") or "").endswith(".mp4")) else "PHOTO"
            if slot_type == "text":
                post_type = "TEXT_ONLY"
            
            row = {
                "Date (YYYY-MM-DD)": date_local,
                "Time (HH:MM, 24h)": time_local,
                "Timezone": "America/Matamoros",
                "Post Type": post_type,
                "Media URL": media_url,
                "Caption": full_copy,
                "Link URL": f"https://wa.me/5218787880735",
                "Hashtags": " ".join(HASHTAGS),
                "Location": "Piedras Negras, Coahuila, México",
                "First Comment": "Cotiza por WhatsApp: 878 788 0735",
            }
            writer.writerow(row)
    
    print(f"✅ CSV generado: {OUTPUT_PATH}")
    print(f"📊 {len(schedule)} filas escritas")
    return len(schedule)


if __name__ == "__main__":
    generate_meta_csv()
