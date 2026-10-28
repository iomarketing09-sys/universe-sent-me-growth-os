#!/usr/bin/env bash
# Sync diario de Growth OS — lo invoca growth-os-sync.service (systemd).
#
# Qué hace:
#   1. Carga credenciales del .env (systemd ya las inyecta; esto cubre ejecuciones manuales).
#   2. Sincroniza todos los tenants con datos en vivo de Meta, Ads, Google y WhatsApp.
#   3. Guarda el JSON completo en logs/sync/last.json y una línea de resumen en
#      logs/sync/history.log (esto es lo que queda en el journal).
#
# Sale con código != 0 si el sync falla, para que systemd lo marque como failed.
#
# Uso manual:  bash scripts/cron_sync.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ -f "$ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$ROOT/.env"
  set +a
fi

LOG_DIR="$ROOT/logs/sync"
mkdir -p "$LOG_DIR"
OUT="$LOG_DIR/last.json"
ERR="$LOG_DIR/last.err"
TMP="$(mktemp "$LOG_DIR/.last.XXXXXX")"

TS="$(date '+%Y-%m-%d %H:%M:%S')"

# Retención: los snapshots timestamped viven fuera de git y no crecen sin tope.
find "$ROOT/tenants" -path "*/data/sync/*.json" -type f -mtime +90 -delete 2>/dev/null || true
echo "[$TS] iniciando sync"

# 900s de tope: si Meta o Google no responden, el servicio falla en vez de colgarse.
if timeout 900 python3 scripts/sync_all.py \
    --all --live-meta --live-ads --live-google --live-whatsapp --quiet \
    >"$TMP" 2>"$ERR"; then
  mv "$TMP" "$OUT"
  STATUS=0
else
  STATUS=$?
  rm -f "$TMP"
  echo "[$TS] ERROR: el sync falló con código $STATUS" >&2
  tail -n 20 "$ERR" >&2 || true
fi

if [ "$STATUS" -eq 0 ]; then
  python3 - "$OUT" "$TS" <<'PY'
import json
import sys

path, ts = sys.argv[1], sys.argv[2]

try:
    data = json.load(open(path, encoding="utf-8"))
except (OSError, ValueError) as exc:
    print(f"[{ts}] ERROR: no pude leer {path}: {exc}", file=sys.stderr)
    raise SystemExit(1)

results = data if isinstance(data, list) else [data]
lines = [f"[{ts}] sync OK ({len(results)} tenants)"]

for result in results:
    tenant = result.get("tenant_id", "?")
    sources = result.get("sources") or {}
    statuses = {name: (value or {}).get("status", "?") for name, value in sources.items()}
    if all(status == "not_configured" for status in statuses.values()):
        lines.append(f"  {tenant}: sin configurar")
        continue

    lines.append(f"  {tenant}: " + " ".join(f"{k}={v}" for k, v in statuses.items()))

    ads = sources.get("ads") or {}
    for campaign in ads.get("campaigns") or []:
        lines.append(
            "    ads {name}: gasto=${spend:.2f} impresiones={imp} clics={clicks} "
            "conversaciones={conv} costo/conv=${cpconv:.2f}".format(
                name=campaign.get("name", "?"),
                spend=float(campaign.get("spend") or 0),
                imp=int(campaign.get("impressions") or 0),
                clicks=int(campaign.get("clicks") or 0),
                conv=int(campaign.get("conversations") or 0),
                cpconv=float(campaign.get("cost_per_conversation") or 0),
            )
        )

try:
    from modules.communications.whatsapp import conversations

    depth = conversations.depth_distribution("flexi")
    lines.append(
        "    whatsapp D1: conversaciones={c} profundidad_prom={d} buckets={b}".format(
            c=depth.get("conversations", 0),
            d=depth.get("average_depth", 0),
            b=depth.get("buckets", {}),
        )
    )
except Exception as exc:  # el sync no debe fallar por un reporte extra
    lines.append(f"    whatsapp D1: no disponible ({type(exc).__name__})")

summary = "\n".join(lines)
print(summary)
with open(path.replace("last.json", "history.log"), "a", encoding="utf-8") as fh:
    fh.write(summary + "\n")
PY
  STATUS=$?
fi

echo "[$TS] fin (código $STATUS)"
exit "$STATUS"
