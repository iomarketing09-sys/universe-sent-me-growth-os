#!/usr/bin/env bash
# Ejecuta el watchdog interno y, después, envía el latido al monitor externo.
# El latido se envía aunque el watchdog reporte un problema de negocio: el
# monitor externo mide liveness del host, no la salud de los workflows.
set +e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

/usr/bin/python3 "$ROOT/scripts/run_ops_health.py" --notify --json
status=$?

/usr/bin/python3 "$ROOT/scripts/ping_external_monitor.py" || true

exit "$status"
