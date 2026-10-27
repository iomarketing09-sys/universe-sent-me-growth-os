"""Kit de marca por tenant: colores, tipografía y reglas visuales.

El kit se lee de ``tenants/<id>/brand_kit.json``. Si el tenant no tiene archivo
propio, se arma un kit mínimo desde ``config.json`` y ``brand_voice.json`` para
que el módulo nunca invente material de otra marca.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_RULES = {
    "solo_modelos_en_inventario": True,
    "no_precio_en_arte": True,
    "no_stock_en_arte": True,
    "logo_obligatorio": True,
}


def project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[1]


def tenant_path(tenant_id: str, base_path: Optional[str] = None) -> Path:
    root = Path(base_path) if base_path else project_root()
    return root / "tenants" / tenant_id


def load_brand_kit(tenant_id: str, base_path: Optional[str] = None) -> Dict[str, Any]:
    """Devuelve el kit visual del tenant, aislado por tenant."""
    path = tenant_path(tenant_id, base_path)
    kit_path = path / "brand_kit.json"
    if kit_path.is_file():
        kit = json.loads(kit_path.read_text(encoding="utf-8"))
        kit.setdefault("tenant_id", tenant_id)
        kit.setdefault("source", str(kit_path))
        kit["rules"] = {**DEFAULT_RULES, **(kit.get("rules") or {})}
        return kit

    config_path = path / "config.json"
    voice_path = path / "brand_voice.json"
    if not config_path.is_file():
        raise FileNotFoundError(f"No existe config.json para el tenant: {tenant_id}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    voice = (
        json.loads(voice_path.read_text(encoding="utf-8"))
        if voice_path.is_file()
        else {}
    )
    guidelines = config.get("brand_guidelines", {}) or {}
    identity = voice.get("brand_identity", {}) or {}

    return {
        "tenant_id": tenant_id,
        "source": str(config_path),
        "brand": identity.get("name") or config.get("business_name") or tenant_id,
        "tagline": identity.get("tagline", ""),
        "voice": guidelines.get("brand_voice", ""),
        "palette": [],
        "typography": {"status": "pendiente"},
        "hashtags": guidelines.get("approved_hashtags", []),
        "content_pillars": guidelines.get("content_pillars", []),
        "logo": {},
        "rules": dict(DEFAULT_RULES),
    }


def palette_hex(tenant_id: str, base_path: Optional[str] = None) -> Dict[str, str]:
    """Paleta como ``{nombre: hex}``, útil para generar piezas."""
    kit = load_brand_kit(tenant_id, base_path)
    return {
        str(color.get("name")): str(color.get("hex"))
        for color in kit.get("palette", [])
        if color.get("name") and color.get("hex")
    }


def logo_path(tenant_id: str, base_path: Optional[str] = None) -> Optional[Path]:
    """Ruta absoluta al logo principal, si el kit la declara."""
    kit = load_brand_kit(tenant_id, base_path)
    relative = (kit.get("logo") or {}).get("primary")
    if not relative:
        return None
    candidate = tenant_path(tenant_id, base_path) / relative
    return candidate if candidate.is_file() else None


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Kit de marca por tenant")
    parser.add_argument("tenant")
    parser.add_argument("--base-path", default=None)
    args = parser.parse_args()
    print(
        json.dumps(
            load_brand_kit(args.tenant, args.base_path),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
