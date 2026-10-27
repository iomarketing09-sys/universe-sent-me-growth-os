"""Copywriter Agent - genera copy por tenant usando su voz y una campaña concreta.

Por defecto trabaja en dry-run: genera y valida, pero no escribe archivos. Con `--write`
guarda la propuesta dentro de la carpeta de la campaña, nunca en otro tenant.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from modules.creative.agents.copywriter_agent.skills.copy_validator import validate_batch
from modules.creative.agents.copywriter_agent.skills.copy_validator import normalize
from modules.creative.agents.copywriter_agent.skills.omni_client import (
    DEFAULT_MODEL,
    FALLBACK_MODELS,
    OmniRouteClient,
    OmniRouteError,
    extract_json,
)
from modules.creative.agents.copywriter_agent.skills.prompt_builder import (
    build_messages,
    build_repair_prompt,
)
from modules.creative.agents.copywriter_agent.skills.voice_loader import load_voice_profile


PREFERRED_MODEL_ORDER = ("142801", "143201", "306703", "143001", "142901")

def _project_root() -> Path:
    """Raíz del repo, sin importar en qué módulo viva este archivo."""
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return Path.cwd()




@dataclass
class CampaignContext:
    tenant_id: str
    campaign_slug: str
    campaign_path: Path
    brief: str
    audience: str
    assets_manifest: str
    config: Dict[str, Any]
    ads_config: Dict[str, Any]
    voice: Dict[str, Any]
    assignments: List[Dict[str, Any]]


FALLBACK_COPY: Dict[str, Dict[str, Dict[str, str]]] = {
    "142801": {
        "beneficio_directo": {
            "headline": "Comodidad para tu día",
            "primary_text": "Conoce ISAURA de Flexi y siente el confort en cada paso. Escríbenos y te asesoramos.",
            "description": "Asesoría en tienda",
        },
        "prueba_social": {
            "headline": "Flexi en Piedras Negras",
            "primary_text": "ISAURA está en Flexi, distribuidor oficial en Piedras Negras. Escríbenos y te orientamos.",
            "description": "Asesoría en tienda",
        },
    },
    "142901": {
        "beneficio_directo": {
            "headline": "Confort para tu rutina",
            "primary_text": "JOCELYN de Flexi te acompaña con confort en tu rutina. Escríbenos y te asesoramos.",
            "description": "Te ayudamos a elegir",
        },
        "prueba_social": {
            "headline": "Flexi, distribuidor oficial",
            "primary_text": "JOCELYN está en Flexi, distribuidor oficial en Piedras Negras. Escríbenos y te orientamos.",
            "description": "Atención en tienda",
        },
    },
    "143001": {
        "beneficio_directo": {
            "headline": "Camina con confort",
            "primary_text": "Conoce GINNY de Flexi y camina con confort todos los días. Escríbenos y te asesoramos.",
            "description": "Asesoría en tienda",
        },
        "prueba_social": {
            "headline": "Flexi, distribuidor oficial",
            "primary_text": "GINNY está en Flexi, distribuidor oficial en Piedras Negras. Escríbenos y te orientamos.",
            "description": "Atención en tienda",
        },
    },
    "143201": {
        "beneficio_directo": {
            "headline": "Comodidad para tu día",
            "primary_text": "Descubre LYDIA de Flexi y siente el confort en cada paso. Escríbenos y te asesoramos.",
            "description": "Asesoría en tienda",
        },
        "prueba_social": {
            "headline": "Flexi en Piedras Negras",
            "primary_text": "LYDIA está en Flexi, distribuidor oficial en Piedras Negras. Escríbenos y te orientamos.",
            "description": "Asesoría en tienda",
        },
    },
    "306703": {
        "beneficio_directo": {
            "headline": "Confort Quirelli para ti",
            "primary_text": "Conoce ARISHA de Quirelli y siente el confort en cada paso. Escríbenos y te asesoramos.",
            "description": "Asesoría en tienda",
        },
        "prueba_social": {
            "headline": "Quirelli, distribuidor oficial",
            "primary_text": "ARISHA está en Quirelli, distribuidor oficial en Piedras Negras. Escríbenos y te orientamos.",
            "description": "Atención en tienda",
        },
    },
}


class CopywriterAgent:
    def __init__(
        self,
        tenant_id: str,
        base_path: Optional[str] = None,
        model: Optional[str] = None,
        offline: bool = False,
    ):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path) if base_path else _project_root()
        self.tenant_path = self.base_path / "tenants" / tenant_id
        self.model = model or DEFAULT_MODEL
        self.offline = offline
        self.client = OmniRouteClient() if not offline else None

    def _load_config(self) -> Dict[str, Any]:
        config_path = self.tenant_path / "config.json"
        if not config_path.is_file():
            raise FileNotFoundError(f"No existe config.json para el tenant: {self.tenant_id}")
        return json.loads(config_path.read_text(encoding="utf-8"))

    def load_context(self, campaign_slug: str, variants: int = 4) -> CampaignContext:
        config = self._load_config()
        campaign_path = self.tenant_path / "ads" / "campanas" / campaign_slug

        brief_path = campaign_path / "01_brief.md"
        audience_path = campaign_path / "02_audiencia.md"
        assets_path = campaign_path / "_assets_manifest.md"

        brief = brief_path.read_text(encoding="utf-8") if brief_path.is_file() else ""
        audience = audience_path.read_text(encoding="utf-8") if audience_path.is_file() else ""
        assets_manifest = assets_path.read_text(encoding="utf-8") if assets_path.is_file() else ""

        ads_config = config.get("ads", {})
        voice = load_voice_profile(self.tenant_path)
        assignments = self._build_assignments(ads_config, variants)

        return CampaignContext(
            tenant_id=self.tenant_id,
            campaign_slug=campaign_slug,
            campaign_path=campaign_path,
            brief=brief,
            audience=audience,
            assets_manifest=assets_manifest,
            config=config,
            ads_config=ads_config,
            voice=voice,
            assignments=assignments,
        )

    def _build_assignments(
        self, ads_config: Dict[str, Any], variants: int
    ) -> List[Dict[str, Any]]:
        approved = ads_config.get("approved_models", [])
        allowed_angles = ads_config.get("allowed_angles", ["beneficio_directo", "prueba_social"])

        ordered = []
        for code in PREFERRED_MODEL_ORDER:
            match = next((m for m in approved if str(m.get("code")) == code), None)
            if match:
                ordered.append(match)

        assignments = []
        for i, model in enumerate(ordered[:variants]):
            angle = allowed_angles[i % len(allowed_angles)]
            assignments.append(
                {
                    "id": f"v{i + 1}",
                    "angle": angle,
                    "model_code": str(model.get("code")),
                    "model_name": model.get("name", ""),
                    "brand": model.get("brand", ""),
                }
            )
        return assignments

    def generate(
        self,
        campaign_slug: str,
        variants: int = 4,
        write: bool = False,
    ) -> Dict[str, Any]:
        context = self.load_context(campaign_slug, variants)

        if self.offline:
            copied = self._fallback_variants(context)
            model_used = "fallback:offline"
            source = "fallback:offline"
            warnings = ["Modo offline: usando copy de respaldo local."]
        else:
            copied, source, model_used = self._generate_with_model(context)
            warnings = []

        variant_validation = self._validate(copied, context)
        passed = all(item["passed"] for item in variant_validation)

        result: Dict[str, Any] = {
            "tenant_id": self.tenant_id,
            "campaign_slug": campaign_slug,
            "generated_at": date.today().isoformat(),
            "voice_profile": str(self.tenant_path / "brand_voice.json"),
            "voice_approved_by": context.voice.get("approved_by", ""),
            "skills": [
                "marketingskills-copywriting",
                "marketingskills-ad-creative",
            ],
            "model_requested": self.model,
            "model_used": model_used,
            "source": source,
            "warnings": warnings,
            "variants": copied,
            "validation": variant_validation,
            "passed": passed,
        }

        if write:
            result["written"] = self.write_proposal(context, result)
        return result

    def _generate_with_model(
        self, context: CampaignContext, warnings: List[str]
    ) -> tuple[List[Dict[str, Any]], str, str]:
        messages = build_messages(
            tenant_id=context.tenant_id,
            campaign_slug=context.campaign_slug,
            voice=context.voice,
            ads_config=context.ads_config,
            brief=context.brief,
            audience=context.audience,
            assets_manifest=context.assets_manifest,
            assignments=context.assignments,
        )
        models = (self.model, *[m for m in FALLBACK_MODELS if m != self.model])

        try:
            response = self.client.chat_with_fallback(
                messages, models=models, max_tokens=2200
            )
            copied = self._coerce_variants(extract_json(response.content), context)
            validation = self._validate(copied, context)

            if not all(item["passed"] for item in validation):
                errors = [
                    f"{item.get('id', '?')}: {error}"
                    for item in validation
                    for error in item.get("errors", [])
                ]
                repair_messages = [
                    *messages,
                    {"role": "assistant", "content": response.content},
                    {"role": "user", "content": build_repair_prompt(errors)},
                ]
                repaired = self.client.chat_with_fallback(
                    repair_messages, models=models, max_tokens=2200
                )
                repaired_variants = self._coerce_variants(
                    extract_json(repaired.content), context
                )
                repaired_validation = self._validate(repaired_variants, context)
                if all(item["passed"] for item in repaired_validation):
                    if repaired.model != self.model:
                        warnings.append(
                            f"El modelo principal no respondió; se usó `{repaired.model}`."
                        )
                    return repaired_variants, f"omniroute:{repaired.model}", repaired.model
                warnings.append(
                    "El modelo no corrigió la validación; se usó copy de respaldo local."
                )
                return self._fallback_variants(context), "fallback:validation", response.model

            if response.model != self.model:
                warnings.append(
                    f"El modelo principal no respondió; se usó `{response.model}`."
                )
            return copied, f"omniroute:{response.model}", response.model
        except (OmniRouteError, ValueError, KeyError) as exc:
            warnings.append(f"Fallo del modelo: {exc}. Se usó copy de respaldo local.")
            return self._fallback_variants(context), "fallback:model_error", "none"

    def _coerce_variants(
        self, data: Dict[str, Any], context: CampaignContext
    ) -> List[Dict[str, Any]]:
        raw_variants = data.get("variants") if isinstance(data, dict) else data
        if not isinstance(raw_variants, list):
            raise ValueError("La salida del modelo no contiene una lista `variants`")

        by_id = {v["id"]: v for v in raw_variants if isinstance(v, dict) and v.get("id")}
        ordered = []
        for assign in context.assignments:
            variant = by_id.get(assign["id"])
            if not variant:
                raise ValueError(f"Falta variante {assign['id']} en la respuesta del modelo")

            full = {
                "id": assign["id"],
                "angle": assign["angle"],
                "model_code": assign["model_code"],
                "model_name": assign["model_name"],
                "brand": assign.get("brand", ""),
                "headline": str(variant.get("headline", "")).strip(),
                "primary_text": str(variant.get("primary_text", "")).strip(),
                "description": str(variant.get("description", "")).strip(),
                "cta": str(variant.get("cta", "SEND_MESSAGE")).strip(),
                "hypothesis": str(variant.get("hypothesis", "")).strip(),
            }
            ordered.append(full)
        return ordered

    def _fallback_variants(self, context: CampaignContext) -> List[Dict[str, Any]]:
        out = []
        for assign in context.assignments:
            code = assign["model_code"]
            angle = assign["angle"]
            fallback = FALLBACK_COPY.get(code, {}).get(angle, {})
            out.append(
                {
                    "id": assign["id"],
                    "angle": angle,
                    "model_code": code,
                    "model_name": assign["model_name"],
                    "brand": assign.get("brand", ""),
                    "headline": fallback.get("headline", "Confort para tu día"),
                    "primary_text": fallback.get("primary_text", "Escríbenos y te asesoramos."),
                    "description": fallback.get("description", "Asesoría en tienda"),
                    "cta": "SEND_MESSAGE",
                    "hypothesis": f"Control para {code} {angle}.",
                }
            )
        return out

    def _polish_variants(self, variants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for v in variants:
            if "headline" in v:
                v["headline"] = v["headline"][:40]
            if "primary_text" in v:
                v["primary_text"] = v["primary_text"][:125]
            if "description" in v:
                v["description"] = v["description"][:30]
        return variants

    def _hypothesis(self, assignment: Dict[str, Any]) -> str:
        angle = assignment["angle"]
        code = assignment["model_code"]
        if angle == "beneficio_directo":
            return f"El ángulo de comodidad en {code} superará en CTR al ángulo de confianza local en mujeres de 28 a 55 años de Piedras Negras."
        return f"La mención de distribuidor oficial en {code} superará en tasa de conversación a una variante con CTA genérico en la misma audiencia."

    def _validate(
        self, variants: List[Dict[str, Any]], context: CampaignContext
    ) -> List[Dict[str, Any]]:
        allowed = context.ads_config.get("allowed_angles", ["beneficio_directo", "prueba_social"])
        approved_codes = [
            str(m.get("code")) for m in context.ads_config.get("approved_models", [])
        ]
        forbidden = context.ads_config.get("forbidden_terms", [])
        voice_avoid = (context.voice.get("vocabulary", {}) or {}).get("avoid", [])

        _, results = validate_batch(
            variants,
            allowed_angles=allowed,
            approved_model_codes=approved_codes,
            forbidden_terms=forbidden,
            voice_avoid=voice_avoid,
        )

        for i, v in enumerate(variants):
            own_code = str(v.get("model_code", ""))
            own_name = str(v.get("model_name", "")).lower()
            blob = normalize(
                " ".join(str(v.get(key, "")) for key in ("headline", "primary_text", "description"))
            )
            for model in context.ads_config.get("approved_models", []):
                name = normalize(str(model.get("name", "")))
                code = str(model.get("code", ""))
                if code == own_code or not name:
                    continue
                if name in blob and name != own_name:
                    results[i]["errors"].append(
                        f"La variante {v.get('id')} menciona el modelo {model.get('name')} "
                        f"pero está asignada a {v.get('model_name')}"
                    )
                    results[i]["passed"] = False
        return results

    def _next_version(self, campaign_path: Path) -> int:
        copy_dir = campaign_path / "piezas" / "copy"
        if not copy_dir.is_dir():
            return 1
        versions = []
        for path in copy_dir.glob("propuesta_v*.md"):
            match = re.search(r"propuesta_v(\d+)\.md$", path.name)
            if match:
                versions.append(int(match.group(1)))
        return max(versions, default=0) + 1

    def write_proposal(
        self, context: CampaignContext, result: Dict[str, Any]
    ) -> Dict[str, str]:
        version = self._next_version(context.campaign_path)
        copy_dir = context.campaign_path / "piezas" / "copy"
        copy_dir.mkdir(parents=True, exist_ok=True)

        markdown_path = copy_dir / f"propuesta_v{version}.md"
        json_path = copy_dir / f"variantes_v{version}.json"
        markdown_path.write_text(self._render_markdown(context, result, version), encoding="utf-8")
        json_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        self._update_state(context, version)
        return {"markdown": str(markdown_path), "json": str(json_path)}

    def _render_markdown(
        self, context: CampaignContext, result: Dict[str, Any], version: int
    ) -> str:
        compliance_state = "OK" if result["passed"] else "CON ERRORES — NO APROBAR"
        rows = []
        for variant in result["variants"]:
            rows.append(
                "| {id} | {angle} | {code} {name} | {headline} | {primary} | {description} |".format(
                    id=variant["id"],
                    angle=variant["angle"],
                    code=variant["model_code"],
                    name=variant["model_name"],
                    headline=variant["headline"].replace("|", "\\|"),
                    primary=variant["primary_text"].replace("|", "\\|"),
                    description=variant["description"].replace("|", "\\|"),
                )
            )

        details = []
        for variant, validation in zip(result["variants"], result["validation"]):
            details.append(
                f"""### {variant['id']} — {variant['angle']} — {variant['model_code']} {variant['model_name']}

