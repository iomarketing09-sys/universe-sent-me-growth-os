# Growth OS - Flujo Completo y Estado por Componente

**Fecha:** 15 Octubre 2026  
**Versión:** 2.0 (Corregido: Canon solo para tenant universe)  
**Estado General:** 🟢 Núcleo Operativo | 🟡 Datos Reales Parciales | 🔴 Bloqueantes Externos

---

## 🏗️ ARQUITECTURA GENERAL - DUAL TRACK

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GROWTH OS - ARQUITECTURA DUAL TRACK                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                         TENANTS (6)                                  │  │
│   │  ┌─────────────────────┐    ┌──────────────────────────────────┐   │  │
│   │  │  NATIVE_DIGITAL (1) │    │  PHYSICAL_CRO (5)                │   │  │
│   │  │  • universe         │    │  • flexi                         │   │  │
│   │  │  • canon_governed   │    │  • la-cupula                     │   │  │
│   │  │  • Canon workflow   │    │  • firma-bordados                │   │  │
│   │  │  • Monetización     │    │  • micas-art-deco                │   │  │
│   │  │    nativa           │    │  • bam-in-a-can                  │   │  │
│   │  └─────────────────────┘    │  • CRO Audit workflow            │   │  │
│   │                             │  • Funnels, no canon             │   │  │
│   │                             └──────────────────────────────────┘   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    SYNC_ALL.PY (Orquestador)                        │  │
│   │  Meta Graph API (6/6) │ GBP (4/6 config, 1/6 real) │ GSC/Bing (0/6) │  │
│   │  Directory Scraper (1/6)                                               │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                  MODEL ROUTER (OmniRoute - 9 modelos)               │  │
│   │  GPT-OSS 20B/120B (Groq) │ Llama Vision (NVIDIA) │ Gemini │ Morph │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐           │
│         ▼                          ▼                          ▼           │
│ ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐   │
│ │  BRAND VOICE    │      │  META ADS       │      │  WHATSAPP       │   │
│ │  AGENT          │      │  AGENT          │      │  AGENT          │   │
│ │  (GPT-OSS 20B)  │      │  (GPT-OSS 120B) │      │  (Morph V3)     │   │
│ └─────────────────┘      └─────────────────┘      └─────────────────┘   │
│         │                      │                      │                  │
│         └──────────────────────┼──────────────────────┘                  │
│                                ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    CGO ORCHESTRATOR                                 │  │
│   │  Daily Pipeline · Weekly Calendar · Tenant Onboarding              │  │
│   │  Cross-tenant Reports · Canon Sync · Meta Publishing               │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 ESTRUCTURA DEL REPOSITORIO

