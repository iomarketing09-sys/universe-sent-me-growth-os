#!/usr/bin/env python3
from pathlib import Path

FILE = Path("responders/universe_responder.py")
with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

# Reemplazar la función de generación con el nuevo prompt seco y soporte para revisión
old_gen_func_start = "    def _generate_omniroute_response("
new_gen_func = '''    def _generate_omniroute_response(self, publication_context: Dict[str, Any], comment: str, is_review: bool = False) -> Optional[str]:
        """Genera una respuesta en personaje usando OmniRoute y Llama 3.2 Vision."""
        import os
        import requests
        from pathlib import Path

        base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:20128/v1")
        model = os.getenv("OMNIROUTE_MODEL", "nvidia/meta/llama-3.2-11b-vision-instruct")
        api_key = os.getenv("OPENAI_API_KEY", "")

        if not api_key:
            for parent_dir in [Path(__file__).resolve().parents[3], Path(__file__).resolve().parents[4]]:
                env_file = parent_dir / ".env"
                if env_file.exists():
                    with open(env_file, "r", encoding="utf-8") as f:
                        for line in f:
                            if "=" in line and not line.startswith("#"):
                                k, v = line.split("=", 1)
                                if k.strip() in ("OPENAI_API_KEY", "OMNIROUTE_API_KEY"):
                                    api_key = v.strip().strip("'").strip('"')
                                    break
                if api_key:
                    break

        character = self._context_value(publication_context, "character") or "Universe"
        meme_text = self._context_value(publication_context, "meme_text") or ""
        visual_context = self._context_value(publication_context, "visual_context") or ""
        caption = self._context_value(publication_context, "caption") or ""

        sys_prompt = (
            f"Eres la voz del personaje '{character}' de la marca de memes 'Universe Sent Me'.\\n"
            "Reglas de oro de tono:\\n"
            "- Remate MUY CORTO, seco, irónico y directo (máximo 1 sola oración, menos de 90 caracteres).\\n"
            "- NUNCA expliques el chiste ni des rodeos ('Me parece que...', 'Ah genial...'). Ve directo al remate.\\n"
            "- Humor memero cotidiano (prioridades absurdas, comida > romance, cansancio existencial, ironía).\\n"
            "- PROHIBIDO sonar corporativo, amable por compromiso o dar lecciones de vida."
        )

        user_prompt = (
            f"Meme: {meme_text} ({visual_context})\\n"
            f"Copy: {caption}\\n"
            f"Comentario del seguidor: '{comment}'\\n"
        )
        if is_review:
            user_prompt += "Comentario ambiguo o casual. Da un remate cómico muy corto y neutro:\\n"
        else:
            user_prompt += "Remata el chiste con humor en una sola frase corta y directa:\\n"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 50,
            "temperature": 0.7,
            "stream": False
        }

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        try:
            r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=20)
            if r.status_code == 200:
                resp = r.json()["choices"][0]["message"]["content"].strip()
                return resp.strip("'").strip('"')
        except Exception as e:
            print(f"Aviso de OmniRoute en respuesta: {e}")
        return None
'''

# Reemplazar desde def _generate_omniroute_response hasta el inicio de respond
start_idx = code.find(old_gen_func_start)
end_idx = code.find("    def respond(", start_idx)
if start_idx != -1 and end_idx != -1:
    code = code[:start_idx] + new_gen_func + "\n" + code[end_idx:]

# Habilitar propuestas para decisión 'respond' y 'review'
old_call = '''        response_text = None
        if decision == "respond":
            response_text = self._generate_omniroute_response(publication_context, comment)
            if not response_text:
                decision = "review"'''

new_call = '''        response_text = None
        if decision in ("respond", "review"):
            is_rev = (decision == "review")
            response_text = self._generate_omniroute_response(publication_context, comment, is_review=is_rev)'''

if old_call in code:
    code = code.replace(old_call, new_call)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ universe_responder.py actualizado con tono seco y propuestas en revisión.")
