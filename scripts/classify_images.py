#!/usr/bin/env python3
"""Clasifica imágenes de catálogo/campaña: producto solo vs persona visible.

Heurística por nombre/ruta (gratis) y verificación opcional con visión vía
OmniRoute. Escribe un CSV para decidir qué se conserva al limpiar assets.

Uso:
    python3 scripts/classify_images.py "ruta/a/fotos" --out data/image_classification.csv
    python3 scripts/classify_images.py "ruta/a/fotos" --vision --limit 20
"""

from __future__ import annotations

import argparse
import base64
import csv
import io
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

import requests


DEFAULT_BASE_URL = "http://127.0.0.1:20128/v1"
DEFAULT_MODEL = "auto/vision"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CSV_FIELDS = [
    "path", "filename", "product_code", "color", "folder",
    "heuristic_label", "heuristic_reason", "vision_label", "person_present",
    "person_count", "shot_type", "vision_confidence", "model", "error",
]

PRODUCT_ANGLES = re.compile(
    r"_(ADELANTE|ATRAS|LATERAL|DER|IZQ|ARRIBA|ABAJO|PAR|PERFIL|DETALLE|SUELA|INTERIOR)\b",
    re.IGNORECASE,
)
LIFESTYLE = re.compile(r"ESTILO\s*DE\s*VIDA|LIFESTYLE|_MODELO?\b", re.IGNORECASE)
WHATSAPP = re.compile(r"^IMG-\d{8}-WA\d+", re.IGNORECASE)
PRODUCT_CODE = re.compile(r"(?<!\d)(\d{6})(?!\d)")

VISION_PROMPT = (
    'Analiza esta foto de calzado. Responde SOLO JSON: {"person_present": true|false, '
    '"person_count": 0|1|2, "shot_type": "product_only"|"model"|"lifestyle"|"detail", '
    '"confidence": 0.0-1.0}. person_present=true si se ve cualquier parte de una persona.'
)


def iter_images(paths: list[Path]) -> list[Path]:
    images: list[Path] = []
    for path in paths:
        if path.is_dir():
            images.extend(
                item for item in sorted(path.rglob("*"))
                if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS
            )
        elif path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(path)
    return images


def heuristic_classification(path: Path) -> tuple[str, str]:
    name = path.name
    folder = str(path.parent).lower()
    if LIFESTYLE.search(name):
        return "person_likely", "nombre indica estilo de vida"
    if PRODUCT_ANGLES.search(name):
        return "product_only", "nombre incluye ángulo de catálogo"
    if WHATSAPP.match(name):
        return "unknown", "imagen de WhatsApp sin metadatos en el nombre"
    if "campaña" in folder or "campana" in folder:
        return "unknown", "carpeta de campaña: puede incluir modelo"
    return "unknown", "sin convención reconocible en el nombre"


def extract_product_code(filename: str) -> str:
    match = PRODUCT_CODE.search(filename)
    return match.group(1) if match else ""


def guess_color(filename: str) -> str:
    colors = ["NEGRO", "BLANCO", "BEIGE", "TAN", "CAFE", "CAFÉ", "MOKA", "CHERRY",
              "PLATA", "DORADO", "ROJO", "AZUL", "VERDE", "GRIS", "CHOCOLATE"]
    upper = filename.upper()
    for color in colors:
        if color in upper:
            return color
    return ""


def encode_for_vision(path: Path, max_side: int = 1024) -> str:
    from PIL import Image

    with Image.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((max_side, max_side))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def call_vision(path: Path, model: str, base_url: str, api_key: str, max_side: int) -> dict[str, Any]:
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": VISION_PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_for_vision(path, max_side)}"}},
            ],
        }],
        "max_tokens": 250,
        "temperature": 0,
    }
    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    content = re.sub(r"^```(?:json)?|```$", "", content, flags=re.MULTILINE).strip()
    start, end = content.find("{"), content.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"Respuesta sin JSON: {content[:120]}")
    return json.loads(content[start:end + 1])


def classify(path: Path, options: argparse.Namespace) -> dict[str, str]:
    label, reason = heuristic_classification(path)
    row = {
        "path": str(path),
        "filename": path.name,
        "product_code": extract_product_code(path.name),
        "color": guess_color(path.name),
        "folder": str(path.parent),
        "heuristic_label": label,
        "heuristic_reason": reason,
        "vision_label": "",
        "person_present": "",
        "person_count": "",
        "shot_type": "",
        "vision_confidence": "",
        "model": "",
        "error": "",
    }

    should_use_vision = options.vision and (
        options.vision_all or label != "product_only"
    )
    if not should_use_vision:
        return row

    api_key = os.getenv("OMNIROUTE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        row["error"] = "Falta OMNIROUTE_API_KEY/OPENAI_API_KEY"
        return row

    try:
        result = call_vision(path, options.model, options.base_url, api_key, options.max_side)
        person = bool(result.get("person_present"))
        row.update({
            "vision_label": "person" if person else "product_only",
            "person_present": "true" if person else "false",
            "person_count": str(result.get("person_count", "")),
            "shot_type": str(result.get("shot_type", "")),
            "vision_confidence": str(result.get("confidence", "")),
            "model": options.model,
        })
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"
    return row


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Carpetas o imágenes a clasificar")
    parser.add_argument("--out", type=Path, default=Path("data/image_classification.csv"))
    parser.add_argument("--vision", action="store_true", help="Verificar con modelo de visión")
    parser.add_argument("--vision-all", action="store_true", help="Usar visión también en product_only")
    parser.add_argument("--limit", type=int, default=0, help="Máximo de imágenes (0 = todas)")
    parser.add_argument("--model", default=os.getenv("OMNIROUTE_VISION_MODEL", DEFAULT_MODEL))
    parser.add_argument("--base-url", default=os.getenv("OMNIROUTE_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--max-side", type=int, default=1024, help="Lado máximo para redimensionar antes de visión")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    options = parse_args(argv)
    images = iter_images(options.paths)
    if options.limit:
        images = images[:options.limit]
    if not images:
        print("No se encontraron imágenes.", file=sys.stderr)
        return 1

    rows = []
    for index, image in enumerate(images, start=1):
        row = classify(image, options)
        rows.append(row)
        status = row["vision_label"] or row["heuristic_label"]
        print(f"[{index}/{len(images)}] {status:14} {image.name}")

    options.out.parent.mkdir(parents=True, exist_ok=True)
    with options.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    summary: dict[str, int] = {}
    for row in rows:
        key = row["vision_label"] or row["heuristic_label"]
        summary[key] = summary.get(key, 0) + 1
    print(f"\nTotal: {len(rows)} | {summary}")
    print(f"CSV: {options.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
