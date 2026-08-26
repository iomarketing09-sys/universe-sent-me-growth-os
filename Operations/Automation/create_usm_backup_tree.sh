#!/usr/bin/env bash
# Creates only the approved empty USM_PRE_LUKS_BACKUP directory tree.
# Default is --plan. --execute requires the exact confirmation string.

set -euo pipefail
umask 077

readonly REQUIRED_CONFIRMATION='CREATE_EMPTY_USM_BACKUP_TREE'
MODE='plan'
TARGET_MOUNT=''
CONFIRMATION=''

usage() {
  cat <<'EOF'
Usage:
  create_usm_backup_tree.sh --plan --target-mount /run/media/$USER/Fernando
  create_usm_backup_tree.sh --execute --target-mount /run/media/$USER/Fernando \
    --confirm CREATE_EMPTY_USM_BACKUP_TREE

This wrapper creates directories only. It never copies, encrypts, reads private
USM data, deletes files, formats media, changes mounts, or modifies existing
files on the external disk.
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --plan) MODE='plan' ;;
    --execute) MODE='execute' ;;
    --target-mount)
      shift
      [ "$#" -gt 0 ] || die '--target-mount requires a path'
      TARGET_MOUNT="$1"
      ;;
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

[ -n "$TARGET_MOUNT" ] || die '--target-mount is required'
[ -d "$TARGET_MOUNT" ] || die 'target mount directory does not exist'
mountpoint -q "$TARGET_MOUNT" || die 'target must be the mounted volume root'

readonly FSTYPE="$(findmnt -T "$TARGET_MOUNT" -no FSTYPE)"
readonly SOURCE="$(findmnt -T "$TARGET_MOUNT" -no SOURCE)"
[ "$FSTYPE" = 'vfat' ] || die "expected vfat target, found: $FSTYPE"
[ "$SOURCE" != '/' ] || die 'refusing to operate on the Xubuntu root filesystem'

readonly BACKUP_ROOT="$TARGET_MOUNT/USM_PRE_LUKS_BACKUP"
readonly REQUIRED_DIRS=(
  '00_PROTOCOL'
  '10_CIPHERTEXT'
  '20_MANIFEST'
  '30_INTEGRITY'
  '40_RESTORE_EVIDENCE'
)

printf 'mode=%s\n' "$MODE"
printf 'target_mount=%s\n' "$TARGET_MOUNT"
printf 'source=%s\n' "$SOURCE"
printf 'fstype=%s\n' "$FSTYPE"
printf 'backup_root=%s\n' "$BACKUP_ROOT"
printf 'directories=%s\n' "${REQUIRED_DIRS[*]}"

if [ "$MODE" = 'plan' ]; then
  printf 'STATUS=plan_only_no_directories_created\n'
  exit 0
fi

[ "$MODE" = 'execute' ] || die 'invalid mode'
[ "$CONFIRMATION" = "$REQUIRED_CONFIRMATION" ] || die 'exact --confirm string is required'

if [ -e "$BACKUP_ROOT" ]; then
  die 'USM_PRE_LUKS_BACKUP already exists; refusing to alter any existing structure'
fi

mkdir "$BACKUP_ROOT"
for dir in "${REQUIRED_DIRS[@]}"; do
  mkdir "$BACKUP_ROOT/$dir"
done

printf 'STATUS=empty_tree_created\n'
find "$BACKUP_ROOT" -mindepth 0 -maxdepth 1 -type d -printf '%f\n' | sort
