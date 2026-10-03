#!/usr/bin/env python3
from pathlib import Path

FILE = Path("main.py")
with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

old_review_block = '''            for idx, item in enumerate(need_review, 1):
                res, pctx = item
                reason = res.get("responder_result", {}).get("review_reason") or "Requiere revision"
                risk = res.get("responder_result", {}).get("risk_level", "medium")
                post_id = res.get("comment_id", "").split("_")[0]
                print(f"[{idx}] Post: {post_id} | Riesgo: {risk}")
                print(f"    👤 Comentario: {res.get('comment_text')}")
                print(f"    🚩 Motivo: {reason}")
                print("-" * 80)'''

new_review_block = '''            for idx, item in enumerate(need_review, 1):
                res, pctx = item
                reason = res.get("responder_result", {}).get("review_reason") or "Requiere revision"
                risk = res.get("responder_result", {}).get("risk_level", "medium")
                post_id = res.get("comment_id", "").split("_")[0]
                char = pctx.get("character") or "Universe"
                resp_text = res.get("responder_result", {}).get("response") or "(Sin propuesta tentativa)"
                print(f"[{idx}] Post: {post_id} | Personaje: {char} | Riesgo: {risk}")
                print(f"    👤 Comentario: {res.get('comment_text')}")
                print(f"    🚩 Motivo: {reason}")
                print(f"    ✨ Propuesta tentativa: {resp_text}")
                print("-" * 80)'''

if old_review_block in code:
    code = code.replace(old_review_block, new_review_block)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ main.py actualizado para mostrar propuestas en revisión humana.")
else:
    print("ℹ️ main.py ya tenía el formato actualizado.")
