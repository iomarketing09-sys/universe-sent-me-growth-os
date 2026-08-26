#!/usr/bin/env bash
# Restores the one approved USM ciphertext only after a separate human approval.
# The default --plan and --dry-run modes never call age --decrypt or create data.

set -euo pipefail
umask 077

readonly REQUIRED_CONFIRMATION='RUN_CONTROLLED_USM_RESTORE'
MODE='plan'
TARGET_MOUNT=''
BACKUP_STAMP=''
CONFIRMATION=''
ACKNOWLEDGE_PLAINTEXT='false'
RESTORE_ROOT=''

usage() {
  cat <<'EOF'
Usage:
  validate_usm_restore_controlled.sh --plan
  validate_usm_restore_controlled.sh --dry-run --target-mount /run/media/$USER/Fernando \
    --backup-stamp YYYYMMDDTHHMMSSZ
  validate_usm_restore_controlled.sh --execute --target-mount /run/media/$USER/Fernando \
    --backup-stamp YYYYMMDDTHHMMSSZ --acknowledge-temporary-plaintext \
    --confirm RUN_CONTROLLED_USM_RESTORE

Safety contract:
  - --plan and --dry-run do not decrypt, create temporary data, or write evidence.
  - --execute requires a separate approval because restored private data exists
    temporarily on the current unencrypted Xubuntu filesystem.
  - The temporary path is removed on normal completion and on shell exit, but
    this is filesystem-path cleanup, not a secure-erase guarantee.
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

cleanup_restore_root() {
  if [ -n "$RESTORE_ROOT" ] && [ -d "$RESTORE_ROOT" ]; then
    rm -rf -- "$RESTORE_ROOT" || true
  fi
}
trap cleanup_restore_root EXIT

while [ "$#" -gt 0 ]; do
  case "$1" in
    --plan) MODE='plan' ;;
    --dry-run) MODE='dry-run' ;;
    --execute) MODE='execute' ;;
    --target-mount)
      shift
      [ "$#" -gt 0 ] || die '--target-mount requires a path'
      TARGET_MOUNT="$1"
      ;;
    --backup-stamp)
      shift
      [ "$#" -gt 0 ] || die '--backup-stamp requires a UTC stamp'
      BACKUP_STAMP="$1"
      ;;
    --acknowledge-temporary-plaintext) ACKNOWLEDGE_PLAINTEXT='true' ;;
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
STATUS=plan_only_no_decrypt_no_temp_data_no_external_writes
required_before_execute=separate_G-SEC-1A.3g_approval
temporary_restore_location=$HOME/.config/.usm-restore-validation.<stamp>.XXXXXX
cleanup_limit=path_removal_only_not_secure_erase
EOF
  exit 0
fi

[ -n "$TARGET_MOUNT" ] || die '--target-mount is required'
[ -n "$BACKUP_STAMP" ] || die '--backup-stamp is required'
case "$BACKUP_STAMP" in
  ????-??-??*) die 'backup stamp must be compact UTC format YYYYMMDDTHHMMSSZ' ;;
esac
[ -d "$TARGET_MOUNT" ] || die 'target mount directory does not exist'
mountpoint -q "$TARGET_MOUNT" || die 'target must be a mounted volume root'

readonly TARGET_SOURCE="$(findmnt -T "$TARGET_MOUNT" -no SOURCE)"
readonly TARGET_FSTYPE="$(findmnt -T "$TARGET_MOUNT" -no FSTYPE)"
readonly TARGET_LABEL="$(lsblk -no LABEL "$TARGET_SOURCE" 2>/dev/null | head -n 1 | tr -d '[:space:]')"
[ "$TARGET_SOURCE" = '/dev/sdc3' ] || die "expected approved source /dev/sdc3, found: $TARGET_SOURCE"
[ "$TARGET_FSTYPE" = 'vfat' ] || die "expected vfat target, found: $TARGET_FSTYPE"
[ "$TARGET_LABEL" = 'Fernando' ] || die "expected target label Fernando, found: ${TARGET_LABEL:-unset}"
command -v age >/dev/null 2>&1 || die 'age is not available'
command -v tar >/dev/null 2>&1 || die 'tar is not available'
command -v sha256sum >/dev/null 2>&1 || die 'sha256sum is not available'

