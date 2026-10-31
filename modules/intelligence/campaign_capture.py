"""Captura automática de cortes de métricas para campañas de Meta Ads.

La campaña se considera programada cuando existe ``meta_ids.json`` con
``campaign.start_time``. Los cortes son E24, E48, E72, diarios posteriores y un
corte final dos horas después del cierre. El proceso es idempotente: el estado
local evita repetir un corte ya guardado.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from modules.intelligence.ads_ledger import ad_insight_row, record_ad_insights
from modules.intelligence.ads_reporting import DEFAULT_MAX_CPA, build_report, render_markdown
from modules.intelligence.campaign_optimizer import (
    build_change_plan,
    load_policy,
    plan_paths,
    render_plan_markdown,
)


CHECKPOINT_HOURS = (24, 48, 72)
DAILY_INTERVAL_HOURS = 24
FINAL_GRACE_HOURS = 2
STATE_SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class Campaign:
    tenant_id: str
    slug: str
    campaign_id: str
    name: str
    start_at: datetime
    stop_at: Optional[datetime]
    timezone_name: str


@dataclass(frozen=True)
class Checkpoint:
    label: str
    due_at: datetime


def project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[2]


def _parse_time(value: object, *, local_tz=None) -> Optional[datetime]:
    if value in (None, ""):
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=local_tz or datetime.now().astimezone().tzinfo)
    return parsed


def _aware_now(now: Optional[datetime] = None) -> datetime:
    current = now or datetime.now().astimezone()
    if current.tzinfo is None:
        current = current.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return current


def _hours_between(start: datetime, end: datetime) -> float:
    """Diferencia real en horas, inmune a cambios de horario de verano."""
    return (
        end.astimezone(timezone.utc) - start.astimezone(timezone.utc)
    ).total_seconds() / 3600


def _tenant_ids(base_path: Path) -> List[str]:
    tenants_dir = base_path / "tenants"
    if not tenants_dir.is_dir():
        return []
    return sorted(
        path.name
        for path in tenants_dir.iterdir()
        if path.is_dir() and (path / "config.json").is_file()
    )


def _tenant_timezone(tenant_dir: Path) -> tuple[ZoneInfo, str]:
    try:
        config = json.loads((tenant_dir / "config.json").read_text(encoding="utf-8"))
        name = str(config.get("timezone") or "UTC")
        return ZoneInfo(name), name
    except (OSError, ValueError, ZoneInfoNotFoundError):
        return ZoneInfo("UTC"), "UTC"


def discover_campaigns(
    base_path: Optional[Path] = None,
    tenant_ids: Optional[Iterable[str]] = None,
) -> List[Campaign]:
    """Descubre campañas con IDs publicados y fecha exacta de inicio."""
    root = Path(base_path) if base_path else project_root()
    selected = list(tenant_ids) if tenant_ids else _tenant_ids(root)
    campaigns: List[Campaign] = []
    for tenant_id in selected:
        tenant_tz, timezone_name = _tenant_timezone(root / "tenants" / tenant_id)
        campaigns_dir = root / "tenants" / tenant_id / "ads" / "campanas"
        for path in sorted(campaigns_dir.glob("*/meta_ids.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(payload, dict):
                continue
            campaign = payload.get("campaign") or {}
            if not isinstance(campaign, dict):
                continue
            campaign_id = str(campaign.get("id") or "")
            start_at = _parse_time(campaign.get("start_time"))
            if not campaign_id or start_at is None:
                continue
            start_at = start_at.astimezone(tenant_tz)
            stop_at = _parse_time(campaign.get("stop_time"))
            if stop_at is not None:
                stop_at = stop_at.astimezone(tenant_tz)
            campaigns.append(
                Campaign(
                    tenant_id=tenant_id,
                    slug=path.parent.name,
                    campaign_id=campaign_id,
                    name=str(campaign.get("name") or path.parent.name),
                    start_at=start_at,
                    stop_at=stop_at,
                    timezone_name=timezone_name,
                )
            )
    return sorted(campaigns, key=lambda item: (item.start_at, item.tenant_id, item.slug))


def checkpoint_schedule(campaign: Campaign) -> List[Checkpoint]:
    """Cortes E24/E48/E72, diarios hasta el cierre y FINAL tras cerrar."""
    tenant_tz = ZoneInfo(campaign.timezone_name)

    def due_after(hours: int) -> datetime:
        # Los cortes son horas transcurridas reales; el cambio de horario no
        # debe correr el checkpoint una hora.
        return (campaign.start_at.astimezone(timezone.utc) + timedelta(hours=hours)).astimezone(
            tenant_tz
        )

    points: List[Checkpoint] = []
    for hours in CHECKPOINT_HOURS:
        due = due_after(hours)
        if campaign.stop_at is None or due <= campaign.stop_at:
            points.append(Checkpoint(f"E{hours}", due))

    if campaign.stop_at is not None:
        hours = CHECKPOINT_HOURS[-1] + DAILY_INTERVAL_HOURS
        while True:
            due = due_after(hours)
            if due > campaign.stop_at:
                break
            points.append(Checkpoint(f"E{hours}", due))
            hours += DAILY_INTERVAL_HOURS
        points.append(
            Checkpoint(
                "FINAL",
                (
                    campaign.stop_at.astimezone(timezone.utc)
                    + timedelta(hours=FINAL_GRACE_HOURS)
                ).astimezone(tenant_tz),
            )
        )
    return points


def state_path(tenant_id: str, base_path: Optional[Path] = None) -> Path:
    root = Path(base_path) if base_path else project_root()
    return root / "tenants" / tenant_id / "ads" / "insights" / "capture_state.json"


def report_dir(tenant_id: str, slug: str, base_path: Optional[Path] = None) -> Path:
    root = Path(base_path) if base_path else project_root()
    return root / "tenants" / tenant_id / "ads" / "insights" / "captures" / slug


def _read_state(path: Path) -> Dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"schema_version": STATE_SCHEMA_VERSION, "campaigns": {}}
    if not isinstance(payload, dict):
        return {"schema_version": STATE_SCHEMA_VERSION, "campaigns": {}}
    payload.setdefault("schema_version", STATE_SCHEMA_VERSION)
    payload.setdefault("campaigns", {})
    return payload


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _write_json(path: Path, payload: Dict) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _campaign_dir(campaign: Campaign, root: Path) -> Path:
    return root / "tenants" / campaign.tenant_id / "ads" / "campanas" / campaign.slug


def reconcile_campaign_metadata(
    campaign: Campaign,
    base_path: Optional[Path] = None,
    *,
    ads: Optional[List[Dict]] = None,
    now: Optional[datetime] = None,
) -> Dict:
    """Alinea ``campaign.json.published`` con los IDs observados en Meta.

    Solo corrige metadata local. No envía cambios a Meta. Si la evidencia es
    ambigua (varios ad sets para la misma campaña), bloquea la ejecución en vez
    de adivinar.
    """
    root = Path(base_path) if base_path else project_root()
    current = _aware_now(now)
    campaign_dir = _campaign_dir(campaign, root)
    meta_path = campaign_dir / "meta_ids.json"
    spec_path = campaign_dir / "campaign.json"

    result = {
        "status": "checked",
        "source": None,
        "checked_at": current.isoformat(),
        "changes": [],
        "execution_blocked": False,
        "execution_blockers": [],
        "campaign_json_artifact": None,
    }

    observed_adset_ids = sorted(
        {
            str(ad.get("adset_id"))
            for ad in (ads or [])
            if str(ad.get("campaign_id")) == campaign.campaign_id and ad.get("adset_id")
        }
    )
    if len(observed_adset_ids) > 1:
        result.update(
            {
                "status": "blocked",
                "source": "meta_api_ads",
                "execution_blocked": True,
                "execution_blockers": [
                    "La campaña reporta varios ad sets: " + ", ".join(observed_adset_ids)
                ],
            }
        )
        return result

    try:
        meta_payload = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        result.update(
            {
                "status": "blocked",
                "execution_blocked": True,
                "execution_blockers": [f"No se pudo leer meta_ids.json: {exc}"],
            }
        )
        return result
    if not isinstance(meta_payload, dict):
        result.update(
            {
                "status": "blocked",
                "execution_blocked": True,
                "execution_blockers": ["meta_ids.json no contiene un objeto"],
            }
        )
        return result

    meta_campaign_id = str(((meta_payload.get("campaign") or {}).get("id")) or "")
    meta_adset_id = str(((meta_payload.get("adset") or {}).get("id")) or "")
    canonical_campaign_id = meta_campaign_id or campaign.campaign_id
    canonical_adset_id = observed_adset_ids[0] if observed_adset_ids else meta_adset_id
    result["source"] = "meta_api_ads" if observed_adset_ids else "meta_ids.json"
    result["meta_captured_at"] = meta_payload.get("captured_at")
    result["canonical"] = {
        "campaign_id": canonical_campaign_id,
        "adset_id": canonical_adset_id,
    }

    if not canonical_adset_id:
        result.update(
            {
                "status": "blocked",
                "execution_blocked": True,
                "execution_blockers": ["No hay un ad set canónico confirmado"],
            }
        )
        return result

    if not spec_path.is_file():
        result["status"] = "no_local_spec"
        return result
    try:
        spec_payload = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        result.update(
            {
                "status": "blocked",
                "execution_blocked": True,
                "execution_blockers": [f"No se pudo leer campaign.json: {exc}"],
            }
        )
        return result
    if not isinstance(spec_payload, dict):
        result.update(
            {
                "status": "blocked",
                "execution_blocked": True,
                "execution_blockers": ["campaign.json no contiene un objeto"],
            }
        )
        return result

    published = spec_payload.setdefault("published", {})
    if not isinstance(published, dict):
        result.update(
            {
                "status": "blocked",
                "execution_blocked": True,
                "execution_blockers": ["campaign.json.published no es un objeto"],
            }
        )
        return result

    expected = {
        "campaign_id": canonical_campaign_id,
        "adset_id": canonical_adset_id,
    }
    changes = []
    for field, correct_value in expected.items():
        previous = published.get(field)
        if str(previous or "") != correct_value:
            changes.append(
                {"field": f"published.{field}", "previous": previous, "current": correct_value}
            )
            published[field] = correct_value

    if not changes:
        result["status"] = "ok"
        return result

    reconciliation = {
        "status": "reconciled",
        "source": result["source"],
        "reconciled_at": current.isoformat(),
        "meta_captured_at": result.get("meta_captured_at"),
        "changes": changes,
    }
    spec_payload["metadata_reconciliation"] = reconciliation
    try:
        _write_json(spec_path, spec_payload)
    except OSError as exc:
        result.update(
            {
                "status": "blocked",
                "execution_blocked": True,
                "execution_blockers": [f"No se pudo actualizar campaign.json: {exc}"],
            }
        )
        return result

    result.update(
        {
            "status": "reconciled",
            "changes": changes,
            "campaign_json_artifact": str(spec_path.relative_to(root)),
        }
    )
    return result


def _is_done(entry: Optional[Dict]) -> bool:
    return bool(entry and entry.get("status") in ("captured", "missed"))


def due_checkpoint(
    campaign: Campaign,
    state: Dict,
    now: datetime,
) -> tuple[Optional[Checkpoint], List[Checkpoint]]:
    """Devuelve el corte más reciente pendiente y los que quedaron atrás."""
    campaign_state = (state.get("campaigns") or {}).get(campaign.slug) or {}
    if campaign_state.get("campaign_id") not in (None, campaign.campaign_id):
        campaign_state = {}
    recorded = campaign_state.get("checkpoints") or {}
    pending = [
        point
        for point in checkpoint_schedule(campaign)
        if point.due_at <= now and not _is_done(recorded.get(point.label))
    ]
    if not pending:
        return None, []
    return pending[-1], pending[:-1]


def next_checkpoint(campaign: Campaign, state: Dict, now: datetime) -> Optional[Checkpoint]:
    campaign_state = (state.get("campaigns") or {}).get(campaign.slug) or {}
    if campaign_state.get("campaign_id") not in (None, campaign.campaign_id):
        campaign_state = {}
    recorded = campaign_state.get("checkpoints") or {}
    future = [
        point
        for point in checkpoint_schedule(campaign)
        if point.due_at > now and not _is_done(recorded.get(point.label))
    ]
    return future[0] if future else None


def _capture_payload(
    campaign: Campaign,
    checkpoint: Checkpoint,
    report: Dict,
    now: datetime,
) -> Dict:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "tenant_id": campaign.tenant_id,
        "campaign_slug": campaign.slug,
        "campaign_id": campaign.campaign_id,
        "campaign_name": campaign.name,
        "checkpoint": checkpoint.label,
        "scheduled_for": checkpoint.due_at.isoformat(),
        "captured_at": now.isoformat(),
        "elapsed_hours": round(_hours_between(campaign.start_at, now), 2),
        "scheduled_elapsed_hours": _scheduled_elapsed_hours(campaign, checkpoint),
        "late_minutes": max(0, int(_hours_between(checkpoint.due_at, now) * 60)),
        "ads": report["ads"],
        "total_spend": report["total_spend"],
        "total_conversations": report["total_conversations"],
        "blended_cost_per_conversation": report["blended_cost_per_conversation"],
        "max_cpa": report["max_cpa"],
        "alerts": report["alerts"],
    }


def _scheduled_elapsed_hours(campaign: Campaign, checkpoint: Checkpoint) -> float:
    """Antigüedad que representa el corte, no la hora real de ejecución."""
    return round(_hours_between(campaign.start_at, checkpoint.due_at), 2)


def _write_change_plan(
    *,
    campaign: Campaign,
    checkpoint: Checkpoint,
    report: Dict,
    capture_payload: Dict,
    metadata_reconciliation: Dict,
    current: datetime,
    root: Path,
) -> List[Path]:
    """Persiste un plan recomendado; no contiene ni ejecuta escrituras en Meta."""
    plan = build_change_plan(
        report,
        tenant_id=campaign.tenant_id,
        campaign_id=campaign.campaign_id,
        campaign_slug=campaign.slug,
        campaign_name=campaign.name,
        elapsed_hours=_scheduled_elapsed_hours(campaign, checkpoint),
        capture_elapsed_hours=capture_payload["elapsed_hours"],
        scheduled_for=checkpoint.due_at.isoformat(),
        generated_at=current,
        checkpoint=checkpoint.label,
        policy=load_policy(root / "tenants" / campaign.tenant_id),
        metadata_reconciliation=metadata_reconciliation,
    )
    json_path, md_path = plan_paths(
        campaign.tenant_id,
        campaign.slug,
        checkpoint.label,
        root,
    )
    _write_json(json_path, plan)
    _write_text(md_path, render_plan_markdown(plan))
    return [json_path, md_path]


def run_due_captures(
    *,
    tenant_ids: Optional[Sequence[str]] = None,
    base_path: Optional[Path] = None,
    now: Optional[datetime] = None,
    dry_run: bool = False,
    max_cpa: float = DEFAULT_MAX_CPA,
    fetcher: Optional[Callable[[Dict], Dict]] = None,
) -> Dict:
    """Captura los cortes vencidos. No hace nada si no hay checkpoints due."""
    root = Path(base_path) if base_path else project_root()
    current = _aware_now(now)
    campaigns = discover_campaigns(root, tenant_ids)
    by_tenant: Dict[str, List[Campaign]] = {}
    for campaign in campaigns:
        by_tenant.setdefault(campaign.tenant_id, []).append(campaign)

    results: List[Dict] = []
    for tenant_id, tenant_campaigns in sorted(by_tenant.items()):
        path = state_path(tenant_id, root)
        state = _read_state(path)
        selected = []
        for campaign in tenant_campaigns:
            checkpoint, missed = due_checkpoint(campaign, state, current)
            if checkpoint:
                selected.append((campaign, checkpoint, missed))

        if not selected:
            upcoming = [
                point
                for campaign in tenant_campaigns
                if (point := next_checkpoint(campaign, state, current)) is not None
            ]
            results.append(
                {
                    "tenant_id": tenant_id,
                    "status": "no_due",
                    "next_checkpoint": min(upcoming, key=lambda item: item.due_at).label
                    if upcoming
                    else None,
                    "next_due_at": min(upcoming, key=lambda item: item.due_at).due_at.isoformat()
                    if upcoming
                    else None,
                    "artifacts": [],
                }
            )
            continue

        if dry_run:
            results.append(
                {
                    "tenant_id": tenant_id,
                    "status": "dry_run",
                    "due": [
                        {
                            "campaign": campaign.slug,
                            "checkpoint": checkpoint.label,
                            "due_at": checkpoint.due_at.isoformat(),
                            "missed": [point.label for point in missed],
                        }
                        for campaign, checkpoint, missed in selected
                    ],
                    "artifacts": [],
                }
            )
            continue

        try:
            config = json.loads((root / "tenants" / tenant_id / "config.json").read_text(encoding="utf-8"))
            if fetcher is None:
                from modules.intelligence.ads_adapters import capture_ads_insights

                fetcher = capture_ads_insights
            api_result = fetcher(config)
        except Exception as exc:
            results.append(
                {
                    "tenant_id": tenant_id,
                    "status": "error",
                    "note": f"{type(exc).__name__}: {exc}",
                    "artifacts": [],
                }
            )
            continue

        if api_result.get("status") != "success":
            results.append(
                {
                    "tenant_id": tenant_id,
                    "status": "error",
                    "note": api_result.get("note") or api_result.get("status"),
                    "artifacts": [],
                }
            )
            continue

        all_ads = api_result.get("ads") or []
        record_ad_insights(tenant_id, all_ads, day=current.date(), base_path=root)
        artifacts: List[str] = []
        for campaign, checkpoint, missed in selected:
            campaign_ads = [
                ad
                for ad in all_ads
                if str(ad.get("campaign_id")) == campaign.campaign_id
            ]
            reconciliation = reconcile_campaign_metadata(
                campaign,
                root,
                ads=campaign_ads,
                now=current,
            )
            rows = [
                ad_insight_row(ad, current.date().isoformat(), current.isoformat())
                for ad in campaign_ads
            ]
            report = build_report(rows, max_cpa)
            payload = _capture_payload(campaign, checkpoint, report, current)
            json_path = report_dir(tenant_id, campaign.slug, root) / f"{checkpoint.label}.json"
            md_path = json_path.with_suffix(".md")
            _write_json(json_path, payload)
            _write_text(
                md_path,
                render_markdown(
                    report,
                    tenant_id=tenant_id,
                    campaign_slug=campaign.slug,
                    campaign_id=campaign.campaign_id,
                    checkpoint=checkpoint.label,
                    scheduled_for=checkpoint.due_at.isoformat(),
                    captured_at=current.isoformat(),
                    elapsed_hours=payload["elapsed_hours"],
                    late_minutes=payload["late_minutes"],
                ),
            )
            plan_files = _write_change_plan(
                campaign=campaign,
                checkpoint=checkpoint,
                report=report,
                capture_payload=payload,
                metadata_reconciliation=reconciliation,
                current=current,
                root=root,
            )
            artifact_files = [json_path, md_path, *plan_files]
            artifact_paths = [str(path.relative_to(root)) for path in artifact_files]
            if reconciliation.get("campaign_json_artifact"):
                artifact_paths.append(reconciliation["campaign_json_artifact"])
            artifacts.extend(artifact_paths)

            campaign_state = state["campaigns"].setdefault(campaign.slug, {})
            campaign_state.update(
                {
                    "campaign_id": campaign.campaign_id,
                    "name": campaign.name,
                    "start_at": campaign.start_at.isoformat(),
                    "stop_at": campaign.stop_at.isoformat() if campaign.stop_at else None,
                }
            )
            checkpoints = campaign_state.setdefault("checkpoints", {})
            for point in missed:
                checkpoints[point.label] = {
                    "status": "missed",
                    "scheduled_for": point.due_at.isoformat(),
                    "recorded_at": current.isoformat(),
                    "reason": f"captured_later_checkpoint:{checkpoint.label}",
                }
            checkpoints[checkpoint.label] = {
                "status": "captured",
                "scheduled_for": checkpoint.due_at.isoformat(),
                "captured_at": current.isoformat(),
                "late_minutes": payload["late_minutes"],
                "total_spend": report["total_spend"],
                "total_conversations": report["total_conversations"],
                "remaining_alerts": report["alerts"],
                "artifacts": artifact_paths,
            }

        _write_json(path, state)
        results.append(
            {
                "tenant_id": tenant_id,
                "status": "captured",
                "campaigns": [campaign.slug for campaign, _, _ in selected],
                "checkpoints": [checkpoint.label for _, checkpoint, _ in selected],
                "artifacts": artifacts,
            }
        )

    statuses = {item["status"] for item in results}
    if "error" in statuses:
        status = "error"
    elif "captured" in statuses:
        status = "success"
    elif "dry_run" in statuses:
        status = "dry_run"
    else:
        status = "no_due"
    return {"status": status, "checked_at": current.isoformat(), "tenants": results}


def _print_result(result: Dict) -> None:
    print(f"[{result['status']}] captura de campañas · {result['checked_at']}")
    for tenant in result["tenants"]:
        if tenant["status"] == "no_due":
            next_due = tenant.get("next_due_at")
            suffix = f" · próximo {next_due}" if next_due else ""
            print(f"  {tenant['tenant_id']}: sin cortes pendientes{suffix}")
        elif tenant["status"] == "dry_run":
            for item in tenant["due"]:
                print(
                    f"  {tenant['tenant_id']}: pendiente {item['campaign']} "
                    f"{item['checkpoint']} ({item['due_at']})"
                )
        elif tenant["status"] == "captured":
            print(
                f"  {tenant['tenant_id']}: capturado "
                f"{', '.join(tenant['checkpoints'])} · {len(tenant['artifacts'])} archivos"
            )
        else:
            print(f"  {tenant['tenant_id']}: error · {tenant.get('note', '')}", file=sys.stderr)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Captura cortes E24/E48/E72/diarios/FINAL de Ads")
    parser.add_argument("--tenant", action="append", help="Tenant objetivo; repetible")
    parser.add_argument("--all-tenants", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Solo muestra cortes pendientes")
    parser.add_argument("--max-cpa", type=float, default=DEFAULT_MAX_CPA)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    tenants = args.tenant if args.tenant and not args.all_tenants else None
    result = run_due_captures(
        tenant_ids=tenants,
        dry_run=args.dry_run,
        max_cpa=args.max_cpa,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_result(result)
    return 1 if result["status"] == "error" else 0


if __name__ == "__main__":
    raise SystemExit(main())
