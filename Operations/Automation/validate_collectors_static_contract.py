#!/usr/bin/env python3
"""Validate USM collector contracts by parsing public source only.

Safety boundary: this script uses ast.parse and text reads only. It never imports
collector modules, reads private configuration, opens a socket, invokes OAuth,
calls an API, writes evidence, or starts a scheduled/background process.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIREMENTS = ROOT / "official_metrics_requirements.txt"
EXAMPLE = ROOT / "official_metrics_config.example.json"


def call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def calls_in(tree: ast.AST) -> set[str]:
    return {
        name
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        if (name := call_name(node.func)) is not None
    }


def require(text: str, expected: list[str], label: str, failures: list[str]) -> None:
    missing = [value for value in expected if value not in text]
    if missing:
        failures.append(f"{label}: missing {', '.join(missing)}")


def review_meta(name: str, source: Path, failures: list[str]) -> None:
    text = source.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(source))
    calls = calls_in(tree)
    require(text, ["Universe Sent Me", "USM_META_USER_ACCESS_TOKEN", "~/.local/share/usm-metrics/evidence"], name, failures)
    if "requests.get" not in calls:
        failures.append(f"{name}: requests.get is absent")
    forbidden = sorted(call for call in calls if call in {"requests.post", "requests.put", "requests.patch", "requests.delete"})
    if forbidden:
        failures.append(f"{name}: forbidden write request call(s): {', '.join(forbidden)}")


def main() -> int:
    failures: list[str] = []
    tiktok = ROOT / "fetch_tiktok_official_metrics.py"
    youtube = ROOT / "fetch_youtube_official_metrics.py"
    facebook = ROOT / "fetch_facebook_official_metrics.py"
    instagram = ROOT / "fetch_instagram_official_metrics.py"
    meta_probe = ROOT / "validate_meta_local_readonly.py"
    for source in (tiktok, youtube, facebook, instagram, meta_probe, REQUIREMENTS, EXAMPLE):
        if not source.is_file():
            failures.append(f"required public artifact is absent: {source.name}")
    if failures:
        print(json.dumps({"status": "static_contract_blocked", "failures": failures}, ensure_ascii=False))
        return 1

    tiktok_text = tiktok.read_text(encoding="utf-8")
    tiktok_calls = calls_in(ast.parse(tiktok_text, filename=str(tiktok)))
    require(
        tiktok_text,
        ["Universe Sent Me", "USM_TIKTOK_CLIENT_KEY", "USM_TIKTOK_CLIENT_SECRET", "user.info.basic", "video.list", "~/.local/share/usm-metrics/evidence"],
        "TikTok collector",
        failures,
    )
    if "requests.post" not in tiktok_calls:
        failures.append("TikTok collector: expected POST-only OAuth/Display contract is absent")

    youtube_text = youtube.read_text(encoding="utf-8")
    require(
        youtube_text,
        [
            "Universe Sent Me",
            "youtube.readonly",
            "yt-analytics.readonly",
            "yt-analytics-monetary.readonly",
            "monetization_status",
            "not_available",
            "~/.local/share/usm-metrics/evidence",
        ],
        "YouTube collector",
        failures,
    )

    review_meta("Facebook collector", facebook, failures)
    review_meta("Instagram collector", instagram, failures)

    probe_text = meta_probe.read_text(encoding="utf-8")
    probe_calls = calls_in(ast.parse(probe_text, filename=str(meta_probe)))
    require(probe_text, ["Universe Sent Me", "USM_META_USER_ACCESS_TOKEN", "GET-only connection and authorization validation"], "Meta validation probe", failures)
    if "requests.get" not in probe_calls:
        failures.append("Meta validation probe: requests.get is absent")
    if any(call in probe_calls for call in {"requests.post", "requests.put", "requests.patch", "requests.delete"}):
        failures.append("Meta validation probe: contains a forbidden write request call")

    requirements = REQUIREMENTS.read_text(encoding="utf-8")
    require(
        requirements,
        ["requests>=2.31,<3", "google-api-python-client>=2.140,<3", "google-auth-oauthlib>=1.2,<2", "google-auth-httplib2>=0.2,<1"],
        "requirements",
        failures,
    )
    example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    if example.get("brand") != "Universe Sent Me":
        failures.append("example configuration: brand differs from Universe Sent Me")
    if set(example) - {"brand", "timezone", "evidence_dir", "tiktok", "youtube"}:
        failures.append("example configuration: unexpected top-level key")

    result = {
        "status": "static_contract_passed" if not failures else "static_contract_blocked",
        "reviewed_collectors": ["TikTok", "YouTube", "Facebook", "Instagram"],
        "checked_artifacts": [source.name for source in (tiktok, youtube, facebook, instagram, meta_probe, REQUIREMENTS, EXAMPLE)],
        "guarantees": [
            "ast_parse_only_no_collector_import",
            "no_private_config_or_token_read",
            "no_network_or_oauth",
            "no_evidence_or_canonical_write",
            "no_scheduler_or_service_start",
        ],
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
