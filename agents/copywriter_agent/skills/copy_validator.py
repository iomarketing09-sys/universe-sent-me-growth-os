"""Validación local y determinista del copy antes de proponerlo."""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, Iterable, List, Sequence, Tuple


MAX_HEADLINE = 40
MAX_PRIMARY = 125
MAX_DESCRIPTION = 30

# Bloqueos adicionales que no dependen del tenant. Se aplican siempre.
HARD_BLOCKED = (
    "precio",
    "costo",
    "stock",
    "disponible",
    "disponibilidad",
    "existencia",
    "apartado",
    "talla",
    "tallas",
    "color",
    "colores",
    "promocion",
    "descuento",
    "oferta",
    "compra",
    "comprar",
    "online",
    "tienda fisica",
    "envio",
    "gratis",
    "meses sin intereses",
    "msi",
    "2x1",
    "cumpleanos",
    "garantizado",
    "garantia",
    "asegurada",
    "calidad asegurada",
    "el mejor",
    "los mejores",
    "numero 1",
    "#1",
    "cientos de clientes",
    "clientes satisfechos",
    "client",
    "recomiend",
    "eleccion",
    "eligen",
    "prefieren",
    "favorit",
    "opinion",
    "resena",
    "testimonio",
    "probado",
    "profesional",
    "profesionales",
    "usan",
    "confianza",
    "confian",
    "soporte",
    "certificado",
    "certificada",
    "sello",
    "llega",
    "apoyo",
    "suavidad",
    "amortiguacion",
    "ligereza",
    "cansancio",
    "fatiga",
    "muchas mujeres",
    "muchas personas",
    "piel genuina",
    "vacuno",
    "walking soft",
    "inyeccion directa",
    "capsula de aire",
    "recovery form",
    "hexafoam",
)

MESSAGE_CTA_MARKERS = (
    "escribenos",
    "mandanos",
    "envianos",
    "contactanos",
    "te asesoramos",
    "te orientamos",
    "te ayudamos",
    "solicita informes",
    "preguntanos",
    "pregunta por",
    "manda un whatsapp",
    "mandanos un whatsapp",
    "escribenos por whatsapp",
)


def normalize(text: str) -> str:
    """Minúsculas, sin acentos, sin signos raros, espacios colapsados."""
    if not text:
        return ""
    text = text.replace("×", "x").replace("–", "-").replace("—", "-")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9%+#]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _contains(text: str, term: str) -> bool:
    needle = normalize(term)
    return bool(needle) and needle in normalize(text)


def _field_text(variant: Dict[str, Any]) -> str:
    return " ".join(
        str(variant.get(key, ""))
        for key in ("headline", "primary_text", "description")
    )


def validate_variant(
    variant: Dict[str, Any],
    *,
    allowed_angles: Sequence[str],
    approved_model_codes: Sequence[str],
    forbidden_terms: Iterable[str] = (),
    voice_avoid: Iterable[str] = (),
) -> Dict[str, Any]:
    """Devuelve errores y warnings para una variante."""
    errors: List[str] = []
    warnings: List[str] = []

    required = (
        "id",
        "angle",
        "model_code",
        "headline",
        "primary_text",
        "description",
        "cta",
        "hypothesis",
    )
    for key in required:
        if not str(variant.get(key, "")).strip():
            errors.append(f"Falta el campo obligatorio: {key}")

    headline = str(variant.get("headline", "")).strip()
    primary = str(variant.get("primary_text", "")).strip()
    description = str(variant.get("description", "")).strip()

    if len(headline) > MAX_HEADLINE:
        errors.append(f"Headline tiene {len(headline)} caracteres; máximo {MAX_HEADLINE}")
    if len(primary) > MAX_PRIMARY:
        errors.append(f"Primary text tiene {len(primary)} caracteres; máximo {MAX_PRIMARY}")
    if len(description) > MAX_DESCRIPTION:
        errors.append(
            f"Description tiene {len(description)} caracteres; máximo {MAX_DESCRIPTION}"
        )

    if variant.get("cta") != "SEND_MESSAGE":
        errors.append("El CTA debe ser exactamente SEND_MESSAGE")
    if variant.get("angle") not in allowed_angles:
        errors.append(f"Ángulo no permitido: {variant.get('angle')!r}")
    if variant.get("model_code") not in approved_model_codes:
        errors.append(f"Modelo no aprobado: {variant.get('model_code')!r}")

    blob = _field_text(variant)
    blob_normalized = normalize(blob)
    brand = normalize(str(variant.get("brand", "")))
    if brand == "flexi" and "quirelli" in blob_normalized:
        errors.append("La variante es de Flexi y no puede presentarse como Quirelli")
    if brand == "quirelli" and any(
        name in blob_normalized for name in ("isaura", "jocelyn", "ginny", "lydia")
    ):
        errors.append("La variante es de Quirelli y menciona un modelo Flexi")
    if not any(marker in normalize(primary) for marker in MESSAGE_CTA_MARKERS):
        errors.append(
            "El primary text debe invitar a iniciar la conversación de WhatsApp "
            "(por ejemplo: 'Escríbenos')."
        )
    blocked = list(dict.fromkeys([*forbidden_terms, *voice_avoid, *HARD_BLOCKED]))
    for term in blocked:
        if _contains(blob, term):
            errors.append(f"Término prohibido detectado: {term!r}")

    if "\n" in primary:
        warnings.append("El primary text tiene saltos de línea; Meta puede truncarlo")
    if primary.lower() == headline.lower():
        warnings.append("El primary text repite el headline")
    if description.lower() in primary.lower() and description:
        warnings.append("La descripción está contenida en el primary text")
    if len(re.findall(r"[!¡]", blob)) > 1:
        warnings.append("Más de un signo de exclamación en la pieza")

    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "char_counts": {
            "headline": len(headline),
            "primary_text": len(primary),
            "description": len(description),
        },
    }


def validate_batch(
    variants: Sequence[Dict[str, Any]],
    *,
    allowed_angles: Sequence[str],
    approved_model_codes: Sequence[str],
    forbidden_terms: Iterable[str] = (),
    voice_avoid: Iterable[str] = (),
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Valida todas las variantes y devuelve el resultado por variante."""
    results: List[Dict[str, Any]] = []
    for variant in variants:
        result = validate_variant(
            variant,
            allowed_angles=allowed_angles,
            approved_model_codes=approved_model_codes,
            forbidden_terms=forbidden_terms,
            voice_avoid=voice_avoid,
        )
        result["id"] = variant.get("id")
        results.append(result)
    return all(result["passed"] for result in results), results
