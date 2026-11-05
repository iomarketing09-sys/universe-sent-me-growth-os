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
from datetime import datetime, timedelta, timezone
import json
import re
import modules.intelligence.historical_baseline as historical_baseline


# Mapping de hora local a nombre de slot (consistente con dryrun)
TIME_TO_SLOT = {
    "08:30": "morning",
    "10:00": "morning",
    "11:00": "late-morning",
    "13:30": "afternoon",
    "14:00": "afternoon",
    "16:00": "late-afternoon",
    "17:00": "pre-evening",
    "19:00": "evening",
    "19:30": "evening",
    "20:00": "evening",
    "21:00": "night",
}

META_IMPORT_FIELDS = [
    "Date (YYYY-MM-DD)",
    "Time (HH:MM, 24h)",
    "Timezone",
    "Post Type",
    "Media URL",
    "Caption",
    "Link URL",
    "Hashtags",
    "Location",
    "First Comment",
    "Pilar",
    "Hypothesis ID",
    "Experiment ID",
]

POST_TYPES = {"PHOTO", "VIDEO", "REEL", "TEXT"}

CANON_CHARACTERS = (
    "Universe",
    "Wilfred",
    "Elara",
    "Ganso",
    "Payaso",
    "Kiri",
    "Evan",
    "Fantasma",
    "Kael",
    "Maeve",
    "Silvio",
    "Chipitillo",
)

# Hora de referencia por banda, tomada del ranking histórico.
BAND_HOUR = {"06-11": "10:00", "12-16": "13:30", "17-21": "19:00", "22-05": "21:00"}

# Parrilla real de Universe (hora de Matamoros). 13:30 es la hora estelar.
SLOT_HOURS = ("10:00", "11:00", "13:30", "16:00", "17:00", "19:00")
STAR_HOUR = "13:30"

# Regla de reuse: 2 por día, 3 como máximo, nunca en horas consecutivas.
MIN_REUSE_PER_DAY = 2
MAX_REUSE_PER_DAY = 3

PILLARS = (
    "Humor Existencial",
    "Sabiduría Práctica",
    "Lore",
    "Comunidad / UGC",
)

# Personaje -> pilar por defecto. El pilar real lo decide el chiste, esto solo
# es el punto de partida cuando el asset no trae uno declarado.
PILLAR_BY_CHARACTER = {
    "Universe": "Humor Existencial",
    "Ganso": "Humor Existencial",
    "Payaso": "Humor Existencial",
    "Wilfred": "Sabiduría Práctica",
    "Elara": "Sabiduría Práctica",
    "Kiri": "Sabiduría Práctica",
    "Evan": "Lore",
    "Kael": "Lore",
    "Maeve": "Lore",
    "Fantasma": "Lore",
}


def parse_asset_filename(name: str) -> Dict[str, Any]:
    """Extrae código, personajes y chiste de ``<código> - <personajes> - <texto>``."""
    stem = Path(str(name)).stem
    parts = [part.strip() for part in stem.split(" - ")]
    code = parts[0].strip() if parts and parts[0].strip().isdigit() else ""
    rest = parts[1:] if code else parts
    characters: List[str] = []
    if rest:
        for token in str(rest[0]).replace(",", "+").split("+"):
            token = token.strip()
            if not token:
                continue
            normalized = token if token in CANON_CHARACTERS else ""
            if not normalized and token.lower() in {"el ganso", "ganso"}:
                normalized = "Ganso"
            if normalized:
                characters.append(normalized)
        rest = rest[1:]
    meme_text = " - ".join(rest).strip()
    # Ruido del nombre: fechas al final "(10-jun-26)" y códigos internos "CNT018".
    meme_text = re.sub(r"\s*\([^)]*\d[^)]*\)\s*$", "", meme_text).strip()
    if re.fullmatch(r"CNT\d+", meme_text, re.IGNORECASE):
        meme_text = ""
    # Sin código numérico el nombre es sólo personaje + etiqueta del archivo
    # ("Fantasma - MardeNubes 1"): no es un chiste, se resuelve por visión.
    if not code and len(meme_text) < 15:
        meme_text = ""
    return {"code": code, "characters": characters, "meme_text": meme_text}


