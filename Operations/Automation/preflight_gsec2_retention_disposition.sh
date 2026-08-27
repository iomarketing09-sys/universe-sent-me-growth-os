#!/usr/bin/env bash
# G-SEC-2.2a synthetic retention/disposition preflight.
# Design reminder: policy model only; never read or delete any real local record.
set -euo pipefail

readonly CONFIRMATION='RUN_USM_GSEC2_RETENTION_DISPOSITION_SYNTHETIC'
readonly REPO_ROOT="${HOME}/universe-sent-me-growth-os"
MODE='plan'
CONFIRM=''

usage() {
  cat <<'EOF'
Usage:
  preflight_gsec2_retention_disposition.sh --plan
  preflight_gsec2_retention_disposition.sh --preflight
  preflight_gsec2_retention_disposition.sh --execute --confirm RUN_USM_GSEC2_RETENTION_DISPOSITION_SYNTHETIC

Safety limits: fixture-only; no private paths, environment, collector, socket,
OAuth/API, service, scheduler, installation, ledger/evidence, deletion, or external output.
EOF
}

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
while [ "$#" -gt 0 ]; do
  case "$1" in
    --plan) MODE='plan' ;;
    --preflight) MODE='preflight' ;;
    --execute) MODE='execute' ;;
    --confirm) shift; [ "$#" -gt 0 ] || die '--confirm requires the exact confirmation string'; CONFIRM="$1" ;;
    --help|-h) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
  shift
done

printf 'USM G-SEC-2.2a synthetic retention and disposition preflight\n'
printf 'mode=%s\nnetwork=prohibited\nreal_data=prohibited\nprivate_path_and_environment_read=prohibited\ncollector_and_service_start=prohibited\n' "$MODE"
[ "$MODE" = 'plan' ] && { usage; exit 0; }
[ -d "$REPO_ROOT/.git" ] || die 'canonical GitHub repository clone is absent'
command -v python3 >/dev/null 2>&1 || die 'python3 is required'
readonly VALIDATOR="$REPO_ROOT/Operations/Automation/validate_gsec2_retention_disposition_synthetic.py"
readonly FIXTURE="$REPO_ROOT/Operations/Automation/fixtures/gsec2_retention_disposition_synthetic.json"
for required in "$VALIDATOR" "$FIXTURE"; do [ -f "$required" ] || die "required synthetic artifact is absent: $required"; done
printf 'python=%s\nrepo_commit=%s\nsynthetic_validator=present\nsynthetic_fixture=present\n' "$(python3 --version 2>&1)" "$(git -C "$REPO_ROOT" log -1 --format=%h)"
if pgrep -af '[o]mniroute|[d]ocker compose|[f]etch_(tiktok|youtube|facebook|instagram)_official_metrics|[r]un_daily_metrics_cut|[r]un_metrics_windows' >/dev/null; then
  echo 'STATUS=blocked_usm_service_or_collector_process_detected'
  pgrep -af '[o]mniroute|[d]ocker compose|[f]etch_(tiktok|youtube|facebook|instagram)_official_metrics|[r]un_daily_metrics_cut|[r]un_metrics_windows'
  exit 1
fi
if [ "$MODE" = 'preflight' ]; then
  echo 'services_or_collectors=not_detected'
  echo 'STATUS=preflight_complete_gsec2_retention_disposition_synthetic_only_no_network_no_private_read'
  exit 0
fi
[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$CONFIRM" = "$CONFIRMATION" ] || die 'exact --confirm string is required'
cd "$REPO_ROOT/Operations/Automation"
PYTHONDONTWRITEBYTECODE=1 python3 -B validate_gsec2_retention_disposition_synthetic.py
echo 'STATUS=gsec2_retention_disposition_synthetic_complete_no_network_no_private_read'