```
growth-os/
├── core/growthos-core/          # Core Python package (✅ stable)
│   ├── core/                    # Domain models & enums
│   │   ├── enums.py             # All enumerated types (EstadoPieza, Plataforma, etc.)
│   │   └── models.py            # Pydantic v2 models (Piece, Publication, Experiment, etc.)
│   ├── storage/                 # Persistence layer
│   │   ├── csv_adapter.py       # CSV-based storage with enum handling
│   │   └── repositories.py      # Repository pattern (account-scoped isolation)
│   ├── integrations/            # External APIs (✅ Meta / 🟡 Google / 🟡 Directories)
│   │   ├── meta_graph.py        # Meta Graph API v20 — 6/6 tenants operational
│   │   ├── google_business.py   # GBP + GSC + Bing unified (fallback config.json)
│   │   └── directory_scraper.py # Web directories + Meta API fallback
│   ├── scripts/                 # Utility scripts
│   ├── tests/                   # Core package test suite (9/9 passing)
│   └── data/                    # CSV data files (account-scoped)
├── GrowthOS/                    # Operational docs & queues (🟢 active)
│   ├── 00_01_Changelog_GrowthOS.md
│   ├── 00_Índice.md
│   ├── 01_00_Arquitectura_Calendario_Escalable.md
│   ├── 01_01_Calendario_Semanal.md          # Weekly calendar (W01, agosto 2026)
│   ├── 01_02_Content_Backlog.md             # Backlog v3.2 (updated 2026-08-23)
│   ├── 01_03_Reuse_Queue.md
│   ├── 01_04_Production_Queue.md            # Pipeline with Meta-verified assets
│   ├── 01_05_Approval_Queue.md              # Bottleneck: pending Claude/Fernando
│   ├── Integracion_Growth_OS.md             # Canon bridge (last sync 2026-08-23, commit 1daaad5)
│   ├── Canon_Contradictions_Report.md
│   ├── Content_Inventory.csv                # Master identity source
│   └── Content_Inventory_CANONICAL.csv      # Canonical version
├── Studio_Governance.md         # Governance summary (authoritative in canon repo)
├── skills/                      # Codex skills
│   └── growth-cgo/              # Chief Growth Officer agent (✅ primary)
│       ├── SKILL.md             # Complete operational instructions
│       ├── agents/openai.yaml   # UI metadata & 8 invocation modes
│       ├── scripts/verify_setup.py
│       └── references/          # governance.md, canon_integration.md, calendar_architecture.md, core_models.md
├── tenants/                     # Multi-tenant configurations (6 active)
│   ├── universe/                # native_digital (canon-governed)
│   ├── la-cupula/               # physical_cro (restaurante/eventos)
│   ├── flexi/                   # physical_cro (zapatería) — **ACTIVE TENANT**
│   ├── firma-bordados/          # physical_cro (GBP real sept 2026)
│   ├── micas-art-deco/          # physical_cro (arte/decoración)
│   └── bam-in-a-can/            # physical_cro (bebidas)
├── agents/                      # Specialized agents (3 operational)
│   ├── brand_voice_agent/       # Copywriting
│   ├── meta_ads_agent/          # Campaign planner + creatives
│   └── whatsapp_agent/          # Conversion flow 5-step + CRM (✅ fixed)
├── tools/                       # Operational tooling
│   └── tenant_auditor.py        # CRO audit for physical tenants
├── scripts/                     # Orchestration
│   ├── sync_all.py              # Unified daily sync (Meta + Google + Directories)
│   ├── sync_google.py
│   └── sync_metrics.py
├── tests/                       # Integration test suite (91 pass, 38 fail legacy)
├── Operations/                  # Research, metrics, audit artifacts
│   ├── Production/              # Production briefs, assets, analysis
│   └── Research/                # Performance reports, inventories
├── docs/                        # Living documentation
│   ├── GROWTH_OS_FLUJO_COMPLETO.md      # This architecture overview
│   ├── ESTADO_GROWTH_20261013.md        # Current status snapshot
│   ├── CHANGELOG_20261013.md            # v1.0.0 multi-tenant base
│   ├── PENDIENTES_GROWTH_20261012.md    # Action items
│   ├── WHATSAPP_AGENT_FLOW_FIX.md
│   ├── META_ADS_AGENT_SUMMARY_20261014.md
│   └── AUTOMATION_CLASSIFICATION.md
├── .active_tenant               # Current tenant: "flexi"
├── .env                         # Global secrets (Meta tokens)
└── .env.example                 # Template
```

**Key Principle**: This repo (`universe-sent-me-growth-os`) = **operational workspace** (CGO read/write). Canon repo (`universe-sent-me-1`) = **read-only** for CGO; Claude guards it. Bridge: `GrowthOS/Integracion_Growth_OS.md`.

---

## Current State Snapshot (2026-10-14)

### ✅ Operational (Green)
- **Meta Graph API**: 6/6 tenants syncing (followers, views, engagement, video, reactions)
- **Core package**: Models, enums, CSV storage, repositories — all tests pass
- **Brand Voice Agent**: Copywriting functional
- **Meta Ads Agent**: Planner + creatives + budget ready
- **Monetization Agent**: Ledger, umbral y conciliación read-only; integrado al CGO
- **WhatsApp Agent**: 5-step conversion + persistent CRM (fixed)
- **Model Router (OmniRoute)**: 9 free models (Groq, NVIDIA, Cloudflare, Gemini, Morph)