def load_meme_text_index(tenant_id: str, base_path: Optional[Path] = None) -> Dict[str, str]:
    """Transcripciones de visión: ``filename -> meme_text``.

    Las llena ``scripts/transcribe_memes.py`` para assets viejos cuyo nombre no
    trae el chiste. No sustituye al nombre: solo rellena lo que falta.
    """
    import csv

    root = Path(base_path) if base_path else Path(__file__).resolve().parents[2]
    path = root / "tenants" / tenant_id / "assets_meme_text.csv"
    if not path.is_file():
        return {}
    index: Dict[str, str] = {}
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                name = str(row.get("filename") or "").strip()
                text = str(row.get("meme_text") or "").strip()
                if name and text:
                    index[name] = text
    except (OSError, csv.Error, UnicodeDecodeError):
        return {}
    return index


def available_assets(
    assets_dir: Path, meme_index: Optional[Dict[str, str]] = None
) -> List[Dict[str, Any]]:
    """Lista los assets disponibles del inventario sin abrir los archivos."""
    directory = Path(assets_dir)
    if not directory.is_dir():
        return []
    assets: List[Dict[str, Any]] = []
    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}:
            continue
        parsed = parse_asset_filename(path.name)
        meme_text = parsed["meme_text"] or (meme_index or {}).get(path.name, "")
        assets.append(
            {
                "filename": path.name,
                "path": str(path),
                "code": parsed["code"],
                "characters": parsed["characters"],
                "meme_text": meme_text,
                "type": "video" if suffix in {".mp4", ".mov"} else "photo",
            }
        )
    return assets


def default_assets_dir(tenant_id: str) -> Path:
    """Carpeta de assets nuevos del tenant (convención Drive de Universe)."""
    return Path.home() / "GoogleDrive" / "Universe sent me" / "Assets" / "Assets Nuevos"


def default_reuse_dir(tenant_id: str) -> Path:
    """Archivo de publicados (reuse), con una carpeta por mes."""
    return Path.home() / "GoogleDrive" / "Universe sent me" / "Assets" / "Publicado (Reuse)"


_MONTH_ORDER = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
    "noviembre": 11, "diciembre": 12,
}


def _month_rank(folder_name: str) -> int:
    """Orden cronológico de ``04 Abril`` -> 4. Desconocido al final."""
    words = str(folder_name).replace("-", " ").replace("_", " ").split()
    for word in words:
        key = "".join(char for char in word.lower() if char.isalpha())
        if key in _MONTH_ORDER:
            return _MONTH_ORDER[key]
    return 99


def reuse_assets(
    reuse_dir: Path, meme_index: Optional[Dict[str, str]] = None
) -> List[Dict[str, Any]]:
    """Assets ya publicados, del mes más viejo al más nuevo.

    Se prefiere lo más antiguo para ir vaciando las carpetas viejas.
    """
    root = Path(reuse_dir)
    if not root.is_dir():
        return []
    assets: List[Dict[str, Any]] = []
    folders = sorted(
        (path for path in root.iterdir() if path.is_dir()),
        key=lambda path: (_month_rank(path.name), path.name),
    )
    for folder in folders:
        month = folder.name
        for path in sorted(folder.iterdir()):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}:
                continue
            parsed = parse_asset_filename(path.name)
            assets.append(
                {
                    "filename": path.name,
                    "path": str(path),
                    "code": parsed["code"],
                    "characters": parsed["characters"],
                    "meme_text": parsed["meme_text"] or (meme_index or {}).get(path.name, ""),
                    "type": "video" if path.suffix.lower() in {".mp4", ".mov"} else "photo",
                    "reuse": True,
                    "month": month,
                    "month_rank": _month_rank(month),
                }
            )
    # Primero los que traen chiste en el nombre: sin él no hay caption posible.
    # Dentro de cada grupo, el mes más viejo primero para ir vaciando carpetas.
    assets.sort(key=lambda a: (0 if a["meme_text"] else 1, a["month_rank"], a["filename"]))
    return assets


