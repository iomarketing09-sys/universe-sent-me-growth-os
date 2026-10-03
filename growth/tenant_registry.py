"""
Registro de tenants para arquitectura multi-usuario.

Aísla configuración y assets de cada tenant bajo su identificador único.
"""
from pathlib import Path
from typing import Dict, Any, Optional
import json


class TenantRegistry:
    """Gestiona aislamiento de tenants en Growth OS."""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).resolve().parents[1]
        self.tenants_dir = self.base_path / "tenants"
        self.tenants_dir.mkdir(exist_ok=True)
    
    def get_tenant_dir(self, tenant_id: str) -> Path:
        """Obtiene directorio del tenant (lo crea si no existe)."""
        tenant_dir = self.tenants_dir / tenant_id
        tenant_dir.mkdir(exist_ok=True)
        return tenant_dir
    
    def get_manifest_path(self, tenant_id: str) -> Path:
        """Ruta al manifest del tenant."""
        return self.get_tenant_dir(tenant_id) / "assets_manifest.json"
    
    def get_config_path(self, tenant_id: str) -> Path:
        """Ruta a la configuración del tenant."""
        return self.get_tenant_dir(tenant_id) / "config.json"
    
    def get_dryrun_output_path(self, tenant_id: str) -> Path:
        """Ruta al output de dry-run del tenant."""
        return self.get_tenant_dir(tenant_id) / "dryrun_output.json"
    
    def save_manifest(self, tenant_id: str, manifest: Dict[str, Any]) -> None:
        """Guarda manifest del tenant."""
        path = self.get_manifest_path(tenant_id)
        with path.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    def load_manifest(self, tenant_id: str) -> Dict[str, Any]:
        """Carga manifest del tenant."""
        path = self.get_manifest_path(tenant_id)
        if not path.exists():
            raise FileNotFoundError(f"Manifest no encontrado para tenant: {tenant_id}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    
    def save_config(self, tenant_id: str, config: Dict[str, Any]) -> None:
        """Guarda configuración del tenant."""
        path = self.get_config_path(tenant_id)
        with path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def load_config(self, tenant_id: str) -> Dict[str, Any]:
        """Carga configuración del tenant."""
        path = self.get_config_path(tenant_id)
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    
    def list_tenants(self) -> list:
        """Lista todos los tenants registrados."""
        if not self.tenants_dir.exists():
            return []
        return [d.name for d in self.tenants_dir.iterdir() if d.is_dir()]


# Instancia global para uso conveniente
_default_registry = None

def get_registry() -> TenantRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = TenantRegistry()
    return _default_registry


def isolate_firma_bordados() -> Dict[str, Any]:
    """
    Aísla la configuración y assets de Firma Bordados bajo tenant 'firma-bordados'.
    
    Copia el manifest actual y config al directorio del tenant.
    """
    registry = get_registry()
    tenant_id = "firma-bordados"
    
    # Cargar manifest actual (desde growth/)
    source_manifest_path = Path(__file__).resolve().parents[1] / "growth" / "assets_manifest.json"
    with source_manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Configuración del tenant
    config = {
        "tenant_id": tenant_id,
        "client_name": "Firma Bordados",
        "whatsapp_number": "878 788 0735",
        "whatsapp_e164": "5218787880735",
        "contact_channel": "WhatsApp",
        "excluded_categories": ["parches", "gorras"],
        "timezone": "America/Matamoros",
        "utc_offset_hours": 5,
        "assets_root": "tenants/firma-bordados/assets/Firma Bordados",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    
    # Guardar en directorio del tenant
    registry.save_manifest(tenant_id, manifest)
    registry.save_config(tenant_id, config)
    
    return {
        "tenant_id": tenant_id,
        "manifest_path": str(registry.get_manifest_path(tenant_id)),
        "config_path": str(registry.get_config_path(tenant_id)),
        "assets_count": len(manifest.get("assets", [])),
        "status": "isolated"
    }


if __name__ == "__main__":
    from datetime import datetime, timezone
    result = isolate_firma_bordados()
    print(json.dumps(result, indent=2, ensure_ascii=False))
