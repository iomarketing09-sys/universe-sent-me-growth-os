"""Responder de comentarios de Universe Sent Me.

La lógica vive en el módulo de comunicaciones. El archivo histórico del tenant
se conserva como envoltorio de compatibilidad.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Optional
import re
import random

from modules.communications.llm import DEFAULT_MODEL, OmniRouteClient, OmniRouteError
from modules.communications.comments.paths import load_tenant_config
from modules.communications.policy import check_response, is_low_signal, normalize_response


def requires_meme_context(tenant_id: str, base_path: Optional[Path] = None) -> bool:
    """True si el tenant declara que sus comentarios dependen del chiste."""
    config = load_tenant_config(tenant_id, base_path)
    comments = config.get("comments") or {}
    return bool(comments.get("requires_meme_context"))


def lacks_meme_context(
    tenant_id: str,
    base_path: Optional[Path],
    publication_context: Optional[Dict[str, Any]],
) -> bool:
    """True si el tenant necesita el chiste y la publicación no lo tiene."""
    if not requires_meme_context(tenant_id, base_path):
        return False
    meme_text = str((publication_context or {}).get("meme_text") or "").strip()
    return not meme_text


class UniverseResponder:
    def __init__(
        self,
        *,
        tenant_id: str = "universe",
        base_path: Optional[Path] = None,
        client: Optional[OmniRouteClient] = None,
        model: Optional[str] = None,
    ) -> None:
        self.tenant_id = tenant_id
        self.base_path = base_path
        self.client = client
        self.model = model or DEFAULT_MODEL
        # Keyword lists for safety filtering (keep these)
        self.spam_keywords = ["http", ".com", "www", "follow me", "suscribete", "visita mi", "gana dinero", "bitcoin", "cripto"]
        self.troll_keywords = ["idiota", "estúpido", "molesto", "odio", "baste", "callate", "cállate", "basura", "peor", "peor aún"]
        self.commercial_keywords = ["compro", "vendo", "precio", "cuánto cuesta", "dónde compro", "link", "promo", "descuento", "oferta"]
        self.mention_pattern = "@"

        # Minimal question words (we'll also check for '?')
        self.question_words = ["cómo", "qué", "cuándo", "dónde", "por qué", "cuál", "será", "qué es", "como es"]

        # Minimal signals for expressive types (only used when needed to disambiguate)
        self.affection_signals = ["amo", "love", "te quiero", "adoro", "♥", "💖", "te amo", "me encanta", "😍", "😘", "💕"]
        self.opinion_signals = ["pienso", "creo", "opino", "parece", "me parece", "en mi opinión", "según yo"]
        self.disagreement_signals = ["no", "pero", "sin embargo", "aunque", "esto no es", "no estoy de acuerdo", "discrepo"]
        self.personal_experience_signals = ["me pasó", "mi experiencia", "en mi caso", "personalmente", "a mí me"]
        self.story_signals = ["historia", "chisme", "novio", "novia", "ex", "pareja", "rola", "algo pasó", "entonces", "y luego", "resultado", "contar", "te cuento"]
        self.humor_signals = ["jaja", "ja ja", "😂", "🤣", "😆", "lol", "risas", "crack", "divertido", "gracioso", "jajaja", "ja ja ja"]

        # Optional cosmic flair phrases (used probabilistically)
        self.cosmic_phrases = [
            "El universo tomó nota de eso.",
            "Los astros susurraron algo al respecto.",
            "Una señal interestelar cruzó el feed.",
            "El destino arquivó este momento bajo 'coincidencias cósmicas'.",
            "Parece que el cosmos tuvo algo que decir.",
            "Según mis cálculos intergalácticos, esto estaba escrito.",
            "La energía del momento resonó en otra galaxia.",
        ]

        # Phrases that would make the response sound institutional, preachy, or unsafe
        self.forbidden_phrases = [
            "deberíamos", "debería", "deberías", "deberían",
            "es importante que", "es necesario que", "hay que",
            "tenemos que", "uno debe", "se debería",
            "diagnosticar", "diagnóstico", "consejo", "aconsejar",
            "terapia", "terapéutico", "lección", "moraleja",
            "respecto a", "en cuanto a", " según estudios",
            "según la ciencia", "demuestra que", "indica que",
        ]

    def _context_value(self, context: Dict[str, Any], *keys: str) -> str:
        """Read canonical context while tolerating legacy fixture keys."""
        for key in keys:
            value = context.get(key)
            if value:
                return str(value)
        return ""

    def _classify_comment(self, comment: str) -> str:
        """Coarse classification using only safety/neutral signals."""
        comment_lower = comment.lower()
        if self.mention_pattern in comment:
            return "mention"
        # Check for person name pattern (two or more capitalized words)
        # Pattern for sequences of capitalized words (allowing for accents and ñ)
        import re
        if re.search(r'\b[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+(?:\s+[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]+)+\b', comment):
            return "mention"
        if any(k in comment_lower for k in self.spam_keywords):
            return "spam"
        if any(k in comment_lower for k in self.troll_keywords):
            return "troll"
        if any(k in comment_lower for k in self.commercial_keywords):
            return "commercial_intent"
        # Question detection: presence of ? or question words
        if '?' in comment or any(w in comment_lower for w in self.question_words):
            return "question"
        # Everything else goes to "other" for now; we will refine later using context
        return "other"

    def _determine_expressive_type(self, comment: str, relation_to_meme: str) -> str:
        """Determine expressive type based on comment and relation to meme.
        Only used when raw_type is 'other' to refine the type for intention/response generation."""
        comment_lower = comment.lower()
        # If relation suggests a specific expressive context, use it
        if relation_to_meme == "humor_extension":
            return "humor"
        if relation_to_meme == "personal_identification":
            return "identification"
        if relation_to_meme == "story_extension":
            return "story_or_gossip"
        # For direct references, we check for expressive signals only if needed
        if relation_to_meme in ["direct_meme_reference", "character_reference", "caption_reference"]:
            # Check for affection
            if any(s in comment_lower for s in self.affection_signals):
                return "affection"
            # Check for opinion
            if any(s in comment_lower for s in self.opinion_signals):
                return "opinion"
            # Check for disagreement (non-troll)
            if any(s in comment_lower for s in self.disagreement_signals):
                return "disagreement"
            # Check for personal experience
            if any(s in comment_lower for s in self.personal_experience_signals):
                return "personal_experience"
            # Check for story
            if any(s in comment_lower for s in self.story_signals):
                return "story_or_gossip"
            # Check for humor
            if any(s in comment_lower for s in self.humor_signals):
                return "humor"
            # Default to other
            return "other"
        # For general_reaction or unclear, we rely on signals in comment
        # Check affection
        if any(s in comment_lower for s in self.affection_signals):
            return "affection"
        # Check opinion
        if any(s in comment_lower for s in self.opinion_signals):
            return "opinion"
        # Check disagreement (non-troll)
        if any(s in comment_lower for s in self.disagreement_signals):
            return "disagreement"
        # Check personal experience
        if any(s in comment_lower for s in self.personal_experience_signals):
            return "personal_experience"
        # Check story
        if any(s in comment_lower for s in self.story_signals):
            return "story_or_gossip"
        # Check humor
        if any(s in comment_lower for s in self.humor_signals):
            return "humor"
        # Default to other
        return "other"

    def _intention_apparent(self, comment_type: str, comment: str, relation_to_meme: str) -> str:
        """Generate intention string based on refined type and relation."""
        intentions = {
            "humor": "Está expresando humor o risa ante la publicación.",
            "identification": "Se identifica con la situación o personaje de la publicación.",
            "personal_experience": "Está compartiendo una experiencia personal relacionada.",
            "story_or_gossip": "Está mencionando una historia personal o chisme relacionado.",
            "question": "Está haciendo una pregunta legítima sobre la publicación o su contenido.",
            "affection": "Está expresando afecto o cariño hacia la publicación o su contenido.",
            "opinion": "Está expresando una opinión o punto de vista sobre la publicación.",
            "disagreement": "Está expresando desacuerdo o una visión contraria.",
            "troll": "Está intentando provocar o molestar (troll).",
            "spam": "Está compartiendo contenido no solicitado o promocional.",
            "commercial_intent": "Está mostrando intención comercial o de compra/venta.",
            "mention": "Está mencionando a alguien en específico.",
            "other": "Está compartiendo un comentario general o de reacción.",
        }
        base = intentions.get(comment_type, "Está compartiendo un comentario.")
        # Add relation nuance if helpful
        if relation_to_meme not in ["general_reaction", "unrelated", "unclear"]:
            base += f" Se relaciona con el meme como: {relation_to_meme}."
        return base

    def _relation_to_meme(self, publication_context: Dict[str, Any], comment: str) -> str:
        """Determine the relationship between comment and publication context by analyzing meme context."""
        comment_lower = comment.lower()

        # Get context values
        meme_text = self._context_value(publication_context, "meme_text")
        caption = self._context_value(publication_context, "caption")
        visual_context = self._context_value(publication_context, "visual_context")
        character = self._context_value(publication_context, "character")
        asset_ref = self._context_value(publication_context, "asset_ref")

        # Check for direct meme text references
        if meme_text:
            # Extract key phrases from meme text (words longer than 3 chars)
            meme_words = [word.strip('.,!?¿¡""''()[]{}') for word in meme_text.lower().split()
                         if len(word.strip('.,!?¿¡""''()[]{}')) > 3]
            # Check if any significant meme word appears in comment
            if any(word in comment_lower for word in meme_words if len(word) > 4):
                return "direct_meme_reference"

        # Check for caption references
        if caption:
            caption_words = [word.strip('.,!?¿¡""''()[]{}') for word in caption.lower().split()
                           if len(word.strip('.,!?¿¡""''()[]{}')) > 3]
            if any(word in comment_lower for word in caption_words if len(word) > 4):
                return "caption_reference"

        # Check for character references
        if character and len(character.strip()) > 1:
            character_lower = character.lower()
            # Check for character name or nicknames
            if character_lower in comment_lower or \
               any(nick in comment_lower for nick in ["el", "la", "los", "las"] if character_lower.startswith(nick) and len(character_lower) > len(nick)+1):
                return "character_reference"

        # Check for visual/context references
        if visual_context:
            visual_words = [word.strip('.,!?¿¡""''()[]{}') for word in visual_context.lower().split()
                          if len(word.strip('.,!?¿¡""''()[]{}')) > 3]
            if any(word in comment_lower for word in visual_words if len(word) > 4):
                return "visual_context_reference"

        # Check for personal identification with the situation
        identification_phrases = ["me pasa", "soy yo", "me siento", "me identifica", "eso soy yo",
                                "me pasó", "me pasó a mí", "a mí me pasa", "me identifica con"]
        if any(phrase in comment_lower for phrase in identification_phrases):
            # If also mentions feeling/experience related to meme topic
            if any(word in comment_lower for word in ["siento", "pasó", "me", "yo"]):
                return "personal_identification"

        # Check for humor/extensions of the meme
        humor_extensions = ["jaja", "ja ja", "😂", "🤣", "😆", "lol", "risas", "crack", "divertido", "gracioso", "jajaja", "ja ja ja",
                          "se parte", "parte el alma", "me mató", "me asesinó", "dead", "kill me"]
        if any(ext in comment_lower for ext in humor_extensions):
            return "humor_extension"

        # Check for story/gossip extensions
        story_extensions = ["historia", "chisme", "novio", "novia", "ex", "pareja", "rola",
                          "algo pasó", "entonces", "y luego", "resultado", "contar", "te cuento"]
        if any(ext in comment_lower for ext in story_extensions):
            return "story_extension"

        # Check if it's a direct question about the content
        question_indicators = ["qué", "cómo", "por qué", "cuándo", "dónde", "cuál", " quién", "cómo es",
                             "qué significa", "qué dice", "qué quiere decir", "perdón", "disculpa"]
        if any(indicator in comment_lower for indicator in question_indicators) and ("?" in comment or True):
            # Check if question relates to meme content
            if meme_text and any(word in comment_lower for word in meme_text.lower().split() if len(word) > 4):
                return "question_about_content"
            elif caption and any(word in comment_lower for word in caption.lower().split() if len(word) > 4):
                return "question_about_content"
            # If it's a generic question like "perdón va?" we still mark as question_about_content? maybe not.
            # We'll leave as general_reaction for now; decision will treat it as review.

        # Default to general reaction if we can't determine a specific relation
        return "general_reaction"

    def _decision(
        self,
        comment_type: str,
        relation_to_meme: str,
    ) -> str:
        """Make decision based on coarse type and refined relation."""
        if comment_type == "mention":
            return "no_response"
        if comment_type in ["spam", "troll", "commercial_intent"]:
            return "no_response"
        if comment_type == "question":
            if relation_to_meme == "question_about_content":
                return "respond"
            else:
                return "review"
        # For expressive types (humor, identification, etc.) we generally respond if relation is not weak
        if comment_type in ["humor", "identification", "personal_experience", "story_or_gossip", "affection", "opinion", "disagreement"]:
            if relation_to_meme in ["direct_meme_reference", "character_reference", "caption_reference",
                                   "humor_extension", "story_extension", "personal_identification",
                                   "visual_context_reference", "question_about_content"]:
                return "respond"
            else:
                # For general_reaction or unclear, we review (could be ambiguous)
                return "review"
        # For other types, we decide based on relation
        if comment_type == "other":
            if relation_to_meme in ["direct_meme_reference", "character_reference", "caption_reference"]:
                return "respond"
            if relation_to_meme in ["topic_reference", "personal_identification", "humor_extension", "story_extension", "general_reaction"]:
                return "review"
            if relation_to_meme in ["unrelated", "unclear"]:
                return "no_response"
        return "no_response"

    def _add_cosmic_optional(self, text: str) -> str:
        """With 30% probability, append a random cosmic phrase."""
        if random.random() < 0.3:
            phrase = random.choice(self.cosmic_phrases)
            return f"{text} {phrase}"
        return text

    def _passes_quality(self, text: str) -> bool:
        """Valida tono, longitud y ausencia de claims antes de publicar."""
        return check_response(
            text,
            extra_forbidden=self.forbidden_phrases,
        ).ok


    def _is_low_signal(self, comment: str) -> bool:
        """Detecta comentarios mínimos, risas solas, emojis o monosílabos (Regla Gris)."""
        return is_low_signal(comment)

    def _generate_omniroute_response(self, publication_context: Dict[str, Any], comment: str, is_review: bool = False) -> Optional[str]:
        """Genera una respuesta en personaje con el cliente OmniRoute compartido."""
        client = self.client or OmniRouteClient(
            tenant_id=self.tenant_id,
            base_path=self.base_path,
        )

        character = self._context_value(publication_context, "character") or "Universe"
        meme_text = self._context_value(publication_context, "meme_text") or ""
        visual_context = self._context_value(publication_context, "visual_context") or ""
        caption = self._context_value(publication_context, "caption") or ""

        sys_prompt = (
            f"Eres la voz del personaje '{character}' de la marca de memes 'Universe Sent Me'.\n"
            "Reglas de oro de tono:\n"
            "- Remate MUY CORTO, seco, irónico y directo (máximo 1 sola oración, menos de 90 caracteres).\n"
            "- NUNCA expliques el chiste ni des rodeos ('Me parece que...', 'Ah genial...'). Ve directo al remate.\n"
            "- Humor memero cotidiano (prioridades absurdas, comida > romance, cansancio existencial, ironía).\n"
            "- PROHIBIDO sonar corporativo, amable por compromiso o dar lecciones de vida."
        )

        user_prompt = (
            f"Meme: {meme_text} ({visual_context})\n"
            f"Copy: {caption}\n"
            f"Comentario del seguidor: '{comment}'\n"
        )
        if is_review:
            user_prompt += "Comentario ambiguo o casual. Da un remate cómico muy corto y neutro:\n"
        else:
            user_prompt += "Remata el chiste con humor en una sola frase corta y directa:\n"

        try:
            result = client.chat(
                [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=self.model,
                max_tokens=80,
                temperature=0.7,
            )
        except OmniRouteError as exc:
            print(f"Aviso de OmniRoute en respuesta: {exc}")
            return None
        except Exception as exc:
            print(f"Aviso de OmniRoute en respuesta: {type(exc).__name__}")
            return None

        response = normalize_response(result.content)
        if response.casefold() in {"", "none", "null"}:
            return None
        return response

    def respond(self, publication_context: Dict[str, Any], comment: str) -> Dict[str, Any]:
        """Main response generation method."""
        if self._is_low_signal(comment):
            return {
                "publication_id": publication_context.get("publication_id"),
                "comment": comment,
                "comment_type": "baja_señal",
                "apparent_intent": "Reacción mínima, risa o baja señal (Gris)",
                "relation_to_meme": "general_reaction",
                "decision": "no_response",
                "response": None,
                "risk_level": "low",
                "quality_ok": True,
                "quality": None,
            }

        raw_type = self._classify_comment(comment)
        relation_to_meme = self._relation_to_meme(publication_context, comment)
        # Determine final expressive type (may override raw_type for 'other')
        if raw_type == "other":
            comment_type = self._determine_expressive_type(comment, relation_to_meme)
        else:
            comment_type = raw_type
        intention = self._intention_apparent(comment_type, comment, relation_to_meme)
        decision = self._decision(comment_type, relation_to_meme)

        if decision in ("respond", "review") and lacks_meme_context(
            self.tenant_id, self.base_path, publication_context
        ):
            return {
                "publication_id": publication_context.get("publication_id"),
                "comment": comment,
                "comment_type": comment_type,
                "apparent_intent": intention,
                "relation_to_meme": relation_to_meme,
                "decision": "sin_contexto",
                "response": None,
                "risk_level": "low",
                "quality_ok": False,
                "quality": None,
                "review_reason": "Falta meme_text para responder con contexto",
            }

        response_text = None
        quality = None
        if decision in ("respond", "review"):
            is_rev = (decision == "review")
            response_text = self._generate_omniroute_response(publication_context, comment, is_review=is_rev)
            if response_text:
                quality = check_response(
                    response_text,
                    extra_forbidden=self.forbidden_phrases,
                )
                if not quality.ok:
                    response_text = None
                    decision = "review"
            else:
                decision = "review"

        result: Dict[str, Any] = {
            "publication_id": publication_context.get("publication_id"),
            "comment": comment,
            "comment_type": comment_type,
            "apparent_intent": intention,
            "relation_to_meme": relation_to_meme,
            "decision": decision,
            "response": response_text,
            "risk_level": "low",
            "quality_ok": quality.ok if quality is not None else response_text is None and decision == "no_response",
            "quality": quality.to_dict() if quality is not None else None,
        }

        # Set risk level and review reason based on decision
        if decision == "review":
            result["risk_level"] = "medium"
            if quality is not None and not quality.ok:
                result["review_reason"] = (
                    "Borrador bloqueado por política de calidad: "
                    + quality.reason
                )
            elif response_text is None:
                result["review_reason"] = (
                    "No se pudo generar un borrador válido; requiere revisión humana."
                )
            else:
                result["review_reason"] = "Requiere revisión humana debido a ambigüedad o posible riesgo."
        elif decision == "respond":
            result["risk_level"] = "low"
        else:  # no_response
            result["risk_level"] = "low"

        return result

    def _generate_base_response(self, comment_type: str, intention: str, relation_to_meme: str, publication_context: Dict[str, Any]) -> Optional[str]:
        """Generate a base response based on comment type and context."""
        # Get meme context for personalization
        meme_text = self._context_value(publication_context, "meme_text")
        caption = self._context_value(publication_context, "caption")
        character = self._context_value(publication_context, "character")

        # Fix Kirby typo if present
        if character == "kirby":
            character = "kiri"

        # Do not respond to baja señal comments
        if intention == "baja_señal":
            return None

        # Contextual responses by type - using actual meme context
        if comment_type == "humor":
            if character == "universe" and meme_text:
                # Extract key phrase from meme for humorous response
                if "humano estupido" in meme_text.lower():
                    return "Jaja, sí nos hacemos los 'humanos estúpidos' por amor y al fin somos humanos. Ese meme nos partió 😂"
                elif "toxica" in meme_text.lower():
                    return "JAJA, caer con persona toxica no nos hace débiles, nos hace humanos. Ese frame 2 es todo un estado de ánimo"
                else:
                    return f"JAJA, eso es demasiado real: '{meme_text[:30]}...' - el universo siempre nos partió"
            elif character == "wilfred":
                return "JAJAJA, qué observación más aguda, Wilfred aprobaría este humor de bosque encantado"
            else:
                return random.choice([
                    "Jaja, sí es bastante relatable 😂",
                    "La verdad me partió también",
                    "Es que es demasiado real",
                    "Sí, el universo tiene sentido del humor",
                    "JAJAJA me identifico totalmente"
                ])

        elif comment_type == "identification":
            if character == "silvio" and meme_text:
                # Silvio's style: wise but direct (removed theatrical elements not in fixture)
                if "bache emocional" in meme_text.lower():
                    return "¡Ay, el bache emocional! Silvio diría: salimos de él, ya sea chisotoso o insoportable"
                else:
                    return f"Exacto, nos pasa a más de uno. Como diría Silvio: '{meme_text[:40]}...'"
            elif character == "wilfred":
                return "Te entiendo completamente, Wilfred asiente desde su lugar"
            else:
                return random.choice([
                    "¡Exacto! Nos pasa a más de uno",
                    "Te entiendo completamente",
                    "Estamos en el mismo barco",
                    "La solidarity es real",
                    "Sí, somos muchos los que hemos estado ahí"
                ])

        elif comment_type == "personal_experience":
            if character == "elara" and meme_text:
                return f"Gracias por compartir tu experiencia. Como diría Elara mientras cultiva su jardín de la mente: cada historia cuenta y la tuya importa"
            else:
                return random.choice([
                    "Gracias por compartir tu experiencia",
                    "Valoro mucho que hayas abierto tu corazón",
                    "Cada historia cuenta, la tuya importa",
                    "Gracias por confiar y compartir",
                    "Tu experiencia le da valor a esta conversación"
                ])

        elif comment_type == "story_or_gossip":
            if character == "universe":
                return "Wow, qué historia más intensa. El gato con lentes dice: gracias por confiar y compartir eso en nuestro universo"
            else:
                return random.choice([
                    "Wow, qué historia más intensa",
                    "Gracias por confiar y compartir eso",
                    "Cada día aprendemos algo nuevo de las historias de otros",
                    "Gracias por ser parte de esta comunidad",
                    "Historias como la tuya nos hacen crecer"
                ])

        elif comment_type == "affection":
            if character == "universe":
                return "¡Gracias! El amor siempre regresa 💖 (dice el gato con lentes mientras ajusta sus espejuelos)"
            else:
                return random.choice([
                    "¡Gracias! El amor siempre regresa 💖",
                    "Te quiero mucho también",
                    "Mutuo, siempre",
                    "El cariño es lo que mueve este universo",
                    "Gracias por existir y brindar tu luz"
                ])

        elif comment_type == "opinion":
            if character == "elara":
                return f"Punto válido, gracias por compartir tu perspectiva. Elara añadiría que cultivamos esa opinión en nuestro jardín mental"
            else:
                return random.choice([
                    "Punto válido, gracias por compartir tu perspectiva",
                    "Interesante forma de verlo",
                    "Gracias por enriquecer la conversación con tu visión",
                    "Cada opinión suma, gracias por la tuya",
                    "Respetamos tu punto de vista, gracias por compartirlo"
                ])

        elif comment_type == "disagreement":
            if character == "wilfred":
                return f"Gracias por tu perspectiva, aunque no esté de acuerdo. Wilfred diría desde su lugar: entiendo tu punto, aunque lo veo diferente"
            else:
                return random.choice([
                    "Gracias por tu perspectiva, aunque no esté de acuerdo",
                    "Entiendo tu punto, aunque lo veo diferente",
                    "Gracias por compartir tu visión, aporta al diálogo",
                    "Respetamos tu opinión, aunque tengamos diferencias",
                    "Gracias por participar, el desacuerdo también enriquece"
                ])

        elif comment_type == "question" and relation_to_meme == "question_about_content":
            # Try to answer based on meme context
            if character == "elara" and meme_text:
                if "jardin de mi mente" in meme_text.lower():
                    return "Según Elara: cultivando el jardin de la mente significa poner límites ('Ahorita no papito') y enfocarse en el crecimiento interior. Es decir 'no' a lo que nos agota"
                elif "michelada" in meme_text.lower():
                    return "Como diría Elara: aceptar que somos más como una michelada que colágeno o ensure... con chilito y cacahuates, por supuesto"
            elif meme_text:
                return f"Según el meme: '{meme_text}' - es una reflexión sobre cómo nos afectan ciertas situaciones."
            elif caption:
                return f"La publicación dice: '{caption}' - habla sobre precisamente eso que preguntas."
            else:
                return "Buena pregunta, trata sobre cómo ciertas situaciones nos impactan emocionalmente."

        elif comment_type == "other":
            if relation_to_meme in ["direct_meme_reference", "character_reference", "caption_reference"]:
                if character == "silvio":
                    return f"¡Le pegaste al tema central! Silvio aprobaría con una frase sobre baches emocionales"
                elif character == "elara":
                    return f"Exacto, conectaste con la esencia del meme. Como diría Elara mientras riega sus plantas mentales: 'Sabiduría pura'"
                else:
                    return "Exacto, le pegaste al tema central de la publicación."
            elif relation_to_meme in ["humor_extension", "story_extension"]:
                return "Gracias por seguir la onda y agregar tu toque."
            else:
                return "Gracias por participar en la conversación."

        return None  # Default to no response if we can't generate something appropriate
