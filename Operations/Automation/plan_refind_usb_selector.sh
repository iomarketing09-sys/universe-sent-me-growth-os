#!/usr/bin/env bash
# USM rEFInd Plan B — read-only preflight.
# Design reminder: inspect only; never install packages, modify EFI/NVRAM, mount media, or write disk state.
set -euo pipefail

readonly MODE="${1:---plan}"
readonly ESP_MOUNT="/boot/efi"
readonly REFIND_PACKAGE="refind"

usage() {
  cat <<'EOF'
Usage: plan_refind_usb_selector.sh --plan

This wrapper only reads local state. It never installs rEFInd, writes the ESP,
creates or deletes UEFI entries, changes BootOrder, mounts devices, or changes disks.
EOF
}

if [[ "$MODE" != "--plan" ]]; then
  usage >&2
  echo "STATUS=blocked_only_plan_is_allowed" >&2
  exit 64
fi

echo "USM rEFInd Plan B — read-only preflight"
echo "mode=plan"
echo "writes=none"
echo

if ! findmnt -n --target "$ESP_MOUNT" >/dev/null 2>&1; then
  echo "ESP_STATUS=not_mounted"
  echo "STATUS=blocked_esp_not_mounted"
  exit 1
fi

esp_source="$(findmnt -n -o SOURCE --target "$ESP_MOUNT")"
esp_fstype="$(findmnt -n -o FSTYPE --target "$ESP_MOUNT")"
echo "esp_mount=$ESP_MOUNT"
echo "esp_source=$esp_source"
echo "esp_fstype=$esp_fstype"

if [[ "$esp_fstype" != "vfat" ]]; then
  echo "STATUS=blocked_esp_fstype_not_vfat"
  exit 1
fi

df -h "$ESP_MOUNT"
echo
echo "--- EFI DIRECTORIES ---"
find "$ESP_MOUNT/EFI" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort

if [[ -d "$ESP_MOUNT/EFI/ubuntu" ]]; then
  echo "ubuntu_loader_directory=present"
else
  echo "ubuntu_loader_directory=missing"
  echo "STATUS=blocked_ubuntu_loader_missing"
  exit 1
fi

if [[ -d "$ESP_MOUNT/EFI/refind" ]]; then
  echo "refind_directory=already_present"
else
  echo "refind_directory=absent"
fi

echo
echo "--- PACKAGE CANDIDATE ---"
apt-cache policy "$REFIND_PACKAGE"

echo
echo "--- SECURE BOOT ---"
if command -v mokutil >/dev/null 2>&1; then
  mokutil --sb-state || true
else
  echo "MOKUTIL_NOT_INSTALLED"
fi

echo
echo "--- UEFI STATE (READ-ONLY; MAY REQUEST LOCAL SUDO PASSWORD) ---"
if command -v efibootmgr >/dev/null 2>&1; then
  sudo efibootmgr -v
else
  echo "EFIBOOTMGR_NOT_INSTALLED"
fi

echo
echo "STATUS=plan_complete_no_esp_nvrmam_or_package_changes"
