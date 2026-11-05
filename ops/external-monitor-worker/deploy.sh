#!/usr/bin/env bash
# Despliega el monitor externo compartido en Cloudflare Workers + D1.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"
ROOT_ENV="$ROOT/.env"
ACCOUNT_FILE="$ROOT/tenants/flexi/whatsapp/config.json"
DB_NAME="growth_os_external_monitor"

export npm_config_cache="${npm_config_cache:-$DIR/.wrangler/npm-cache}"
export npm_config_update_notifier=false
export WRANGLER_SEND_METRICS=false
export XDG_CONFIG_HOME="$DIR/.wrangler/config"
export WRANGLER_LOG_PATH="$DIR/.wrangler/logs/wrangler.log"
mkdir -p "$XDG_CONFIG_HOME" "$(dirname "$WRANGLER_LOG_PATH")"
WRANGLER="npx --yes wrangler@4"

get_from() {
  python3 - "$1" "$2" <<'PY'
import sys
from pathlib import Path
path, key = Path(sys.argv[1]), sys.argv[2]
if not path.exists():
    sys.exit(0)
for line in path.read_text().splitlines():
    line = line.strip()
    if line.startswith(key + "="):
        print(line.split("=", 1)[1].strip().strip('"\''))
        break
PY
}

export CLOUDFLARE_API_TOKEN="$(get_from "$ROOT_ENV" CLOUDFLARE_API_TOKEN)"
if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  export CLOUDFLARE_API_TOKEN="$(get_from "$ROOT_ENV" CF_API_TOKEN)"
fi
export CLOUDFLARE_ACCOUNT_ID="$(get_from "$ROOT_ENV" CLOUDFLARE_ACCOUNT_ID)"
if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  export CLOUDFLARE_ACCOUNT_ID="$(python3 - "$ACCOUNT_FILE" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
print((json.loads(path.read_text()).get("cloudflare") or {}).get("account_id", "") if path.exists() else "")
PY
)"
fi

if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ] || [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  echo "ERROR: faltan CLOUDFLARE_ACCOUNT_ID o CLOUDFLARE_API_TOKEN/CF_API_TOKEN" >&2
  exit 2
fi

cd "$DIR"

echo "== 1/6 comprobando credenciales =="
$WRANGLER whoami

echo "== 2/6 base D1 =="
DB_ID="$($WRANGLER d1 list --json 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    data = []
print(next((d.get('uuid', '') for d in data if d.get('name') == '$DB_NAME'), ''))
" || true)"
if [ -z "$DB_ID" ]; then
  echo "  creando $DB_NAME..."
  OUT="$($WRANGLER d1 create "$DB_NAME" 2>&1 || true)"
  printf '%s\n' "$OUT"
  DB_ID="$(printf '%s' "$OUT" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)"
fi
[ -n "$DB_ID" ] || { echo "ERROR: no pude obtener el database_id" >&2; exit 3; }
echo "  database_id=$DB_ID"

python3 - "$DB_ID" <<'PY'
import re, sys
from pathlib import Path
path = Path("wrangler.toml")
path.write_text(re.sub(r'database_id\s*=\s*"[^"]*"', f'database_id = "{sys.argv[1]}"', path.read_text(), count=1))
PY

echo "== 3/6 esquema =="
$WRANGLER d1 execute "$DB_NAME" --remote --yes --file=schema.sql

echo "== 4/6 despliegue =="
$WRANGLER deploy

echo "== 5/6 secretos =="
MONITOR_TOKEN="$(get_from "$ROOT_ENV" EXTERNAL_MONITOR_TOKEN)"
if [ -z "$MONITOR_TOKEN" ]; then
  MONITOR_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
  printf '\nEXTERNAL_MONITOR_TOKEN=%s\n' "$MONITOR_TOKEN" >> "$ROOT_ENV"
  echo "  EXTERNAL_MONITOR_TOKEN generado y guardado en .env"
fi
printf '%s' "$MONITOR_TOKEN" | $WRANGLER secret put MONITOR_TOKEN
printf '%s' "$(get_from "$ROOT_ENV" TELEGRAM_BOT_TOKEN)" | $WRANGLER secret put TELEGRAM_BOT_TOKEN
printf '%s' "$(get_from "$ROOT_ENV" TELEGRAM_CHAT_ID)" | $WRANGLER secret put TELEGRAM_CHAT_ID
sleep 2

echo "== 6/6 URL y prueba =="
HEARTBEAT_URL="https://growth-os-external-monitor.io-marketing-09.workers.dev/heartbeat?token=$MONITOR_TOKEN"
python3 - "$ROOT_ENV" "$HEARTBEAT_URL" <<'PY'
import sys
from pathlib import Path
path, value = Path(sys.argv[1]), sys.argv[2]
line = f"EXTERNAL_MONITOR_HEARTBEAT_URL={value}"
text = path.read_text()
if "EXTERNAL_MONITOR_HEARTBEAT_URL=" in text:
    lines = [line if item.startswith("EXTERNAL_MONITOR_HEARTBEAT_URL=") else item for item in text.splitlines()]
    path.write_text("\n".join(lines) + "\n")
else:
    path.write_text(text.rstrip() + "\n" + line + "\n")
PY
python3 "$ROOT/scripts/ping_external_monitor.py"
TOKEN="$MONITOR_TOKEN" python3 - <<'PY'
import json, os, urllib.request
url = "https://growth-os-external-monitor.io-marketing-09.workers.dev/check?token=" + os.environ["TOKEN"]
request = urllib.request.Request(
    url,
    headers={"Accept": "application/json", "User-Agent": "GrowthOS-ExternalMonitor/1.0"},
)
with urllib.request.urlopen(request, timeout=20) as response:
    data = json.load(response)
print(json.dumps(data, indent=2, ensure_ascii=False))
PY

echo "Listo. Heartbeat y checks activos."
