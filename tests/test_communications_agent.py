"""Tests del Agente de Comunicaciones, política y cliente OmniRoute."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.communications.agent import CommunicationsAgent
from modules.communications.comments.responder import UniverseResponder
from modules.communications.llm import ChatResult, OmniRouteClient, OmniRouteError, extract_json
from modules.communications.policy import check_response, is_low_signal


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload, ensure_ascii=False)

    def json(self):
        return self.payload


class FakeClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def chat_json(self, messages, **kwargs):
        self.calls.append({"messages": messages, **kwargs})
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return ChatResult(
            content=json.dumps(response, ensure_ascii=False),
            model="openai/gpt-4.1-mini",
            usage={"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130},
            latency_ms=125,
            data=response,
        )


def _agent_result(**overrides):
    payload = {
        "intent": "humor",
        "risk": "low",
        "needs_response": True,
        "character": "Universe",
        "draft": "Primer síntoma detectado.",
        "confidence": 0.86,
        "policy_flags": [],
        "reason": "Comentario con señal suficiente.",
    }
    payload.update(overrides)
    return payload


def test_policy_acepta_remate_corto_y_rechaza_riesgos():
    assert check_response("Primer síntoma detectado.").ok
    assert not check_response("").ok
    assert "too_long" in check_response("x" * 91).flags
    assert "corporate_phrase" in check_response("Gracias por comentar, saludos.").flags
    assert "commercial_claim" in check_response("El precio es $1,899 y hay tallas.").flags
    assert "url" in check_response("Mira https://example.com").flags
    assert "forbidden_phrase" in check_response("El diagnóstico se hace solo.").flags
    assert check_response("Te aprecio mucho.").ok


def test_baja_senal_se_detecta_sin_llamar_al_modelo(tmp_path):
    client = FakeClient([])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    assert is_low_signal("Uff 🔥")
    result = agent.suggest("Uff 🔥", {"character": "Universe"})

    assert client.calls == []
    assert result["decision"] == "no_response"
    assert result["needs_response"] is False
    assert result["model"] == "deterministic"


def test_extract_json_tolera_cercas_y_texto_extra():
    assert extract_json('```json\n{"ok": true}\n```') == {"ok": True}
    assert extract_json('Resultado: {"ok": true, "n": 2} fin') == {"ok": True, "n": 2}
    with pytest.raises(ValueError):
        extract_json("sin json")


def test_cliente_omniroute_envia_json_mode_y_parsea(monkeypatch):
    calls = []

    def fake_post(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse(
            {
                "model": "openai/gpt-4.1-mini",
                "choices": [{"message": {"content": '{"ok": true, "idioma": "es"}'}}],
                "usage": {"total_tokens": 12},
            }
        )

    monkeypatch.setattr("modules.communications.llm.requests.post", fake_post)
    client = OmniRouteClient(
        tenant_id="universe",
        base_url="http://127.0.0.1:20128/v1/",
        api_key="test-secret",
    )

    result = client.chat_json([{"role": "user", "content": "hola"}])

    assert result.data == {"ok": True, "idioma": "es"}
    assert result.usage == {"total_tokens": 12}
    assert calls[0][0] == "http://127.0.0.1:20128/v1/chat/completions"
    assert calls[0][1]["json"]["response_format"] == {"type": "json_object"}
    assert calls[0][1]["headers"]["Authorization"] == "Bearer test-secret"


def test_cliente_omniroute_no_expone_credenciales_en_error(monkeypatch):
    monkeypatch.setattr(
        "modules.communications.llm.requests.post",
        lambda *args, **kwargs: FakeResponse({"error": {"message": "falló"}}, status_code=500),
    )
    client = OmniRouteClient(base_url="http://localhost:1/v1", api_key="secret-value")

    with pytest.raises(OmniRouteError) as exc_info:
        client.chat([{"role": "user", "content": "hola"}])

    assert "secret-value" not in str(exc_info.value)
    assert "HTTP 500" in str(exc_info.value)


def test_agente_no_envia_ids_ni_autor_al_modelo(tmp_path):
    client = FakeClient([_agent_result()])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest(
        "No lo creo jajaja",
        {
            "publication_id": "post-secreto-123",
            "character": "Universe",
            "meme_text": "Te voy a encontrar",
            "caption": "Ups",
        },
    )

    serialized = json.dumps(client.calls[0]["messages"], ensure_ascii=False)
    assert "post-secreto-123" not in serialized
    assert "comment_id" not in serialized
    assert result["decision"] == "suggest"
    assert result["response"] == "Primer síntoma detectado."
    assert result["publishable"] is True
    assert result["approval_required"] is True


def test_agente_bloquea_borrador_que_falla_politica(tmp_path):
    client = FakeClient([_agent_result(draft="El precio es $1,899 y hay tallas disponibles.")])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest("¿Cuánto cuesta?", {"character": "Universe"})

    assert result["needs_response"] is True
    assert result["quality_ok"] is False
    assert result["decision"] == "review"
    assert result["response"] is None
    assert result["publishable"] is False
    assert "commercial_claim" in result["policy_flags"]


def test_responder_bloquea_generacion_fuera_de_politica():
    responder = UniverseResponder()
    responder._classify_comment = lambda comment: "humor"
    responder._relation_to_meme = lambda context, comment: "direct_meme_reference"
    responder._decision = lambda comment_type, relation: "respond"
    responder._is_low_signal = lambda comment: False
    responder._generate_omniroute_response = lambda *args, **kwargs: "El precio es $1,899."

    result = responder.respond({"publication_id": "p1", "character": "Universe"}, "Me encanta")

    assert result["decision"] == "review"
    assert result["response"] is None
    assert result["quality_ok"] is False
    assert "commercial_claim" in result["quality"]["flags"]


def test_shadow_compara_con_aprobacion_sin_escribir_aprobaciones(tmp_path):
    storage = tmp_path / "tenants" / "universe" / "comment_responses" / "facebook_comments"
    storage.mkdir(parents=True)
    context_dir = tmp_path / "tenants" / "universe"
    context_dir.mkdir(parents=True, exist_ok=True)
    approvals_path = storage / "aprobaciones.json"
    approvals_path.write_text(
        json.dumps(
            {
                "approvals": [
                    {
                        "comment_id": "post_1_comment_1",
                        "comment_text": "No lo creo jajaja",
                        "character": "Universe",
                        "approved": True,
                        "approved_response": "No lo creas.",
                    },
                    {
                        "comment_id": "post_1_comment_2",
                        "comment_text": "jajaja",
                        "character": "Universe",
                        "approved": False,
                        "approved_response": "Propuesta anterior.",
                    },
                    {
                        "comment_id": "post_2_comment_3",
                        "comment_text": "Comentario con contexto",
                        "character": "Existencial",
                        "approved": True,
                        "approved_response": "Respuesta humana.",
                    },
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (context_dir / "publication_contexts.json").write_text(
        json.dumps(
            {
                "post_1": {
                    "publication_id": "post_1",
                    "character": "Universe",
                    "meme_text": "Te voy a encontrar",
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    before = approvals_path.read_bytes()
    before_mtime = approvals_path.stat().st_mtime_ns
    client = FakeClient(
        [
            _agent_result(),
            _agent_result(
                intent="opinion",
                draft="Existencia confirmada.",
                confidence=0.7,
            ),
        ]
    )
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)
    report_path = tmp_path / "report.json"

    report = agent.shadow(report_path=report_path)

    assert report_path.is_file()
    assert approvals_path.read_bytes() == before
    assert approvals_path.stat().st_mtime_ns == before_mtime
    assert report["summary"]["completed"] == 3
    assert report["summary"]["agreement"]["matches"] == 3
    assert report["summary"]["agreement"]["true_positive"] == 2
    assert report["summary"]["agreement"]["true_negative"] == 1
    assert report["records"][2]["context_found"] is False
    assert report["records"][0]["reference"]["quality"]["ok"] is True
    assert all("post_1" not in call["messages"][1]["content"] for call in client.calls)
    assert all("author" not in json.dumps(call["messages"]) for call in client.calls)
