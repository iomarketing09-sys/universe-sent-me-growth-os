#!/usr/bin/env bash
# Read-only inspector for candidate external backup media before LUKS migration.
# It never mounts, unmounts, repairs, formats, writes, copies, or deletes data.

set -euo pipefail
export LC_ALL=C

section() {
  printf '\n===== %s =====\n' "$1"
}

section 'SAFE READ-ONLY SCOPE'
cat <<'EOF'
This inspection reads only block-device and mount metadata. It does not read
file contents, copy data, create folders, mount/unmount devices, repair file
systems, format media, or expose secrets. Review the output before sharing.
EOF

section 'ALL BLOCK DEVICES'
lsblk -o NAME,TRAN,TYPE,FSTYPE,LABEL,SIZE,FSAVAIL,FSUSE%,MOUNTPOINTS,MODEL

section 'MOUNTED FILESYSTEMS'
findmnt -r -o SOURCE,TARGET,FSTYPE,OPTIONS,SIZE,AVAIL,USE% || true

section 'REMOVABLE MEDIA MOUNT CANDIDATES'
if [ -d "/media/$USER" ]; then
  findmnt -rn -o SOURCE,TARGET,FSTYPE,SIZE,AVAIL,USE% \
    | awk -v prefix="/media/$USER/" '$2 ~ "^" prefix {print}' || true
else
  printf 'NO_MEDIA_DIRECTORY_FOR_CURRENT_USER\n'
fi

if [ -d "/run/media/$USER" ]; then
  findmnt -rn -o SOURCE,TARGET,FSTYPE,SIZE,AVAIL,USE% \
    | awk -v prefix="/run/media/$USER/" '$2 ~ "^" prefix {print}' || true
fi

section 'ASSESSMENT REMINDERS'
cat <<'EOF'
- A 28.8 GB USB is below the 36 GB logical-backup target and must not be the
  only pre-LUKS backup medium.
- A disk with at least 128 GB free may be a candidate only after confirming
  its filesystem, free space, mount status, and that its existing Windows data
  will not be altered.
- Do not run formatting, partitioning, chkdsk, fsck, mount-repair, copy, or
  encryption commands at this stage.
EOF

section 'END OF READ-ONLY INSPECTION'
printf 'STATUS=external_media_metadata_only_complete\n'
