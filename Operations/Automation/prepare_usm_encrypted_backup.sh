#!/usr/bin/env bash
# Design-stage encrypted backup wrapper for the planned Xubuntu-to-LUKS migration.
# Design philosophy for this file: use only the pre-approved external-tree layout,
# stream plaintext directly to ciphertext, and fail closed before any data read.
# Default mode is --plan: it does not create folders, archives, encrypted files,
# keys, checksums, or copies. --execute remains separately gated.

set -euo pipefail
umask 077

readonly REQUIRED_CONFIRMATION='CREATE_ENCRYPTED_USM_BACKUP'
MODE='plan'
TARGET_MOUNT=''
INCLUDE_PRIVATE='false'
CONFIRMATION=''

usage() {
  cat <<'EOF'
Usage:
  prepare_usm_encrypted_backup.sh --plan
  prepare_usm_encrypted_backup.sh --dry-run --target-mount /run/media/$USER/<label>
  prepare_usm_encrypted_backup.sh --execute --target-mount /run/media/$USER/<label> \
    --include-private --confirm CREATE_ENCRYPTED_USM_BACKUP

Modes:
  --plan       Prints the design and safety gates only. Default; no filesystem writes.
  --dry-run    Validates tools, source-root metadata and target mount. No copy or encryption.
  --execute    Creates one encrypted .age archive only after every gate below is approved.

Security rules:
  - The script never accepts a passphrase from command-line arguments or environment variables.
  - age prompts interactively at execution. Do not leave the passphrase blank and do not paste it into chat.
  - The identity/passphrase recovery material must remain outside this disk, Drive, GitHub, email and chat.
  - The three approved private roots are omitted unless --include-private is supplied with the exact confirmation string.
  - --execute only accepts the pre-created USM_PRE_LUKS_BACKUP directory tree.
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

source_metadata() {
  local path="$1"
  if [ -e "$path" ] || [ -L "$path" ]; then
    printf 'SOURCE_PRESENT path=%s type=' "$path"
    stat -c '%F mode=%a owner=%U:%G' "$path" 2>/dev/null || printf 'unknown'
    printf '\n'
  else
    printf 'SOURCE_ABSENT path=%s\n' "$path"
  fi
}

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
    --include-private) INCLUDE_PRIVATE='true' ;;
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

readonly PUBLIC_ROOTS=(
  "$HOME/universe-sent-me-growth-os"
  "$HOME/bin"
)
readonly PRIVATE_ROOTS=(
  "$HOME/.config/usm-metrics"
  "$HOME/.local/share/usm-metrics"
  "$HOME/omniroute-pilot"
)

printf 'USM encrypted migration-backup design\n'
printf 'mode=%s\n' "$MODE"
printf 'public_roots=%s\n' "${#PUBLIC_ROOTS[@]}"
printf 'private_roots_included=%s\n' "$INCLUDE_PRIVATE"

if [ "$MODE" = 'plan' ]; then
  cat <<'EOF'

Pre-created external-tree layout required before --execute:
  <target-mount>/USM_PRE_LUKS_BACKUP/
    00_PROTOCOL/           protocol text without sensitive data
    10_CIPHERTEXT/         encrypted .age archive only
    20_MANIFEST/           non-secret run manifest
    30_INTEGRITY/          SHA-256 of ciphertext only
    40_RESTORE_EVIDENCE/   restore result after a separate approved test

Public/reconstructible roots:
  - ~/universe-sent-me-growth-os
  - ~/bin

Private roots approved for a future ciphertext but excluded unless --include-private:
  - ~/.config/usm-metrics
  - ~/.local/share/usm-metrics
  - ~/omniroute-pilot

Required gates before --execute:
  1. G-SEC-1A.3a created the target tree and G-SEC-1A.3b approved these sources.
  2. age is installed from an approved source and is available on PATH.
  3. Passphrase recovery material is stored outside the external disk, Drive,
     GitHub, email, chat and the archive.
  4. A non-sensitive restoration test procedure is approved.
  5. The target mount is the intended external vfat volume, not Xubuntu root.
EOF
  exit 0
fi

[ -n "$TARGET_MOUNT" ] || die '--target-mount is required for dry-run or execute'
[ -d "$TARGET_MOUNT" ] || die 'target mount directory does not exist'
mountpoint -q "$TARGET_MOUNT" || die 'target must be an existing mount point, not a subdirectory'

printf 'target_mount=%s\n' "$TARGET_MOUNT"
findmnt -T "$TARGET_MOUNT" -no SOURCE,FSTYPE,SIZE,AVAIL,USE% || die 'cannot resolve target mount metadata'

printf '\nPublic source metadata:\n'
for root in "${PUBLIC_ROOTS[@]}"; do source_metadata "$root"; done
printf '\nPrivate source metadata:\n'
for root in "${PRIVATE_ROOTS[@]}"; do source_metadata "$root"; done

