#!/usr/bin/env python3
"""Llena el caption de los slots del plan con la voz del tenant.

Toma `plan_contenido.csv`, lee el texto del meme desde `Media URL` (convención
`<código> - <personajes> - <texto>`) y escribe el caption generado por el
Copywriter Agent en modo orgánico.

No publica ni programa: solo edita el plan. Los slots ya aprobados no se
reemplazan salvo que se pida con `--force`.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modules.creative.agents.copywriter_agent.social_post import (  # noqa: E402
    CaptionError,
    generate_caption,
)
from modules.creative.agents.copywriter_agent.skills.omni_client import (  # noqa: E402
    OmniRouteError,
)
from modules.intelligence.planner import (  # noqa: E402
    load_meme_text_index,
    parse_asset_filename,
)

# Muletillas de la voz: máximo una vez por semana para no sonar a plantilla.
SIGNATURES = (
    "no tiene nombre todavía",
    "me acabo de dar cuenta",
    "obvio que",
    "yo también",
)

FIELDS = [
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
]


def pillar_for(characters):
    mapping = {
        "Universe": "Humor Existencial",
        "El Ganso": "Humor Existencial",
        "Payaso": "Humor Existencial",
        "Wilfred": "Sabiduría Práctica",
        "Elara": "Sabiduría Práctica",
        "Kael": "Lore",
        "Maeve": "Lore",
        "Fantasma": "Lore",
    }
    for name in characters:
        if name in mapping:
            return mapping[name]
    return "Humor Existencial"


def _save(plan: Path, rows: list) -> None:
    with plan.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--plan", default=None)
    parser.add_argument("--force", action="store_true", help="reescribe captions existentes")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = Path(args.plan) if args.plan else ROOT / "tenants" / args.tenant / "plan_contenido.csv"
    if not plan.is_file():
        print(f"No existe el plan: {plan}", file=sys.stderr)
        return 1

    with plan.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    meme_index = load_meme_text_index(args.tenant)
    changed = 0
    used_openers: list[str] = []
    used_phrases: list[str] = []
    for row in rows:
        if row.get("Caption", "").strip() and not args.force:
            continue
        parsed = parse_asset_filename(row.get("Media URL", ""))
        meme_text = parsed.get("meme_text") or meme_index.get(row.get("Media URL", ""), "")
        characters = parsed.get("characters") or []
        if not meme_text:
            print(
                f"[falta] {row['Date (YYYY-MM-DD)']} {row['Time (HH:MM, 24h)']}: "
                f"{row.get('Media URL', '')!r} no trae chiste en el nombre; hay que escribirlo."
            )
            continue
        if args.dry_run:
            print(f"[dry] {row['Date (YYYY-MM-DD)']} {row['Time (HH:MM, 24h)']} "
                  f"{pillar_for(characters)} -> {meme_text[:70]}")
            continue
        try:
            result = generate_caption(
                args.tenant,
                meme_text=meme_text,
                characters=characters,
                pillar=pillar_for(characters),
                avoid_openers=used_openers,
                avoid_phrases=used_phrases,
            )
        except (CaptionError, OmniRouteError) as exc:
            print(f"[error] {row['Date (YYYY-MM-DD)']}: {exc}", file=sys.stderr)
            continue
        used_openers.append(" ".join(result["caption"].split()[:2]))
        for signature in SIGNATURES:
            if signature.lower() in result["caption"].lower():
                used_phrases.append(signature)
        row["Caption"] = result["caption"]
        row["Pilar"] = result["pillar"]
        changed += 1
        if not args.dry_run:
            _save(plan, rows)
        print(f"[ok] {row['Date (YYYY-MM-DD)']} {row['Time (HH:MM, 24h)']} · {result['caption']}")

    if not args.dry_run and changed:
        print(f"Escritos {changed} captions en {plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
