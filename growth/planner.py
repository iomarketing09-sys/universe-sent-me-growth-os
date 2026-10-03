"""
Planner interface para Growth OS.

Proporciona una estructura clara para el scheduling:
    ScheduleItem -> validation -> MetaPublisher -> publication_log

NO implementa la migración completa del manifiesto aún.
Solo define la interfaz y puede consumir la fuente existente más estable.
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
import growth.historical_baseline as historical_baseline


# Mapping de hora local a nombre de slot (consistente con dryrun)
TIME_TO_SLOT = {
    "08:30": "morning",
    "14:00": "afternoon",
    "19:30": "evening",
    "20:00": "evening",
}

def build_slot_id(tenant_id: str, date_str: str, time_str: str) -> str:
    """Construye slot_id consistente: tenant-YYYYMMDD-slotname-NN"""
    slot_name = TIME_TO_SLOT.get(time_str, "unknown")
    date_key = date_str.replace("-", "")
    # Para el contador, usamos un hash simple basado en la hora
    hour = int(time_str.split(":")[0])
    counter = (hour // 3) + 1  # 08->1, 14->2, 19/20->3/4
    return f"{tenant_id}-{date_key}-{slot_name}-{counter:02d}"


@dataclass
class ScheduleItem:
    """Estructura unificada para un item de programación."""
    tenant_id: str
    slot_id: str
    date: str                    # YYYY-MM-DD (local)
    time: str                    # HH:MM (local, 24h)
    datetime_utc: str            # ISO 8601 UTC
    type: str                    # "photo" | "video" | "text" | "reel"
    asset_ref: Optional[str] = None
    asset_filename: Optional[str] = None
    caption: str = ""
    hashtags: str = ""
    link_url: str = ""
    first_comment: str = ""
    location: str = ""
    source_path: Optional[str] = None
    confidence: str = "DETERMINISTIC"
    
    # Metadatos internos
    _meta: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario plano para serialización."""
        d = asdict(self)
        d.pop('_meta', None)
        return d
    
    @classmethod
    def from_dryrun_slot(cls, slot: Dict[str, Any], tenant_id: str) -> 'ScheduleItem':
        """Crea ScheduleItem desde un slot de dryrun_output.json."""
        historical_evidence = None
        asset_filename = slot.get("source_filename")
        if asset_filename:
            try:
                historical_evidence = historical_baseline.get_historical_reuse_info(asset_filename)
            except Exception:
                historical_evidence = None
        else:
            historical_evidence = None
        return cls(
            tenant_id=tenant_id,
            slot_id=slot.get("slot_id", ""),
            date=slot.get("date_local", ""),
            time=slot.get("time_local", ""),
            datetime_utc=slot.get("datetime_utc", ""),
            type=slot.get("slot_type", "media"),
            asset_ref=slot.get("asset_ref"),
            asset_filename=slot.get("source_filename"),
            caption=slot.get("description", ""),
            hashtags="",
            link_url=slot.get("whatsapp_e164") and f"https://wa.me/{slot['whatsapp_e164']}",
            first_comment="",
            location="",
            source_path=slot.get("source_path"),
            confidence=slot.get("confidence", "DETERMINISTIC"),
            _meta={"historical_evidence": historical_evidence}
        )

    @classmethod
    def from_meta_import_row(cls, row: Dict[str, str], tenant_id: str) -> 'ScheduleItem':
        """Crea ScheduleItem desde una fila de meta_import.csv."""
        # Determinar tipo
        post_type = row.get("Post Type", "").strip().upper()
        if post_type in ("VIDEO", "REEL"):
            type_ = "video"
        elif post_type in ("TEXT", "TEXT_ONLY"):
            type_ = "text"
        else:
            type_ = "photo"
        
        date_str = row.get("Date (YYYY-MM-DD)", "")
        time_str = row.get("Time (HH:MM, 24h)", "")
        
        # Build consistent slot_id
        slot_id = build_slot_id(tenant_id, date_str, time_str)
        
        # Convert local time to UTC (assuming America/Matamoros = UTC-5)
        dt_local = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        # UTC = local + 5 hours (America/Matamoros is UTC-5)
        from datetime import timedelta
        dt_utc = dt_local + timedelta(hours=5)
        datetime_utc = dt_utc.replace(tzinfo=timezone.utc).isoformat()
        
        # Get asset filename from the row
        asset_filename = row.get("Media URL", "").strip() or None
        historical_evidence = None
        if asset_filename:
            try:
                historical_evidence = historical_baseline.get_historical_reuse_info(asset_filename)
            except Exception:
                historical_evidence = None
        else:
            historical_evidence = None
        return cls(
            tenant_id=tenant_id,
            slot_id=slot_id,
            date=date_str,
            time=time_str,
            datetime_utc=datetime_utc,
            type=type_,
            asset_ref=None,
            asset_filename=asset_filename,
            caption=row.get("Caption", ""),
            hashtags=row.get("Hashtags", ""),
            link_url=row.get("Link URL", ""),
            first_comment=row.get("First Comment", ""),
            location=row.get("Location", ""),
            _meta={"historical_evidence": historical_evidence}
        )

    def build_meta_payload(self) -> Dict[str, Any]:
        """Construye el payload para MetaPublisher."""
        payload = {
            "caption": self.caption,
            "published": "false",
            "scheduled_publish_time": self.datetime_utc,
        }
        if self.link_url:
            payload["link"] = self.link_url
        return payload


