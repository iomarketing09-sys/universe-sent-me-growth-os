#!/usr/bin/env bash
# G-SEC-2.5 public-template integrity preflight; no private reads, network, or execution.
set -euo pipefail

readonly CONFIRMATION="RUN_USM_GSEC2_TEMPLATE_STATIC_INTEGRITY"
readonly SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly REPOSITORY_ROOT="$(cd "${SCRIPT_DIRECTORY}/../.." && pwd)"
readonly VALIDATOR="${SCRIPT_DIRECTORY}/validate_gsec2_template_static_integrity.py"
readonly FIXTURE="${SCRIPT_DIRECTORY}/fixtures/gsec2_template_static_integrity_expectations.json"

usage() {
  cat <<'EOF'
Usage:
  preflight_gsec2_template_static_integrity.sh --plan
  preflight_gsec2_template_static_integrity.sh --preflight
  preflight_gsec2_template_static_integrity.sh --execute --confirm RUN_USM_GSEC2_TEMPLATE_STATIC_INTEGRITY

This gate reads only three public Markdown documents and one public expectations fixture.
It does not read private paths or environment values, open network sockets, request consent,
authorize an operation, invoke collectors, or write ledger/evidence/external output.
EOF
}

print_boundary() {
  printf '%s\n' 'USM G-SEC-2.5 public-template static-integrity preflight'
  printf '%s\n' "mode=$1"
  printf '%s\n' 'network=prohibited'
  printf '%s\n' 'private_path_and_environment_read=prohibited'
  printf '%s\n' 'real_consent_or_operation_authorization=prohibited'
  printf '%s\n' 'collector_and_service_start=prohibited'
  printf '%s\n' 'external_and_canonical_write=prohibited'
}

require_public_artifacts() {
  command -v python3 >/dev/null || { printf '%s\n' 'STATUS=blocked_python_missing'; exit 1; }
  [[ -f "${VALIDATOR}" && ! -L "${VALIDATOR}" ]] || { printf '%s\n' 'STATUS=blocked_validator_missing_or_symlink'; exit 1; }
  [[ -f "${FIXTURE}" && ! -L "${FIXTURE}" ]] || { printf '%s\n' 'STATUS=blocked_fixture_missing_or_symlink'; exit 1; }
  [[ -f "${SCRIPT_DIRECTORY}/2026-08-25_Consentimiento_Piloto_Real_Shadow_Ledger_USM.md" ]] || { printf '%s\n' 'STATUS=blocked_gsec2_contract_missing'; exit 1; }
  [[ -f "${SCRIPT_DIRECTORY}/2026-08-27_Plantilla_Tarjeta_Consentimiento_Puntual_USM.md" ]] || { printf '%s\n' 'STATUS=blocked_consent_template_missing'; exit 1; }
  [[ -f "${SCRIPT_DIRECTORY}/2026-08-27_Ficha_Propuesta_Minima_Comparacion_Alcance_USM.md" ]] || { printf '%s\n' 'STATUS=blocked_proposal_sheet_missing'; exit 1; }
}

check_processes() {
  if pgrep -a -f '[f]etch_(tiktok|youtube|facebook|instagram)_official_metrics|[o]mniroute|[d]ocker[[:space:]].*(compose|run)|[c]ompose' >/dev/null; then
    printf '%s\n' 'STATUS=blocked_collector_or_service_process_detected'
    exit 1
  fi
}

if [[ $# -eq 1 && "$1" == "--plan" ]]; then
  print_boundary 'plan'
  printf '%s\n' 'STATUS=plan_complete_no_document_read_no_network_no_real_consent'
  exit 0
fi

if [[ $# -eq 1 && "$1" == "--preflight" ]]; then
  print_boundary 'preflight'
  require_public_artifacts
  check_processes
  printf '%s\n' "python=$(python3 --version)"
  printf '%s\n' "repo_commit=$(git -C "${REPOSITORY_ROOT}" rev-parse --short HEAD)"
  printf '%s\n' 'public_documents_and_fixture=present'
  printf '%s\n' 'services_or_collectors=not_detected'
  printf '%s\n' 'STATUS=preflight_complete_gsec2_template_static_only_no_network_no_private_read'
  exit 0
fi

if [[ $# -eq 3 && "$1" == "--execute" && "$2" == "--confirm" && "$3" == "${CONFIRMATION}" ]]; then
  print_boundary 'execute'
  require_public_artifacts
  check_processes
  printf '%s\n' "python=$(python3 --version)"
  printf '%s\n' "repo_commit=$(git -C "${REPOSITORY_ROOT}" rev-parse --short HEAD)"
  printf '%s\n' 'public_documents_and_fixture=present'
  PYTHONDONTWRITEBYTECODE=1 python3 -B "${VALIDATOR}"
  printf '%s\n' 'STATUS=gsec2_template_static_integrity_complete_no_network_no_private_read_no_real_consent'
  exit 0
fi

usage
exit 2
