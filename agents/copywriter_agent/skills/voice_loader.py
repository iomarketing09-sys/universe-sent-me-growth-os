"""Carga y resume el perfil de voz de un tenant."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class VoiceProfileError(ValueError):
    """El tenant no tiene un perfil de voz utilizable."""


def load_voice_profile(tenant_path: Path) -> Dict[str, Any]:
    """Carga `tenants/<id>/brand_voice.json` y valida lo mínimo necesario."""
    path = tenant_path / "brand_voice.json"
    if not path.is_file():
        raise VoiceProfileError(
            f"No existe el perfil de voz del tenant: {path}. "
            "El Copywriter Agent no usa la voz de otro tenant."
        )

    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise VoiceProfileError(f"brand_voice.json inválido: {exc}") from exc

    if not profile.get("brand_identity", {}).get("name"):
        raise VoiceProfileError("brand_voice.json no tiene brand_identity.name")
    if not profile.get("voice_attributes"):
        raise VoiceProfileError("brand_voice.json no tiene voice_attributes")

    profile["_source_path"] = str(path)
    return profile


def voice_summary(profile: Dict[str, Any]) -> str:
    """Resumen compacto para el prompt; no sustituye al perfil completo."""
    identity = profile.get("brand_identity", {})
    attrs = profile.get("voice_attributes", {})
    vocab = profile.get("vocabulary", {})
    compliance = profile.get("compliance", {})
    patterns = profile.get("messaging_patterns", {})

    lines = [
        f"Marca: {identity.get('name', '')}",
        f"Tagline: {identity.get('tagline', '')}",
        f"Propuesta de valor: {identity.get('value_proposition', '')}",
        f"Tono: {attrs.get('tone', '')}",
        f"Formalidad: {attrs.get('formality', '')}",
        f"Perspectiva: {attrs.get('perspective', '')}",
        f"Emojis: {attrs.get('emoji_usage', '')}",
        "Diferenciadores: " + "; ".join(identity.get("differentiators", [])[:6]),
        "Vocabulario preferido: " + "; ".join(vocab.get("preferred", [])[:12]),
        "Vocabulario a evitar: " + "; ".join(vocab.get("avoid", [])[:12]),
        "Claims prohibidos: " + "; ".join(compliance.get("prohibited_claims", [])[:12]),
        "Aperturas de ejemplo: " + " | ".join(patterns.get("opening", [])[:3]),
        "CTAs suaves: " + " | ".join(patterns.get("cta_soft", [])[:3]),
    ]

    sub_brands = profile.get("sub_brands", {})
    if sub_brands:
        lines.append(
            "Sub-marcas: "
            + "; ".join(
                f"{name}: {data.get('tagline', '')}" for name, data in sub_brands.items()
            )
        )

    evidence = profile.get("published_copy_evidence", {})
    if evidence.get("posts_analyzed"):
        lines.append(
            "Copy publicado analizado: "
            f"{evidence['posts_analyzed']} posts "
            f"(mediana {evidence.get('length', {}).get('median_chars', '?')} caracteres)"
        )

    return "\n".join(line for line in lines if line.strip())


def compact_evidence(profile: Dict[str, Any], max_examples: int = 3) -> Dict[str, Any]:
    """Reduce la evidencia de copy publicado para el prompt del copywriter."""
    evidence = profile.get("published_copy_evidence", {}) or {}
    if not evidence.get("posts_analyzed"):
        return {}

    examples = evidence.get("signature_examples", [])[:max_examples]
    return {
        "posts_analyzed": evidence.get("posts_analyzed"),
        "period": evidence.get("period", {}),
        "length": evidence.get("length", {}),
        "emoji": evidence.get("emoji", {}),
        "openings": evidence.get("openings", [])[:3],
        "recurring_words": evidence.get("recurring_words", [])[:10],
        "recurring_phrases": evidence.get("recurring_phrases", [])[:8],
        "local_markers": evidence.get("local_markers", [])[:4],
        "observed_patterns": evidence.get("observed_patterns", [])[:6],
        "ad_translation": evidence.get("ad_translation", []),
        "signature_examples": [
            {"text": item.get("text", ""), "why": item.get("why", "")}
            for item in examples
        ],
    }
