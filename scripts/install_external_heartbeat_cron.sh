#!/usr/bin/env bash
# Instala el heartbeat externo en el crontab del usuario, sin sudo.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKER="# Growth OS external heartbeat"
JOB="*/5 * * * * cd $ROOT && set -a && . ./.env && set +a && /usr/bin/python3 scripts/ping_external_monitor.py >> logs/external_monitor.log 2>&1"

CURRENT="$(crontab -l 2>/dev/null || true)"
{
  printf '%s\n' "$CURRENT" | grep -vF "$MARKER" | grep -vF "scripts/ping_external_monitor.py" || true
  printf '%s\n' "$MARKER"
  printf '%s\n' "$JOB"
} | sed '/^[[:space:]]*$/d' | crontab -

echo "Heartbeat externo instalado cada 5 minutos en el crontab del usuario."
