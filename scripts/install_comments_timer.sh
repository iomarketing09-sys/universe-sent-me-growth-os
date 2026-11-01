#!/usr/bin/env bash
# Instala y activa el timer de captura de comentarios (sin publicar).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo cp \
  "$ROOT/scripts/growth-os-comments.service" \
  "$ROOT/scripts/growth-os-comments.timer" \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-comments.timer

systemctl list-timers growth-os-comments.timer --no-pager