def pillar_for(characters: List[str]) -> str:
    """Pilar sugerido a partir del personaje; el chiste manda si hay duda."""
    for name in characters or []:
        if name in PILLAR_BY_CHARACTER:
            return PILLAR_BY_CHARACTER[name]
    return "Humor Existencial"


def reuse_positions(slot_count: int, star_index: int, count: int) -> List[int]:
    """Posiciones de reuse sin horas consecutivas, evitando la hora estelar."""
    count = max(0, min(count, MAX_REUSE_PER_DAY))
    if count == 0:
        return []
    best: Optional[List[int]] = None
    best_cost: Optional[tuple] = None

    from itertools import combinations

    for combo in combinations(range(slot_count), count):
        if any(b - a == 1 for a, b in zip(combo, combo[1:])):
            continue
        # Preferir lo más alejado de la hora estelar (bandas más débiles).
        cost = (
            star_index in combo,
            -sum(abs(index - star_index) for index in combo),
            combo,
        )
        if best_cost is None or cost < best_cost:
            best, best_cost = list(combo), cost
    return best or []


def _character_order(ranking: Dict[str, Any]) -> List[str]:
    """Personajes del canon ordenados por mediana de interacciones."""
    measured = [row for row in ranking.get("by_character", []) if row["publications"] >= 2]
    measured.sort(key=lambda row: (-row["median_score"], -row["publications"]))
    order: List[str] = []
    for row in measured:
        name = str(row.get("character") or "")
        if name in CANON_CHARACTERS and name not in order:
            order.append(name)
    for row in ranking.get("by_character", []):
        name = str(row.get("character") or "")
        if name in CANON_CHARACTERS and name not in order:
            order.append(name)
    for name in CANON_CHARACTERS:
        if name not in order:
            order.append(name)
    return order


