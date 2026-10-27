# Arquitectura Calendario Escalable

## Principio: Calendario Semanal Escalable

El calendario no es un grid fijo, es un **sistema de slots parametrizables** que escala con el número de tenants y piezas.

---

## Estructura de Datos

### Slot Semanal
```python
class WeeklySlot(BaseModel):
    week_id: str              # W01_2026 (año-semana ISO)
    day: int                  # 0=Lunes ... 6=Domingo
    slot_index: int           # 0, 1, 2... (múltiples slots por día)
    tenant_id: str            # universe, flexi, etc.
    piece_id: Optional[str]   # CNT-xxxx si asignado
    track: str                # native_digital | physical_cro
    status: SlotStatus        # EMPTY | RESERVED | PROGRAMMED | PUBLISHED
    platform: List[Plataforma]  # [INSTAGRAM, FACEBOOK, REELS, STORIES]
```

### Estados de Slot
```
EMPTY → RESERVED (pieza asignada) → PROGRAMMED (en Meta scheduler) → PUBLISHED
```

---

## Reglas de Asignación

### Native Digital (universe)
- **Calendario semanal completo** (7 días × N slots)
- Slots reservados por `calendar-planner` basado en:
  - Reuse Queue (evergreen cada 30 días)
  - Production Queue (assets listos)
  - Approval Queue (pendientes Claude/Fernando)
  - Hipótesis Growth OS (slots experimentales)

### Physical CRO (5 tenants)
- **NO hay calendario semanal**
- Usan **Plan Diario** (publicación reactiva basada en leads/funnel)
- `tenant-auditor` valida antes de cada publicación
- Meta Ads maneja scheduling nativo (no growth-os scheduler)

---

## Capacidad por Track

| Track | Slots/Semana | Frecuencia | Plataformas |
|-------|-------------|------------|-------------|
| Native Digital | 7-14 (1-2/día) | Semanal fija | IG Feed, Reels, Stories, FB |
| Physical CRO | Variable (0-7) | On-demand | IG Feed, FB, WhatsApp |

---

## Integración con Meta Scheduler

```
GrowthOS Calendar (slots) 
    │
    ▼
python3 scripts/sync_all.py --tenant universe
    │
    ▼
growth/ig_scheduler.py (daemon o --once)
    │
    ▼
Meta Graph API → Scheduled Posts
```

---

## Escalabilidad

### Añadir Tenant Native Digital
1. Registrar en `tenants/{nuevo}/config.json` con `tenant_type: native_digital`
2. `calendar-planner` incluye automáticamente en weekly calendar
3. Slots disponibles = (slots base) / (tenants native_digital)

### Añadir Tenant Physical CRO
1. Registrar con `tenant_type: physical_cro`
2. Ejecutar `tenant-onboarding` (CRO audit)
3. Configurar funnels en `config.json`
4. NO se añade al calendario semanal

---

## Comandos

```bash
# Generar calendario semanal (solo universe)
python3 scripts/generate_weekly_calendar.py --week W01_2026

# Ver slots disponibles
python3 scripts/sync_all.py --list

# Publicar slot programado
python3 growth/ig_scheduler.py --tenant universe --once
```

---

*Actualizado: 15 Octubre 2026*
