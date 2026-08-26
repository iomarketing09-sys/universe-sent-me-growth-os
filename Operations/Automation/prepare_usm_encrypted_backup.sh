#!/usr/bin/env bash
# Design-stage encrypted backup wrapper for the planned Xubuntu-to-LUKS migration.
# Default mode is --plan: it does not create folders, archives, encrypted files,
# keys, checksums, or copies. --execute is intentionally gated and must be
# approved separately after a non-sensitive restoration test plan exists.

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
  - Private roots are omitted unless --include-private is supplied with the exact confirmation string.
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

Folder layout created only by --execute after separate approval:
  <target-mount>/USM_PRE_LUKS_BACKUP/
    archives/      encrypted .age archives only
    manifests/     non-secret run manifest
    checksums/     SHA-256 of ciphertext only

Public/reconstructible roots:
  - ~/universe-sent-me-growth-os
  - ~/bin

Private roots, excluded by default:
  - ~/.config/usm-metrics
  - ~/.local/share/usm-metrics
  - ~/omniroute-pilot

Required gates before --execute:
  1. G-SEC-1A.3 approves target folder and source categories.
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
readonly ARCHIVE_DIR="$BACKUP_ROOT/archives"
readonly MANIFEST_DIR="$BACKUP_ROOT/manifests"
readonly CHECKSUM_DIR="$BACKUP_ROOT/checksums"
readonly ARCHIVE_NAME="usm_pre_luks_${RUN_DATE}.tar.gz.age"
readonly TEMP_ARCHIVE="$ARCHIVE_DIR/.${ARCHIVE_NAME}.partial"
readonly FINAL_ARCHIVE="$ARCHIVE_DIR/$ARCHIVE_NAME"
readonly MANIFEST="$MANIFEST_DIR/usm_pre_luks_${RUN_DATE}.manifest.txt"
readonly CHECKSUM="$CHECKSUM_DIR/usm_pre_luks_${RUN_DATE}.sha256"

mkdir -p "$ARCHIVE_DIR" "$MANIFEST_DIR" "$CHECKSUM_DIR"
trap 'rm -f "$TEMP_ARCHIVE"' EXIT

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
  printf 'backup_type=usm_pre_luks_encrypted\n'
  printf 'created_utc=%s\n' "$RUN_DATE"
  printf 'ciphertext_file=%s\n' "$ARCHIVE_NAME"
  printf 'ciphertext_sha256_file=%s\n' "$(basename "$CHECKSUM")"
  printf 'encryption=age_passphrase_interactive\n'
  printf 'sources=public_roots_plus_approved_private_roots\n'
  printf 'restore_gate=required_before_luks_migration\n'
} > "$MANIFEST"

if command -v age-inspect >/dev/null 2>&1; then
  age-inspect "$FINAL_ARCHIVE" > "$MANIFEST_DIR/usm_pre_luks_${RUN_DATE}.age-inspect.txt"
fi

trap - EXIT
printf 'STATUS=encrypted_backup_created\n'
printf 'ciphertext=%s\n' "$FINAL_ARCHIVE"
printf 'manifest=%s\n' "$MANIFEST"
printf 'checksum=%s\n' "$CHECKSUM"
