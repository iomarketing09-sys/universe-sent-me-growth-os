#!/usr/bin/env python3
"""Reporte de rendimiento por anuncio.

Lee el ledger diario que llena el sync. Con ``--live`` consulta Meta y actualiza
el corte de hoy.

    python3 tools/ads_report.py --tenant flexi --campaign 120247658527630665
    python3 tools/ads_report.py --tenant flexi --campaign 120247658527630665 --live
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core" / "growthos-core"))

from modules.intelligence.ads_ledger import load_ad_insights, record_ad_insights
from modules.intelligence.ads_reporting import DEFAULT_MAX_CPA, build_report, render_text


def _fetch_live(tenant_id: str, campaign_id: str) -> List[Dict]:
    from modules.intelligence.ads_adapters import capture_ads_insights

    config_path = ROOT / "tenants" / tenant_id / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    result = capture_ads_insights(config)
    if result.get("status") != "success":
        raise RuntimeError(result.get("note") or result.get("status"))
    ads = [ad for ad in (result.get("ads") or []) if ad.get("campaign_id") == campaign_id]
    record_ad_insights(tenant_id, ads, base_path=ROOT)
    return ads


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Rendimiento por anuncio")
    parser.add_argument("--tenant", required=True)
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--max-cpa", type=float, default=DEFAULT_MAX_CPA)
    parser.add_argument("--live", action="store_true", help="Consultar Meta y actualizar el corte de hoy")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.live:
            _fetch_live(args.tenant, args.campaign)
        rows = load_ad_insights(args.tenant, campaign_id=args.campaign, base_path=ROOT)
        report = build_report(rows, args.max_cpa)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not report["ads"]:
        print("Sin datos. Corre el sync con --live-ads o usa --live.")
        return 0
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
