#!/usr/bin/env bash
# G-SEC-2.3a synthetic barrier preflight.
# Design reminder: validate policy rejects only; do not read private data, start services, or enable integrations.
set -euo pipefail

readonly CONFIRMATION='RUN_USM_GSEC2_SYNTHETIC_BARRIERS'
readonly REPO_ROOT="${HOME}/universe-sent-me-growth-os"
MODE='plan'
CONFIRM=''

usage() {
  cat <<'EOF'
Usage:
  preflight_gsec2_readonly_barriers.sh --plan
  preflight_gsec2_readonly_barriers.sh --preflight
  preflight_gsec2_readonly_barriers.sh --execute --confirm RUN_USM_GSEC2_SYNTHETIC_BARRIERS

Safety limits:
  - --plan does not inspect the operating environment.
  - --preflight checks only repository, public script/fixture presence and active process names.
  - --execute runs only validate_gsec2_readonly_barriers_synthetic.py with Python -B.
  - The fixture is synthetic; no collector, private configuration, token, evidence or environment variable is read.
  - This wrapper never opens network/OAuth, installs packages, creates a ledger, starts Docker/OmniRoute, or schedules work.
EOF
}

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --plan) MODE='plan' ;;
    --preflight) MODE='preflight' ;;
    --execute) MODE='execute' ;;
    --confirm)
      shift
      [ "$#" -gt 0 ] || die '--confirm requires the exact confirmation string'
      CONFIRM="$1"
      ;;
    --help|-h) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
  shift
done

printf 'USM G-SEC-2 synthetic read-only barrier preflight\n'
printf 'mode=%s\n' "$MODE"
printf 'network=prohibited\n'
printf 'real_data=prohibited\n'
printf 'private_path_and_environment_read=prohibited\n'
printf 'collector_and_service_start=prohibited\n'

if [ "$MODE" = 'plan' ]; then
  usage
  exit 0
fi

[ -d "$REPO_ROOT/.git" ] || die 'canonical GitHub repository clone is absent'
command -v python3 >/dev/null 2>&1 || die 'python3 is required'

readonly VALIDATOR="$REPO_ROOT/Operations/Automation/validate_gsec2_readonly_barriers_synthetic.py"
readonly FIXTURE="$REPO_ROOT/Operations/Automation/fixtures/gsec2_readonly_barriers_synthetic.json"
for required in "$VALIDATOR" "$FIXTURE"; do
  [ -f "$required" ] || die "required synthetic artifact is absent: $required"
done

printf 'python=%s\n' "$(python3 --version 2>&1)"
printf 'repo_commit=%s\n' "$(git -C "$REPO_ROOT" log -1 --format=%h)"
printf 'synthetic_validator=present\n'
printf 'synthetic_fixture=present\n'

if pgrep -af '[o]mniroute|[d]ocker compose|[f]etch_(tiktok|youtube|facebook|instagram)_official_metrics|[r]un_daily_metrics_cut|[r]un_metrics_windows' >/dev/null; then
  echo 'STATUS=blocked_usm_service_or_collector_process_detected'
  pgrep -af '[o]mniroute|[d]ocker compose|[f]etch_(tiktok|youtube|facebook|instagram)_official_metrics|[r]un_daily_metrics_cut|[r]un_metrics_windows'
  exit 1
fi

if [ "$MODE" = 'preflight' ]; then
  echo 'services_or_collectors=not_detected'
  echo 'STATUS=preflight_complete_gsec2_synthetic_only_no_network_no_private_read'
  exit 0
fi

[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$CONFIRM" = "$CONFIRMATION" ] || die 'exact --confirm string is required'

cd "$REPO_ROOT/Operations/Automation"
PYTHONDONTWRITEBYTECODE=1 python3 -B validate_gsec2_readonly_barriers_synthetic.py
echo 'STATUS=gsec2_synthetic_barriers_complete_no_network_no_private_read'
