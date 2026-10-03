"""
Dry-run para generar payloads OmniRoute desde el manifest determinístico.

Genera 20 slots (16 media + 4 texto) para la semana 31 ago - 6 sep 2026.
Incluye tenant isolation (firma-bordados), UTC timestamps y WhatsApp 878 788 0735.
"""
from pathlib import Path
from typing import Dict, Any, List
import json
from datetime import datetime, timezone, timedelta

from growth.asset_resolver import load_manifest


TENANT_ID = "firma-bordados"
WHATSAPP_NUMBER = "878 788 0735"
WHATSAPP_CLEAN = "5218787880735"  # formato E.164 México

# Semana objetivo: 31 agosto - 6 septiembre 2026
WEEK_START = datetime(2026, 8, 31, 0, 0, 0, tzinfo=timezone.utc)
WEEK_END = datetime(2026, 9, 6, 23, 59, 59, tzinfo=timezone.utc)

# Slots diarios (horarios locales CDMX = UTC-5, convertidos a UTC)
# 08:30 local = 13:30 UTC
# 14:00 local = 19:00 UTC
# 19:30 local = 00:30 UTC (día siguiente)
DAILY_SLOTS_LOCAL = [
    ("morning", 8, 30),    # 08:30
    ("afternoon", 14, 0),  # 14:00
    ("evening", 19, 30),   # 19:30
]

# Offset CDMX a UTC (CDMX = UTC-5 en agosto)
CDMX_OFFSET = timedelta(hours=5)


def local_to_utc(local_dt: datetime) -> datetime:
    """Convierte datetime local CDMX a UTC."""
    return local_dt + CDMX_OFFSET


def generate_week_schedule() -> List[Dict[str, Any]]:
    """
    Genera el schedule completo de 20 slots para la semana.
    16 media (del manifest) + 4 texto = 20 total
    """
    manifest = load_manifest()
    assets = manifest.get("assets", [])
    constraints = manifest.get("business_constraints", {})
    
    # Mapear assets por día (basado en asset_ref)
    day_assets = {
        "monday": ["lunes_detalle_uniforme", "img_wa_0003", "video_20_anos"],
        "tuesday": ["calidad_logo_bordado", "fb_img_1787256185059", "fb_img_1787256197738"],
        "wednesday": ["miercoles_nombres_bordados", "iniciales_monogramas", "fb_img_1787256206553"],
        "thursday": ["jueves_que_personalizarias", "file_catalog_myo", "fb_img_1787256161650"],
        "friday": ["sabado_etiqueta_negocio_local", "guia_pedido", "firma_bordados_reel"],
        "saturday": ["domingo_agenda_pedido_v2"],  # 1 media
        "sunday": [],  # sin media
    }
    
    # Texto slots: total 4 = sábado 1 + domingo 3
    text_slots = {
        "monday": 0,
        "tuesday": 0,
        "wednesday": 0,
        "thursday": 0,
        "friday": 0,
        "saturday": 1,  # 1 texto
        "sunday": 3,    # 3 texto
    }
    
    day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    schedule = []
    slot_counter = 0
    
    for day_idx, day_name in enumerate(day_names):
        base_date = WEEK_START + timedelta(days=day_idx)
        
        media_refs = day_assets.get(day_name, [])
        media_count = len(media_refs)
        text_count = text_slots.get(day_name, 0)
        total_slots = media_count + text_count
        
        for slot_idx in range(total_slots):
            slot_type = "media" if slot_idx < media_count else "text"
            asset_ref = media_refs[slot_idx] if slot_type == "media" else None
            
            slot_name, hour, minute = DAILY_SLOTS_LOCAL[slot_idx]
            local_dt = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            utc_dt = local_to_utc(local_dt)
            
            slot_counter += 1
            slot_id = f"{TENANT_ID}-{utc_dt.strftime('%Y%m%d')}-{slot_name}-{slot_counter:02d}"
            
            asset_info = None
            if asset_ref:
                for a in assets:
                    if a["asset_ref"] == asset_ref:
                        asset_info = a
                        break
            
            payload = {
                "tenant_id": TENANT_ID,
                "slot_id": slot_id,
                "slot_type": slot_type,
                "day": day_name,
                "date_local": base_date.strftime("%Y-%m-%d"),
                "time_local": f"{hour:02d}:{minute:02d}",
                "datetime_utc": utc_dt.isoformat(),
                "datetime_local": local_dt.isoformat(),
                "whatsapp_number": WHATSAPP_NUMBER,
                "whatsapp_e164": WHATSAPP_CLEAN,
                "contact_channel": constraints.get("contact_channel", "WhatsApp"),
                "excluded_categories": constraints.get("excluded_categories", []),
            }
            
            if asset_info:
                payload.update({
                    "asset_ref": asset_info["asset_ref"],
                    "source_filename": asset_info["source_filename"],
                    "source_file_key": asset_info["source_file_key"],
                    "source_path": asset_info.get("source_path"),
                    "description": asset_info.get("description", ""),
                    "confidence": asset_info.get("confidence", "DETERMINISTIC"),
                })
            else:
                payload.update({
                    "asset_ref": None,
                    "source_filename": None,
                    "source_file_key": None,
                    "source_path": None,
                    "description": f"Texto programado - {day_name} {slot_name}",
                    "confidence": "TEXT_ONLY",
                })
            
            schedule.append(payload)
    
    return schedule


