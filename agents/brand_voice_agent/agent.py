"""
Brand Voice Agent - Main Agent Class
=====================================
Orquesta todos los skills: copywriting, compliance, tone, research, A/B testing.
"""

import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from .models import ModelRouter, get_model_alias, get_generation_params
from .memory import BrandVoiceMemory, BrandVoiceProfile, memory
from .skills.meta_compliance import MetaComplianceChecker, ComplianceResult
from .skills.tone_analyzer import ToneAnalyzer
from .skills.competitor_research import CompetitorResearcher
from .skills.ab_variants import ABVariantGenerator, VariantStrategy
from .skills.post_voice_analyzer import analyze_posts, load_posts


class BrandVoiceAgent:
    """
    Agente principal de Brand Voice.
    
    Un agente por tenant. Carga profile, expone métodos para generar copy,
    validar compliance, analizar tono, investigar competencia, generar A/B tests.
    """
    
    def __init__(self, tenant_id: str, base_path: str = "/home/universe-sent-me/growth-os"):
        self.tenant_id = tenant_id
        self.base_path = Path(base_path)
        self.tenant_path = self.base_path / "tenants" / tenant_id
        
        # Cargar perfil
        self.profile = self._load_or_create_profile()
        
        # Inicializar skills
        self.compliance = MetaComplianceChecker(self.profile.to_dict() if self.profile else {})
        self.tone = ToneAnalyzer(self.profile.to_dict() if self.profile else {})
        self.research = CompetitorResearcher(self.profile.to_dict() if self.profile else {})
        self.ab_test = ABVariantGenerator(self.profile.to_dict() if self.profile else {})
        self.router = ModelRouter()
        
        # Router de modelos
        self.model_router = ModelRouter()
    
    def _load_or_create_profile(self) -> BrandVoiceProfile:
        """Carga perfil existente o crea uno base desde config.json"""
        existing = memory.load(self.tenant_id)
        if existing:
            return existing
        
        # Crear desde config.json del tenant
        config_path = self.tenant_path / "config.json"
        base_data = {}
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Extraer brand voice del config si existe
            if "brand_guidelines" in config:
                bg = config["brand_guidelines"]
                
                # Helper para parsear brand_voice (puede ser string o dict)
                bv = bg.get("brand_voice", {})
                if isinstance(bv, str):
                    # Si es string, usarlo como tone y deducir formality
                    tone = bv
                    formality = "tú cercano"
                    emoji_usage = "moderado"
                    vocab_preferred = []
                    vocab_avoid = []
                else:
                    # Si es dict, extraer campos
                    tone = bv.get("tone", "")
                    formality = bv.get("formality", "tú cercano")
                    emoji_usage = bv.get("emoji_usage", "moderado")
                    vocab_preferred = bv.get("vocabulary_preferred", [])
                    vocab_avoid = bv.get("vocabulary_avoid", [])
                
                base_data = {
                    "brand_identity": {
                        "name": config.get("business_name", self.tenant_id),
                        "tagline": bg.get("tagline", ""),
                        "value_proposition": bg.get("value_prop", ""),
                        "differentiators": bg.get("differentiators", [])
                    },
                    "voice_attributes": {
                        "tone": tone,
                        "formality": formality,
                        "emoji_usage": emoji_usage,
                        "sentence_length": "media",
                        "perspective": "tú cercano"
                    },
                    "vocabulary": {
                        "preferred": vocab_preferred,
                        "avoid": vocab_avoid,
                        "product_terms": []
                    },
                    "messaging_patterns": {
                        "opening": ["¡Hola! Bienvenido a {brand} 👋"],
                        "closing": ["¡Gracias por contactarnos! 😊"],
                        "cta_soft": ["¿Te ayudo?", "¿Necesitas más info?"],
                        "cta_direct": ["Haz tu pedido", "Agenda tu cita"]
                    },
                    "channel_rules": {},
                    "compliance": {
                        "prohibited_claims": ["mejor del mercado", "garantizado 100%"]
                    },
                    "examples": {}
                }
        
        profile = memory.create_from_scratch(self.tenant_id, base_data)
        memory.save(profile)
        return profile
    
    def reload_profile(self):
        """Recarga perfil desde disco"""
        self.profile = memory.load(self.tenant_id) or self._load_or_create_profile()
        # Re-inicializar skills con perfil actualizado
        self._refresh_skills()
    
    def _refresh_skills(self):
        """Re-inicializa skills con perfil actual"""
        profile_dict = self.profile.to_dict() if self.profile else {}
        self.compliance = MetaComplianceChecker(profile_dict)
        self.tone = ToneAnalyzer(profile_dict)
        self.research = CompetitorResearcher(profile_dict)
        self.ab_test = ABVariantGenerator(profile_dict)
    
    # ============================================================
    # EVIDENCIA DE COPY PUBLICADO
    # ============================================================
    
    def analyze_published_copy(self) -> Dict[str, Any]:
        """Analiza los copys reales publicados por el tenant en Meta.

        Lee `tenants/<id>/data/meta_posts_*.json`, deduplica los posts y
        devuelve patrones verificables de hook, longitud, emojis, hashtags,
        vocabulario y cierres. No inventa ejemplos: si no hay posts, devuelve
        un resultado vacío.
        """
        posts, sources = load_posts(self.tenant_path)
        return analyze_posts(posts, sources=sources)
    
    def apply_published_copy_evidence(self) -> Dict[str, Any]:
        """Guarda la evidencia de copy publicado dentro de `brand_voice.json`."""
        evidence = self.analyze_published_copy()
        if not evidence.get("posts_analyzed"):
            return evidence

        self.profile.published_copy_evidence = evidence
        if evidence.get("sources"):
            for source in evidence["sources"]:
                if source not in self.profile.sources:
                    self.profile.sources.append(source)
        self.save_profile()
        return evidence
    
    # ============================================================
    # COPY GENERATION
    # ============================================================
    
    def generate_whatsapp_templates(
        self,
        purposes: List[str] = None,
        count_per_purpose: int = 3
    ) -> Dict[str, List[Dict]]:
        """
        Genera templates WhatsApp para múltiples propósitos.
        
        Args:
            purposes: ["CATALOG", "PROMO", "ORDER_CONFIRMATION", "SUPPORT", "WELCOME"]
            count_per_purpose: Variantes por propósito (incluye control)
        
        Returns:
            Dict[purpose] -> List[template variants]
        """
        purposes = purposes or ["CATALOG", "PROMO", "ORDER_CONFIRMATION", "SUPPORT", "WELCOME"]
        
        # Base templates por propósito
        base_templates = self._get_base_templates()
        
        results = {}
        for purpose in purposes:
            if purpose not in base_templates:
                continue
            
            base = base_templates[purpose]
            
            # Generar variantes A/B
            variants = self.ab_test.generate_variants(
                base_copy=base["body"],
                task_type="whatsapp",
                count=count_per_purpose
            )
            
            # Validar compliance cada variante
            validated = []
            for v in variants:
                compliance = self.compliance.check_whatsapp_template(
                    name=f"{self.tenant_id}_{purpose.lower()}_{v['id']}",
                    category="UTILITY",
                    body=v["copy"],
                    language="es_MX"
                )
                v["compliance"] = {
                    "passed": compliance.passed,
                    "score": compliance.score,
                    "meta_ready": compliance.meta_ready,
                    "violations": [
                        {"rule": v.rule, "severity": v.severity, "message": v.message}
                        for v in compliance.violations
                    ]
                }
                validated.append(v)
            
            results[purpose] = validated
        
        return results
    
    def _get_base_templates(self) -> Dict[str, Dict]:
        """Templates base por propósito (usando brand profile)"""
        brand = self.profile.brand_identity.name if self.profile else self.tenant_id
        opening = self.profile.messaging_patterns.opening[0] if self.profile and self.profile.messaging_patterns.opening else "¡Hola! 👋"
        closing = self.profile.messaging_patterns.closing[0] if self.profile and self.profile.messaging_patterns.closing else "¡Gracias! 😊"
        cta_soft = self.profile.messaging_patterns.cta_soft[0] if self.profile and self.profile.messaging_patterns.cta_soft else "¿Te ayudo?"
        
        return {
            "CATALOG": {
                "name": "catalogo",
                "body": f"{opening}\n\nEn {brand} tenemos lo que buscas 😊\n\n{cta_soft}\n\n{closing}"
            },
            "PROMO": {
                "name": "promocion",
                "body": f"{opening}\n\n¡Tenemos promociones especiales para ti! 🎁\n\n{cta_soft}\n\n{closing}"
            },
            "ORDER_CONFIRMATION": {
                "name": "confirmacion_pedido",
                "body": f"{opening}\n\nTu pedido ha sido confirmado ✅\n\nTe notificaremos cuando esté listo.\n\n{closing}"
            },
            "SUPPORT": {
                "name": "soporte",
                "body": f"{opening}\n\n¿En qué te podemos ayudar hoy? 😊\n\nEscribe tu duda y te respondemos.\n\n{closing}"
            },
            "WELCOME": {
                "name": "bienvenida",
                "body": f"{opening}\n\n¡Bienvenido a {brand}! 🎉\n\nSomos distribuidores oficiales con la mejor calidad.\n\n{cta_soft}\n\n{closing}"
            }
        }
    
    def generate_meta_ads(
        self,
        objective: str = "SALES",
        format_type: str = "CAROUSEL",
        count: int = 5
    ) -> List[Dict]:
        """
        Genera copy para Meta Ads.
        
        Returns:
            Lista de variantes con headline, primary_text, description, CTA
        """
        brand = self.profile.brand_identity.name if self.profile else self.tenant_id
        benefits = self.profile.brand_identity.differentiators if self.profile else []
        
        base_headlines = [
            f"{brand}: {benefits[0] if benefits else 'Calidad garantizada'} 🛡️",
            f"¿Buscas {self._get_main_benefit().lower()}? {brand} 👇",
            f"{brand} - Distribuidor oficial ✅",
            f"Tu {self._get_main_product()} ideal está en {brand} 🎯"
        ]
        
        base_primary = [
            f"En {brand} somos distribuidores oficiales con años de experiencia. "
            f"Ofrecemos {', '.join(benefits[:2]) if benefits else 'calidad y garantía'}. "
            f"¿Necesitas ayuda para elegir? Te asesoramos gratis 😊",
            f"Descubre por qué cientos de clientes eligen {brand}. "
            f"Calidad, comodidad y respaldo de marca líder. "
            f"Envío rápido y garantía de satisfacción 📦"
        ]
        
        variants = []
        
        # Generar combinaciones
        for i in range(min(count, len(base_headlines) * len(base_primary))):
            h_idx = i % len(base_headlines)
            p_idx = i // len(base_headlines)
            
            variants.append({
                "id": f"v{i}",
                "headline": base_headlines[h_idx],
                "primary_text": base_primary[p_idx],
                "description": f"{brand} - Calidad oficial",
                "cta": "SEND_MESSAGE",
            })
        
        return variants
    
    def _get_main_benefit(self) -> str:
        benefits = self.profile.brand_identity.differentiators if self.profile else []
        return benefits[0] if benefits else "calidad"
    
    def _get_main_product(self) -> str:
        return "producto"
    
    # ============================================================
    # TONE & COMPLIANCE
    # ============================================================
    
    def check_meta_ad(self, headline: str, primary_text: str) -> Dict[str, Any]:
        """Valida un copy contra políticas de Meta Ads."""
        result = self.compliance.check_meta_ad(headline, primary_text)
        return {
            'is_compliant': result.passed,
            'violations': [
                {'type': v.rule, 'severity': v.severity, 'message': v.message}
                for v in result.violations
            ]
        }
    
    def analyze_tone(self, text: str) -> Dict[str, Any]:
        """Analiza adhesión al Brand Voice."""
        analysis = self.tone.analyze(text)
        return {
            'overall': analysis.overall,
            'breakdown': analysis.breakdown,
            'feedback': analysis.feedback,
            'matches': analysis.matches,
            'suggestions': analysis.suggestions
        }
    
    # ============================================================
    # RESEARCH & A/B
    # ============================================================
    
    def research_competitors(
        self,
        competitors: List[str],
        location: str = "",
        channels: List[str] = None
    ) -> Dict:
        """Investiga competidores (requiere modelo con browsing)"""
        return self.research.research_competitors(competitors, location, channels)
    
    def get_research_prompt(self, competitor: str, location: str = "") -> str:
        """Genera prompt para modelo con browsing"""
        return self.research.generate_research_prompt(competitor, location)
    
    def analyze_competitor_copy(self, competitor: str, copy: str) -> Dict:
        return self.research.analyze_competitor_copy(copy)
    
    def generate_ab_variants(
        self,
        base_copy: str,
        task_type: str = "whatsapp",
        count: int = 4
    ) -> List[Dict]:
        """Genera variantes A/B testeables"""
        return self.ab_test.generate_variants(base_copy, task_type, count)
    
    # ============================================================
    # PROFILE MANAGEMENT
    # ============================================================
    
    def save_profile(self) -> Path:
        """Guarda perfil actual"""
        return memory.save(self.profile)
    
    def update_profile(self, updates: Dict) -> BrandVoiceProfile:
        """Actualiza perfil parcialmente"""
        profile_dict = self.profile.to_dict()
        profile_dict.update(updates)
        self.profile = BrandVoiceProfile.from_dict(profile_dict)
        self._refresh_skills()
        self.save_profile()
        return self.profile
    
    def add_example(self, good: str, bad: str):
        """Agrega ejemplos de buen/mal copy"""
        if self.profile:
            self.profile.examples.good = good
            self.profile.examples.bad = bad
            self.save_profile()
    
    # ============================================================
    # UTILITIES
    # ============================================================
    
    def get_model_for_task(self, task: str) -> str:
        """Obtiene alias de modelo para OmniRoute"""
        return get_model_alias(task)
    
    def get_generation_params(self, task: str) -> Dict:
        return get_generation_params(task)
    
    def get_status(self) -> Dict:
        """Estado del agente"""
        return {
            "tenant_id": self.tenant_id,
            "profile_exists": self.profile is not None,
            "profile_version": self.profile.version if self.profile else "N/A",
            "profile_updated": self.profile.updated if self.profile else "N/A",
            "skills_loaded": {
                "compliance": True,
                "tone": True,
                "research": True,
                "ab_test": True
            },
            "model_routing": self.model_router.list_models()
        }


def create_agent(tenant_id: str, base_path: str = "/home/universe-sent-me/growth-os") -> BrandVoiceAgent:
    """Factory function"""
    return BrandVoiceAgent(tenant_id, base_path)


# CLI usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agent.py <tenant_id> [command]")
        print(
            "Commands: status, analyze_posts, apply_posts, generate_templates, "
            "generate_ads, test_tone"
        )
        sys.exit(1)
    
    tenant_id = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "status"
    
    agent = create_agent(tenant_id)
    
    if command == "status":
        print(json.dumps(agent.get_status(), indent=2, ensure_ascii=False))
    
    elif command in ("analyze_posts", "apply_posts"):
        result = (
            agent.apply_published_copy_evidence()
            if command == "apply_posts"
            else agent.analyze_published_copy()
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "generate_templates":
        result = agent.generate_whatsapp_templates()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "generate_ads":
        result = agent.generate_meta_ads()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "test_tone":
        if len(sys.argv) < 4:
            print("Usage: python agent.py <tenant> test_tone '<text>'")
            sys.exit(1)
        text = sys.argv[3]
        result = agent.analyze_tone(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
