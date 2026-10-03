#!/usr/bin/env python3
from pathlib import Path

FILE = Path("main.py")
with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

with open("main.py.bak_dashboard", "w", encoding="utf-8") as f:
    f.write(code)

# 1. Inicializar contadores y listas
old_init = "        processed_count = 0\n        needs_response_count = 0"
new_init = """        processed_count = 0
        needs_response_count = 0
        ready_to_respond = []
        need_review = []
        low_signal_count = 0
        already_seen_count = 0
        total_examined = 0"""

if old_init in code:
    code = code.replace(old_init, new_init)

# 2. Suprimir impresión ruidosa individual y clasificar en listas
old_display = '''                # Display result
                print(f"\\nComment ID: {result['comment_id']}")
                print(f"Comment: {result['comment_text'][:100]}{'...' if len(result['comment_text']) > 100 else ''}")
                print(f"Filter Reason: {result.get('filter_reason', 'N/A')}")
                print(f"Processed: {result['processed']}")
                print(f"Needs Response: {result['needs_response']}")
                if "responder_result" in result:
                    resp = result["responder_result"]
                    if result.get("needs_response"):
                        print(f"Response: {resp.get('response')}")
                    print(f"Type: {resp.get('comment_type', 'N/A')}")
                    print(f"Intent: {resp.get('apparent_intent', 'N/A')}")
                    print(f"Relation to Meme: {resp.get('relation_to_meme', 'N/A')}")
                    print(f"Decision: {resp.get('decision', 'N/A')}")
                    print(f"Risk Level: {resp.get('risk_level', 'N/A')}")
                    if resp.get("review_reason"):
                        print(f"Review Reason: {resp.get('review_reason')}")
                print("-" * 40)'''

new_display = '''                total_examined += 1
                if result.get("filter_reason") == "Already seen":
                    already_seen_count += 1
                else:
                    resp = result.get("responder_result", {})
                    decision = resp.get("decision", result.get("decision"))
                    if decision == "no_response" or result.get("comment_type") == "baja_señal":
                        low_signal_count += 1
                    elif decision == "respond" and result.get("needs_response"):
                        ready_to_respond.append((result, publication_context))
                    elif decision == "review":
                        need_review.append((result, publication_context))'''

if old_display in code:
    code = code.replace(old_display, new_display)

# 3. Reemplazar resumen con el Tablero Ejecutivo
old_summary = '''        print(f"\\nSummary:")
        print(f"- Comments examined: {len(posts) * 50 if posts else 0}")  # Approximate
        print(f"- Comments processed: {processed_count}")
        print(f"- Comments needing response: {needs_response_count}")
        print(f"- Comments filtered out: {len(posts) * 50 - processed_count if posts else 0}")
        
        if needs_response_count > 0 and not self.dry_run:
            print("\\n⚠️  WARNING: Live mode detected comments needing response!")
            print("   Use --publish-approved with an approval file to publish responses.")
        elif needs_response_count > 0 and self.dry_run:
            print(f"\\n💡 Dry-run mode: {needs_response_count} comments would need response.")
            print("   To publish, use --publish-approved with an approval file.")
        
        print("="*80)'''

new_summary = '''        # Render Tablero Ejecutivo
        print("\n" + "="*80)
        print(f"🎯 PROPUESTAS LISTAS PARA RESPONDER ({len(ready_to_respond)})")
        print("="*80)
        if not ready_to_respond:
            print("  (No hay comentarios con propuesta en este lote)")
        else:
            for idx, (res, pctx) in enumerate(ready_to_respond, 1):
                char = pctx.get("character") or "Universe"
                asset = pctx.get("asset_ref") or "Meme"
                resp_text = res.get("responder_result", {}).get("response") or "N/A"
                post_id = res["comment_id"].split("_")[0]
                print(f"[{idx}] Post: {post_id} | Personaje: {char} ({asset})")
                print(f"    👤 Comentario: \"{res['comment_text']}\"")
                print(f"    ✨ Respuesta: \"{resp_text}\"")
                print("-" * 80)

        print("\n" + "="*80)
        print(f"⚠️  COMENTARIOS PARA REVISIÓN HUMANA / SENSIBLES ({len(need_review)})")
        print("="*80)
        if not need_review:
            print("  (Ningún comentario sensible o agresivo detectado)")
        else:
            for idx, (res, pctx) in enumerate(need_review, 1):
                reason = res.get("responder_result", {}).get("review_reason") or "Requiere revisión"
                risk = res.get("responder_result", {}).get("risk_level", "medium")
                post_id = res["comment_id"].split("_")[0]
                print(f"[{idx}] Post: {post_id} | Riesgo: {risk}")
                print(f"    👤 Comentario: \"{res['comment_text']}\"")
                print(f"    🚩 Motivo: {reason}")
                print("-" * 80)

        print("\n" + "="*80)
        print("📊 RESUMEN OPERATIVO")
        print("="*80)
        print(f"  • Total comentarios examinados: {total_examined}")
        print(f"  • Descartados por baja señal (emojis, risas, menciones vacías): {low_signal_count}")
        print(f"  • Omitidos por ya haber sido vistos: {already_seen_count}")
        print(f"  • Requieren revisión humana (sensibles/agresivos): {len(need_review)}")
        print(f"  • Propuestas generadas listas para responder: {len(ready_to_respond)}")
        print("="*80)
        
        if len(ready_to_respond) > 0 and self.dry_run:
            print("💡 Dry-run mode: Para guardar plantilla de aprobación, usa:")
            print("   python3 main.py --create-template aprobaciones.json")
        print("="*80)'''

if old_summary in code:
    code = code.replace(old_summary, new_summary)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ main.py actualizado con el Tablero Ejecutivo.")
