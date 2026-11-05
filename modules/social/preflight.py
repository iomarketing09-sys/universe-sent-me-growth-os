"""Preflight local de publicación para Instagram.

Valida lo que puede fallar antes de llamar a Meta: credenciales, host,
formato soportado, existencia del asset y dimensiones. La comprobación remota
de permisos es opcional y nunca corre por defecto.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from modules.social.ig_publisher import (
    IMAGE_HOSTS,
    get_meta_tokens,
    load_tenant_credentials,
)

SUPPORTED_FEED_TYPES = {"", "PHOTO", "IMAGE", "CAROUSEL"}
MAX_CAROUSEL_ITEMS = 20
SUPPORTED_FORMATS = {"JPEG", "PNG"}
MIN_ASPECT_RATIO = 4 / 5
MAX_ASPECT_RATIO = 1.91
MIN_DIMENSION = 320
MAX_IMAGE_BYTES = 8 * 1024 * 1024


@dataclass
class PreflightResult:
    tenant_id: str
    ok: bool = True
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    checks: List[Dict[str, Any]] = field(default_factory=list)

    def add(self, check: str, status: str, detail: str) -> None:
        self.checks.append({"check": check, "status": status, "detail": detail})
        if status == "fail":
            self.ok = False
            self.issues.append(f"{check}: {detail}")
        elif status == "warn":
            self.warnings.append(f"{check}: {detail}")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _find_asset(asset_root: Path, filename: str) -> Optional[Path]:
    if not asset_root.is_dir():
        return None
    for root, _dirs, files in os.walk(asset_root, followlinks=True):
        if filename in files:
            return Path(root) / filename
    return None


def _check_image(path: Path, result: PreflightResult) -> None:
    size = path.stat().st_size
    if size <= 0:
        result.add("asset:size", "fail", f"{path.name} está vacío")
        return
    if size > MAX_IMAGE_BYTES:
        result.add(
            "asset:size",
            "fail",
            f"{path.name} pesa {size / (1024 * 1024):.1f} MB; máximo 8 MB",
        )
    else:
        result.add("asset:size", "ok", f"{path.name}: {size / 1024:.0f} KB")

    try:
        from PIL import Image

        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
            image_format = str(image.format or "").upper()
    except Exception as exc:
        result.add("asset:image", "fail", f"{path.name} no es una imagen legible: {exc}")
        return

    if image_format not in SUPPORTED_FORMATS:
        result.add(
            "asset:format",
            "fail",
            f"{path.name}: formato {image_format or 'desconocido'} no soportado; usar JPEG o PNG",
        )
    else:
        result.add("asset:format", "ok", f"{path.name}: {image_format}")

    if min(width, height) < MIN_DIMENSION:
        result.add(
            "asset:dimensions",
            "fail",
            f"{path.name}: {width}x{height}; mínimo {MIN_DIMENSION}px por lado",
        )
        return

    result.add("asset:dimensions", "ok", f"{path.name}: {width}x{height}")

    ratio = width / height if height else 0
    if not (MIN_ASPECT_RATIO <= ratio <= MAX_ASPECT_RATIO):
        result.add(
            "asset:aspect",
            "fail",
            f"{path.name}: relación {ratio:.2f}; Instagram feed acepta 4:5 a 1.91:1",
        )
    else:
        result.add("asset:aspect", "ok", f"{path.name}: {width}x{height} ({ratio:.2f})")


def _check_remote_permissions(tenant_id: str, creds: Dict[str, str], result: PreflightResult) -> None:
    try:
        import requests

        page_token, ig_id = get_meta_tokens(creds["META_ACCESS_TOKEN"], creds["FB_PAGE_ID"])
        response = requests.get(
            f"https://graph.facebook.com/v19.0/{ig_id}/content_publishing_limit",
            params={"fields": "quota_usage,quota_total", "access_token": page_token},
            timeout=20,
        )
        payload = response.json()
        if response.status_code != 200 or "error" in payload:
            result.add("permissions:instagram", "fail", f"Meta rechazó la consulta: {payload}")
        else:
            result.add(
                "permissions:instagram",
                "ok",
                f"IG {ig_id} puede consultar su límite de publicación",
            )
    except Exception as exc:
        result.add("permissions:instagram", "fail", f"No se pudo validar permiso: {exc}")


def preflight_tenant(
    tenant_id: str,
    *,
    item: Any = None,
    base_path: Optional[Path] = None,
    check_remote: bool = False,
) -> PreflightResult:
    root = Path(base_path) if base_path else Path.cwd()
    result = PreflightResult(tenant_id=tenant_id)

    try:
        creds = load_tenant_credentials(tenant_id, base_path=root)
        result.add("credentials", "ok", "FB_PAGE_ID y META_ACCESS_TOKEN presentes")
    except Exception as exc:
        result.add("credentials", "fail", str(exc))
        return result

    host = str(creds.get("IMAGE_HOST") or "imgbb").strip().lower()
    if host not in IMAGE_HOSTS:
        result.add("image_host", "fail", f"IMAGE_HOST inválido: {host}")
    elif host == "catbox":
        result.add(
            "image_host",
            "fail",
            "catbox no es apto para producción; migrar a imgbb, R2 o S3",
        )
    else:
        result.add("image_host", "ok", host)

    asset_root = root / "tenants" / tenant_id / "assets"
    if not asset_root.is_dir():
        result.add("assets", "fail", f"No existe {asset_root}")

    if item is not None:
        post_type = str(getattr(item, "post_type", "") or "").strip().upper()
        if post_type not in SUPPORTED_FEED_TYPES:
            result.add(
                "format",
                "fail",
                f"Post Type {post_type} no soportado por el publisher actual (Fase 3)",
            )
        else:
            result.add("format", "ok", post_type or "PHOTO")

        media_value = str(getattr(item, "media_filename", "") or "").strip()
        filenames = [name.strip() for name in media_value.split("|") if name.strip()]
        if not filenames:
            result.add("asset", "fail", "El slot no tiene media")
        elif post_type == "CAROUSEL" and len(filenames) < 2:
            result.add("asset", "fail", "El carrusel necesita al menos dos imágenes")
        elif post_type == "CAROUSEL" and len(filenames) > MAX_CAROUSEL_ITEMS:
            result.add(
                "asset",
                "fail",
                f"El carrusel tiene {len(filenames)} imágenes; máximo {MAX_CAROUSEL_ITEMS}",
            )
        else:
            for filename in filenames:
                asset_path = _find_asset(asset_root, filename)
                if asset_path is None:
                    result.add("asset", "fail", f"Asset no encontrado: {filename}")
                    continue
                result.add("asset", "ok", str(asset_path))
                _check_image(asset_path, result)

    if check_remote:
        _check_remote_permissions(tenant_id, creds, result)

    return result


def preflight_items(
    tenant_id: str,
    items: Iterable[Any],
    *,
    base_path: Optional[Path] = None,
    check_remote: bool = False,
) -> List[PreflightResult]:
    return [
        preflight_tenant(
            tenant_id,
            item=item,
            base_path=base_path,
            check_remote=check_remote,
        )
        for item in items
    ]


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    from modules.social.ig_scheduler import parse_tenant_schedule

    parser = argparse.ArgumentParser(description="Preflight de publicación Instagram")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--remote", action="store_true", help="Validar permisos contra Meta")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = preflight_tenant(args.tenant, check_remote=args.remote)
    schedule = parse_tenant_schedule(args.tenant)
    item_results = preflight_items(
        args.tenant,
        schedule,
        check_remote=args.remote,
    )
    payload = {
        "tenant": result.to_dict(),
        "items": [entry.to_dict() for entry in item_results],
        "ok": result.ok and all(entry.ok for entry in item_results),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"[{'OK' if payload['ok'] else 'BLOCKED'}] preflight · {args.tenant}")
        for check in result.checks:
            print(f"  - {check['check']}: {check['status']} · {check['detail']}")
        for entry, schedule_item in zip(item_results, schedule):
            state = "OK" if entry.ok else "BLOCKED"
            print(f"  - slot {schedule_item.date_str} {schedule_item.time_str}: {state}")
            for issue in entry.issues:
                print(f"      fail: {issue}")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
