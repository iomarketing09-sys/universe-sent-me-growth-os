"""Auditoría local de un tenant para onboarding.

Solo lee archivos del repositorio: no llama a Meta, Google ni scraping.
Devuelve un dictamen con checks individuales para que CGO decida si el tenant
está listo o qué le falta.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
SKIP = "SKIP"

READY = "READY"
PARTIAL = "PARTIAL"
BLOCKED = "BLOCKED"

REQUIRED_CONFIG_KEYS = ("tenant_id", "client_name", "timezone", "contact_channel")
VALID_TRACKS = {"native_digital", "physical_cro"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
SYNC_MAX_AGE_DAYS = 3


def _project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[4]


def _check(
    check_id: str,
    name: str,
    state: str,
    detail: str,
    action: str = "",
) -> Dict[str, Any]:
    return {
        "id": check_id,
        "name": name,
        "state": state,
        "detail": detail,
        "action": action,
    }


def _load_config(tenant_dir: Path) -> Dict[str, Any]:
    path = tenant_dir / "config.json"
    if not path.is_file():
        raise FileNotFoundError("config.json no existe")
    return json.loads(path.read_text(encoding="utf-8"))


def _check_config(config: Dict[str, Any]) -> Dict[str, Any]:
    missing = [key for key in REQUIRED_CONFIG_KEYS if not config.get(key)]
    if missing:
        return _check(
            "config",
            "Configuración del tenant",
            WARN,
            f"Faltan campos: {', '.join(missing)}",
            f"Agregar {', '.join(missing)} a config.json",
        )
    return _check("config", "Configuración del tenant", PASS, "Campos obligatorios completos.")


def _check_track(config: Dict[str, Any]) -> Dict[str, Any]:
    track = str(config.get("tenant_type") or "")
    if track in VALID_TRACKS:
        return _check("track", "Track de negocio", PASS, f"tenant_type={track}")
    return _check(
        "track",
        "Track de negocio",
        WARN,
        f"tenant_type ausente o inválido: {track or '(vacío)'}",
        "Definir tenant_type como native_digital o physical_cro",
    )


def _check_brand(tenant_id: str, base_path: Optional[Path]) -> Dict[str, Any]:
    from modules.creative.brand_kit import load_brand_kit, logo_path

    try:
        kit = load_brand_kit(tenant_id, str(base_path) if base_path else None)
    except Exception as exc:
        return _check(
            "brand_kit",
            "Identidad de marca",
            FAIL,
            f"No se pudo cargar brand kit: {type(exc).__name__}",
            "Crear brand_kit.json o completar config.json",
        )

    has_voice = bool(str(kit.get("voice") or "").strip())
    if not has_voice:
        voice_file = (base_path or _project_root()) / "tenants" / tenant_id / "brand_voice.json"
        if voice_file.is_file():
            try:
                voice = json.loads(voice_file.read_text(encoding="utf-8"))
                has_voice = bool(
                    voice.get("brand_identity") or voice.get("voice_attributes")
                )
            except ValueError:
                has_voice = False
    has_palette = bool(kit.get("palette"))
    logo = logo_path(tenant_id, str(base_path) if base_path else None)

    detail = (
        f"voz={'sí' if has_voice else 'no'}, "
        f"paleta={'sí' if has_palette else 'no'}, "
        f"logo={'sí' if logo else 'no'}"
    )
    if has_voice and logo:
        return _check("brand_kit", "Identidad de marca", PASS, detail)
    return _check(
        "brand_kit",
        "Identidad de marca",
        WARN,
        detail,
        "Completar voz, paleta y logo en el brand kit",
    )


def _check_assets(tenant_dir: Path) -> Dict[str, Any]:
    assets = tenant_dir / "assets"
    if not assets.is_dir():
        return _check(
            "assets",
            "Assets de producto/contenido",
            WARN,
            "No existe carpeta assets/",
            "Cargar imágenes del tenant en assets/",
        )
    count = sum(
        1
        for path in assets.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    if count == 0:
        return _check(
            "assets",
            "Assets de producto/contenido",
            WARN,
            "assets/ existe pero no tiene imágenes.",
            "Subir imágenes al tenant",
        )
    return _check("assets", "Assets de producto/contenido", PASS, f"{count} imágenes.")


def _check_inventory(tenant_id: str, config: Dict[str, Any], base_path: Optional[Path]) -> Dict[str, Any]:
    from modules.creative.image_selector import load_approved_models, list_model_assets

    try:
        models = load_approved_models(tenant_id, str(base_path) if base_path else None)
    except Exception as exc:
        return _check(
            "inventory",
            "Inventario declarado",
            FAIL,
            f"No se pudo leer el inventario: {type(exc).__name__}",
            "Revisar config.ads.approved_models",
        )

    if not models:
        return _check(
            "inventory",
            "Inventario declarado",
            WARN,
            "Sin modelos declarados (inventario parcial o vacío).",
            "Cargar modelos en config.ads.approved_models",
        )

    without_assets = 0
    for model in models:
        try:
            images = list_model_assets(
                tenant_id, model, str(base_path) if base_path else None
            )
        except Exception:
            images = []
        if not images:
            without_assets += 1

    detail = f"{len(models)} modelos declarados"
    if without_assets:
        detail += f", {without_assets} sin imágenes"
        return _check(
            "inventory",
            "Inventario declarado",
            WARN,
            detail + " (el inventario puede ser parcial).",
            "Completar imágenes de los modelos sin assets",
        )
    return _check("inventory", "Inventario declarado", PASS, detail)


def _check_channels(tenant_dir: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    meta = config.get("meta") or {}
    ads = config.get("ads") or {}
    whatsapp_config = tenant_dir / "whatsapp" / "config.json"
    has_wa = whatsapp_config.is_file()
    has_meta = bool(meta.get("page_id") or meta.get("ig_user_id"))
    has_ads = bool(ads.get("ad_account_id"))

    found = []
    if has_meta:
        found.append("meta")
    if has_wa:
        found.append("whatsapp")
    if has_ads:
        found.append("ads")

    if not found:
        return _check(
            "channels",
            "Canales conectados",
            WARN,
            "Sin canales declarados en config.",
            "Configurar Meta, WhatsApp o Ads",
        )
    missing = [name for name, ok in (("meta", has_meta), ("whatsapp", has_wa), ("ads", has_ads)) if not ok]
    if missing:
        return _check(
            "channels",
            "Canales conectados",
            WARN,
            f"Conectados: {', '.join(found)}. Faltan: {', '.join(missing)}.",
            "Conectar los canales faltantes",
        )
    return _check("channels", "Canales conectados", PASS, ", ".join(found))


def _check_schedule(tenant_dir: Path) -> Dict[str, Any]:
    candidates = list(tenant_dir.glob("meta_import*.csv")) + list(
        tenant_dir.glob("future_schedule.csv")
    )
    if not candidates:
        return _check(
            "schedule",
            "Calendario de publicación",
            WARN,
            "Sin meta_import*.csv ni future_schedule.csv.",
            "Crear el calendario del tenant",
        )
    latest = max(candidates, key=lambda path: path.stat().st_mtime)
    return _check("schedule", "Calendario de publicación", PASS, f"Usando {latest.name}.")


def _check_sync(tenant_dir: Path) -> Dict[str, Any]:
    path = tenant_dir / "data" / "sync" / "latest.json"
    if not path.is_file():
        return _check(
            "sync",
            "Snapshot del sync",
            WARN,
            "No hay data/sync/latest.json.",
            "Ejecutar scripts/sync_all.py para el tenant",
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        stamp = payload.get("generated_at") or payload.get("timestamp")
        when = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        age_days = (datetime.now(timezone.utc) - when).days
    except Exception:
        return _check("sync", "Snapshot del sync", WARN, "Snapshot ilegible o sin fecha.")
    if age_days > SYNC_MAX_AGE_DAYS:
        return _check(
            "sync",
            "Snapshot del sync",
            WARN,
            f"Snapshot de hace {age_days} días.",
            "Volver a correr el sync",
        )
    return _check("sync", "Snapshot del sync", PASS, f"Actualizado hace {age_days} días.")


def _check_history(tenant_dir: Path, track: str) -> Dict[str, Any]:
    if track != "native_digital":
        return _check(
            "history",
            "Histórico de contenido",
            SKIP,
            "Solo aplica a tenants native_digital.",
        )
    if (tenant_dir / "historical").is_dir():
        return _check("history", "Histórico de contenido", PASS, "historical/ presente.")
    return _check(
        "history",
        "Histórico de contenido",
        WARN,
        "Sin carpeta historical/.",
        "Cargar histórico para habilitar reuse",
    )


def audit_tenant(tenant_id: str, base_path: Optional[str] = None) -> Dict[str, Any]:
    """Audita un tenant y devuelve checks, estado y siguientes acciones."""
    root = Path(base_path) if base_path else _project_root()
    tenant_dir = root / "tenants" / tenant_id

    if not tenant_dir.is_dir():
        return {
            "tenant_id": tenant_id,
            "track": "",
            "status": BLOCKED,
            "score": 0.0,
            "checks": [
                _check(
                    "config",
                    "Configuración del tenant",
                    FAIL,
                    f"No existe el directorio tenants/{tenant_id}.",
                    "Crear el tenant con su config.json",
                )
            ],
            "next_actions": ["Crear el tenant con su config.json"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    try:
        config = _load_config(tenant_dir)
    except Exception as exc:
        return {
            "tenant_id": tenant_id,
            "track": "",
            "status": BLOCKED,
            "score": 0.0,
            "checks": [
                _check(
                    "config",
                    "Configuración del tenant",
                    FAIL,
                    f"config.json inválido: {type(exc).__name__}",
                    "Corregir config.json",
                )
            ],
            "next_actions": ["Corregir config.json"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    track = str(config.get("tenant_type") or "")
    checks: List[Dict[str, Any]] = [
        _check_config(config),
        _check_track(config),
        _check_brand(tenant_id, root),
        _check_assets(tenant_dir),
        _check_inventory(tenant_id, config, root),
        _check_channels(tenant_dir, config),
        _check_schedule(tenant_dir),
        _check_sync(tenant_dir),
        _check_history(tenant_dir, track),
    ]

    applicable = [item for item in checks if item["state"] != SKIP]
    passed = [item for item in applicable if item["state"] == PASS]
    score = round(len(passed) / len(applicable), 2) if applicable else 0.0

    if any(item["state"] == FAIL and item["id"] == "config" for item in checks):
        status = BLOCKED
    elif any(item["state"] in (WARN, FAIL) for item in checks):
        status = PARTIAL
    else:
        status = READY

    next_actions = [item["action"] for item in checks if item["action"] and item["state"] != PASS]

    return {
        "tenant_id": tenant_id,
        "track": track,
        "status": status,
        "score": score,
        "checks": checks,
        "next_actions": next_actions,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Audita un tenant de Growth OS.")
    parser.add_argument("tenant_id")
    parser.add_argument("--base-path", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = audit_tenant(args.tenant_id, args.base_path)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['tenant_id']}: {result['status']} ({result['score']})")
        for item in result["checks"]:
            print(f"  [{item['state']}] {item['name']}: {item['detail']}")
    return 0 if result["status"] != BLOCKED else 1


if __name__ == "__main__":
    raise SystemExit(main())
