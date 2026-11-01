"""Genera reportes legibles para revisar propuestas de comentarios."""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from modules.communications.policy import check_response


CSV_FIELDS = [
    "numero",
    "comment_id",
    "autor",
    "personaje",
    "comentario",
    "respuesta_propuesta",
    "estado",
    "calidad",
    "alertas",
    "motivo_revision",
    "modelo",
    "publicado",
]


def _text(value: Any) -> str:
    return str(value or "").strip()


def _approval_item(item: Dict[str, Any], index: int) -> Dict[str, Any]:
    agent = item.get("agent") if isinstance(item.get("agent"), dict) else {}
    response = _text(item.get("approved_response") or item.get("response"))
    quality = check_response(response) if response else None
    flags = list(agent.get("policy_flags") or [])
    if quality:
        flags.extend(quality.flags)
    flags = list(dict.fromkeys(flags))
    if item.get("published") or item.get("reply_id"):
        status = "publicada"
    elif item.get("approved") is True:
        status = "aprobada"
    elif response:
        status = "pendiente de aprobación"
    else:
        status = "sin respuesta propuesta"

    return {
        "numero": index,
        "comment_id": _text(item.get("comment_id")),
        "autor": _text(item.get("author")),
        "personaje": _text(item.get("character")) or "Universe",
        "comentario": _text(item.get("comment_text") or item.get("original_comment")),
        "respuesta_propuesta": response,
        "estado": status,
        "calidad_ok": quality.ok if quality else False,
        "calidad": "OK" if quality and quality.ok else "REVISAR",
        "alertas": ", ".join(flags),
        "motivo_revision": _text(item.get("review_reason") or agent.get("reason")),
        "modelo": _text(agent.get("model")),
        "publicado": bool(item.get("published") or item.get("reply_id")),
    }


def _shadow_item(record: Dict[str, Any], index: int) -> Dict[str, Any]:
    agent = record.get("agent") if isinstance(record.get("agent"), dict) else {}
    reference = record.get("reference") if isinstance(record.get("reference"), dict) else {}
    item = {
        "comment_id": record.get("comment_id"),
        "comment_text": record.get("comment_text"),
        "character": agent.get("character"),
        "approved": reference.get("approved") is True,
        "approved_response": agent.get("draft") or agent.get("response"),
        "review_reason": agent.get("reason") if agent.get("decision") == "review" else "",
        "agent": agent,
    }
    return _approval_item(item, index)


def _item_decision(item: Dict[str, Any]) -> str:
    agent = item.get("agent") if isinstance(item.get("agent"), dict) else {}
    return _text(agent.get("decision") or item.get("decision")).casefold()


def load_review_items(
    path: Path,
    *,
    only_decision: Optional[str] = None,
) -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        source = payload
        converter = _approval_item
    elif isinstance(payload, dict) and isinstance(payload.get("approvals"), list):
        source = payload["approvals"]
        converter = _approval_item
    elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
        source = payload["records"]
        converter = _shadow_item
    else:
        raise ValueError("El archivo no contiene 'approvals' ni 'records'")

    items = []
    for item in source:
        if isinstance(item, dict):
            if only_decision and _item_decision(item) != only_decision.casefold():
                continue
            items.append(converter(item, len(items) + 1))
    return items


def _quote_block(value: str, empty: str = "(vacío)") -> str:
    text = value or empty
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def render_markdown(
    items: Iterable[Dict[str, Any]],
    *,
    source: Path,
    only_decision: Optional[str] = None,
) -> str:
    items = list(items)
    lines = [
        "# Revisión de propuestas de comentarios",
        "",
        f"- Fuente: `{source}`",
        f"- Generado: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Propuestas: {len(items)}",
    ]
    if only_decision:
        lines.append(f"- Filtro: `{only_decision}`")
    lines.extend(
        [
            "",
            "Este archivo es solo para revisión. Para publicar, edita `approved: true`",
            "en la cola de aprobaciones correspondiente y usa el publicador autorizado.",
            "",
        ]
    )
    for item in items:
        lines.extend(
            [
                f"## {item['numero']}. {item['personaje']}",
                "",
                f"- **Estado:** {item['estado']}",
                f"- **Calidad:** {item['calidad']}",
                f"- **Autor:** {item['autor'] or 'Usuario'}",
                f"- **Modelo:** {item['modelo'] or 'legacy'}",
            ]
        )
        if item["alertas"]:
            lines.append(f"- **Alertas:** {item['alertas']}")
        if item["motivo_revision"]:
            lines.append(f"- **Motivo:** {item['motivo_revision']}")
        lines.extend(
            [
                "",
                "**Comentario**",
                "",
                _quote_block(item["comentario"]),
                "",
                "**Respuesta propuesta**",
                "",
                _quote_block(item["respuesta_propuesta"], "(sin respuesta propuesta)"),
                "",
                "- [ ] Revisada",
                "- [ ] Aprobada para publicar",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _atomic_text(path: Path, content: str, *, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding=encoding,
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def write_csv(path: Path, items: Iterable[Dict[str, Any]]) -> None:
    rows = list(items)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8-sig",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in CSV_FIELDS} for row in rows)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def default_output_paths(source: Path) -> tuple[Path, Path]:
    output_dir = source.parent if source.parent.name == "reports" else source.parent / "reports"
    return output_dir / f"{source.stem}.md", output_dir / f"{source.stem}.csv"


def generate_review_files(
    source: Path,
    *,
    markdown_path: Optional[Path] = None,
    csv_path: Optional[Path] = None,
    only_decision: Optional[str] = None,
) -> Dict[str, Any]:
    source = Path(source)
    items = load_review_items(source, only_decision=only_decision)
    default_markdown, default_csv = default_output_paths(source)
    markdown_path = Path(markdown_path) if markdown_path else default_markdown
    csv_path = Path(csv_path) if csv_path else default_csv
    _atomic_text(
        markdown_path,
        render_markdown(items, source=source, only_decision=only_decision),
    )
    write_csv(csv_path, items)
    return {
        "source": str(source),
        "items": len(items),
        "markdown": str(markdown_path),
        "csv": str(csv_path),
        "pending": sum(item["estado"] == "pendiente de aprobación" for item in items),
        "quality_failed": sum(item["calidad"] != "OK" for item in items),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Genera Markdown y CSV para revisar comentarios")
    parser.add_argument("--input", type=Path, required=True, help="JSON de aprobaciones o reporte sombra")
    parser.add_argument("--markdown", type=Path, default=None)
    parser.add_argument("--csv", type=Path, default=None)
    parser.add_argument(
        "--only-suggested",
        action="store_true",
        help="incluye solo registros cuya decisión sea suggest",
    )
    args = parser.parse_args(argv)
    try:
        result = generate_review_files(
            args.input,
            markdown_path=args.markdown,
            csv_path=args.csv,
            only_decision="suggest" if args.only_suggested else None,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"❌ No se pudo generar la revisión: {type(exc).__name__}: {exc}")
        return 1
    print(f"📝 Markdown: {result['markdown']}")
    print(f"📊 CSV: {result['csv']}")
    print(f"   Propuestas: {result['items']} · Pendientes: {result['pending']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
