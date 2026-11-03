#!/usr/bin/env bash
# Instala el watchdog de operación compartida y su timer.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo cp \
  "$ROOT/scripts/growth-os-health.service" \
  "$ROOT/scripts/growth-os-health.timer" \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-health.timer

systemctl list-timers growth-os-health.timer --no-pager
