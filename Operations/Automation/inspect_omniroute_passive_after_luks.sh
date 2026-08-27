#!/usr/bin/env bash
# USM post-LUKS OmniRoute passive inspection.
# Design reminder: inspect only filenames, local process/port presence and Docker client metadata; never read secrets or start components.
set -euo pipefail

readonly OMNIROOT="${HOME}/omniroute-pilot"
readonly OMNIPORT='20128'

usage() {
  cat <<'EOF'
Usage: inspect_omniroute_passive_after_luks.sh [--plan|--preflight]

This inspection never installs Docker, starts/stops containers, reads .env files,
contacts an API, opens a network connection, or processes a prompt or real data.
EOF
}

MODE='plan'
case "${1:---plan}" in
  --plan) MODE='plan' ;;
  --preflight) MODE='preflight' ;;
  --help|-h) usage; exit 0 ;;
  *) usage >&2; echo 'STATUS=blocked_passive_modes_only' >&2; exit 64 ;;
esac

printf 'USM OmniRoute passive inspection after LUKS\n'
printf 'mode=%s\n' "$MODE"
printf 'service_start=prohibited\n'
printf 'network_request=prohibited\n'
printf 'secret_read=prohibited\n'

if [ "$MODE" = 'plan' ]; then
  usage
  exit 0
fi

[ -d "$OMNIROOT" ] || { echo 'STATUS=blocked_omniroute_directory_absent'; exit 1; }
stat -c 'omniroute_root=%n mode=%a owner=%U:%G' "$OMNIROOT"

echo '--- ARTIFACT NAMES ONLY ---'
find "$OMNIROOT" -maxdepth 2 -type f \( \
  -name 'compose.yml' -o -name 'compose.yaml' -o \
  -name 'docker-compose.yml' -o -name 'docker-compose.yaml' -o \
  -name 'Dockerfile' -o -name '.env' -o -name '.env.example' -o \
  -name 'package.json' -o -name 'requirements.txt' -o -name 'README*' \
\) -printf '%P\n' | sort

echo '--- DOCKER CLIENT METADATA ---'
if command -v docker >/dev/null 2>&1; then
  docker --version
  if docker compose version >/dev/null 2>&1; then
    docker compose version
  else
    echo 'docker_compose_plugin=absent'
  fi
else
  echo 'docker_client=absent'
fi

if command -v docker-compose >/dev/null 2>&1; then
  docker-compose --version
else
  echo 'docker_compose_legacy=absent'
fi

echo '--- PROCESS AND PORT CHECK ---'
if pgrep -af 'omniroute|docker compose|docker-compose' >/dev/null; then
  echo 'STATUS=blocked_omniroute_or_compose_process_detected'
  pgrep -af 'omniroute|docker compose|docker-compose'
  exit 1
fi

if ss -ltnH '( sport = :'"$OMNIPORT"' )' 2>/dev/null | grep -q .; then
  echo "STATUS=blocked_port_${OMNIPORT}_listening"
  ss -ltnH '( sport = :'"$OMNIPORT"' )'
  exit 1
fi

echo 'omniroute_or_compose_process=not_detected'
echo "port_${OMNIPORT}=not_listening"
echo 'STATUS=passive_inspection_complete_no_service_start_no_network_request'