def _build_pool(assets: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    pool: Dict[str, List[Dict[str, Any]]] = {}
    for asset in assets:
        for name in asset["characters"] or ["Universe"]:
            pool.setdefault(name, []).append(asset)
    return pool


def _pick(
    pool: Dict[str, List[Dict[str, Any]]],
    name: str,
    used: set,
) -> Optional[Dict[str, Any]]:
    for asset in pool.get(name, []):
        if asset["filename"] not in used:
            return asset
    return None


def _propose_single_hour(
    tenant_id: str,
    *,
    start_date: str,
    days: int,
    hour: Optional[str],
    per_day: int,
    assets: List[Dict[str, Any]],
    ranking: Dict[str, Any],
) -> Dict[str, Any]:
    """Modo clásico: un slot por día a la hora de la mejor banda."""
    bands = sorted(
        [band for band in ranking.get("by_hour_band", []) if band["publications"] >= 2],
        key=lambda band: -band["median_score"],
    )
    chosen_band = (bands or ranking.get("by_hour_band") or [{}])[0]
    chosen_hour = hour or BAND_HOUR.get(str(chosen_band.get("hour_band") or ""), "19:00")

    order = _character_order(ranking)
    pool = _build_pool(assets)
    rotation = [name for name in order if pool.get(name)]
    used: set = set()
    items: List[ScheduleItem] = []
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    notes: List[str] = []

    cursor = 0
    for day_index in range(max(1, days)):
        current_date = start + timedelta(days=day_index)
        for _ in range(max(1, per_day)):
            picked = None
            for _ in range(len(rotation) or 1):
                name = rotation[cursor % len(rotation)] if rotation else ""
                cursor += 1
                picked = _pick(pool, name, used)
                if picked:
                    break
            if not picked:
                continue
            used.add(picked["filename"])
            characters = picked["characters"] or ["Universe"]
            items.append(
                ScheduleItem(
                    tenant_id=tenant_id,
                    slot_id=build_slot_id(tenant_id, current_date.isoformat(), chosen_hour),
                    date=current_date.isoformat(),
                    time=chosen_hour,
                    datetime_utc="",
                    type=picked["type"],
                    asset_ref=picked["code"] or None,
                    asset_filename=picked["filename"],
                    caption=picked["meme_text"],
                    hashtags=" ".join(
                        [f"#{name}USM" for name in characters]
                        + ["#humor", "#UniverseSentMe"]
                    ),
                    pillar=pillar_for(characters),
                    origin="nuevo",
                )
            )

    return {
        "tenant_id": tenant_id,
        "start_date": start_date,
        "days": days,
        "hour": chosen_hour,
        "band": str(chosen_band.get("hour_band") or ""),
        "hours": [chosen_hour],
        "assets_available": len(assets),
        "reuse_available": 0,
        "items": items,
        "leftovers": [asset["filename"] for asset in assets if asset["filename"] not in used],
        "notes": notes,
    }


def propose_week(
    tenant_id: str = "universe",
    *,
    start_date: str,
    days: int = 3,
    hour: Optional[str] = None,
    per_day: int = 1,
    hours: Optional[List[str]] = None,
    assets_dir: Optional[Path] = None,
    reuse_dir: Optional[Path] = None,
    reuse_per_day: Optional[int] = None,
    base_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Propone el calendario del periodo con inventario y ranking histórico.

    Dos modos:

    - ``hours`` vacío: un slot por día a la hora de la mejor banda (modo clásico).
    - ``hours`` con la parrilla del día: llena todos los slots, mezcla assets
      nuevos con reuse y aplica la regla de reuse (2 por día, 3 máximo, nunca
      en horas consecutivas y nunca en la hora estelar).

    No publica ni escribe nada.
    """
    meme_index = load_meme_text_index(tenant_id, base_path=base_path)
    assets = available_assets(
        Path(assets_dir) if assets_dir else default_assets_dir(tenant_id), meme_index
    )
    ranking = historical_baseline.rank_publications(tenant_id, base_path=base_path)

    if not hours:
        proposal = _propose_single_hour(
            tenant_id,
            start_date=start_date,
            days=days,
            hour=hour,
            per_day=per_day,
            assets=assets,
            ranking=ranking,
        )
        if not assets:
            proposal["notes"].append("Sin assets disponibles en el inventario.")
        if not _character_order(ranking):
            proposal["notes"].append("Ningún asset del inventario declara un personaje del canon.")
        return proposal

    slot_hours = list(hours)
    reuse_pool_assets = (
        reuse_assets(Path(reuse_dir), meme_index)
        if reuse_dir
        else reuse_assets(default_reuse_dir(tenant_id), meme_index)
    )
    start = datetime.strptime(start_date, "%Y-%m-%d").date()

    try:
        star_index = slot_hours.index(STAR_HOUR)
    except ValueError:
        star_index = len(slot_hours) // 2

    order = _character_order(ranking)
    new_pool = _build_pool(assets)
    reuse_pool = _build_pool(reuse_pool_assets)
    rotation = [name for name in order if new_pool.get(name) or reuse_pool.get(name)]

    target_reuse = MIN_REUSE_PER_DAY if reuse_per_day is None else reuse_per_day
    target_reuse = max(0, min(target_reuse, MAX_REUSE_PER_DAY))

    used: set = set()
    items: List[ScheduleItem] = []
    notes: List[str] = []
    cursor = 0

    for day_index in range(max(1, days)):
        current_date = start + timedelta(days=day_index)
        new_needed = len(slot_hours) - target_reuse
        new_left = [asset for asset in assets if asset["filename"] not in used]
        reuse_count = target_reuse
        if len(new_left) < new_needed and reuse_count < MAX_REUSE_PER_DAY:
            reuse_count = min(MAX_REUSE_PER_DAY, reuse_count + 1)
            notes.append(
                f"{current_date.isoformat()}: inventario nuevo corto, se usan {reuse_count} reuse."
            )

        positions = set(reuse_positions(len(slot_hours), star_index, reuse_count))
        if len(positions) < reuse_count:
            notes.append(
                f"{current_date.isoformat()}: no hubo forma de colocar {reuse_count} reuse "
                "sin horas consecutivas."
            )

        for index, slot_hour in enumerate(slot_hours):
            is_reuse = index in positions
            pool = reuse_pool if is_reuse else new_pool
            picked: Optional[Dict[str, Any]] = None

            if index == star_index and not is_reuse:
                # La hora estelar rota el mejor personaje disponible, día con día.
                offset = day_index % len(order) if order else 0
                for name in order[offset:] + order[:offset]:
                    picked = _pick(new_pool, name, used)
                    if picked:
                        break

            if not picked:
                for _ in range(len(rotation) or 1):
                    name = rotation[cursor % len(rotation)] if rotation else ""
                    cursor += 1
                    picked = _pick(pool, name, used)
                    if picked:
                        break

            if not picked:
                # Sin asset de ese personaje: cualquier disponible del mismo origen.
                for asset in (reuse_pool_assets if is_reuse else assets):
                    if asset["filename"] not in used:
                        picked = asset
                        break

            if not picked:
                notes.append(f"{current_date.isoformat()} {slot_hour}: sin asset disponible.")
                continue

            used.add(picked["filename"])
            characters = picked["characters"] or ["Universe"]
            items.append(
                ScheduleItem(
                    tenant_id=tenant_id,
                    slot_id=build_slot_id(tenant_id, current_date.isoformat(), slot_hour),
                    date=current_date.isoformat(),
                    time=slot_hour,
                    datetime_utc="",
                    type=picked["type"],
                    asset_ref=picked["code"] or None,
                    asset_filename=picked["filename"],
                    caption=picked["meme_text"],
                    hashtags=" ".join(
                        [f"#{name}USM" for name in characters]
                        + ["#humor", "#UniverseSentMe"]
                    ),
                    pillar=pillar_for(characters),
                    origin="reuse" if is_reuse else "nuevo",
                )
            )

    return {
        "tenant_id": tenant_id,
        "start_date": start_date,
        "days": days,
        "hour": STAR_HOUR if STAR_HOUR in slot_hours else slot_hours[0],
        "band": "",
        "hours": slot_hours,
        "assets_available": len(assets),
        "reuse_available": len(reuse_pool_assets),
        "items": items,
        "leftovers": [asset["filename"] for asset in assets if asset["filename"] not in used],
        "notes": notes,
    }


def build_slot_id(tenant_id: str, date_str: str, time_str: str) -> str:
    """Construye slot_id consistente: tenant-YYYYMMDD-slotname-NN"""
    slot_name = TIME_TO_SLOT.get(time_str)
    if slot_name is None:
        try:
            hour = int(time_str.split(":")[0])
        except (ValueError, IndexError):
            hour = 0
        slot_name = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
    date_key = date_str.replace("-", "")
    # El contador es el minuto del día: único por hora, sin colisiones.
    try:
        hour_text, minute_text = time_str.split(":")[:2]
        counter = int(hour_text) * 60 + int(minute_text)
    except (ValueError, IndexError):
        counter = 0
    return f"{tenant_id}-{date_key}-{slot_name}-{counter:04d}"


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
    pillar: str = ""
    origin: str = ""  # "nuevo" | "reuse"
    hypothesis_id: str = ""
    experiment_id: str = ""
    
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
                historical_evidence = historical_baseline.get_historical_reuse_info(
                    asset_filename, tenant_id=tenant_id
                )
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
                historical_evidence = historical_baseline.get_historical_reuse_info(
                    asset_filename, tenant_id=tenant_id
                )
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
            pillar=row.get("Pilar", ""),
            origin=row.get("Origin", ""),
            hypothesis_id=row.get("Hypothesis ID", ""),
            experiment_id=row.get("Experiment ID", ""),
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

    def validate_items(
        self,
        items: List[ScheduleItem],
        *,
        timezone_name: str = "America/Matamoros",
    ) -> tuple:
        """Devuelve ``(rows, errors)`` sin escribir nada."""
        errors: List[str] = []
        rows: Dict[tuple, Dict[str, str]] = {}
        for item in items:
            label = f"{item.date} {item.time}"
            try:
                datetime.strptime(f"{item.date} {item.time}", "%Y-%m-%d %H:%M")
            except ValueError:
                errors.append(f"{label}: fecha u hora inválida (YYYY-MM-DD HH:MM)")
                continue
            post_type = str(item.type or "").strip().upper()
            if post_type == "MEDIA":
                post_type = "PHOTO"
            if post_type not in POST_TYPES:
                errors.append(f"{label}: Post Type {item.type!r} no soportado")
                continue
            if post_type != "TEXT" and not str(item.asset_filename or "").strip():
                errors.append(f"{label}: falta Media URL")
                continue
            if post_type == "TEXT" and not str(item.caption or "").strip():
                errors.append(f"{label}: TEXT sin Caption")
                continue
            key = (item.date, item.time)
            if key in rows:
                errors.append(f"{label}: slot duplicado en el plan")
                continue
            rows[key] = {
                "Date (YYYY-MM-DD)": item.date,
                "Time (HH:MM, 24h)": item.time,
                "Timezone": timezone_name,
                "Post Type": post_type,
                "Media URL": str(item.asset_filename or ""),
                "Caption": item.caption or "",
                "Link URL": item.link_url or "",
                "Hashtags": item.hashtags or "",
                "Location": item.location or "",
                "First Comment": item.first_comment or "",
                "Pilar": item.pillar or "",
                "Hypothesis ID": item.hypothesis_id or "",
                "Experiment ID": item.experiment_id or "",
            }

        return rows, errors

    def write_meta_import(
        self,
        items: List[ScheduleItem],
        path: Path,
        *,
        timezone_name: str = "America/Matamoros",
        merge: bool = True,
    ) -> Dict[str, Any]:
        """Valida y escribe ``meta_import.csv`` de forma idempotente.

        La clave de mezcla es (fecha, hora): volver a correr el plan actualiza
        ese slot en lugar de duplicarlo. Con ``merge=False`` se reescribe el
        archivo completo.

        Lanza ``ValueError`` con la lista de problemas si algún slot no es
        válido; en ese caso no escribe nada.
        """
        import csv

        rows, errors = self.validate_items(items, timezone_name=timezone_name)

        if errors:
            raise ValueError("; ".join(errors))

        existing: List[Dict[str, str]] = []
        if merge and path.is_file():
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                existing = list(csv.DictReader(handle))

        merged: Dict[tuple, Dict[str, str]] = {}
        for row in existing:
            key = (
                str(row.get("Date (YYYY-MM-DD)") or "").strip(),
                str(row.get("Time (HH:MM, 24h)") or "").strip(),
            )
            merged[key] = {field: str(row.get(field) or "") for field in META_IMPORT_FIELDS}
        replaced = sum(1 for key in rows if key in merged)
        merged.update(rows)

        ordered = [merged[key] for key in sorted(merged)]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=META_IMPORT_FIELDS)
            writer.writeheader()
            writer.writerows(ordered)

        return {
            "written": len(rows),
            "replaced": replaced,
            "total": len(ordered),
            "path": str(path),
        }


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
