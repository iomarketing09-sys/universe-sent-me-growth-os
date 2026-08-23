"""Print non-trivial comments from a read-only Facebook delta for human review."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "Operations/Research/2026-08-23_Facebook_Comment_Review_Delta_05.json"
rows = json.loads(INPUT.read_text(encoding="utf-8")).get("comments", [])
word_re = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+")
for row in sorted(rows, key=lambda item: (item.get("post_id", ""), item.get("comment_created_time", ""))):
    text = (row.get("comment_message") or "").replace("\n", " ").strip()
    words = word_re.findall(text)
    if not text or len(words) <= 1:
        continue
    if row.get("category") in {"Emoji_o_símbolo", "Sin_contenido", "Respuesta_breve"}:
        continue
    print("POST", row.get("post_id"))
    print("ID", row.get("comment_id"), "TIME", row.get("comment_created_time"), "TYPE", row.get("comment_type"))
    print(text)
    print("---")