readonly BACKUP_ROOT="$TARGET_MOUNT/USM_PRE_LUKS_BACKUP"
readonly PROTOCOL="$BACKUP_ROOT/00_PROTOCOL/BACKUP_PROTOCOL_v1.txt"
readonly CIPHERTEXT_NAME="usm_pre_luks_${BACKUP_STAMP}.tar.gz.age"
readonly CIPHERTEXT="$BACKUP_ROOT/10_CIPHERTEXT/$CIPHERTEXT_NAME"
readonly MANIFEST="$BACKUP_ROOT/20_MANIFEST/usm_pre_luks_${BACKUP_STAMP}.manifest.txt"
readonly CHECKSUM="$BACKUP_ROOT/30_INTEGRITY/usm_pre_luks_${BACKUP_STAMP}.sha256"
readonly EVIDENCE="$BACKUP_ROOT/40_RESTORE_EVIDENCE/restore_check_${BACKUP_STAMP}.txt"
readonly VALIDATOR="$(dirname "$0")/validate_usm_restore_tree.py"

for required in "$BACKUP_ROOT" "$PROTOCOL" "$CIPHERTEXT" "$MANIFEST" "$CHECKSUM" "$VALIDATOR"; do
  [ -e "$required" ] || die "required restore artifact is absent"
done
[ ! -e "$EVIDENCE" ] || die 'restore evidence already exists; refusing a second validation'
grep -Fx 'scope_profile=code_scripts_and_approved_private' "$MANIFEST" >/dev/null || die 'manifest scope profile does not match approved scope'
grep -Fx 'restore_status=pending' "$MANIFEST" >/dev/null || die 'manifest restore status is not pending'
sha256sum -c "$CHECKSUM"

printf 'target_source=%s\n' "$TARGET_SOURCE"
printf 'target_fstype=%s\n' "$TARGET_FSTYPE"
printf 'target_label=%s\n' "$TARGET_LABEL"
printf 'ciphertext=%s\n' "$CIPHERTEXT_NAME"

if [ "$MODE" = 'dry-run' ]; then
  printf 'STATUS=restore_dry_run_complete_no_decrypt_no_temp_data_no_external_writes\n'
  exit 0
fi

[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$CONFIRMATION" = "$REQUIRED_CONFIRMATION" ] || die 'exact --confirm string is required'
[ "$ACKNOWLEDGE_PLAINTEXT" = 'true' ] || die '--acknowledge-temporary-plaintext is required'

readonly TEMP_PARENT="$HOME/.config"
[ -d "$TEMP_PARENT" ] || die 'private temporary parent is absent'
RESTORE_ROOT="$(mktemp -d "$TEMP_PARENT/.usm-restore-validation.${BACKUP_STAMP}.XXXXXX")"
chmod 700 "$RESTORE_ROOT"

printf 'age will now request the recovery passphrase interactively.\n'
printf 'Restored private data exists only temporarily under a private local path.\n'
age --decrypt "$CIPHERTEXT" | tar -xzf - -C "$RESTORE_ROOT" --no-same-owner --no-same-permissions
python3 "$VALIDATOR" "$RESTORE_ROOT"
sha256sum -c "$CHECKSUM"

rm -rf -- "$RESTORE_ROOT"
[ ! -e "$RESTORE_ROOT" ] || die 'temporary restore path remains after cleanup'
RESTORE_ROOT=''

{
  printf 'protocol_version=1\n'
  printf 'backup_stamp=%s\n' "$BACKUP_STAMP"
  printf 'ciphertext_file=%s\n' "$CIPHERTEXT_NAME"
  printf 'ciphertext_checksum=verified_ok_before_and_after_restore\n'
  printf 'scope_profile=code_scripts_and_approved_private\n'
  printf 'restored_required_roots_structure=validated\n'
  printf 'temporary_path_cleanup=passed\n'
  printf 'cleanup_limit=path_removal_only_not_secure_erase\n'
  printf 'operator_confirmation=%s\n' "$REQUIRED_CONFIRMATION"
} > "$EVIDENCE"

printf 'STATUS=controlled_restore_validation_passed\n'
printf 'restore_evidence=%s\n' "$EVIDENCE"
