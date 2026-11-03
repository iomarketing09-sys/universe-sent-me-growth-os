"""Tests del Agente de Comunicaciones, política y cliente OmniRoute."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from modules.communications.agent import CommunicationsAgent, _context_hints
from modules.communications.comments import facebook as comments_facebook
from modules.communications.comments.responder import UniverseResponder
from modules.communications.llm import ChatResult, OmniRouteClient, OmniRouteError, extract_json
from modules.communications.policy import check_response, comment_risk_flags, is_low_signal


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


class FakeAgent:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def suggest(self, comment, publication_context):
        self.calls.append((comment, publication_context))
        return dict(self.result)


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
    assert check_response("No es garantía de nada.").ok
    assert "brand_slogan" in check_response("Chipitillo no complace, gobierna.").flags
    assert "sexual_double_sense" in check_response("Perfecto, luz y palos en la oscuridad.").flags
    assert "intimacy" in check_response("Desde que me hackeaste el corazón.").flags


def test_baja_senal_se_detecta_sin_llamar_al_modelo(tmp_path):
    client = FakeClient([])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    assert is_low_signal("Uff 🔥")
    assert is_low_signal("Nooooo 😂😂😂😂")
    assert is_low_signal("Caracter ☠️🔥")
    assert not is_low_signal("Caracter 🙃👏")
    result = agent.suggest("Uff 🔥", {"character": "Universe"})
    empty = agent.suggest("", {"character": "Universe"})

    assert client.calls == []
    assert result["decision"] == "no_response"
    assert result["needs_response"] is False
    assert result["model"] == "deterministic"
    assert empty["decision"] == "no_response"


def test_albur_se_envia_a_revision_sin_llamar_al_modelo(tmp_path):
    client = FakeClient([])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)
    comment = "Voy hacer un cuarto oscuro para dar palos de luz"

    assert "sexual_double_sense" in comment_risk_flags(comment)
    result = agent.suggest(comment, {"character": "Kiri+Evan"})

    assert client.calls == []
    assert result["decision"] == "review"
    assert result["risk"] == "high"
    assert result["policy_flags"] == ["sexual_double_sense"]
    assert result["needs_response"] is True
    assert result["response"] is None
    assert "revisión humana" in result["reason"]


def test_contenido_sexual_detectado_por_emoji_queda_en_revision(tmp_path):
    client = FakeClient([])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)
    comment = "Osea si , Pero la entrada eres tu , mamacita 😈🫦👅"

    result = agent.suggest(comment, {"character": "Universe"})

    assert client.calls == []
    assert result["decision"] == "review"
    assert result["risk"] == "high"
    assert "sexual_double_sense" in result["policy_flags"]


def test_modelo_que_marca_contenido_sexual_queda_en_revision(tmp_path):
    client = FakeClient(
        [
            _agent_result(
                intent="sexual",
                risk="high",
                needs_response=False,
                draft=None,
                reason="Contenido sexual explícito.",
            )
        ]
    )
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest("Quiero más de eso contigo", {"character": "Universe"})

    assert result["decision"] == "review"
    assert result["risk"] == "high"
    assert result["needs_response"] is False
    assert result["publishable"] is False


def test_adapter_conserva_revision_sin_respuesta_automatica():
    result = comments_facebook.CommentProcessor._agent_result_to_responder(
        {
            "intent": "sexual",
            "risk": "high",
            "needs_response": False,
            "decision": "review",
            "response": None,
            "reason": "Contenido sexual explícito.",
        }
    )

    assert result["decision"] == "review"
    assert result["response"] is None
    assert result["review_reason"] == "Contenido sexual explícito."
    assert result["risk_level"] == "high"


def test_chiste_literal_del_asset_fuerza_revision_sin_alterar_borrador(tmp_path):
    draft = "Poético y con hambre, la combinación perfecta para Kiri+Evan."
    client = FakeClient([_agent_result(draft=draft)])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest(
        "Que poético!",
        {
            "character": "Kiri+Evan",
            "asset_ref": "260716 - Kiri +Evan - Te voy a comer.png",
            "meme_text": "😏🫣 Te voy a cuidar #UniverseSentMe",
        },
    )

    assert result["decision"] == "review"
    assert result["response"] is None
    assert result["draft"] == draft
    assert "literal_asset_joke" in result["policy_flags"]


def test_borrador_generico_que_ignora_el_meme_fuerza_revision(tmp_path):
    client = FakeClient([_agent_result(draft="¿Urgente? ¿Y para qué? ¿Para complicarte más?")])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest(
        "Me urge una platica de esas",
        {
            "character": "Evan",
            "asset_ref": "260511 - Evan.png",
            "meme_text": "🫣🫣 pues es que también... ¿Que es una plática normal?",
        },
    )

    assert result["decision"] == "review"
    assert result["response"] is None
    assert "context_mismatch" in result["policy_flags"]


def test_borrador_que_ignora_la_broma_de_gasto_fuerza_revision(tmp_path):
    client = FakeClient([_agent_result(draft="Claro, el centro comercial online nunca duerme.")])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest(
        "O por las cosas que miro en páginas raras....",
        {
            "character": "Maeve",
            "asset_ref": "260721 - Maeve - Si supieras cuanto gasto.png",
            "caption": "#MaeveUSM #humor #gastos",
        },
    )

    assert result["decision"] == "review"
    assert "context_mismatch" in result["policy_flags"]


def test_borrador_de_gasto_con_remate_cotidiano_pasa(tmp_path):
    client = FakeClient([_agent_result(draft="Lo raro sale barato, o eso decimos para dormir.")])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest(
        "O por las cosas que miro en páginas raras....",
        {
            "character": "Maeve",
            "asset_ref": "260721 - Maeve - Si supieras cuanto gasto.png",
            "caption": "#MaeveUSM #humor #gastos",
        },
    )

    assert result["decision"] == "suggest"
    assert result["context_flags"] == []


def test_borrador_familiar_que_ignora_el_remate_del_meme_fuerza_revision(tmp_path):
    client = FakeClient([_agent_result(draft="Claro, hablar de ellos es deporte extremo sin medalla.")])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest(
        "De mi cuñado y mi marido no van a estar hablando 😂",
        {
            "character": "Universe",
            "asset_ref": "260626 - Universe.png",
            "meme_text": "El primer síntoma de estar p3ndjo es sentirse muy chingón.",
        },
    )

    assert result["decision"] == "review"
    assert result["response"] is None
    assert "context_mismatch" in result["policy_flags"]


def test_agente_reescribe_una_vez_si_el_borrador_incumple_politica(tmp_path):
    client = FakeClient(
        [
            _agent_result(draft="Ahí tienes el diagnóstico: dos especialistas en sentirse chingones."),
            _agent_result(draft="Ese síntoma ya es tradición familiar."),
        ]
    )
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest(
        "De mi cuñado y mi marido no van a estar hablando 😂",
        {
            "character": "Universe",
            "asset_ref": "260626 - Universe.png",
            "meme_text": "El primer síntoma de estar p3ndjo es sentirse muy chingón.",
        },
    )

    assert result["decision"] == "suggest"
    assert result["attempts"] == 2
    assert result["repair"]["attempted"] is True
    assert "diagnóstico" not in result["draft"].casefold()
    assert len(client.calls) == 2


def test_bandera_del_modelo_impide_sugerir(tmp_path):
    client = FakeClient([_agent_result(policy_flags=["possible_troll"])])
    agent = CommunicationsAgent("universe", base_path=tmp_path, client=client)

    result = agent.suggest("No lo creo jajaja", {"character": "Universe"})

    assert result["decision"] == "review"
    assert result["response"] is None
    assert "model_policy_flag" in result["policy_flags"]


def test_senales_contextuales_no_mezclan_bromas():
    ghost_context = {
        "asset_ref": "260715 - Elara+Fantasma - no te mueres.png",
        "meme_text": "🤷‍♂️✨ #ElaraUSM",
    }
    personal_hints = _context_hints("Apoco si? Siempre has sentido algo por mi?", ghost_context)
    family_hints = _context_hints(
        "De mi cuñado y mi marido no van a estar hablando 😂",
        {
            "asset_ref": "260626 - Universe.png",
            "meme_text": "El primer síntoma de estar p3ndjo es sentirse muy chingón.",
        },
    )

    assert "El remate del asset" not in personal_hints
    assert "evasiva seca" in personal_hints
    assert "ellos son así" in family_hints
    assert "No inventes" in family_hints
    assert "sentirse muy chingón" in family_hints


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
            "asset_ref": "260626 - Universe.png",
            "meme_text": "Te voy a encontrar",
            "caption": "Ups",
        },
    )

    serialized = json.dumps(client.calls[0]["messages"], ensure_ascii=False)
    assert "post-secreto-123" not in serialized
    assert "comment_id" not in serialized
    assert "260626 - Universe.png" in serialized
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


def test_processor_con_agente_genera_aprobacion_false_sin_publicar(tmp_path, monkeypatch):
    agent = FakeAgent(
        {
            "intent": "humor",
            "risk": "low",
            "needs_response": True,
            "character": "Universe",
            "draft": "Primer síntoma detectado.",
            "confidence": 0.9,
            "policy_flags": [],
            "reason": "Señal suficiente.",
            "quality_ok": True,
            "quality": {"ok": True, "flags": []},
            "decision": "suggest",
            "response": "Primer síntoma detectado.",
            "publishable": True,
            "model": "openai/gpt-4.1-mini",
            "usage": {"total_tokens": 100},
            "latency_ms": 50,
        }
    )
    processor = comments_facebook.CommentProcessor(
        dry_run=True,
        hours=48,
        max_comments=1,
        tenant_id="universe",
        base_path=tmp_path,
        response_agent=True,
        agent=agent,
    )
    now = datetime.now(timezone.utc).isoformat()
    processor._load_environment = lambda: None
    processor._get_page_id = lambda: "page_1"
    processor._get_explicit_page_token = lambda: "token"
    processor._load_publication_contexts = lambda: None
    processor.page_id = "page_1"
    processor.publication_contexts = [
        {
            "publication_id": "post_1",
            "character": "Universe",
            "meme_text": "Te voy a encontrar",
        }
    ]

    def fake_get(endpoint, params):
        if endpoint == "page_1/posts":
            return {"data": [{"id": "post_1", "created_time": now}]}
        if endpoint == "post_1/comments":
            return {
                "data": [
                    {
                        "id": "comment_1",
                        "message": "No lo creo jajaja",
                        "created_time": now,
                        "from": {"id": "user_1", "name": "Usuario"},
                        "comments": {"data": []},
                    }
                ]
            }
        return None

    processor._make_get_request = fake_get
    monkeypatch.setattr(
        comments_facebook,
        "append_comment_log",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr("requests.post", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no publicar")))

    assert processor.run() == 0

    payload = json.loads(processor.aprobaciones_file.read_text(encoding="utf-8"))
    approval = payload["approvals"][0]
    assert approval["approved"] is False
    assert approval["approved_response"] == "Primer síntoma detectado."
    assert approval["agent"]["name"] == "communications_agent"
    assert approval["agent"]["model"] == "openai/gpt-4.1-mini"
    assert len(agent.calls) == 1


def test_processor_usa_fallback_si_el_agente_falla(tmp_path):
    class FailingAgent:
        def suggest(self, comment, publication_context):
            raise RuntimeError("sin modelo")

    processor = comments_facebook.CommentProcessor(
        tenant_id="universe",
        base_path=tmp_path,
        response_agent=True,
        agent=FailingAgent(),
    )
    processor.responder.respond = lambda context, comment: {
        "comment_type": "humor",
        "decision": "respond",
        "response": "Respuesta legacy.",
        "risk_level": "low",
    }

    result = processor._respond_to_comment({"character": "Universe"}, "Comentario")

    assert result["response"] == "Respuesta legacy."
    assert result["agent_metadata"]["fallback"] is True
    assert result["agent_metadata"]["error_type"] == "RuntimeError"


def test_cli_de_comentarios_activa_agente_por_flag(monkeypatch):
    captured = {}

    class FakeProcessor:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def run(self):
            return 0

    monkeypatch.setattr(comments_facebook, "CommentProcessor", FakeProcessor)

    assert comments_facebook.main(["--agent", "--agent-model", "openai/gpt-4.1-mini"]) == 0
    assert captured["response_agent"] is True
    assert captured["agent_model"] == "openai/gpt-4.1-mini"
