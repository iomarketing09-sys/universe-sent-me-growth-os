#!/usr/bin/env python3
"""
Verify CGO Setup - Verifica entorno completo del Chief Growth Officer
"""

import sys
from pathlib import Path

# Add growthos-core to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "core" / "growthos-core"))
# Add project root for growth module
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

def check_core_imports():
    """Verifica imports del core"""
    print("🔍 Verificando imports core...")
    try:
        from growthos.core import models, enums
        from growthos.storage import csv_adapter, repositories
        from growth.tenant_registry import get_registry
        print("  ✅ growthos.core imports OK")
        print("  ✅ growthos.storage imports OK")
        print("  ✅ growth.tenant_registry OK")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def check_tenants():
    """Verifica tenants registrados"""
    print("\n🔍 Verificando tenants...")
    from growth.tenant_registry import get_registry
    registry = get_registry()
    tenants = registry.list_tenants()
    
    print(f"  Tenants registrados: {len(tenants)}")
    for tid in tenants:
        config = registry.load_config(tid)
        ttype = config.get("tenant_type", "unknown")
        name = config.get("business_name", tid)
        meta_ok = bool(config.get("meta", {}).get("page_id"))
        gbp_ok = bool(config.get("google_business", {}).get("place_id"))
        print(f"  • {tid} ({ttype}): {name} | Meta: {'✅' if meta_ok else '❌'} | GBP: {'✅' if gbp_ok else '❌'}")
    
    return len(tenants) > 0


def check_agents():
    """Verifica agents disponibles"""
    print("\n🔍 Verificando agents...")
    agents_path = Path(__file__).resolve().parents[3] / "agents"
    
    expected = ["brand_voice_agent", "meta_ads_agent", "whatsapp_agent", "copywriter_agent"]
    all_ok = True
    for agent in expected:
        agent_path = agents_path / agent
        if agent_path.exists():
            has_agent_py = (agent_path / "agent.py").exists()
            if has_agent_py:
                print(f"  • {agent}: ✅")
            else:
                print(f"  • {agent}: ⚠️ (sin agent.py)")
                all_ok = False
        else:
            print(f"  • {agent}: ❌ NO EXISTE")
            all_ok = False
    return all_ok


def check_scripts():
    """Verifica scripts de orquestación"""
    print("\n🔍 Verificando scripts...")
    scripts_path = Path(__file__).resolve().parents[3] / "scripts"
    
    expected = ["sync_all.py", "sync_google.py", "sync_metrics.py"]
    all_ok = True
    for script in expected:
        script_path = scripts_path / script
        if script_path.exists():
            print(f"  • {script}: ✅")
        else:
            print(f"  • {script}: ❌")
            all_ok = False
    return all_ok


def check_skills():
    """Verifica skills CGO"""
    print("\n🔍 Verificando skills...")
    skills_path = Path(__file__).resolve().parents[1]
    
    checks = [
        ("SKILL.md", skills_path / "SKILL.md"),
        ("agents/openai.yaml", skills_path / "agents" / "openai.yaml"),
        ("references/governance.md", skills_path / "references" / "governance.md"),
        ("references/canon_integration.md", skills_path / "references" / "canon_integration.md"),
        ("references/calendar_architecture.md", skills_path / "references" / "calendar_architecture.md"),
        ("references/core_models.md", skills_path / "references" / "core_models.md"),
    ]
    
    all_ok = True
    for name, path in checks:
        if path.exists():
            print(f"  • {name}: ✅")
        else:
            print(f"  • {name}: ❌")
            all_ok = False
    return all_ok


def check_docs():
    """Verifica docs clave"""
    print("\n🔍 Verificando docs...")
    docs_path = Path(__file__).resolve().parents[3] / "docs"
    
    expected = [
        "GROWTH_OS_FLUJO_COMPLETO.md",
        "ESTADO_GROWTH_20261013.md",
        "MODULO_REVENUE_LITE.md",
        "WHATSAPP_AGENT_FLOW_FIX.md",
        "META_ADS_AGENT_SUMMARY_20261014.md",
        "PENDIENTES_GROWTH_20261012.md",
    ]
    
    all_ok = True
    for doc in expected:
        doc_path = docs_path / doc
        if doc_path.exists():
            print(f"  • {doc}: ✅")
        else:
            print(f"  • {doc}: ❌")
            all_ok = False
    return all_ok


def check_meta_token():
    """Verifica token Meta"""
    print("\n🔍 Verificando token Meta...")
    import os
    from dotenv import load_dotenv
    
    env_path = Path(__file__).resolve().parents[3] / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        token = os.getenv("META_ACCESS_TOKEN")
        if token:
            print(f"  ✅ META_ACCESS_TOKEN presente ({len(token)} chars)")
        else:
            print("  ⚠️ META_ACCESS_TOKEN no encontrado en .env")
    else:
        print("  ❌ .env no encontrado")


def main():
    print("=" * 60)
    print("GROWTH CGO - VERIFICACIÓN DE SETUP")
    print("=" * 60)
    
    checks = [
        check_core_imports(),
        check_tenants(),
        check_agents(),
        check_scripts(),
        check_skills(),
        check_docs(),
    ]
    check_meta_token()
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ SETUP COMPLETO - CGO listo para operar")
        return 0
    else:
        print("❌ SETUP INCOMPLETO - Revisar items marcados")
        return 1


if __name__ == "__main__":
    sys.exit(main())
