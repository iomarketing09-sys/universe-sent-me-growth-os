"""Agente de Comunicaciones en modo sugerencia y análisis sombra.

El agente propone respuestas y evalúa decisiones, pero nunca publica ni cambia
aprobaciones. Toda salida requiere revisión y autorización humana.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from modules.communications.comments.paths import CommentPaths, repository_root
from modules.communications.comments.review import load_approvals
from modules.communications.llm import DEFAULT_MODEL, OmniRouteClient
from modules.communications.policy import (
    DEFAULT_MAX_CHARS,
    check_response,
    comment_risk_flags,
    is_low_signal,
    normalize_response,
)


VALID_RISKS = {"low", "medium", "high"}


def _text(value: Any) -> str:
    return str(value or "").strip()


def _boolean(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return _text(value).casefold() in {"true", "1", "yes", "si", "sí"}


def _confidence(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _string_list(value: Any) -> List[str]:
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list):
        values = value
    else:
        values = []
    return list(dict.fromkeys(item for item in (_text(value) for value in values) if item))


def _merge_usage(*usages: Dict[str, Any]) -> Dict[str, Any]:
    """Suma uso de tokens cuando el agente necesita una segunda pasada."""
    merged: Dict[str, Any] = {}
    for usage in usages:
        for key, value in (usage or {}).items():
            if isinstance(value, (int, float)):
                merged[key] = merged.get(key, 0) + value
            elif key not in merged:
                merged[key] = value
    return merged


def _safe_context(context: Dict[str, Any], fallback_character: str = "Universe") -> Dict[str, str]:
    """Solo envía contenido público y contexto creativo al modelo."""
    return {
        "character": _text(context.get("character")) or fallback_character,
        "asset_ref": _text(context.get("asset_ref")),
        "meme_text": _text(context.get("meme_text")),
        "visual_context": _text(context.get("visual_context")),
        "caption": _text(context.get("caption")),
    }


def _context_policy_flags(
    comment: str,
    context: Dict[str, str],
    draft: str,
) -> tuple[List[str], List[str]]:
    """Bloquea borradores que ignoran o contradicen el chiste del asset."""
    flags: List[str] = []
    reasons: List[str] = []
    comment_lower = comment.casefold()
    asset = context.get("asset_ref", "").casefold()
    meme = context.get("meme_text", "").casefold()
    caption = context.get("caption", "").casefold()
    creative = " ".join((asset, meme, caption))
    draft_lower = draft.casefold()

    if "te voy a comer" in asset and "te voy a comer" not in meme:
        if any(
            phrase in draft_lower
            for phrase in ("hambre", "comer", "comida", "caníbal", "canibal", "morder")
        ):
            flags.append("literal_asset_joke")
            reasons.append("Interpreta literalmente el nombre del archivo en vez del meme.")

    if "plática normal" in creative or "platica normal" in creative:
        if "platica" in comment_lower or "plática" in comment_lower:
            if not any(
                cue in draft_lower
                for cue in (
                    "plática",
                    "platica",
                    "normal",
                    "conversación",
                    "conversacion",
                    "hablar",
                    "mito",
                    "unicornio",
                    "misterio",
                    "raro",
                    "última vez",
                    "ultima vez",
                    "inexistente",
                )
            ):
                flags.append("context_mismatch")
                reasons.append("No conecta con la broma de que no existe una plática normal.")

    if "cuanto gasto" in creative or "#gastos" in creative:
        if not any(
            cue in draft_lower
            for cue in (
                "gast",
                "compr",
                "presupuesto",
                "carrito",
                "páginas",
                "paginas",
                "cartera",
                "barat",
            )
        ):
            flags.append("context_mismatch")
            reasons.append("No conecta con la broma de cuánto gasta Maeve.")

    if "no te mueres" in asset and ("coopera" in comment_lower or "crush" in comment_lower):
        if not any(
            cue in draft_lower
            for cue in ("muere", "muert", "morir", "vive", "vivo", "viva", "sobreviv", "sigue")
        ):
            flags.append("context_mismatch")
            reasons.append("No recupera el remate del asset: la persona no coopera, pero sigue viva.")

    if "cuñado" in comment_lower and "marido" in comment_lower:
        invented_scene = any(
            cue in draft_lower
            for cue in ("reunión familiar", "reunion familiar", "palomitas", "quién lleva", "quien lleva")
        )
        follows_joke = any(
            cue in draft_lower for cue in ("cuñado", "marido", "ellos", "casa", "así", "asi")
        )
        if invented_scene and not follows_joke:
            flags.append("invented_scene")
            reasons.append("Inventa una escena en vez de seguir la complicidad familiar.")

    if ("primer síntoma" in meme or "primer sintoma" in meme) and "ching" in meme:
        if not any(
            cue in draft_lower
            for cue in (
                "síntoma",
                "sintoma",
                "ching",
                "creer",
                "p3ndj",
                "pendej",
                "tont",
            )
        ):
            flags.append("context_mismatch")
            reasons.append("No aterriza en el remate del meme sobre sentirse muy chingón.")

    return list(dict.fromkeys(flags)), reasons


def _context_hints(comment: str, context: Dict[str, str]) -> str:
    """Señales específicas del contexto que ayudan al modelo a no generalizar."""
    comment_lower = comment.casefold()
    asset = context.get("asset_ref", "").casefold()
    meme = context.get("meme_text", "").casefold()
    caption = context.get("caption", "").casefold()
    creative = " ".join((asset, meme, caption))
    hints: List[str] = []

    if "🙃" in comment and "👏" in comment:
        hints.append("El aplauso es sarcástico: sí requiere un remate seco, no es baja señal.")
    if "te voy a comer" in asset and "te voy a cuidar" in meme:
        hints.append("El meme canónico dice 'Te voy a cuidar'; no hables de comer, hambre ni comida.")
    if "plática normal" in creative or "platica normal" in creative:
        if "platica" in comment_lower or "plática" in comment_lower:
            hints.append("Aterriza en la broma de que las pláticas normales no existen.")
    if "cuanto gasto" in creative or "#gastos" in creative:
        hints.append(
            "La broma es el gasto de Maeve. Conecta con gastar desde una lógica espiritual o "
            "cósmica de alguien que se justifica con el universo; no conviertas la respuesta en "
            "un ataque a la cartera ni al bolsillo del comentarista."
        )
    if "reacciona mi cuerpo" in creative and "prueba" in comment_lower:
        hints.append(
            "La broma es la invitación pícara de Kael a ver cómo reacciona su cuerpo. Mantén "
            "el coqueteo con suspenso y seguridad; no hables de cansancio, rechazo ni de dejar "
            "la prueba a medias."
        )
    if ("barájale" in creative or "barajeale" in creative) and "evan" in creative:
        hints.append(
            "El meme es Evan insistiendo en que la bruja le baraje las cartas. Sigue el juego "
            "de la terquedad y la insistencia, sin burlarte del comentarista."
        )
    if "no te mueres" in asset and ("coopera" in comment_lower or "crush" in comment_lower):
        hints.append("El remate del asset es que la persona no coopera, pero tampoco se muere.")
    if "cuñado" in comment_lower and "marido" in comment_lower:
        hints.append(
            "La broma es que ellos son así: el remate debe señalar que el meme ya los "
            "describió, con filo y complicidad. No inventes reuniones, palomitas ni escenas, "
            "evita cerrar con una frase tibia y no uses listas de síntomas, clínica, "
            "diagnóstico ni paciente."
        )
    if ("primer síntoma" in meme or "primer sintoma" in meme) and "ching" in meme:
        hints.append(
            "El remate del meme es que sentirse muy chingón es el primer síntoma de estar "
            "p3ndjo; aterriza ahí con sarcasmo, sin insultar directamente al comentarista. "
            "No lo conviertas en diagnóstico, clínica, consulta ni paciente."
        )
    if "sentido algo por mi" in comment_lower or "sientes algo" in comment_lower:
        hints.append(
            "El comentario es personal: no confirmes sentimientos, no coquetees y no uses el "
            "remate de 'no te mueres'; responde con una evasiva seca en personaje."
        )
    if "poético" in comment_lower or "poetico" in comment_lower:
        hints.append("Comenta el tono sin volver literal el nombre del archivo.")
    return "\n".join(f"- {hint}" for hint in hints) or "- (sin señales adicionales)"


def _find_context(
    contexts: Dict[str, Any],
    comment_id: str,
    fallback_character: str = "Universe",
) -> tuple[Dict[str, str], bool]:
    post_id = _text(comment_id).split("_", 1)[0]
    candidates: List[Dict[str, Any]] = []
    if post_id:
        for key, value in contexts.items():
            if not isinstance(value, dict):
                continue
            publication_id = _text(value.get("publication_id")) or _text(key)
            if publication_id == post_id or publication_id.endswith(f"_{post_id}"):
                candidates.append(value)
        if not candidates and isinstance(contexts.get(post_id), dict):
            candidates.append(contexts[post_id])
    if candidates:
        return _safe_context(candidates[0], fallback_character), True
    return _safe_context({}, fallback_character), False


class CommunicationsAgent:
    """Orquesta clasificación, borrador y política sin publicar nada."""

    name = "communications_agent"
    mode = "suggest"

    def __init__(
        self,
        tenant_id: str = "universe",
        *,
        base_path: Optional[Path] = None,
        storage_dir: Optional[Path] = None,
        client: Optional[OmniRouteClient] = None,
        model: Optional[str] = None,
        max_chars: int = DEFAULT_MAX_CHARS,
    ):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path).resolve() if base_path else repository_root()
        self.paths = CommentPaths.for_tenant(tenant_id, self.base_path, storage_dir)
        self.client = client or OmniRouteClient(tenant_id=tenant_id, base_path=self.base_path)
        self.model = model or os.getenv("OMNIROUTE_MODEL") or DEFAULT_MODEL
        self.max_chars = max_chars

    def _messages(self, comment: str, context: Dict[str, str]) -> List[Dict[str, str]]:
        system = (
            "Eres el Agente de Comunicaciones de Universe Sent Me. "
            "Trabajas en modo sugerencia: propones, nunca publicas ni apruebas.\n"
            "Responde únicamente con un objeto JSON válido, sin Markdown ni texto extra.\n"
            "Esquema exacto:\n"
            '{"intent":"question|humor|identification|opinion|disagreement|affection|sexual|'
            'spam|troll|commercial|mention|low_signal|other",'
            '"risk":"low|medium|high","needs_response":true,"character":"Universe",'
            '"draft":"Respuesta propuesta o null","confidence":0.0,'
            '"policy_flags":[],"reason":"Explicación breve"}\n'
            "Reglas:\n"
            "- La voz es seca, irónica, ácida, cotidiana y en personaje; un solo remate breve.\n"
            "- El humor ácido se dirige a la situación, a la pose o a la ridiculez del meme; "
            "nunca a la dignidad de una persona. No insultes ni humilles al comentarista. "
            "Síguele el juego con sarcasmo y complicidad.\n"
            "- Primero identifica el remate del MEME y después responde al comentario usándolo. "
            "No contestes solo el texto del comentario como si el arte no existiera.\n"
            f"- El draft debe tener máximo {self.max_chars} caracteres, una línea y no explicar el chiste.\n"
            "- No inventes precios, stock, tallas, envíos, descuentos ni disponibilidad.\n"
            "- No des consejo médico, legal, financiero ni terapéutico.\n"
            "- No uses 'diagnóstico', 'diagnosticar' ni lenguaje clínico, ni siquiera como "
            "metáfora; el meme puede decir 'síntoma' sin convertirlo en consulta médica.\n"
            "- Si el comentario es spam, troll, mención o insulto, usa needs_response=false y draft=null.\n"
            "- Si el comentario contiene albur, doble sentido sexual o sexualiza a un personaje, "
            "usa intent=sexual, risk=high, needs_response=false y draft=null. Queda para revisión humana.\n"
            "- Si es solo un eco o reacción mínima sin un giro propio, usa needs_response=false y draft=null. "
            "Ejemplos claros: 'Nooooo 😂😂😂😂', 'Uff 🔥', 'Caracter ☠️🔥'.\n"
            "- No confundas una reacción con un giro: si el comentario añade burla, duda o sarcasmo claro, "
            "puede responderse de forma seca. Un aplauso sarcástico como 🙃👏 puede ser un giro válido; "
            "un emoji de fuego o calavera por sí solo no lo es.\n"
            "- No expreses romance, celos, posesión, intimidad ni sentimientos reales hacia el comentarista. "
            "Si el comentario es personal, esquiva el tema y vuelve al chiste.\n"
            "- No uses eslóganes de empoderamiento, liderazgo, autoayuda ni frases de 'mujer empoderada'. "
            "Nada de 'gobierna', 'reina', 'jefa' o 'empoderada'.\n"
            "- Evita frases genéricas de revista o motivación. La respuesta debe aterrizar en el meme, "
            "el nombre del asset o el remate visual.\n"
            "- Prohibido abrir con 'Claro', 'Claro, porque', 'Es que', 'La verdad', 'Bueno', "
            "'Pues', 'Mira' o 'Básicamente'. Empieza directo en la imagen, el remate o el personaje.\n"
            "- El MEME y el COPY mandan sobre el nombre del archivo. Si el asset y el meme difieren, "
            "responde al chiste visible, nunca al nombre técnico.\n"
            "- Interpreta el asset y el comentario juntos, no por palabras aisladas. Si el asset dice "
            "'Te voy a comer', no hables de hambre, comida ni canibalismo literal. Si el asset dice 'no te mueres' y el comentario "
            "habla de un crush que no coopera, el chiste es que esa persona sigue viva.\n"
            "- Si el comentario bromea con familia o pareja, sigue la complicidad sin excluir a nadie. "
            "No conviertas una broma compartida en una frase genérica de superioridad.\n"
            "- No uses 'enamorado', 'corazón', 'amor' ni promesas de afecto. Si el comentario pregunta por "
            "sentimientos, desvía hacia la ficción o el meme sin coquetear.\n"
            "- Ejemplos de criterio: 'Caracter ☠️🔥' es baja señal; 'Caracter 🙃👏' puede recibir un remate seco. "
            "'Me urge una plática de esas' debe conectar con la broma de que no existen las pláticas normales. "
            "Una broma sobre familia o pareja se sigue con complicidad, no con una escena inventada.\n"
            "- Si falta contexto o hay duda, usa needs_response=false y risk=medium.\n"
            "- No incluyas enlaces, menciones, hashtags ni frases corporativas.\n"
            "- La aprobación y publicación siempre las decide una persona."
        )
        user = (
            f"PERSONAJE: {context.get('character') or 'Universe'}\n"
            f"ASSET CREATIVO: {context.get('asset_ref') or '(sin referencia)'}\n"
            f"MEME: {context.get('meme_text') or '(sin texto)'}\n"
            f"CONTEXTO VISUAL: {context.get('visual_context') or '(sin descripción)'}\n"
            f"COPY: {context.get('caption') or '(sin copy)'}\n"
            f"ARRANQUES YA USADOS (no los repitas): {self._recent_openers() or '(ninguno)'}\n"
            "SEÑALES DE CONTEXTO:\n"
            f"{_context_hints(comment, context)}\n"
            f"COMENTARIO PÚBLICO: {_text(comment)}"
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    def _recent_openers(self, limit: int = 8) -> str:
        """Devuelve los arranques ya usados para que el modelo no los repita."""
        try:
            payload = json.loads(self.paths.approvals_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return ""
        items = [
            item
            for item in (payload.get("approvals") or [])
            if isinstance(item, dict) and str(item.get("approved_response") or "").strip()
        ]
        openers: List[str] = []
        for item in items[-limit:]:
            first = str(item["approved_response"]).strip().split()[0].strip(",.¡!¿?\"'«»“”")
            if first and first not in openers:
                openers.append(first)
        return ", ".join(openers)

    def _repair_messages(
        self,
        comment: str,
        context: Dict[str, str],
        rejected: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Pide una reescritura cuando el primer borrador incumple la política."""
        messages = self._messages(comment, context)
        flags = ", ".join(rejected.get("policy_flags") or []) or "incumplimiento de política"
        reason = _text(rejected.get("reason")) or "La propuesta fue rechazada."
        if "formulaic_opener" in (rejected.get("policy_flags") or []):
            reason += " Empieza con otra palabra: no uses 'Claro', 'Es que' ni 'La verdad'."
        messages.append(
            {
                "role": "assistant",
                "content": json.dumps(
                    {"needs_response": True, "draft": rejected.get("draft")},
                    ensure_ascii=False,
                ),
            }
        )
        messages.append(
            {
                "role": "user",
                "content": (
                    "La propuesta anterior fue rechazada por: "
                    f"{flags}. {reason}\n"
                    "Reescribe desde cero. Conserva el humor ácido, el remate del meme y la "
                    "complicidad con el comentario, pero corrige exactamente ese problema. "
                    "No repitas las palabras o frases señaladas."
                ),
            }
        )
        return messages

    def _normalize(
        self,
        payload: Dict[str, Any],
        context: Dict[str, str],
        comment: str,
        *,
        model: str,
        usage: Dict[str, Any],
        latency_ms: int,
    ) -> Dict[str, Any]:
        needs_response = _boolean(payload.get("needs_response"))
        risk = _text(payload.get("risk")).casefold()
        if risk not in VALID_RISKS:
            risk = "medium"
        intent = _text(payload.get("intent")).casefold() or "other"
        character = context.get("character") or _text(payload.get("character")) or "Universe"
        draft = normalize_response(payload.get("draft"))
        model_flags = _string_list(payload.get("policy_flags"))
        human_review = intent == "sexual" or "sexual_double_sense" in model_flags

        quality = check_response(draft, max_chars=self.max_chars)
        context_flags: List[str] = []
        context_reasons: List[str] = []
        if needs_response and draft:
            context_flags, context_reasons = _context_policy_flags(comment, context, draft)
        policy_flags = list(model_flags) + context_flags
        if needs_response:
            policy_flags.extend(quality.flags)
        if risk == "high":
            policy_flags.append("high_risk")
        if model_flags:
            policy_flags.append("model_policy_flag")
        policy_flags = list(dict.fromkeys(policy_flags))

        if human_review:
            decision = "review"
            public_draft = None
        elif not needs_response:
            decision = "no_response"
            public_draft = None
        elif quality.ok and not policy_flags and risk != "high":
            decision = "suggest"
            public_draft = draft
        else:
            decision = "review"
            public_draft = None

        reason = _text(payload.get("reason"))
        if decision == "review":
            reason = " ".join(
                part
                for part in (reason, None if human_review else quality.reason, *context_reasons)
                if part
            ).strip()

        return {
            "intent": intent,
            "risk": risk,
            "needs_response": needs_response,
            "character": character,
            "draft": draft or None,
            "confidence": _confidence(payload.get("confidence")),
            "policy_flags": policy_flags,
            "context_flags": context_flags,
            "reason": reason,
            "quality_ok": quality.ok if needs_response else True,
            "quality": quality.to_dict() if needs_response else None,
            "decision": decision,
            "response": public_draft,
            "publishable": decision == "suggest" and public_draft is not None,
            "approval_required": True,
            "model": model,
            "usage": usage,
            "latency_ms": latency_ms,
        }

    def suggest(
        self,
        comment: str,
        publication_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Genera una propuesta validada; no escribe ni publica."""
        context = _safe_context(publication_context or {})
        if is_low_signal(comment):
            return {
                "intent": "low_signal",
                "risk": "low",
                "needs_response": False,
                "character": context["character"],
                "draft": None,
                "confidence": 1.0,
                "policy_flags": [],
                "reason": "Reacción mínima o de baja señal; no requiere respuesta.",
                "quality_ok": True,
                "quality": None,
                "decision": "no_response",
                "response": None,
                "publishable": False,
                "approval_required": True,
                "model": "deterministic",
                "usage": {},
                "latency_ms": 0,
            }
        risk_flags = comment_risk_flags(comment)
        if risk_flags:
            return {
                "intent": "other",
                "risk": "high",
                "needs_response": True,
                "character": context["character"],
                "draft": None,
                "confidence": 1.0,
                "policy_flags": list(risk_flags),
                "reason": "El comentario contiene contenido sexual o doble sentido; requiere revisión humana.",
                "quality_ok": False,
                "quality": None,
                "decision": "review",
                "response": None,
                "publishable": False,
                "approval_required": True,
                "model": "deterministic",
                "usage": {},
                "latency_ms": 0,
            }
        result = self.client.chat_json(
            self._messages(comment, context),
            model=self.model,
            max_tokens=260,
            temperature=0.4,
        )
        payload = result.data or {}
        normalized = self._normalize(
            payload,
            context,
            comment,
            model=result.model,
            usage=result.usage,
            latency_ms=result.latency_ms,
        )
        normalized["attempts"] = 1
        normalized["repair"] = {"attempted": False}

        should_repair = (
            normalized["needs_response"]
            and normalized["decision"] == "review"
            and normalized["risk"] != "high"
            and bool(normalized["context_flags"] or not normalized["quality_ok"])
        )
        if not should_repair:
            return normalized

        try:
            repaired = self.client.chat_json(
                self._repair_messages(comment, context, normalized),
                model=self.model,
                max_tokens=260,
                temperature=0.4,
            )
        except Exception as exc:
            normalized["repair"] = {
                "attempted": True,
                "error_type": type(exc).__name__,
            }
            return normalized

        repaired_normalized = self._normalize(
            repaired.data or {},
            context,
            comment,
            model=repaired.model,
            usage=_merge_usage(result.usage, repaired.usage),
            latency_ms=result.latency_ms + repaired.latency_ms,
        )
        repaired_normalized["attempts"] = 2
        repaired_normalized["repair"] = {
            "attempted": True,
            "first_decision": normalized["decision"],
            "first_flags": list(normalized["policy_flags"]),
        }
        return repaired_normalized

    def _load_contexts(self) -> Dict[str, Any]:
        path = self.paths.publication_contexts_file
        if not path.is_file():
            return {}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return payload if isinstance(payload, dict) else {}

    def shadow(
        self,
        *,
        limit: Optional[int] = None,
        report_path: Optional[Path] = None,
        input_path: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Analiza aprobaciones existentes sin modificarlas ni llamar a Meta."""
        source_path = Path(input_path) if input_path else self.paths.approvals_file
        payload = load_approvals(source_path)
        if payload is None:
            raise FileNotFoundError(f"No existe {source_path}")
        approvals = payload.get("approvals") or []
        if not isinstance(approvals, list):
            raise ValueError("'approvals' debe ser una lista")
        if limit is not None:
            if limit < 1:
                raise ValueError("limit debe ser mayor que cero")
            approvals = approvals[:limit]

        contexts = self._load_contexts()
        records: List[Dict[str, Any]] = []
        errors: List[Dict[str, str]] = []
        for item in approvals:
            if not isinstance(item, dict):
                continue
            comment_id = _text(item.get("comment_id"))
            comment_text = _text(item.get("comment_text"))
            reference_approved = item.get("approved") is True
            context, context_found = _find_context(
                contexts,
                comment_id,
                _text(item.get("character")) or "Universe",
            )
            reference_response = _text(item.get("approved_response"))
            record: Dict[str, Any] = {
                "comment_id": comment_id,
                "comment_text": comment_text,
                "context_found": context_found,
                "reference": {
                    "approved": reference_approved,
                    "approved_response": reference_response or None,
                    "quality": check_response(reference_response, max_chars=self.max_chars).to_dict()
                    if reference_response
                    else None,
                },
                "agent": None,
                "matches_reference": None,
                "error": None,
            }
            try:
                result = self.suggest(comment_text, context)
                record["agent"] = result
                record["matches_reference"] = result["needs_response"] == reference_approved
            except Exception as exc:
                message = f"{type(exc).__name__}: {exc}"
                record["error"] = message
                errors.append({"comment_id": comment_id, "error": message})
            records.append(record)

        completed = [record["agent"] for record in records if record["agent"]]
        matches = sum(record["matches_reference"] is True for record in records if record["agent"])
        compared = sum(record["matches_reference"] is not None for record in records)
        true_positive = sum(
            bool(record["agent"]["needs_response"]) and bool(record["reference"]["approved"])
            for record in records
            if record["agent"]
        )
        false_positive = sum(
            bool(record["agent"]["needs_response"]) and not bool(record["reference"]["approved"])
            for record in records
            if record["agent"]
        )
        true_negative = sum(
            not bool(record["agent"]["needs_response"]) and not bool(record["reference"]["approved"])
            for record in records
            if record["agent"]
        )
        false_negative = sum(
            not bool(record["agent"]["needs_response"]) and bool(record["reference"]["approved"])
            for record in records
            if record["agent"]
        )
        usage_totals: Dict[str, int] = {}
        for result in completed:
            for key, value in (result.get("usage") or {}).items():
                if isinstance(value, (int, float)):
                    usage_totals[key] = usage_totals.get(key, 0) + int(value)

        report: Dict[str, Any] = {
            "agent": {
                "name": self.name,
                "mode": self.mode,
                "model": self.model,
                "tenant_id": self.tenant_id,
                "approval_required": True,
                "publication": "disabled",
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "inputs": {
                "approvals_file": str(source_path),
                "publication_contexts_file": str(self.paths.publication_contexts_file),
            },
            "summary": {
                "total": len(records),
                "completed": len(completed),
                "errors": len(errors),
                "needs_response": sum(bool(result["needs_response"]) for result in completed),
                "no_response": sum(not bool(result["needs_response"]) for result in completed),
                "suggested": sum(result["decision"] == "suggest" for result in completed),
                "review": sum(result["decision"] == "review" for result in completed),
                "quality_ok": sum(bool(result["quality_ok"]) for result in completed),
                "quality_failed": sum(
                    result["needs_response"] and not bool(result["quality_ok"])
                    for result in completed
                ),
                "agreement": {
                    "compared": compared,
                    "matches": matches,
                    "mismatches": compared - matches,
                    "rate": round(matches / compared, 4) if compared else None,
                    "true_positive": true_positive,
                    "false_positive": false_positive,
                    "true_negative": true_negative,
                    "false_negative": false_negative,
                },
                "average_confidence": round(
                    sum(float(result["confidence"]) for result in completed) / len(completed), 4
                )
                if completed
                else None,
                "average_latency_ms": round(
                    sum(int(result["latency_ms"]) for result in completed) / len(completed), 1
                )
                if completed
                else None,
                "usage": usage_totals,
            },
            "errors": errors,
            "records": records,
        }

        if report_path is not None:
            destination = Path(report_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(f"{destination.suffix}.tmp")
            temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(destination)
            report["report_path"] = str(destination)
        return report


def _default_report_path(paths: CommentPaths) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return paths.storage_dir / "reports" / f"communications_shadow_{stamp}.json"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Agente de Comunicaciones en modo sugerencia")
    parser.add_argument("--tenant", default="universe", help="Tenant a analizar")
    parser.add_argument("--shadow", action="store_true", help="Ejecuta el análisis sombra")
    parser.add_argument("--limit", type=int, default=None, help="Máximo de comentarios a analizar")
    parser.add_argument("--model", default=os.getenv("OMNIROUTE_MODEL") or DEFAULT_MODEL)
    parser.add_argument("--base-path", type=Path, default=None)
    parser.add_argument("--storage-dir", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None, help="Ruta del reporte JSON")
    parser.add_argument("--input", type=Path, default=None, help="JSON alternativo de aprobaciones")
    parser.add_argument("--no-report", action="store_true", help="No escribe reporte a disco")
    parser.add_argument("--json", action="store_true", help="Imprime el reporte completo")
    args = parser.parse_args(argv)

    if not args.shadow:
        parser.error("Indica --shadow; este agente no publica respuestas")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit debe ser mayor que cero")

    agent = CommunicationsAgent(
        args.tenant,
        base_path=args.base_path,
        storage_dir=args.storage_dir,
        model=args.model,
    )
    report_path = None if args.no_report else (args.report or _default_report_path(agent.paths))
    try:
        report = agent.shadow(
            limit=args.limit,
            report_path=report_path,
            input_path=args.input,
        )
    except Exception as exc:
        print(f"❌ No se pudo ejecutar el análisis sombra: {type(exc).__name__}: {exc}")
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        summary = report["summary"]
        agreement = summary["agreement"]
        print("📡 Análisis sombra del Agente de Comunicaciones")
        print(f"   Tenant: {agent.tenant_id} · Modelo: {agent.model}")
        print(f"   Analizados: {summary['completed']}/{summary['total']} · Errores: {summary['errors']}")
        print(
            f"   Respuesta sugerida: {summary['needs_response']} · "
            f"Sin respuesta: {summary['no_response']}"
        )
        print(
            f"   Calidad: {summary['quality_ok']} OK · "
            f"{summary['quality_failed']} bloqueadas"
        )
        if agreement["compared"]:
            print(
                f"   Acuerdo con aprobación humana: {agreement['matches']}/"
                f"{agreement['compared']} ({agreement['rate']:.0%})"
            )
        if report.get("report_path"):
            print(f"   Reporte: {report['report_path']}")
        print("   Publicación: deshabilitada; se requiere aprobación humana.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
