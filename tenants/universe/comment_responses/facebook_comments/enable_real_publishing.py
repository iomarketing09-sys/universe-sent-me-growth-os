#!/usr/bin/env python3
import py_compile
from pathlib import Path

FILE = Path("main.py")
with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

real_publish_func = '''def publish_approved(approval_file: str):
    """Publica las respuestas aprobadas directamente en Facebook Graph API."""
    import os
    import json
    import requests
    from pathlib import Path

    # Obtener token de la página desde el entorno o .env
    token = os.getenv("PAGE_ACCESS_TOKEN") or os.getenv("PAGE_ACCES_TOKEN") or os.getenv("META_ACCESS_TOKEN")
    if not token:
        for parent_dir in [Path(__file__).resolve().parents[2], Path(__file__).resolve().parents[3]]:
            env_file = parent_dir / ".env"
            if env_file.exists():
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line and not line.startswith("#"):
                            k, v = line.split("=", 1)
                            if k.strip() in ("PAGE_ACCESS_TOKEN", "PAGE_ACCES_TOKEN", "META_ACCESS_TOKEN"):
                                token = v.strip().strip("'").strip('"')
                                break
            if token:
                break

    if not token:
        print("❌ Error: No se encontró PAGE_ACCESS_TOKEN en .env")
        return 1

    try:
        with open(approval_file, "r", encoding="utf-8") as f:
            approval_data = json.load(f)

        approvals = approval_data.get("approvals", [])
        to_publish = [a for a in approvals if a.get("approved", False) and a.get("approved_response")]

        print("=" * 80)
        print(f"🚀 PUBLICANDO {len(to_publish)} RESPUESTAS EN META GRAPH API")
        print("=" * 80)

        if not to_publish:
            print("⚠️ No hay comentarios marcados con 'approved: true'.")
            return 0

        success_count = 0
        for i, item in enumerate(to_publish, 1):
            comment_id = item.get("comment_id")
            reply_text = item.get("approved_response")
            char = item.get("character", "Universe")

            print(f"[{i}/{len(to_publish)}] Publicando respuesta de {char}...")
            print(f"    Comentario ID: {comment_id}")
            print(f"    Texto: \\\"{reply_text}\\\"")

            url = f"https://graph.facebook.com/v19.0/{comment_id}/comments"
            payload = {"message": reply_text, "access_token": token}

            try:
                r = requests.post(url, data=payload, timeout=30)
                res = r.json()
                if "id" in res:
                    reply_id = res["id"]
                    print(f"    ✅ Publicado con éxito! Meta Reply ID: {reply_id}")
                    success_count += 1
                else:
                    err = res.get("error", {}).get("message", res)
                    print(f"    ❌ Error de Meta: {err}")
            except Exception as e:
                print(f"    ❌ Error de conexión: {e}")
            print("-" * 80)

        print("=" * 80)
        print(f"📊 RESUMEN: {success_count}/{len(to_publish)} respuestas enviadas a Facebook.")
        print("=" * 80)
        return 0 if success_count == len(to_publish) else 1

    except Exception as e:
        print(f"❌ Error leyendo archivo de aprobaciones: {e}")
        return 1

'''

start_idx = code.find("def publish_approved(approval_file: str):")
end_idx = code.find("def main():", start_idx)

if start_idx != -1 and end_idx != -1:
    code = code[:start_idx] + real_publish_func + code[end_idx:]
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(code)
    py_compile.compile(str(FILE), doraise=True)
    print("✅ main.py actualizado con la función de publicación real.")
else:
    print("⚠️ No se pudo localizar el bloque exacto de publish_approved.")
