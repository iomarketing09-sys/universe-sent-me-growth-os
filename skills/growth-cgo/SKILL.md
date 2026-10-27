# Growth CGO Skill - Chief Growth Officer

**Descripción**: Orquestador principal del Growth OS. Coordina daily pipeline, weekly calendar, tenant onboarding, cross-tenant reporting, canon sync, y meta publishing.

---

## Capabilities

| Capability | Description |
|------------|-------------|
| `daily_pipeline` | Ejecuta pipeline diario multi-tenant (contenido → approve → publish) |
| `weekly_calendar` | Genera calendario semanal (solo native_digital/universe) |
| `tenant_onboarding` | Onboarding de nuevos tenants (physical_cro o native_digital) |
| `cross_tenant_report` | Reporte consolidado de métricas cross-tenant |
| `canon_sync` | Sincroniza con canon repo (solo universe) |
| `meta_publishing` | Coordina publicación en Meta (IG/FB) via meta-publisher |
| `verify_setup` | Verifica entorno CGO completo |

---

## Invocation Modes

| Mode | Model | Temp | Max Tokens | Use Case |
|------|-------|------|------------|----------|
| `DAILY_PIPELINE` | GPT-OSS 20B | 0.3 | 1500 | Pipeline diario multi-tenant |
| `WEEKLY_CALENDAR` | GPT-OSS 120B | 0.2 | 2000 | Calendario semanal (native_digital) |
| `TENANT_ONBOARDING` | GPT-OSS 120B | 0.4 | 3000 | Onboarding physical_cro + audit |
| `CROSS_TENANT_REPORT` | GPT-OSS 120B | 0.3 | 2500 | Métricas consolidadas |
| `CANON_SYNC` | GPT-OSS 20B | 0.1 | 1000 | Pre-check canon (Claude valida) |
| `META_PUBLISHING` | GPT-OSS 120B | 0.5 | 2000 | Publicación IG/FB |
| `BRAND_COMPLIANCE` | GPT-OSS 20B | 0.2 | 800 | Validación brand voice |

---

## Sub-Agentes Invocados

| Sub-Agent | Trigger | Purpose |
|-----------|---------|---------|
| `content-writer` | Daily pipeline | Genera copy para piezas |
| `calendar-planner` | Weekly calendar | Planifica slots semanales |
| `canon-validator` | Canon sync | Pre-check antes de Claude |
| `meta-ads-agent` | Meta publishing | Campañas + creativas |
| `brand-voice-agent` | Cualquier generación copy | Validación voice |
| `tenant-auditor` | Tenant onboarding | CRO audit (physical_cro) |

---

## Reglas de Track (Dual Track)

| Track | Tenants | Workflow | Aprobaciones |
|-------|---------|----------|--------------|
| **Native Digital** | universe | Canon → Calendar → Publish | Claude (canon) + Fernando |
| **Physical CRO** | flexi, la-cupula, firma-bordados, micas-art-deco, bam-in-a-can | CRO Audit → Funnel → Publish | tenant-auditor (GPT-OSS 120B) |

---

## Gates de Control

| Gate | Track | Quién Decide | Cuándo |
|------|-------|--------------|--------|
| Canon Approval | Native | Fernando / Claude | Antes de Programado/Publicado |
| CRO Audit Pass | Physical | tenant-auditor | Onboarding + antes de publicar |
| Meta Token Valid | Ambos | meta-publisher | Cada publish |
| Brand Compliance | Ambos | Brand Voice Agent | Cada pieza generada |
| Lead Qualified | Ambos | WhatsApp Agent | Paso 2 flujo |

---

## Comandos CLI

```bash
# Verificar setup
python3 skills/growth-cgo/scripts/verify_setup.py

# Daily pipeline (CGO)
python3 -m skills.growth_cgo --mode daily_pipeline --tenant flexi

# Weekly calendar (solo universe)
python3 -m skills.growth_cgo --mode weekly_calendar

# Tenant onboarding
python3 -m skills.growth_cgo --mode tenant_onboarding --tenant new-tenant --type physical_cro

# Cross-tenant report
python3 -m skills.growth_cgo --mode cross_tenant_report

# Canon sync (pre-check)
python3 -m skills.growth_cgo --mode canon_sync
```

---

## Archivos de Referencia

- `references/governance.md` - Gobernanza dual-track
- `references/canon_integration.md` - Puente canon repo
- `references/calendar_architecture.md` - Arquitectura calendario escalable
- `references/core_models.md` - Modelos core (Piece, Publication, Deal, etc.)
