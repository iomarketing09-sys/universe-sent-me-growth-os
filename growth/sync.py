"""Sincronización segura y reutilizable de evidencia por tenant.

La primera versión trabaja únicamente con configuración y evidencia local ya
guardada. No carga secretos, no llama APIs externas, no publica contenido y no
envía mensajes.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from growth.tenant_registry import TenantRegistry, get_registry


SYNC_SCHEMA_VERSION = "1.0"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
REDACTED_VALUE = "[REDACTED]"
SENSITIVE_KEY_PATTERN = re.compile(
    r"(?:access_)?token|secret|password|authorization|cookie|api[_-]?key",
    re.IGNORECASE,
)
SENSITIVE_QUERY_PATTERN = re.compile(
    r"([?&](?:access_)?token|[?&](?:client_)?secret|[?&]api[_-]?key|[?&]authorization)=([^&#\s]+)",
    re.IGNORECASE,
)
BEARER_TOKEN_PATTERN = re.compile(r"(Bearer\s+)[^\s\"']+", re.IGNORECASE)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _read_json(path: Path) -> Optional[Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _latest(paths: Iterable[Path]) -> Optional[Path]:
    candidates = [path for path in paths if path.is_file()]
    return max(candidates, key=lambda path: path.stat().st_mtime) if candidates else None


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def redact_sensitive_data(value: Any) -> Any:
    """Devuelve una copia apta para snapshots, logs y salida de CLI.

    Los resultados de Graph pueden incluir URLs de paginación que arrastran el
    token de acceso. El token nunca debe persistir dentro de evidencia de un
    tenant ni imprimirse en la salida de sincronización.
    """
    if isinstance(value, dict):
        return {
            key: REDACTED_VALUE
            if SENSITIVE_KEY_PATTERN.search(str(key))
            else redact_sensitive_data(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_sensitive_data(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_sensitive_data(item) for item in value)
    if isinstance(value, str):
        redacted = SENSITIVE_QUERY_PATTERN.sub(r"\1=" + REDACTED_VALUE, value)
        return BEARER_TOKEN_PATTERN.sub(r"\1" + REDACTED_VALUE, redacted)
    return value


def _csv_summary(path: Path) -> Dict[str, Any]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as exc:
        return {"status": "error", "note": str(exc), "evidence": _relative(path)}

    latest_row = rows[-1] if rows else {}
    return {
        "status": "local_evidence",
        "evidence": _relative(path),
        "rows": len(rows),
        "period_start": latest_row.get("period_start"),
        "period_end": latest_row.get("period_end"),
    }


def _json_metrics_summary(path: Optional[Path]) -> Dict[str, Any]:
    if path is None:
        return {"status": "no_local_evidence"}

    data = _read_json(path)
    if not isinstance(data, dict):
        return {"status": "invalid_local_evidence", "evidence": _relative(path)}

    return {
        "status": "local_evidence",
        "evidence": _relative(path),
        "period_start": data.get("period_start"),
        "period_end": data.get("period_end"),
        "clicks": data.get("total_clicks"),
        "impressions": data.get("total_impressions"),
    }


def collect_meta(tenant_path: Path, config: Dict[str, Any], live_meta: bool = False) -> Dict[str, Any]:
    meta = config.get("meta") or {}
    if not meta.get("page_id"):
        return {"status": "not_configured", "mode": "local_evidence"}

    snapshot = _latest((tenant_path / "data").glob("meta_metrics_*.csv"))
    result = {
        "status": "configured_no_local_evidence",
        "mode": "live_meta" if live_meta else "local_evidence",
        "page_configured": True,
        "instagram_configured": bool(meta.get("ig_user_id")),
    }
    # Si live_meta está activado, intentar capturar en vivo
    if live_meta:
        try:
            from growth.integrations.meta_graph import capture_organic
            live_result = capture_organic(config)
            if live_result.get("status") == "success":
                result["live_data"] = live_result
                result["status"] = "live_success"
            elif live_result.get("status") == "not_configured":
                result["status"] = "not_configured"
                result["note"] = live_result.get("note")
            else:
                result["status"] = "live_error"
                result["note"] = live_result.get("note")
        except Exception as e:
            result["status"] = "live_error"
            result["note"] = f"Excepción en capture_organic: {e}"
    elif snapshot:
        result["metrics"] = _csv_summary(snapshot)
        result["status"] = "local_evidence"
    return result



def collect_google(tenant_path: Path, config: Dict[str, Any], live_google: bool = False) -> Dict[str, Any]:
    google = config.get("google_business") or {}
    search_console = config.get("search_console") or {}
    bing_config = config.get("bing_webmaster") or {}
    
    # Verificar configuración
    has_place_id = bool(google.get("place_id"))
    has_site_url = bool(search_console.get("site_url") or google.get("website"))
    
    if not has_place_id and not has_site_url:
        return {"status": "not_configured", "mode": "local_evidence"}

    data_dir = tenant_path / "data"
    gsc = _latest(data_dir.glob("gsc_metrics_*.json"))
    bing = _latest(data_dir.glob("bing_metrics_*.json"))
    gbp = _latest(data_dir.glob("gbp_insights_*.json"))
    
    services = {
        "google_business": {"status": "configured_no_local_evidence"},
        "search_console": _json_metrics_summary(gsc),
        "bing": _json_metrics_summary(bing),
    }
    
    has_evidence = any(service["status"] == "local_evidence" for service in services.values())
    
    # Si live_google está activado, intentar capturar en vivo
    if live_google:
        try:
            from growth.integrations.google_webmaster import capture_google_webmaster, capture_google_business
            
            # GSC + Bing
            webmaster_result = capture_google_webmaster(config)
            if webmaster_result.get("status") == "success":
                services["search_console"] = webmaster_result.get("search_console", {})
                services["bing"] = webmaster_result.get("bing_webmaster", {})
                has_evidence = True
            
            # Google Business Profile
            gbp_result = capture_google_business(config)
            services["google_business"] = gbp_result
            
            if has_evidence:
                return {
                    "status": "live_success",
                    "mode": "live_google",
                    "services": services,
                    "summary": webmaster_result.get("summary", {})
                }
        except Exception as e:
            return {
                "status": "live_error",
                "mode": "live_google",
                "error": str(e),
                "services": services,
            }
    
    return {
        "status": "local_evidence" if has_evidence else "configured_no_local_evidence",
        "mode": "local_evidence",
        "services": services,
    }


def collect_ads(tenant_path: Path, config: Dict[str, Any], live_ads: bool = False) -> Dict[str, Any]:
    campaigns_dir = tenant_path / "ads" / "campanas"
    campaigns = []
    for state_path in sorted(campaigns_dir.glob("*/00_estado.md")):
        text = state_path.read_text(encoding="utf-8")
        match = re.search(r"^\| Estado \|\s*(.*?)\s*\|$", text, re.MULTILINE)
        campaigns.append(
            {
                "campaign": state_path.parent.name,
                "state": match.group(1) if match else "not_recorded",
                "evidence": _relative(state_path),
            }
        )

    ads = config.get("ads") or {}
    account_configured = bool(ads.get("ad_account_id"))
    
    # Branch live_ads: capturar métricas en vivo desde Marketing API
    if live_ads:
        try:
            from growth.integrations.ads_adapters import capture_ads_insights
            live_result = capture_ads_insights(config)
            if live_result.get("status") == "success":
                return {
                    "status": "live_success",
                    "mode": "live_ads",
                    "ad_account_configured": account_configured,
                    "campaigns": live_result["campaigns"],
                    "summary": live_result["summary"],
                    "local_campaigns": campaigns,
                }
            elif live_result.get("status") == "not_configured":
                return {
                    "status": "not_configured",
                    "mode": "live_ads",
                    "ad_account_configured": account_configured,
                    "note": live_result.get("note"),
                    "local_campaigns": campaigns,
                }
            else:
                return {
                    "status": "live_error",
                    "mode": "live_ads",
                    "ad_account_configured": account_configured,
                    "note": live_result.get("note"),
                    "local_campaigns": campaigns,
                }
        except Exception as e:
            return {
                "status": "live_error",
                "mode": "live_ads",
                "ad_account_configured": account_configured,
                "error": str(e),
                "local_campaigns": campaigns,
            }
    
    return {
        "status": "local_evidence" if campaigns else "not_configured",
        "mode": "local_evidence",
        "ad_account_configured": account_configured,
        "live_metrics_available": False,
        "campaigns": campaigns,
    }


def collect_whatsapp(tenant_path: Path, live_whatsapp: bool = False) -> Dict[str, Any]:
    worker = tenant_path / "whatsapp" / "webhook-worker" / "wrangler.toml"
    crm_path = tenant_path / "crm" / "contacts.json"
    contacts = _read_json(crm_path)
    contact_count = len(contacts) if isinstance(contacts, dict) else 0
    test_records = 0
    if isinstance(contacts, dict):
        test_records = sum(
            1
            for key in contacts
            if any(marker in key.lower() for marker in ("test", "debug", "fresh", "trace"))
        )

    if not worker.exists() and not crm_path.exists():
        return {"status": "not_configured", "mode": "local_evidence"}

    # Branch live_whatsapp: capturar datos remotos del worker si está activado
    if live_whatsapp:
        try:
            from growth.integrations.whatsapp_adapters import collect_whatsapp_live
            live_result = collect_whatsapp_live(tenant_path)
            return {
                "status": live_result["outcome"],
                "mode": "live_whatsapp",
                "live_worker_configured": live_result["worker_config"]["worker_deployed"],
                "live_message_echoes": live_result["message_echoes"],
                "live_remote_contacts": live_result["remote_contacts"],
                "contacts": {"total": contact_count, "test_records": test_records},
            }
        except Exception as e:
            return {
                "status": "live_error",
                "mode": "live_whatsapp",
                "error": str(e),
                "contacts": {"total": contact_count, "test_records": test_records},
            }

    return {
        "status": "configured_observation" if worker.exists() else "local_evidence",
        "mode": "local_evidence",
        "listen_only_worker_configured": bool(worker.exists()),
    }
def collect_directories(config: Dict[str, Any]) -> Dict[str, Any]:
    sources = config.get("external_sources") or {}
    if not sources:
        return {"status": "not_configured", "mode": "local_evidence"}
    return {
        "status": "configured_no_local_evidence",
        "mode": "local_evidence",
        "configured_sources": sorted(sources),
    }


def sync_tenant(tenant_id: str, registry: Optional[TenantRegistry] = None, args: Optional[argparse.Namespace] = None) -> Dict[str, Any]:
    """Construye un snapshot de evidencia local para un tenant existente."""
    registry = registry or get_registry()
    tenant_path = registry.tenants_dir / tenant_id
    config_path = tenant_path / "config.json"
    if not config_path.is_file():
        raise FileNotFoundError(f"No existe config.json para el tenant: {tenant_id}")

    config = registry.load_config(tenant_id)
    sources = {
        "meta": collect_meta(tenant_path, config, live_meta=args.live_meta if args else False),
        "google": collect_google(tenant_path, config, live_google=args.live_google if args else False),
        "ads": collect_ads(tenant_path, config, live_ads=args.live_ads if args else False),
        "whatsapp": collect_whatsapp(tenant_path, live_whatsapp=args.live_whatsapp if args else False),
        "directories": collect_directories(config),
    }
    status_counts: Dict[str, int] = {}
    for source in sources.values():
        status = source["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    snapshot = {
        "schema_version": SYNC_SCHEMA_VERSION,
        "tenant_id": tenant_id,
        "generated_at": _utc_now().isoformat(),
        "mode": "local_evidence",
        "external_requests": 0,
        "external_writes": 0,
        "sources": sources,
        "summary": status_counts,
    }
    return redact_sensitive_data(snapshot)


def write_snapshot(snapshot: Dict[str, Any], tenant_path: Path) -> Dict[str, Path]:
    """Guarda un histórico, latest.json y un log mínimo del sync."""
    sync_dir = tenant_path / "data" / "sync"
    sync_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.fromisoformat(snapshot["generated_at"]).strftime("%Y%m%dT%H%M%SZ")
    historical_path = sync_dir / f"{timestamp}.json"
    latest_path = sync_dir / "latest.json"
    log_path = sync_dir / "sync_log.jsonl"
    safe_snapshot = redact_sensitive_data(snapshot)
    payload = json.dumps(safe_snapshot, ensure_ascii=False, indent=2) + "\n"

    historical_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "generated_at": safe_snapshot["generated_at"],
                    "tenant_id": safe_snapshot["tenant_id"],
                    "mode": safe_snapshot["mode"],
                    "summary": safe_snapshot["summary"],
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    return {"historical": historical_path, "latest": latest_path, "log": log_path}


def sanitize_saved_snapshots(tenant_path: Path) -> int:
    """Elimina secretos de snapshots históricos ya generados para un tenant."""
    sync_dir = tenant_path / "data" / "sync"
    updated = 0
    for path in sync_dir.glob("*.json"):
        data = _read_json(path)
        if data is None:
            continue
        safe_data = redact_sensitive_data(data)
        if safe_data == data:
            continue
        path.write_text(json.dumps(safe_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        updated += 1
    return updated


def list_tenants(registry: Optional[TenantRegistry] = None) -> list[Dict[str, Any]]:
    registry = registry or get_registry()
    tenants = []
    for tenant_id in registry.list_tenants():
        config = registry.load_config(tenant_id)
        tenants.append(
            {
                "tenant_id": tenant_id,
                "type": config.get("tenant_type", "unknown"),
                "business_name": config.get("business_name") or config.get("client_name") or config.get("brand_name") or tenant_id,
                "meta_configured": bool((config.get("meta") or {}).get("page_id")),
                "google_configured": bool((config.get("google_business") or {}).get("place_id")),
            }
        )
    return tenants
