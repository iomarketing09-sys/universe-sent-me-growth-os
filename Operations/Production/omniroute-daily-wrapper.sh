#!/usr/bin/env bash
# Uso diario seguro de OmniRoute local con Groq.
# No guarda la API key, el prompt ni la respuesta después de terminar.

set -Eeuo pipefail

usage() {
  cat <<'USAGE'
Uso:
  omniroute-daily-wrapper.sh             Prompt de una sola línea.
  omniroute-daily-wrapper.sh --multiline Prompt de varias líneas; termina escribiendo FIN en una línea separada.
  omniroute-daily-wrapper.sh --help      Mostrar esta ayuda.
USAGE
}

PROMPT_MODE="single"
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --multiline)
      PROMPT_MODE="multiline"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf 'Opción no reconocida: %s\n\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

ENDPOINT="${OMNIROUTE_URL:-http://127.0.0.1:20128/v1/chat/completions}"
MODEL="${OMNIROUTE_MODEL:-groq/openai/gpt-oss-20b}"
MAX_TOKENS="${OMNIROUTE_MAX_TOKENS:-400}"
TEMPERATURE="${OMNIROUTE_TEMPERATURE:-0.4}"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/omniroute-wrapper.XXXXXX")"
PAYLOAD_FILE="$TMP_DIR/payload.json"
HEADERS_FILE="$TMP_DIR/headers.txt"
RESPONSE_FILE="$TMP_DIR/response.json"

cleanup() {
  unset OMNIROUTE_API_KEY PROMPT PAYLOAD_FILE RESPONSE_FILE HEADERS_FILE
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT HUP INT TERM

if ! command -v curl >/dev/null 2>&1; then
  printf 'Error: curl no está instalado.\n' >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf 'Error: python3 no está instalado.\n' >&2
  exit 1
fi

printf 'Endpoint local: %s\n' "$ENDPOINT"
printf 'Modelo: %s\n\n' "$MODEL"

if [[ "$PROMPT_MODE" == "multiline" ]]; then
  printf '%s\n' 'Escribe el prompt. Cuando termines, escribe únicamente FIN en una línea separada:'
  PROMPT=""
  while IFS= read -r line; do
    if [[ "$line" == "FIN" ]]; then
      break
    fi
    if [[ -n "$PROMPT" ]]; then
      PROMPT+=$'\n'
    fi
    PROMPT+="$line"
  done
else
  read -r -p 'Prompt sintético o anonimizado: ' PROMPT
fi

if [[ -z "${PROMPT//[[:space:]]/}" ]]; then
  printf 'Error: el prompt no puede estar vacío.\n' >&2
  exit 1
fi

read -r -s -p 'API key de OmniRoute: ' OMNIROUTE_API_KEY
printf '\n'
if [[ -z "$OMNIROUTE_API_KEY" ]]; then
  printf 'Error: la API key no puede estar vacía.\n' >&2
  exit 1
fi

PROMPT="$PROMPT" MODEL="$MODEL" MAX_TOKENS="$MAX_TOKENS" TEMPERATURE="$TEMPERATURE" \
python3 - "$PAYLOAD_FILE" <<'PY'
import json
import os
import sys

payload = {
    "model": os.environ["MODEL"],
    "messages": [{"role": "user", "content": os.environ["PROMPT"]}],
    "temperature": float(os.environ["TEMPERATURE"]),
    "reasoning_effort": "low",
    "max_tokens": int(os.environ["MAX_TOKENS"]),
    "stream": False,
}

with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump(payload, handle, ensure_ascii=False)
PY

set +e
HTTP_STATUS="$(curl --silent --show-error --no-buffer \
  --connect-timeout 5 \
  --max-time 120 \
  --dump-header "$HEADERS_FILE" \
  --output "$RESPONSE_FILE" \
  --write-out '%{http_code}' \
  --config - <<CURL_CONFIG
url = "$ENDPOINT"
request = POST
header = "Authorization: Bearer $OMNIROUTE_API_KEY"
header = "Content-Type: application/json"
data-binary = "@$PAYLOAD_FILE"
CURL_CONFIG
)"
CURL_EXIT=$?
set -e

if [[ "$CURL_EXIT" -ne 0 ]]; then
  printf '\nError: no se pudo conectar con OmniRoute local.\n' >&2
  exit "$CURL_EXIT"
fi

printf '\nHTTP_STATUS: %s\n' "$HTTP_STATUS"

if [[ "$HTTP_STATUS" != "200" ]]; then
  printf '%s\n' '--- RESPUESTA DE ERROR ---' >&2
  cat "$RESPONSE_FILE" >&2
  printf '\n%s\n' '--- HEADERS OMNIROUTE ---' >&2
  grep -iE '^x-omniroute-(latency-ms|tokens-in|tokens-out|response-cost|model|provider|decision|version|cache-hit):' "$HEADERS_FILE" >&2 || true
  exit 1
fi

python3 - "$RESPONSE_FILE" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)

if "error" in data:
    print("Error del provider:")
    print(json.dumps(data["error"], ensure_ascii=False, indent=2))
    raise SystemExit(1)

choices = data.get("choices") or []
if not choices:
    print("Respuesta recibida sin choices:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    raise SystemExit(1)

message = choices[0].get("message") or {}
content = message.get("content") or ""
print("--- RESPUESTA ---")
print(content)
print("--- CONTROL ---")
print(f"finish_reason: {choices[0].get('finish_reason', 'unknown')}")
usage = data.get("usage") or {}
if usage:
    print(
        "tokens: entrada={} salida={} total={}".format(
            usage.get("prompt_tokens", "?"),
            usage.get("completion_tokens", "?"),
            usage.get("total_tokens", "?"),
        )
    )
PY

printf '%s\n' '--- HEADERS OMNIROUTE ---'
grep -iE '^x-omniroute-(latency-ms|tokens-in|tokens-out|response-cost|model|provider|decision|version|cache-hit):' "$HEADERS_FILE" || true
