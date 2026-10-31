#!/usr/bin/env python3
"""Descarga ingresos diarios de contenido de Meta para Universe.

Usa el token de usuario del entorno para obtener un Page Access Token y
consulta ``content_monetization_earnings`` y
``monetization_approximate_earnings`` día por día. Guarda solo valores y
metadatos, nunca el token ni las URLs de paginación.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
TENANT_DIR = SCRIPT_DIR.parent
REPO_ROOT = SCRIPT_DIR.parents[2]
GRAPH_URL = "https://graph.facebook.com/v23.0"
MICRO_PER_USD = 100_000_000


def _load_env(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("'\"")
    return values


def _credentials() -> tuple[str, str]:
    values: Dict[str, str] = {}
    for path in (TENANT_DIR / ".env", REPO_ROOT / ".env"):
        values.update(_load_env(path))
    token = os.environ.get("META_ACCESS_TOKEN") or values.get("META_ACCESS_TOKEN", "")
    page_id = os.environ.get("FB_PAGE_ID") or values.get("FB_PAGE_ID", "1036844829507460")
    if not token:
        raise RuntimeError("Falta META_ACCESS_TOKEN en el entorno o en .env")
    return token, page_id


def _get(path: str, params: Dict[str, str]) -> Dict[str, Any]:
    url = f"{GRAPH_URL}/{path}?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8"))
        except Exception:
            body = {}
        error = body.get("error") or {}
        message = error.get("message") or "Error HTTP de Meta"
        raise RuntimeError(f"Meta Graph {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"No se pudo conectar a Meta Graph: {exc.reason}") from exc


def _page_token(user_token: str, page_id: str) -> str:
    payload = _get("me/accounts", {
        "fields": "id,name,access_token",
        "access_token": user_token,
    })
    for page in payload.get("data", []):
        if str(page.get("id")) == page_id and page.get("access_token"):
            return str(page["access_token"])
    raise RuntimeError(f"El token no tiene acceso a la página {page_id}")


def _daily_blocks(payload: Dict[str, Any]) -> Dict[str, Any]:
    blocks: Dict[str, Any] = {}
    for block in payload.get("data", []):
        if block.get("period") == "day" and block.get("name") in (
            "content_monetization_earnings",
            "monetization_approximate_earnings",
        ):
            blocks[str(block["name"])] = block
    return blocks


def _day_value(block: Optional[Dict[str, Any]]) -> Any:
    values = (block or {}).get("values") or []
    return values[0].get("value") if values else None


def _daterange(start: date, end: date) -> Iterable[date]:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def fetch_earnings(since: date, until: date) -> Dict[str, Any]:
    user_token, page_id = _credentials()
    token = _page_token(user_token, page_id)
    rows: List[Dict[str, Any]] = []
    total_content = 0.0
    total_approximate = 0.0

    for day in _daterange(since, until):
        payload = _get(f"{page_id}/insights", {
            "metric": "content_monetization_earnings,monetization_approximate_earnings",
            "since": day.isoformat(),
            "until": day.isoformat(),
            "access_token": token,
        })
        blocks = _daily_blocks(payload)
        content_value = _day_value(blocks.get("content_monetization_earnings"))
        approximate_value = _day_value(blocks.get("monetization_approximate_earnings"))
        content_raw = content_value.get("microAmount") if isinstance(content_value, dict) else None
        content_usd = round(float(content_raw or 0) / MICRO_PER_USD, 2)
        approximate_usd = round(float(approximate_value or 0), 2)
        currency = str(
            (content_value or {}).get("currency")
            if isinstance(content_value, dict)
            else "USD"
        )
        rows.append({
            "date": day.isoformat(),
            "content_monetization_micro_amount": content_raw,
            "content_monetization_usd": content_usd,
            "approximate_earnings_usd": approximate_usd,
            "currency": currency,
        })
        total_content += content_usd
        total_approximate += approximate_usd

    config_path = TENANT_DIR / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.is_file() else {}
    return {
        "tenant_id": config.get("tenant_id", "universe"),
        "page_id": page_id,
        "business_id": (config.get("meta") or {}).get("business_id", ""),
        "metric": "content_monetization_earnings",
        "source": "meta_graph_api",
        "mode": "read_only",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "period_start": since.isoformat(),
        "period_end": until.isoformat(),
        "currency": "USD",
        "days": rows,
        "total_content_monetization_usd": round(total_content, 2),
        "total_approximate_earnings_usd": round(total_approximate, 2),
        "note": (
            "content_monetization_earnings se normaliza desde microAmount; "
            "monetization_approximate_earnings se conserva en USD. "
            "No incluye necesariamente bonus u otros ajustes de la app."
        ),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Descargar ingresos diarios de Meta")
    today = date.today()
    parser.add_argument("--since", default=today.replace(day=1).isoformat())
    parser.add_argument("--until", default=today.isoformat())
    parser.add_argument("--output", default="")
    args = parser.parse_args(argv)

    since = date.fromisoformat(args.since)
    until = date.fromisoformat(args.until)
    if since > until:
        raise SystemExit("since no puede ser mayor que until")

    payload = fetch_earnings(since, until)
    output = Path(args.output) if args.output else (
        SCRIPT_DIR / "monetization" / f"{until.isoformat()}_Meta_Content_Earnings.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "period_start": payload["period_start"],
        "period_end": payload["period_end"],
        "days": len(payload["days"]),
        "total_content_monetization_usd": payload["total_content_monetization_usd"],
        "total_approximate_earnings_usd": payload["total_approximate_earnings_usd"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
