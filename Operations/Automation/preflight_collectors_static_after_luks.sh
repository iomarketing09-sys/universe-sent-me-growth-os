#!/usr/bin/env bash
# USM post-LUKS collector static-review preflight.
# Design reminder: parse only public code/config examples; never import collectors, read private config, use network, or start processes.
set -euo pipefail

readonly CONFIRMATION='RUN_USM_COLLECTORS_STATIC_REVIEW'
readonly REPO_ROOT="${HOME}/universe-sent-me-growth-os"
MODE='plan'
CONFIRM=''

usage() {
  cat <<'EOF'
Usage:
  preflight_collectors_static_after_luks.sh --plan
  preflight_collectors_static_after_luks.sh --preflight
  preflight_collectors_static_after_luks.sh --execute --confirm RUN_USM_COLLECTORS_STATIC_REVIEW

Safety limits: the wrapper does not import or run collectors, read ~/.config/usm-metrics,
read evidence, load environment tokens, make network/OAuth calls, write evidence, start
Docker/OmniRoute, or create schedules. The --execute mode runs only an AST/text parser.
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

printf 'USM collectors static review after LUKS\n'
printf 'mode=%s\n' "$MODE"
printf 'collector_execution=prohibited\n'
printf 'private_config_and_token_read=prohibited\n'
printf 'network_oauth_and_scheduler=prohibited\n'

if [ "$MODE" = 'plan' ]; then
  usage
  exit 0
fi

[ -d "$REPO_ROOT/.git" ] || die 'canonical GitHub repository clone is absent'
command -v python3 >/dev/null 2>&1 || die 'python3 is required'
readonly REVIEWER="$REPO_ROOT/Operations/Automation/validate_collectors_static_contract.py"
[ -f "$REVIEWER" ] || die 'static collector reviewer is absent'

for source in \
  fetch_tiktok_official_metrics.py \
  fetch_youtube_official_metrics.py \
  fetch_facebook_official_metrics.py \
  fetch_instagram_official_metrics.py \
  validate_meta_local_readonly.py \
  official_metrics_requirements.txt \
  official_metrics_config.example.json; do
  [ -f "$REPO_ROOT/Operations/Automation/$source" ] || die "required public artifact is absent: $source"
done

printf 'python=%s\n' "$(python3 --version 2>&1)"
printf 'repo_commit=%s\n' "$(git -C "$REPO_ROOT" log -1 --format=%h)"
printf 'public_artifacts=present\n'

if [ "$MODE" = 'preflight' ]; then
  echo 'STATUS=preflight_complete_static_only_no_private_read_no_network'
  exit 0
fi

[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$CONFIRM" = "$CONFIRMATION" ] || die 'exact --confirm string is required'
cd "$REPO_ROOT/Operations/Automation"
PYTHONDONTWRITEBYTECODE=1 python3 -B validate_collectors_static_contract.py
echo 'STATUS=collectors_static_review_complete_no_private_read_no_network'
