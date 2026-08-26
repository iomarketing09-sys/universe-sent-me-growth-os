#!/usr/bin/env bash
# Fictitious-only age round-trip validator. It never reads USM paths or media.
# Usage: validate_age_fictitious_roundtrip.sh /absolute/path/to/age/bin

set -euo pipefail
umask 077

[ "$#" -eq 1 ] || {
  printf 'USAGE: %s /absolute/path/to/age/bin\n' "$0" >&2
  exit 2
}

readonly AGE_BIN="$1"
readonly AGE_KEYGEN_BIN="$(dirname "$AGE_BIN")/age-keygen"

[ -x "$AGE_BIN" ] || {
  printf 'ERROR: age binary is not executable\n' >&2
  exit 2
}
[ -x "$AGE_KEYGEN_BIN" ] || {
  printf 'ERROR: age-keygen binary is not executable\n' >&2
  exit 2
}

readonly TEMP_ROOT="$(mktemp -d /tmp/usm-age-fictitious.XXXXXX)"
cleanup() {
  rm -rf "$TEMP_ROOT"
  printf 'TEMP_ROOT_REMOVED=%s\n' "$TEMP_ROOT"
}
trap cleanup EXIT

printf 'TEMP_ROOT=%s\n' "$TEMP_ROOT"
printf '%s\n' \
  'USM fictitious backup rehearsal' \
  'record_type=synthetic' \
  'purpose=pre_luks_restore_validation' \
  > "$TEMP_ROOT/fixture.txt"

"$AGE_KEYGEN_BIN" -o "$TEMP_ROOT/identity.txt" >/dev/null
"$AGE_KEYGEN_BIN" -y "$TEMP_ROOT/identity.txt" > "$TEMP_ROOT/recipient.txt"
"$AGE_BIN" -R "$TEMP_ROOT/recipient.txt" -o "$TEMP_ROOT/fixture.txt.age" "$TEMP_ROOT/fixture.txt"
"$AGE_BIN" -d -i "$TEMP_ROOT/identity.txt" -o "$TEMP_ROOT/restored.txt" "$TEMP_ROOT/fixture.txt.age"

cmp -s "$TEMP_ROOT/fixture.txt" "$TEMP_ROOT/restored.txt"
SOURCE_SHA256="$(sha256sum "$TEMP_ROOT/fixture.txt" | awk '{print $1}')"
RESTORED_SHA256="$(sha256sum "$TEMP_ROOT/restored.txt" | awk '{print $1}')"
CIPHERTEXT_BYTES="$(stat -c '%s' "$TEMP_ROOT/fixture.txt.age")"

[ "$SOURCE_SHA256" = "$RESTORED_SHA256" ]
[ "$CIPHERTEXT_BYTES" -gt 0 ]

printf 'source_sha256=%s\n' "$SOURCE_SHA256"
printf 'restored_sha256=%s\n' "$RESTORED_SHA256"
printf 'ciphertext_bytes=%s\n' "$CIPHERTEXT_BYTES"
printf 'fixture_roundtrip=passed\n'
