"""WhatsApp Agent: reporte de solo lectura de la conversación de un tenant.

No envía mensajes: junta volumen, profundidad de conversación, atribución a
anuncios y diagnóstico de ecos en un solo reporte.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from modules.communications.whatsapp import conversations as conv
from modules.communications.whatsapp import d1
from modules.communications.whatsapp.echo_diagnostics import diagnose_echoes


class WhatsAppAgent:
    def __init__(self, tenant_id: str = "flexi", base_path: Optional[str] = None):
        self.tenant_id = tenant_id
        self.base_path = base_path

    def volume(self) -> Dict[str, Any]:
        """Eventos por dirección y estados de entrega."""
        directions = {
            str(row.get("direction")): int(row.get("n") or 0)
            for row in d1.query(
                "SELECT direction, COUNT(*) AS n FROM events GROUP BY direction",
                tenant_id=self.tenant_id,
                base_path=self.base_path,
            )
        }
        statuses = {
            str(row.get("status")): int(row.get("n") or 0)
            for row in d1.query(
                "SELECT COALESCE(status, 'unknown') AS status, COUNT(*) AS n"
                " FROM events WHERE direction = 'status' GROUP BY status",
                tenant_id=self.tenant_id,
                base_path=self.base_path,
            )
        }
        return {"directions": directions, "statuses": statuses}

    def conversations(self, limit: int = 200) -> Dict[str, Any]:
        return conv.conversation_summary(
            self.tenant_id, limit=limit, base_path=self.base_path
        )

    def depth(self) -> Dict[str, Any]:
        return conv.depth_distribution(self.tenant_id, base_path=self.base_path)

    def campaigns(self) -> Dict[str, Any]:
        return conv.campaign_conversations(self.tenant_id, base_path=self.base_path)

    def echoes(self, check_graph: bool = True) -> Dict[str, Any]:
        return diagnose_echoes(
            self.tenant_id, base_path=self.base_path, check_graph=check_graph
        ).to_dict()

    def report(self, limit: int = 200, check_graph: bool = False) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "volume": self.volume(),
            "depth": self.depth(),
            "campaigns": self.campaigns(),
            "recent_conversations": self.conversations(limit=limit)["conversations"],
            "echoes": self.echoes(check_graph=check_graph),
        }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="WhatsApp Agent (solo lectura)")
    parser.add_argument("tenant", nargs="?", default="flexi")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--graph", action="store_true", help="Consultar Graph API en el diagnóstico")
    parser.add_argument(
        "--only",
        choices=["report", "volume", "conversations", "depth", "campaigns", "echoes"],
        default="report",
    )
    args = parser.parse_args()

    agent = WhatsAppAgent(args.tenant)
    if args.only == "report":
        result: Any = agent.report(limit=args.limit, check_graph=args.graph)
    elif args.only == "echoes":
        result = agent.echoes(check_graph=args.graph)
    else:
        result = getattr(agent, args.only)()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