class Planner:
    """
    Interfaz de planificación.
    
    Puede cargar desde diferentes fuentes y producir una lista de ScheduleItems.
    """
    
    def __init__(self, tenant_id: str = "firma-bordados"):
        self.tenant_id = tenant_id
    
    def load_from_dryrun(self, dryrun_path: Path) -> List[ScheduleItem]:
        """Carga schedule desde dryrun_output.json."""
        with dryrun_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        schedule = data.get("schedule", [])
        return [ScheduleItem.from_dryrun_slot(slot, self.tenant_id) for slot in schedule]
    
    def load_from_meta_import(self, meta_import_path: Path) -> List[ScheduleItem]:
        """Carga schedule desde meta_import.csv (fuente más estable actual)."""
        import csv
        with meta_import_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        return [ScheduleItem.from_meta_import_row(row, self.tenant_id) for row in rows]
    
    def filter_slots(self, items: List[ScheduleItem], slot_ids: List[str]) -> List[ScheduleItem]:
        """Filtra por lista de slot_ids."""
        slot_id_set = set(slot_ids)
        return [item for item in items if item.slot_id in slot_id_set]
    
    def filter_future(self, items: List[ScheduleItem]) -> List[ScheduleItem]:
        """Filtra solo slots futuros (datetime_utc > ahora)."""
        now = datetime.now(timezone.utc)
        result = []
        for item in items:
            try:
                dt = datetime.fromisoformat(item.datetime_utc.replace("Z", "+00:00"))
                if dt >= now:
                    result.append(item)
            except:
                pass
        return result


def build_schedule(
    tenant_id: str = "firma-bordados",
    source: str = "meta_import",  # "dryrun" | "meta_import"
    dryrun_path: Optional[Path] = None,
    meta_import_path: Optional[Path] = None,
    slot_ids: Optional[List[str]] = None,
    future_only: bool = True,
) -> List[ScheduleItem]:
    """
    Función de conveniencia para construir schedule.
    
    Args:
        tenant_id: ID del tenant
        source: Fuente de datos ("dryrun" o "meta_import")
        dryrun_path: Ruta a dryrun_output.json (si source="dryrun")
        meta_import_path: Ruta a meta_import.csv (si source="meta_import")
        slot_ids: Lista opcional de slot_ids a filtrar
        future_only: Si True, filtra solo slots futuros
    
    Returns:
        Lista de ScheduleItems listos para validación y publicación
    """
    planner = Planner(tenant_id)
    
    if source == "dryrun":
        path = dryrun_path or Path("dryrun_output.json")
        items = planner.load_from_dryrun(path)
    else:
        path = meta_import_path or Path(f"tenants/{tenant_id}/meta_import.csv")
        items = planner.load_from_meta_import(path)
    
    if slot_ids:
        items = planner.filter_slots(items, slot_ids)
    
    if future_only:
        items = planner.filter_future(items)
    
    return items


if __name__ == "__main__":
    import sys
    
    # Demo
    items = build_schedule("firma-bordados", source="meta_import")
    print(f"Loaded {len(items)} schedule items")
    for item in items[:3]:
        print(f"  {item.slot_id} | {item.date} {item.time} | {item.type} | {item.asset_filename or 'TEXT'}")
