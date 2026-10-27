"""Extrae evidencia de voz a partir de los copys publicados de un tenant.

El perfil `brand_voice.json` describe la voz de forma declarativa. Este módulo
la contrasta con lo que la marca realmente publica en Meta para que el
Copywriter Agent no escriba con una voz genérica o inventada.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF]")
HASHTAG_RE = re.compile(r"#([\wÁÉÍÓÚÜÑáéíóúüñ]+)")
URL_RE = re.compile(r"https?://\S+")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")

STOPWORDS = {
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con",
    "contra", "cual", "cuando", "de", "del", "desde", "donde", "durante", "e",
    "el", "ella", "ellas", "ellos", "en", "entre", "era", "es", "esa", "ese",
    "eso", "esta", "este", "esto", "estos", "estas", "fue", "ha", "hasta",
    "hay", "hoy", "la", "las", "le", "les", "lo", "los", "más", "me", "mi",
    "mis", "muy", "no", "nos", "nuestra", "nuestro", "o", "para", "pero",
    "por", "que", "se", "sin", "sobre", "su", "sus", "te", "tu", "tus", "un",
    "una", "uno", "y", "ya", "también", "tiene", "tienen", "todo", "toda",
    "todos", "todas", "cada", "día", "dias", "días", "así", "aquí",
}

NON_PROPER_WORDS = {
    "para", "hoy", "este", "esta", "cada", "los", "las", "un", "una", "tu",
    "tus", "ven", "elige", "encuentra", "dale", "descubre", "conoce",
    "complementa", "disfruta", "brilla", "confía", "visítanos", "tenemos",
}

LOCAL_PHRASE_WORDS = ("zapater", "piedras", "flexi", "soriana", "híper", "hiper")

DECISION_CUES = (
    "te esperamos", "ven por", "encuentra", "descubre", "elige", "conoce",
    "complementa", "disfruta", "brilla", "dale", "confía", "visítanos",
)

LOCAL_HINT_RE = re.compile(
    r"(?:zapater[ií]a\s+#?[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+|"
    r"piedras\s*negras|soriana(?:\\s+h[ií]per)?(?:\\s+local\s+\\d+)?)",
    re.IGNORECASE,
)


def load_posts(tenant_path: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Carga y deduplica los posts de `data/meta_posts_*.json`."""
    data_dir = tenant_path / "data"
    files = sorted(data_dir.glob("meta_posts_*.json"))
    by_id: Dict[str, Dict[str, Any]] = {}
    used_files: List[str] = []

    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, list):
            continue
        used_files.append(path.name)
        for item in payload:
            if not isinstance(item, dict):
                continue
            message = str(item.get("message") or "").strip()
            if not message:
                continue
            key = str(item.get("post_id") or message[:80])
            current = by_id.get(key)
            if current is None or str(item.get("created_time") or "") > str(
                current.get("created_time") or ""
            ):
                by_id[key] = {
                    "post_id": key,
                    "message": message,
                    "created_time": str(item.get("created_time") or ""),
                    "permalink_url": str(item.get("permalink_url") or ""),
                    "_source_file": path.name,
                }

    posts = sorted(
        by_id.values(),
        key=lambda item: item.get("created_time", ""),
        reverse=True,
    )
    return posts, used_files


def _strip_markup(text: str) -> str:
    text = URL_RE.sub(" ", text)
    text = HASHTAG_RE.sub(" ", text)
    text = EMOJI_RE.sub(" ", text)
    return text


def _words(text: str) -> List[str]:
    clean = _strip_markup(text).lower()
    clean = re.sub(r"[^0-9a-záéíóúüñ\s]", " ", clean)
    return [word for word in clean.split() if len(word) > 2 and word not in STOPWORDS]


def _ngrams(words: Sequence[str], n: int) -> Iterable[Tuple[str, ...]]:
    for index in range(len(words) - n + 1):
        yield tuple(words[index : index + n])


def _percentile(values: Sequence[int], fraction: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * fraction)))
    return ordered[index]


def _sentences(text: str) -> List[str]:
    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]
    return [part for part in parts if not part.startswith("#")]


def _first_hook(text: str) -> str:
    sentences = _sentences(text)
    if not sentences:
        return ""
    return sentences[0][:120]


