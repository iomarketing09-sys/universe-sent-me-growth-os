#!/usr/bin/env python3
import re
from pathlib import Path

FILE = Path("universe_responder.py")
BACKUP = Path("universe_responder.py.bak_omniroute")

with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

with open(BACKUP, "w", encoding="utf-8") as f:
    f.write(code)

# 1. Agregar métodos _is_low_signal y _generate_omniroute_response
helper_methods = '''
    def _is_low_signal(self, comment: str) -> bool:
        """Detecta comentarios mínimos, risas solas, emojis o monosílabos (Regla Gris)."""
        if not comment:
            return True
        clean = re.sub(r'[^\w\s]', '', comment).strip().lower()
        if len(clean) < 3:
            return True
        # Solo risas
        if re.fullmatch(r'(ja|je|ji|jo|ha|he|hi|ho|lol|xd|lmao)+', clean):
            return True
        # Monosílabos y acuerdos vacíos
        low_words = {
            "exacto", "si", "sí", "no", "total", "cierto", "tal cual",
            "literal", "amén", "amen", "de acuerdo", "así es", "asi es",
            "confirmo", "x2", "x3", "omg", "wow", "uy", "ay", "sep", "nop", "bien"
        }
        if clean in low_words:
            return True
        if comment.strip().startswith("@"):
            return True
        return False

    def _generate_omniroute_response(self, publication_context: Dict[str, Any], comment: str) -> Optional[str]:
        """Genera una respuesta en personaje usando OmniRoute y Llama 3.2 Vision."""
        import requests
        import os
        base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:20128/v1")
        model = os.getenv("OMNIROUTE_MODEL", "nvidia/meta/llama-3.2-11b-vision-instruct")
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        if not api_key:
            env_path = Path(__file__).resolve().parents[2] / ".env"
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        if line.startswith("OMNIROUTE_API_KEY=") or line.startswith("OPENAI_API_KEY="):
                            api_key = line.strip().split("=", 1).strip("\x27\"")
        
        character = self._context_value(publication_context, "character") or "Universe"
        meme_text = self._context_value(publication_context, "meme_text") or ""
        visual_context = self._context_value(publication_context, "visual_context") or ""
        caption = self._context_value(publication_context, "caption") or ""
        
        sys_prompt = (
            f"Eres el generador de respuestas comunitarias de 'Universe Sent Me'.\\n"
            f"Responde desde la voz del personaje '{character}'.\\n"
            "Reglas de tono:\\n"
            "- Humor cálido, breve, irónico y empático con la situación del meme.\\n"
            "- Máximo 140 caracteres.\\n"
            "- PROHIBIDO sonar corporativo (NUNCA digas 'gracias por comentar', 'gracias por ser parte de la comunidad', 'saludos').\\n"
            "- Ríete con el seguidor, no del seguidor."
        )
        
        user_prompt = (
            f"Contexto del meme:\\n"
            f"- Personaje: {character}\\n"
            f"- Texto del meme: {meme_text}\\n"
            f"- Escena visual: {visual_context}\\n"
            f"- Caption: {caption}\\n\\n"
            f"Comentario del seguidor:\\n"
            f"'{comment}'\\n\\n"
            "Genera una respuesta en personaje:"
        )
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 80,
            "temperature": 0.7,
            "stream": False
        }
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        try:
            r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=20)
            if r.status_code == 200:
                resp = r.json()["choices"][0]["message"]["content"].strip()
                return resp.strip('"\'')
        except Exception as e:
            print(f"Aviso de OmniRoute en respuesta: {e}")
        return None
'''

# Inyectar métodos auxiliares antes de respond()
code = code.replace("    def respond(", helper_methods + "\n    def respond(")

# 2. Actualizar el método respond() para usar el filtro y OmniRoute
old_respond_start = '''    def respond(self, publication_context: Dict[str, Any], comment: str) -> Dict[str, Any]:
        """Main response generation method."""
        raw_type = self._classify_comment(comment)'''

new_respond_start = '''    def respond(self, publication_context: Dict[str, Any], comment: str) -> Dict[str, Any]:
        """Main response generation method."""
        # 1. Filtro estricto de baja señal (Gris)
        if self._is_low_signal(comment):
            return {
                "publication_id": publication_context.get("publication_id"),
                "comment": comment,
                "comment_type": "baja_señal",
                "apparent_intent": "Reacción mínima, risa o baja señal (Gris)",
                "relation_to_meme": "general_reaction",
                "decision": "no_response",
                "response": None,
                "risk_level": "low"
            }

        raw_type = self._classify_comment(comment)'''

code = code.replace(old_respond_start, new_respond_start)

# 3. Sustituir la llamada a _generate_base_response y _add_cosmic_optional por _generate_omniroute_response
old_gen = '''        response_text = None
        if decision == "respond":
            # Generate a simple contextual response based on comment type and meme context
            response_text = self._generate_base_response(comment_type, intention, relation_to_meme, publication_context)
            if response_text and self._passes_quality(response_text):
                response_text = self._add_cosmic_optional(response_text)
            else:
                response_text = None  # Fall back to no response if quality check fails'''

new_gen = '''        response_text = None
        if decision == "respond":
            # Llamar a OmniRoute con Llama 3.2 y el contexto del meme
            response_text = self._generate_omniroute_response(publication_context, comment)
            if not response_text:
                decision = "review"  # Si OmniRoute no pudo responder, va a revisión sin fallar'''

code = code.replace(old_gen, new_gen)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ universe_responder.py actualizado con filtro de baja señal y OmniRoute.")
