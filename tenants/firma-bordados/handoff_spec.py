"""
Generador de handoff_spec.md para el equipo operativo.
LOCAL/OFFLINE - documentación técnica completa.
"""
from pathlib import Path
import json
from datetime import datetime, timezone


TENANT_DIR = Path(__file__).resolve().parent
DRYRUN_PATH = Path(__file__).resolve().parents[2] / "dryrun_output.json"
MANIFEST_PATH = TENANT_DIR / "assets_manifest.json"
CONFIG_PATH = TENANT_DIR / "config.json"
META_CSV_PATH = TENANT_DIR / "meta_import.csv"
OUTPUT_PATH = TENANT_DIR / "handoff_spec.md"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_handoff_spec() -> None:
    dryrun = load_json(DRYRUN_PATH)
    manifest = load_json(MANIFEST_PATH)
    config = load_json(CONFIG_PATH)
    
    schedule = dryrun["schedule"]
    business_constraints = dryrun["business_constraints"]
    
    now = datetime.now(timezone.utc).isoformat()
    
    lines = []
    lines.append("# Handoff Spec — Firma Bordados")
    lines.append("")
    lines.append(f"**Generado:** {now}")
    lines.append(f"**Tenant:** {dryrun['tenant_id']}")
    lines.append(f"**Cliente:** {config.get('client_name', 'Firma Bordados')}")
    lines.append(f"**Semana:** {dryrun['week_start'][:10]} a {dryrun['week_end'][:10]}")
    lines.append("")
    
    # 1. Resumen ejecutivo
    lines.append("## 1. Resumen Ejecutivo")
    lines.append("")
    lines.append("Este documento contiene la especificación técnica completa para la publicación de la semana del **31 de agosto al 6 de septiembre de 2026** para el cliente **Firma Bordados**.")
    lines.append("")
    lines.append("| Métrica | Valor |")
    lines.append("|---------|-------|")
    lines.append(f"| Total slots | **{len(schedule)}** |")
    media_count = sum(1 for s in schedule if s["slot_type"] == "media")
    text_count = sum(1 for s in schedule if s["slot_type"] == "text")
    lines.append(f"| Media (imagen/video) | **{media_count}** |")
    lines.append(f"| Texto only | **{text_count}** |")
    lines.append(f"| WhatsApp atención | **{config['whatsapp_number']}** |")
    lines.append(f"| Zona horaria | **{config['timezone']} (UTC{config['utc_offset_hours']:+d})** |")
    lines.append(f"| Categorías excluidas | **{', '.join(business_constraints['excluded_categories'])}** |")
    lines.append("")
    
    # 2. Configuración técnica
    lines.append("## 2. Configuración Técnica")
    lines.append("")
    lines.append("### 2.1 Información del Tenant")
    lines.append("")
    for k, v in config.items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")
    
    lines.append("### 2.2 Restricciones Comerciales")
    lines.append("")
    lines.append("⚠️ **OBLIGATORIO** - No publicar contenido relacionado con:")
    for cat in business_constraints['excluded_categories']:
        lines.append(f"- {cat}")
    lines.append("")
    lines.append("✅ **Canal de atención único:** WhatsApp")
    lines.append(f"- Número visible: `{config['whatsapp_number']}`")
    lines.append(f"- Link directo: `https://wa.me/{config['whatsapp_e164']}`")
    lines.append("")
    
    # 3. Assets determinísticos
    lines.append("## 3. Assets Determinísticos (16 media)")
    lines.append("")
    lines.append("Todos los assets tienen `confidence: DETERMINISTIC` y rutas físicas verificadas.")
    lines.append("")
    lines.append("| Asset Ref | Archivo | Ruta | Tipo | Descripción |")
    lines.append("|-----------|---------|------|------|-------------|")
    
    assets = manifest.get("assets", [])
    for a in assets:
        if a["confidence"] == "DETERMINISTIC":
            path = a.get("source_path") or "root"
            ftype = "VIDEO" if a["source_filename"].endswith(".mp4") else "IMAGE"
            lines.append(f"| {a['asset_ref']} | {a['source_filename']} | {path} | {ftype} | {a.get('description', '')} |")
    lines.append("")
    
    # 4. Schedule completo
    lines.append("## 4. Schedule Completo (20 slots)")
    lines.append("")
    lines.append("Formato: **Fecha local • Hora local (UTC) • Tipo • Asset/Contenido**")
    lines.append("")
    
    current_day = None
    for slot in schedule:
        day = slot["day"]
        if day != current_day:
            current_day = day
            day_label = day.capitalize()
            lines.append(f"### {day_label} ({slot['date_local']})")
            lines.append("")
        
        dt_utc = slot["datetime_utc"]
        dt_local = slot["datetime_local"]
        slot_type = slot["slot_type"]
        asset_ref = slot.get("asset_ref") or "TEXTO"
        desc = slot.get("description", "")
        
        type_icon = "📸" if slot_type == "media" else "📝"
        lines.append(f"- **{slot['time_local']}** ({dt_utc[:19]}Z) {type_icon} **{asset_ref}** — {desc}")
    
    lines.append("")
    
    # 5. Archivos de entrega
    lines.append("## 5. Archivos de Entrega")
    lines.append("")
    lines.append("| Archivo | Descripción | Ubicación |")
    lines.append("|---------|-------------|-----------|")
    lines.append(f"| `meta_import.csv` | CSV listo para importar en Meta Business Suite | `{META_CSV_PATH.relative_to(TENANT_DIR)}` |")
    lines.append(f"| `assets_manifest.json` | Manifest de 16 assets determinísticos | `{MANIFEST_PATH.relative_to(TENANT_DIR)}` |")
    lines.append(f"| `config.json` | Configuración del tenant (WhatsApp, timezone, constraints) | `{CONFIG_PATH.relative_to(TENANT_DIR)}` |")
    lines.append(f"| `dryrun_output.json` | Payloads completos validados para OmniRoute | `../dryrun_output.json` |")
    lines.append("")
    
    # 6. Instrucciones de publicación
    lines.append("## 6. Instrucciones para Equipo Operativo")
    lines.append("")
    lines.append("### 6.1 Importación en Meta Business Suite")
    lines.append("")
    lines.append("1. Abrir **Meta Business Suite** > **Planificador** > **Importar CSV**")
    lines.append("2. Seleccionar `meta_import.csv`")
    lines.append("3. Verificar que se importen **20 publicaciones** (16 media + 4 texto)")
    lines.append("4. Revisar cada slot:")
    lines.append("   - Fecha/hora correcta (zona horaria America/Matamoros)")
    lines.append("   - Media URL apunta al archivo correcto en Google Drive")
    lines.append("   - Caption incluye WhatsApp `878 788 0735` y hashtags")
    lines.append("   - Ubicación: `Piedras Negras, Coahuila, México`")
    lines.append("5. Programar (no publicar inmediatamente)")
    lines.append("")
    
    lines.append("### 6.2 Verificación Pre-Publicación")
    lines.append("")
    lines.append("- [ ] Todos los 16 archivos de media existen en Google Drive")
    lines.append("- [ ] No hay contenido de `parches` ni `gorras`")
    lines.append("- [ ] WhatsApp `878 788 0735` visible en todos los captions")
    lines.append("- [ ] Hashtags base presentes: `#FirmaBordados #BordadoPersonalizado #UniformesCorporativos #PiedrasNegras #EaglePass #Bordados #Embroidery`")
    lines.append("- [ ] Link `https://wa.me/5218787880735` funcional")
    lines.append("- [ ] Zona horaria `America/Matamoros` seleccionada")
    lines.append("")
    
    lines.append("### 6.3 Post-Publicación (Auditoría)")
    lines.append("")
    lines.append("Después de la semana, el sistema LOCAL ejecutará auditoría automática:")
    lines.append("- Comparar `publication_log.csv` con métricas reales")
    lines.append("- Actualizar `status` → `published` + `published_at` + métricas")
    lines.append("- Generar reporte de `reach`, `interactions`, `DMs`, `leads`")
    lines.append("")
    
    # 7. Payloads técnicos (referencia)
    lines.append("## 7. Referencia Técnica - Payloads OmniRoute")
    lines.append("")
    lines.append("Cada slot tiene payload validado para OmniRoute con:")
    lines.append("- `tenant_id: firma-bordados`")
    lines.append("- `slot_id` único (ej: `firma-bordados-20260831-morning-01`)")
    lines.append("- `datetime_utc` ISO 8601 con timezone")
    lines.append("- `whatsapp_e164: 5218787880735`")
    lines.append("- `excluded_categories: [parches, gorras]`")
    lines.append("- Para media: `asset_ref`, `source_filename`, `source_file_key`, `confidence: DETERMINISTIC`")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*Documento generado automáticamente por Growth OS — LOCAL/OFFLINE*")
    lines.append("*Sin llamadas a APIs externas — Arquitectura multi-tenant aislada*")
    
    content = "\n".join(lines)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"✅ Handoff spec generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_handoff_spec()