def _closing(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines = [line for line in lines if not line.replace(" ", "").startswith("#")]
    return lines[-1][:120] if lines else ""


def _proper_nouns(texts: Sequence[str]) -> List[str]:
    counter: Counter[str] = Counter()
    for text in texts:
        for raw in re.findall(r"\b[A-ZÁÉÍÓÚÜÑ][\wáéíóúüñ]{2,}\b", text):
            if raw.lower() in STOPWORDS or raw.lower() in NON_PROPER_WORDS:
                continue
            counter[raw] += 1
    return [word for word, count in counter.most_common(12) if count >= 2]


def _local_markers(texts: Sequence[str]) -> List[str]:
    counter: Counter[str] = Counter()
    for text in texts:
        for match in LOCAL_HINT_RE.findall(text):
            counter[re.sub(r"\s+", " ", match).strip()] += 1
    return [marker for marker, count in counter.most_common(8) if count >= 2]


def _signature_examples(
    posts: Sequence[Dict[str, Any]], median_length: int, limit: int = 4
) -> List[Dict[str, Any]]:
    ranked = sorted(
        posts,
        key=lambda item: abs(len(item["message"]) - median_length),
    )
    examples: List[Dict[str, Any]] = []
    seen_hooks = set()
    for post in ranked:
        hook = _first_hook(post["message"])
        fingerprint = re.sub(r"\W+", "", hook.lower())[:32]
        if fingerprint in seen_hooks:
            continue
        seen_hooks.add(fingerprint)
        examples.append(
            {
                "text": post["message"],
                "created_time": post.get("created_time", ""),
                "chars": len(post["message"]),
                "emojis": len(EMOJI_RE.findall(post["message"])),
                "why": "Hook y ritmo representativos del copy publicado.",
            }
        )
        if len(examples) >= limit:
            break
    return examples


def analyze_posts(
    posts: Sequence[Dict[str, Any]],
    *,
    sources: Sequence[str] = (),
    max_examples: int = 4,
) -> Dict[str, Any]:
    """Devuelve un resumen estructurado y acotado para alimentar al copywriter."""
    texts = [str(post.get("message") or "").strip() for post in posts if post.get("message")]
    if not texts:
        return {
            "posts_analyzed": 0,
            "sources": list(sources),
            "observed_patterns": ["No hay copys publicados disponibles para analizar."],
            "ad_translation": [],
            "signature_examples": [],
        }

    lengths = [len(text) for text in texts]
    median_length = _percentile(lengths, 0.5)
    emoji_counts = [len(EMOJI_RE.findall(text)) for text in texts]
    hashtag_counts = [len(HASHTAG_RE.findall(text)) for text in texts]
    sentence_counts = [len(_sentences(text)) for text in texts]

    hashtags: Counter[str] = Counter()
    for text in texts:
        hashtags.update(f"#{tag}" for tag in HASHTAG_RE.findall(text))

    words: Counter[str] = Counter()
    for text in texts:
        words.update(_words(text))

    bigrams: Counter[str] = Counter()
    trigrams: Counter[str] = Counter()
    for text in texts:
        tokens = _words(text)
        bigrams.update(" ".join(gram) for gram in _ngrams(tokens, 2))
        trigrams.update(" ".join(gram) for gram in _ngrams(tokens, 3))

    hooks = [_first_hook(text) for text in texts]
    second_person_hooks = [
        hook for hook in hooks if re.search(r"\b(tu|tus|te)\b", hook, re.IGNORECASE)
    ]
    decision_posts = [
        text for text in texts if any(cue in text.lower() for cue in DECISION_CUES)
    ]
    exclamation_posts = [text for text in texts if "!" in text]
    question_posts = [text for text in texts if "?" in text]

    created_times = sorted(
        str(post.get("created_time") or "") for post in posts if post.get("created_time")
    )

    observed: List[str] = []
    observed.append(
        f"{len(texts)} posts: longitud mediana {median_length} caracteres "
        f"(rango {min(lengths)}–{max(lengths)})."
    )
    emoji_ratio = sum(1 for count in emoji_counts if count) / len(texts)
    observed.append(
        f"{emoji_ratio:.0%} de los posts usan emojis "
        f"(mediana {_percentile(emoji_counts, 0.5)} por post)."
    )
    hashtag_ratio = sum(1 for count in hashtag_counts if count) / len(texts)
    observed.append(
        f"{hashtag_ratio:.0%} de los posts incluyen hashtags "
        f"(mediana {_percentile(hashtag_counts, 0.5)} por post)."
    )
    observed.append(
        f"{len(second_person_hooks)}/{len(hooks)} hooks abren en segunda persona "
        f"o hablan directamente de 'tu/tus/te'."
    )
    observed.append(
        f"{len(decision_posts)}/{len(texts)} posts cierran con una invitación "
        "a descubrir, elegir, visitar o escribir."
    )
    observed.append(
        f"{len(exclamation_posts)}/{len(texts)} posts usan exclamación y "
        f"{len(question_posts)}/{len(texts)} usan pregunta."
    )
    observed.append(
        f"Mediana de {_percentile(sentence_counts, 0.5)} frases por post; "
        "los hooks son cortos y sensoriales."
    )

    return {
        "posts_analyzed": len(texts),
        "sources": list(sources),
        "period": {
            "from": created_times[0] if created_times else "",
            "to": created_times[-1] if created_times else "",
        },
        "length": {
            "avg_chars": round(sum(lengths) / len(lengths), 1),
            "median_chars": median_length,
            "p25_chars": _percentile(lengths, 0.25),
            "p75_chars": _percentile(lengths, 0.75),
        },
        "emoji": {
            "posts_with_emoji": sum(1 for count in emoji_counts if count),
            "ratio": round(emoji_ratio, 2),
            "median_per_post": _percentile(emoji_counts, 0.5),
        },
        "hashtags": {
            "posts_with_hashtags": sum(1 for count in hashtag_counts if count),
            "ratio": round(hashtag_ratio, 2),
            "top": [tag for tag, _ in hashtags.most_common(10)],
        },
        "openings": list(dict.fromkeys(hook for hook in hooks if hook))[:6],
        "closings": list(
            dict.fromkeys(closing for closing in (_closing(text) for text in texts) if closing)
        )[:4],
        "second_person_openings_ratio": round(len(second_person_hooks) / len(hooks), 2),
        "recurring_words": [word for word, count in words.most_common(15) if count >= 2],
        "recurring_phrases": [
            phrase
            for phrase, count in (trigrams + bigrams).most_common(24)
            if count >= 2
            and not any(word in phrase for word in LOCAL_PHRASE_WORDS)
        ][:10],
        "proper_nouns": _proper_nouns(texts),
        "local_markers": _local_markers(texts),
        "observed_patterns": observed,
        "ad_translation": [
            "Conserva la segunda persona, el hook sensorial y las frases cortas del copy orgánico.",
            "Quita hashtags, direcciones y horarios: el anuncio debe invitar a escribir por WhatsApp.",
            "No copies frases literales ni emojis; replica el ritmo y el vocabulario de la marca.",
            "La calidez y cercanía del copy publicado deben notarse incluso en 125 caracteres.",
        ],
        "signature_examples": _signature_examples(posts, median_length, max_examples),
    }
