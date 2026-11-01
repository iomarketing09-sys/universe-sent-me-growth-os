#!/usr/bin/env bash
# Instala el publicador de respuestas ya aprobadas y su timer.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo cp \
  "$ROOT/scripts/growth-os-comments-publish.service" \
  "$ROOT/scripts/growth-os-comments-publish.timer" \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now growth-os-comments-publish.timer
sudo systemctl start --no-block growth-os-comments-publish.service

systemctl list-timers growth-os-comments-publish.timer --no-pager
