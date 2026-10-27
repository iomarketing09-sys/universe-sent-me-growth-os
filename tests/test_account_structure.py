import os
from pathlib import Path

def test_growth_os_structure():
    base = Path(__file__).parent.parent  # growth-os directory
    core_dir = base / "core" / "growthos-core"
    accounts_dir = base / "accounts"  # This is the accounts directory for CSV storage
    tenants_dir = base / "tenants"    # This is the main tenants directory
    agents_dir = base / "agents"
    tests_dir = base / "tests"

    # Core exists and has the expected subdirectories
    assert core_dir.exists(), "Core directory does not exist"
    package_dir = core_dir / "growthos"
    assert package_dir.exists(), "Core/growthos package does not exist"
    assert (package_dir / "core").exists(), "Core/growthos/core does not exist"
    assert (package_dir / "storage").exists(), "Core/growthos/storage does not exist"
    assert (package_dir / "config").exists(), "Core/growthos/config does not exist"
    assert (core_dir / "scripts").exists(), "Core/scripts does not exist"
    assert (core_dir / "docs").exists(), "Core/docs does not exist"
    assert (core_dir / "tests").exists(), "Core/tests does not exist"

    # Accounts directory exists (for CSV storage per account)
    assert accounts_dir.exists(), "Accounts directory does not exist"

    # Each account directory exists in accounts/
    assert (accounts_dir / "firma_bordados").exists(), "Firma Bordados account directory does not exist in accounts/"
    assert (accounts_dir / "universe_sent_me").exists(), "Universe Sent Me account directory does not exist in accounts/"

    # Each account has data directory in accounts/
    assert (accounts_dir / "firma_bordados" / "data").exists(), "Firma Bordados data directory does not exist in accounts/"
    assert (accounts_dir / "universe_sent_me" / "data").exists(), "Universe Sent Me data directory does not exist in accounts/"

    # Tenants directory exists (main tenant configs)
    assert tenants_dir.exists(), "Tenants directory does not exist"

    # Each tenant directory exists in tenants/
    assert (tenants_dir / "firma-bordados").exists(), "Firma Bordados tenant directory does not exist in tenants/"
    assert (tenants_dir / "universe").exists(), "Universe Sent Me tenant directory does not exist in tenants/"

    # Each tenant has docs directory
    assert (tenants_dir / "firma-bordados" / "docs").exists(), "Firma Bordados docs directory does not exist in tenants/"
    assert (tenants_dir / "universe" / "docs").exists(), "Universe Sent Me docs directory does not exist in tenants/"

    # Los agentes viven dentro del módulo que sirven; los pendientes siguen en agents/
    modules_dir = base / "modules"
    assert modules_dir.exists(), "Modules directory does not exist"
    assert (modules_dir / "identity" / "agents" / "brand_voice_agent").exists(), "brand_voice_agent should live in modules/identity"
    assert (modules_dir / "creative" / "agents" / "copywriter_agent").exists(), "copywriter_agent should live in modules/creative"

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

    print("Account structure test PASSED.")

if __name__ == "__main__":
    test_growth_os_structure()
