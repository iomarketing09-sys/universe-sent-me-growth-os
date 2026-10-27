"""Selección de imágenes reales de producto para piezas creativas.

Regla del sistema: solo se usan modelos que están en el inventario del tenant
(``config.ads.approved_models``). El material de marca puede venir de cualquier
fuente aprobada, pero el producto siempre es real.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ACCESSORY_HINTS = ("bolsa", "cartera", "cinturon", "calcetin", "accesorio")
DETAIL_HINTS = ("detalle", "detail", "suela", "suela_", "closeup", "close_up")
NINE_VIEW_HINTS = ("nine", "9v", "nineview", "nine_view")

DEFAULT_MAX_PER_MODEL = 5
DEFAULT_MAX_TOTAL = 8


def project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[1]


def _tenant_path(tenant_id: str, base_path: Optional[str] = None) -> Path:
    root = Path(base_path) if base_path else project_root()
    return root / "tenants" / tenant_id


def load_approved_models(
    tenant_id: str, base_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Modelos aprobados/inventario del tenant, según ``config.ads``."""
    config_path = _tenant_path(tenant_id, base_path) / "config.json"
    if not config_path.is_file():
        raise FileNotFoundError(f"No existe config.json para el tenant: {tenant_id}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    return list((config.get("ads") or {}).get("approved_models") or [])


def _classify(filename: str, model_code: str) -> str:
    stem = Path(filename).stem.lower()
    if any(hint in stem for hint in ACCESSORY_HINTS):
        return "complemento"
    if any(hint in stem for hint in DETAIL_HINTS):
        return "detalle"
    if any(hint in stem for hint in NINE_VIEW_HINTS):
        return "nine_view"
    others = {
        token
        for token in re.findall(r"(?<!\d)\d{6}(?!\d)", stem)
        if token != str(model_code)
    }
    return "combo" if others else "producto"


def _dedupe_key(filename: str) -> str:
    """``JOCELYN_TAN (1).jpg`` y ``JOCELYN_TAN.jpg`` son el mismo asset."""
    stem = Path(filename).stem.lower().strip()
    stem = re.sub(r"\s*\(\d+\)$", "", stem)
    stem = re.sub(r"_copia$", "", stem)
    return stem


def _copy_rank(filename: str) -> tuple:
    """Prefiere el archivo original sobre ``nombre (1).jpg``."""
    stem = Path(filename).stem
    has_copy_suffix = bool(re.search(r"\s*\(\d+\)$", stem))
    return (has_copy_suffix, Path(filename).suffix.isupper(), filename)


def _find_asset_dir(tenant_dir: Path, model: Dict[str, Any]) -> Optional[Path]:
    """Directorio declarado en config o, si no coincide, búsqueda por código."""
    declared = model.get("asset_dir")
    if declared and (tenant_dir / declared).is_dir():
        return tenant_dir / declared
    code = str(model.get("code", "")).strip()
    assets = tenant_dir / "assets"
    if code and assets.is_dir():
        for candidate in sorted(assets.glob(f"*/*/{code}")):
            if candidate.is_dir():
                return candidate
    return None


def _score(entry: Dict[str, Any]) -> tuple:
    """Orden de preferencia: producto solo > nine view > detalle > combo > complemento."""
    rank = {
        "producto": 0,
        "nine_view": 1,
        "detalle": 2,
        "combo": 3,
        "complemento": 4,
    }[entry["kind"]]
    return (rank, entry["filename"].lower())


def list_model_assets(
    tenant_id: str,
    model: Dict[str, Any],
    base_path: Optional[str] = None,
    max_images: int = DEFAULT_MAX_PER_MODEL,
) -> List[Dict[str, Any]]:
    """Imágenes de un modelo, sin duplicados por mayúsculas/minúsculas."""
    code = str(model.get("code", "")).strip()
    if not code:
        return []
    tenant_dir = _tenant_path(tenant_id, base_path)
    asset_dir = _find_asset_dir(tenant_dir, model)
    if asset_dir is None:
        return []

    seen: Dict[str, Dict[str, Any]] = {}
    for path in sorted(asset_dir.iterdir(), key=lambda p: _copy_rank(p.name)):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        key = _dedupe_key(path.name)
        if key in seen:
            continue
        seen[key] = {
            "model_code": code,
            "model_name": model.get("name", ""),
            "brand": model.get("brand", ""),
            "filename": path.name,
            "path": str(path.relative_to(_tenant_path(tenant_id, base_path))),
            "kind": _classify(path.name, code),
        }

    ordered = sorted(seen.values(), key=_score)
    return ordered[:max_images] if max_images else ordered


def select_campaign_assets(
    tenant_id: str,
    campaign_slug: Optional[str] = None,
    base_path: Optional[str] = None,
    max_per_model: int = DEFAULT_MAX_PER_MODEL,
    max_total: int = DEFAULT_MAX_TOTAL,
    model_codes: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """Selecciona imágenes por modelo de la campaña, respetando el inventario."""
    models = load_approved_models(tenant_id, base_path)
    wanted = {str(code) for code in model_codes} if model_codes else None
    approved_codes = [str(model.get("code")) for model in models]
    not_in_inventory: List[str] = []
    if wanted:
        not_in_inventory = sorted(wanted - set(approved_codes))
        models = [m for m in models if str(m.get("code")) in wanted]

    selection: List[Dict[str, Any]] = []
    missing: List[str] = list(not_in_inventory)
    for model in models:
        assets = list_model_assets(
            tenant_id, model, base_path=base_path, max_images=max_per_model
        )
        if not assets:
            missing.append(str(model.get("code")))
            continue
        selection.extend(assets)

    if max_total:
        selection = selection[:max_total]

    return {
        "tenant_id": tenant_id,
        "campaign_slug": campaign_slug,
        "approved_models": approved_codes,
        "models_not_in_inventory": not_in_inventory,
        "models_without_assets": missing,
        "max_per_model": max_per_model,
        "max_total": max_total,
        "selected": selection,
        "total": len(selection),
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Selector de imágenes por modelo")
    parser.add_argument("tenant")
    parser.add_argument("--campaign", default=None)
    parser.add_argument("--base-path", default=None)
    parser.add_argument("--max-per-model", type=int, default=DEFAULT_MAX_PER_MODEL)
    parser.add_argument("--max-total", type=int, default=DEFAULT_MAX_TOTAL)
    parser.add_argument("--models", nargs="*", default=None)
    args = parser.parse_args()

    result = select_campaign_assets(
        args.tenant,
        campaign_slug=args.campaign,
        base_path=args.base_path,
        max_per_model=args.max_per_model,
        max_total=args.max_total,
        model_codes=args.models,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
