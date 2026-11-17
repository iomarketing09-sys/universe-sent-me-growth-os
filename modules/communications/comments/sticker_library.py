"""Biblioteca segura de imágenes de respuesta para Universe Sent Me.

La biblioteca es de solo lectura: nunca mueve ni renombra los originales.
Las sugerencias son metadatos para revisión humana; no publican por sí solas.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any, Optional

DEFAULT_LIBRARY_DIR = Path("/home/universe-sent-me/GoogleDrive/Universe sent me/Respuestas")

# Reglas revisadas visualmente. Los disparadores describen intención, no palabras
# sueltas que puedan convertir una coincidencia accidental en una respuesta.
STICKER_RULES: dict[str, dict[str, Any]] = {
    "no hay meme, solo te amo.jpeg": {
        "label": "Afecto espontáneo", "category": "affection",
        "intent": "Responder a una expresión genuina de cariño.",
        "tone": "afectuoso",
        "triggers": ("te amo", "te quiero", "te mando amor", "solo queria decirte que te quiero"),
        "compatible_context": ("declaraciones de cariño", "mensajes afectuosos"),
        "avoid_context": ("sarcasmo", "conflicto", "burla"),
    },
    "toma este corazon.jpeg": {
        "label": "Gesto de cariño", "category": "affection",
        "intent": "Devolver un gesto afectuoso o enviar un corazón.",
        "tone": "afectuoso",
        "triggers": ("te mando un corazon", "toma un corazon", "te envio un corazon", "va un corazon"),
        "compatible_context": ("agradecimientos afectuosos", "intercambio de corazones"),
        "avoid_context": ("sarcasmo", "discusión"),
    },
    "Me encorazona.jpeg": {
        "label": "Reacción afectuosa", "category": "affection",
        "intent": "Expresar ternura, simpatía o que algo tocó emocionalmente.",
        "tone": "tierno con humor",
        "triggers": ("me encorazona", "me dio ternura", "que bonito detalle", "me llego al corazon"),
        "compatible_context": ("gestos tiernos", "historias emotivas", "muestras de cariño"),
        "avoid_context": ("coqueteo no correspondido", "duelo", "situaciones delicadas"),
    },
    "jaja jaja.jpeg": {
        "label": "Risa compartida", "category": "shared_laughter",
        "intent": "Acompañar una broma que ambas partes encuentran graciosa.",
        "tone": "alegre y cómplice",
        "triggers": ("me estoy riendo", "me hizo reir", "nos dio mucha risa", "no puedo parar de reir", "jajaja"),
        "compatible_context": ("bromas compartidas", "comentarios claramente humorísticos"),
        "avoid_context": ("burla hacia una persona", "sarcasmo hostil", "comentarios de una sola risa sin contexto"),
    },
    "Duermete otro rato.jpeg": {
        "label": "Comentario que no aporta", "category": "silencing_humor",
        "intent": "Bromear cuando alguien reconoce que no tiene nada útil que aportar o insiste en comentar sin contenido.",
        "tone": "sarcástico y directo",
        "triggers": ("si no tienes nada que poner", "no pongas nada", "mejor no comentes", "no tienes nada que aportar", "duermete otro rato"),
        "compatible_context": ("comentarios vacíos reconocidos como broma", "intervenciones fuera de tema sin contenido"),
        "avoid_context": ("cansancio real", "insomnio", "salud", "tristeza", "vulnerabilidad"),
    },
    "money.jpeg": {
        "label": "Dinero / interés económico", "category": "money",
        "intent": "Reaccionar a una conversación explícita sobre dinero, pagos o billetes.",
        "tone": "humorístico",
        "triggers": ("hablando de dinero", "no tengo dinero", "me falta dinero", "me pagas", "cuanto me vas a pagar", "puro dinero", "billetes"),
        "compatible_context": ("pagos", "deudas tratadas en tono ligero", "dinero y ganancias"),
        "avoid_context": ("dificultad económica real", "desempleo", "emergencia", "solicitud de ayuda"),
    },
    "ok respeto tu desicion equivocada.jpeg": {
        "label": "Desacuerdo irónico", "category": "ironic_disagreement",
        "intent": "Expresar desacuerdo de forma irónica sin convertirlo en ataque personal.",
        "tone": "irónico",
        "triggers": ("respeto tu decision", "decision equivocada", "aunque no estoy de acuerdo", "esa decision no tiene sentido"),
        "compatible_context": ("opiniones opuestas en tono ligero", "decisiones debatidas entre conocidos"),
        "avoid_context": ("decisiones médicas", "problemas personales graves", "ataques o humillaciones"),
    },
    "payaso.jpeg": {
        "label": "Ridículo / autoironía", "category": "self_deprecating_humor",
        "intent": "Representar que uno mismo hizo el ridículo o que una situación resultó absurda.",
        "tone": "autoirónico",
        "triggers": ("hice el ridiculo", "quede como payaso", "me siento payaso", "que payasada", "estoy haciendo el ridiculo"),
        "compatible_context": ("anécdotas propias", "errores contados con humor", "situaciones absurdas"),
        "avoid_context": ("insultar a un usuario", "acoso", "humillación", "salud mental"),
    },
    "pero cuenta que no somos adivinos.jpeg": {
        "label": "Pedir contexto", "category": "clarification",
        "intent": "Pedir que alguien explique una historia o comentario que dejó información importante fuera.",
        "tone": "humorístico y directo",
        "triggers": ("no somos adivinos", "cuenta bien el chisme", "explica el contexto", "pero explicate", "y que paso despues"),
        "compatible_context": ("historias incompletas", "anécdotas sin contexto", "chismes contados a medias"),
        "avoid_context": ("trauma", "duelo", "situaciones sensibles", "preguntas genuinas de ayuda"),
    },
    "Universe - Mira te llama tu mama.jpeg": {
        "label": "Retirada humorística", "category": "playful_exit",
        "intent": "Bromear para sugerir que alguien se retire de una conversación o situación, solo cuando existe confianza.",
        "tone": "burlesco y juguetón",
        "triggers": ("te llama tu mama", "tu mama te llama", "ya retirate", "mejor vete", "corre de aqui"),
        "compatible_context": ("bromas entre conocidos", "despedidas juguetonas", "situaciones absurdas"),
        "avoid_context": ("expulsar seriamente a alguien", "conflicto", "acoso", "persona vulnerable"),
    },
    "y la perra seguia y seguia.jpeg": {
        "label": "Insistencia", "category": "persistence",
        "intent": "Señalar en tono de broma que alguien repite algo o no deja de insistir.",
        "tone": "humorístico e irónico",
        "triggers": ("seguia y seguia", "no deja de insistir", "sigue y sigue", "otra vez con lo mismo", "no se cansa de repetir"),
        "compatible_context": ("repetición de una broma", "insistencia ligera", "historias reiterativas"),
        "avoid_context": ("acoso", "hostigamiento", "denuncias", "situaciones de riesgo"),
    },
    "Yo por dentro.jpeg": {
        "label": "Caos interior / identificación", "category": "inner_state",
        "intent": "Mostrar que por dentro se experimenta una reacción intensa distinta de la apariencia exterior.",
        "tone": "identificable y humorístico",
        "triggers": ("asi estoy por dentro", "por dentro estoy gritando", "por dentro soy un caos", "por dentro me siento", "mi mente por dentro"),
        "compatible_context": ("reacciones internas exageradas", "nervios", "caos emocional expresado con humor"),
        "avoid_context": ("crisis emocional", "ataque de pánico real", "duelo", "solicitud de apoyo"),
    },
}

# Imágenes potencialmente hirientes o estigmatizantes: inventariadas, pero
# deliberadamente excluidas del selector automático.
HUMAN_REVIEW_ONLY = {
    "Pastillas para esquizofrenia.jpeg", "Diganle que si esta enfermito.jpeg",
    "pinche desicion toda estupida.jpeg", "toma, para que borres la cuenta.jpeg",
    "Este no es tu muro y no somos tus amigos.jpeg",
}


def _normalize(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", text.casefold())).strip()


def list_stickers(library_dir: Optional[Path] = None) -> list[dict[str, Any]]:
    """Devuelve inventario ordenado sin alterar archivos originales."""
    root = Path(library_dir) if library_dir is not None else DEFAULT_LIBRARY_DIR
    if not root.is_dir():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name.casefold()):
        if not path.is_file() or path.suffix.casefold() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        rule = STICKER_RULES.get(path.name, {})
        items.append({
            "filename": path.name,
            "label": rule.get("label", path.stem),
            "category": rule.get("category", "unclassified"),
            "intent": rule.get("intent", ""),
            "tone": rule.get("tone", ""),
            "triggers": list(rule.get("triggers", ())),
            "compatible_context": list(rule.get("compatible_context", ())),
            "avoid_context": list(rule.get("avoid_context", ())),
            "classified": bool(rule),
            "human_review_only": path.name in HUMAN_REVIEW_ONLY,
            "available": True,
            "size_bytes": path.stat().st_size,
        })
    return items


def suggest_sticker(
    comment: object,
    publication_context: Optional[dict[str, Any]] = None,
    *,
    library_dir: Optional[Path] = None,
) -> Optional[dict[str, Any]]:
    """Sugiere una imagen solo ante una coincidencia textual clara.

    La sugerencia nunca reemplaza el borrador de texto ni autoriza publicación.
    """
    context = publication_context or {}
    corpus = _normalize(" ".join([
        str(comment or ""),
        str(context.get("meme_text") or ""),
        str(context.get("caption") or ""),
        str(context.get("visual_context") or ""),
    ]))
    available = {item["filename"] for item in list_stickers(library_dir)}
    matches: list[tuple[int, str, dict[str, Any], str]] = []
    for filename, rule in STICKER_RULES.items():
        if filename not in available or filename in HUMAN_REVIEW_ONLY:
            continue
        triggers = [_normalize(trigger) for trigger in rule["triggers"]]
        hits = [
            trigger for trigger in triggers
            if trigger and re.search(rf"(?<!\w){re.escape(trigger)}(?!\w)", corpus)
        ]
        if hits:
            matches.append((max(map(len, hits)), filename, rule, max(hits, key=len)))
    if not matches:
        return None
    matches.sort(key=lambda item: (item[0], item[1]), reverse=True)
    # Si hay dos intenciones posibles, no adivinar cuál quiso expresar la persona.
    if len(matches) > 1:
        return None
    _, filename, rule, trigger = matches[0]
    return {
        "filename": filename,
        "label": rule["label"],
        "category": rule["category"],
        "intent": rule["intent"],
        "tone": rule["tone"],
        "compatible_context": list(rule["compatible_context"]),
        "avoid_context": list(rule["avoid_context"]),
        "matched_trigger": trigger,
        "mode": "image_only",
        "requires_human_approval": True,
        "publication_authorized": False,
    }
