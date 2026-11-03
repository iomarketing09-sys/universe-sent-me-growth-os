#!/usr/bin/env bash
# Instala el ciclo de métricas de intelligence y su timer.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo cp \
  "$ROOT/scripts/growth-os-intelligence.service" \
  "$ROOT/scripts/growth-os-intelligence.timer" \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-intelligence.timer

systemctl list-timers growth-os-intelligence.timer --no-pager
