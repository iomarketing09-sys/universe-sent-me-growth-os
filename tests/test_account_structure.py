import os
from pathlib import Path

def test_growth_os_structure():
    base = Path(__file__).parent.parent  # growth-os directory
    core_dir = base / "core" / "growthos-core"
    accounts_dir = base / "accounts"
    firma_bordados_dir = accounts_dir / "firma_bordados"
    universe_sent_me_dir = accounts_dir / "universe_sent_me"
    shared_dir = base / "shared"
    tests_dir = base / "tests"

    # Core exists and has the expected subdirectories
    assert core_dir.exists(), "Core directory does not exist"
    assert (core_dir / "core").exists(), "Core/core does not exist"
    assert (core_dir / "storage").exists(), "Core/storage does not exist"
    assert (core_dir / "scripts").exists(), "Core/scripts does not exist"
    assert (core_dir / "docs").exists(), "Core/docs does not exist"
    assert (core_dir / "tests").exists(), "Core/tests does not exist"

    # Accounts directory exists
    assert accounts_dir.exists(), "Accounts directory does not exist"

    # Each account directory exists
    assert firma_bordados_dir.exists(), "Firma Bordados account directory does not exist"
    assert universe_sent_me_dir.exists(), "Universe Sent Me account directory does not exist"

    # Each account has data directory
    assert (firma_bordados_dir / "data").exists(), "Firma Bordados data directory does not exist"
    assert (universe_sent_me_dir / "data").exists(), "Universe Sent Me data directory does not exist"

    # Each account has docs directory
    assert (firma_bordados_dir / "docs").exists(), "Firma Bordados docs directory does not exist"
    assert (universe_sent_me_dir / "docs").exists(), "Universe Sent Me docs directory does not exist"

    # Shared directories exist
    assert shared_dir.exists(), "Shared directory does not exist"
    assert (shared_dir / "automations").exists(), "Shared/automations does not exist"
    assert (shared_dir / "tools").exists(), "Shared/tools does not exist"
    assert (shared_dir / "integrations").exists(), "Shared/integrations does not exist"

    # Tests directory exists
    assert tests_dir.exists(), "Tests directory does not exist"

    # Check that there are no .env files in the core
    env_files = list(core_dir.rglob("*.env*"))
    assert len(env_files) == 0, f"Found .env files in core: {env_files}"

    # Check that there is no .git in the core
    git_dir = core_dir / ".git"
    assert not git_dir.exists(), "Core should not have a .git directory"

    # Check that there is no venv in the core
    venv_dir = core_dir / "venv"
    assert not venv_dir.exists(), "Core should not have a venv directory"

    # Check that the accounts do not have .git or venv (they shouldn't, but we are being safe)
    for acc_dir in [firma_bordados_dir, universe_sent_me_dir]:
        assert not (acc_dir / ".git").exists(), f"Account {acc_dir.name} should not have a .git directory"
        assert not (acc_dir / "venv").exists(), f"Account {acc_dir.name} should not have a venv directory"
        # Also check for .env files in the account directories (should not be in the core, but might be in account configs)
        # We allow .env in account config directories, but not in the root of the account? We'll be lenient and just note.
        # We'll check the root of the account for .env files and warn but not fail.
        account_env = list(acc_dir.rglob("*.env*"))
        # We'll allow these in the account's config directory, but we'll just note if found in the root.
        # For simplicity, we'll just check the root of the account.
        root_env = [f for f in account_env if f.parent == acc_dir]
        assert len(root_env) == 0, f"Account {acc_dir.name} should not have .env files in its root: {root_env}"

    print("Account structure test PASSED.")

if __name__ == "__main__":
    test_growth_os_structure()
