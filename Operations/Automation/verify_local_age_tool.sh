#!/usr/bin/env bash
# Design philosophy for this file: verify the encryption tool only; never read
# USM roots, touch the external backup tree, request a passphrase, or create data.

set -euo pipefail

readonly REQUIRED_CONFIRMATION='INSTALL_AND_VERIFY_AGE'
MODE='plan'
CONFIRMATION=''

usage() {
  cat <<'EOF'
Usage:
  verify_local_age_tool.sh --plan
  verify_local_age_tool.sh --install-and-verify --confirm INSTALL_AND_VERIFY_AGE

The script only checks or installs the Ubuntu `age` package from configured
system repositories, then prints its executable path and version. It never
reads USM data, accesses the external backup disk, asks for a passphrase,
creates ciphertext, or calls a remote backup service.
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --plan) MODE='plan' ;;
    --install-and-verify) MODE='install-and-verify' ;;
    --confirm)
      shift
      [ "$#" -gt 0 ] || die '--confirm requires the exact confirmation string'
      CONFIRMATION="$1"
      ;;
    --help|-h) usage; exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
  shift
done

printf 'mode=%s\n' "$MODE"
if [ "$MODE" = 'plan' ]; then
  cat <<'EOF'
STATUS=plan_only_no_package_changes
planned_source=Ubuntu configured system repositories
planned_actions=check_or_install_age_then_print_path_and_version
prohibited=USM_data_external_disk_passphrase_ciphertext_remote_backup
EOF
  exit 0
fi

[ "$MODE" = 'install-and-verify' ] || die 'invalid mode'
[ "$CONFIRMATION" = "$REQUIRED_CONFIRMATION" ] || die 'exact --confirm string is required'

if ! command -v age >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y age
fi

readonly AGE_PATH="$(command -v age)"
readonly AGE_VERSION="$(age --version 2>&1)"
readonly PACKAGE_VERSION="$(dpkg-query -W -f='${Version}' age 2>/dev/null || printf 'not_reported')"

printf 'age_path=%s\n' "$AGE_PATH"
printf 'age_version=%s\n' "$AGE_VERSION"
printf 'package_version=%s\n' "$PACKAGE_VERSION"
printf 'STATUS=age_available_no_usm_data_processed\n'
