# Gobernanza Growth OS - Dual Track

## Principio Fundamental

**Dos tracks, dos workflows, dos criterios de aprobación:**

| Track | Tenants | Gobernanza | Publicación |
|-------|---------|------------|-------------|
| **Native Digital** | universe | Canon-governed | Requiere: Claude (canon) + Fernando (estrategia) |
| **Physical CRO** | flexi, la-cupula, firma-bordados, micas-art-deco, bam-in-a-can | CRO Audit | Requiere: tenant-auditor (GPT-OSS 120B) |

---

## Canon Track (Solo universe)

### Qué es Canon
- Contenido narrativo del universo `universe-sent-me` (personajes: Universe, Wilfred, Fantasma, Elara, etc.)
- Reglas de continuidad visual y narrativa
- Monetización nativa (merch, afiliados, contenido premium)

### Flujo de Aprobación
```
Idea → Backlog → Production Queue → Approval Queue → Calendar → Publish
              ↑                    ↑
         CGO planifica        Claude valida canon
                              Fernando aprueba estrategia
```

### Gates
1. **Canon Validator** (GPT-OSS 20B) - Pre-check automático
2. **Claude** (externo) - Validación final de canon
3. **Fernando** - Aprobación estratégica/narrativa

---

## CRO Track (5 Physical Tenants)

### Qué es CRO
- Conversion Rate Optimization para negocios físicos
- Funnels de venta (no canon)
- Métricas: leads, cotizaciones, ventas, unit economics

### Flujo de Aprobación
```
Lead → CRO Audit → Funnel Config → Content → tenant-auditor → Publish
                    ↑
              tenant-auditor valida
              (GPT-OSS 120B)
```

### Gates
1. **Tenant Auditor** (GPT-OSS 120B) - Audit completa onboarding + pre-publish
2. **Meta Token Valid** - Verificación técnica antes de publish
3. **Brand Compliance** - Brand Voice Agent valida copy

---

## Separación Estricta

| Aspecto | Native Digital | Physical CRO |
|---------|---------------|--------------|
| Calendario | Semanal (calendar-planner) | Diario (Plan Diario) |
| Aprobación canon | SÍ (Claude) | NO |
| Aprobación CRO | NO | SÍ (tenant-auditor) |
| Monetización | Nativa (merch, afiliados) | Ventas directas, B2B |
| WhatsApp | Soporte comunidad | Conversión 5 pasos + CRM |
| Meta Ads | Brand awareness | Performance (ventas) |

---

## Roles

| Rol | Responsabilidad | Track |
|-----|-----------------|-------|
| **CGO (Orquestador)** | Daily pipeline, calendar, onboarding, reporting | Ambos |
| **Brand Voice Agent** | Copywriting, compliance voz | Ambos |
| **Meta Ads Agent** | Campañas, creativas, budget | Ambos |
| **WhatsApp Agent** | Conversión, CRM | Ambos |
| **Content Writer** | Generación piezas | Native |
| **Calendar Planner** | Slots semanales | Native |
| **Canon Validator** | Pre-check canon | Native |
| **Tenant Auditor** | CRO audit | Physical |
| **Claude (externo)** | Canon approval final | Native |
| **Fernando (humano)** | Estrategia, canon, claims | Ambos |

---

*Actualizado: 15 Octubre 2026*
