#!/usr/bin/env bash
# Xubuntu pre-LUKS backup inventory for Universe Sent Me.
# Reads metadata and package/service names only. It never reads file contents,
# environment values, tokens, raw evidence, browser profiles, SSH keys, or
# OmniRoute/USM configuration contents. It makes no changes and uses no sudo.

set -euo pipefail
export LC_ALL=C

section() {
  printf '\n===== %s =====\n' "$1"
}

value_or_missing() {
  local command_name="$1"
  shift
  if command -v "$command_name" >/dev/null 2>&1; then
    "$@" 2>&1 || printf 'UNAVAILABLE_OR_FAILED\n'
  else
    printf 'NOT_INSTALLED\n'
  fi
}

path_metadata() {
  local path="$1"
  if [ -e "$path" ] || [ -L "$path" ]; then
    printf 'PATH: %s\n' "$path"
    stat -c 'TYPE=%F MODE=%a OWNER=%U:%G SIZE_BYTES=%s MODIFIED=%y' "$path" 2>/dev/null || true
    du -sh "$path" 2>/dev/null || true
  else
    printf 'PATH: %s (ABSENT)\n' "$path"
  fi
}

section 'SAFE INVENTORY SCOPE'
cat <<'EOF'
This report contains metadata only. It intentionally excludes file contents,
environment values, tokens, OAuth credentials, API keys, raw evidence, browser
profiles, SSH material, email content, chat history, and Docker inspect output.
Do not paste secrets into chat. Review the report before sharing it.
EOF

section 'SYSTEM AND STORAGE METADATA'
value_or_missing uname uname -srmo
if [ -r /etc/os-release ]; then
  grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release || true
fi
value_or_missing lsblk lsblk -o NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS
value_or_missing df df -hT /

section 'CORE APPLICATIONS AND RUNTIMES'
for binary in python3 pip3 git curl wget node npm pnpm docker docker-compose podman gws; do
  if command -v "$binary" >/dev/null 2>&1; then
    printf '%s\t%s\n' "$binary" "$(command -v "$binary")"
  else
    printf '%s\tNOT_INSTALLED\n' "$binary"
  fi
done
value_or_missing python3 python3 --version
value_or_missing node node --version
value_or_missing npm npm --version
value_or_missing pnpm pnpm --version
value_or_missing git git --version
value_or_missing docker docker --version
value_or_missing gws gws --version

section 'MANUALLY INSTALLED APT PACKAGES'
if command -v apt-mark >/dev/null 2>&1; then
  apt-mark showmanual | sort
else
  printf 'APT_MARK_UNAVAILABLE\n'
fi

section 'SNAP AND FLATPAK APPLICATION NAMES'
if command -v snap >/dev/null 2>&1; then
  snap list 2>/dev/null || printf 'SNAP_LIST_UNAVAILABLE\n'
else
  printf 'SNAP_NOT_INSTALLED\n'
fi
if command -v flatpak >/dev/null 2>&1; then
  flatpak list --app --columns=application,version 2>/dev/null || printf 'FLATPAK_LIST_UNAVAILABLE\n'
else
  printf 'FLATPAK_NOT_INSTALLED\n'
fi

section 'LOCAL SERVICES AND CONTAINERS METADATA'
if command -v systemctl >/dev/null 2>&1; then
  systemctl is-enabled docker.service 2>/dev/null || true
  systemctl is-active docker.service 2>/dev/null || true
  systemctl --user list-timers --all --no-pager 2>/dev/null || printf 'USER_TIMERS_UNAVAILABLE\n'
fi
if command -v docker >/dev/null 2>&1; then
  docker ps -a --format 'CONTAINER={{.Names}} IMAGE={{.Image}} STATUS={{.Status}}' 2>/dev/null || printf 'DOCKER_LIST_UNAVAILABLE\n'
fi

section 'PROJECT AND CONFIGURATION PATH METADATA'
for path in \
  "$HOME/bin" \
  "$HOME/omniroute-pilot" \
  "$HOME/.config/usm-metrics" \
  "$HOME/.local/share/usm-metrics" \
  "$HOME/universe-sent-me-growth-os" \
  "$HOME/Documents" \
  "$HOME/Desktop" \
  "$HOME/Pictures" \
  "$HOME/Videos" \
  "$HOME/Downloads"; do
  path_metadata "$path"
done

section 'SAFE FILE NAME INVENTORY FOR LOCAL USM SCRIPTS'
if [ -d "$HOME/bin" ]; then
  find "$HOME/bin" -maxdepth 1 -type f -printf 'FILE=%f SIZE_BYTES=%s MODIFIED=%TY-%Tm-%TdT%TH:%TM:%TS\n' 2>/dev/null | sort
else
  printf 'HOME_BIN_ABSENT\n'
fi

section 'KNOWN USM VIRTUAL ENVIRONMENT PACKAGE NAMES'
for python_path in \
  "$HOME/.local/share/usm-metrics/venv/bin/python" \
  "$HOME/.local/share/usm-metrics/venv/bin/python3"; do
  if [ -x "$python_path" ]; then
    printf 'VENV=%s\n' "$python_path"
    "$python_path" -m pip freeze 2>/dev/null || printf 'VENV_PIP_METADATA_UNAVAILABLE\n'
  fi
done

section 'EXPLICITLY EXCLUDED FROM THIS REPORT'
cat <<'EOF'
- Contents of ~/.config/usm-metrics and ~/.local/share/usm-metrics
- Evidence/raw folders, shadow-ledger paths, tokens and OAuth credentials
- OmniRoute configuration/data contents and Docker inspect output
- Browser profiles, cookies, saved passwords and history
- SSH keys, GPG keys, email, chat, documents, media and account data
- Crontab contents and system configuration file contents
EOF

section 'END OF SAFE INVENTORY'
printf 'STATUS=inventory_metadata_only_complete\n'
