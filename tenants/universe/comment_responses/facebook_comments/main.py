#!/usr/bin/env python3
"""
Facebook Comment Response Pilot for Universe Sent Me (Stateful Inbox Edition).

Features:
- Lookback window por horas (--hours, por defecto 48h)
- Detección automática de respuestas de la página (manuales o de bot)
- Filtro de baja señal determinista (emojis, risas, menciones)
- Dashboard ejecutivo de cobertura en tiempo real
- Lista de pendientes ordenada cronológicamente (anti-rezagados)
- Generación automática de plantilla de aprobación
- Modo dry-run y modo live seguro
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.facebook_comments.context.parse_real_pubs import parse_publication_contexts_real
from src.facebook_comments.responders.universe_responder import UniverseResponder


class CommentProcessor:
    """Main processor for Facebook comment responses with Stateful Inbox."""
    
    def __init__(self, dry_run: bool = True, hours: int = 48, max_comments: int = 200, max_context_items: int = 8):
        self.dry_run = dry_run
        self.hours = hours
        self.max_comments = max_comments
        self.max_context_items = max_context_items
        self.responder = UniverseResponder()
        self.publication_contexts = []
        self.page_token = None
        self.page_id = self._get_page_id()
        self.aprobaciones_file = Path(__file__).parent / "aprobaciones.json"

    def _load_environment(self):
        """Load environment variables from .env files."""
        tenant_env = Path(__file__).parent.parent.parent / ".env"
        if tenant_env.exists():
            with open(tenant_env, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key.strip() not in os.environ:
                            os.environ[key.strip()] = value.strip()

    def _get_page_id(self) -> Optional[str]:
        return os.environ.get("FB_PAGE_ID", "1036844829507460")

    def _get_graph_version(self) -> str:
        return os.environ.get("META_GRAPH_VERSION", "v26.0")

    def _get_meta_token(self) -> Optional[str]:
        return os.environ.get("PAGE_ACCESS_TOKEN") or os.environ.get("META_ACCESS_TOKEN") or os.environ.get("PAGE_ACCES_TOKEN")

    def _make_get_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        if not self.page_token:
            print(f"❌ Error: Token vacío para {endpoint}")
            return None
        base_url = f"https://graph.facebook.com/{self._get_graph_version()}/{endpoint}"
        all_params = params.copy()
        all_params['access_token'] = self.page_token
        query = urllib.parse.urlencode(all_params)
        try:
            with urllib.request.urlopen(base_url + "?" + query) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            print(f"❌ Error HTTP {e.code} en {endpoint}: {err_msg}")
            return None
        except Exception as e:
            print(f"❌ Error de conexión en {endpoint}: {e}")
            return None

    def _load_publication_contexts(self):
        self.publication_contexts = []
        json_path = Path(__file__).resolve().parent.parent.parent / "publication_contexts.json"
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.publication_contexts.extend(data.values())
                    elif isinstance(data, list):
                        self.publication_contexts.extend(data)
            except Exception:
                pass

        fixture_path = Path(__file__).parent / "contexts" / "fixture.md"
        if fixture_path.exists():
            try:
                legacy = parse_publication_contexts_real(str(fixture_path))
                self.publication_contexts.extend(legacy)
            except Exception:
                pass

    def _find_context(self, post_id: str) -> Dict[str, Any]:
        clean_id = post_id.split("_")[-1]
        for ctx in self.publication_contexts:
            pub_id = str(ctx.get("publication_id", ""))
            if post_id in pub_id or clean_id in pub_id:
                return ctx
        return {
            "publication_id": post_id,
            "character": "Universe",
            "asset_ref": "General",
            "meme_text": "",
            "caption": ""
        }

    def _check_already_replied(self, comment: Dict[str, Any]) -> bool:
        """Verifica si la página ya respondió a este comentario."""
        sub_comments = comment.get("comments", {}).get("data", [])
        for sub in sub_comments:
            from_info = sub.get("from", {})
            if str(from_info.get("id")) == str(self.page_id) or from_info.get("name") == "Universe Sent Me":
                return True
        return False

    def run(self) -> int:
        self._load_environment()
        self.page_token = self._get_meta_token()
        if not self.page_token:
            print("❌ Error: No se encontró token en .env")
            return 1
        
        self._load_publication_contexts()
        cutoff_dt = datetime.now(timezone.utc) - timedelta(hours=self.hours)

        print(f"\nConsultando publicaciones y comentarios de las últimas {self.hours} horas...")
        posts_resp = self._make_get_request(
            f"{self.page_id}/posts",
            {"limit": 25, "fields": "id,created_time,message"}
        )
        if not posts_resp or "data" not in posts_resp:
            print("❌ Error al obtener posts de la página.")
            return 1

        recent_posts = []
        for p in posts_resp["data"]:
            created_str = p.get("created_time")
            if created_str:
                p_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                if p_dt >= cutoff_dt:
                    recent_posts.append(p)

        total_comments = 0
        already_replied_count = 0
        low_signal_count = 0
        pending_candidates = []

        for p in recent_posts:
            post_id = p["id"]
            pctx = self._find_context(post_id)

            # Pedimos sub-comentarios para detectar si la página ya contestó
            comm_resp = self._make_get_request(
                f"{post_id}/comments",
                {"limit": 100, "fields": "id,message,created_time,from,comments{id,from,message,created_time}"}
            )
            if not comm_resp or "data" not in comm_resp:
                continue

            for c in comm_resp["data"]:
                total_comments += 1
                comment_text = c.get("message", "").strip()
                author_name = c.get("from", {}).get("name", "Usuario")
                comment_dt_str = c.get("created_time", "")

                # 1. ¿Ya lo respondió la página?
                if self._check_already_replied(c):
                    already_replied_count += 1
                    continue

                # 2. Procesar con el responder
                res = self.responder.respond(publication_context=pctx, comment=comment_text)
                decision = res.get("decision", "no_response")
                comment_type = res.get("comment_type", "")

                # 3. ¿Es baja señal (emojis, risas, menciones)?
                if decision == "no_response" or comment_type == "baja_señal":
                    low_signal_count += 1
                    continue

                # 4. Es un comentario de alta señal pendiente de respuesta
                pending_candidates.append({
                    "comment_id": c["id"],
                    "post_id": post_id,
                    "author": author_name,
                    "comment_text": comment_text,
                    "created_time": comment_dt_str,
                    "character": pctx.get("character") or "Universe",
                    "asset": pctx.get("asset_ref") or "Meme",
                    "proposed_response": res.get("response", ""),
                    "decision": decision,
                    "risk_level": res.get("risk_level", "low"),
                    "review_reason": res.get("review_reason", "")
                })

        # Ordenar pendientes cronológicamente (más antiguo primero)
        pending_candidates.sort(key=lambda x: x["created_time"])

        # ==============================================================================
        # DASHBOARD DE BANDEJA DE ENTRADA
        # ==============================================================================
        print("\n" + "=" * 80)
        print(f"📥 BANDEJA DE COMUNIDAD UNIVERSE SENT ME (Últimas {self.hours} horas)")
        print("=" * 80)
        print(f"  • Posts activos analizados: {len(recent_posts)}")
        print(f"  • Total comentarios recibidos: {total_comments}")
        print(f"    - 🟢 Ya respondidos (por ti o por bot): {already_replied_count}")
        print(f"    - ⚪ Descartados por baja señal (emojis/risas): {low_signal_count}")
        print(f"    - 🟡 PENDIENTES DE ATENCIÓN (Alta señal sin respuesta): {len(pending_candidates)}")
        print("=" * 80)

        if not pending_candidates:
            print("\n✨ ¡Bandeja limpia! No hay comentarios de alta señal pendientes de respuesta.")
            return 0

        print(f"\n🎯 COMENTARIOS PENDIENTES DE RESPUESTA ({len(pending_candidates)}):")
        print("-" * 80)

        approvals_list = []
        for idx, item in enumerate(pending_candidates, 1):
            char = item["character"]
            risk = item["risk_level"]
            risk_badge = "⚠️ REVISIÓN" if risk != "low" or item["decision"] == "review" else "✅ LISTO"
            
            print(f"[{idx}] {risk_badge} | Personaje: {char} | Autor: {item['author']}")
            print(f"    📅 Fecha: {item['created_time']}")
            print(f"    👤 Comentario: \"{item['comment_text']}\"")
            if item["review_reason"]:
                print(f"    🚩 Alerta: {item['review_reason']}")
            print(f"    ✨ Propuesta de {char}: \"{item['proposed_response']}\"")
            print("-" * 80)

            approvals_list.append({
                "comment_id": item["comment_id"],
                "author": item["author"],
                "comment_text": item["comment_text"],
                "character": char,
                "approved_response": item["proposed_response"],
                "approved": False  # Tú decides ponerle True
            })

        # Guardar automáticamente la plantilla de aprobaciones
        template_payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "lookback_hours": self.hours,
            "total_pending": len(approvals_list),
            "instructions": "Cambia 'approved: true' en los comentarios que quieras publicar y edita el texto si deseas.",
            "approvals": approvals_list
        }
        with open(self.aprobaciones_file, "w", encoding="utf-8") as f:
            json.dump(template_payload, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Plantilla de aprobaciones guardada automáticamente en:")
        print(f"   {self.aprobaciones_file}")
        print("\nPara publicar las que apruebes:")
        print("  1. Abre 'aprobaciones.json' y cambia 'approved': true en las deseadas.")
        print("  2. Ejecuta: python3 main.py --live --publish-approved aprobaciones.json\n")
        return 0


def publish_approved(approval_file: str):
    """Publica las respuestas aprobadas directamente en Facebook Graph API."""
    import requests
    token = os.getenv("PAGE_ACCESS_TOKEN") or os.getenv("META_ACCESS_TOKEN")
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
            print(f"    Texto: \"{reply_text}\"")

            url = f"https://graph.facebook.com/v21.0/{comment_id}/comments"

            # Soporte nativo dual: Sticker de imagen vs Texto plano
            if isinstance(reply_text, str) and reply_text.startswith("[STICKER:") and "]" in reply_text:
                st_name = reply_text.split("[STICKER:")[1].split("]")[0].strip()
                print(f"    🎨 Tipo: Sticker ({st_name})")
                from pathlib import Path
                st_paths = [
                    Path(__file__).resolve().parents[2] / "assets" / "stickers" / st_name,
                    Path("/home/universe-sent-me/GoogleDrive/Universe sent me/Respuestas") / st_name
                ]
                st_file = next((p for p in st_paths if p.exists()), None)
                if not st_file:
                    print(f"    ❌ Error: Archivo de sticker no encontrado: {st_name}")
                    continue
                try:
                    with open(st_file, "rb") as img:
                        r = requests.post(url, data={"access_token": token}, files={"source": img}, timeout=30)
                        res = r.json()
                        if "id" in res:
                            print(f"    ✅ Publicado con éxito! Meta Reply ID: {res['id']}")
                            success_count += 1
                        else:
                            err = res.get("error", {}).get("message", res)
                            print(f"    ❌ Error de Meta: {err}")
                except Exception as e:
                    print(f"    ❌ Error de conexión: {e}")
            else:
                print(f"    Texto: \"{reply_text}\"")
                payload = {"message": reply_text, "access_token": token}
                try:
                    r = requests.post(url, data=payload, timeout=30)
                    res = r.json()
                    if "id" in res:
                        print(f"    ✅ Publicado con éxito! Meta Reply ID: {res['id']}")
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


def main():
    parser = argparse.ArgumentParser(description="Facebook Comment Response Pilot for Universe Sent Me")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Modo prueba (GET real, no publica)")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Modo en vivo para publicar")
    parser.add_argument("--hours", type=int, default=48, help="Ventana de tiempo en horas a revisar (por defecto 48)")
    parser.add_argument("--publish-approved", metavar="FILE", help="Publica las respuestas aprobadas desde JSON")
    
    args = parser.parse_args()
    
    if args.publish_approved:
        if args.dry_run:
            print("❌ Error: --publish-approved requiere el flag --live.")
            return 1
        return publish_approved(args.publish_approved)
    
    processor = CommentProcessor(dry_run=args.dry_run, hours=args.hours)
    return processor.run()


if __name__ == "__main__":
    sys.exit(main())
