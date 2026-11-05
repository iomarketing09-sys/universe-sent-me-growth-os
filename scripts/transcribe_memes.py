#!/usr/bin/env python3
"""Transcribe el texto de un meme con un modelo de visión vía OmniRoute.

La imagen se manda en base64 desde este script al modelo; al chat solo regresa
texto. No abre visores ni carga la imagen en la conversación.

Escribe/actualiza `tenants/<id>/assets_meme_text.csv`, que el planner usa para
los assets cuyo nombre no trae el chiste. No renombra archivos.

Uso:
    python3 scripts/transcribe_memes.py --tenant universe --folder "05 Mayo" --limit 5
    python3 scripts/transcribe_memes.py --tenant universe --file "260548 - Wilfred.png"
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
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import requests  # noqa: E402

from modules.intelligence.planner import (  # noqa: E402
    default_assets_dir,
    default_reuse_dir,
    parse_asset_filename,
)

FIELDS = ["asset_ref", "filename", "folder", "meme_text", "status", "model", "source"]
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_MODEL = os.getenv("MEME_VISION_MODEL", "auto/vision")
BASE_URL = os.getenv("OMNIROUTE_BASE_URL", "http://127.0.0.1:20128/v1")

PROMPT = (
    "Transcribe LITERALMENTE todo el texto visible en esta imagen, respetando los "
    "saltos de línea. Si no hay texto, responde exactamente: SIN_TEXTO. "
    "No describas la imagen, no interpretes, no traduzcas, no agregues comillas."
)


class VisionError(RuntimeError):
    """El modelo de visión no respondió o no está disponible."""


def encode_image(path: Path, max_side: int = 768) -> str:
    from PIL import Image

    with Image.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((max_side, max_side))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=82)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def transcribe(path: Path, model: str = DEFAULT_MODEL, max_side: int = 768) -> str:
    api_key = os.getenv("OMNIROUTE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise VisionError("Falta OMNIROUTE_API_KEY.")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(path, max_side)}"
                        },
                    },
                ],
            }
        ],
        "max_tokens": 300,
        "temperature": 0,
    }
    response = requests.post(
        f"{BASE_URL.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=120,
    )
    if response.status_code != 200:
        raise VisionError(f"HTTP {response.status_code}: {response.text[:200]}")
    content = response.json()["choices"][0]["message"]["content"].strip()
    content = re.sub(r"^```(?:text|txt)?|```$", "", content).strip()
    if content.upper().startswith("SIN_TEXTO"):
        return ""
    # La marca de agua del handle no es parte del chiste.
    content = re.sub(r"@UniverseSentMe|#UniverseSentMe", " ", content, flags=re.IGNORECASE)
    return " ".join(content.split())


def load_index(path: Path) -> Dict[str, Dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row["filename"]: row for row in csv.DictReader(handle)}


def save_index(path: Path, index: Dict[str, Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for name in sorted(index):
            writer.writerow({field: index[name].get(field, "") for field in FIELDS})


def candidates(args) -> List[Path]:
    if args.file:
        return [Path(args.file)]
    root = Path(args.root) if args.root else (
        default_reuse_dir(args.tenant) if args.reuse else default_assets_dir(args.tenant)
    )
    if args.folder:
        root = root / args.folder
    if not root.is_dir():
        return []
    return [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in IMAGE_EXT
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tenant", default="universe")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--folder", default=None)
    parser.add_argument("--file", default=None)
    parser.add_argument("--reuse", action="store_true", help="usar la carpeta de publicados")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--force", action="store_true", help="re-transcribir aunque ya tenga texto")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    index_path = ROOT / "tenants" / args.tenant / "assets_meme_text.csv"
    index = load_index(index_path)
    done = 0
    for path in candidates(args)[: args.limit]:
        if args.file is None and path.name in index and index[path.name].get("meme_text") and not args.force:
            continue
        parsed = parse_asset_filename(path.name)
        if parsed["meme_text"] and not args.force:
            continue
        if args.dry_run:
            print(f"[dry] {path.name}")
            continue
        try:
            text = transcribe(path, model=args.model)
        except (VisionError, requests.RequestException, OSError) as exc:
            print(f"[error] {path.name}: {exc}", file=sys.stderr)
            continue
        index[path.name] = {
            "asset_ref": parsed["code"],
            "filename": path.name,
            "folder": path.parent.name,
            "meme_text": text,
            "status": "transcrito" if text else "sin_texto",
            "model": args.model,
            "source": "vision",
        }
        done += 1
        print(f"[ok] {path.name} -> {text[:90] or '(sin texto)'}")
        save_index(index_path, index)

    if not args.dry_run and done:
        print(f"{done} memes transcritos en {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
