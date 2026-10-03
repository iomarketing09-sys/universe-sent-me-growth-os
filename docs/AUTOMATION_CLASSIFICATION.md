# Automation Classification - Growth OS Multi-Cuenta

## Methodology

1. Static inspection of file names, paths, and content (head/tail) to infer purpose.
2. No execution of scripts, no API calls, no reading of secrets.
3. Classification based on:
   - Core reusability: generic utilities, validation, data transformation not tied to a specific account.
   - Shared candidate: potentially reusable but depends on configuration or APIs.
   - Account-specific: scripts that reference account-specific data, IDs, or services.
   - Obsolete/duplicate: duplicates, experimental, or superseded.
   - Requires review: unclear responsibility.

## Inspected Lots (so far)

### LOT 1: /home/universe-sent-me/new-growth-os/

List of relevant Python files (excluding venv, __pycache__, and auditoria_firma_bordados/omniroute + Firma WEB/* which is clearly external to Growth OS and belongs to another project).

Files inspected:

- /home/universe-sent-me/new-growth-os/config.py
- /home/universe-sent-me/new-growth-os/core/__init__.py
- /home/universe-sent-me/new-growth-os/core/enums.py
- /home/universe-sent-me/new-growth-os/core/models.py
- /home/universe-sent-me/new-growth-os/scripts/automate_publication_metrics.py
- /home/universe-sent-me/new-growth-os/scripts/automate_publication_sqlite.py
- /home/universe-sent-me/new-growth-os/scripts/drive_example.py
- /home/universe-sent-me/new-growth-os/scripts/example_usage.py
- /home/universe-sent-me/new-growth-os/scripts/export_assets_for_growthos.py
- /home/universe-sent-me/new-growth-os/scripts/export_assets_from_audit.py
- /home/universe-sent-me/new-growth-os/scripts/export_drive_inventory.py
- /home/universe-sent-me/new-growth-os/scripts/export_drive_inventory_real.py
- /home/universe-sent-me/new-growth-os/storage/csv_adapter.py
- /home/universe-sent-me/new-growth-os/storage/drive/__init__.py
- /home/universe-sent-me/new-growth-os/storage/drive/adapter.py
- /home/universe-sent-me/new-growth-os/storage/drive_repository.py
- /home/universe-sent-me/new-growth-os/storage/repositories.py
- /home/universe-sent-me/new-growth-os/validate_export.py

Classification per file:

| File | Category | Justification |
|------|----------|---------------|
| config.py | CORE_REUTILIZABLE | Simple Settings class, no account-specific logic. |
| core/__init__.py | CORE_REUTILIZABLE | Package initializer. |
| core/enums.py | CORE_REUTILIZABLE | Domain enums used across accounts. |
| core/models.py | CORE_REUTILIZABLE | Pydantic models with validators, account-agnostic. |
| scripts/automate_publication_metrics.py | REQUIRES_REVIEW | Name suggests publication metrics; likely uses APIs; need to inspect content to determine if generic or account-specific. |
| scripts/automate_publication_sqlite.py | REQUIRES_REVIEW | SQLite automation; could be generic storage utility. |
| scripts/drive_example.py | SHARED_CANDIDATE | Example for Google Drive; likely shows generic Drive adapter usage. |
| scripts/example_usage.py | CORE_REUTILIZABLE | Demonstrates how to use repositories with account_id; generic. |
| scripts/export_assets_for_growthos.py | FIRMA_BORDADOS | Explicitly references Firma Bordados audit; account-specific. |
| scripts/export_assets_from_audit.py | FIRMA_BORDADOS | Exports from audit; specific to Firma Bordados. |
| scripts/export_drive_inventory.py | REQUIRES_REVIEW | Exports Drive inventory; may be generic or tied to a specific account's Drive. |
| scripts/export_drive_inventory_real.py | REQUIRES_REVIEW | Similar to above; likely account-specific if uses real credentials. |
| storage/csv_adapter.py | CORE_REUTILIZABLE | Generic CSV adapter with enum handling. |
| storage/drive/__init__.py | CORE_REUTILIZABLE | Package init for Drive storage. |
| storage/drive/adapter.py | SHARED_CANDIDATE | Google Drive adapter; may need credentials but the class is generic. |
| storage/drive_repository.py | SHARED_CANDIDATE | Repository for Drive files; generic but depends on Drive service. |
| storage/repositories.py | CORE_REUTILIZABLE | Core repository pattern with account_id support. |
| validate_export.py | REQUIRES_REVIEW | Validates exports; could be generic or tied to a specific export format. |

Notes:
- The auditoria_firma_bordados/omniroute + Firma WEB/* files are clearly part of an external project (OmniRoute + Firma WEB) and are not Growth OS automations; they are excluded from classification.
- The core, storage, and example_usage are part of the validated core and are CORE_REUTILIZABLE.
- Scripts that mention "audit" or "Firma Bordados" are classified as FIRMA_BORDADOS.
- Others are marked REQUIRES_REVIEW pending further inspection of their content to determine if they are generic or account-specific.

## Next Steps

Continue inspection of:
- /home/universe-sent-me/universe-sent-me-growth-os/ (Operations/, tools/, scripts/, data/)
- /home/universe-sent-me/growthos/ (if any scripts)
- /home/universe-sent-me/growth-os/ (already existing, but we may have missed some)

Then complete the classification matrix and architecture documents.

