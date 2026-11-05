#!/usr/bin/env bash
# Instala el timer de captura de métricas de Ads (E24/E48/E72/diarios/FINAL).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo cp \
  "$ROOT/scripts/growth-os-ads.service" \
  "$ROOT/scripts/growth-os-ads.timer" \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-ads.timer

systemctl list-timers growth-os-ads.timer --no-pager