if [ "$MODE" = 'dry-run' ]; then
  readonly DRY_RUN_BACKUP_ROOT="$TARGET_MOUNT/USM_PRE_LUKS_BACKUP"
  readonly DRY_RUN_DIRS=(
    "$DRY_RUN_BACKUP_ROOT/00_PROTOCOL"
    "$DRY_RUN_BACKUP_ROOT/10_CIPHERTEXT"
    "$DRY_RUN_BACKUP_ROOT/20_MANIFEST"
    "$DRY_RUN_BACKUP_ROOT/30_INTEGRITY"
    "$DRY_RUN_BACKUP_ROOT/40_RESTORE_EVIDENCE"
  )
  [ -d "$DRY_RUN_BACKUP_ROOT" ] || die 'approved USM_PRE_LUKS_BACKUP tree is absent'
  for dir in "${DRY_RUN_DIRS[@]}"; do
    [ -d "$dir" ] || die "required approved directory is absent: $dir"
  done
  if command -v age >/dev/null 2>&1; then
    printf 'age_available=%s\n' "$(command -v age)"
    age --version 2>/dev/null || true
  else
    printf 'age_available=NO\n'
  fi
  printf 'STATUS=dry_run_complete_no_files_created\n'
  exit 0
fi

[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$INCLUDE_PRIVATE" = 'true' ] || die '--execute requires --include-private after approval'
[ "$CONFIRMATION" = "$REQUIRED_CONFIRMATION" ] || die 'exact --confirm string is required'
command -v age >/dev/null 2>&1 || die 'age is required but not installed'

for root in "${PUBLIC_ROOTS[@]}" "${PRIVATE_ROOTS[@]}"; do
  [ -e "$root" ] || die "approved source root absent: $root"
done

readonly RUN_DATE="$(date -u +%Y%m%dT%H%M%SZ)"
readonly BACKUP_ROOT="$TARGET_MOUNT/USM_PRE_LUKS_BACKUP"
readonly PROTOCOL_DIR="$BACKUP_ROOT/00_PROTOCOL"
readonly ARCHIVE_DIR="$BACKUP_ROOT/10_CIPHERTEXT"
readonly MANIFEST_DIR="$BACKUP_ROOT/20_MANIFEST"
readonly CHECKSUM_DIR="$BACKUP_ROOT/30_INTEGRITY"
readonly RESTORE_EVIDENCE_DIR="$BACKUP_ROOT/40_RESTORE_EVIDENCE"
readonly REQUIRED_BACKUP_DIRS=(
  "$PROTOCOL_DIR"
  "$ARCHIVE_DIR"
  "$MANIFEST_DIR"
  "$CHECKSUM_DIR"
  "$RESTORE_EVIDENCE_DIR"
)
readonly PROTOCOL="$PROTOCOL_DIR/BACKUP_PROTOCOL_v1.txt"
readonly ARCHIVE_NAME="usm_pre_luks_${RUN_DATE}.tar.gz.age"
readonly TEMP_ARCHIVE="$ARCHIVE_DIR/.${ARCHIVE_NAME}.partial"
readonly FINAL_ARCHIVE="$ARCHIVE_DIR/$ARCHIVE_NAME"
readonly MANIFEST="$MANIFEST_DIR/usm_pre_luks_${RUN_DATE}.manifest.txt"
readonly CHECKSUM="$CHECKSUM_DIR/usm_pre_luks_${RUN_DATE}.sha256"

[ -d "$BACKUP_ROOT" ] || die 'approved USM_PRE_LUKS_BACKUP tree is absent'
for dir in "${REQUIRED_BACKUP_DIRS[@]}"; do
  [ -d "$dir" ] || die "required approved directory is absent: $dir"
  [ -z "$(find "$dir" -mindepth 1 -maxdepth 1 -print -quit)" ] || die "required directory is not empty: $dir"
done
BACKUP_COMPLETE='false'
cleanup_failed_backup() {
  if [ "$BACKUP_COMPLETE" != 'true' ]; then
    rm -f "$TEMP_ARCHIVE" "$FINAL_ARCHIVE" "$CHECKSUM" "$MANIFEST" "$PROTOCOL"
  fi
}
trap cleanup_failed_backup EXIT

printf 'age will now request a passphrase interactively. Do not leave it blank.\n'
printf 'Streaming archive directly into ciphertext; no plaintext archive file is created.\n'
tar -C "$HOME" -czf - \
  universe-sent-me-growth-os \
  bin \
  .config/usm-metrics \
  .local/share/usm-metrics \
  omniroute-pilot \
  | age --passphrase -o "$TEMP_ARCHIVE"

mv -f "$TEMP_ARCHIVE" "$FINAL_ARCHIVE"
sha256sum "$FINAL_ARCHIVE" > "$CHECKSUM"
{
  printf 'protocol_version=1\n'
  printf 'backup_type=usm_pre_luks_encrypted\n'
  printf 'encryption=age_passphrase_interactive\n'
  printf 'ciphertext_only_on_external_vfat=true\n'
  printf 'restore_evidence=required_before_luks_migration\n'
} > "$PROTOCOL"
{
  printf 'backup_type=usm_pre_luks_encrypted\n'
  printf 'protocol_version=1\n'
  printf 'created_utc=%s\n' "$RUN_DATE"
  printf 'ciphertext_file=%s\n' "$ARCHIVE_NAME"
  printf 'ciphertext_sha256_file=%s\n' "$(basename "$CHECKSUM")"
  printf 'encryption=age_passphrase_interactive\n'
  printf 'scope_profile=code_scripts_and_approved_private\n'
  printf 'restore_status=pending\n'
  printf 'operator_confirmation=%s\n' "$REQUIRED_CONFIRMATION"
} > "$MANIFEST"

BACKUP_COMPLETE='true'
trap - EXIT
printf 'STATUS=encrypted_backup_created\n'
printf 'ciphertext=%s\n' "$FINAL_ARCHIVE"
printf 'protocol=%s\n' "$PROTOCOL"
printf 'manifest=%s\n' "$MANIFEST"
printf 'checksum=%s\n' "$CHECKSUM"
