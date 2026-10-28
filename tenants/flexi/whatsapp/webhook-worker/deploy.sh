#!/usr/bin/env bash
# Despliegue del receptor solo-escucha (Cloudflare Worker + D1) para el tenant `flexi`.
#
# Credenciales (archivos ignorados por git). Se buscan primero en
# `tenants/flexi/.env` y, si no están ahí, en `growth-os/.env`:
#   CLOUDFLARE_ACCOUNT_ID=...       (si falta, se toma de whatsapp/config.json)
#   CLOUDFLARE_API_TOKEN=... o CF_API_TOKEN=...
#                                    (permisos: Workers Scripts:Edit, D1:Edit)
#   WHATSAPP_VERIFY_TOKEN=...        (solo para crear/actualizar el secreto;
#                                     si falta, el secreto existente se conserva)
#
# Uso:  bash deploy.sh
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TENANT_ENV="$DIR/../../.env"
ROOT_ENV="$DIR/../../../../.env"
DB_NAME="flexi_whatsapp_obs"

export npm_config_cache="${npm_config_cache:-/tmp/npmcache}"
export npm_config_update_notifier=false
export WRANGLER_SEND_METRICS=false
# wrangler escribe estado y logs en $XDG_CONFIG_HOME/.wrangler. En este entorno XDG_CONFIG_HOME
# ya viene definida y no es escribible dentro del sandbox, así que la forzamos a /tmp.
export XDG_CONFIG_HOME=/tmp/wrangler-config
export WRANGLER_LOG_PATH=/tmp/wrangler-logs/wrangler.log
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

get_env() {
  local value
  value="$(get_from "$TENANT_ENV" "$1")"
  if [ -z "$value" ]; then value="$(get_from "$ROOT_ENV" "$1")"; fi
  printf '%s' "$value"
}

export CLOUDFLARE_API_TOKEN="$(get_env CLOUDFLARE_API_TOKEN)"
if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  export CLOUDFLARE_API_TOKEN="$(get_env CF_API_TOKEN)"
fi
export CLOUDFLARE_ACCOUNT_ID="$(get_env CLOUDFLARE_ACCOUNT_ID)"
if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  CLOUDFLARE_ACCOUNT_ID="$(python3 - "$DIR/../config.json" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
print((json.loads(path.read_text()).get("cloudflare") or {}).get("account_id", "") if path.exists() else "")
PY
)"
  export CLOUDFLARE_ACCOUNT_ID
fi
VERIFY_TOKEN="$(get_env WHATSAPP_VERIFY_TOKEN)"

if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ] || [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
  echo "ERROR: faltan CLOUDFLARE_ACCOUNT_ID o CLOUDFLARE_API_TOKEN/CF_API_TOKEN" >&2
  echo "       revisados: $TENANT_ENV y $ROOT_ENV" >&2
  exit 2
fi

cd "$DIR"

echo "== 1/5 comprobando credenciales =="
$WRANGLER whoami

echo "== 2/5 base D1 =="
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

echo "== 3/5 esquema =="
$WRANGLER d1 execute "$DB_NAME" --remote --yes --file=schema.sql

echo "== 4/5 despliegue =="
# El secreto se sube DESPUÉS: Cloudflare no permite crear secretos de un script
# que todavía no existe ("No access to the specified resource").
$WRANGLER deploy

echo "== 5/5 secreto del verify token =="
if [ -n "${VERIFY_TOKEN:-}" ]; then
  printf '%s' "$VERIFY_TOKEN" | $WRANGLER secret put WHATSAPP_VERIFY_TOKEN
else
  echo "  omitido: WHATSAPP_VERIFY_TOKEN no está en el entorno; se conserva el secreto actual."
fi

echo
echo "Listo. URL del webhook: <la de arriba>/webhook"
