#!/usr/bin/env python3
"""G-SEC-2.5: public-document integrity checks only; no private reads or network."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXPECTATIONS_PATH = (
    REPOSITORY_ROOT
    / "Operations/Automation/fixtures/gsec2_template_static_integrity_expectations.json"
)


def blocked(reason: str) -> None:
    print(
        json.dumps(
            {
                "status": "gsec2_template_static_integrity_blocked",
                "reason": reason,
                "guarantees": [
                    "public_document_read_only",
                    "no_private_path_or_environment_read",
                    "no_network_or_socket_use",
                    "no_real_consent_or_operation_authorization",
                    "no_ledger_evidence_or_external_write",
                ],
            },
            ensure_ascii=False,
        )
    )
    raise SystemExit(1)


def safely_read_public_document(relative_path: str) -> str:
    candidate = (REPOSITORY_ROOT / relative_path).resolve()
    if not candidate.is_relative_to(REPOSITORY_ROOT):
        blocked("document_path_outside_repository")
    if candidate.is_symlink() or not candidate.is_file():
        blocked(f"missing_or_nonregular_public_document:{relative_path}")
    return candidate.read_text(encoding="utf-8")


def require_marker(document_name: str, document_text: str, marker: str, failures: list[str]) -> None:
    if marker not in document_text:
        failures.append(f"{document_name}:missing_marker:{marker}")


def main() -> None:
    if EXPECTATIONS_PATH.is_symlink() or not EXPECTATIONS_PATH.is_file():
        blocked("missing_or_nonregular_public_expectations_fixture")

    try:
        expectations = json.loads(EXPECTATIONS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        blocked(f"unreadable_public_expectations_fixture:{type(error).__name__}")

    failures: list[str] = []
    reviewed_documents: list[str] = []
    document_texts: dict[str, str] = {}

    for name, specification in expectations.get("documents", {}).items():
        path = specification.get("path")
        if not isinstance(path, str):
            failures.append(f"{name}:missing_public_path")
            continue
        text = safely_read_public_document(path)
        document_texts[name] = text
        reviewed_documents.append(path)
        require_marker(name, text, f"status: {specification.get('status')}", failures)
        for marker in specification.get("required_markers", []):
            require_marker(name, text, marker, failures)

    proposal_sheet = document_texts.get("proposal_sheet", "")
    for control in expectations.get("required_comparison_controls", []):
        require_marker("proposal_sheet", proposal_sheet, f"| {control}", failures)

    template = document_texts.get("consent_template", "")
    if template.count("[PENDIENTE — no emitir]") < 5:
        failures.append("consent_template:insufficient_unissued_placeholders")
    if "[PENDIENTE — no solicitar]" not in template:
        failures.append("consent_template:approval_field_not_marked_unissued")

    if failures:
        print(
            json.dumps(
                {
                    "status": "gsec2_template_static_integrity_blocked",
                    "reviewed_documents": reviewed_documents,
                    "failures": failures,
                    "guarantees": [
                        "public_document_read_only",
                        "no_private_path_or_environment_read",
                        "no_network_or_socket_use",
                        "no_real_consent_or_operation_authorization",
                        "no_ledger_evidence_or_external_write",
                    ],
                },
                ensure_ascii=False,
            )
        )
        raise SystemExit(1)

    print(
        json.dumps(
            {
                "status": "gsec2_template_static_integrity_passed",
                "reviewed_documents": reviewed_documents,
                "checked_constraints": {
                    "brand": expectations.get("brand"),
                    "max_observations": expectations.get("limits", {}).get("max_observations"),
                    "retention_days": expectations.get("limits", {}).get("retention_days"),
                    "validity_hours": expectations.get("limits", {}).get("validity_hours"),
                    "comparison_controls": expectations.get("required_comparison_controls", []),
                },
                "guarantees": [
                    "public_document_read_only",
                    "no_private_path_or_environment_read",
                    "no_network_or_socket_use",
                    "no_real_consent_or_operation_authorization",
                    "no_ledger_evidence_or_external_write",
                ],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
