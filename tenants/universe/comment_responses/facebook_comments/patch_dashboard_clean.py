#!/usr/bin/env python3
import py_compile
from pathlib import Path

FILE = Path("main.py")
with open(FILE, "r", encoding="utf-8") as f:
    code = f.read()

# A. Inicializar listas y contadores
old_init = "        processed_count = 0\n        needs_response_count = 0"
new_init = """        processed_count = 0
        needs_response_count = 0
        ready_to_respond = []
        need_review = []
        low_signal_count = 0
        already_seen_count = 0
        total_examined = 0"""

code = code.replace(old_init, new_init)

# B. Clasificar en listas y suprimir impresión ruidosa individual
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

new_display = """                total_examined += 1
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
                        need_review.append((result, publication_context))"""

code = code.replace(old_display, new_display)

# C. Sustituir resumen final con el Tablero Ejecutivo
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

new_summary = """        print()
        print("=" * 80)
        print(f"🎯 PROPUESTAS LISTAS PARA RESPONDER ({len(ready_to_respond)})")
        print("=" * 80)
        if not ready_to_respond:
            print("  (No hay propuestas pendientes en este lote)")
        else:
            for idx, item in enumerate(ready_to_respond, 1):
                res, pctx = item
                char = pctx.get("character") or "Universe"
                asset = pctx.get("asset_ref") or "Meme"
                resp_text = res.get("responder_result", {}).get("response") or "N/A"
                post_id = res.get("comment_id", "").split("_")[0]
                print(f"[{idx}] Post: {post_id} | Personaje: {char} ({asset})")
                print(f"    👤 Comentario: {res.get('comment_text')}")
                print(f"    ✨ Respuesta: {resp_text}")
                print("-" * 80)

        print()
        print("=" * 80)
        print(f"⚠️  COMENTARIOS PARA REVISION HUMANA / SENSIBLES ({len(need_review)})")
        print("=" * 80)
        if not need_review:
            print("  (Ningun comentario sensible detectado)")
        else:
            for idx, item in enumerate(need_review, 1):
                res, pctx = item
                reason = res.get("responder_result", {}).get("review_reason") or "Requiere revision"
                risk = res.get("responder_result", {}).get("risk_level", "medium")
                post_id = res.get("comment_id", "").split("_")[0]
                print(f"[{idx}] Post: {post_id} | Riesgo: {risk}")
                print(f"    👤 Comentario: {res.get('comment_text')}")
                print(f"    🚩 Motivo: {reason}")
                print("-" * 80)

        print()
        print("=" * 80)
        print("📊 RESUMEN OPERATIVO")
        print("=" * 80)
        print(f"  • Total comentarios examinados: {total_examined}")
        print(f"  • Descartados por baja senal (emojis, risas, menciones vacias): {low_signal_count}")
        print(f"  • Omitidos por ya haber sido vistos: {already_seen_count}")
        print(f"  • Requieren revision humana (sensibles/agresivos): {len(need_review)}")
        print(f"  • Propuestas generadas listas para responder: {len(ready_to_respond)}")
        print("=" * 80)
        
        if len(ready_to_respond) > 0 and self.dry_run:
            print("💡 Dry-run mode: Para guardar plantilla de aprobacion, usa:")
            print("   python3 main.py --create-template aprobaciones.json")
        print("=" * 80)"""

code = code.replace(old_summary, new_summary)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(code)

py_compile.compile(str(FILE), doraise=True)
print("✅ main.py actualizado y compilado con exito.")
