"""Caption para publicación orgánica usando la voz del tenant.

Extiende el Copywriter Agent al caso que no es anuncio: un meme o imagen ya
existe y solo hace falta el caption. Reusa el mismo perfil de voz
(``tenants/<id>/brand_voice.json``) y el mismo cliente de OmniRoute.

Regla central: el caption no repite el chiste. Si el modelo devuelve el mismo
texto del meme, se reintenta una vez y, si vuelve a fallar, se levanta
``CaptionError`` en vez de publicar algo plano.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from .skills.omni_client import (
    DEFAULT_MODEL,
    FALLBACK_MODELS,
    OmniRouteClient,
    extract_json,
)
from .skills.voice_loader import load_voice_profile, voice_summary


MAX_CAPTION_CHARS = 100
PILLARS = (
    "Humor Existencial",
    "Sabiduría Práctica",
    "Lore",
    "Comunidad / UGC",
)


class CaptionError(ValueError):
    """No se pudo generar un caption usable."""


def _normalize(text: str) -> str:
    """Minúsculas, sin acentos y sin signos, para comparar similitud."""
    decomposed = unicodedata.normalize("NFKD", text or "")
    plain = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(
        "".join(char if char.isalnum() else " " for char in plain.lower()).split()
    )


def build_social_messages(
    voice: Dict[str, Any],
    *,
    meme_text: str,
    characters: Sequence[str],
    pillar: str,
    platform: str = "Instagram",
    avoid_openers: Sequence[str] = (),
) -> List[Dict[str, str]]:
    """Arma el prompt de caption orgánico a partir de la voz del tenant."""
    organic = (voice.get("channel_rules", {}) or {}).get("organic_social", {}) or {}
    anti_tono = organic.get("anti_tono", []) or []
    caption_rule = organic.get(
        "caption_rule", "El caption no repite el chiste; lo aterriza en una línea."
    )
    avoid = (voice.get("vocabulary", {}) or {}).get("avoid", []) or []

    system = "\n".join(
        [
            "Eres el copywriter de Universe Sent Me. Escribes captions de una o dos líneas",
            "para memes que ya existen. No explicas el chiste, no lo repites y no moralizas.",
            "",
            "## Voz del tenant",
            voice_summary(voice),
            "",
            "## Límites obligatorios",
            *[f"- {rule}" for rule in anti_tono],
            f"- {caption_rule}",
            "- Español mexicano coloquial, tuteo, sin emojis salvo que el chiste lo pida.",
            "- UNA sola frase de máximo 12 palabras. Sin remate, sin segunda cláusula.",
            "- No repitas ni parafrasees el texto del meme: cambia el ángulo, no lo alargues.",
            "- Sin hashtags: los agrega el sistema.",
            "- No inventes nombres propios que no aparezcan en el texto del meme.",
            "Vocabulario prohibido: " + ", ".join(avoid),
            "",
            "Las aperturas de ejemplo del perfil son referencia de tono: no las copies",
            "literalmente, ni siquiera cambiando una palabra.",
            "El pilar se decide por el tipo de chiste, no por el personaje: un meme de",
            "cualquier personaje puede ser Humor Existencial.",
            "Pilares válidos: " + ", ".join(PILLARS),
            *(
                ["No empieces con estas frases, ya se usaron: " + " | ".join(avoid_openers)]
                if avoid_openers
                else []
            ),
            "Devuelve solo JSON: {\"caption\": \"...\", \"pillar\": \"...\"}",
        ]
    )
    user = "\n".join(
        [
            f"Plataforma: {platform}",
            f"Pilar: {pillar}",
            f"Personaje(s): {', '.join(characters) or 'Universe'}",
            f"Texto que ya trae el meme: {meme_text}",
            "Escribe el caption.",
        ]
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def _parse_response(content: str) -> tuple[str, str, bool]:
    """Extrae caption y pilar. ``parsed`` es False si el JSON vino incompleto."""
    parsed = True
    try:
        data = extract_json(content)
    except Exception:  # el modelo a veces devuelve texto plano o JSON cortado
        data = {}
        parsed = False

    caption = str(data.get("caption") or "").strip()
    if not caption:
        match = re.search(r'"caption"\s*:\s*"(.*?)(?:"\s*,|"\s*$|$)', content, re.S)
        caption = match.group(1) if match else ""
    if not caption:
        caption = content.strip().strip('"')
    if caption.startswith("{"):
        caption = ""

    pillar = " ".join(str(data.get("pillar") or "").split())
    if not pillar:
        match = re.search(r'"pillar"\s*:\s*"([^"]*)"?', content)
        pillar = match.group(1).strip() if match else ""
    if parsed and not caption:
        parsed = False
    return " ".join(caption.split()), pillar, parsed


def trim_caption(caption: str) -> str:
    """Deja una sola frase: si el modelo agregó remate, se descarta."""
    cap = " ".join((caption or "").split())
    if not cap:
        return ""
    first = re.split(r"(?<=[.!?])\s+", cap)[0].strip()
    if len(first) >= 15:
        cap = first
    if len(cap) > MAX_CAPTION_CHARS:
        cap = cap[:MAX_CAPTION_CHARS].rsplit(" ", 1)[0].strip()
    return cap.rstrip(",;:")


def is_usable(caption: str) -> bool:
    """Descarta captions vacíos, cortados a media palabra o demasiado cortos."""
    cap = (caption or "").strip()
    if len(cap) < 15:
        return False
    if cap[-1] in ".!?…)\"":
        return True
    # Sin puntuación final: aceptar solo si termina en palabra completa y larga.
    return len(cap.split()) >= 4 and cap.split()[-1].isalpha() and len(cap.split()[-1]) >= 3


def is_duplicate(caption: str, meme_text: str) -> bool:
    """True si el caption solo repite el chiste."""
    normalized_caption = _normalize(caption)
    normalized_meme = _normalize(meme_text)
    if not normalized_caption or not normalized_meme:
        return False
    if normalized_caption == normalized_meme:
        return True
    if normalized_meme in normalized_caption and len(normalized_caption) <= len(normalized_meme) + 12:
        return True
    return False


def generate_caption(
    tenant_id: str,
    *,
    meme_text: str,
    characters: Sequence[str],
    pillar: str,
    platform: str = "Instagram",
    base_path: Optional[Path] = None,
    client: Optional[OmniRouteClient] = None,
    avoid_openers: Sequence[str] = (),
    avoid_phrases: Sequence[str] = (),
) -> Dict[str, Any]:
    """Genera el caption de un post orgánico y valida que no repita el chiste."""
    root = Path(base_path) if base_path else Path(__file__).resolve().parents[4]
    voice = load_voice_profile(root / "tenants" / tenant_id)
    messages = build_social_messages(
        voice,
        meme_text=meme_text,
        characters=characters,
        pillar=pillar,
        platform=platform,
        avoid_openers=avoid_openers,
    )
    client = client or OmniRouteClient()
    models = (DEFAULT_MODEL, *FALLBACK_MODELS)

    last_caption = ""
    for attempt in range(3):
        result = client.chat_with_fallback(messages, models, max_tokens=500, temperature=0.8)
        last_caption, chosen_pillar, parsed = _parse_response(result.content)
        last_caption = trim_caption(last_caption)
        repeated = [
            phrase
            for phrase in avoid_phrases
            if _normalize(phrase) and _normalize(phrase) in _normalize(last_caption)
        ]
        if (
            parsed
            and is_usable(last_caption)
            and not is_duplicate(last_caption, meme_text)
            and not repeated
        ):
            return {
                "tenant_id": tenant_id,
                "caption": last_caption,
                "model": result.model,
                "meme_text": meme_text,
                "pillar": chosen_pillar if chosen_pillar in PILLARS else pillar,
                "characters": list(characters),
            }
        messages = messages + [
            {"role": "assistant", "content": last_caption or "(vacío)"},
            {
                "role": "user",
                "content": (
                    "Eso no sirve: repite el chiste, repite frases de otros captions "
                    "o salió corto. Escribe otra versión distinta, una sola frase, "
                    "sin parafrasear el texto del meme."
                ),
            },
        ]

    raise CaptionError(
        f"El caption repite el chiste o salió vacío para: {meme_text[:80]!r}"
    )