- **Headline ({len(variant['headline'])}/40):** {variant['headline']}
- **Primary text ({len(variant['primary_text'])}/125):** {variant['primary_text']}
- **Description ({len(variant['description'])}/30):** {variant['description']}
- **CTA:** `{variant['cta']}`
- **Hipótesis:** {variant['hypothesis']}
- **Compliance:** {'OK' if validation['passed'] else 'ERROR'}
"""
            )

        warnings = "\n".join(f"- {warning}" for warning in result["warnings"]) or "- Ninguno."
        return f"""# Propuesta creativa G2 — {context.campaign_slug}

**Estado:** pendiente de aprobación de Fernando (G2)
**Generado:** {result['generated_at']}
**Tenant:** `{context.tenant_id}`
**Voz de marca:** `{result['voice_profile']}`
**Skills:** {', '.join(f'`{skill}`' for skill in result['skills'])}
**Modelo:** `{result['model_used']}` (`{result['model_requested']}` solicitado)
**Fuente del copy:** `{result['source']}`
**Compliance local:** **{compliance_state}**

> Esta propuesta no se publicó en Meta. No se subieron imágenes ni se creó ningún anuncio.
> `03_creativos.md` se llena solo después de que apruebes esta versión.

## Tabla de variantes

| # | Ángulo | Modelo | Headline | Primary text | Description |
|---|---|---|---|---|---|
{chr(10).join(rows)}

