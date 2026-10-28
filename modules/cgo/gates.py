"""Gates reutilizables del orquestador CGO.

Un gate nunca imprime valores de credenciales: solo verifica presencia.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from modules.cgo.result import (
    GATE_FAIL,
    GATE_NOT_CONFIGURED,
    GATE_PASS,
    GATE_SKIP,
    GATE_UNKNOWN,
    CgoContext,
    GateResult,
)
from modules.cgo.tracks import UNKNOWN, capability_allowed, load_config, tenant_track

TOKEN_KEYS = (
    "META_ACCESS_TOKEN",
    "META_PAGE_TOKEN",
    "IG_ACCESS_TOKEN",
    "FB_ACCESS_TOKEN",
    "WHATSAPP_TOKEN",
    "WHATSAPP_ACCESS_TOKEN",
)


def _env_key_names(path: Path) -> set:
    """Nombres de variables con valor no vacío. Nunca devuelve valores."""
    if not path.is_file():
        return set()
    names = set()
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if value.strip():
                names.add(key.strip())
    except OSError:
        return set()
    return names


def has_token(ctx: CgoContext, tenant_id: str) -> bool:
    import os

    keys = set(os.environ) & set(TOKEN_KEYS)
    keys |= _env_key_names(ctx.base_path / ".env") & set(TOKEN_KEYS)
    keys |= _env_key_names(ctx.tenant_path(tenant_id) / ".env") & set(TOKEN_KEYS)
    return bool(keys)


def gate_track(ctx: CgoContext, capability: str, tenant_id: str) -> GateResult:
    track = tenant_track(tenant_id, ctx.base_path)
    if track == UNKNOWN:
        return GateResult(
            "track",
            GATE_UNKNOWN,
            f"tenant_type ausente o inválido en tenants/{tenant_id}/config.json",
        )
    if not capability_allowed(capability, track):
        return GateResult(
            "track",
            GATE_FAIL,
            f"{capability} no aplica al track {track}.",
        )
    return GateResult("track", GATE_PASS, f"track={track}")


def gate_config(ctx: CgoContext, tenant_id: str) -> Tuple[GateResult, Dict[str, Any]]:
    try:
        config = load_config(tenant_id, ctx.base_path)
    except FileNotFoundError:
        return GateResult("config", GATE_FAIL, "Falta config.json."), {}
    except ValueError:
        return GateResult("config", GATE_FAIL, "config.json inválido."), {}

    if not config.get("tenant_id"):
        return GateResult("config", GATE_UNKNOWN, "config.json sin tenant_id."), config
    if not config.get("client_name"):
        return GateResult("config", GATE_UNKNOWN, "config.json sin client_name."), config
    return GateResult("config", GATE_PASS, "config.json válido."), config


def gate_token(ctx: CgoContext, tenant_id: str) -> GateResult:
    if not ctx.publish:
        return GateResult("token", GATE_SKIP, "dry-run: no se necesita token.")
    if has_token(ctx, tenant_id):
        return GateResult("token", GATE_PASS, "credencial presente (valor no expuesto).")
    return GateResult("token", GATE_FAIL, "No hay token de Meta configurado.")


def gate_brand(ctx: CgoContext, tenant_id: str) -> GateResult:
    from modules.creative.brand_kit import load_brand_kit

    try:
        kit = load_brand_kit(tenant_id, str(ctx.base_path))
    except Exception as exc:
        return GateResult("brand", GATE_FAIL, f"No se pudo cargar brand kit: {type(exc).__name__}")
    if kit.get("voice") or kit.get("palette"):
        return GateResult("brand", GATE_PASS, "Identidad de marca disponible.")
    return GateResult("brand", GATE_UNKNOWN, "Brand kit sin voz ni paleta.")


def gate_cro_audit(ctx: CgoContext, tenant_id: str) -> GateResult:
    from modules.intelligence.agents.tenant_auditor import audit_tenant

    audit = audit_tenant(tenant_id, str(ctx.base_path))
    if audit["status"] == "READY":
        return GateResult("cro_audit", GATE_PASS, f"score={audit['score']}")
    if audit["status"] == "BLOCKED":
        return GateResult("cro_audit", GATE_FAIL, "Auditoría bloqueada: revisar config.")
    missing = len(audit.get("next_actions") or [])
    return GateResult(
        "cro_audit",
        GATE_UNKNOWN,
        f"score={audit['score']}, {missing} pendientes.",
    )


def canon_path(ctx: CgoContext, tenant_id: str) -> Optional[Path]:
    import os

    env_path = os.environ.get("CANON_REPO_PATH")
    candidates = []
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(ctx.tenant_path(tenant_id) / "canon")
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def gate_canon(ctx: CgoContext, tenant_id: str) -> GateResult:
    path = canon_path(ctx, tenant_id)
    if path is None:
        return GateResult(
            "canon",
            GATE_NOT_CONFIGURED,
            "Sin CANON_REPO_PATH ni tenants/<id>/canon.",
        )
    return GateResult("canon", GATE_PASS, f"canon en {path.name}")
