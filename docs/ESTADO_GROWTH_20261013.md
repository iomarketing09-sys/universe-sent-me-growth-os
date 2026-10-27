# Estado Growth OS - 13 Octubre 2026

## Snapshot Actual

### ✅ Operativo (Green)
- **Meta Graph API**: 6/6 tenants syncing (followers, views, engagement, video, reactions)
- **Core package**: Models, enums, CSV storage, repositories — all tests pass
- **Brand Voice Agent**: Copywriting funcional
- **Meta Ads Agent**: Planner + creatives + budget ready
- **WhatsApp Agent**: 5-step conversion + persistent CRM (fixed)
- **Model Router (OmniRoute)**: 9 modelos gratuitos (Groq, NVIDIA, Cloudflare, Gemini, Morph)

### 🟡 Parcial / En Progreso
- **Google Business Profile**: 4/6 tenants configurados, solo `firma-bordados` con datos reales (fallback manual)
- **Search Console (GSC)**: 0/6 — requiere sitios web verificados
- **Bing Webmaster**: 0/6 — requiere sitios verificados + API keys
- **Directory Scraper**: 1/6 (`la-cupula` via EspecialEvento)

### 🔴 Bloqueado (Dependencias Externas)
| Blocker | Tenants Afectados | Owner |
|---------|------------------|-------|
| GSC site verification | la-cupula, flexi, firma-bordados, micas-art-deco | Cliente |
| GBP OAuth refresh tokens | la-cupula, flexi | Cliente (cuenta owner GBP) |
| Meta Ads BM access | Todos los 6 | Cliente (agregar usuario a BM) |
| Bing API keys | Todos los 6 | Cliente |

---

## Referencia Rápida de Tenants

| Tenant | Tipo | Meta Page ID | GBP Place ID | Config Clave |
|--------|------|--------------|--------------|--------------|
| **universe** | native_digital | 1036844829507460 | N/A | Canon-gobernado, `canon_bridge` seteado |
| **la-cupula** | physical_cro | 112400694016638 | ChIJ3_plrReNX4YR... | EspecialEvento directory |
| **flexi** | physical_cro | 361528203707668 | ChIJJWR9SOGLX4YR... | **ACTIVO**, sitio Linktree |
| **firma-bordados** | physical_cro | 1789755574420276 | ChIJGbgbJEaNX4YR... | Datos GBP reales (4.7★, 127 reviews) |
| **micas-art-deco** | physical_cro | 349027898519180 | ChIJr_LyMLCLX4YR... | Solo config |
| **bam-in-a-can** | physical_cro | 772205095974946 | ❌ | Solo config |

**Tipos de Tenant**:
- `native_digital`: Canon-gobernado, monetización nativa, calendar + publish flow
- `physical_cro`: Reglas CRO, funnels, sin canon, auditoría requerida antes de publicar

---

## Comandos de Desarrollo

```bash
# Core tests
python3 -m pytest core/growthos-core/tests/ -v

# Integration tests
python3 -m pytest tests/ -v --tb=short

# Sync tenant específico
python3 scripts/sync_all.py --tenant flexi --quiet

# Verificar setup CGO
python3 skills/growth-cgo/scripts/verify_setup.py

# Validar token Meta
python3 inspect_meta_token.py
```

---

*Actualizado: 13 Octubre 2026*  
*Próxima revisión: 20 Octubre 2026*