## Copy completo

{chr(10).join(details)}

## Warnings

{warnings}

## Checklist para aprobar G2

- [ ] Apruebo los 4 copies y sus ángulos.
- [ ] Apruebo los modelos asignados a cada variante.
- [ ] Confirmo que no hay claims rechazados ni promesas de stock, talla, precio o promo.
- [ ] Confirmo que se usarán solo imágenes de los 5 modelos aprobados + material de marca.
- [ ] Autorizo pasar a selección de 6–8 imágenes y armar las piezas.

## Después de la aprobación

1. Copiar la tabla aprobada a `03_creativos.md`.
2. Seleccionar 6–8 imágenes de `_assets_manifest.md`.
3. Generar las piezas y validar compliance visual.
4. Pedir G3 (autorización de gasto) antes de tocar Meta.
"""

    def _update_state(self, context: CampaignContext, version: int) -> None:
        state_path = context.campaign_path / "00_estado.md"
        if not state_path.is_file():
            return
        text = state_path.read_text(encoding="utf-8")
        text = re.sub(
            r"^\| Estado \|.*\|$",
            "| Estado | **G1 APROBADO — G2 pendiente de aprobación "
            f"(propuesta v{version} generada)** |",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        log_line = (
            f"| {date.today().isoformat()} | Copywriter Agent genera propuesta v{version} "
            "(4 variantes); G2 pendiente | CGO |"
        )
        if log_line not in text:
            text = text.rstrip() + "\n" + log_line + "\n"
        state_path.write_text(text, encoding="utf-8")


def create_copywriter_agent(tenant_id: str, base_path: Optional[str] = None, **kwargs: Any) -> CopywriterAgent:
    return CopywriterAgent(tenant_id, base_path=base_path, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Copywriter Agent de Growth OS")
    parser.add_argument("tenant", help="ID del tenant, por ejemplo flexi")
    parser.add_argument("--campaign", required=True, help="Slug de la campaña")
    parser.add_argument("--variants", type=int, default=4, help="Número de variantes (default 4)")
    parser.add_argument("--write", action="store_true", help="Guarda la propuesta en la campaña")
    parser.add_argument("--offline", action="store_true", help="No llama a OmniRoute; usa respaldo local")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Modelo OmniRoute")
    parser.add_argument("--base-path", default=None, help="Raíz de Growth OS")
    args = parser.parse_args()

    agent = CopywriterAgent(
        args.tenant,
        base_path=args.base_path,
        model=args.model,
        offline=args.offline,
    )
    try:
        result = agent.generate(
            args.campaign,
            variants=args.variants,
            write=args.write,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.write:
        print("\nDRY RUN: no se escribió ningún archivo. Usa --write para guardar la propuesta.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