def validate_payloads(schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Valida que todos los payloads sean correctos para OmniRoute."""
    errors = []
    warnings = []
    
    for i, payload in enumerate(schedule):
        required_fields = [
            "tenant_id", "slot_id", "slot_type", "day", "date_local",
            "time_local", "datetime_utc", "whatsapp_number", "whatsapp_e164"
        ]
        for field in required_fields:
            if field not in payload:
                errors.append(f"Slot {i}: campo requerido faltante: {field}")
        
        if payload.get("tenant_id") != TENANT_ID:
            errors.append(f"Slot {i}: tenant_id incorrecto: {payload.get('tenant_id')}")
        
        if payload.get("whatsapp_number") != WHATSAPP_NUMBER:
            warnings.append(f"Slot {i}: whatsapp_number distinto al configurado")
        
        try:
            datetime.fromisoformat(payload["datetime_utc"].replace("Z", "+00:00"))
        except (ValueError, KeyError):
            errors.append(f"Slot {i}: datetime_utc inválido: {payload.get('datetime_utc')}")
        
        excluded = payload.get("excluded_categories", [])
        if "parches" not in excluded or "gorras" not in excluded:
            warnings.append(f"Slot {i}: excluded_categories no incluye parches/gorras")
    
    media_count = sum(1 for p in schedule if p["slot_type"] == "media")
    text_count = sum(1 for p in schedule if p["slot_type"] == "text")
    
    return {
        "valid": len(errors) == 0,
        "total_slots": len(schedule),
        "media_slots": media_count,
        "text_slots": text_count,
        "errors": errors,
        "warnings": warnings,
    }


def dry_run() -> Dict[str, Any]:
    """Ejecuta el dry-run completo."""
    print(f"🔍 DRY-RUN OmniRoute - Tenant: {TENANT_ID}")
    print(f"📅 Semana: {WEEK_START.strftime('%Y-%m-%d')} a {WEEK_END.strftime('%Y-%m-%d')}")
    print(f"📱 WhatsApp: {WHATSAPP_NUMBER}")
    print("-" * 60)
    
    schedule = generate_week_schedule()
    validation = validate_payloads(schedule)
    
    print(f"✅ Slots totales: {validation['total_slots']}")
    print(f"   📸 Media: {validation['media_slots']}")
    print(f"   📝 Texto: {validation['text_slots']}")
    
    if validation["errors"]:
        print(f"❌ Errores: {len(validation['errors'])}")
        for e in validation["errors"]:
            print(f"   - {e}")
    else:
        print("✅ Validación: PASÓ")
    
    if validation["warnings"]:
        print(f"⚠️  Advertencias: {len(validation['warnings'])}")
        for w in validation["warnings"]:
            print(f"   - {w}")
    
    print("-" * 60)
    print("📋 Muestra de payloads (primeros 3):")
    for payload in schedule[:3]:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print()
    
    return {
        "tenant_id": TENANT_ID,
        "week_start": WEEK_START.isoformat(),
        "week_end": WEEK_END.isoformat(),
        "whatsapp_number": WHATSAPP_NUMBER,
        "business_constraints": {
            "excluded_categories": ["parches", "gorras"],
            "contact_channel": "WhatsApp"
        },
        "schedule": schedule,
        "validation": validation
    }


if __name__ == "__main__":
    result = dry_run()
    
    output_path = Path(__file__).resolve().parents[1] / "dryrun_output.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultado completo guardado en: {output_path}")
    
    exit(0 if result["validation"]["valid"] else 1)
