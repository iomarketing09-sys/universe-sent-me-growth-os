#!/usr/bin/env bash
# USM post-LUKS selective restoration wrapper.
# Design reminder: preserve GitHub's repository clone as canonical, restore only approved private roots into LUKS, and never write to Fernando.
set -euo pipefail
umask 077

readonly CONFIRMATION='RESTORE_USM_TO_LUKS'
readonly BACKUP_STAMP='20260826T042149Z'
MODE='plan'
TARGET_MOUNT=''
CONFIRM=''

usage() {
  cat <<'EOF'
Usage:
  restore_usm_post_luks_selective.sh --plan
  restore_usm_post_luks_selective.sh --preflight --target-mount /run/media/$USER/Fernando
  restore_usm_post_luks_selective.sh --execute --target-mount /run/media/$USER/Fernando \
    --confirm RESTORE_USM_TO_LUKS

Safety rules:
  - --plan is the default and does not read the external disk.
  - --preflight verifies ciphertext integrity without decrypting or writing.
  - --execute decrypts only after separate authorization and interactive local passphrase entry.
  - The current GitHub clone is never restored from the older archive.
  - Existing destination roots cause a hard failure; this wrapper never overwrites them.
EOF
}

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    --plan) MODE='plan' ;;
    --preflight) MODE='preflight' ;;
    --execute) MODE='execute' ;;
    --target-mount)
      shift
      [ "$#" -gt 0 ] || die '--target-mount requires a path'
      TARGET_MOUNT="$1"
      ;;
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

printf 'USM post-LUKS selective restoration\n'
printf 'mode=%s\n' "$MODE"
printf 'archive_repository_restore=disabled_github_is_canonical\n'

if [ "$MODE" = 'plan' ]; then
  usage
  exit 0
fi

[ -n "$TARGET_MOUNT" ] || die '--target-mount is required'
[ -d "$TARGET_MOUNT" ] || die 'target mount directory does not exist'
mountpoint -q "$TARGET_MOUNT" || die 'target must be a mount point'

readonly TARGET_SOURCE="$(findmnt -T "$TARGET_MOUNT" -no SOURCE)"
readonly TARGET_FSTYPE="$(findmnt -T "$TARGET_MOUNT" -no FSTYPE)"
readonly TARGET_LABEL="$(lsblk -no LABEL "$TARGET_SOURCE" 2>/dev/null | head -n 1 | tr -d '[:space:]')"
[ "$TARGET_FSTYPE" = 'vfat' ] || die "expected vfat target, found: $TARGET_FSTYPE"
[ "$TARGET_LABEL" = 'Fernando' ] || die "expected target label Fernando, found: ${TARGET_LABEL:-unset}"

readonly BACKUP_ROOT="$TARGET_MOUNT/USM_PRE_LUKS_BACKUP"
readonly CIPHER="$BACKUP_ROOT/10_CIPHERTEXT/usm_pre_luks_${BACKUP_STAMP}.tar.gz.age"
readonly CHECKSUM="$BACKUP_ROOT/30_INTEGRITY/usm_pre_luks_${BACKUP_STAMP}.sha256"
readonly MANIFEST="$BACKUP_ROOT/20_MANIFEST/usm_pre_luks_${BACKUP_STAMP}.manifest.txt"
readonly REQUIRED_ROOTS=(
  "$HOME/bin"
  "$HOME/.config/usm-metrics"
  "$HOME/.local/share/usm-metrics"
  "$HOME/omniroute-pilot"
)

[ -f "$CIPHER" ] || die 'ciphertext is absent'
[ -f "$CHECKSUM" ] || die 'checksum file is absent'
[ -f "$MANIFEST" ] || die 'manifest is absent'
[ -d "$HOME/universe-sent-me-growth-os/.git" ] || die 'current GitHub repository clone is required'
command -v age >/dev/null 2>&1 || die 'age is required'
command -v tar >/dev/null 2>&1 || die 'tar is required'
command -v sha256sum >/dev/null 2>&1 || die 'sha256sum is required'
grep -qx 'scope_profile=code_scripts_and_approved_private' "$MANIFEST" || die 'unexpected archive scope profile'

printf 'target_source=%s\n' "$TARGET_SOURCE"
printf 'target_fstype=%s\n' "$TARGET_FSTYPE"
printf 'target_label=%s\n' "$TARGET_LABEL"
sha256sum -c "$CHECKSUM"

if [ "$MODE" = 'preflight' ]; then
  printf 'STATUS=preflight_complete_no_decrypt_no_restore_no_external_writes\n'
  exit 0
fi

[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$CONFIRM" = "$CONFIRMATION" ] || die 'exact --confirm string is required'

for root in "${REQUIRED_ROOTS[@]}"; do
  [ ! -e "$root" ] || die "destination already exists: $root"
done

readonly STAGE="$(mktemp -d "$HOME/.config/.usm-postluks-restore.${BACKUP_STAMP}.XXXXXX")"
cleanup() { rm -rf -- "$STAGE"; }
trap cleanup EXIT

printf 'age will now request the passphrase interactively.\n'
age -d "$CIPHER" | tar -xzf - -C "$STAGE" --no-same-owner --no-same-permissions \
  bin .config/usm-metrics .local/share/usm-metrics omniroute-pilot

for path in \
  "$STAGE/bin" \
  "$STAGE/.config/usm-metrics" \
  "$STAGE/.local/share/usm-metrics" \
  "$STAGE/omniroute-pilot"; do
  [ -d "$path" ] || die "expected restored path is absent: $path"
done

sha256sum -c "$CHECKSUM"
install -d -m 700 "$HOME/.config" "$HOME/.local" "$HOME/.local/share"
mv "$STAGE/bin" "$HOME/bin"
mv "$STAGE/.config/usm-metrics" "$HOME/.config/usm-metrics"
mv "$STAGE/.local/share/usm-metrics" "$HOME/.local/share/usm-metrics"
mv "$STAGE/omniroute-pilot" "$HOME/omniroute-pilot"

printf 'STATUS=selective_restore_complete_repository_preserved\n'