### 🟡 Partial / In Progress
- **Google Business Profile**: 4/6 tenants configured, only `firma-bordados` has real data (manual fallback)
- **Search Console (GSC)**: 0/6 — requires verified websites
- **Bing Webmaster**: 0/6 — requires verified sites + API keys
- **Directory Scraper**: 1/6 (`la-cupula` via EspecialEvento)

### 🔴 Blocked (External Dependencies)
| Blocker | Tenants Affected | Owner |
|---------|-----------------|-------|
| GSC site verification | la-cupula, flexi, firma-bordados, micas-art-deco | Client |
| GBP OAuth refresh tokens | la-cupula, flexi | Client (GBP owner account) |
| Meta Ads BM access | All 6 | Client (add user to BM) |
| Bing API keys | All 6 | Client |

---

## Build, Test, and Development Commands

| Command | Purpose |
|---------|---------|
| `python3 -m pytest core/growthos-core/tests/ -v` | Core unit tests (9/9) |
| `python3 -m pytest tests/ -v --tb=short` | Full integration suite |
| `python3 scripts/sync_all.py --tenant flexi --quiet` | Sync single tenant (Meta + Google + Directories) |
| `python3 scripts/sync_all.py --list` | List all tenants with features |
| `python3 scripts/sync_all.py --tenant firma-bordados --skip-google` | Meta-only sync |
| `python3 -c "from growthos.core import models; print('OK')"` | Verify core imports |
| `python3 skills/growth-cgo/scripts/verify_setup.py` | Verify CGO environment |
| `python3 inspect_meta_token.py` | Validate Meta token |

---

## Tenant Quick Reference

| Tenant | Type | Meta Page ID | GBP Place ID | Key Config |
|--------|------|--------------|--------------|------------|
| **universe** | native_digital | 1036844829507460 | N/A | Canon-governed, `canon_bridge` set |
| **la-cupula** | physical_cro | 112400694016638 | ChIJ3_plrReNX4YR... | EspecialEvento directory |
| **flexi** | physical_cro | 361528203707668 | ChIJJWR9SOGLX4YR... | **ACTIVE**, Linktree site |
| **firma-bordados** | physical_cro | 1789755574420276 | ChIJGbgbJEaNX4YR... | Real GBP data (4.7★, 127 reviews) |
| **micas-art-deco** | physical_cro | 349027898519180 | ChIJr_LyMLCLX4YR... | Config only |
| **bam-in-a-can** | physical_cro | 772205095974946 | ❌ | Config only |

**Tenant Types**:
- `native_digital`: Canon-governed, monetización nativa, calendar + publish flow
- `physical_cro`: CRO rules, funnels, no canon, audit required before publishing

---

## Coding Style & Naming Conventions

- **Language**: Python 3.10+ with type hints everywhere
- **Formatting**: 4-space indentation, 100-char line limit
- **Imports**: Absolute from `growthos.core` (package root in `core/growthos-core/`)
- **Enums**: PascalCase names, UPPER_SNAKE_CASE values (`EstadoPieza.IDEA`)
- **Models**: Pydantic v2, PascalCase classes, snake_case fields
- **Repositories**: `ClassNameRepository` pattern, snake_case methods
- **Files**: snake_case Python modules, PascalCase markdown docs
- **Commits**: `type(scope): description` (feat, fix, chore, docs, test, refactor)

---

## Test Commands

```bash
# Core tests
python3 -m pytest core/growthos-core/tests/ -v

# Integration tests
python3 -m pytest tests/ -v --tb=short

# Specific tenant tests
python3 -m pytest tests/test_asset_validator.py -v
```
