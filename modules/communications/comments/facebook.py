#!/usr/bin/env python3
"""Captura y publicación de comentarios de Facebook.

El procesador recibe el tenant y sus rutas de forma explícita. Importar el
módulo no lee credenciales, no crea directorios y no publica nada.

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
import time
import urllib.error
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from modules.communications.comments.log import (
    append_comment_log,
    merge_approval_payload,
    migrate_comment_log,
    write_json_atomic,
)
from modules.communications.comments.paths import CommentPaths, load_tenant_config
from modules.communications.comments.responder import (
    UniverseResponder,
    lacks_meme_context,
    requires_meme_context,
)
from modules.config.env import META_ENV_KEYS, load_env_values, parse_env_file


def load_env_file(path: Path, override: bool = False) -> Dict[str, str]:
    """Lee un archivo Meta sin modificar ``os.environ``."""
    del override
    return {
        key: value
        for key, value in parse_env_file(path).items()
        if key in META_ENV_KEYS
    }


def load_environment(
    base_path: Optional[Path] = None,
    tenant_id: str = "universe",
) -> Dict[str, str]:
    paths = CommentPaths.for_tenant(tenant_id, base_path)
    return load_env_values(paths.env_files, keys=META_ENV_KEYS)


def resolve_page_token(
    user_token: Optional[str],
    page_id: str,
    version: Optional[str] = None,
) -> Optional[str]:
    if not user_token or not page_id:
        return user_token

    version = version or os.getenv("META_GRAPH_VERSION", "v26.0")
    query = urllib.parse.urlencode(
        {
            "fields": "id,name,access_token",
            "access_token": user_token,
            "limit": 100,
        }
    )
    url = f"https://graph.facebook.com/{version}/me/accounts?{query}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        print(f"⚠️ No se pudo resolver el token de página: {exc}")
        return user_token

    for account in payload.get("data", []):
        if str(account.get("id")) == str(page_id) and account.get("access_token"):
            return account["access_token"]
    return user_token


class CommentProcessor:
    """Main processor for Facebook comment responses with Stateful Inbox."""

    def __init__(
        self,
        dry_run: bool = True,
        hours: int = 48,
        max_comments: int = 200,
        max_context_items: int = 8,
        *,
        tenant_id: str = "universe",
        base_path: Optional[Path] = None,
        storage_dir: Optional[Path] = None,
        response_agent: bool = False,
        agent_model: Optional[str] = None,
        agent: Optional[Any] = None,
    ):
        self.dry_run = dry_run
        self.hours = hours
        self.max_comments = max_comments
        self.max_context_items = max_context_items
        self.tenant_id = tenant_id
        self.paths = CommentPaths.for_tenant(tenant_id, base_path, storage_dir)
        self.base_path = self.paths.base_path
        self.tenant_config = load_tenant_config(tenant_id, self.base_path)
        self.responder = UniverseResponder(tenant_id=tenant_id, base_path=self.base_path)
        self.response_agent = bool(response_agent or agent is not None)
        self.agent_model = agent_model
        self.agent = agent
        self.publication_contexts = []
        self._environment: Dict[str, str] = {}
        self.page_token = None
        self.page_id = self._get_page_id()
        self.page_name = str(
            self.tenant_config.get("meta", {}).get("page_name")
            or self.tenant_config.get("client_name")
            or "Universe Sent Me"
        )
        self.base_dir = self.paths.storage_dir
        self.aprobaciones_file = self.base_dir / "aprobaciones.json"
        self.comments_log_file = self.base_dir / "data" / "comments_log.csv"

    def _load_environment(self):
        """Load tenant and repository environment files."""
        self._environment = load_environment(self.base_path, self.tenant_id)

    def _get_page_id(self) -> Optional[str]:
        configured = str((self.tenant_config.get("meta") or {}).get("page_id") or "")
        return self._environment.get("FB_PAGE_ID") or configured or None

    def _get_graph_version(self) -> str:
        return self._environment.get("META_GRAPH_VERSION", "v26.0")

    def _get_meta_token(self) -> Optional[str]:
        return (
            self._environment.get("PAGE_ACCESS_TOKEN")
            or self._environment.get("META_ACCESS_TOKEN")
            or self._environment.get("PAGE_ACCES_TOKEN")
        )

    def _get_explicit_page_token(self) -> Optional[str]:
        return self._environment.get("PAGE_ACCESS_TOKEN") or self._environment.get(
            "PAGE_ACCES_TOKEN"
        )

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
        json_path = self.paths.publication_contexts_file
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
            if str(from_info.get("id")) == str(self.page_id) or from_info.get("name") == self.page_name:
                return True
        return False

    def _register_missing_contexts(self, posts: List[Dict[str, Any]]) -> int:
        """Abre una fila vacía en el CSV de dictado para posts sin chiste.

        Solo aplica a tenants que declaran ``comments.requires_meme_context``.
        No escribe el JSON: el chiste entra por el CSV y el import explícito.
        """
        if not requires_meme_context(self.tenant_id, self.base_path):
            return 0
        csv_path = (
            self.paths.tenant_dir / "metrics" / "publication_contexts_review.csv"
        )
        rows: List[Dict[str, str]] = []
        if csv_path.is_file():
            with csv_path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
        known = {str(row.get("id") or "").strip() for row in rows}
        known.update(
            str(ctx.get("publication_id") or "").strip()
            for ctx in self.publication_contexts
        )

        added = 0
        for post in posts:
            post_id = str(post.get("id") or "").strip()
            if not post_id or post_id in known:
                continue
            if str(self._find_context(post_id).get("meme_text") or "").strip():
                continue
            message = " ".join(str(post.get("message") or "").split())
            character = ""
            for tag in message.split():
                if tag.startswith("#") and tag.endswith("USM") and len(tag) > 4:
                    character = tag[1:-3]
                    break
            rows.append(
                {
                    "id": post_id,
                    "copy": message,
                    "personaje": character,
                    "meme_text": "",
                    "asset_ref": "",
                    "status": "",
                }
            )
            known.add(post_id)
            added += 1

        if not added:
            return 0
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "id",
                    "copy",
                    "personaje",
                    "meme_text",
                    "asset_ref",
                    "status",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)
        return added

    def _load_delegated_comment_ids(self) -> set[str]:
        """IDs ya movidos a otra cola de aprobación, para no duplicarlos."""
        delegated: set[str] = set()
        batch_files = sorted(self.base_dir.glob("aprobaciones_*.json"))
        for path in [self.aprobaciones_file, *batch_files]:
            is_master = path.name == self.aprobaciones_file.name
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            items = payload.get("approvals") if isinstance(payload, dict) else None
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, dict):
                    continue
                delegated_to = bool(item.get("delegated_to"))
                if is_master:
                    if not delegated_to:
                        continue
                else:
                    approved_pending = (
                        item.get("approved") is True
                        and item.get("published") is not True
                        and not str(item.get("reply_id") or "").strip()
                    )
                    if not (delegated_to or approved_pending):
                        continue
                comment_id = str(item.get("comment_id") or "").strip()
                if comment_id:
                    delegated.add(comment_id)
        return delegated

    def _get_response_agent(self):
        if self.agent is None:
            from modules.communications.agent import CommunicationsAgent

            self.agent = CommunicationsAgent(
                self.tenant_id,
                base_path=self.base_path,
                storage_dir=self.paths.storage_dir,
                model=self.agent_model,
            )
        return self.agent

    @staticmethod
    def _agent_result_to_responder(result: Dict[str, Any]) -> Dict[str, Any]:
        """Adapta la salida estructurada del agente al contrato histórico."""
        needs_response = bool(result.get("needs_response"))
        if result.get("decision") == "review":
            decision = "review"
        elif not needs_response:
            decision = "no_response"
        elif result.get("decision") == "suggest":
            decision = "respond"
        else:
            decision = "review"

        response = result.get("response") if decision == "respond" else None
        reason = str(result.get("reason") or "").strip()
        metadata = {
            "name": "communications_agent",
            "model": result.get("model"),
            "intent": result.get("intent"),
            "confidence": result.get("confidence"),
            "quality_ok": result.get("quality_ok"),
            "policy_flags": result.get("policy_flags") or [],
            "usage": result.get("usage") or {},
        }
        return {
            "comment_type": result.get("intent") or "other",
            "apparent_intent": reason,
            "relation_to_meme": "",
            "decision": decision,
            "response": response,
            "risk_level": result.get("risk") or "low",
            "review_reason": reason if decision == "review" else "",
            "quality_ok": result.get("quality_ok"),
            "quality": result.get("quality"),
            "agent_metadata": metadata,
        }

    def _respond_to_comment(
        self,
        publication_context: Dict[str, Any],
        comment: str,
    ) -> Dict[str, Any]:
        if lacks_meme_context(self.tenant_id, self.base_path, publication_context):
            return {
                "publication_id": publication_context.get("publication_id"),
                "comment": comment,
                "comment_type": "sin_contexto",
                "apparent_intent": "Falta el chiste del meme",
                "relation_to_meme": "unclear",
                "decision": "sin_contexto",
                "response": None,
                "risk_level": "low",
                "review_reason": "Falta meme_text para responder con contexto",
            }
        if not self.response_agent:
            return self.responder.respond(publication_context, comment)
        try:
            result = self._get_response_agent().suggest(comment, publication_context)
            return self._agent_result_to_responder(result)
        except Exception as exc:
            print(f"⚠️ Agente de Comunicaciones no disponible; usando fallback: {type(exc).__name__}")
            fallback = self.responder.respond(publication_context, comment)
            fallback["agent_metadata"] = {
                "name": "legacy_responder",
                "fallback": True,
                "error_type": type(exc).__name__,
            }
            return fallback

    def _log_comment(
        self,
        comment: Dict[str, Any],
        result: Dict[str, Any],
        *,
        publish_status: str,
    ) -> None:
        append_comment_log(
            self.comments_log_file,
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "comment_id": comment.get("id", ""),
                "comment_text": comment.get("message", comment.get("text", "")),
                "from_id": comment.get("from", {}).get("id", ""),
                "created_time": comment.get("created_time", ""),
                "processed": True,
                "needs_response": result.get("decision") in ("respond", "review"),
                "response_text": result.get("response") or "",
                "comment_type": result.get("comment_type", ""),
                "apparent_intent": result.get("apparent_intent", ""),
                "relation_to_meme": result.get("relation_to_meme", ""),
                "decision": result.get("decision", ""),
                "risk_level": result.get("risk_level", ""),
                "review_reason": result.get("review_reason", ""),
                "filter_reason": result.get("filter_reason", ""),
                "publish_status": publish_status,
            },
        )

    def run(self) -> int:
        self._load_environment()
        self.page_id = self._get_page_id()
        if not self.page_id:
            print("❌ Error: No hay page_id en config.json ni FB_PAGE_ID")
            return 1
        self.page_token = self._get_explicit_page_token() or resolve_page_token(
            self._get_meta_token(),
            self.page_id,
            self._get_graph_version(),
        )
        if not self.page_token:
            print("❌ Error: No se encontró token en .env")
            return 1

        migration = migrate_comment_log(self.comments_log_file)
        if migration.changed:
            print(
                f"🧹 Log normalizado: {migration.rows} filas "
                f"({migration.legacy_rows} con esquema anterior)."
            )

        self._load_publication_contexts()
        delegated_comment_ids = self._load_delegated_comment_ids()
        if self.response_agent:
            print("🧠 Generador de propuestas: CommunicationsAgent (solo sugerencias).")
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

        opened = self._register_missing_contexts(recent_posts)
        if opened:
            print(f"📝 Filas de dictado abiertas: {opened} (falta meme_text)")

        total_comments = 0
        already_replied_count = 0
        delegated_count = 0
        low_signal_count = 0
        missing_context_count = 0
        pending_candidates = []
        processed_count = 0

        for p in recent_posts:
            if processed_count >= self.max_comments:
                break
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
                if processed_count >= self.max_comments:
                    break
                processed_count += 1
                total_comments += 1
                comment_text = c.get("message", c.get("text", "")).strip()
                author_name = c.get("from", {}).get("name", "Usuario")
                comment_dt_str = c.get("created_time", "")

                # 1. ¿Ya lo respondió la página?
                if self._check_already_replied(c):
                    already_replied_count += 1
                    self._log_comment(
                        c,
                        {"decision": "already_replied", "comment_type": "already_replied"},
                        publish_status="already_replied",
                    )
                    continue

                if str(c.get("id", "")) in delegated_comment_ids:
                    delegated_count += 1
                    self._log_comment(
                        c,
                        {
                            "decision": "delegated",
                            "comment_type": "delegated",
                            "filter_reason": "delegated_to_batch",
                        },
                        publish_status="discarded",
                    )
                    continue

                # 2. Procesar con el responder
                res = self._respond_to_comment(pctx, comment_text)
                decision = res.get("decision", "no_response")
                comment_type = res.get("comment_type", "")

                # 3. ¿Es baja señal (emojis, risas, menciones)?
                if decision == "no_response" or comment_type == "baja_señal":
                    low_signal_count += 1
                    self._log_comment(c, res, publish_status="discarded")
                    continue

                # 3b. Falta el chiste del meme: no se propone respuesta
                if decision == "sin_contexto":
                    missing_context_count += 1
                    self._log_comment(c, res, publish_status="sin_contexto")
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
                    "review_reason": res.get("review_reason", ""),
                    "agent_metadata": res.get("agent_metadata"),
                })
                self._log_comment(c, res, publish_status="pending_approval")

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
        print(f"    - 🔁 Delegados a otra cola: {delegated_count}")
        print(f"    - ⚪ Descartados por baja señal (emojis/risas): {low_signal_count}")
        print(f"    - 🏳️ Sin chiste (falta meme_text): {missing_context_count}")
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

            approval = {
                "comment_id": item["comment_id"],
                "author": item["author"],
                "comment_text": item["comment_text"],
                "character": char,
                "approved_response": item["proposed_response"],
                "approved": False,  # Tú decides ponerle True
                "comment_created_at": item.get("created_time") or "",
                "first_seen_at": datetime.now(timezone.utc).isoformat(),
            }
            if item.get("agent_metadata"):
                approval["agent"] = item["agent_metadata"]
            if item.get("review_reason"):
                approval["review_reason"] = item["review_reason"]
            if item.get("risk_level") and item["risk_level"] != "low":
                approval["risk_level"] = item["risk_level"]
            approvals_list.append(approval)

        existing_payload = None
        if self.aprobaciones_file.exists():
            try:
                with self.aprobaciones_file.open("r", encoding="utf-8") as handle:
                    existing_payload = json.load(handle)
            except (OSError, json.JSONDecodeError):
                existing_payload = None

        template_payload = merge_approval_payload(
            existing_payload,
            approvals_list,
            generated_at=datetime.now(timezone.utc).isoformat(),
            lookback_hours=self.hours,
        )
        write_json_atomic(self.aprobaciones_file, template_payload)

        print(f"\n💾 Plantilla de aprobaciones guardada automáticamente en:")
        print(f"   {self.aprobaciones_file}")
        print("\nPara publicar las que apruebes:")
        print("  1. Abre 'aprobaciones.json' y cambia 'approved': true en las deseadas.")
        print("  2. Ejecuta: python3 main.py --live --publish-approved aprobaciones.json\n")
        return 0


def _existing_page_reply(
    comment_id: str,
    token: str,
    page_id: str,
    page_name: str = "Universe Sent Me",
    version: Optional[str] = None,
) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    import requests

    version = version or os.getenv("META_GRAPH_VERSION", "v26.0")
    url = f"https://graph.facebook.com/{version}/{comment_id}/comments"
    params = {
        "fields": "id,from,message,created_time",
        "limit": 100,
        "access_token": token,
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        payload = response.json()
    except Exception as exc:
        return False, None, str(exc)

    if response.status_code != 200 or "error" in payload:
        return False, None, str(payload.get("error", payload))

    for reply in payload.get("data", []):
        author = reply.get("from", {})
        if str(author.get("id")) == str(page_id) or author.get("name") == page_name:
            return True, reply, ""
    return True, None, ""


def publish_approved(
    approval_file: str,
    comments_log_path: Optional[str] = None,
    *,
    tenant_id: str = "universe",
    base_path: Optional[Path] = None,
    batch_size: Optional[int] = None,
    batch_pause_seconds: int = 0,
) -> int:
    """Publica respuestas aprobadas en tandas y sin repetir las existentes."""
    import requests

    if batch_size is not None and batch_size < 1:
        raise ValueError("batch_size debe ser mayor que cero o None")
    if batch_pause_seconds < 0:
        raise ValueError("batch_pause_seconds no puede ser negativo")

    paths = CommentPaths.for_tenant(tenant_id, base_path)
    config = load_tenant_config(tenant_id, paths.base_path)
    environment = load_environment(paths.base_path, tenant_id)
    page_id = environment.get("FB_PAGE_ID") or str((config.get("meta") or {}).get("page_id") or "")
    page_name = str(
        (config.get("meta") or {}).get("page_name")
        or config.get("client_name")
        or "Universe Sent Me"
    )
    token = (
        environment.get("PAGE_ACCESS_TOKEN")
        or environment.get("PAGE_ACCES_TOKEN")
        or resolve_page_token(
            environment.get("META_ACCESS_TOKEN"),
            page_id,
            environment.get("META_GRAPH_VERSION"),
        )
    )
    if not token:
        print("❌ Error: No se encontró PAGE_ACCESS_TOKEN en .env")
        return 1

    approval_path = Path(approval_file)
    comments_log = (
        Path(comments_log_path)
        if comments_log_path
        else paths.comments_log_file
    )

    try:
        with approval_path.open("r", encoding="utf-8") as handle:
            approval_data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"❌ Error leyendo archivo de aprobaciones: {exc}")
        return 1

    approvals = approval_data.get("approvals", [])
    to_publish = [
        item
        for item in approvals
        if item.get("approved", False)
        and item.get("approved_response")
        and not item.get("published")
        and not item.get("reply_id")
    ]

    print("=" * 80)
    print(f"🚀 PUBLICANDO {len(to_publish)} RESPUESTAS EN META GRAPH API")
    if batch_size:
        batches = (len(to_publish) + batch_size - 1) // batch_size
        print(
            f"   Tandas: {batches} · máximo {batch_size} por tanda · "
            f"pausa {batch_pause_seconds}s"
        )
    print("=" * 80)

    if not to_publish:
        print("⚠️ No hay comentarios nuevos marcados con 'approved: true'.")
        return 0

    version = environment.get("META_GRAPH_VERSION", "v26.0")
    success_count = 0
    failure_count = 0

    for index, item in enumerate(to_publish, 1):
        if (
            batch_size
            and index > 1
            and (index - 1) % batch_size == 0
            and batch_pause_seconds > 0
        ):
            print(
                f"⏸️ Pausa de {batch_pause_seconds}s antes de la tanda "
                f"{(index - 1) // batch_size + 1}..."
            )
            time.sleep(batch_pause_seconds)

        comment_id = str(item.get("comment_id", "")).strip()
        reply_text = str(item.get("approved_response", "")).strip()
        character = item.get("character", "Universe")

        print(f"[{index}/{len(to_publish)}] Publicando respuesta de {character}...")
        print(f"    Comentario ID: {comment_id}")
        print(f"    Texto: \"{reply_text}\"")

        if not comment_id or not reply_text:
            print("    ❌ Error: comment_id o approved_response vacío.")
            failure_count += 1
            continue

        checked, existing_reply, check_error = _existing_page_reply(
            comment_id, token, page_id, page_name, version
        )
        if not checked:
            print(f"    ❌ No se pudo verificar si ya existe respuesta: {check_error}")
            item["last_error"] = f"verificación fallida: {check_error}"
            failure_count += 1
            write_json_atomic(approval_path, approval_data)
            print("-" * 80)
            continue

        if existing_reply:
            published_at = existing_reply.get("created_time") or datetime.now(timezone.utc).isoformat()
            item["published"] = True
            item["published_at"] = published_at
            item["reply_id"] = existing_reply.get("id", "")
            success_count += 1
            append_comment_log(
                comments_log,
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "comment_id": comment_id,
                    "comment_text": item.get("comment_text") or item.get("original_comment", ""),
                    "processed": True,
                    "needs_response": True,
                    "response_text": reply_text,
                    "comment_type": "approval",
                    "decision": "published",
                    "publish_status": "already_published",
                    "published_at": published_at,
                    "reply_id": existing_reply.get("id", ""),
                },
            )
            write_json_atomic(approval_path, approval_data)
            print(f"    ✅ Ya existía en Meta; no se duplicó. Reply ID: {existing_reply.get('id', '')}")
            print("-" * 80)
            continue

        url = f"https://graph.facebook.com/{version}/{comment_id}/comments"
        try:
            if reply_text.startswith("[STICKER:") and "]" in reply_text:
                sticker_name = reply_text.split("[STICKER:")[1].split("]")[0].strip()
                print(f"    🎨 Tipo: Sticker ({sticker_name})")
                sticker_paths = [
                    paths.tenant_dir / "assets" / "stickers" / sticker_name,
                    Path("/home/universe-sent-me/GoogleDrive/Universe sent me/Respuestas") / sticker_name,
                ]
                sticker_file = next((path for path in sticker_paths if path.exists()), None)
                if not sticker_file:
                    raise FileNotFoundError(f"sticker no encontrado: {sticker_name}")
                with sticker_file.open("rb") as image:
                    response = requests.post(
                        url,
                        data={"access_token": token},
                        files={"source": image},
                        timeout=30,
                    )
            else:
                response = requests.post(
                    url,
                    data={"message": reply_text, "access_token": token},
                    timeout=30,
                )
            payload = response.json()
        except Exception as exc:
            item["last_error"] = str(exc)
            failure_count += 1
            write_json_atomic(approval_path, approval_data)
            print(f"    ❌ Error de conexión: {exc}")
            print("-" * 80)
            continue

        reply_id = payload.get("id")
        if response.status_code == 200 and reply_id:
            published_at = datetime.now(timezone.utc).isoformat()
            item["published"] = True
            item["published_at"] = published_at
            item["reply_id"] = reply_id
            item.pop("last_error", None)
            success_count += 1
            append_comment_log(
                comments_log,
                {
                    "timestamp": published_at,
                    "comment_id": comment_id,
                    "comment_text": item.get("comment_text") or item.get("original_comment", ""),
                    "processed": True,
                    "needs_response": True,
                    "response_text": reply_text,
                    "comment_type": "approval",
                    "decision": "published",
                    "publish_status": "published",
                    "published_at": published_at,
                    "reply_id": reply_id,
                },
            )
            write_json_atomic(approval_path, approval_data)
            print(f"    ✅ Publicado con éxito. Meta Reply ID: {reply_id}")
        else:
            error = payload.get("error", {}).get("message", payload)
            item["last_error"] = str(error)
            failure_count += 1
            write_json_atomic(approval_path, approval_data)
            print(f"    ❌ Error de Meta: {error}")
        print("-" * 80)

    print("=" * 80)
    print(f"📊 RESUMEN: {success_count}/{len(to_publish)} respuestas confirmadas en Facebook.")
    if failure_count:
        print(f"⚠️ Fallaron {failure_count}; revisa 'last_error' y vuelve a ejecutar.")
    print("=" * 80)
    return 0 if failure_count == 0 else 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Facebook Comment Response Pilot for Universe Sent Me")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Modo prueba (GET real, no publica)")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Modo en vivo para publicar")
    parser.add_argument("--hours", type=int, default=48, help="Ventana de tiempo en horas a revisar (por defecto 48)")
    parser.add_argument("--max-comments", type=int, default=200, help="Máximo de comentarios a procesar por corrida")
    parser.add_argument("--publish-approved", metavar="FILE", help="Publica las respuestas aprobadas desde JSON")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Máximo de respuestas por tanda al publicar aprobadas (default: 5)",
    )
    parser.add_argument(
        "--batch-pause-seconds",
        type=int,
        default=900,
        help="Pausa entre tandas al publicar aprobadas (default: 900s)",
    )
    parser.add_argument("--tenant-id", default="universe", help="Tenant dueño de los comentarios")
    parser.add_argument("--base-path", type=Path, default=None, help="Raíz del repositorio")
    parser.add_argument("--storage-dir", type=Path, default=None, help="Directorio de datos de comentarios")
    parser.add_argument(
        "--agent",
        action="store_true",
        help="Genera propuestas con CommunicationsAgent (solo sugerencias, nunca publica)",
    )
    parser.add_argument("--agent-model", default=None, help="Modelo de OmniRoute para el agente")

    args = parser.parse_args(argv)

    if args.publish_approved:
        if args.dry_run:
            print("❌ Error: --publish-approved requiere el flag --live.")
            return 1
        return publish_approved(
            args.publish_approved,
            tenant_id=args.tenant_id,
            base_path=args.base_path,
            batch_size=args.batch_size,
            batch_pause_seconds=args.batch_pause_seconds,
        )

    processor = CommentProcessor(
        dry_run=args.dry_run,
        hours=args.hours,
        max_comments=max(1, args.max_comments),
        tenant_id=args.tenant_id,
        base_path=args.base_path,
        storage_dir=args.storage_dir,
        response_agent=args.agent,
        agent_model=args.agent_model,
    )
    return processor.run()


if __name__ == "__main__":
    raise SystemExit(main())
