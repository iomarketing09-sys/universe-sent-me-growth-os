#!/usr/bin/env python3
"""Genera un plan de cambios local desde una captura de métricas.

Solo lee archivos locales y escribe el plan en
``tenants/<tenant>/ads/plans/<slug>/``. No consulta ni modifica Meta.

    python3 tools/ads_plan.py --tenant flexi \
      --campaign 120247658527630665 --checkpoint E48
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core" / "growthos-core"))

from modules.intelligence.campaign_capture import (
    discover_campaigns,
    reconcile_campaign_metadata,
    report_dir,
)
from modules.intelligence.campaign_optimizer import (
    build_change_plan,
    load_policy,
    plan_paths,
    render_plan_markdown,
)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _write_json(path: Path, payload: Dict) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _select_campaign(tenant_id: str, reference: str):
    matches = [
        campaign
        for campaign in discover_campaigns(ROOT, [tenant_id])
        if reference in (campaign.campaign_id, campaign.slug)
    ]
    if not matches:
        raise ValueError(f"No encontré la campaña {reference!r} para {tenant_id!r}")
    if len(matches) > 1:
        raise ValueError(f"La referencia {reference!r} coincide con varias campañas")
    return matches[0]


def _capture_file(campaign, checkpoint: str, override: Optional[Path]) -> Path:
    if override is not None:
        return override
    return report_dir(campaign.tenant_id, campaign.slug, ROOT) / f"{checkpoint}.json"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Genera un plan de cambios sin tocar Meta")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--campaign", required=True, help="ID de Meta o slug local")
    parser.add_argument("--checkpoint", required=True, help="E24, E48, E72, E96, FINAL...")
    parser.add_argument("--capture", type=Path, help="Captura JSON alternativa")
    parser.add_argument("--dry-run", action="store_true", help="No escribe archivos locales")
    parser.add_argument("--json", action="store_true", help="Imprime el plan como JSON")
    args = parser.parse_args(argv)

    try:
        campaign = _select_campaign(args.tenant, args.campaign)
        capture_path = _capture_file(campaign, args.checkpoint, args.capture)
        capture = json.loads(capture_path.read_text(encoding="utf-8"))
        if capture.get("campaign_id") not in (None, campaign.campaign_id):
            raise ValueError(
                f"La captura pertenece a {capture.get('campaign_id')!r}, "
                f"no a {campaign.campaign_id!r}"
            )
        scheduled_for = capture.get("scheduled_for")
        if not scheduled_for:
            raise ValueError("La captura no contiene scheduled_for; no se puede decidir")
        scheduled_at = datetime.fromisoformat(str(scheduled_for).replace("Z", "+00:00"))
        elapsed_hours = (
            scheduled_at.astimezone(timezone.utc)
            - campaign.start_at.astimezone(timezone.utc)
        ).total_seconds() / 3600
        reconciliation = reconcile_campaign_metadata(campaign, ROOT)
        plan = build_change_plan(
            capture,
            tenant_id=campaign.tenant_id,
            campaign_id=campaign.campaign_id,
            campaign_slug=campaign.slug,
            campaign_name=campaign.name,
            elapsed_hours=elapsed_hours,
            capture_elapsed_hours=capture.get("elapsed_hours"),
            scheduled_for=scheduled_for,
            checkpoint=args.checkpoint,
            policy=load_policy(ROOT / "tenants" / campaign.tenant_id),
            metadata_reconciliation=reconciliation,
        )
        json_path, md_path = plan_paths(
            campaign.tenant_id,
            campaign.slug,
            args.checkpoint,
            ROOT,
        )
        if not args.dry_run:
            _write_json(json_path, plan)
            _write_text(md_path, render_plan_markdown(plan))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    elif args.dry_run:
        print(render_plan_markdown(plan))
    else:
        print(f"Plan: {json_path.relative_to(ROOT)}")
        print(f"Evidencia: {md_path.relative_to(ROOT)}")
        print("Modo: recommendation_only · sin escrituras en Meta")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
