#!/usr/bin/env bash
# USM post-LUKS synthetic preflight.
# Design reminder: allow only fixture-only, no-network verification; keep OmniRoute, collectors, cron, and all real data inactive.
set -euo pipefail

readonly CONFIRMATION='RUN_USM_SYNTHETIC_BOUNDARY_SUITE'
readonly REPO_ROOT="${HOME}/universe-sent-me-growth-os"
MODE='plan'
CONFIRM=''

usage() {
  cat <<'EOF'
Usage:
  preflight_usm_synthetic_after_luks.sh --plan
  preflight_usm_synthetic_after_luks.sh --preflight
  preflight_usm_synthetic_after_luks.sh --execute --confirm RUN_USM_SYNTHETIC_BOUNDARY_SUITE

Safety limits:
  - --plan does not inspect the operating environment.
  - --preflight reads only script/fixture metadata and process state.
  - --execute runs only validate_synthetic_boundary_suite.py with Python -B.
  - This wrapper does not install packages, open network connections, read private metrics,
    start OmniRoute/Docker, invoke collectors, schedule cron, or write canonical ledgers.
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

printf 'USM post-LUKS synthetic preflight\n'
printf 'mode=%s\n' "$MODE"
printf 'network=prohibited\n'
printf 'real_data=prohibited\n'
printf 'services_start=prohibited\n'

if [ "$MODE" = 'plan' ]; then
  usage
  exit 0
fi

[ -d "$REPO_ROOT/.git" ] || die 'canonical GitHub repository clone is absent'
command -v python3 >/dev/null 2>&1 || die 'python3 is required'

readonly SUITE="$REPO_ROOT/Operations/Automation/validate_synthetic_boundary_suite.py"
readonly NORMALIZER="$REPO_ROOT/Operations/Automation/validate_normalization_dry_run.py"
readonly LEDGER="$REPO_ROOT/Operations/Automation/validate_shadow_ledger_synthetic.py"
readonly NORMALIZER_FIXTURE="$REPO_ROOT/Operations/Automation/fixtures/normalization_dry_run_synthetic.json"
readonly LEDGER_FIXTURE="$REPO_ROOT/Operations/Automation/fixtures/shadow_ledger_synthetic.json"
for required in "$SUITE" "$NORMALIZER" "$LEDGER" "$NORMALIZER_FIXTURE" "$LEDGER_FIXTURE"; do
  [ -f "$required" ] || die "required synthetic file is absent: $required"
done

printf 'python=%s\n' "$(python3 --version 2>&1)"
printf 'repo_commit=%s\n' "$(git -C "$REPO_ROOT" log -1 --format=%h)"
printf 'fixture_normalizer=present\n'
printf 'fixture_shadow_ledger=present\n'

if pgrep -af 'omniroute|docker compose|fetch_(tiktok|youtube|facebook|instagram)_official_metrics|run_daily_metrics_cut|run_metrics_windows' >/dev/null; then
  echo 'STATUS=blocked_usm_service_or_collector_process_detected'
  pgrep -af 'omniroute|docker compose|fetch_(tiktok|youtube|facebook|instagram)_official_metrics|run_daily_metrics_cut|run_metrics_windows'
  exit 1
fi

if [ "$MODE" = 'preflight' ]; then
  echo 'services_or_collectors=not_detected'
  echo 'STATUS=preflight_complete_fixture_only_no_network_no_real_data'
  exit 0
fi

[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$CONFIRM" = "$CONFIRMATION" ] || die 'exact --confirm string is required'

cd "$REPO_ROOT/Operations/Automation"
python3 -B validate_synthetic_boundary_suite.py
echo 'STATUS=synthetic_boundary_suite_complete_no_real_data'
