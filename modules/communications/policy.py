"""Política de calidad para respuestas de comunicaciones.

La política es deliberadamente conservadora: cualquier bandera impide que un
borrador generado se trate como publicable. La aprobación humana sigue siendo
un requisito separado.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


DEFAULT_MAX_CHARS = 90

FORMULAIC_OPENERS = (
    "claro",
    "es que",
    "la verdad",
    "bueno",
    "pues",
    "mira",
    "básicamente",
    "basicamente",
)

_OPENER_PATTERN = re.compile(
    r"^(?:" + "|".join(re.escape(item) for item in FORMULAIC_OPENERS) + r")\b",
    re.IGNORECASE,
)

FORBIDDEN_PHRASES = (
    "deberíamos",
    "debería",
    "deberías",
    "deberían",
    "es importante que",
    "es necesario que",
    "hay que",
    "tenemos que",
    "uno debe",
    "se debería",
    "diagnosticar",
    "diagnóstico",
    "diagnostico",
    "consejo",
    "aconsejar",
    "terapia",
    "terapéutico",
    "lección",
    "moraleja",
    "respecto a",
    "en cuanto a",
    "según estudios",
    "según la ciencia",
    "demuestra que",
    "indica que",
)

CORPORATE_PHRASES = (
    "gracias por comentar",
    "gracias por tu comentario",
    "gracias por ser parte",
    "gracias por formar parte",
    "estamos para servirte",
    "para servirte",
    "tu opinión es importante",
    "tu opinion es importante",
    "nos alegra",
    "te invitamos a",
    "síguenos",
    "siguenos",
    "saludos",
    "excelente día",
    "excelente dia",
    "community manager",
)

COMMERCIAL_PHRASES = (
    "precio",
    "cuesta",
    "costo",
    "disponible en",
    "tallas",
    "compra",
    "comprar",
    "descuento",
    "promo",
    "envío",
    "envio",
    "financiamiento",
    "mensaje directo",
    "whatsapp",
)

AI_DISCLAIMER_PHRASES = (
    "como modelo",
    "como ia",
    "inteligencia artificial",
    "no tengo acceso",
    "lo siento",
)

SEXUAL_DOUBLE_SENSE_PHRASES = (
    "palos",
    "regalar palos",
    "dar palos",
    "palos de luz",
    "coger",
    "sexo",
    "sexual",
    "caliente",
    "excitado",
    "excitada",
    "ven aquí",
    "ven aqui",
    "mamacita",
    "mamacito",
    "desnudo",
    "desnuda",
    "🫦",
    "👅",
    "🍆",
    "🍑",
    "💦",
    "🥵",
)

INTIMACY_PHRASES = (
    "mi amor",
    "te amo",
    "me gustas",
    "mi corazón",
    "mi corazon",
    "hackeaste el corazón",
    "hackeaste el corazon",
    "sentimientos por ti",
    "celoso",
    "celosa",
    "enamorado",
    "enamorada",
    "enamorarse",
    "beso",
    "abrazo",
)

BRAND_SLOGAN_PHRASES = (
    "gobierna",
    "empoderada",
    "empoderado",
    "reina",
    "jefa",
    "líder",
    "lider",
    "manifiesta",
    "abundancia",
)



@dataclass(frozen=True)
class QualityDecision:
    """Resultado inspeccionable de la política."""

    ok: bool
    flags: tuple[str, ...]
    reason: str
    characters: int
    max_chars: int

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "flags": list(self.flags),
            "reason": self.reason,
            "characters": self.characters,
            "max_chars": self.max_chars,
        }


def normalize_response(text: object) -> str:
    """Limpia envoltorios frecuentes del modelo sin cambiar el contenido."""
    if text is None:
        return ""
    value = str(text).strip()
    if value.startswith("```") and value.endswith("```"):
        value = value[3:-3].strip()
        if value.lower().startswith("text"):
            value = value[4:].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    if value.casefold() in {"null", "none", "n/a"}:
        return ""
    for prefix in ("respuesta:", "borrador:", "draft:"):
        if value.lower().startswith(prefix):
            value = value[len(prefix) :].strip()
    return value


def _contains_any(lowered: str, phrases: Iterable[str]) -> bool:
    return any(
        re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", lowered)
        for phrase in phrases
    )


def is_low_signal(comment: object) -> bool:
    """Descarta solo contenido vacío, emojis aislados y risas sin contenido."""
    value = str(comment or "").strip()
    if not value:
        return True
    # Keep letters and numbers; punctuation/emoji-only reactions become empty.
    clean = re.sub(r"[^\w\s]", "", value).strip().casefold()
    if not clean:
        return True
    if re.fullmatch(r"(?:ja|je|ji|jo|ha|he|hi|ho|lol|xd|lmao)+", clean):
        return True
    return False


def comment_signal(comment: object, page_name: str = "Universe Sent Me") -> str:
    """Clasifica señales deterministas antes de cualquier agente generativo."""
    value = str(comment or "").strip()
    if is_low_signal(value):
        return "low_signal"
    lowered = value.casefold()
    page = str(page_name or "").strip().casefold()
    # A question mark is conclusive. Without punctuation, require a recognizable
    # interrogative construction; a phrase such as "Que diablos haha" is not
    # enough to classify a comment as a question.
    question_without_punctuation = re.compile(
        r"^(?:qué|que|cómo|como|cuándo|cuando|dónde|donde|por qué|por que|cuál|cual)\s+"
        r"(?:es|son|significa|dice|pasó|paso|hago|puedo|quieres|quiero|opinas|piensas|te parece|se hace|funciona|cuesta)\b",
        re.IGNORECASE,
    )
    if "?" in value or "¿" in value or question_without_punctuation.search(value):
        return "question"
    # Brand references embedded in sexualized/spam content are not clean brand
    # signals. Hold them for human review instead of inflating brand metrics.
    if page and page in lowered:
        sexual_pattern = re.compile(r"(?i)(?<!\w)(?:s[€e]x[¥y]?|sex[¥y]?|ric+a+|ric+o+)(?!\w)")
        if _contains_any(lowered, SEXUAL_DOUBLE_SENSE_PHRASES) or sexual_pattern.search(value):
            return "risky_brand_mention"
        if _contains_any(lowered, ("http", "www", "follow me", "gana dinero", "bitcoin", "cripto")):
            return "risky_brand_mention"
        return "brand_mention"
    if "@" in value:
        return "tagged_mention"
    return ""


def comment_risk_flags(comment: object) -> tuple[str, ...]:
    """Marca comentarios para revisión humana sin respuesta automática."""
    lowered = str(comment or "").casefold()
    flags: list[str] = []
    if _contains_any(lowered, SEXUAL_DOUBLE_SENSE_PHRASES):
        flags.append("sexual_double_sense")
    return tuple(flags)


def check_response(
    text: object,
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    extra_forbidden: Iterable[str] = (),
) -> QualityDecision:
    """Evalúa un texto antes de permitir que se proponga para publicación."""
    value = normalize_response(text)
    flags: list[str] = []
    reasons: list[str] = []
    lowered = value.casefold()

    if not value:
        flags.append("empty")
        reasons.append("La respuesta está vacía.")
    elif len(value) < 3:
        flags.append("too_short")
        reasons.append("La respuesta es demasiado corta.")

    if len(value) > max_chars:
        flags.append("too_long")
        reasons.append(f"Excede {max_chars} caracteres.")
    if "\n" in value or "\r" in value:
        flags.append("multi_line")
        reasons.append("Debe ser una sola línea.")
    if len(value) > 10 and value.isupper():
        flags.append("all_caps")
        reasons.append("No debe estar todo en mayúsculas.")
    if re.search(r"https?://|www\.", lowered):
        flags.append("url")
        reasons.append("No debe incluir enlaces.")
    if "@" in value:
        flags.append("mention")
        reasons.append("No debe mencionar cuentas.")
    if re.search(r"#[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9_]+", value):
        flags.append("hashtag")
        reasons.append("No debe incluir hashtags.")

    if _contains_any(lowered, FORBIDDEN_PHRASES):
        flags.append("forbidden_phrase")
        reasons.append("Incluye una frase prohibida por la guía de voz.")
    if _contains_any(lowered, extra_forbidden):
        flags.append("legacy_forbidden_phrase")
        reasons.append("Incluye una frase prohibida por el responder.")
    if _contains_any(lowered, CORPORATE_PHRASES):
        flags.append("corporate_phrase")
        reasons.append("Suena corporativo o institucional.")
    if _contains_any(lowered, COMMERCIAL_PHRASES):
        flags.append("commercial_claim")
        reasons.append("No puede afirmar precio, stock, disponibilidad o venta.")
    if _contains_any(lowered, AI_DISCLAIMER_PHRASES):
        flags.append("ai_disclaimer")
        reasons.append("No debe sonar como asistente ni justificarse.")
    if _contains_any(lowered, SEXUAL_DOUBLE_SENSE_PHRASES):
        flags.append("sexual_double_sense")
        reasons.append("No debe contener albur ni doble sentido sexual.")
    if _contains_any(lowered, INTIMACY_PHRASES):
        flags.append("intimacy")
        reasons.append("No debe sugerir intimidad o sentimientos reales.")
    if _contains_any(lowered, BRAND_SLOGAN_PHRASES):
        flags.append("brand_slogan")
        reasons.append("No debe sonar a eslogan de empoderamiento o marca.")
    opener_candidate = value.lstrip(" \t\"'«“¡!¿?")
    if _OPENER_PATTERN.match(opener_candidate):
        flags.append("formulaic_opener")
        reasons.append(
            "No debe empezar con muletillas tipo 'Claro', 'Es que' o 'La verdad'."
        )

    unique_flags = tuple(dict.fromkeys(flags))
    return QualityDecision(
        ok=not unique_flags,
        flags=unique_flags,
        reason=" ".join(reasons) if reasons else "Cumple la política de respuesta.",
        characters=len(value),
        max_chars=max_chars,
    )


def passes_quality(text: object, *, max_chars: int = DEFAULT_MAX_CHARS) -> bool:
    """Atajo booleano para callers que solo necesitan el gate."""
    return check_response(text, max_chars=max_chars).ok
