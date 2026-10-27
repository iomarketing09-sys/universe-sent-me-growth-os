"""
Brand Voice Memory - Gestión de Perfiles de Voz por Tenant
===========================================================
Carga, guarda y versiona Brand Voice Profiles en tenants/{id}/brand_voice.json
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field, fields
from datetime import datetime
from copy import deepcopy


@dataclass
class Vocabulary:
    preferred: List[str] = field(default_factory=list)
    avoid: List[str] = field(default_factory=list)
    product_terms: List[str] = field(default_factory=list)


@dataclass
class VoiceAttributes:
    tone: str = ""
    formality: str = ""
    emoji_usage: str = ""
    sentence_length: str = ""
    perspective: str = ""


@dataclass
class MessagingPatterns:
    opening: List[str] = field(default_factory=list)
    closing: List[str] = field(default_factory=list)
    cta_soft: List[str] = field(default_factory=list)
    cta_direct: List[str] = field(default_factory=list)


@dataclass
class ChannelRules:
    whatsapp: Dict[str, Any] = field(default_factory=dict)
    meta_ads: Dict[str, Any] = field(default_factory=dict)
    organic_social: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Compliance:
    meta_templates_category: str = "UTILITY"
    language: str = "es_MX"
    prohibited_claims: List[str] = field(default_factory=list)
    required_disclaimers: List[str] = field(default_factory=list)


@dataclass
class BrandIdentity:
    name: str = ""
    tagline: str = ""
    value_proposition: str = ""
    differentiators: List[str] = field(default_factory=list)


@dataclass
class Examples:
    good: str = ""
    bad: str = ""


@dataclass
class BrandVoiceProfile:
    """Perfil completo de voz de marca para un tenant"""
    tenant_id: str
    version: str = "1.0"
    updated: str = ""
    sources: List[str] = field(default_factory=list)
    
    brand_identity: BrandIdentity = field(default_factory=BrandIdentity)
    voice_attributes: VoiceAttributes = field(default_factory=VoiceAttributes)
    vocabulary: Vocabulary = field(default_factory=Vocabulary)
    messaging_patterns: MessagingPatterns = field(default_factory=MessagingPatterns)
    channel_rules: ChannelRules = field(default_factory=ChannelRules)
    compliance: Compliance = field(default_factory=Compliance)
    examples: Examples = field(default_factory=Examples)
    sub_brands: Dict[str, Any] = field(default_factory=dict)
    published_copy_evidence: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: str = ""
    approved_by: str = ""
    approval_date: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BrandVoiceProfile":
        def build(model, payload):
            allowed = {f.name for f in fields(model)}
            return model(**{k: v for k, v in (payload or {}).items() if k in allowed})

        # Handle nested dataclasses
        nested = {
            "brand_identity": build(BrandIdentity, data.get("brand_identity")),
            "voice_attributes": build(VoiceAttributes, data.get("voice_attributes")),
            "vocabulary": build(Vocabulary, data.get("vocabulary")),
            "messaging_patterns": build(MessagingPatterns, data.get("messaging_patterns")),
            "channel_rules": build(ChannelRules, data.get("channel_rules")),
            "compliance": build(Compliance, data.get("compliance")),
            "examples": build(Examples, data.get("examples")),
        }
        # Remove nested/unknown keys from data and merge
        allowed_top = {f.name for f in fields(cls)} - set(nested)
        flat = {k: v for k, v in data.items() if k in allowed_top}
        return cls(**flat, **nested)


class BrandVoiceMemory:
    """Gestión de persistencia y versionado de Brand Voice Profiles"""
    
    def __init__(self, base_path: str = "/home/universe-sent-me/growth-os"):
        self.base_path = Path(base_path)
        self.tenants_path = self.base_path / "tenants"
    
    def _get_profile_path(self, tenant_id: str) -> Path:
        return self.tenants_path / tenant_id / "brand_voice.json"
    
    def _get_history_dir(self, tenant_id: str) -> Path:
        return self.tenants_path / tenant_id / "brand_voice_history"
    
    def load(self, tenant_id: str) -> Optional[BrandVoiceProfile]:
        """Carga perfil existente"""
        path = self._get_profile_path(tenant_id)
        if not path.exists():
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return BrandVoiceProfile.from_dict(data)
    
    def save(self, profile: BrandVoiceProfile, create_backup: bool = True) -> Path:
        """Guarda perfil (crea backup automático)"""
        path = self._get_profile_path(tenant_id=profile.tenant_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup previo
        if create_backup and path.exists():
            self._create_backup(profile.tenant_id)
        
        # Update metadata
        profile.updated = datetime.now().isoformat()
        if not profile.created_at:
            profile.created_at = profile.updated
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(profile.to_dict(), f, ensure_ascii=False, indent=2)
        
        return path
    
    def _create_backup(self, tenant_id: str) -> Path:
        """Crea backup versionado"""
        history_dir = self._get_history_dir(tenant_id)
        history_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = history_dir / f"brand_voice_{timestamp}.json"
        
        src = self._get_profile_path(tenant_id)
        if src.exists():
            import shutil
            shutil.copy2(src, backup_path)
        
        return backup_path
    
    def create_from_scratch(self, tenant_id: str, base_data: Dict[str, Any] = None) -> BrandVoiceProfile:
        """Crea perfil vacío con defaults"""
        profile = BrandVoiceProfile(
            tenant_id=tenant_id,
            version="1.0",
            created_at=datetime.now().isoformat(),
            updated=datetime.now().isoformat(),
        )
        
        # Merge base_data si existe
        if base_data:
            for key, value in base_data.items():
                if hasattr(profile, key) and value:
                    setattr(profile, key, value)
        
        return profile
    
    def list_history(self, tenant_id: str) -> List[Path]:
        """Lista backups disponibles"""
        history_dir = self._get_history_dir(tenant_id)
        if not history_dir.exists():
            return []
        return sorted(history_dir.glob("brand_voice_*.json"), reverse=True)
    
    def restore_backup(self, tenant_id: str, backup_name: str) -> BrandVoiceProfile:
        """Restaura un backup específico"""
        backup_path = self._get_history_dir(tenant_id) / backup_name
        with open(backup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        profile = BrandVoiceProfile.from_dict(data)
        self.save(profile, create_backup=True)
        return profile
    
    def exists(self, tenant_id: str) -> bool:
        return self._get_profile_path(tenant_id).exists()
    
    def delete(self, tenant_id: str) -> bool:
        """Elimina perfil (con backup previo)"""
        path = self._get_profile_path(tenant_id)
        if path.exists():
            self._create_backup(tenant_id)
            path.unlink()
            return True
        return False


# Instancia global
memory = BrandVoiceMemory()
