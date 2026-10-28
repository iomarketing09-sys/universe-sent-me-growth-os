"""Meta Ads Agent: lee y explica los resultados de campañas de Meta.

Solo lectura: consulta la Marketing API (o un snapshot local) y devuelve
métricas normalizadas por campaña. No crea, edita, pausa ni publica anuncios.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from modules.intelligence.ads_adapters import capture_ads_insights

CONVERSATION_ACTIONS = (
    "onsite_conversion.messaging_conversation_started_7d",
    "onsite_conversion.messaging_first_reply",
    "onsite_conversion.total_messaging_connection",
)


def project_root() -> Path:
    current = Path(__file__).resolve().parent
    for candidate in (current, *current.parents):
        if (candidate / "tenants").is_dir() and (candidate / "modules").is_dir():
            return candidate
    return current.parents[4]


class MetaAdsAgent:
    """Resultados de Meta Ads por tenant, con métricas derivadas."""

    def __init__(
        self,
        tenant_id: str = "flexi",
        base_path: Optional[str] = None,
        fetcher: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path) if base_path else project_root()
        self.tenant_path = self.base_path / "tenants" / tenant_id
        self.fetcher = fetcher or capture_ads_insights

    # ------------------------------------------------------------------ config
    def load_config(self) -> Dict[str, Any]:
        path = self.tenant_path / "config.json"
        if not path.is_file():
            raise FileNotFoundError(f"No existe config.json para el tenant: {self.tenant_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def ad_account_id(self) -> str:
        ads = self.load_config().get("ads") or {}
        return str(ads.get("ad_account_id") or "")

    # ------------------------------------------------------------------- datos
    def fetch(self) -> Dict[str, Any]:
        """Consulta la Marketing API. Lanza si el tenant no tiene ads configurados."""
        config = self.load_config()
        if not (config.get("ads") or {}).get("ad_account_id"):
            raise ValueError(f"El tenant {self.tenant_id} no tiene ads.ad_account_id")
        return self.fetcher(config)

    def load_snapshot(self) -> Dict[str, Any]:
        """Lee el último snapshot del sync diario, sin salir a la red."""
        path = self.tenant_path / "data" / "sync" / "latest.json"
        if not path.is_file():
            raise FileNotFoundError(f"No hay snapshot del sync en {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def ads_source(self, offline: bool = False) -> Dict[str, Any]:
        if not offline:
            return self.fetch()
        snapshot = self.load_snapshot()
        sources = snapshot.get("sources") or {}
        return sources.get("ads") or {}

    # --------------------------------------------------------------- métricas
    @staticmethod
    def _kpis(campaign: Dict[str, Any]) -> Dict[str, Any]:
        spend = float(campaign.get("spend") or 0)
        impressions = int(campaign.get("impressions") or 0)
        clicks = int(campaign.get("clicks") or 0)
        conversations = int(campaign.get("conversations") or 0)
        return {
            "spend": round(spend, 2),
            "impressions": impressions,
            "clicks": clicks,
            "reach": int(campaign.get("reach") or 0),
            "ctr": round(float(campaign.get("ctr") or 0), 2),
            "cpc": round(float(campaign.get("cpc") or 0), 2),
            "cpm": round(float(campaign.get("cpm") or 0), 2),
            "conversations": conversations,
            "cost_per_conversation": round(
                conversations and spend / conversations or 0.0, 2
            ),
            "click_to_conversation": round(
                conversations and clicks / conversations or 0.0, 2
            ),
        }

    def campaigns(
        self, offline: bool = False, campaign_slug: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        source = self.ads_source(offline=offline)
        campaigns = source.get("campaigns") or []
        if campaign_slug:
            campaigns = [c for c in campaigns if campaign_slug in str(c.get("name", ""))]
        return [
            {
                "id": c.get("id"),
                "name": c.get("name", ""),
                "objective": c.get("objective", ""),
                "status": c.get("status", ""),
                **self._kpis(c),
                "messaging_metrics": c.get("messaging_metrics") or {},
            }
            for c in campaigns
        ]

    def summary(self, offline: bool = False) -> Dict[str, Any]:
        campaigns = self.campaigns(offline=offline)
        totals = {
            key: round(sum(c[key] for c in campaigns), 2)
            for key in ("spend", "impressions", "clicks", "reach", "conversations")
        }
        totals["cost_per_conversation"] = round(
            totals["conversations"] and totals["spend"] / totals["conversations"] or 0.0, 2
        )
        totals["ctr"] = round(
            totals["impressions"] and 100 * totals["clicks"] / totals["impressions"] or 0.0, 2
        )
        return {"campaigns": len(campaigns), **totals}

    def report(
        self, offline: bool = False, campaign_slug: Optional[str] = None
    ) -> Dict[str, Any]:
        campaigns = self.campaigns(offline=offline, campaign_slug=campaign_slug)
        totals = {
            key: round(sum(c[key] for c in campaigns), 2)
            for key in ("spend", "impressions", "clicks", "reach", "conversations")
        }
        totals["cost_per_conversation"] = round(
            totals["conversations"] and totals["spend"] / totals["conversations"] or 0.0, 2
        )
        totals["ctr"] = round(
            totals["impressions"] and 100 * totals["clicks"] / totals["impressions"] or 0.0, 2
        )
        return {
            "tenant_id": self.tenant_id,
            "ad_account_id": self.ad_account_id(),
            "source": "snapshot" if offline else "marketing_api",
            "campaign_filter": campaign_slug,
            "totals": totals,
            "campaigns": campaigns,
            "notes": self._notes(campaigns),
        }

    @staticmethod
    def _notes(campaigns: List[Dict[str, Any]]) -> List[str]:
        notes: List[str] = []
        for campaign in campaigns:
            messaging = campaign.get("messaging_metrics") or {}
            if messaging.get("messaging_user_depth_2"):
                continue
            notes.append(
                f"{campaign['name']}: Meta no reporta profundidad 2/3 en esta campaña; "
                "la profundidad real de conversación se mide con el módulo communications."
            )
        return notes


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Meta Ads Agent (solo lectura)")
    parser.add_argument("tenant", nargs="?", default="flexi")
    parser.add_argument("--campaign", default=None, help="Filtra por nombre/slug de campaña")
    parser.add_argument("--offline", action="store_true", help="Usa el último snapshot del sync")
    parser.add_argument("--base-path", default=None)
    args = parser.parse_args()

    agent = MetaAdsAgent(args.tenant, base_path=args.base_path)
    print(
        json.dumps(
            agent.report(offline=args.offline, campaign_slug=args.campaign),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
