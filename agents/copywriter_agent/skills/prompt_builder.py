"""Construye los prompts del Copywriter Agent a partir de la voz y la campaña."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Sequence

from .copy_validator import HARD_BLOCKED
from .voice_loader import compact_evidence, voice_summary


BASE_DIR = Path(__file__).resolve().parent
VENDOR_DIR = BASE_DIR / "vendor"
PROMPTS_DIR = BASE_DIR.parent / "prompts"

GENERAL_SKILL = VENDOR_DIR / "marketingskills-copywriting" / "SKILL.md"
AD_SKILL = VENDOR_DIR / "marketingskills-ad-creative" / "SKILL.md"
ROLE_PROMPT = PROMPTS_DIR / "system.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_system_prompt() -> str:
    return "\n\n".join(
        [
            _read(ROLE_PROMPT).strip(),
            "## Skill 1: copywriting base\n\n" + _read(GENERAL_SKILL).strip(),
            "## Skill 2: copy para anuncios Meta\n\n" + _read(AD_SKILL).strip(),
        ]
    )


def build_messages(
    *,
    tenant_id: str,
    campaign_slug: str,
    voice: Dict[str, Any],
    ads_config: Dict[str, Any],
    brief: str,
    audience: str,
    assets_manifest: str,
    assignments: Sequence[Dict[str, Any]],
) -> List[Dict[str, str]]:
    approved_models = [
        {
            "code": str(model.get("code")),
            "name": model.get("name", ""),
            "brand": model.get("brand", ""),
        }
        for model in ads_config.get("approved_models", [])
    ]
    targeting = ads_config.get("targeting", {}) or {}
    voice_avoid = (voice.get("vocabulary", {}) or {}).get("avoid", [])
    blocked_terms = sorted(
        {
            *HARD_BLOCKED,
            *(ads_config.get("forbidden_terms", []) or []),
            *(voice_avoid or []),
        }
    )
    context = {
        "tenant_id": tenant_id,
        "campaign_slug": campaign_slug,
        "voice_summary": voice_summary(voice),
        "published_copy_evidence": compact_evidence(voice),
        "voice_approved": bool(voice.get("approved_by")),
        "objective": "Iniciar conversaciones de WhatsApp con intención real (click-to-WhatsApp)",
        "market": {
            "city": targeting.get("city"),
            "region": targeting.get("region"),
            "country": targeting.get("country"),
            "radius_km": targeting.get("radius_km"),
            "age_min": targeting.get("age_min"),
            "age_max": targeting.get("age_max"),
            "genders": targeting.get("genders"),
        },
        "allowed_angles": ads_config.get("allowed_angles", []),
        "forbidden_terms": ads_config.get("forbidden_terms", []),
        "hard_blocked_terms": blocked_terms,
        "claims_status": ads_config.get("claims_status", ""),
        "claims_rejected": ads_config.get("claims_rejected", []),
        "approved_models": approved_models,
        "assignments": assignments,
        "brief_excerpt": brief[:1400],
        "audience_excerpt": audience[:1000],
        "assets_excerpt": assets_manifest[:900],
    }

    output_contract = {
        "variants": [
            {
                "id": "v1",
                "angle": "beneficio_directo",
                "model_code": "142801",
                "headline": "Máximo 40 caracteres",
                "primary_text": "Máximo 125 caracteres",
                "description": "Máximo 30 caracteres",
                "cta": "SEND_MESSAGE",
                "hypothesis": "Hipótesis falsable con métrica, comparación y dirección",
            }
        ]
    }

    user_prompt = f"""
Escribe el copy de 4 variantes para la campaña `{campaign_slug}` del tenant `{tenant_id}`.

Contexto verificado:
{json.dumps(context, ensure_ascii=False, indent=2)}

Asignación fija (no la cambies):
{json.dumps(assignments, ensure_ascii=False, indent=2)}

Reglas duras:
1. Español de México, tono tú cercano, sin sonar acartonado.
2. Solo los ángulos y modelos asignados. No inventes modelos, precios, stock, tallas, colores ni promociones.
3. No menciones envío, meses sin intereses, 2x1, descuentos, ofertas ni cumpleaños.
4. No prometas respuesta inmediata ni disponibilidad.
5. El CTA siempre es `SEND_MESSAGE` y el texto principal debe invitar a escribir por WhatsApp
   (por ejemplo: "Escríbenos y te asesoramos").
6. Prohibido decir "compra", "comprar", "online", "tienda física", "calidad asegurada" o
   cualquier promesa de resultado.
7. Flexi es el distribuidor oficial, no el modelo. No escribas "ARISHA es distribuidor".
8. Prohibida la prueba social fabricada: no uses "clientes", "clientas", "recomiendan",
   "testimonios", "elección", "favorito", "muchas mujeres" ni "probado". La única prueba
   permitida es "distribuidor oficial".
9. No uses "certificado", "certificada", "sello" ni "soporte"; no están respaldados.
10. No uses "llega", "apoyo", "suavidad", "amortiguación", "ligereza", "cansancio" ni
    "fatiga": son claims de producto o disponibilidad no verificados.
11. No atribuyas tecnologías específicas a un modelo (Walking Soft, Hexafoam, Cápsula de Aire,
    Recovery Form, Inyección Directa) ni materiales (piel genuina, vacuno); no están verificados
    por modelo en el manifiesto de esta campaña. Habla de confort en general.
12. Titular <= 40 caracteres; texto principal <= 125; descripción <= 30.
13. La descripción complementa el texto principal; no lo repite.
14. Cero emojis o máximo uno por variante. Mejor cero.
15. Cada hipótesis debe poder perder: métrica, comparación y dirección esperada.
16. No repitas la misma estructura en las 4 variantes.
17. Devuelve SOLO JSON válido, sin Markdown, sin explicación.
18. El campo `published_copy_evidence` contiene copys reales del tenant. Úsalo como
    ancla de ritmo y vocabulario: hooks sensoriales en segunda persona, frases cortas
    y cercanía. No copies frases literales, hashtags, emojis ni direcciones; el
    anuncio debe sentirse de la misma marca sin romper las reglas 1-17.
19. Si el copy real y las reglas de la campaña chocan, mandan las reglas de la campaña.
20. Prohibidas las aperturas genéricas tipo "Descubre el confort de...", "Confort para tu
    día" o "Camina con confort". Cada hook debe partir de una escena o sensación cotidiana
    concreta (pies, paso, rutina, domingo, trabajo, ocasión especial) sin inventar hechos.
21. Varía la estructura entre variantes: una puede abrir con escena, otra con beneficio,
    otra con pregunta y otra con invitación. No repitas la fórmula "Modelo + beneficio".
22. El validador bloquea literalmente estos términos. No uses ninguno, ni en singular ni
    en plural, ni como sinónimo directo:
    {json.dumps(blocked_terms, ensure_ascii=False)}

Contrato de salida:
{json.dumps(output_contract, ensure_ascii=False, indent=2)}
""".strip()

    return [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_prompt},
    ]


def build_repair_prompt(errors: Sequence[str]) -> str:
    error_text = "\n".join(f"- {error}" for error in errors)
    return (
        "Tu respuesta anterior no pasó la validación local. Corrige exactamente estos puntos. "
        "Conserva las variantes que ya cumplen y reescribe las que fallan. Devuelve de nuevo "
        "SOLO el JSON completo con las 4 variantes, sin explicación:\n"
        f"{error_text}"
    )
