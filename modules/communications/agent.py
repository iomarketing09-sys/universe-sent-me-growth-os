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


def _safe_context(context: Dict[str, Any], fallback_character: str = "Universe") -> Dict[str, str]:
    """Solo envía contenido público y contexto creativo al modelo."""
    return {
        "character": _text(context.get("character")) or fallback_character,
        "meme_text": _text(context.get("meme_text")),
        "visual_context": _text(context.get("visual_context")),
        "caption": _text(context.get("caption")),
    }


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
            '{"intent":"question|humor|identification|opinion|disagreement|affection|'
            'spam|troll|commercial|mention|low_signal|other",'
            '"risk":"low|medium|high","needs_response":true,"character":"Universe",'
            '"draft":"Respuesta propuesta o null","confidence":0.0,'
            '"policy_flags":[],"reason":"Explicación breve"}\n'
            "Reglas:\n"
            "- La voz es seca, irónica, cotidiana y en personaje; un solo remate breve.\n"
            f"- El draft debe tener máximo {self.max_chars} caracteres, una línea y no explicar el chiste.\n"
            "- No inventes precios, stock, tallas, envíos, descuentos ni disponibilidad.\n"
            "- No des consejo médico, legal, financiero ni terapéutico.\n"
            "- Si el comentario es spam, troll, mención, insulto, riesgo alto o solo una reacción mínima, "
            "usa needs_response=false y draft=null.\n"
            "- Si falta contexto o hay duda, usa needs_response=false y risk=medium.\n"
            "- No incluyas enlaces, menciones, hashtags ni frases corporativas.\n"
            "- La aprobación y publicación siempre las decide una persona."
        )
        user = (
            f"PERSONAJE: {context.get('character') or 'Universe'}\n"
            f"MEME: {context.get('meme_text') or '(sin texto)'}\n"
            f"CONTEXTO VISUAL: {context.get('visual_context') or '(sin descripción)'}\n"
            f"COPY: {context.get('caption') or '(sin copy)'}\n"
            f"COMENTARIO PÚBLICO: {_text(comment)}"
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    def _normalize(
        self,
        payload: Dict[str, Any],
        context: Dict[str, str],
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

        quality = check_response(draft, max_chars=self.max_chars)
        policy_flags = list(model_flags)
        if needs_response:
            policy_flags.extend(quality.flags)
        if risk == "high":
            policy_flags.append("high_risk")
        if model_flags:
            policy_flags.append("model_policy_flag")
        policy_flags = list(dict.fromkeys(policy_flags))

        if not needs_response:
            decision = "no_response"
            public_draft = None
        elif quality.ok and not model_flags and risk != "high":
            decision = "suggest"
            public_draft = draft
        else:
            decision = "review"
            public_draft = None

        reason = _text(payload.get("reason"))
        if decision == "review":
            reason = " ".join(part for part in (reason, quality.reason) if part).strip()

        return {
            "intent": intent,
            "risk": risk,
            "needs_response": needs_response,
            "character": character,
            "draft": draft or None,
            "confidence": _confidence(payload.get("confidence")),
            "policy_flags": policy_flags,
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
        if not _text(comment):
            raise ValueError("El comentario está vacío")
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
        result = self.client.chat_json(
            self._messages(comment, context),
            model=self.model,
            max_tokens=260,
            temperature=0.4,
        )
        payload = result.data or {}
        return self._normalize(
            payload,
            context,
            model=result.model,
            usage=result.usage,
            latency_ms=result.latency_ms,
        )

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
    ) -> Dict[str, Any]:
        """Analiza aprobaciones existentes sin modificarlas ni llamar a Meta."""
        payload = load_approvals(self.paths.approvals_file)
        if payload is None:
            raise FileNotFoundError(f"No existe {self.paths.approvals_file}")
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
                "approvals_file": str(self.paths.approvals_file),
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
        report = agent.shadow(limit=args.limit, report_path=report_path)
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
